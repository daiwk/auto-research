from __future__ import annotations

from auto_research.runtime import device_for

import csv
import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..industrial_ranking import require_backend


@dataclass(frozen=True)
class SessionExample:
    history: tuple[tuple[int, ...], ...]
    positives: tuple[int, ...]
    negatives: tuple[int, ...]


@dataclass(frozen=True)
class SessionData:
    train: tuple[SessionExample, ...]
    validation: tuple[SessionExample, ...]
    test: tuple[SessionExample, ...]
    item_count: int
    users: int


@dataclass(frozen=True)
class SessionRecConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    maximum_sessions: int = 8
    maximum_items: int = 12
    rows: int = 350_000
    users: int = 2_000
    steps: int = 180
    batch_size: int = 48
    learning_rate: float = 5e-4
    sampled_items: int = 128
    rank_weight: float = 0.01


def load_kuairand_sessions(root: Path, config: SessionRecConfig) -> SessionData:
    path = root / "kuairand-pure" / "data" / "log_standard_4_22_to_5_08_pure.csv"
    if not path.exists():
        from ...datasets import kuairand_pure_files

        path = kuairand_pure_files(root) / path.name
    raw: dict[int, list[tuple[int, int, bool]]] = {}
    with path.open(encoding="utf-8") as stream:
        for index, row in enumerate(csv.DictReader(stream)):
            if index >= config.rows:
                break
            user = int(row["user_id"])
            if user >= config.users:
                continue
            positive = row["is_click"] == "1" or row["long_view"] == "1"
            raw.setdefault(user, []).append(
                (int(row["time_ms"]), int(row["video_id"]), positive)
            )
    raw_items = sorted({item for events in raw.values() for _, item, _ in events})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    train: list[SessionExample] = []
    validation: list[SessionExample] = []
    test: list[SessionExample] = []
    retained = 0
    for events in raw.values():
        sessions: list[list[tuple[int, bool]]] = []
        previous = None
        for timestamp, raw_item, positive in sorted(events):
            if previous is None or timestamp - previous > 30 * 60 * 1000:
                sessions.append([])
            sessions[-1].append((item_ids[raw_item], positive))
            previous = timestamp
        sessions = [session for session in sessions if any(flag for _, flag in session)]
        if len(sessions) < 3:
            continue
        retained += 1
        examples = []
        for target in range(1, len(sessions)):
            positives = tuple(dict.fromkeys(item for item, flag in sessions[target] if flag))
            negatives = tuple(dict.fromkeys(item for item, flag in sessions[target] if not flag))
            history = tuple(
                tuple(item for item, flag in session if flag)[-config.maximum_items :]
                for session in sessions[max(0, target - config.maximum_sessions) : target]
            )
            history = tuple(session for session in history if session)
            if history and positives:
                examples.append(SessionExample(history, positives, negatives))
        if len(examples) >= 2:
            train.extend(examples[:-2])
            validation.append(examples[-2])
            test.append(examples[-1])
    return SessionData(tuple(train), tuple(validation), tuple(test), len(raw_items), retained)


def build_model(item_count: int, config: SessionRecConfig, hierarchical: bool):
    torch, nn = require_backend()

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count + 1, config.dimensions, padding_idx=item_count)
            self.position = nn.Embedding(
                config.maximum_sessions if hierarchical else config.maximum_sessions * config.maximum_items,
                config.dimensions,
            )
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, config.dimensions * 4,
                dropout=0.0, batch_first=True, norm_first=True,
            )
            self.encoder = nn.TransformerEncoder(layer, config.layers)
            self.norm = nn.LayerNorm(config.dimensions)

        def encode(self, values, mask):
            embedded = self.item(values)
            if hierarchical:
                weights = mask.unsqueeze(-1)
                embedded = (embedded * weights).sum(2) / weights.sum(2).clamp_min(1)
                sequence_mask = mask.any(2)
            else:
                embedded = embedded.flatten(1, 2)
                sequence_mask = mask.flatten(1, 2)
            positions = torch.arange(embedded.shape[1], device=embedded.device)
            hidden = self.encoder(
                embedded + self.position(positions),
                src_key_padding_mask=~sequence_mask,
            )
            last = sequence_mask.long().sum(1).clamp_min(1) - 1
            return self.norm(hidden[torch.arange(len(hidden), device=hidden.device), last])

        def score(self, query, items):
            return (query.unsqueeze(1) * self.item(items)).sum(-1)

    return Model()


def _collate(rows, item_count: int, config: SessionRecConfig, device, torch):
    values = torch.full(
        (len(rows), config.maximum_sessions, config.maximum_items), item_count,
        dtype=torch.long, device=device,
    )
    mask = torch.zeros_like(values, dtype=torch.bool)
    for batch, row in enumerate(rows):
        for session_index, session in enumerate(row.history[-config.maximum_sessions :]):
            items = session[-config.maximum_items :]
            values[batch, session_index, : len(items)] = torch.tensor(items, device=device)
            mask[batch, session_index, : len(items)] = True
    return values, mask


def train_and_evaluate(data: SessionData, config: SessionRecConfig, seed: int, hierarchical: bool):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_model(data.item_count, config, hierarchical).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    model.train()
    for _ in range(config.steps):
        rows = [data.train[rng.randrange(len(data.train))] for _ in range(config.batch_size)]
        values, mask = _collate(rows, data.item_count, config, device, torch)
        query = model.encode(values, mask)
        candidates = []
        targets = []
        negative_masks = []
        for row in rows:
            positive = rng.choice(row.positives)
            pool = [
                item for item in dict.fromkeys((*row.positives, *row.negatives))
                if item != positive
            ]
            while len(pool) < config.sampled_items - 1:
                item = rng.randrange(data.item_count)
                if item != positive and item not in pool:
                    pool.append(item)
            rng.shuffle(pool)
            pool = pool[: config.sampled_items - 1]
            pool.append(positive)
            rng.shuffle(pool)
            targets.append(pool.index(positive))
            candidates.append(pool)
            negative_masks.append([item in row.negatives for item in pool])
        candidate_tensor = torch.tensor(candidates, device=device)
        logits = model.score(query, candidate_tensor)
        retrieval = torch.nn.functional.cross_entropy(logits, torch.tensor(targets, device=device))
        hard_mask = torch.tensor(negative_masks, device=device)
        positive_score = logits[torch.arange(len(rows), device=device), torch.tensor(targets, device=device)]
        hard_score = logits.masked_fill(~hard_mask, -1e4).max(1).values
        rank = torch.nn.functional.softplus(hard_score - positive_score).mean()
        loss = retrieval + config.rank_weight * rank
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    validation = evaluate(model, data.validation, data.item_count, config, device, torch)
    metrics = evaluate(model, data.test, data.item_count, config, device, torch)
    return {
        **metrics,
        "validation": validation,
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "seconds": time.perf_counter() - started,
        "parameters": sum(value.numel() for value in model.parameters()),
        "device": device.type,
    }


def evaluate(model, rows, item_count, config, device, torch):
    recalls, ndcgs = [], []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            batch = rows[start : start + config.batch_size]
            values, mask = _collate(batch, item_count, config, device, torch)
            query = model.encode(values, mask)
            scores = query @ model.item.weight[:item_count].T
            top = scores.topk(min(20, item_count), dim=1).indices.cpu().tolist()
            for predicted, row in zip(top, batch):
                positives = set(row.positives)
                hits = [index for index, item in enumerate(predicted) if item in positives]
                recalls.append(len(hits) / len(positives))
                ndcgs.append(sum(1 / np.log2(index + 2) for index in hits) / sum(
                    1 / np.log2(index + 2) for index in range(min(len(positives), len(predicted)))
                ))
    return {"recall_at_20": float(np.mean(recalls)), "ndcg_at_20": float(np.mean(ndcgs)), "examples": len(rows)}
