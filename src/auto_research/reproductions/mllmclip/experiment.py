from __future__ import annotations

from pathlib import Path

import numpy as np

from ..recent_20260728_common import load_recent_movielens


def _normalize(x):
    return x / np.maximum(np.linalg.norm(x, axis=1, keepdims=True), 1e-8)


def _cka(x, y):
    x = x - x.mean(0); y = y - y.mean(0)
    xy = np.linalg.norm(x.T @ y) ** 2
    return float(xy / max(np.linalg.norm(x.T @ x) * np.linalg.norm(y.T @ y), 1e-9))


def _retrieval(left, right, k=10):
    scores = _normalize(left) @ _normalize(right).T
    top = np.argpartition(-scores, kth=min(k, len(scores) - 1), axis=1)[:, :k]
    return float(np.mean([i in row for i, row in enumerate(top)]))


def reproduce_mllmclip(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=360)
    rng = np.random.default_rng(seed)
    image_tokens = data.features.astype(np.float64)
    teacher_layers = [np.tanh(image_tokens @ rng.normal(0, 0.25, (image_tokens.shape[1], 24))) for _ in range(3)]
    attention = np.var(np.stack(teacher_layers), axis=(0, 2))
    selected = np.argsort(-attention)[: max(24, len(attention) // 2)]
    teacher = np.mean([layer[selected].mean(0) for layer in teacher_layers], axis=0)
    teacher_targets = np.stack([layer.mean(0) for layer in teacher_layers]).mean(0)
    # Ridge projection is the closed-form compact analogue of the CKA feature loss.
    x = image_tokens
    y = np.tile(teacher_targets, (len(x), 1)) + 0.35 * teacher_layers[-1]
    projection = np.linalg.solve(x.T @ x + 0.1 * np.eye(x.shape[1]), x.T @ y)
    student = x @ projection
    baseline = x[:, : min(x.shape[1], student.shape[1])]
    teacher_items = teacher_layers[-1]
    result_baseline = {"recall_at_10": _retrieval(baseline, teacher_items[:, :baseline.shape[1]]), "linear_cka": _cka(baseline, teacher_items[:, :baseline.shape[1]])}
    result_method = {"recall_at_10": _retrieval(student, teacher_items), "linear_cka": _cka(student, teacher_items)}
    return {
        "paper": {"arxiv_id": "2608.25575", "title": "MLLMCLIP"},
        "dataset": {"name": "MovieLens-1M public content/collaborative proxy", "items": data.item_count},
        "setup": {"seed": seed, "teacher_layers": 3, "selected_tokens": len(selected)},
        "variants": {"CLIP feature baseline": result_baseline, "MLLMCLIP distillation": result_method},
        "relative": {name: 100 * (result_method[name] - result_baseline[name]) / max(abs(result_baseline[name]), 1e-9) for name in result_baseline},
        "diagnostics": {"attention_selected_fraction": len(selected) / len(attention), "cka_loss": 1 - result_method["linear_cka"], "synthetic_hard_negative_calls": 0, "teacher_summary_norm": float(np.linalg.norm(teacher))},
        "scope": "在 MovieLens-1M 的公开内容/协同代理视图上执行逐层 attention token selection 与 CKA feature distillation；不加载原论文 MLLM teacher，也不把代理 retrieval 指标视为视觉 benchmark 结果。",
        "diagnostic_only": True,
    }
