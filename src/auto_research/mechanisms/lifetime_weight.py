"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def lifetime_weight(log_retention, horizon: int):
    """STEPQuant Eq. (7), including the stable unit-retention limit."""
    import torch

    if horizon < 1:
        raise ValueError("horizon must be positive")
    ratio = torch.exp(2 * log_retention)
    denominator = 1 - ratio
    geometric = (1 - ratio.pow(horizon)) / denominator.clamp_min(1e-12)
    return torch.where(denominator.abs() < 1e-8, torch.full_like(ratio, float(horizon)), geometric)
