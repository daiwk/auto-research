"""ActKV action-oriented eviction policy, independent of serving kernels.

This is the LRFU selection part of ActKV Algorithm 1. It does not implement
the paper's paged-attention recovery or in-place CUDA compaction kernels, so
it must not be reported as an end-to-end ActKV throughput reproduction.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EvictionResult:
    retained_indices: tuple[int, ...]
    keep_scores: tuple[float, ...]
    hit_indices: tuple[int, ...]


def action_lrfu_step(
    action_attention: np.ndarray,
    prior_keep_scores: np.ndarray,
    *,
    budget: int,
    decay: float = 0.8,
    top_p: float = 0.9,
) -> EvictionResult:
    """Update scores from one action region and retain the top-budget slots.

    ``prior_keep_scores`` describes the already-retained prefix; newly
    appended observation/reasoning/action slots receive an initial zero.
    ``top_p`` is the cumulative *attention mass* of the hit set. Ties use
    stable slot ordering; output indices remain in sequence order so a KV
    compactor can copy them without permuting positions.
    """
    attention = np.asarray(action_attention, dtype=np.float64)
    prior = np.asarray(prior_keep_scores, dtype=np.float64)
    if attention.ndim != 1 or prior.ndim != 1 or len(attention) == 0:
        raise ValueError("attention and prior scores must be nonempty 1-D vectors")
    if len(prior) > len(attention):
        raise ValueError("prior scores cannot exceed the current cache length")
    if not np.isfinite(attention).all() or (attention < 0).any():
        raise ValueError("attention scores must be finite and nonnegative")
    if not np.isfinite(prior).all() or (prior < 0).any():
        raise ValueError("prior scores must be finite and nonnegative")
    if not 0 < budget <= len(attention) or not 0 <= decay <= 1 or not 0 < top_p <= 1:
        raise ValueError("invalid budget, decay, or top-p threshold")
    scores = np.zeros_like(attention)
    scores[:len(prior)] = prior
    hits = np.zeros(len(attention), dtype=bool)
    total_attention = float(attention.sum())
    if total_attention > 0:
        ordered = np.argsort(-attention, kind="stable")
        cumulative = 0.0
        for index in ordered:
            if cumulative >= top_p * total_attention:
                break
            hits[index] = True
            cumulative += float(attention[index])
    scores = decay * scores + np.where(hits, attention, 0.0)
    selected = np.argsort(-scores, kind="stable")[:budget]
    retained = tuple(sorted(int(index) for index in selected))
    return EvictionResult(
        retained_indices=retained,
        keep_scores=tuple(float(scores[index]) for index in retained),
        hit_indices=tuple(int(index) for index in np.flatnonzero(hits)),
    )
