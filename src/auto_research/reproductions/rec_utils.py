from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..datasets import movielens_100k


@dataclass(frozen=True)
class MovieLensSequences:
    train: tuple[tuple[int, ...], ...]
    validation: tuple[int, ...]
    test: tuple[int, ...]
    item_count: int
    item_features: np.ndarray
    popularity: np.ndarray


def load_movielens_sequences(dataset_dir: Path, minimum_rating: float = 4.0) -> MovieLensSequences:
    ratings = movielens_100k(dataset_dir)
    raw_items = sorted({item for _, item, _, _ in ratings})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    by_user: dict[int, list[tuple[int, int]]] = {}
    popularity = np.zeros(len(raw_items), dtype=np.float64)
    for user, item, rating, timestamp in ratings:
        if rating >= minimum_rating:
            encoded = item_ids[item]
            by_user.setdefault(user, []).append((timestamp, encoded))
            popularity[encoded] += 1

    train, validation, test = [], [], []
    for events in by_user.values():
        sequence = tuple(item for _, item in sorted(events))
        if len(sequence) >= 7:
            train.append(sequence[:-2])
            validation.append(sequence[-2])
            test.append(sequence[-1])
    return MovieLensSequences(
        train=tuple(train),
        validation=tuple(validation),
        test=tuple(test),
        item_count=len(raw_items),
        item_features=_load_item_features(dataset_dir, raw_items),
        popularity=popularity,
    )


def _load_item_features(dataset_dir: Path, raw_items: list[int]) -> np.ndarray:
    path = dataset_dir / "ml-100k" / "u.item"
    rows: dict[int, np.ndarray] = {}
    with path.open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip("\n").split("|")
            rows[int(fields[0])] = np.asarray(fields[5:24], dtype=np.float64)
    matrix = np.stack([rows[item] for item in raw_items])
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.maximum(norms, 1.0)


def transitions(sequences: tuple[tuple[int, ...], ...]) -> np.ndarray:
    pairs = [(left, right) for sequence in sequences for left, right in zip(sequence, sequence[1:])]
    return np.asarray(pairs, dtype=np.int64)


def ranking_metrics(
    sequences: MovieLensSequences,
    scorer,
    target: str = "test",
    top_k: int = 10,
) -> dict[str, float]:
    targets = sequences.test if target == "test" else sequences.validation
    hits = ndcg = 0.0
    recommended: list[int] = []
    for index, (history, expected) in enumerate(
        zip(sequences.train, targets, strict=True)
    ):
        context = history + (
            (sequences.validation[index],) if target == "test" else ()
        )
        scores = np.asarray(scorer(context), dtype=np.float64).copy()
        scores[list(set(context))] = -np.inf
        cutoff = min(top_k, len(scores))
        top = np.argpartition(scores, -cutoff)[-cutoff:]
        top = top[np.argsort(scores[top])[::-1]]
        recommended.extend(int(item) for item in top)
        positions = np.flatnonzero(top == expected)
        if positions.size:
            hits += 1.0
            ndcg += 1.0 / math.log2(int(positions[0]) + 2)
    count = len(targets)
    pop = sequences.popularity / max(sequences.popularity.sum(), 1.0)
    head = set(np.argsort(pop)[-max(1, sequences.item_count // 10) :])
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "head_share_at_10": sum(item in head for item in recommended) / len(recommended),
        "mean_popularity_at_10": float(np.mean(pop[recommended])),
    }


def summarize_runs(runs: list[dict[str, float]]) -> dict[str, float]:
    return {
        key: float(np.mean([run[key] for run in runs]))
        for key in runs[0]
    } | {
        f"{key}_std": float(np.std([run[key] for run in runs]))
        for key in runs[0]
    }
