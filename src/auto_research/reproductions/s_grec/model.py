from __future__ import annotations

from auto_research.runtime import device_for

import copy
import random
import time
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import require_backend
from .psj import semantic_rewards


@dataclass(frozen=True)
class GeneratorConfig:
    dimensions: int = 64
    sequence_length: int = 20
    batch_size: int = 32
    group_size: int = 16
    learning_rate: float = 8e-4
    clip_epsilon: float = 0.2
    semantic_sampling_ratio: float = 0.05


def build_generator(item_count: int, codes: np.ndarray, config: GeneratorConfig):
    torch, nn = require_backend()
    code_sizes = tuple(int(codes[:, level].max()) + 1 for level in range(codes.shape[1]))

    class SIDGenerator(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.history_position = nn.Embedding(config.sequence_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions,
                4,
                2 * config.dimensions,
                dropout=0.0,
                batch_first=True,
                norm_first=True,
            )
            self.history_encoder = nn.TransformerEncoder(layer, 2)
            self.code_embeddings = nn.ModuleList(
                [nn.Embedding(size, config.dimensions) for size in code_sizes]
            )
            self.decoder = nn.GRUCell(config.dimensions, config.dimensions)
            self.heads = nn.ModuleList(
                [nn.Linear(config.dimensions, size) for size in code_sizes]
            )

        def encode(self, histories):
            positions = torch.arange(histories.shape[1], device=histories.device)
            hidden = self.item(histories) + self.history_position(positions)
            encoded = self.history_encoder(hidden)
            mask = histories.ne(0).float().unsqueeze(-1)
            return (encoded * mask).sum(1) / mask.sum(1).clamp_min(1)

        def log_probs(self, histories, candidate_codes):
            hidden = self.encode(histories)
            if candidate_codes.ndim == 3:
                batch, candidates, levels = candidate_codes.shape
                hidden = hidden[:, None].expand(-1, candidates, -1).reshape(
                    batch * candidates, -1
                )
                candidate_codes = candidate_codes.reshape(batch * candidates, levels)
            else:
                candidates = None
            logp = torch.zeros(len(candidate_codes), device=candidate_codes.device)
            for level, head in enumerate(self.heads):
                logits = torch.log_softmax(head(hidden), -1)
                token = candidate_codes[:, level]
                logp += logits.gather(1, token[:, None]).squeeze(1)
                hidden = self.decoder(self.code_embeddings[level](token), hidden)
            if candidates is not None:
                logp = logp.view(batch, candidates)
            return logp

    return SIDGenerator()


def train_sft(data, steps: int, config: GeneratorConfig, seed: int):
    torch, _ = require_backend()
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_generator(len(data.codes), data.codes, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    code_tensor = torch.tensor(data.codes, dtype=torch.long, device=device)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    model.train()
    for _ in range(steps):
        rows = [data.train[rng.randrange(len(data.train))] for _ in range(config.batch_size)]
        histories = _histories([row.history for row in rows], config, device, torch)
        targets = torch.tensor([row.target for row in rows], device=device)
        loss = -model.log_probs(histories, code_tensor[targets]).mean() / data.codes.shape[1]
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    window = min(10, len(losses))
    return model, {
        "steps": steps,
        "initial_loss": float(np.mean(losses[:window])),
        "final_loss": float(np.mean(losses[-window:])),
        "seconds": time.perf_counter() - started,
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def train_policy(base_model, data, judge, steps, mode, config, seed):
    torch, _ = require_backend()
    model = copy.deepcopy(base_model)
    device = next(model.parameters()).device
    if mode == "business":
        return model, {
            "mode": mode,
            "steps": 0,
            "semantic_sampling_ratio": config.semantic_sampling_ratio,
            "semantic_queries": 0,
            "mean_loss": 0.0,
            "mean_business_reward": 0.0,
            "clip_fraction": 0.0,
            "directional_consistency": 0.0,
            "mean_semantic_coefficient": 0.0,
            "semantic_bound_violations": 0,
            "seconds": 0.0,
            "note": "MiniOneRec-style SFT checkpoint; no semantic policy optimization",
        }
    code_tensor = torch.tensor(data.codes, dtype=torch.long, device=device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-5)
    rng = random.Random(seed)
    np_rng = np.random.default_rng(seed)
    losses, rewards, clips, lambdas = [], [], [], []
    semantic_queries = 0
    aligned = compared = bound_violations = 0
    started = time.perf_counter()
    model.train()
    for _ in range(steps):
        row = data.train[rng.randrange(len(data.train))]
        candidates = _candidate_group(row, data, config.group_size, np_rng)
        history = _histories([row.history], config, device, torch)
        candidate_codes = code_tensor[candidates].unsqueeze(0)
        with torch.no_grad():
            old_logp = model.log_probs(history, candidate_codes)[0]
        business = torch.zeros(config.group_size, device=device)
        business[0] = 1.0
        business_advantage = _standardize(business, torch)
        use_semantic = mode != "business" and rng.random() < config.semantic_sampling_ratio
        if use_semantic:
            semantic_queries += 1
            semantic = torch.tensor(
                semantic_rewards(judge, data, row.history, candidates),
                dtype=torch.float32,
                device=device,
            )
            semantic_advantage = _standardize(semantic, torch)
            compared += len(candidates)
            consistent = torch.sign(business_advantage) == torch.sign(semantic_advantage)
            aligned += int(consistent.sum().cpu())
        else:
            semantic = torch.zeros_like(business)
            semantic_advantage = torch.zeros_like(business)
            consistent = torch.zeros_like(business, dtype=torch.bool)
        if mode == "reward_sum":
            advantage = _standardize(business + semantic, torch)
            coefficient = torch.ones_like(advantage) if use_semantic else torch.zeros_like(advantage)
        elif mode == "adv_sum":
            advantage = business_advantage + semantic_advantage
            coefficient = torch.ones_like(advantage) if use_semantic else torch.zeros_like(advantage)
        elif mode == "a2po":
            magnitude = torch.minimum(business_advantage.abs(), semantic_advantage.abs()) / (
                torch.maximum(business_advantage.abs(), semantic_advantage.abs()) + 1e-8
            )
            coefficient = consistent.float() * magnitude
            contribution = coefficient * semantic_advantage
            bound_violations += int(
                (contribution.abs() > business_advantage.abs() + 1e-6).sum().cpu()
            )
            advantage = business_advantage + contribution
        else:
            advantage = business_advantage
            coefficient = torch.zeros_like(advantage)
        for _epoch in range(1):
            current = model.log_probs(history, candidate_codes)[0]
            ratio = torch.exp((current - old_logp).clamp(-10.0, 10.0))
            clipped = ratio.clamp(1 - config.clip_epsilon, 1 + config.clip_epsilon)
            loss = -torch.min(ratio * advantage, clipped * advantage).mean()
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
        losses.append(float(loss.detach().cpu()))
        rewards.append(float(business.mean().cpu()))
        clips.append(float((ratio.detach().sub(1).abs() > config.clip_epsilon).float().mean().cpu()))
        if use_semantic:
            lambdas.extend(coefficient.detach().cpu().tolist())
    return model, {
        "mode": mode,
        "steps": steps,
        "semantic_sampling_ratio": config.semantic_sampling_ratio,
        "semantic_queries": semantic_queries,
        "mean_loss": float(np.mean(losses)),
        "mean_business_reward": float(np.mean(rewards)),
        "clip_fraction": float(np.mean(clips)),
        "directional_consistency": aligned / max(1, compared),
        "mean_semantic_coefficient": float(np.mean(lambdas)) if lambdas else 0.0,
        "semantic_bound_violations": bound_violations,
        "seconds": time.perf_counter() - started,
    }


def score_catalog(model, data, row, config, chunk=512):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    history = _histories([row.history], config, device, torch)
    codes = torch.tensor(data.codes, dtype=torch.long, device=device)
    output = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(codes), chunk):
            candidates = codes[start : start + chunk].unsqueeze(0)
            output.append(model.log_probs(history, candidates)[0].cpu().numpy())
    return np.concatenate(output)


def _candidate_group(row, data, size, rng):
    excluded = set(row.history) | {row.target}
    similarities = data.vectors @ data.vectors[row.target]
    hard = np.argsort(similarities)[::-1]
    candidates = [row.target]
    for item in hard:
        value = int(item)
        if value not in excluded and value not in candidates:
            candidates.append(value)
        if len(candidates) >= max(2, size // 2):
            break
    while len(candidates) < size:
        value = int(rng.integers(len(data.codes)))
        if value not in excluded and value not in candidates:
            candidates.append(value)
    return candidates


def _histories(histories, config, device, torch):
    rows = []
    for history in histories:
        values = list(history[-config.sequence_length :])
        values = [0] * (config.sequence_length - len(values)) + values
        rows.append(values)
    return torch.tensor(rows, dtype=torch.long, device=device)


def _standardize(value, torch):
    return (value - value.mean()) / value.std(unbiased=False).clamp_min(1e-4)
