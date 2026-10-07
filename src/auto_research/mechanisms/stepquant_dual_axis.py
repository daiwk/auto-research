"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def stepquant_dual_axis(state, row_impact, bits: int = 6, iterations: int = 4):
    """STEPQuant Eqs. (11)-(14): impact-aware row and column fitting."""
    import torch

    if state.ndim != 2 or row_impact.shape != state.shape[:1]:
        raise ValueError("state must be [key rows, value columns] with one row impact per row")
    eps = torch.finfo(state.dtype).eps
    magnitude = state.abs().mean(dim=1).clamp_min(eps)
    impact = row_impact.to(state).clamp_min(eps)
    row_scale = magnitude.sqrt() / impact.sqrt()
    column_scale = torch.ones(state.shape[1], device=state.device, dtype=state.dtype)
    limit = 2 ** (bits - 1) - 1
    for _ in range(iterations):
        normalized = state / (row_scale[:, None] * column_scale[None, :]).clamp_min(eps)
        codes = normalized.round().clamp(-limit, limit)
        numerator = ((impact[:, None] * row_scale[:, None] * codes) * (impact[:, None] * state)).sum(dim=0)
        denominator = (impact[:, None] * row_scale[:, None] * codes).square().sum(dim=0).clamp_min(eps)
        column_scale = (numerator / denominator).abs().clamp_min(eps)
    restored = row_scale[:, None] * column_scale[None, :] * codes
    return restored, {"row_scale": row_scale, "column_scale": column_scale, "codes": codes}
