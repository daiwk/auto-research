"""Extracted unchanged from auto_research.recommendation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



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
