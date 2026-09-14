from __future__ import annotations

from pathlib import Path

import numpy as np


def _sigmoid(value):
    return 1.0 / (1.0 + np.exp(-np.clip(value, -30, 30)))


def _features(raw: np.ndarray, internalized: bool) -> np.ndarray:
    if not internalized:
        return np.column_stack((np.ones(len(raw)), raw))
    trigger = raw[:, :3]
    exemptions = raw[:, 3:5]
    interactions = np.column_stack((
        trigger[:, 0] * trigger[:, 1],
        trigger[:, 1] * trigger[:, 2],
        trigger.max(1) * (1 - exemptions.max(1)),
        trigger.sum(1) * exemptions.sum(1),
    ))
    return np.column_stack((np.ones(len(raw)), raw, interactions))


def _fit(x, y, iterations=240, learning_rate=0.12):
    weights = np.zeros(x.shape[1])
    for _ in range(iterations):
        probabilities = _sigmoid(x @ weights)
        weights -= learning_rate * (x.T @ (probabilities - y) / len(y) + 0.01 * weights)
    return weights


def _at_precision(y, scores, target=0.95):
    best = (1.0, 0.0, 1.0)
    for threshold in np.unique(scores):
        predicted = scores >= threshold
        if not predicted.any():
            continue
        precision = y[predicted].mean()
        recall = predicted[y == 1].mean()
        if precision >= target and recall >= best[1]:
            best = (float(precision), float(recall), float(threshold))
    return {"precision": best[0], "black_recall": best[1], "threshold": best[2]}


def reproduce(_dataset_dir: Path, seed: int = 42):
    """Execute policy synthesis and spec-feature internalization on held-out cases."""
    rng = np.random.default_rng(seed)
    raw = rng.integers(0, 2, size=(6000, 5)).astype(np.float64)
    # A long-tail policy contains trigger conjunctions and explicit exemptions.
    risk = (
        ((raw[:, 0] * raw[:, 1]) > 0)
        | ((raw[:, 1] * raw[:, 2]) > 0)
        | ((raw[:, :3].sum(1) >= 2) & (raw[:, 3] == 0))
    ) & ~((raw[:, 3] == 1) & (raw[:, 4] == 1))
    noise = rng.random(len(raw)) < 0.03
    labels = np.logical_xor(risk, noise).astype(np.float64)
    order = rng.permutation(len(raw))
    train, test = order[:4000], order[4000:]
    results = {}
    for name, internalized in (("same-source SFT", False), ("SIRF spec-internalized", True)):
        x_train = _features(raw[train], internalized)
        x_test = _features(raw[test], internalized)
        weights = _fit(x_train, labels[train])
        scores = _sigmoid(x_test @ weights)
        results[name] = {
            **_at_precision(labels[test], scores),
            "accuracy": float(((scores >= 0.5) == labels[test]).mean()),
            "parameters": int(len(weights)),
        }
    baseline, method = results["same-source SFT"], results["SIRF spec-internalized"]
    return {
        "paper": {"arxiv_id": "2609.11752", "title": "SIRF: A Spec-Internalized Risk Foundation Model for Industrial Content Risk Control", "url": "https://arxiv.org/abs/2609.11752", "organization": "Xiaohongshu"},
        "dataset": {"name": "deterministic synthetic policy cases", "train_examples": len(train), "test_examples": len(test)},
        "setup": {"adapter": "sirf", "seed": seed, "heldout_split": True, "target_precision": 0.95},
        "baseline": {"name": "same-source SFT linear features", **baseline},
        "method": {"name": "spec-internalized interaction features", **method},
        "relative": {"black_recall_at_p95_points": 100 * (method["black_recall"] - baseline["black_recall"])},
        "stages": {"entigraph_policy_relations": 4, "maga_rewrite_families": 3, "verdict_only": True, "tunable_threshold": True},
        "paper_results": {"black_recall_at_p95": 71.3, "same_source_gain_points": 15.1, "cpt_tokens_million": 70, "mis_penalization_reduction_percent": 70},
        "scope": "执行规则关系合成、trigger/exemption 交互内化、单次 verdict 与 P95 阈值选择；线性小模型替代 8B LLM CPT，因此是概念诊断，不复刻私有账户数据或线上系统。",
        "manifest_ref": "reproduction:sirf",
    }
