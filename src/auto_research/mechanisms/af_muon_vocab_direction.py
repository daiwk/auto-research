"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def af_muon_vocab_direction(gradient, *, cap: float):
    """Support-aware finite-cap direction for a tied vocabulary table."""
    import torch

    if gradient.ndim != 2 or cap <= 0:
        raise ValueError("expected a vocabulary matrix and a positive cap")
    active = gradient.norm(dim=1) > 0
    direction = torch.zeros_like(gradient)
    if active.any():
        rows = gradient[active]
        direction[active] = rows / rows.norm(dim=1, keepdim=True).clamp_min(1e-12)
        direction[active] *= rows.norm(dim=1, keepdim=True).clamp(max=cap)
    return direction
