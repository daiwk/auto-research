"""Extracted unchanged from auto_research.recommendation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



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
