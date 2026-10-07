"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def token_level_video_credit(reward_gradient, *, group_advantage: float):
    """Normalize frozen-VLM gradient magnitudes into dense TVRL credit."""
    import torch

    credit = reward_gradient.norm(dim=-1)
    credit = credit / credit.mean(dim=-1, keepdim=True).clamp_min(1e-12)
    return credit.detach() * group_advantage
