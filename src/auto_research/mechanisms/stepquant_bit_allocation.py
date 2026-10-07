"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations

import math

def stepquant_bit_allocation(distortions, log_retention, bit_options, average_bits: float, sizes=None):
    """Solve STEPQuant Eq. (8) by exact multiple-choice dynamic programming.

    ``distortions[u, j]`` is the calibrated distortion for unit ``u`` at
    ``bit_options[j]``.  The returned map is fixed across requests, matching
    the paper's post-training calibration contract.
    """
    import numpy as np

    distortions = np.asarray(distortions, dtype=np.float64)
    retention = np.asarray(log_retention, dtype=np.float64)
    bits = tuple(int(value) for value in bit_options)
    if distortions.ndim != 2 or distortions.shape[1] != len(bits):
        raise ValueError("distortions must be [units, bit options]")
    if retention.shape != (distortions.shape[0],):
        raise ValueError("one log-retention value is required per unit")
    sizes = np.ones(distortions.shape[0], dtype=np.int64) if sizes is None else np.asarray(sizes, dtype=np.int64)
    if sizes.shape != retention.shape or np.any(sizes <= 0):
        raise ValueError("sizes must be positive and match units")
    budget = int(math.floor(float(average_bits) * int(sizes.sum())))
    weights = np.asarray([
        sum(math.exp(2 * step * value) for step in range(128)) for value in retention
    ])
    states = {0: (0.0, ())}
    for unit in range(distortions.shape[0]):
        next_states = {}
        for used, (cost, choices) in states.items():
            for option, bit in enumerate(bits):
                total = used + bit * int(sizes[unit])
                if total > budget:
                    continue
                candidate = (cost + weights[unit] * distortions[unit, option], choices + (bit,))
                if total not in next_states or candidate[0] < next_states[total][0]:
                    next_states[total] = candidate
        states = next_states
    if not states:
        raise ValueError("bit budget cannot accommodate the minimum precision")
    used = min(states, key=lambda value: (states[value][0], -value))
    return {"bits": np.asarray(states[used][1], dtype=np.int64), "weighted_distortion": states[used][0], "used_bits": used, "budget_bits": budget}
