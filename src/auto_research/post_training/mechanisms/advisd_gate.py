"""Extracted unchanged from auto_research.post_training.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def advisd_gate(contrasts, donor_contrasts, abstentions, *, quantile: float):
    """Keep abstentions and issued advice above the donor-calibrated gate."""
    import torch

    if not 0 < quantile < 1 or contrasts.shape != abstentions.shape:
        raise ValueError("invalid AdviSD gate inputs")
    threshold = torch.quantile(donor_contrasts.abs(), quantile)
    selected = abstentions.bool() | (contrasts.abs() > threshold)
    return selected, threshold
