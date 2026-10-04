"""CMP balanced exposure and per-query utility estimation (Eq. 5, 6, 9).

This is a measurement tool, not a validated across-query memory eviction policy.
"""

from __future__ import annotations

import math
import numpy as np


def balanced_exposure(pool_size: int, timesteps: int, slots: int, *, seed: int = 42) -> np.ndarray:
    """Fixed row sums and column counts differing by at most one.

    A randomly permuted cyclic assignment then swaps 2x2 edges to diversify
    co-exposure without losing the balanced marginal assignment. No row can
    contain a duplicate memory. Every memory must have both exposed/control arms.
    """
    if pool_size < 2 or timesteps < 2 or not 0 < slots < pool_size:
        raise ValueError("require at least two memories/steps and 0 < slots < pool")
    if timesteps * slots < pool_size or math.ceil(timesteps * slots / pool_size) >= timesteps:
        raise ValueError("horizon does not provide positive exposed and control support")
    rng = np.random.default_rng(seed)
    labels = rng.permutation(pool_size)
    schedule = np.zeros((timesteps, pool_size), dtype=bool)
    for t in range(timesteps):
        schedule[t, labels[(np.arange(slots) + t * slots) % pool_size]] = True
    for _ in range(timesteps * pool_size * 4):
        a, b = rng.choice(timesteps, 2, replace=False)
        left, right = (
            np.flatnonzero(schedule[a] & ~schedule[b]),
            np.flatnonzero(schedule[b] & ~schedule[a]),
        )
        if len(left) and len(right):
            i, j = rng.choice(left), rng.choice(right)
            schedule[a, [i, j]] = [False, True]
            schedule[b, [i, j]] = [True, False]
    return schedule[rng.permutation(timesteps)]


def estimate_utility(exposure: np.ndarray, outcomes: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Balanced Hájek estimator = arm mean difference, plus estimated SE.

    Pass randomized-arm indicators, never guessed propensities from ranker hits.
    At least two observations per arm are needed for a variance estimate.
    """
    z, y = np.asarray(exposure), np.asarray(outcomes, dtype=float)
    if z.dtype != bool or z.ndim != 2 or y.shape != (len(z),) or not np.isfinite(y).all():
        raise ValueError("expected boolean exposure [time, memory] and finite outcomes")
    estimates, errors = [], []
    for exposed in z.T:
        positive, negative = y[exposed], y[~exposed]
        if min(len(positive), len(negative)) < 2:
            raise ValueError("each arm requires at least two observations")
        estimates.append(positive.mean() - negative.mean())
        errors.append(
            np.sqrt(positive.var(ddof=1) / len(positive) + negative.var(ddof=1) / len(negative))
        )
    return np.asarray(estimates), np.asarray(errors)


def query_decision(utility: float, standard_error: float, *, irreversibility: float = 10.0) -> str:
    """Eq. 9: forget only when its posterior loss is smaller; ties abstain."""
    if not math.isfinite(utility) or math.isnan(standard_error) or standard_error < 0:
        raise ValueError("invalid estimate or standard error")
    if not math.isfinite(irreversibility) or irreversibility < 1:
        raise ValueError("irreversibility must be finite and >= 1")
    if math.isinf(standard_error):
        return "noop"
    if standard_error == 0:
        return "forget" if utility < 0 else "noop"
    z = utility / standard_error
    positive = 0.5 * math.erfc(-z / math.sqrt(2))
    negative = 0.5 * math.erfc(z / math.sqrt(2))
    density = math.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)
    g = irreversibility * z * positive + z * negative + (irreversibility - 1) * density
    return "forget" if g < 0 else "noop"
