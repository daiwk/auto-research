"""Recommendation kernels from the Oct-1 intake batch."""

from __future__ import annotations


def recap_recursive_routes(features, shared_block, *, routes: int, ema_decay: float):
    """Weight-shared recursive routes, inference averaging and trajectory EMA."""
    import torch

    if routes < 1 or not 0 <= ema_decay < 1:
        raise ValueError("invalid RECAP recursion configuration")
    hidden = features
    outputs = []
    ema = None
    for _ in range(routes):
        hidden = shared_block(hidden)
        outputs.append(hidden)
        ema = hidden.detach() if ema is None else ema_decay * ema + (1 - ema_decay) * hidden.detach()
    stacked = torch.stack(outputs, dim=0)
    return stacked.mean(0), {"routes": stacked, "trajectory_ema": ema}


def cohortmix_prior(membership, historical_success, historical_failure, *, alpha0: float, beta0: float, strength: float):
    """Metadata-conditioned fixed-strength Beta mixture prior."""
    import numpy as np

    membership = np.asarray(membership, dtype=np.float64)
    success = np.asarray(historical_success, dtype=np.float64)
    failure = np.asarray(historical_failure, dtype=np.float64)
    if success.shape != failure.shape or success.ndim != 2 or membership.shape != (success.shape[0],):
        raise ValueError("membership=[groups], history=[groups,arms]")
    if not np.isclose(membership.sum(), 1) or min(alpha0, beta0, strength) <= 0:
        raise ValueError("invalid mixture or pseudo-counts")
    mean = (alpha0 + success) / (alpha0 + beta0 + success + failure)
    alpha_h = strength * mean
    beta_h = strength * (1 - mean)
    return membership @ alpha_h, membership @ beta_h


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


def cohortmix_update(alpha, beta, chosen, rewards):
    """Independent user posterior update after one slate."""
    import numpy as np

    alpha = np.asarray(alpha, dtype=np.float64).copy()
    beta = np.asarray(beta, dtype=np.float64).copy()
    for arm, reward in zip(chosen, rewards):
        if reward not in (0, 1):
            raise ValueError("bandit rewards must be binary")
        alpha[arm] += reward
        beta[arm] += 1 - reward
    return alpha, beta
