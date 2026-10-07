"""Extracted unchanged from auto_research.foundation_latest_20260916; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

def loopspec_schedule(acceptance_by_depth, verify_cost: float = 1.0):
    """Select the first and residual proposal depths by expected saved work."""
    rates = np.asarray(acceptance_by_depth, dtype=np.float64)
    depths = np.arange(1, len(rates) + 1, dtype=np.float64)
    utility = rates * depths - verify_cost
    first = int(np.argmax(utility))
    residual = np.maximum(rates[first + 1:] - rates[first], 0.0)
    second = int(first + 1 + np.argmax(residual)) if len(residual) and residual.max() > 0 else first
    return first + 1, second + 1, {
        "expected_saved_depth": float(max(0.0, utility[first])),
        "residual_gate_open": float(second != first),
    }
