"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def dr_opd_reverse_kl(student_log_prob, teacher_log_prob, token_weights, response_mask):
    """Sampled weighted reverse-KL gradient target used after the Dr. OPD solve."""
    if not (student_log_prob.shape == teacher_log_prob.shape == token_weights.shape == response_mask.shape):
        raise ValueError("all token tensors must share a shape")
    gap = student_log_prob - teacher_log_prob.detach()
    mask = response_mask.to(gap.dtype)
    return (token_weights.detach() * gap * mask).sum() / mask.sum().clamp_min(1)
