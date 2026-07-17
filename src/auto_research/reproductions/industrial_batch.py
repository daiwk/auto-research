from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .rec_utils import load_movielens_sequences


FAIR_DIN_STEPS = 100


@dataclass(frozen=True)
class CompactSequences:
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    features: np.ndarray
    popularity: np.ndarray

    @property
    def item_count(self) -> int:
        return len(self.features)

    @property
    def item_features(self) -> np.ndarray:
        """Compatibility alias used by the shared DIN baseline."""
        return self.features


def compact_movielens(
    root: Path, maximum_users: int = 180, maximum_items: int = 320
) -> CompactSequences:
    raw = load_movielens_sequences(root)
    selected = set(np.argsort(-raw.popularity)[:maximum_items].tolist())
    rows = []
    for history, validation, test in zip(raw.train, raw.validation, raw.test):
        sequence = [item for item in (*history, validation, test) if item in selected]
        sequence = list(dict.fromkeys(sequence))
        if len(sequence) >= 7:
            rows.append(sequence)
        if len(rows) >= maximum_users:
            break
    items = sorted({item for row in rows for item in row})
    mapping = {item: index for index, item in enumerate(items)}
    encoded = [[mapping[item] for item in row] for row in rows]
    return CompactSequences(
        train=tuple(tuple(row[:-2]) for row in encoded),
        validation=tuple(row[-2] for row in encoded),
        test=tuple(row[-1] for row in encoded),
        features=raw.item_features[items].astype(np.float32),
        popularity=raw.popularity[items].astype(np.float32),
    )


def evaluate_scores(data: CompactSequences, scorer, k: int = 10) -> dict[str, float]:
    hits = ndcg = 0.0
    catalog = []
    for user, (history, target) in enumerate(zip(data.train, data.test)):
        context = (*history, data.validation[user])
        scores = np.asarray(scorer(context), dtype=np.float64).copy()
        scores[list(set(context))] = -np.inf
        top = np.argsort(-scores)[:k]
        catalog.extend(top.tolist())
        positions = np.flatnonzero(top == target)
        if positions.size:
            hits += 1
            ndcg += 1 / math.log2(int(positions[0]) + 2)
    head = set(np.argsort(-data.popularity)[: max(1, data.item_count // 10)])
    return {
        "hit_at_10": hits / len(data.test),
        "ndcg_at_10": ndcg / len(data.test),
        "head_share_at_10": sum(item in head for item in catalog) / len(catalog),
    }


def run_din_baseline(data: CompactSequences, seeds, steps: int):
    """Train DIN on the exact split and catalog used by a reproduction."""
    from .din.model import DINConfig, score_all, train_model
    from .rec_utils import summarize_runs

    config = DINConfig(steps=steps, batch_size=48)
    runs = []
    training = []
    for seed in seeds:
        model, metrics = train_model("din", data, config, seed)
        runs.append(
            evaluate_scores(
                data,
                lambda history, model=model: score_all(
                    model, history, data.item_count, config
                ),
            )
        )
        training.append(metrics)
    return summarize_runs(runs), training


def require_torch():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError("This reproduction requires `pip install -e '.[neural-recs]'`.") from exc
    return torch, nn


def device_for(torch):
    from auto_research.runtime import device_for as resolve_device
    return resolve_device(torch)


def training_pairs(data: CompactSequences, maximum_history: int = 20):
    rows = []
    for sequence in data.train:
        for index in range(1, len(sequence)):
            history = sequence[max(0, index - maximum_history) : index]
            rows.append((history, sequence[index]))
    return rows


def padded_histories(histories, length: int, device, torch):
    rows = []
    for history in histories:
        recent = tuple(history[-length:])
        rows.append((recent[0],) * (length - len(recent)) + recent)
    return torch.tensor(rows, dtype=torch.long, device=device)
