"""Extracted unchanged from auto_research.recommendation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def effective_training_time(timeline):
    """Meta ETT% and independently owned lifecycle-loss accounting."""
    total = sum(float(duration) for duration in timeline.values())
    if total <= 0 or "training" not in timeline:
        raise ValueError("timeline requires positive training and wall time")
    losses = {stage: float(value) / total for stage, value in timeline.items() if stage != "training"}
    return float(timeline["training"]) / total, losses
