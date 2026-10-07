"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def token_policy_gradient_loss(student_log_prob, token_advantage, response_mask):
    """Token-mean policy-gradient surrogate shared by SIPO diagnostics."""
    if not (student_log_prob.shape == token_advantage.shape == response_mask.shape):
        raise ValueError("student scores, advantage and mask must match")
    mask = response_mask.to(student_log_prob.dtype)
    return -(student_log_prob * token_advantage.detach() * mask).sum() / mask.sum().clamp_min(1)
