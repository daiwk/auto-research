"""Extracted unchanged from auto_research.post_training.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def ross_selective_loss(logits, tokens, selected_continuations):
    """Keep full historical context but supervise only selected model continuations."""
    import torch.nn.functional as F

    if logits.shape[:-1] != tokens.shape or tokens.shape != selected_continuations.shape:
        raise ValueError("ROSS tensors must share batch/time axes")
    losses = F.cross_entropy(logits.transpose(1, 2), tokens, reduction="none")
    mask = selected_continuations.to(losses.dtype)
    return (losses * mask).sum() / mask.sum().clamp_min(1)
