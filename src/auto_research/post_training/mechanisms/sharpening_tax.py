"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def sharpening_tax(base_success, post_success, *, samples: int):
    """Measure coverage lost after post-training at a fixed sampling budget."""
    import torch

    base_coverage = 1 - (1 - base_success).pow(samples)
    post_coverage = 1 - (1 - post_success).pow(samples)
    return base_coverage - post_coverage
