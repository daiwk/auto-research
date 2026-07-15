from __future__ import annotations

import random
import time
from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import require_backend


@dataclass(frozen=True)
class UniVAConfig:
    dimensions: int = 48
    heads: int = 4
    sequence_length: int = 20
    experts: int = 4
    top_experts: int = 2
    recursive_rounds: int = 2
    batch_size: int = 32
    steps: int = 120
    learning_rate: float = 8e-4
    rl_candidates: int = 8
    value_weight: float = 0.35
    clip_epsilon: float = 0.2


def build_model(item_count: int, code_sizes: tuple[int, ...], config: UniVAConfig):
    torch, nn = require_backend()
    head_dim = config.dimensions // config.heads

    class HSTULayer(nn.Module):
        def __init__(self):
            super().__init__()
            self.uvqk = nn.Linear(config.dimensions, 4 * config.dimensions, bias=False)
            self.output = nn.Linear(config.dimensions, config.dimensions)

        def forward(self, hidden):
            normalized = torch.nn.functional.layer_norm(hidden, (config.dimensions,))
            u, v, q, k = torch.nn.functional.silu(self.uvqk(normalized)).chunk(4, -1)
            q = q.view(*q.shape[:2], config.heads, head_dim)
            k = k.view(*k.shape[:2], config.heads, head_dim)
            v = v.view(*v.shape[:2], config.heads, head_dim)
            scores = torch.einsum("bthd,bshd->bhts", q, k)
            positions = torch.arange(hidden.shape[1], device=hidden.device)
            causal = positions[:, None] >= positions[None, :]
            weights = torch.nn.functional.silu(scores) * causal[None, None] / hidden.shape[1]
            aggregate = torch.einsum("bhts,bshd->bthd", weights, v).flatten(2)
            return hidden + self.output(u * torch.nn.functional.layer_norm(aggregate, (config.dimensions,)))

    class SparseMoE(nn.Module):
        def __init__(self):
            super().__init__()
            self.router = nn.Linear(config.dimensions, config.experts)
            self.shared = _expert(nn, config.dimensions)
            self.routed = nn.ModuleList(
                [_expert(nn, config.dimensions) for _ in range(config.experts)]
            )

        def forward(self, hidden):
            gates = torch.softmax(self.router(hidden), -1)
            top_values, top_indices = torch.topk(gates, config.top_experts, dim=-1)
            routed = torch.stack([expert(hidden) for expert in self.routed], dim=-2)
            selected = routed.gather(
                -2,
                top_indices.unsqueeze(-1).expand(*top_indices.shape, config.dimensions),
            )
            return self.shared(hidden) + (selected * top_values.unsqueeze(-1)).sum(-2)

    class DecoderBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.cross = nn.MultiheadAttention(config.dimensions, config.heads, batch_first=True)
            self.self_attention = nn.MultiheadAttention(config.dimensions, config.heads, batch_first=True)
            self.moe = SparseMoE()
            self.norms = nn.ModuleList([nn.LayerNorm(config.dimensions) for _ in range(3)])

        def forward(self, hidden, memory):
            cross, _ = self.cross(hidden, memory, memory, need_weights=False)
            hidden = self.norms[0](hidden + cross)
            length = hidden.shape[1]
            causal = torch.triu(torch.ones(length, length, device=hidden.device, dtype=torch.bool), diagonal=1)
            self_value, _ = self.self_attention(hidden, hidden, hidden, attn_mask=causal, need_weights=False)
            hidden = self.norms[1](hidden + self_value)
            return self.norms[2](hidden + self.moe(hidden))

    class UniVAModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.history_position = nn.Embedding(config.sequence_length, config.dimensions)
            self.hstu = HSTULayer()
            self.code_embeddings = nn.ModuleList(
                [nn.Embedding(size, config.dimensions) for size in code_sizes]
            )
            self.bos = nn.Parameter(torch.zeros(config.dimensions))
            self.decoder_position = nn.Embedding(len(code_sizes), config.dimensions)
            self.input_block = DecoderBlock()
            self.middle_block = DecoderBlock()
            self.output_block = DecoderBlock()
            self.generation_heads = nn.ModuleList(
                [nn.Linear(config.dimensions, size) for size in code_sizes]
            )
            self.value_heads = nn.ModuleList(
                [nn.Linear(config.dimensions, size) for size in code_sizes]
            )
            self.code_sizes = code_sizes

        def encode(self, histories):
            positions = torch.arange(histories.shape[1], device=histories.device)
            return self.hstu(self.item(histories) + self.history_position(positions))

        def decode(self, memory, codes):
            batch = codes.shape[0]
            previous = [self.bos.expand(batch, 1, -1)]
            for level in range(1, len(self.code_sizes)):
                previous.append(self.code_embeddings[level - 1](codes[:, level - 1]).unsqueeze(1))
            hidden = torch.cat(previous, 1) + self.decoder_position.weight.unsqueeze(0)
            hidden = self.input_block(hidden, memory)
            for _ in range(config.recursive_rounds):
                hidden = self.middle_block(hidden, memory)
            hidden = self.output_block(hidden, memory)
            generation = [head(hidden[:, level]) for level, head in enumerate(self.generation_heads)]
            value = [head(hidden[:, level]) for level, head in enumerate(self.value_heads)]
            return generation, value

        def forward(self, histories, codes):
            return self.decode(self.encode(histories), codes)

    return UniVAModel()


def train_model(codes, ecpm, item_count, rows, config, seed, use_rl):
    torch, _ = require_backend()
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    code_sizes = tuple(int(codes[:, level].max()) + 1 for level in range(codes.shape[1]))
    model = build_model(item_count, code_sizes, config).to(device)
    code_tensor = torch.tensor(codes, dtype=torch.long, device=device)
    value_tensor = torch.tensor(ecpm, dtype=torch.float32, device=device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    old_policy = deepcopy(model).eval() if use_rl else None
    if old_policy is not None:
        for parameter in old_policy.parameters():
            parameter.requires_grad_(False)
    rng = random.Random(seed)
    losses: list[float] = []
    sl_losses: list[float] = []
    rl_losses: list[float] = []
    value_losses: list[float] = []
    started = time.perf_counter()
    model.train()
    warmup = config.steps // 3
    for step in range(config.steps):
        if old_policy is not None and step == warmup:
            old_policy.load_state_dict(model.state_dict())
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = _histories([row[0] for row in batch], config.sequence_length, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        target_codes = code_tensor[targets]
        generation, _ = model(histories, target_codes)
        sl_loss = sum(
            torch.nn.functional.cross_entropy(generation[level], target_codes[:, level])
            for level in range(codes.shape[1])
        ) / codes.shape[1]
        if use_rl and step >= warmup and (step - warmup) % 2:
            loss, policy_loss, value_loss = _rl_loss(
                model,
                old_policy,
                histories,
                targets,
                code_tensor,
                value_tensor,
                config,
                torch,
            )
            rl_losses.append(float(policy_loss.detach().cpu()))
            value_losses.append(float(value_loss.detach().cpu()))
        else:
            loss = sl_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        if (
            old_policy is not None
            and step >= warmup
            and (step - warmup) % 2
            and len(rl_losses) % 4 == 0
        ):
            old_policy.load_state_dict(model.state_dict())
        losses.append(float(loss.detach().cpu()))
        sl_losses.append(float(sl_loss.detach().cpu()))
    window = min(10, len(losses))
    return model, {
        "initial_loss": float(np.mean(losses[:window])),
        "final_loss": float(np.mean(losses[-window:])),
        "initial_sl_loss": float(np.mean(sl_losses[:window])),
        "final_sl_loss": float(np.mean(sl_losses[-window:])),
        "mean_policy_loss": float(np.mean(rl_losses)) if rl_losses else 0.0,
        "mean_value_loss": float(np.mean(value_losses)) if value_losses else 0.0,
        "rl_updates": len(rl_losses),
        "seconds": time.perf_counter() - started,
        "device": device.type,
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
    }


def score_items(model, history, codes, fused, config, chunk=512):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    code_tensor = torch.tensor(codes, dtype=torch.long, device=device)
    histories = _histories([history], config.sequence_length, device, torch)
    model.eval()
    scores = []
    with torch.inference_mode():
        memory = model.encode(histories)
        for start in range(0, len(codes), chunk):
            candidates = code_tensor[start : start + chunk]
            expanded = memory.expand(len(candidates), -1, -1)
            generation, value = model.decode(expanded, candidates)
            score = torch.zeros(len(candidates), device=device)
            for level in range(candidates.shape[1]):
                logits = generation[level] + (value[level] if fused else 0)
                score += torch.log_softmax(logits, -1).gather(
                    1, candidates[:, level : level + 1]
                ).squeeze(1)
            scores.append(score.cpu().numpy())
    return np.concatenate(scores)


def beam_search(model, history, codes, beam_width, fused, constrained, config):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    histories = _histories([history], config.sequence_length, device, torch)
    valid_items = [item for item in range(len(codes)) if item not in set(history)]
    paths: dict[tuple[int, ...], list[int]] = {}
    for item in valid_items:
        paths.setdefault(tuple(int(value) for value in codes[item]), []).append(item)
    prefixes = {()}
    for depth in range(codes.shape[1]):
        prefixes = {path[: depth + 1] for path in paths}
        if depth == 0:
            allowed = {(): sorted({prefix[0] for prefix in prefixes})}
        else:
            allowed = {}
            for prefix in prefixes:
                allowed.setdefault(prefix[:-1], []).append(prefix[-1])
        if depth == 0:
            beams = [((), 0.0)]
        next_beams = []
        prefix_codes = np.zeros((len(beams), codes.shape[1]), dtype=np.int64)
        for row, (prefix, _) in enumerate(beams):
            prefix_codes[row, : len(prefix)] = prefix
        with torch.inference_mode():
            memory = model.encode(histories).expand(len(beams), -1, -1)
            generation, value = model.decode(
                memory, torch.tensor(prefix_codes, dtype=torch.long, device=device)
            )
            logits = generation[depth] + (value[depth] if fused else 0)
            logp = torch.log_softmax(logits, -1).cpu().numpy()
        for row, (prefix, score) in enumerate(beams):
            tokens = allowed.get(prefix, ()) if constrained else range(logp.shape[1])
            for token in tokens:
                next_beams.append((prefix + (int(token),), score + float(logp[row, token])))
        beams = sorted(next_beams, key=lambda entry: entry[1], reverse=True)[:beam_width]
    valid = [entry for entry in beams if entry[0] in paths]
    items = [paths[entry[0]][0] for entry in valid]
    return {"beam_paths": len(beams), "valid_paths": len(valid), "items": items}


def _rl_loss(model, old_policy, histories, targets, codes, ecpm, config, torch):
    batch = histories.shape[0]
    random_items = torch.randint(0, len(codes), (batch, config.rl_candidates - 1), device=histories.device)
    candidates = torch.cat((targets[:, None], random_items), 1)
    candidate_codes = codes[candidates]
    flat_codes = candidate_codes.flatten(0, 1)
    with torch.no_grad():
        memory = old_policy.encode(histories)
        expanded_memory = memory[:, None].expand(
            -1, config.rl_candidates, -1, -1
        ).flatten(0, 1)
        old_generation, old_values = old_policy.decode(expanded_memory, flat_codes)
    old_token_logp = []
    path_logp = torch.zeros(batch * config.rl_candidates, device=histories.device)
    for level in range(flat_codes.shape[1]):
        token_logp = torch.log_softmax(
            old_generation[level] + old_values[level], -1
        ).gather(1, flat_codes[:, level : level + 1]).squeeze(1)
        old_token_logp.append(token_logp.view(batch, config.rl_candidates))
        path_logp += token_logp
    path_logp = path_logp.view(batch, config.rl_candidates)
    sampled = torch.distributions.Categorical(logits=path_logp).sample()
    chosen_items = candidates.gather(1, sampled[:, None]).squeeze(1)
    rewards = ecpm[candidates]
    normalized = (rewards - rewards.mean(1, keepdim=True)) / rewards.std(1, keepdim=True).clamp_min(1e-4)
    chosen_reward = normalized.gather(1, sampled[:, None]).squeeze(1)
    selected_codes = codes[chosen_items]
    selected_generation, selected_values = model(histories, selected_codes)
    policy_terms, value_terms = [], []
    for level in range(selected_codes.shape[1]):
        fused_logits = selected_generation[level] + selected_values[level]
        current = torch.log_softmax(fused_logits, -1).gather(
            1, selected_codes[:, level : level + 1]
        ).squeeze(1)
        old = old_token_logp[level].gather(1, sampled[:, None]).squeeze(1)
        predicted = selected_values[level].gather(
            1, selected_codes[:, level : level + 1]
        ).squeeze(1)
        advantage = chosen_reward - predicted.detach()
        ratio = torch.exp(current - old)
        clipped = ratio.clamp(1 - config.clip_epsilon, 1 + config.clip_epsilon)
        policy_terms.append(-torch.min(ratio * advantage, clipped * advantage).mean())
        value_terms.append(torch.nn.functional.mse_loss(predicted, chosen_reward))
    policy_loss = torch.stack(policy_terms).mean()
    value_loss = torch.stack(value_terms).mean()
    return policy_loss + config.value_weight * value_loss, policy_loss, value_loss


def _histories(histories, length, device, torch):
    rows = []
    for history in histories:
        recent = tuple(history[-length:])
        pad = recent[0] if recent else 0
        rows.append((pad,) * (length - len(recent)) + recent)
    return torch.tensor(rows, dtype=torch.long, device=device)


def _expert(nn, dimensions: int):
    return nn.Sequential(
        nn.Linear(dimensions, 2 * dimensions),
        nn.SiLU(),
        nn.Linear(2 * dimensions, dimensions),
    )
