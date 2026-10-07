"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def lspd_objective(
    student_log_prob,
    teacher_log_prob,
    entropy,
    response_mask,
    *,
    entropy_coeff: float = 0.01,
    huber_threshold: float = 5.0,
):
    """Practical LSPD objective from Eq. (4.6) and Appendix A.1.

    The response-level token means are averaged equally, the teacher is
    detached, and the Huber-style tail has bounded non-zero gradient.
    """
    import torch

    if student_log_prob.shape != teacher_log_prob.shape:
        raise ValueError("student and teacher log probabilities must match")
    if entropy.shape != student_log_prob.shape or response_mask.shape != student_log_prob.shape:
        raise ValueError("entropy and response_mask must match log probabilities")
    if huber_threshold <= 0:
        raise ValueError("huber_threshold must be positive")
    gap = student_log_prob - teacher_log_prob.detach()
    abs_gap = gap.abs()
    penalty = torch.where(
        abs_gap <= huber_threshold,
        gap.square(),
        2 * huber_threshold * abs_gap - huber_threshold**2,
    )
    mask = response_mask.to(dtype=penalty.dtype)
    counts = mask.sum(dim=-1)
    valid = counts > 0
    if not bool(valid.any()):
        raise ValueError("at least one response must contain a valid token")
    per_response_penalty = (penalty * mask).sum(dim=-1) / counts.clamp_min(1)
    per_response_entropy = (entropy * mask).sum(dim=-1) / counts.clamp_min(1)
    objective = (
        per_response_penalty[valid] - entropy_coeff * per_response_entropy[valid]
    ).mean()
    diagnostics = {
        "mean_penalty": float(per_response_penalty[valid].detach().mean()),
        "mean_entropy": float(per_response_entropy[valid].detach().mean()),
        "tail_fraction": float(((abs_gap > huber_threshold) * mask.bool()).sum().detach() / mask.sum()),
    }
    return objective, diagnostics
