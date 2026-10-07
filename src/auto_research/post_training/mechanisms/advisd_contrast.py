"""Extracted unchanged from auto_research.post_training.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def advisd_contrast(logp_with_advice, logp_without_advice):
    """Mean paired response contrast from AdviSD Eq. 3."""
    import torch

    if logp_with_advice.shape != logp_without_advice.shape:
        raise ValueError("paired scoring tensors must align")
    return (logp_with_advice - logp_without_advice).mean(-1)
