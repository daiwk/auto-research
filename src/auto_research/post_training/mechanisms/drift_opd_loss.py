"""Extracted unchanged from auto_research.post_training.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def drift_opd_loss(student_logits, one_step_teacher_logits, future_potential, *, potential_weight: float):
    """One-step reverse-KL plus the offline future-potential correction."""
    import torch.nn.functional as F

    student_log = F.log_softmax(student_logits, dim=-1)
    student = student_log.exp()
    teacher_log = F.log_softmax(one_step_teacher_logits.detach(), dim=-1)
    reverse_kl = (student * (student_log - teacher_log)).sum(-1).mean()
    return reverse_kl - potential_weight * future_potential.mean()
