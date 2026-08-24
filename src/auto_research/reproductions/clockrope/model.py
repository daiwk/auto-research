from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores


def periodic_kernel(delta_hours: np.ndarray, periods=(24.0, 168.0), concentration: float = 4.0):
    """Periodic-Gaussian ClockRoPE prior induced by discrete Fourier harmonics."""
    values = np.zeros_like(delta_hours, dtype=np.float64)
    for period in periods:
        values += np.exp(concentration * (np.cos(2 * np.pi * delta_hours / period) - 1.0))
    return values / len(periods)


def clockrope_scores(data, history, event_hours):
    recent = tuple(history[-12:])
    hours = np.asarray(event_hours[-len(recent):], dtype=np.float64)
    delta = hours[-1] - hours
    weights = periodic_kernel(delta)
    weights /= max(float(weights.sum()), 1e-12)
    periodic_transition = weights @ data.transition[list(recent)]
    periodic_content = weights @ data.cosine[list(recent)]
    return 0.55 * periodic_transition + 0.30 * periodic_content + 0.15 * data.popularity


def rope_baseline_scores(data, history, event_hours):
    del event_hours
    return base_scores(data, history)
