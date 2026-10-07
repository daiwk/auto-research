"""Extracted unchanged from auto_research.foundation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def ce_guided_router(native_logits, predicted_error, *, gamma: float = 1.0, tau: float = 1.0):
    """Error-aware MoE affinity attenuation from Eq. 5--7."""
    import torch

    if native_logits.shape != predicted_error.shape or tau <= 0 or gamma < 0:
        raise ValueError("invalid CE-guided router inputs")
    adjusted = native_logits - gamma * torch.log1p(predicted_error.clamp_min(0) / tau)
    return torch.softmax(adjusted, dim=-1), adjusted
