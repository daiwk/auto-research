"""Extracted unchanged from auto_research.post_training.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def interpolated_policy(student_prob, teacher_prob, gamma: float):
    """IPD token policy m_gamma=(1-gamma)pi_student+gamma*pi_teacher."""
    if student_prob.shape != teacher_prob.shape or not 0 <= gamma <= 1:
        raise ValueError("invalid interpolated-policy inputs")
    return (1 - gamma) * student_prob + gamma * teacher_prob
