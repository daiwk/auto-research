"""Foundation-model reference kernels for the Sep-30 closure."""

from __future__ import annotations


def telescopic_loss(logits_by_depth, targets, sampled_depth: int, *, anchor_weight: float = 1.0):
    """Stochastic prefix supervision plus the mandatory full-capacity anchor."""
    import torch.nn.functional as F

    if not 1 <= sampled_depth <= len(logits_by_depth):
        raise ValueError("sampled depth is outside the model")
    sampled = F.cross_entropy(logits_by_depth[sampled_depth - 1].reshape(-1, logits_by_depth[0].shape[-1]), targets.reshape(-1))
    anchor = F.cross_entropy(logits_by_depth[-1].reshape(-1, logits_by_depth[0].shape[-1]), targets.reshape(-1))
    return sampled + anchor_weight * anchor, {
        "sampled_depth": sampled_depth, "sampled_loss": float(sampled.detach()),
        "anchor_loss": float(anchor.detach()),
    }


def frac_modes(mode_count: int, minimum_rate: float, maximum_rate: float, exponent: float):
    """Log-spaced positive exponential mixture approximating a power-law kernel."""
    import numpy as np

    if mode_count < 2 or not 0 < minimum_rate < maximum_rate or not 0 < exponent < 1:
        raise ValueError("invalid fractional-mode configuration")
    rates = np.geomspace(minimum_rate, maximum_rate, mode_count)
    weights = rates ** exponent
    weights /= weights.sum()
    return rates, weights


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
