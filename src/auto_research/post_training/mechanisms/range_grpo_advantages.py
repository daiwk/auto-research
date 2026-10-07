"""Extracted unchanged from auto_research.post_training.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def range_grpo_advantages(lower, upper):
    """Range-GRPO pairwise interval advantages.

    Non-overlapping intervals receive signed confidence proportional to their
    separation. Overlap produces no unjustified ordering. Point intervals
    reduce to the usual pairwise relative-score signal.
    """
    import torch

    lower = torch.as_tensor(lower)
    upper = torch.as_tensor(upper, device=lower.device, dtype=lower.dtype)
    if lower.ndim != 1 or lower.shape != upper.shape or torch.any(lower > upper):
        raise ValueError("reward intervals must be aligned one-dimensional bounds")
    left = lower[:, None]
    right = upper[:, None]
    separation = torch.where(
        left > upper[None, :],
        left - upper[None, :],
        torch.where(right < lower[None, :], right - lower[None, :], 0.0),
    )
    scale = (upper - lower)[:, None] + (upper - lower)[None, :] + 1.0
    return (separation / scale).mean(-1)
