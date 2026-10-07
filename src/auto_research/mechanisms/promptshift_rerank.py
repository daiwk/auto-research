"""Extracted unchanged from auto_research.recommendation_latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def promptshift_rerank(items, scores, slice_popularity, mainstreamness):
    """Adaptive interpolation with inverse slice popularity."""
    import numpy as np

    items = np.asarray(items, dtype=np.int64)
    scores = np.asarray(scores, dtype=np.float64)
    popularity = np.asarray(slice_popularity, dtype=np.float64)[items]
    if scores.shape != items.shape or not 0 <= mainstreamness <= 1:
        raise ValueError("scores must align with items and mainstreamness must be in [0,1]")
    score_norm = (scores - scores.min()) / max(float(scores.max() - scores.min()), 1e-12)
    combined = (1 - mainstreamness) * score_norm + mainstreamness * (1 - popularity)
    order = np.argsort(-combined, kind="stable")
    return items[order], combined[order]
