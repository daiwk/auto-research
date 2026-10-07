"""Extracted unchanged from auto_research.foundation_latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def telescopic_loss(logits_by_depth, targets, sampled_depth: int, *, anchor_weight: float = 1.0):
    """Stochastic prefix supervision plus the mandatory full-capacity anchor."""
    import torch.nn.functional as F

    if not 1 <= sampled_depth <= len(logits_by_depth):
        raise ValueError("sampled depth is outside the model")
    sampled = F.cross_entropy(logits_by_depth[sampled_depth - 1].reshape(-1, logits_by_depth[0].shape[-1]), targets.reshape(-1))
    anchor = F.cross_entropy(logits_by_depth[-1].reshape(-1, logits_by_depth[0].shape[-1]), targets.reshape(-1))
    return sampled + anchor_weight * anchor, {
        "sampled_depth": sampled_depth, "sampled_loss": float(sampled.detach()),
        "anchor_loss": float(anchor.detach()),
    }
