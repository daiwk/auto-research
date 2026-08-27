"""Post-training objectives from the 2026-08-27 arXiv announcement batch."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"v-rubrics", "clue-opsd", "grin", "grip"}


def update_latest(
    algorithm, state, group, probabilities, reference,
    rollout_training_probabilities, sampled, rng,
):
    del state, rng
    features = group.features
    rewards = group.rewards[sampled]
    sampled_probabilities = probabilities[sampled]
    expected = probabilities @ features

    if algorithm == "v-rubrics":
        # VF, RC and IF are represented by the outcome, process and format
        # axes in the shared candidate suite. Prefix localization gives early
        # visual-grounding credit a larger share than terminal-only rewards.
        components = rewards[:, [0, 2, 3]]
        localized = components @ np.asarray([0.45, 0.35, 0.20])
        scalar = rewards[:, 0]
        advantages = 0.5 * scalar + 0.5 * localized
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-6)
        diagnostics = {
            "visual_faithfulness_credit": float(components[:, 0].mean()),
            "reasoning_consistency_credit": float(components[:, 1].mean()),
            "instruction_following_credit": float(components[:, 2].mean()),
            "prefix_localized_fraction": 0.5,
        }
    elif algorithm == "clue-opsd":
        teacher_logits = np.log(reference + 1e-12) + 0.9 * group.rewards[:, 2]
        teacher = np.exp(teacher_logits - teacher_logits.max())
        teacher /= teacher.sum()
        implicit = np.log((teacher[sampled] + 1e-12) / (sampled_probabilities + 1e-12))
        advantages = implicit - implicit.mean()
        diagnostics = {
            "clue_teacher_process_reward": float(group.rewards[:, 2].mean()),
            "student_full_context_fraction": 1.0,
            "inference_clue_annotations": 0.0,
            "ema_teacher_update_rate": 0.99,
        }
    elif algorithm == "grin":
        on_policy = rollout_training_probabilities[sampled]
        failed = rewards[:, 0] <= np.median(group.rewards[:, 0])
        golden_index = int(np.argmax(group.rewards[:, 0] + 0.35 * group.rewards[:, 2]))
        golden = np.zeros_like(rewards[:, 0])
        golden[sampled == golden_index] = 1.0
        mixed = np.where(failed, golden, rewards[:, 0])
        importance = sampled_probabilities / (on_policy + 1e-12)
        advantages = importance * mixed
        advantages -= advantages.mean()
        diagnostics = {
            "failed_rollout_fraction": float(failed.mean()),
            "golden_answer_injection_fraction": float(failed.mean()),
            "mixed_policy_importance_mean": float(importance.mean()),
            "sft_loss_weight": 0.0,
        }
    elif algorithm == "grip":
        granular = rewards @ np.asarray([0.45, 0.10, 0.35, 0.10])
        alpha = np.clip((granular - granular.min()) / (np.ptp(granular) + 1e-6), 0.0, 1.0)
        interpolated = alpha * sampled_probabilities + (1 - alpha) * reference[sampled]
        advantages = granular - granular.mean()
        diagnostics = {
            "interpolation_alpha_mean": float(alpha.mean()),
            "granular_reward_mean": float(granular.mean()),
            "interpolated_policy_probability_mean": float(interpolated.mean()),
            "extra_rollout_calls": 0.0,
        }
    else:  # pragma: no cover
        raise ValueError(f"unsupported 20260827 algorithm: {algorithm}")

    gradient = np.stack([
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(sampled, advantages)
    ]).mean(0)
    loss = float(-np.mean(advantages * np.log(sampled_probabilities + 1e-12)))
    return gradient, loss, diagnostics
