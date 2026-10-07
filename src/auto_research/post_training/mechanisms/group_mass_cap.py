"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def group_mass_cap(importance_ratios, *, mass_cap: float):
    """Cap total importance mass per rollout group and renormalize."""
    import torch

    if mass_cap <= 0:
        raise ValueError("mass_cap must be positive")
    ratios = importance_ratios.clamp_min(0)
    scale = torch.minimum(torch.ones_like(ratios.sum(-1)), mass_cap / ratios.sum(-1).clamp_min(1e-12))
    return ratios * scale.unsqueeze(-1)
