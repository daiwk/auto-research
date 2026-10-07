"""Extracted unchanged from auto_research.foundation_latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def frac_modes(mode_count: int, minimum_rate: float, maximum_rate: float, exponent: float):
    """Log-spaced positive exponential mixture approximating a power-law kernel."""
    import numpy as np

    if mode_count < 2 or not 0 < minimum_rate < maximum_rate or not 0 < exponent < 1:
        raise ValueError("invalid fractional-mode configuration")
    rates = np.geomspace(minimum_rate, maximum_rate, mode_count)
    weights = rates ** exponent
    weights /= weights.sum()
    return rates, weights
