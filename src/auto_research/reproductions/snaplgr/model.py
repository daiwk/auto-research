from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes


def _coengagement(data) -> np.ndarray:
    graph = np.eye(data.item_count, dtype=np.float64) * 1e-3
    for sequence in data.sequences.train:
        unique = np.asarray(tuple(dict.fromkeys(sequence)), dtype=np.int64)
        graph[np.ix_(unique, unique)] += 1.0
    return graph / np.maximum(graph.sum(axis=1, keepdims=True), 1e-12)


def _code_transition(data, codes: np.ndarray, width: int) -> list[np.ndarray]:
    levels = []
    for level in range(codes.shape[1]):
        counts = np.full((width, width), 1e-3, dtype=np.float64)
        for sequence in data.sequences.train:
            values = codes[np.asarray(sequence, dtype=np.int64), level]
            for left, right in zip(values, values[1:]):
                counts[left, right] += 1.0
        levels.append(counts / counts.sum(axis=1, keepdims=True))
    return levels


def build_snaplgr(data, seed: int, width: int = 8) -> dict:
    features = data.sequences.features.astype(np.float64)
    baseline_codes = hierarchical_codes(features, width=width, seed=seed)
    ppr = _coengagement(data)
    refined = 0.55 * features + 0.45 * (ppr @ features)
    refined /= np.maximum(np.linalg.norm(refined, axis=1, keepdims=True), 1e-12)
    codes = hierarchical_codes(refined, width=width, seed=seed)

    # CPT grounding proxy: each newly introduced SID token is anchored to the
    # mean multimodal feature of the items assigned to it.
    grounded = np.zeros((codes.shape[1], width, features.shape[1]), dtype=np.float64)
    for level in range(codes.shape[1]):
        for code in range(width):
            members = features[codes[:, level] == code]
            if len(members):
                grounded[level, code] = members.mean(0)
    return {
        "width": width,
        "codes": codes,
        "baseline_codes": baseline_codes,
        "grounded": grounded,
        "transitions": _code_transition(data, codes, width),
        "baseline_transitions": _code_transition(data, baseline_codes, width),
    }


def _score(data, state: dict, history, baseline: bool) -> np.ndarray:
    codes = state["baseline_codes"] if baseline else state["codes"]
    transitions = state["baseline_transitions"] if baseline else state["transitions"]
    last = codes[history[-1]]
    score = np.zeros(data.item_count, dtype=np.float64)
    for level, matrix in enumerate(transitions):
        score += matrix[last[level], codes[:, level]] / (level + 1)
    if not baseline:
        context = data.sequences.features[np.asarray(history[-8:], dtype=np.int64)].mean(0)
        grounding = np.zeros(data.item_count, dtype=np.float64)
        for level in range(codes.shape[1]):
            grounding += state["grounded"][level, codes[:, level]] @ context / (level + 1)
        score += 0.25 * grounding
    return score


def score_baseline_sid(data, state: dict, history) -> np.ndarray:
    return _score(data, state, history, baseline=True)


def score_snaplgr(data, state: dict, history) -> np.ndarray:
    return _score(data, state, history, baseline=False)


def snaplgr_diagnostics(state: dict) -> dict[str, float]:
    codes = state["codes"]
    baseline = state["baseline_codes"]
    unique = len({tuple(row) for row in codes})
    baseline_unique = len({tuple(row) for row in baseline})
    return {
        "sid_levels": int(codes.shape[1]),
        "codebook_width": int(state["width"]),
        "sid_utilization": float(unique / len(codes)),
        "baseline_sid_utilization": float(baseline_unique / len(baseline)),
        "sid_collision_rate": float(1 - unique / len(codes)),
        "grounded_tokens": int(np.count_nonzero(np.linalg.norm(state["grounded"], axis=2))),
    }
