from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .rec_utils import load_movielens_1m_sequences


@dataclass(frozen=True)
class RecentMovieLens:
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    features: np.ndarray
    popularity: np.ndarray

    @property
    def item_count(self) -> int:
        return len(self.features)


def load_recent_movielens(
    root: Path, maximum_users: int = 320, maximum_items: int = 480
) -> RecentMovieLens:
    """Use a non-toy MovieLens-1M slice while keeping laptop runs bounded."""
    raw = load_movielens_1m_sequences(root)
    selected = set(np.argsort(-raw.popularity)[:maximum_items].tolist())
    rows: list[list[int]] = []
    for history, validation, test in zip(raw.train, raw.validation, raw.test):
        sequence = [
            item for item in (*history, validation, test) if item in selected
        ]
        if len(sequence) >= 10:
            rows.append(sequence)
        if len(rows) >= maximum_users:
            break
    items = sorted({item for row in rows for item in row})
    mapping = {item: index for index, item in enumerate(items)}
    encoded = [[mapping[item] for item in row] for row in rows]
    return RecentMovieLens(
        train=tuple(tuple(row[:-2]) for row in encoded),
        validation=tuple(row[-2] for row in encoded),
        test=tuple(row[-1] for row in encoded),
        features=raw.item_features[items].astype(np.float32),
        popularity=raw.popularity[items].astype(np.float32),
    )


def padded_histories(histories, length: int, torch, device):
    rows = []
    for history in histories:
        recent = tuple(history[-length:])
        rows.append((recent[0],) * (length - len(recent)) + recent)
    return torch.tensor(rows, dtype=torch.long, device=device)


def training_rows(data: RecentMovieLens, maximum_history: int) -> list[tuple[tuple[int, ...], int]]:
    rows = []
    for sequence in data.train:
        for index in range(2, len(sequence)):
            rows.append(
                (
                    tuple(sequence[max(0, index - maximum_history) : index]),
                    sequence[index],
                )
            )
    return rows


def full_catalog_metrics(data: RecentMovieLens, scorer, split: str = "test") -> dict[str, float]:
    targets = data.test if split == "test" else data.validation
    hit = ndcg = 0.0
    recommendations: list[int] = []
    for user, (history, target) in enumerate(zip(data.train, targets)):
        context = (
            (*history, data.validation[user]) if split == "test" else history
        )
        scores = np.asarray(scorer(context), dtype=np.float64).copy()
        scores[list(set(context))] = -np.inf
        top = np.argsort(-scores)[:10]
        recommendations.extend(top.tolist())
        position = np.flatnonzero(top == target)
        if position.size:
            hit += 1
            ndcg += 1 / math.log2(int(position[0]) + 2)
    head = set(
        np.argsort(-data.popularity)[: max(1, data.item_count // 10)].tolist()
    )
    return {
        "hit_at_10": hit / len(targets),
        "ndcg_at_10": ndcg / len(targets),
        "head_share_at_10": sum(item in head for item in recommendations)
        / len(recommendations),
    }


def relative(method: dict[str, float], baseline: dict[str, float]) -> dict[str, float]:
    return {
        f"{metric}_percent": 100
        * (method[metric] - baseline[metric])
        / max(abs(baseline[metric]), 1e-12)
        for metric in baseline
        if isinstance(baseline[metric], (float, int))
    }
