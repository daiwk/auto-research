"""Post-training mechanisms from the 2026-08-25 public arXiv batch."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"srpo", "erpo"}


def update_latest(
    algorithm, state, group, probabilities, reference,
    rollout_training_probabilities, sampled, rng,
):
    del rollout_training_probabilities, rng
    features = group.features
    rewards = group.rewards[sampled]
    expected = probabilities @ features

    if algorithm == "srpo":
        # A completed trajectory yields a reflection patch.  The patch turns
        # terminal error into a dense process correction, and a same-size
        # teacher scores the reflection-conditioned on-policy candidates.
        outcome = rewards[:, 0]
        process = rewards[:, 2]
        error = outcome.max() - outcome
        patch = error * (process.max() - process + 1e-3)
        teacher_score = outcome + 0.45 * process + 0.30 * patch
        advantages = (teacher_score - teacher_score.mean()) / (
            teacher_score.std() + 1e-6
        )
        diagnostics = {
            "reflection_patches": float(np.count_nonzero(error > 1e-8)),
            "dense_teacher_score_mean": float(teacher_score.mean()),
            "reflection_patch_mean": float(patch.mean()),
        }
    elif algorithm == "erpo":
        # Reference-derived weights favor queries typical under the pre-RL
        # environment.  QKL is kept separate from the sampled response score
        # function, matching the paper's input-side regularization boundary.
        scalar = rewards @ np.asarray((0.70, 0.05, 0.20, 0.05))
        typicality = reference[sampled] / (reference[sampled].mean() + 1e-12)
        advantages = (scalar - scalar.mean()) * np.clip(typicality, 0.5, 1.5)
        query_kl_gradient = features.T @ (probabilities - reference)
        diagnostics = {
            "query_kl": float(np.sum(probabilities * np.log(
                (probabilities + 1e-12) / (reference + 1e-12)
            ))),
            "typicality_weight_mean": float(typicality.mean()),
            "response_policy_kl_coefficient": 0.0,
        }
    else:  # pragma: no cover - guarded by the public config
        raise ValueError(f"unsupported latest algorithm: {algorithm}")

    gradient = np.stack([
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(sampled, advantages)
    ]).mean(0)
    if algorithm == "erpo":
        gradient -= 0.03 * query_kl_gradient
    else:
        gradient -= 0.02 * (features.T @ (probabilities - reference))
    loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, diagnostics
