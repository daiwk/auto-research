from __future__ import annotations

import math

import numpy as np

from ..reproductions.industrial_ranking import evaluate_model, require_backend
from ..reproductions.rec_utils import MovieLensSequences
def recommendation_benchmark(
    model,
    data: MovieLensSequences,
    config,
    *,
    target: str,
    suite: str,
    restricted_path: bool = False,
) -> dict[str, float]:
    """Evaluate one model on fixed, public and selection-safe ranking slices."""
    primary = evaluate_model(model, data, config, target=target)
    result = dict(primary)
    if suite == "core":
        result["primary"] = result["ndcg_at_10"]
        result["public_composite"] = result["ndcg_at_10"]
        return result

    targets = data.test if target == "test" else data.validation
    lengths = np.asarray([len(history) for history in data.train])
    long_cutoff = float(np.quantile(lengths, 0.75))
    long_history = _subset(
        data, [index for index, length in enumerate(lengths) if length >= long_cutoff]
    )
    nonzero_popularity = data.popularity[data.popularity > 0]
    tail_cutoff = float(np.median(nonzero_popularity)) if len(nonzero_popularity) else 0.0
    tail = _subset(
        data,
        [
            index
            for index, item in enumerate(targets)
            if data.popularity[item] <= tail_cutoff
        ],
    )
    recent = MovieLensSequences(
        tuple(history[-4:] for history in data.train),
        data.validation,
        data.test,
        data.item_count,
        data.item_features,
        data.popularity,
    )
    slices = {
        "long_history": evaluate_model(model, long_history, config, target=target),
        "tail_target": evaluate_model(model, tail, config, target=target),
        "recent_only": evaluate_model(model, recent, config, target=target),
    }
    if restricted_path:
        slices["restricted_features"] = _evaluate_with_mode(
            model, data, config, target=target, mode="restricted"
        )
    for name, metrics in slices.items():
        for metric, value in metrics.items():
            result[f"{name}_{metric}"] = value
    ndcgs = [primary["ndcg_at_10"]]
    ndcgs.extend(metrics["ndcg_at_10"] for metrics in slices.values())
    result["primary"] = primary["ndcg_at_10"]
    result["public_composite"] = float(np.mean(ndcgs))
    if suite == "unirank":
        pointwise = _unirank_pointwise(model, data, config, target=target)
        result.update(pointwise)
        result["unirank_composite"] = float(
            0.5 * result["ndcg_at_10"] + 0.5 * result["pointwise_auc"]
        )
    return result


def _subset(data: MovieLensSequences, indices: list[int]) -> MovieLensSequences:
    if not indices:
        indices = list(range(len(data.train)))
    return MovieLensSequences(
        tuple(data.train[index] for index in indices),
        tuple(data.validation[index] for index in indices),
        tuple(data.test[index] for index in indices),
        data.item_count,
        data.item_features,
        data.popularity,
    )


def _evaluate_with_mode(model, data, config, *, target: str, mode: str):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    targets = data.test if target == "test" else data.validation
    hits = ndcg = 0.0
    recommended = []
    model.eval()
    for index, (history, expected) in enumerate(zip(data.train, targets)):
        context = history + ((data.validation[index],) if target == "test" else ())
        recent = context[-config.sequence_length :]
        padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
        with torch.inference_mode():
            logits = model(
                torch.tensor([padded], dtype=torch.long, device=device),
                mode=mode,
            )[0].detach().cpu().numpy()
        logits[list(set(context))] = -np.inf
        cutoff = min(10, len(logits))
        top = np.argpartition(logits, -cutoff)[-cutoff:]
        top = top[np.argsort(logits[top])[::-1]]
        recommended.extend(int(item) for item in top)
        positions = np.flatnonzero(top == expected)
        if positions.size:
            hits += 1.0
            ndcg += 1.0 / math.log2(int(positions[0]) + 2)
    count = len(targets)
    popularity = data.popularity / max(data.popularity.sum(), 1.0)
    head = set(np.argsort(popularity)[-max(1, data.item_count // 10) :])
    return {
        "hit_at_10": hits / count,
        "ndcg_at_10": ndcg / count,
        "head_share_at_10": sum(item in head for item in recommended)
        / len(recommended),
        "mean_popularity_at_10": float(np.mean(popularity[recommended])),
    }


def _unirank_pointwise(model, data, config, *, target: str):
    """UniRank-compatible chronological pointwise evaluation on local data.

    MovieLens has one implicit-positive label rather than UniRank's multi-feedback
    schema. Each chronological target is therefore paired with deterministic,
    unseen negatives and evaluated with global AUC/logloss.
    """
    torch, _ = require_backend()
    device = next(model.parameters()).device
    targets = data.test if target == "test" else data.validation
    logits, labels = [], []
    model.eval()
    for index, (history, positive) in enumerate(zip(data.train, targets)):
        context = history + ((data.validation[index],) if target == "test" else ())
        recent = context[-config.sequence_length :]
        padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
        with torch.inference_mode():
            scores = model(
                torch.tensor([padded], dtype=torch.long, device=device)
            )[0].detach().float().cpu().numpy()
        excluded = set(context) | {positive}
        candidates = [
            item for item in range(data.item_count)
            if item not in excluded
        ]
        rng = np.random.default_rng(index + (17 if target == "test" else 0))
        negatives = rng.choice(
            candidates, size=min(20, len(candidates)), replace=False
        )
        selected = np.concatenate(([positive], negatives))
        selected_scores = scores[selected]
        # Per-impression centering makes logloss comparable across architectures.
        selected_scores = selected_scores - selected_scores.mean()
        scale = max(float(selected_scores.std()), 1.0)
        logits.extend((selected_scores / scale).tolist())
        labels.extend([1.0] + [0.0] * len(negatives))
    values = np.asarray(logits, dtype=np.float64)
    truth = np.asarray(labels, dtype=np.float64)
    probabilities = 1.0 / (1.0 + np.exp(-np.clip(values, -30, 30)))
    logloss = -np.mean(
        truth * np.log(probabilities + 1e-12)
        + (1 - truth) * np.log(1 - probabilities + 1e-12)
    )
    positives = values[truth == 1]
    negatives = values[truth == 0]
    auc = float(
        np.mean(
            [
                np.mean((positive > negatives) + 0.5 * (positive == negatives))
                for positive in positives
            ]
        )
    )
    return {
        "pointwise_auc": auc,
        "pointwise_logloss": float(logloss),
        "pointwise_examples": float(len(values)),
    }
