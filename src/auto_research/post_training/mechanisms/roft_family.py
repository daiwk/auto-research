"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

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
