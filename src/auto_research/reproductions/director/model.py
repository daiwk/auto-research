from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores


def sinkhorn(logits: np.ndarray, iterations: int = 24, temperature: float = 0.35) -> np.ndarray:
    values = np.exp(np.clip(logits / temperature, -30, 30))
    for _ in range(iterations):
        values /= np.maximum(values.sum(axis=1, keepdims=True), 1e-12)
        column_mass = values.sum(axis=0, keepdims=True)
        values /= np.maximum(column_mass, 1.0)
    values /= np.maximum(values.sum(axis=1, keepdims=True), 1e-12)
    return values


def dynamic_indices(data, history, positions: int = 6) -> np.ndarray:
    features = data.sequences.features
    context = features[np.asarray(history[-12:], dtype=np.int64)].mean(0)
    recent = features[history[-1]]
    alpha = np.linspace(0.15, 0.85, positions)[:, None]
    indices = (1 - alpha) * context[None] + alpha * recent[None]
    # Position-dependent cyclic rotation prevents identical rows while keeping
    # every index in the same continuous retrieval space.
    return np.stack([np.roll(row, offset) for offset, row in enumerate(indices)])


def transport_plan(data, history, positions: int = 6) -> tuple[np.ndarray, np.ndarray]:
    logits = dynamic_indices(data, history, positions) @ data.sequences.features.T
    return logits, sinkhorn(logits)


def hard_global_match(logits: np.ndarray) -> list[int]:
    scores = logits.copy()
    chosen: list[int] = []
    for row in range(scores.shape[0]):
        available = scores[row].copy()
        if chosen:
            available[np.asarray(chosen, dtype=np.int64)] = -np.inf
        chosen.append(int(np.argmax(available)))
    return chosen


def score_independent_indices(data, history) -> np.ndarray:
    logits, _ = transport_plan(data, history)
    return logits[0] + 0.15 * base_scores(data, history)


def score_director(data, history) -> np.ndarray:
    logits, plan = transport_plan(data, history)
    coordinated = plan[0] + 0.25 * plan[1:].max(axis=0)
    return coordinated + 0.15 * base_scores(data, history)


def director_diagnostics(data, history) -> dict[str, float]:
    logits, plan = transport_plan(data, history)
    independent = np.argmax(logits, axis=1)
    matched = hard_global_match(logits)
    return {
        "positions": int(logits.shape[0]),
        "parallel_decode_steps": 1,
        "independent_duplicate_count": int(len(independent) - len(set(independent.tolist()))),
        "matched_duplicate_count": int(len(matched) - len(set(matched))),
        "transport_row_error": float(np.abs(plan.sum(axis=1) - 1).max()),
        "transport_max_column_mass": float(plan.sum(axis=0).max()),
    }
