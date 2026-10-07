"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def carm_response_mask(current_log_probs, rollout_log_probs, *, threshold: float):
    """Cancellation-aware sequence gate using mean absolute log ratio."""
    import torch

    drift = (current_log_probs - rollout_log_probs).abs().mean(-1)
    return torch.exp(drift) <= threshold, drift
