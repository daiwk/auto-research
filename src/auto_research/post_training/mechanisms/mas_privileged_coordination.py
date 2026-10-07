"""Extracted unchanged from auto_research.post_training.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def mas_privileged_coordination(student_logp, teacher_logp, conflict_mask):
    """Teacher-only conflict attribution yields masked token distillation."""
    import torch.nn.functional as F

    if student_logp.shape != teacher_logp.shape or conflict_mask.shape != student_logp.shape[:-1]:
        raise ValueError("coordination tensors do not align")
    target = teacher_logp.detach().exp()
    kl = F.kl_div(student_logp, target, reduction="none").sum(-1)
    mask = conflict_mask.to(kl.dtype)
    return (kl * mask).sum() / mask.sum().clamp_min(1)
