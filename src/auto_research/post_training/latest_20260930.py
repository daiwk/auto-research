"""Executable mechanisms for ROFT and Least Square Policy Distillation.

The tensor objectives in this module are faithful to the papers.  The
candidate-policy ``update_latest`` hook is intentionally only an L1 diagnostic
for the repository's small post-training runner; it is not an LLM result.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

import numpy as np


def roft_retrospection_loss(logits, target_ids, target_mask):
    """Globally averaged next-token CE over retrospection tokens only.

    ``target_mask`` must be zero for the task, trajectory, observations and
    feedback.  Gradients may still flow through those context representations,
    matching Eq. (1) of ROFT.
    """
    import torch
    import torch.nn.functional as F

    if logits.ndim != 3 or target_ids.shape != logits.shape[:2]:
        raise ValueError("logits must be [batch, time, vocab] and ids [batch, time]")
    if target_mask.shape != target_ids.shape:
        raise ValueError("target_mask must match target_ids")
    losses = F.cross_entropy(
        logits.reshape(-1, logits.shape[-1]),
        target_ids.reshape(-1),
        reduction="none",
    ).reshape_as(target_ids)
    mask = target_mask.to(dtype=losses.dtype)
    token_count = mask.sum()
    if token_count.item() <= 0:
        raise ValueError("at least one retrospection target token is required")
    return (losses * mask).sum() / token_count


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


def dr_opd_token_weights(
    teacher_student_log_ratio,
    reward_directional_derivative,
    *,
    strength: float = 1.0,
    minimum: float = 0.1,
    maximum: float = 3.0,
    epsilon: float = 1e-6,
):
    """Dr. OPD Eqs. (12)-(14): credit-aware closed-form token weights.

    The caller supplies the JVP directional derivative along the sampled
    reward gradient.  Keeping that interface explicit prevents this L1 kernel
    from pretending that a heuristic score is the paper's model-space JVP.
    """
    import torch

    if teacher_student_log_ratio.shape != reward_directional_derivative.shape:
        raise ValueError("discrepancy and reward directional derivative must match")
    if not 0 < minimum <= maximum:
        raise ValueError("weight bounds must be positive and ordered")
    credits = teacher_student_log_ratio.detach() * reward_directional_derivative.detach()
    rms = credits.square().mean().sqrt().clamp_min(epsilon)
    weights = (1 + strength * credits / rms).clamp(minimum, maximum)
    return weights, {"credit_rms": float(rms), "minimum_weight": float(weights.min()), "maximum_weight": float(weights.max())}


def dr_opd_reverse_kl(student_log_prob, teacher_log_prob, token_weights, response_mask):
    """Sampled weighted reverse-KL gradient target used after the Dr. OPD solve."""
    if not (student_log_prob.shape == teacher_log_prob.shape == token_weights.shape == response_mask.shape):
        raise ValueError("all token tensors must share a shape")
    gap = student_log_prob - teacher_log_prob.detach()
    mask = response_mask.to(gap.dtype)
    return (token_weights.detach() * gap * mask).sum() / mask.sum().clamp_min(1)


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


def token_policy_gradient_loss(student_log_prob, token_advantage, response_mask):
    """Token-mean policy-gradient surrogate shared by SIPO diagnostics."""
    if not (student_log_prob.shape == token_advantage.shape == response_mask.shape):
        raise ValueError("student scores, advantage and mask must match")
    mask = response_mask.to(student_log_prob.dtype)
    return -(student_log_prob * token_advantage.detach() * mask).sum() / mask.sum().clamp_min(1)


@dataclass(frozen=True)
class ReplayItem:
    student_log_prob: np.ndarray
    teacher_log_prob: np.ndarray


class LSPDReplayBuffer:
    """Bounded FIFO replay of off-policy query-response token statistics."""

    def __init__(self, capacity: int = 256):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._items: deque[ReplayItem] = deque(maxlen=capacity)

    def append(self, student_log_prob, teacher_log_prob) -> None:
        student = np.asarray(student_log_prob, dtype=np.float64).copy()
        teacher = np.asarray(teacher_log_prob, dtype=np.float64).copy()
        if student.shape != teacher.shape:
            raise ValueError("student and teacher log probabilities must match")
        self._items.append(ReplayItem(student, teacher))

    def sample(self, size: int, rng: np.random.Generator) -> list[ReplayItem]:
        if not self._items:
            raise ValueError("cannot sample an empty replay buffer")
        indices = rng.choice(len(self._items), size=min(size, len(self._items)), replace=False)
        return [self._items[int(index)] for index in indices]

    def __len__(self) -> int:
        return len(self._items)


def update_latest(algorithm, state, group, probabilities, reference, sampled, rng):
    """L1 candidate-policy analog used by the generic post-training CLI."""
    rewards = group.rewards[sampled] @ np.asarray((0.7, 0.05, 0.2, 0.05))
    expected = probabilities @ group.features
    if algorithm == "roft":
        # The residual is a compact diagnostic analogue of a self-generated
        # correction; the actual masked-token objective is tested separately.
        correction = rewards - rewards.mean()
        advantages = correction
        diagnostics = {
            "retrospection_targets": float(len(sampled)),
            "action_targets": 0.0,
            "reward_policy_update": 0.0,
            "diagnostic_only": 1.0,
        }
    elif algorithm == "lspd":
        student_logp = np.log(probabilities[sampled] + 1e-12)
        teacher_logp = np.log(reference[sampled] + 1e-12)
        gap = student_logp - teacher_logp
        threshold = 5.0
        robust_gradient = np.where(
            np.abs(gap) <= threshold,
            2 * gap,
            2 * threshold * np.sign(gap),
        )
        advantages = -robust_gradient
        advantages -= advantages.mean()
        diagnostics = {
            "mean_logprob_gap": float(np.abs(gap).mean()),
            "replay_compatible": 1.0,
            "diagnostic_only": 1.0,
        }
    else:  # pragma: no cover
        raise ValueError(algorithm)
    gradient = np.zeros_like(state.weights)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (group.features[index] - expected)
    gradient /= max(1, len(sampled))
    return gradient, float(np.mean(np.abs(advantages))), diagnostics
