"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def roft_retrospection_loss(logits, target_ids, target_mask):
    """Globally averaged next-token CE over retrospection tokens only.

    ``target_mask`` must be zero for the task, trajectory, observations and
    feedback.  Gradients may still flow through those context representations,
    matching Eq. (1) of ROFT.
    """
    import torch
    import torch.nn.functional as F

    if logits.ndim != 3 or target_ids.shape != logits.shape[:2]:
        raise ValueError("logits must be [batch, time, vocab] and ids [batch, time]")
    if target_mask.shape != target_ids.shape:
        raise ValueError("target_mask must match target_ids")
    losses = F.cross_entropy(
        logits.reshape(-1, logits.shape[-1]),
        target_ids.reshape(-1),
        reduction="none",
    ).reshape_as(target_ids)
    mask = target_mask.to(dtype=losses.dtype)
    token_count = mask.sum()
    if token_count.item() <= 0:
        raise ValueError("at least one retrospection target token is required")
    return (losses * mask).sum() / token_count
