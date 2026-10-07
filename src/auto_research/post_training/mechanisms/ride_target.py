"""Extracted unchanged from auto_research.post_training.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def ride_target(base_hidden, teacher_hidden, *, extrapolation: float = 1.5):
    """RIDE: extrapolate the RL-induced representation residual beyond teacher."""
    if base_hidden.shape != teacher_hidden.shape or extrapolation < 1:
        raise ValueError("hidden states must match and extrapolation must be >= 1")
    return base_hidden.detach() + extrapolation * (teacher_hidden.detach() - base_hidden.detach())

def ride_loss(student_hidden, base_hidden, teacher_hidden, *, extrapolation: float = 1.5, token_mask=None):
    import torch

    target = ride_target(base_hidden, teacher_hidden, extrapolation=extrapolation)
    squared = (student_hidden - target).square().mean(-1)
    if token_mask is None:
        return squared.mean()
    mask = token_mask.to(squared.dtype)
    return (squared * mask).sum() / mask.sum().clamp_min(1)
