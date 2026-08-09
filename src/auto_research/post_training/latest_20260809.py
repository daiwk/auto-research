"""Post-training objectives selected by the 2026-08-09 audit."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"rrc", "rail", "specroll"}


def update_latest(algorithm, state, group, probabilities, reference,
                  rollout_probabilities, sampled, rng):
    features = group.features
    rewards = group.rewards[sampled] @ np.asarray((0.70, 0.05, 0.20, 0.05))
    expected = probabilities @ features
    diagnostics = {}

    if algorithm == "rrc":
        # Convert a comparative generative reward model into centered rank rewards.
        order = np.argsort(np.argsort(rewards))
        advantages = order / max(len(order) - 1, 1) - 0.5
        anchor = int(np.argmax(group.rewards[:, 0]))
        advantages += 0.20 * (group.rewards[sampled, 0] - group.rewards[anchor, 0])
        diagnostics.update({"ranked_responses": float(len(sampled)),
                            "anchor_reward": float(group.rewards[anchor, 0])})
    elif algorithm == "rail":
        # Recoverability controller focuses intervention on uncertain states
        # whose sampled outcome still has room to improve.
        uncertainty = 1.0 - np.abs(probabilities[sampled] - 0.5) * 2.0
        recoverability = np.clip(uncertainty * (1.0 - rewards + rewards.max()), 0.05, 2.0)
        advantages = (rewards - rewards.mean()) / (rewards.std() + 1e-6)
        advantages *= recoverability
        diagnostics.update({"interventions": float(len(sampled)),
                            "mean_recoverability": float(recoverability.mean()),
                            "rollout_budget_saved": float(np.sum(recoverability < np.median(recoverability)))})
    else:  # specroll
        # Exact verifier keeps the target distribution unchanged; accepted
        # proposal prefixes only alter rollout cost, not the policy objective.
        ratio = np.minimum(probabilities[sampled], rollout_probabilities[sampled]) / np.maximum(
            probabilities[sampled], rollout_probabilities[sampled],
        )
        accepted = np.clip(np.floor(1 + 5 * ratio), 1, 6)
        advantages = (rewards - rewards.mean()) / (rewards.std() + 1e-6)
        diagnostics.update({"verified_proposals": float(len(sampled)),
                            "accepted_draft_length": float(accepted.mean()),
                            "estimated_generation_speedup": float(1 + accepted.mean() / 6)})

    gradient = np.zeros_like(state.weights)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (features[index] - expected)
    gradient /= max(len(sampled), 1)
    gradient -= 0.02 * (features.T @ (probabilities - reference))
    loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, diagnostics
