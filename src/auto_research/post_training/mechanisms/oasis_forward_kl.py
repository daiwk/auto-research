"""Extracted unchanged from auto_research.post_training.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def oasis_forward_kl(student_log_prob, teacher_prob, token_mask, *, entry_clip: float = 5.0):
    """OASIS keeps the clipped OPSD forward-KL but masks to a verified scaffold."""
    if not (student_log_prob.shape == teacher_prob.shape):
        raise ValueError("student and teacher distributions must match")
    if token_mask.shape != student_log_prob.shape[:-1]:
        raise ValueError("token mask must match batch/time axes")
    contribution = teacher_prob * (teacher_prob.clamp_min(1e-12).log() - student_log_prob)
    mask = token_mask.to(contribution.dtype)[..., None]
    return contribution.clamp(max=entry_clip).mul(mask).sum() / mask.sum().clamp_min(1)
