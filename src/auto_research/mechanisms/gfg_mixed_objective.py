"""Extracted unchanged from auto_research.foundation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def gfg_mixed_objective(current_loss, replay_loss, *, replay_fraction: float):
    """GfG mid-training blend that exposes the anti-forgetting trade-off."""
    if not 0 <= replay_fraction <= 1:
        raise ValueError("replay_fraction must be in [0, 1]")
    return (1 - replay_fraction) * current_loss + replay_fraction * replay_loss
