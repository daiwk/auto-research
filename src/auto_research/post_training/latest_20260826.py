"""Post-training mechanisms from the 2026-08-26 public arXiv batch."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"opd-search-plus", "opdvr"}


def update_latest(
    algorithm, state, group, probabilities, reference,
    rollout_training_probabilities, sampled, rng,
):
    """Return an executable candidate-policy analogue of each paper objective."""
    del state, rollout_training_probabilities, rng
    features = group.features
    rewards = group.rewards[sampled]
    expected = probabilities @ features
    sampled_probabilities = probabilities[sampled]
    # The compact candidate suite has no neural teacher.  Construct the frozen
    # teacher distribution once from the reference policy plus the process and
    # outcome signals available in each candidate group; unlike the trainable
    # policy, this distribution is not updated by the objective below.
    teacher_logits = np.log(reference + 1e-12)
    teacher_logits += 0.70 * group.rewards[:, 2] + 0.35 * group.rewards[:, 0]
    teacher_distribution = np.exp(teacher_logits - teacher_logits.max())
    teacher_distribution /= teacher_distribution.sum()
    teacher_probabilities = teacher_distribution[sampled]

    if algorithm == "opd-search-plus":
        # Stage 1: clipped forward-KL weights provide token-level teacher
        # guidance for reasoning/query/answer positions.  The process axis in
        # this candidate suite is the observable analogue of search evidence.
        ratio = np.clip(
            teacher_probabilities / (sampled_probabilities + 1e-12), 0.25, 4.0
        )
        evidence = 0.5 + 0.5 * rewards[:, 2]
        distillation_advantage = ratio * evidence
        distillation_advantage -= distillation_advantage.mean()
        # Stage 2: verifier RL moves beyond the frozen teacher ceiling.
        outcome = rewards[:, 0]
        rl_advantage = (outcome - outcome.mean()) / (outcome.std() + 1e-6)
        advantages = 0.55 * distillation_advantage + 0.45 * rl_advantage
        diagnostics = {
            "forward_kl_ratio_mean": float(ratio.mean()),
            "search_evidence_mean": float(evidence.mean()),
            "rl_refinement_advantage_mean_abs": float(np.abs(rl_advantage).mean()),
            "teacher_finetuning_calls": 0.0,
        }
    elif algorithm == "opdvr":
        # The sampled-token OPD implicit reward is log(pi_T/pi_theta).
        # OPDVR's ReLU gate enforces positive rewards on verifier-correct
        # trajectories and negative rewards on verifier-incorrect trajectories.
        implicit = np.log(
            (teacher_probabilities + 1e-12) / (sampled_probabilities + 1e-12)
        )
        correct = rewards[:, 0] >= np.median(group.rewards[:, 0])
        gated_reward = np.where(correct, np.maximum(implicit, 0.0), -np.maximum(-implicit, 0.0))
        advantages = gated_reward - gated_reward.mean()
        diagnostics = {
            "implicit_opd_reward_mean": float(implicit.mean()),
            "relu_gated_reward_mean": float(gated_reward.mean()),
            "correct_trajectory_fraction": float(correct.mean()),
            "extra_loss_hyperparameters": 0.0,
        }
    else:  # pragma: no cover - guarded by the public config
        raise ValueError(f"unsupported latest algorithm: {algorithm}")

    gradient = np.stack([
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(sampled, advantages)
    ]).mean(0)
    loss = float(-np.mean(advantages * np.log(sampled_probabilities + 1e-12)))
    return gradient, loss, diagnostics
