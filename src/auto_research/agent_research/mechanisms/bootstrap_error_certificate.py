"""Extracted unchanged from auto_research.agent_research.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def bootstrap_error_certificate(task_errors, *, budget: float, confidence: float = 0.95, samples: int = 2000, seed: int = 0):
    """Task-cluster bootstrap upper error bound for selective automation."""
    import numpy as np

    errors = [np.asarray(values, dtype=np.float64) for values in task_errors]
    if not errors or not 0 < confidence < 1 or not 0 <= budget <= 1:
        raise ValueError("invalid clustered errors or certificate parameters")
    rng = np.random.default_rng(seed)
    means = []
    for _ in range(samples):
        selected = rng.integers(0, len(errors), len(errors))
        values = np.concatenate([errors[index] for index in selected])
        means.append(values.mean())
    upper = float(np.quantile(means, confidence))
    return {"upper_error": upper, "certified": upper <= budget, "tasks": len(errors)}
