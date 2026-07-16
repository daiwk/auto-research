from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .industrial_batch import CompactSequences, compact_movielens


@dataclass(frozen=True)
class IndustrialData:
    sequences: CompactSequences
    transition: np.ndarray
    cosine: np.ndarray
    popularity: np.ndarray
    domains: np.ndarray

    @property
    def item_count(self) -> int:
        return self.sequences.item_count


def load_industrial_data(root: Path, maximum_users: int = 220, maximum_items: int = 360) -> IndustrialData:
    data = compact_movielens(root, maximum_users=maximum_users, maximum_items=maximum_items)
    transition = np.ones((data.item_count, data.item_count), dtype=np.float64) * 1e-3
    for sequence in data.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1.0
    transition /= transition.sum(axis=1, keepdims=True)
    features = data.features.astype(np.float64)
    cosine = features @ features.T
    popularity = np.log1p(data.popularity.astype(np.float64))
    popularity /= max(popularity.max(), 1e-9)
    domains = np.argmax(features, axis=1).astype(np.int64)
    return IndustrialData(data, transition, cosine, popularity, domains)


def base_scores(data: IndustrialData, history) -> np.ndarray:
    recent = tuple(history[-8:])
    transition = np.mean(data.transition[list(recent)], axis=0)
    content = np.mean(data.cosine[list(recent)], axis=0)
    return 0.50 * transition + 0.35 * content + 0.15 * data.popularity


def evaluate(data: IndustrialData, scorer, k: int = 10, target_split: str = "test") -> dict[str, float]:
    hits = ndcg = fresh_hits = fresh_total = 0.0
    catalog = []
    fresh = data.popularity <= np.quantile(data.popularity, 0.35)
    targets = data.sequences.test if target_split == "test" else data.sequences.validation
    for user, (history, target) in enumerate(zip(data.sequences.train, targets)):
        context = (*history, data.sequences.validation[user]) if target_split == "test" else history
        scores = np.asarray(scorer(context), dtype=np.float64).copy()
        scores[list(set(context))] = -np.inf
        top = np.argsort(-scores)[:k]
        catalog.extend(top.tolist())
        position = np.flatnonzero(top == target)
        hit = float(bool(position.size))
        hits += hit
        ndcg += 0.0 if not position.size else 1.0 / math.log2(int(position[0]) + 2)
        if fresh[target]:
            fresh_total += 1
            fresh_hits += hit
    head = set(np.argsort(-data.popularity)[: max(1, data.item_count // 10)])
    return {
        "hit_at_10": hits / len(targets),
        "ndcg_at_10": ndcg / len(targets),
        "fresh_hit_at_10": fresh_hits / max(fresh_total, 1),
        "head_share_at_10": sum(item in head for item in catalog) / len(catalog),
    }


def tune_blend(data: IndustrialData, baseline_scorer, method_scorer):
    """Select method strength on validation only; test remains untouched."""
    best = (float("-inf"), 0.0, None)
    # Every reported method must execute its paper-specific path; zero is retained
    # as a separately reported baseline, not a selectable "method" setting.
    for alpha in np.linspace(0.1, 1.0, 10):
        def scorer(history, alpha=alpha):
            return (1.0 - alpha) * baseline_scorer(history) + alpha * method_scorer(history)
        metrics = evaluate(data, scorer, target_split="validation")
        objective = metrics["ndcg_at_10"] + 0.25 * metrics["hit_at_10"]
        if objective > best[0]:
            best = (objective, float(alpha), metrics)
    alpha = best[1]
    return alpha, (lambda history: (1.0 - alpha) * baseline_scorer(history) + alpha * method_scorer(history)), best[2]


def hierarchical_codes(features: np.ndarray, levels: int = 3, width: int = 8, seed: int = 42) -> np.ndarray:
    """Residual k-means Semantic IDs; each level quantizes the previous residual."""
    rng = np.random.default_rng(seed)
    residual = features.astype(np.float64).copy()
    codes = []
    for _ in range(levels):
        centers = residual[rng.choice(len(residual), width, replace=False)].copy()
        for _ in range(12):
            distance = ((residual[:, None] - centers[None]) ** 2).sum(-1)
            assignment = distance.argmin(1)
            for index in range(width):
                members = residual[assignment == index]
                if len(members):
                    centers[index] = members.mean(0)
        codes.append(assignment)
        residual -= centers[assignment]
    return np.stack(codes, axis=1)


def ridge(source: np.ndarray, target: np.ndarray, regularization: float = 1e-2) -> np.ndarray:
    eye = np.eye(source.shape[1]) * regularization
    return np.linalg.solve(source.T @ source + eye, source.T @ target)


def softmax(values: np.ndarray, axis: int = -1) -> np.ndarray:
    shifted = values - np.max(values, axis=axis, keepdims=True)
    exp = np.exp(np.clip(shifted, -40, 40))
    return exp / np.maximum(exp.sum(axis=axis, keepdims=True), 1e-12)


def gain(proposed: dict[str, float], baseline: dict[str, float]) -> dict[str, float]:
    return {
        f"{key}_percent": 100.0 * (proposed[key] - baseline[key]) / max(abs(baseline[key]), 1e-12)
        for key in ("hit_at_10", "ndcg_at_10", "fresh_hit_at_10", "head_share_at_10")
    }


def summary_result(*, key: str, paper: dict, data: IndustrialData, baseline_name: str,
                   method_name: str, baseline: dict, proposed: dict, stages: dict,
                   paper_results: dict, scope: str) -> dict:
    return {
        "paper": paper,
        "dataset": {"name": "MovieLens 100K", "users": len(data.sequences.train), "items": data.item_count},
        "setup": {"adapter": key, "same_split_and_candidates": True},
        "baseline": {"name": baseline_name, **baseline},
        "method": {"name": method_name, **proposed},
        "relative": gain(proposed, baseline),
        "stages": stages,
        "paper_results": paper_results,
        "scope": scope,
    }


def render_standard(result: dict) -> str:
    base, method = result["baseline"], result["method"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / {result['dataset']['items']} items）", "",
        "| Variant | Hit@10 | NDCG@10 | Fresh Hit@10 | Head share@10 |",
        "|---|---:|---:|---:|---:|",
        f"| {base['name']} | {base['hit_at_10']:.4f} | {base['ndcg_at_10']:.4f} | {base['fresh_hit_at_10']:.4f} | {base['head_share_at_10']:.4f} |",
        f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | {method['fresh_hit_at_10']:.4f} | {method['head_share_at_10']:.4f} |", "",
        f"相对同协议基线：Hit@10 {result['relative']['hit_at_10_percent']:+.2f}%，NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ])


def context_matrix(data: IndustrialData) -> tuple[np.ndarray, np.ndarray]:
    rows, targets = [], []
    for sequence in data.sequences.train:
        for end in range(2, len(sequence)):
            rows.append(np.mean(data.sequences.features[list(sequence[max(0, end - 8):end])], axis=0))
            targets.append(sequence[end])
    return np.asarray(rows), np.asarray(targets, dtype=np.int64)
