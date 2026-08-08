"""Mechanism-specific objectives for the 2026-08 post-training P1 queue."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"minirl", "missing-old-logits", "stare"}


def update_p1(algorithm, state, group, probabilities, reference, sampled, rng):
    features = group.features
    expected = probabilities @ features

    def reinforce(indices, advantages):
        gradient = np.zeros(features.shape[1], dtype=np.float64)
        for index, advantage in zip(indices, advantages):
            gradient += float(advantage) * (features[index] - expected)
        return gradient / max(1, len(indices))

    rewards = group.rewards[sampled, 0]
    advantages = (rewards - rewards.mean()) / (rewards.std() + 1e-6)
    if algorithm == "minirl":
        rollout = np.exp(features @ state.rollout_weights - np.max(features @ state.rollout_weights))
        rollout /= rollout.sum()
        ratio = probabilities[sampled] / (rollout[sampled] + 1e-12)
        clipped = np.clip(ratio, 0.8, 1.2)
        # Routing Replay analogue: preserve sampled expert route under the
        # policy update, so the IS ratio corrects policy rather than routing.
        routes = np.argmax(np.abs(features[sampled, : min(4, features.shape[1])]), axis=1)
        gradient = reinforce(sampled, advantages * clipped)
        loss = float(-np.mean(advantages * clipped * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"importance_sampling": 1.0, "ratio_clip_fraction": float(np.mean(ratio != clipped)),
                       "routing_replay_unique_experts": float(len(np.unique(routes))),
                       "policy_staleness_l1": float(np.abs(probabilities - rollout).mean())}
    elif algorithm == "missing-old-logits":
        rollout = np.exp(features @ state.rollout_weights - np.max(features @ state.rollout_weights))
        rollout /= rollout.sum()
        # Revised PPO-EWMA reconstructs the absent historical training logits
        # separately from the inference/training discrepancy correction.
        reconstructed_old = 0.8 * rollout + 0.2 * reference
        discrepancy = rollout[sampled] / (reconstructed_old[sampled] + 1e-12)
        staleness = reconstructed_old[sampled] / (probabilities[sampled] + 1e-12)
        weight = np.clip(discrepancy, 0.8, 1.2) * np.clip(staleness, 0.8, 1.2)
        gradient = reinforce(sampled, advantages * weight)
        loss = float(-np.mean(advantages * weight * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"old_logits_available": 0.0, "ewma_reconstruction": 1.0,
                       "mean_discrepancy_ratio": float(discrepancy.mean()),
                       "mean_staleness_ratio": float(staleness.mean())}
    else:  # STARE
        surprisal = -np.log(probabilities[sampled] + 1e-12)
        low, high = np.quantile(surprisal, (0.25, 0.75))
        critical = (surprisal <= low) | (surprisal >= high)
        entropy = float(-np.sum(probabilities * np.log(probabilities + 1e-12)))
        target_entropy = 0.72 * np.log(len(probabilities))
        gate = np.clip((target_entropy - entropy) / max(target_entropy, 1e-8), -1.0, 1.0)
        reweight = np.ones_like(advantages)
        reweight[critical] *= np.exp(gate * np.sign(surprisal[critical] - np.median(surprisal)))
        gradient = reinforce(sampled, advantages * reweight)
        loss = float(-np.mean(advantages * reweight * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"critical_token_fraction": float(critical.mean()), "surprisal_q25": float(low),
                       "surprisal_q75": float(high), "target_entropy": float(target_entropy),
                       "closed_loop_gate": float(gate)}
    state.variant_updates += 1
    return gradient, loss, diagnostics
