from __future__ import annotations

import numpy as np

from ..industrial_2026 import softmax


def _teacher_scores(data, history) -> np.ndarray:
    events = np.asarray(history, dtype=np.int64)
    features = data.sequences.features[events]
    query = features[-1]
    weights = softmax(features @ query / np.sqrt(features.shape[1]))
    context = weights @ features
    return data.sequences.features @ context + 0.20 * data.transition[events[-8:]].mean(0)


def merge_tokens(data, history, target_tokens: int = 8) -> tuple[np.ndarray, np.ndarray]:
    events = np.asarray(history, dtype=np.int64)
    groups = np.array_split(events, min(target_tokens, len(events)))
    merged = np.stack([data.sequences.features[group].sum(0) / np.sqrt(len(group)) for group in groups])
    sizes = np.asarray([len(group) for group in groups], dtype=np.int64)
    return merged, sizes


def score_merged_student(data, history) -> np.ndarray:
    merged, _ = merge_tokens(data, history)
    query = data.sequences.features[history[-1]]
    weights = softmax(merged @ query / np.sqrt(merged.shape[1]))
    return data.sequences.features @ (weights @ merged)


def score_tm20k(data, history, distillation_weight: float = 0.30) -> np.ndarray:
    student = score_merged_student(data, history)
    teacher = _teacher_scores(data, history)
    return (1 - distillation_weight) * student + distillation_weight * teacher


def tm20k_diagnostics(data, history) -> dict[str, float]:
    merged, sizes = merge_tokens(data, history)
    teacher = _teacher_scores(data, history)
    student = score_merged_student(data, history)
    distilled = score_tm20k(data, history)
    return {
        "input_tokens": int(len(history)),
        "merged_tokens": int(len(merged)),
        "compression_ratio": float(len(merged) / len(history)),
        "largest_merge_group": int(sizes.max()),
        "student_teacher_mse": float(np.mean((student - teacher) ** 2)),
        "distilled_teacher_mse": float(np.mean((distilled - teacher) ** 2)),
    }
