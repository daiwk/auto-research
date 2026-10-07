"""Extracted unchanged from auto_research.recommendation_latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations

from typing import Callable, Iterable

def promptshift_metrics(reference, cued, slice_popularity, relevant: Iterable[int], *, k=20):
    """PromptShift Drift, SliceShift and difficulty-weighted hit diagnostics."""
    import numpy as np

    reference = list(reference)[:k]
    cued = list(cued)[:k]
    if len(reference) != len(cued) or len(set(reference)) != len(reference) or len(set(cued)) != len(cued):
        raise ValueError("rankings must be equally sized and contain unique items")
    popularity = np.asarray(slice_popularity, dtype=np.float64)
    overlap = len(set(reference) & set(cued)) / max(1, len(reference))
    common = set(reference) & set(cued)
    rank_shift = sum(abs(reference.index(item) - cued.index(item)) for item in common)
    rank_shift /= max(1, len(common) * max(1, len(reference) - 1))
    drift = 0.5 * (1 - overlap) + 0.5 * rank_shift
    slice_shift = float(np.mean([popularity[item] for item in cued]) - np.mean([
        popularity[item] for item in reference
    ]))
    relevant = set(relevant)
    difficulty = sum(
        (1.0 / (rank + 1)) * (1.0 - popularity[item])
        for rank, item in enumerate(cued) if item in relevant
    )
    return {"drift": float(drift), "slice_shift": slice_shift,
            "difficulty_at_k": float(difficulty)}
