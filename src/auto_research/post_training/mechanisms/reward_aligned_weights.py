"""Extracted unchanged from auto_research.post_training.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def reward_aligned_weights(teacher_logp, student_logp, outcome_agreement, *, floor=0.1):
    """R²-OPD reallocates dense supervision by outcome and policy disagreement."""
    import torch

    if teacher_logp.shape != student_logp.shape or outcome_agreement.shape != teacher_logp.shape[:-1]:
        raise ValueError("outcome agreement must align with token distributions")
    disagreement = (teacher_logp.detach().exp() * (teacher_logp.detach() - student_logp.detach())).sum(-1).clamp_min(0)
    raw = outcome_agreement.to(disagreement.dtype).clamp(0, 1) * (1 + disagreement)
    return (raw + floor) / (raw.mean().clamp_min(1e-12) + floor)
