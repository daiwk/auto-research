"""Executable L1 mechanisms for the 2026-09-19 post-training batch."""

from __future__ import annotations

import numpy as np


def adaptive_retirement(student_success, teacher_success, discrepancies, success_ratio: float = 0.9):
    """Retire a skill teacher once the student is capable and discrepancy plateaus."""
    student = np.asarray(student_success, dtype=np.float64)
    teacher = np.asarray(teacher_success, dtype=np.float64)
    gap = np.asarray(discrepancies, dtype=np.float64)
    capable = student >= success_ratio * np.maximum(teacher, 1e-8)
    shrinking = np.r_[True, np.diff(gap) < -1e-6]
    active = ~(capable & ~shrinking)
    return active, {
        "retired_fraction": float((~active).mean()),
        "student_teacher_ratio": float(student.mean() / max(teacher.mean(), 1e-8)),
        "discrepancy_improvement": float(gap[0] - gap[-1]) if len(gap) else 0.0,
    }


def comparison_oracle_direction(plus_scores, minus_scores, threshold: float = 0.0):
    """ComPO one-bit zeroth-order direction with entry-wise thresholding."""
    delta = np.asarray(plus_scores, dtype=np.float64) - np.asarray(minus_scores, dtype=np.float64)
    signs = np.sign(delta)
    keep = np.abs(delta) > threshold
    direction = signs * keep
    return direction, {
        "oracle_preference_rate": float((delta > 0).mean()),
        "active_coordinate_fraction": float(keep.mean()),
        "direction_norm": float(np.linalg.norm(direction)),
    }


def trajectory_learnability_weights(policy_logp, successful_reference_logp, temperature: float = 1.0):
    """Aggregate signed token likelihood changes into normalized trajectory weights."""
    policy = np.asarray(policy_logp, dtype=np.float64)
    reference = np.asarray(successful_reference_logp, dtype=np.float64)
    signed_gain = (reference - policy).mean(axis=-1)
    logits = signed_gain / max(temperature, 1e-8)
    weights = np.exp(logits - logits.max())
    weights /= weights.sum() + 1e-12
    return weights, {
        "learnability_entropy": float(-(weights * np.log(weights + 1e-12)).sum()),
        "positive_learnability_fraction": float((signed_gain > 0).mean()),
        "max_trajectory_weight": float(weights.max()),
    }


def update_latest(algorithm, state, group, probabilities, reference, rollout_training_probabilities, sampled, rng):
    del rollout_training_probabilities
    expected = probabilities @ group.features
    rewards = group.rewards[sampled] @ np.asarray((0.7, 0.05, 0.2, 0.05))
    if algorithm == "retire-opd":
        gap = np.abs(reference[sampled] - probabilities[sampled])
        active, diagnostics = adaptive_retirement(
            np.clip(rewards, 0, 1), np.ones_like(rewards), gap,
        )
        advantages = (rewards - rewards.mean()) * active
    elif algorithm == "compo":
        perturbation = rng.normal(size=len(sampled))
        direction, diagnostics = comparison_oracle_direction(
            rewards + 0.05 * perturbation, rewards - 0.05 * perturbation, threshold=0.01,
        )
        advantages = direction - direction.mean()
    elif algorithm == "trajectory-learnability":
        policy = np.log(probabilities[sampled] + 1e-12)[:, None] + group.features[sampled, :3]
        successful = np.log(reference[sampled] + 1e-12)[:, None] + 0.1 * group.rewards[sampled, :3]
        weights, diagnostics = trajectory_learnability_weights(policy, successful)
        advantages = weights * (rewards - np.sum(weights * rewards))
    else:  # pragma: no cover
        raise ValueError(algorithm)
    gradient = np.zeros_like(state.weights)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (group.features[index] - expected)
    gradient /= max(1, len(sampled))
    return gradient, float(np.mean(np.abs(advantages))), diagnostics
