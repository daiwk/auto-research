from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np

from ...datasets import movielens_100k
from .model import SequentialModel, softmax


def reproduce_mdcns(
    dataset_dir: Path,
    seed: int = 42,
    factors: int = 12,
    epochs: int = 4,
    candidate_count: int = 30,
    top_k: int = 5,
) -> dict[str, Any]:
    ratings = movielens_100k(dataset_dir)
    train, test, seen, item_count = build_movie_sequences(ratings)
    results = {
        method: train_sequential(
            train,
            test,
            seen,
            item_count,
            method,
            seed,
            factors,
            epochs,
            candidate_count,
            top_k,
        )
        for method in ("uniform", "dns", "mdcns")
    }
    return {
        "paper": {
            "arxiv_id": "2605.19651",
            "title": "Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation",
            "url": "https://arxiv.org/abs/2605.19651",
            "track": "recommendation",
            "code": "https://github.com/Lyz103/SIGIR26-MDCNS",
        },
        "dataset": "MovieLens 100K (ratings >= 4 as positive feedback)",
        "setup": {
            "split": "per-user leave-last-one-out; earlier transitions for training",
            "users": len(test),
            "train_transitions": len(train),
            "items": item_count,
            "seed": seed,
            "epochs": epochs,
            "candidate_pool": candidate_count,
            "top_k": top_k,
        },
        "results": results,
        "ndcg10_gain_vs_dns_percent": 100
        * (results["mdcns"]["ndcg_at_10"] - results["dns"]["ndcg_at_10"])
        / max(results["dns"]["ndcg_at_10"], 1e-12),
        "ndcg10_gain_vs_uniform_percent": 100
        * (results["mdcns"]["ndcg_at_10"] - results["uniform"]["ndcg_at_10"])
        / max(results["uniform"]["ndcg_at_10"], 1e-12),
    }


def build_movie_sequences(ratings):
    by_user: dict[int, list[tuple[int, int]]] = {}
    items = sorted({item for _, item, _, _ in ratings})
    item_id = {item: index for index, item in enumerate(items)}
    for user, item, rating, timestamp in ratings:
        if rating >= 4:
            by_user.setdefault(user, []).append((timestamp, item_id[item]))
    train: list[tuple[int, int]] = []
    test: list[tuple[int, int]] = []
    seen: dict[int, set[int]] = {}
    for events in by_user.values():
        sequence = [item for _, item in sorted(events)]
        if len(sequence) < 5:
            continue
        train.extend(zip(sequence[:-2], sequence[1:-1]))
        test.append((sequence[-2], sequence[-1]))
        seen[len(test) - 1] = set(sequence[:-1])
    return train, test, seen, len(items)


def train_sequential(
    train,
    test,
    seen,
    item_count,
    method,
    seed,
    factors,
    epochs,
    candidate_count,
    top_k,
):
    rng = np.random.default_rng(seed)
    first = SequentialModel.create(item_count, factors, seed)
    second = (
        SequentialModel.create(item_count, factors, seed + 97)
        if method == "mdcns"
        else None
    )
    examples = np.asarray(train, dtype=np.int64)
    lr, reg = 0.025, 0.002
    for _ in range(epochs):
        rng.shuffle(examples)
        for previous, positive in examples:
            previous, positive = int(previous), int(positive)
            candidates = rng.integers(0, item_count, candidate_count)
            candidates[candidates == positive] = (positive + 1) % item_count
            score1 = first.scores(previous, candidates)
            if method == "uniform":
                first.bpr_update(previous, positive, int(candidates[0]), lr, reg)
            elif method == "dns":
                first.bpr_update(
                    previous, positive, int(candidates[int(np.argmax(score1))]), lr, reg
                )
            else:
                _mdcns_step(
                    first,
                    second,
                    previous,
                    positive,
                    candidates,
                    score1,
                    top_k,
                    rng,
                    lr,
                    reg,
                )
    return ranking_metrics(first, second, test, seen, item_count)


def _mdcns_step(
    first,
    second,
    previous,
    positive,
    candidates,
    score1,
    top_k,
    rng,
    lr,
    reg,
):
    assert second is not None
    score2 = second.scores(previous, candidates)
    disagreement = np.abs(score1 - score2)
    ensemble = 0.5 * (score1 + score2)
    indices = [
        topk_random(score1 + 0.5 * disagreement, top_k, rng),
        topk_random(score2 + 0.5 * disagreement, top_k, rng),
        topk_random(ensemble + 0.5 * disagreement, top_k, rng),
    ]
    for index, weight in zip(indices, (0.4, 0.3, 0.3), strict=True):
        first.bpr_update(previous, positive, int(candidates[index]), lr, reg, weight)
    for index, weight in zip(
        (indices[1], indices[0], indices[2]), (0.4, 0.3, 0.3), strict=True
    ):
        second.bpr_update(previous, positive, int(candidates[index]), lr, reg, weight)
    distill_candidates = np.concatenate(([positive], candidates))
    teacher = softmax(
        0.5
        * (
            first.scores(previous, distill_candidates)
            + second.scores(previous, distill_candidates)
        )
    )
    first.distill(previous, distill_candidates, teacher, lr, gamma=0.05)
    second.distill(previous, distill_candidates, teacher, lr, gamma=0.05)


def topk_random(scores: np.ndarray, top_k: int, rng: np.random.Generator) -> int:
    size = min(top_k, len(scores))
    indices = np.argpartition(scores, -size)[-size:]
    return int(indices[rng.integers(0, len(indices))])


def ranking_metrics(first, second, test, seen, item_count):
    hits = 0.0
    ndcg = 0.0
    all_items = np.arange(item_count)
    for index, (previous, target) in enumerate(test):
        scores = first.scores(previous, all_items)
        if second is not None:
            scores = 0.5 * (scores + second.scores(previous, all_items))
        scores[list(seen[index])] = -np.inf
        cutoff = min(10, item_count)
        top = np.argpartition(scores, -cutoff)[-cutoff:]
        top = top[np.argsort(scores[top])[::-1]]
        positions = np.where(top == target)[0]
        if len(positions):
            hits += 1
            ndcg += 1 / math.log2(int(positions[0]) + 2)
    return {"hit_at_10": hits / len(test), "ndcg_at_10": ndcg / len(test)}
