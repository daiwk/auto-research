"""Extracted unchanged from auto_research.foundation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def pumba_window(step_fn, initial_logits, targets, *, window: int, detach_between_windows: bool = True):
    """Unroll consecutive denoising steps and backpropagate through the carry."""
    import torch.nn.functional as F

    if window < 1:
        raise ValueError("window must be positive")
    logits = initial_logits
    carry = None
    losses = []
    for step in range(window):
        logits, carry = step_fn(logits, carry, step)
        losses.append(F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1)))
    if detach_between_windows and carry is not None:
        carry = carry.detach()
    return sum(losses) / len(losses), carry, tuple(losses)
