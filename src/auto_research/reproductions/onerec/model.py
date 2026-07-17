from __future__ import annotations

from auto_research.runtime import device_for

import copy
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from ..plum.model import SemanticIDIndex


@dataclass(frozen=True)
class OneRecConfig:
    dimensions: int = 96
    heads: int = 4
    layers: int = 2
    experts: int = 4
    history_items: int = 20
    session_items: int = 3
    batch_size: int = 48
    sft_steps: int = 240
    reward_steps: int = 120
    dpo_steps: int = 80
    dpo_pairs: int = 96
    beam_size: int = 12
    evaluation_users: int = 200
    learning_rate: float = 3e-4
    beta: float = 0.1


@dataclass(frozen=True)
class TokenLayout:
    level_offsets: tuple[int, ...]
    bos: int
    eos: int
    vocabulary_size: int

    @classmethod
    def from_index(cls, index: SemanticIDIndex):
        offsets, cursor = [], 0
        for cardinality in index.cardinalities:
            offsets.append(cursor)
            cursor += cardinality
        return cls(tuple(offsets), cursor, cursor + 1, cursor + 2)

    def encode_item(self, code) -> tuple[int, ...]:
        return tuple(offset + int(value) for offset, value in zip(self.level_offsets, code, strict=True))

def require_backend():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError(
            "OneRec trains RQ-SIDs, a session generator, reward model, and DPO; "
            "install with `pip install -e '.[neural-recs]'`."
        ) from exc
    return torch, nn


def build_generator(index: SemanticIDIndex, config: OneRecConfig):
    torch, nn = require_backend()
    layout = TokenLayout.from_index(index)
    maximum_source = config.history_items * len(index.cardinalities)
    maximum_target = config.session_items * len(index.cardinalities) + 1

    class SparseMoE(nn.Module):
        def __init__(self):
            super().__init__()
            self.gate = nn.Linear(config.dimensions, config.experts)
            self.expert = nn.ModuleList(
                [nn.Sequential(nn.Linear(config.dimensions, 4 * config.dimensions), nn.GELU(), nn.Linear(4 * config.dimensions, config.dimensions)) for _ in range(config.experts)]
            )

        def forward(self, values):
            probabilities = torch.softmax(self.gate(values), dim=-1)
            routes = torch.nn.functional.one_hot(
                probabilities.argmax(dim=-1), config.experts
            ).to(values.dtype)
            weights = routes * probabilities
            expert_values = torch.stack([expert(values) for expert in self.expert], dim=-2)
            return (expert_values * weights.unsqueeze(-1)).sum(dim=-2)

    class SessionGenerator(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding(layout.vocabulary_size, config.dimensions)
            self.source_position = nn.Embedding(maximum_source, config.dimensions)
            self.target_position = nn.Embedding(maximum_target, config.dimensions)
            encoder_layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            decoder_layer = nn.TransformerDecoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.encoder = nn.TransformerEncoder(encoder_layer, config.layers)
            self.decoder = nn.TransformerDecoder(decoder_layer, config.layers)
            self.moe = SparseMoE()
            self.output = nn.Linear(config.dimensions, layout.vocabulary_size, bias=False)
            self.output.weight = self.token.weight

        def forward(self, source, target):
            source_positions = torch.arange(source.shape[1], device=source.device)
            target_positions = torch.arange(target.shape[1], device=target.device)
            memory = self.encoder(self.token(source) + self.source_position(source_positions))
            hidden = self.token(target) + self.target_position(target_positions)
            mask = torch.triu(
                torch.ones(target.shape[1], target.shape[1], device=target.device),
                diagonal=1,
            ).bool()
            hidden = self.decoder(hidden, memory, tgt_mask=mask)
            return self.output(hidden + self.moe(hidden))

    return SessionGenerator(), layout


def session_examples(sequences, index: SemanticIDIndex, config: OneRecConfig, cap: int = 24000):
    rows = []
    layout = TokenLayout.from_index(index)
    for sequence in sequences:
        for split in range(2, len(sequence) - config.session_items + 1):
            history = sequence[max(0, split - config.history_items) : split]
            session = sequence[split : split + config.session_items]
            source = tuple(token for item in history for token in layout.encode_item(index.codes[item]))
            target = tuple(token for item in session for token in layout.encode_item(index.codes[item])) + (layout.eos,)
            rows.append((source, target, history, session))
    return tuple(rows[:cap])


def train_generator(model, layout, rows, config: OneRecConfig, seed: int):
    torch, _ = require_backend()
    device = device_for(torch)
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses: list[float] = []
    for _ in range(config.sft_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        source = _pad([row[0] for row in batch], layout.bos, device, torch, left=True)
        targets = _pad([row[1] for row in batch], layout.eos, device, torch)
        decoder_input = torch.cat(
            (torch.full((len(batch), 1), layout.bos, device=device, dtype=torch.long), targets[:, :-1]),
            dim=1,
        )
        optimizer.zero_grad(set_to_none=True)
        logits = model(source, decoder_input)
        loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, layout.vocabulary_size), targets.reshape(-1)
        )
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def build_reward_model(item_count: int, config: OneRecConfig):
    torch, nn = require_backend()

    class RewardModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.score = nn.Sequential(
                nn.Linear(3 * config.dimensions, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, 1),
            )

        def forward(self, history, session):
            user = self.item(history).mean(dim=1)
            slate = self.item(session).mean(dim=1)
            return self.score(torch.cat((user, slate, user * slate), dim=-1)).squeeze(-1)

    return RewardModel()


def train_reward_model(rows, item_count: int, config: OneRecConfig, seed: int):
    torch, _ = require_backend()
    device = device_for(torch)
    model = build_reward_model(item_count, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    for _ in range(config.reward_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = _pad_items([row[2] for row in batch], device, torch, config.history_items)
        positives = torch.tensor([row[3] for row in batch], dtype=torch.long, device=device)
        negatives = torch.tensor(
            [[rng.randrange(item_count) for _ in range(config.session_items)] for _ in batch],
            dtype=torch.long, device=device,
        )
        logits = torch.cat((model(histories, positives), model(histories, negatives)))
        labels = torch.cat((torch.ones(len(batch), device=device), torch.zeros(len(batch), device=device)))
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    model.eval()
    return model, {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
    }


def generate_beams(model, history, index, layout, config: OneRecConfig, catalog=None):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    source_tokens = tuple(
        token for item in history[-config.history_items :]
        for token in layout.encode_item(index.codes[item])
    )
    source = torch.tensor([source_tokens], dtype=torch.long, device=device)
    beams = [((), 0.0)]
    catalog = catalog or _catalog_transitions(index, layout)
    model.eval()
    with torch.inference_mode():
        for position in range(config.session_items * len(index.cardinalities) + 1):
            targets = torch.tensor(
                [[layout.bos, *tokens] for tokens, _ in beams],
                dtype=torch.long, device=device,
            )
            logits = model(source.expand(len(beams), -1), targets)[:, -1]
            expanded = []
            for row, (prefix, score) in enumerate(beams):
                allowed = _catalog_allowed(prefix, position, index, layout, config, catalog)
                log_probabilities = torch.log_softmax(logits[row, allowed], dim=-1)
                per_beam = min(config.beam_size, len(allowed))
                values, columns = torch.topk(log_probabilities, per_beam)
                expanded.extend(
                    (prefix + (allowed[int(column)],), score + float(value))
                    for value, column in zip(values.cpu(), columns.cpu(), strict=True)
                )
            beams = sorted(expanded, key=lambda value: value[1], reverse=True)[: config.beam_size]
    return beams


def _catalog_transitions(index, layout):
    transitions: dict[tuple[int, tuple[int, ...]], set[int]] = {}
    for code in index.codes:
        for level, value in enumerate(code):
            prefix = tuple(int(part) for part in code[:level])
            transitions.setdefault((level, prefix), set()).add(
                layout.level_offsets[level] + int(value)
            )
    return {key: sorted(values) for key, values in transitions.items()}


def _catalog_allowed(prefix, position, index, layout, config, catalog):
    width = len(index.cardinalities)
    if position == config.session_items * width:
        return [layout.eos]
    level = position % width
    item_prefix = prefix[position - level : position]
    raw_prefix = tuple(
        token - layout.level_offsets[prefix_level]
        for prefix_level, token in enumerate(item_prefix)
    )
    return catalog[(level, raw_prefix)]


def decode_session(tokens, index: SemanticIDIndex, layout: TokenLayout, popularity):
    width = len(index.cardinalities)
    groups = index.items_by_code()
    items = []
    for start in range(0, width * 3, width):
        encoded = tokens[start : start + width]
        code = tuple(value - layout.level_offsets[level] for level, value in enumerate(encoded))
        candidates = groups.get(code, ())
        if candidates:
            items.append(max(candidates, key=lambda item: popularity[item]))
    return tuple(items)


def preference_pairs(model, reward, rows, index, layout, popularity, config, seed):
    torch, _ = require_backend()
    rng = random.Random(seed)
    selected = rng.sample(list(rows), min(config.dpo_pairs, len(rows)))
    pairs = []
    device = next(reward.parameters()).device
    catalog = _catalog_transitions(index, layout)
    for row in selected:
        beams = generate_beams(model, row[2], index, layout, config, catalog)
        sessions = [decode_session(tokens, index, layout, popularity) for tokens, _ in beams]
        valid = [(beam, session) for beam, session in zip(beams, sessions, strict=True) if len(session) == config.session_items]
        if len(valid) < 2:
            continue
        histories = _pad_items([row[2]] * len(valid), device, torch, config.history_items)
        session_tensor = torch.tensor([session for _, session in valid], dtype=torch.long, device=device)
        with torch.inference_mode():
            rewards = reward(histories, session_tensor).cpu().numpy()
        winner = int(np.argmax(rewards))
        lower = [index_ for index_, value in enumerate(rewards) if value < rewards[winner]]
        if not lower:
            continue
        # Self-hard loser: highest model likelihood among reward-inferior candidates.
        loser = max(lower, key=lambda index_: valid[index_][0][1])
        pairs.append((row[0], valid[winner][0][0], valid[loser][0][0]))
    return tuple(pairs)


def train_dpo(model, pairs, layout, config: OneRecConfig):
    torch, _ = require_backend()
    reference = copy.deepcopy(model).eval()
    for parameter in reference.parameters():
        parameter.requires_grad_(False)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate * 0.5)
    rng = random.Random(250218965)
    losses = []
    model.train()
    for _ in range(config.dpo_steps):
        batch = [pairs[rng.randrange(len(pairs))] for _ in range(min(config.batch_size, len(pairs)))]
        source = _pad([row[0] for row in batch], layout.bos, next(model.parameters()).device, torch, left=True)
        winner = _pad([row[1] for row in batch], layout.eos, source.device, torch)
        loser = _pad([row[2] for row in batch], layout.eos, source.device, torch)
        policy_margin = _sequence_log_probability(model, source, winner, layout) - _sequence_log_probability(model, source, loser, layout)
        with torch.inference_mode():
            reference_margin = _sequence_log_probability(reference, source, winner, layout) - _sequence_log_probability(reference, source, loser, layout)
        loss = -torch.nn.functional.logsigmoid(config.beta * (policy_margin - reference_margin)).mean()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "pairs": len(pairs),
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
    }


def evaluate_generator(model, data, index, layout, config, seed):
    rng = random.Random(seed)
    users = list(range(len(data.train)))
    rng.shuffle(users)
    users = users[: min(config.evaluation_users, len(users))]
    hits = ndcg = valid = 0.0
    recommended = []
    catalog = _catalog_transitions(index, layout)
    for user in users:
        history = data.train[user] + (data.validation[user],)
        beams = generate_beams(model, history, index, layout, config, catalog)
        ranking = []
        for tokens, _ in beams:
            session = decode_session(tokens, index, layout, data.popularity)
            valid += float(len(session) == config.session_items)
            for item in session:
                if item not in history and item not in ranking:
                    ranking.append(item)
        ranking = ranking[:10]
        recommended.extend(ranking)
        expected = data.test[user]
        if expected in ranking:
            position = ranking.index(expected)
            hits += 1.0
            ndcg += 1.0 / math.log2(position + 2)
    head = set(np.argsort(data.popularity)[-max(1, data.item_count // 10):])
    count = max(1, len(users))
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "head_share_at_10": sum(item in head for item in recommended) / max(1, len(recommended)),
        "valid_session_rate": valid / max(1, len(users) * config.beam_size),
    }


def save_checkpoint(model, reward, directory: Path, torch):
    directory.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), directory / "generator.pt")
    torch.save(reward.state_dict(), directory / "reward_model.pt")


def _sequence_log_probability(model, source, target, layout):
    torch, _ = require_backend()
    decoder_input = torch.cat(
        (torch.full((len(target), 1), layout.bos, device=target.device, dtype=torch.long), target[:, :-1]), dim=1
    )
    logits = model(source, decoder_input)
    values = torch.log_softmax(logits, dim=-1).gather(-1, target.unsqueeze(-1)).squeeze(-1)
    return values.sum(dim=-1)


def _pad(rows, padding, device, torch, left=False):
    width = max(len(row) for row in rows)
    values = []
    for row in rows:
        pads = [padding] * (width - len(row))
        values.append(pads + list(row) if left else list(row) + pads)
    return torch.tensor(values, dtype=torch.long, device=device)


def _pad_items(rows, device, torch, width):
    values = []
    for row in rows:
        recent = row[-width:]
        values.append((recent[0],) * (width - len(recent)) + recent)
    return torch.tensor(values, dtype=torch.long, device=device)
