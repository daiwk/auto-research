"""Reference kernels for retrieval and efficient-serving papers, Sep 2026."""

from __future__ import annotations

import numpy as np


def vendi_score(embeddings) -> float:
    values = np.asarray(embeddings, dtype=np.float64)
    values /= np.linalg.norm(values, axis=1, keepdims=True) + 1e-12
    spectrum = np.linalg.eigvalsh(values @ values.T / len(values))
    spectrum = np.clip(spectrum, 0.0, None)
    spectrum /= spectrum.sum() + 1e-12
    return float(np.exp(-(spectrum * np.log(spectrum + 1e-12)).sum()))


def r4t_targets(query, database, count: int = 6):
    """R4T composite set objective and a single-pass diffusion target set."""
    query = np.asarray(query, dtype=np.float64)
    database = np.asarray(database, dtype=np.float64)
    alignment = database @ query / ((np.linalg.norm(database, axis=1) * np.linalg.norm(query)) + 1e-12)
    selected = [int(np.argmax(alignment))]
    while len(selected) < min(count, len(database)):
        chosen = database[selected]
        redundancy = np.max(database @ chosen.T, axis=1)
        reward = 0.65 * alignment - 0.35 * redundancy
        reward[selected] = -np.inf
        selected.append(int(np.argmax(reward)))
    targets = database[selected]
    return targets, {
        "alignment": float(alignment[selected].mean()),
        "vendi_score": vendi_score(targets),
        "single_pass_targets": float(len(targets)),
    }


def loopspec_schedule(acceptance_by_depth, verify_cost: float = 1.0):
    """Select the first and residual proposal depths by expected saved work."""
    rates = np.asarray(acceptance_by_depth, dtype=np.float64)
    depths = np.arange(1, len(rates) + 1, dtype=np.float64)
    utility = rates * depths - verify_cost
    first = int(np.argmax(utility))
    residual = np.maximum(rates[first + 1:] - rates[first], 0.0)
    second = int(first + 1 + np.argmax(residual)) if len(residual) and residual.max() > 0 else first
    return first + 1, second + 1, {
        "expected_saved_depth": float(max(0.0, utility[first])),
        "residual_gate_open": float(second != first),
    }


def agentkv_scores(keys, phase_queries):
    """Score each cached key against the union of phase-specific query buffers."""
    keys = np.asarray(keys, dtype=np.float64)
    buffers = [np.asarray(value, dtype=np.float64) for value in phase_queries.values() if len(value)]
    if not buffers:
        return np.zeros(len(keys)), {"phases": 0.0}
    queries = np.concatenate(buffers, axis=0)
    queries /= np.linalg.norm(queries, axis=1, keepdims=True) + 1e-12
    normalized_keys = keys / (np.linalg.norm(keys, axis=1, keepdims=True) + 1e-12)
    scores = np.max(normalized_keys @ queries.T, axis=1)
    return scores, {"phases": float(len(buffers)), "queries": float(len(queries))}
