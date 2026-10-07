"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def sipo_token_advantage(
    rewards,
    positive_teacher_log_prob,
    negative_teacher_log_prob,
    valid_teacher_mask,
    *,
    teacher_weight: float = 0.5,
    evidence_clip: float = 0.2,
):
    """SIPO Eqs. (5)-(6): reward direction plus contrastive self-teacher credit."""
    import torch

    if positive_teacher_log_prob.shape != negative_teacher_log_prob.shape:
        raise ValueError("positive and negative teacher token scores must match")
    if positive_teacher_log_prob.shape[0] != rewards.shape[0]:
        raise ValueError("one reward per rollout is required")
    if valid_teacher_mask.shape != positive_teacher_log_prob.shape:
        raise ValueError("valid_teacher_mask must match token scores")
    group_advantage = rewards - rewards.mean()
    evidence = (positive_teacher_log_prob - negative_teacher_log_prob).detach()
    evidence = evidence.clamp(-evidence_clip, evidence_clip) * valid_teacher_mask.to(evidence.dtype)
    advantage = group_advantage[:, None] + teacher_weight * evidence
    return advantage, {
        "uniform_failure_group": bool((rewards == rewards[0]).all()),
        "teacher_covered_tokens": int(valid_teacher_mask.sum()),
        "mean_abs_evidence": float(evidence.abs().mean()),
    }
