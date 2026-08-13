"""Post-training objectives selected by the 2026-08-13 audit."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"pto", "c2-dpo"}


def update_latest(algorithm, state, group, probabilities, reference,
                  rollout_probabilities, sampled, rng):
    features = group.features
    rewards = group.rewards[sampled] @ np.asarray((0.70, 0.05, 0.20, 0.05))
    expected = probabilities @ features
    diagnostics = {}
    if algorithm == "pto":
        continuation = np.roll(group.rewards[:, 0], -1)[sampled]
        lookahead = rewards + 0.45 * continuation
        order = np.argsort(np.argsort(lookahead))
        advantages = order / max(len(order) - 1, 1) - 0.5
        diagnostics.update({
            "preference_tree_nodes": float(len(sampled) * 3),
            "lookahead_depth": 1.0,
            "oracle_comparisons": float(len(sampled) * (len(sampled) - 1) / 2),
        })
    else:
        ranked = sampled[np.argsort(rewards)[::-1]]
        pair_count = max(1, len(ranked) // 2)
        chosen = ranked[:pair_count]
        rejected = ranked[-pair_count:][::-1]
        contextual_margin = probabilities[chosen] - probabilities[rejected]
        degraded_logits = features[:, :-1] @ state.weights[:-1]
        degraded = np.exp(degraded_logits - degraded_logits.max())
        degraded /= degraded.sum()
        degraded_margin = degraded[chosen] - degraded[rejected]
        cpg = contextual_margin - degraded_margin
        advantages = (rewards - rewards.mean()) / (rewards.std() + 1e-6)
        calibration = float(cpg.mean())
        for position, index in enumerate(sampled):
            if index in chosen:
                advantages[position] += 0.35 * calibration
            elif index in rejected:
                advantages[position] -= 0.35 * calibration
        diagnostics.update({
            "contextual_preference_gain": float(cpg.mean()),
            "preference_pairs": float(len(chosen)),
            "ordering_preservation": float(np.mean(contextual_margin >= 0)),
        })
    gradient = np.zeros_like(state.weights)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (features[index] - expected)
    gradient /= max(len(sampled), 1)
    gradient -= 0.02 * (features.T @ (probabilities - reference))
    loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, diagnostics
