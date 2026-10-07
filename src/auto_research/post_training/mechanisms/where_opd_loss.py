"""Extracted unchanged from auto_research.post_training.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def where_opd_loss(student_logits, privileged_teacher_logits, spatial_mask):
    """Where-OPD privileged-spatial teacher KL on student on-policy tokens."""
    import torch
    import torch.nn.functional as F

    if student_logits.shape != privileged_teacher_logits.shape:
        raise ValueError("student and teacher logits must align")
    if spatial_mask.shape != student_logits.shape[:-1]:
        raise ValueError("spatial mask must align with token positions")
    student_logp = F.log_softmax(student_logits, dim=-1)
    with torch.no_grad():
        teacher = F.softmax(privileged_teacher_logits, dim=-1)
    token_kl = F.kl_div(student_logp, teacher, reduction="none").sum(-1)
    weights = spatial_mask.to(token_kl.dtype)
    return (token_kl * weights).sum() / weights.sum().clamp_min(1.0)
