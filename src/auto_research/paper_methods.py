from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from .datasets import movielens_100k, tiny_shakespeare


SIS_PAPER = {
    "arxiv_id": "2607.04728",
    "title": "Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment",
    "url": "https://arxiv.org/abs/2607.04728",
}
MDCNS_PAPER = {
    "arxiv_id": "2605.19651",
    "title": "Divergence Meets Consensus: A Multi-Source Negative Sampling Framework for Sequential Recommendation",
    "url": "https://arxiv.org/abs/2605.19651",
    "code": "https://github.com/Lyz103/SIGIR26-MDCNS",
}


@dataclass(frozen=True)
class SISResult:
    method: str
    samples: int
    top_k: int
    acceptance_rate: float
    weight_variance: float
    mean_abs_log_ratio: float
    effective_sample_size: float


def sis_topk_weight(
    target: np.ndarray,
    behavior: np.ndarray,
    token: int,
    top_k: int,
    rng: np.random.Generator,
) -> tuple[float, bool]:
    """Algorithm 1 of arXiv:2607.04728 for one token position."""
    ratio = float(target[token] / behavior[token])
    top = np.argpartition(behavior, -min(top_k, len(behavior)))[-top_k:]
    if token not in top:
        return ratio, False
    envelope = float(np.max(target[top] / behavior[top]))
    accepted = bool(rng.random() < min(1.0, ratio / envelope))
    return (1.0 if accepted else ratio), accepted


def reproduce_sis(
    dataset_dir: Path,
    seed: int = 42,
    samples: int = 50_000,
    top_k: int = 10,
) -> dict[str, Any]:
    """Mechanism-level SIS reproduction on Tiny Shakespeare token distributions.

    A stale character bigram model is the behavior policy and a later-data bigram
    model is the current policy. This isolates the paper's importance-ratio change
    without claiming to reproduce its Qwen/GRPO accuracy numbers.
    """
    text = tiny_shakespeare(dataset_dir)
    vocab = sorted(set(text))
    token_id = {token: index for index, token in enumerate(vocab)}
    encoded = np.fromiter((token_id[token] for token in text), dtype=np.int64)
    split = int(len(encoded) * 0.45)
    later = int(len(encoded) * 0.8)
    behavior = _bigram_probabilities(encoded[:split], len(vocab), alpha=0.2)
    target = _bigram_probabilities(encoded[split:later], len(vocab), alpha=0.2)
    contexts = encoded[1:split]
    rng = np.random.default_rng(seed)
    raw_weights: list[float] = []
    sis_weights: list[float] = []
    accepted = 0
    for _ in range(samples):
        context = int(contexts[rng.integers(0, len(contexts))])
        token = int(rng.choice(len(vocab), p=behavior[context]))
        raw = float(target[context, token] / behavior[context, token])
        modified, was_accepted = sis_topk_weight(
            target[context], behavior[context], token, top_k, rng
        )
        raw_weights.append(raw)
        sis_weights.append(modified)
        accepted += was_accepted
    baseline = _weight_stats("token_is", raw_weights, 0.0, samples, top_k)
    sis = _weight_stats("sis", sis_weights, accepted / samples, samples, top_k)
    return {
        "paper": SIS_PAPER,
        "dataset": "Tiny Shakespeare",
        "setup": {
            "behavior_policy": "character bigram fitted on first 45%",
            "target_policy": "character bigram fitted on subsequent 35%",
            "samples": samples,
            "seed": seed,
        },
        "baseline": asdict(baseline),
        "method": asdict(sis),
        "variance_reduction_percent": 100
        * (baseline.weight_variance - sis.weight_variance)
        / baseline.weight_variance,
    }


def _bigram_probabilities(
    encoded: np.ndarray, vocab_size: int, alpha: float
) -> np.ndarray:
    counts = np.full((vocab_size, vocab_size), alpha, dtype=np.float64)
    np.add.at(counts, (encoded[:-1], encoded[1:]), 1.0)
    return counts / counts.sum(axis=1, keepdims=True)


def _weight_stats(
    method: str, weights: list[float], acceptance: float, samples: int, top_k: int
) -> SISResult:
    values = np.asarray(weights, dtype=np.float64)
    ess = float(values.sum() ** 2 / np.square(values).sum())
    return SISResult(
        method=method,
        samples=samples,
        top_k=top_k,
        acceptance_rate=acceptance,
        weight_variance=float(values.var()),
        mean_abs_log_ratio=float(np.abs(np.log(np.maximum(values, 1e-12))).mean()),
        effective_sample_size=ess,
    )


@dataclass
class SequentialModel:
    context: np.ndarray
    item: np.ndarray

    @classmethod
    def create(cls, items: int, factors: int, seed: int) -> "SequentialModel":
        rng = np.random.default_rng(seed)
        scale = 0.08 / math.sqrt(factors)
        return cls(
            rng.normal(0, scale, (items, factors)),
            rng.normal(0, scale, (items, factors)),
        )

    def scores(self, previous: int, candidates: np.ndarray) -> np.ndarray:
        return self.item[candidates] @ self.context[previous]

    def bpr_update(
        self,
        previous: int,
        positive: int,
        negative: int,
        lr: float,
        reg: float,
        weight: float = 1.0,
    ) -> None:
        context = self.context[previous].copy()
        pos = self.item[positive].copy()
        neg = self.item[negative].copy()
        diff = float(context @ (pos - neg))
        gradient = weight / (1.0 + math.exp(min(30.0, diff)))
        self.context[previous] += lr * (gradient * (pos - neg) - reg * context)
        self.item[positive] += lr * (gradient * context - reg * pos)
        self.item[negative] += lr * (-gradient * context - reg * neg)

    def distill(
        self,
        previous: int,
        candidates: np.ndarray,
        teacher: np.ndarray,
        lr: float,
        gamma: float,
    ) -> None:
        logits = self.scores(previous, candidates)
        student = _softmax(logits)
        grad = gamma * (student - teacher)
        context = self.context[previous].copy()
        item_vectors = self.item[candidates].copy()
        self.context[previous] -= lr * (grad[:, None] * item_vectors).sum(axis=0)
        np.add.at(self.item, candidates, -lr * grad[:, None] * context)


def reproduce_mdcns(
    dataset_dir: Path,
    seed: int = 42,
    factors: int = 12,
    epochs: int = 4,
    candidate_count: int = 30,
    top_k: int = 5,
) -> dict[str, Any]:
    """Scaled MDCNS reproduction using MovieLens sequential positive feedback."""
    ratings = movielens_100k(dataset_dir)
    train, test, seen, item_count = _movie_sequences(ratings)
    methods = {}
    for method in ("uniform", "dns", "mdcns"):
        metrics = _train_sequential(
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
        methods[method] = metrics
    return {
        "paper": MDCNS_PAPER,
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
        "results": methods,
        "ndcg10_gain_vs_dns_percent": 100
        * (methods["mdcns"]["ndcg_at_10"] - methods["dns"]["ndcg_at_10"])
        / max(methods["dns"]["ndcg_at_10"], 1e-12),
    }


def _movie_sequences(ratings):
    by_user: dict[int, list[tuple[int, int]]] = {}
    items = sorted({item for _, item, _, _ in ratings})
    item_id = {item: index for index, item in enumerate(items)}
    for user, item, rating, timestamp in ratings:
        if rating >= 4:
            by_user.setdefault(user, []).append((timestamp, item_id[item]))
    train: list[tuple[int, int]] = []
    test: list[tuple[int, int]] = []
    seen: dict[int, set[int]] = {}
    for user, events in by_user.items():
        sequence = [item for _, item in sorted(events)]
        if len(sequence) < 5:
            continue
        for left, right in zip(sequence[:-2], sequence[1:-1]):
            train.append((left, right))
        test.append((sequence[-2], sequence[-1]))
        seen[len(test) - 1] = set(sequence[:-1])
    return train, test, seen, len(items)


def _train_sequential(
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
            candidates = rng.integers(0, item_count, candidate_count)
            candidates[candidates == positive] = (positive + 1) % item_count
            score1 = first.scores(int(previous), candidates)
            if method == "uniform":
                first.bpr_update(
                    int(previous), int(positive), int(candidates[0]), lr, reg
                )
            elif method == "dns":
                negative = int(candidates[int(np.argmax(score1))])
                first.bpr_update(int(previous), int(positive), negative, lr, reg)
            else:
                assert second is not None
                score2 = second.scores(int(previous), candidates)
                disagreement = np.abs(score1 - score2)
                ensemble = 0.5 * (score1 + score2)
                indices = [
                    _topk_random(score1 + 0.5 * disagreement, top_k, rng),
                    _topk_random(score2 + 0.5 * disagreement, top_k, rng),
                    _topk_random(ensemble + 0.5 * disagreement, top_k, rng),
                ]
                for index, weight in zip(indices, (0.4, 0.3, 0.3), strict=True):
                    first.bpr_update(
                        int(previous),
                        int(positive),
                        int(candidates[index]),
                        lr,
                        reg,
                        weight,
                    )
                for index, weight in zip(
                    (indices[1], indices[0], indices[2]),
                    (0.4, 0.3, 0.3),
                    strict=True,
                ):
                    second.bpr_update(
                        int(previous),
                        int(positive),
                        int(candidates[index]),
                        lr,
                        reg,
                        weight,
                    )
                distill_candidates = np.concatenate(([positive], candidates))
                teacher = _softmax(
                    0.5
                    * (
                        first.scores(int(previous), distill_candidates)
                        + second.scores(int(previous), distill_candidates)
                    )
                )
                first.distill(int(previous), distill_candidates, teacher, lr, gamma=0.05)
                second.distill(int(previous), distill_candidates, teacher, lr, gamma=0.05)
    return _ranking_metrics(first, second, test, seen, item_count)


def _topk_random(scores: np.ndarray, top_k: int, rng: np.random.Generator) -> int:
    indices = np.argpartition(scores, -min(top_k, len(scores)))[-top_k:]
    return int(indices[rng.integers(0, len(indices))])


def _softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - values.max()
    exp = np.exp(shifted)
    return exp / exp.sum()


def _ranking_metrics(first, second, test, seen, item_count):
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


def write_reproduction_report(results: list[dict[str, Any]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.with_suffix(".json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    lines = ["# Paper Reproduction Report", ""]
    for result in results:
        paper = result["paper"]
        lines.extend(
            [
                f"## [{paper['title']}]({paper['url']})",
                "",
                f"arXiv `{paper['arxiv_id']}` · dataset: {result['dataset']}",
                "",
            ]
        )
        if paper["arxiv_id"] == SIS_PAPER["arxiv_id"]:
            lines.extend(
                [
                    "| Method | Weight variance | Mean |log ratio| | ESS | Accept rate |",
                    "|---|---:|---:|---:|---:|",
                ]
            )
            for key in ("baseline", "method"):
                row = result[key]
                lines.append(
                    f"| {row['method']} | {row['weight_variance']:.6f} | {row['mean_abs_log_ratio']:.6f} | {row['effective_sample_size']:.1f} | {row['acceptance_rate']:.2%} |"
                )
            lines.extend(["", f"SIS reduced importance-weight variance by **{result['variance_reduction_percent']:.2f}%**.", ""])
        else:
            lines.extend(["| Sampler | Hit@10 | NDCG@10 |", "|---|---:|---:|"])
            for method, row in result["results"].items():
                lines.append(f"| {method} | {row['hit_at_10']:.6f} | {row['ndcg_at_10']:.6f} |")
            lines.extend(["", f"MDCNS NDCG@10 change versus DNS: **{result['ndcg10_gain_vs_dns_percent']:.2f}%**.", ""])
    lines.extend(
        [
            "## Scope",
            "",
            "These are mechanism-level, Mac-scale reproductions of the cited algorithms. They preserve the paper-specific equations and comparison baselines, but do not claim to reproduce the papers' large-model or six-dataset headline numbers.",
            "",
        ]
    )
    output.write_text("\n".join(lines), encoding="utf-8")
