"""Extracted unchanged from auto_research.post_training.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def olive_loss(student_logits, teacher_tokens, prefix_lengths):
    """Cross entropy only on teacher continuations sampled after student prefixes."""
    import torch
    import torch.nn.functional as F

    if student_logits.shape[:-1] != teacher_tokens.shape:
        raise ValueError("token and logit shapes do not align")
    positions = torch.arange(teacher_tokens.shape[1], device=teacher_tokens.device)[None]
    mask = positions >= torch.as_tensor(prefix_lengths, device=teacher_tokens.device)[:, None]
    losses = F.cross_entropy(student_logits.transpose(1, 2), teacher_tokens, reduction="none")
    return (losses * mask).sum() / mask.sum().clamp_min(1), mask
