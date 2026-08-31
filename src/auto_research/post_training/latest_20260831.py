"""Post-training mechanisms retained from the 2026-08-27 late batch."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"rlvr-fusion", "video-opsd", "normalized-dpo"}


def _policy_gradient(features, probabilities, indices, advantages):
    expected = probabilities @ features
    rows = [
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(indices, advantages)
    ]
    return np.stack(rows).mean(0)


def update_latest(
    algorithm,
    state,
    group,
    probabilities,
    reference,
    rollout_training_probabilities,
    sampled,
    rng,
):
    del state, rollout_training_probabilities, rng
    features = group.features
    rewards = group.rewards

    if algorithm == "rlvr-fusion":
        # The local contract assumes domain experts already exist, so it executes
        # the paper's cheapest applicable branch: task-vector Merge.  Mix RL and
        # MOPD remain explicit equal-budget diagnostics rather than being blended
        # into an invented fourth objective.
        task_vectors = []
        for axis in range(rewards.shape[1]):
            centered = rewards[:, axis] - rewards[:, axis].mean()
            task_vectors.append(centered @ features / max(1, len(features)))
        task_vectors = np.stack(task_vectors)
        norms = np.linalg.norm(task_vectors, axis=1, keepdims=True) + 1e-12
        cosine = (task_vectors / norms) @ (task_vectors / norms).T
        off_diagonal = cosine[~np.eye(len(cosine), dtype=bool)]
        merged = task_vectors.mean(0)
        gradient = merged / (np.linalg.norm(merged) + 1e-12)
        scalar = rewards @ np.asarray((0.55, 0.10, 0.25, 0.10))
        mix_advantage = scalar[sampled] - scalar[sampled].mean()
        teacher_gap = np.log(reference[sampled] + 1e-12) - np.log(
            probabilities[sampled] + 1e-12
        )
        loss = float(-merged @ (probabilities @ features))
        diagnostics = {
            "executed_fusion_paradigm": 0.0,
            "task_vector_cosine_mean": float(off_diagonal.mean()),
            "merge_vector_norm": float(np.linalg.norm(merged)),
            "mix_rl_advantage_std": float(mix_advantage.std()),
            "mopd_positive_teacher_fraction": float((teacher_gap > 0).mean()),
        }
    elif algorithm == "video-opsd":
        evidence = rewards[:, 2]
        evidence = (evidence - evidence.min()) / (np.ptp(evidence) + 1e-12)
        weights = 0.25 + 0.75 * evidence[sampled]
        teacher_gap = np.log(reference[sampled] + 1e-12) - np.log(
            probabilities[sampled] + 1e-12
        )
        outcome = rewards[sampled, 0]
        advantages = weights * teacher_gap + 0.2 * (outcome - outcome.mean())
        advantages -= advantages.mean()
        gradient = _policy_gradient(features, probabilities, sampled, advantages)
        loss = float(-np.mean(weights * teacher_gap))
        diagnostics = {
            "privileged_frame_fraction": float((evidence >= np.quantile(evidence, 0.75)).mean()),
            "evidence_token_weight_mean": float(weights.mean()),
            "evidence_teacher_gap": float(teacher_gap.mean()),
            "full_video_student_fraction": 1.0,
        }
    elif algorithm == "normalized-dpo":
        winner = int(np.argmax(rewards[:, 0]))
        loser = int(np.argmin(rewards[:, 0]))
        beta = 0.1
        policy_margin = np.log(probabilities[winner] + 1e-12) - np.log(
            probabilities[loser] + 1e-12
        )
        reference_margin = np.log(reference[winner] + 1e-12) - np.log(
            reference[loser] + 1e-12
        )
        margin = policy_margin - reference_margin
        # d[(softplus(-beta*m)-log(2))/beta]/dm = -sigmoid(-beta*m).
        preference_force = 1.0 / (1.0 + np.exp(beta * margin))
        gradient = preference_force * (features[winner] - features[loser])
        loss = float((np.logaddexp(0.0, -beta * margin) - np.log(2.0)) / beta)
        diagnostics = {
            "preference_margin": float(margin),
            "centered_softplus_loss": loss,
            "beta_gradient_prefactor": 1.0,
            "preference_force": float(preference_force),
        }
    else:  # pragma: no cover
        raise ValueError(f"unsupported 20260831 algorithm: {algorithm}")

    return gradient, loss, diagnostics
