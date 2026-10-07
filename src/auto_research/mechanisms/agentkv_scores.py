"""Extracted unchanged from auto_research.foundation_latest_20260916; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

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
