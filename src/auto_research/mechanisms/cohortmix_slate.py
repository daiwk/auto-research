"""Extracted unchanged from auto_research.recommendation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def cohortmix_slate(alpha, beta, *, size: int, unseen=None, seed: int = 0):
    """One Thompson draw per arm and no-repeat slate construction."""
    import numpy as np

    alpha = np.asarray(alpha, dtype=np.float64)
    beta = np.asarray(beta, dtype=np.float64)
    if alpha.shape != beta.shape or size < 1 or np.any(alpha <= 0) or np.any(beta <= 0):
        raise ValueError("invalid Beta posterior")
    mask = np.ones(len(alpha), dtype=bool) if unseen is None else np.asarray(unseen, dtype=bool)
    if mask.shape != alpha.shape or mask.sum() < size:
        raise ValueError("not enough unseen arms")
    rng = np.random.default_rng(seed)
    draws = rng.beta(alpha, beta)
    eligible = np.flatnonzero(mask)
    chosen = eligible[np.argsort(draws[eligible])[-size:][::-1]]
    return tuple(int(index) for index in chosen), draws
