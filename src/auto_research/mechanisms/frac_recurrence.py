"""Extracted unchanged from auto_research.foundation_latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def frac_recurrence(inputs, rates, weights, *, step: float = 1.0):
    """Bounded-state recurrent realization of the finite exponential mixture."""
    import numpy as np

    values = np.asarray(inputs, dtype=np.float64)
    rates = np.asarray(rates, dtype=np.float64)
    weights = np.asarray(weights, dtype=np.float64)
    if values.ndim != 2 or rates.ndim != 1 or rates.shape != weights.shape:
        raise ValueError("inputs=[time,features], rates/weights=[modes]")
    state = np.zeros((len(rates), values.shape[1]), dtype=np.float64)
    decay = np.exp(-rates * step)[:, None]
    output = []
    for value in values:
        state = decay * state + value
        output.append((weights[:, None] * state).sum(0))
    return np.asarray(output), state
