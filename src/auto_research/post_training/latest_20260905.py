"""GAPO adaptive clipping from arXiv:2609.00444."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"gapo"}


def update_latest(algorithm, state, group, probabilities, reference,
                  rollout_training_probabilities, sampled, rng):
    del algorithm, state, reference, rollout_training_probabilities, rng
    rewards = group.rewards[sampled, 0]
    advantages = rewards - rewards.mean()
    correct = rewards > rewards.mean()
    k = len(sampled)
    c = max(1, int(correct.sum()))
    epsilon_lo, epsilon_hi_max = 0.20, 0.28
    positive_clip = epsilon_lo + (epsilon_hi_max - epsilon_lo) * (k - c) / max(1, k - 1)
    ratio = probabilities[sampled] / np.maximum(probabilities[sampled].mean(), 1e-12)
    clipped = np.where(advantages >= 0, np.minimum(ratio, 1.0 + positive_clip), np.maximum(ratio, 1.0 - epsilon_lo))
    expected = probabilities @ group.features
    gradient = np.stack([float(a * w) * (group.features[i] - expected) for i, a, w in zip(sampled, advantages, clipped)]).mean(0)
    loss = float(-np.mean(advantages * clipped * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, {
        "group_correct_count": float(c),
        "adaptive_upper_clip": float(positive_clip),
        "scarce_correct_headroom": float(positive_clip - epsilon_lo),
        "clipped_fraction": float(np.mean(ratio != clipped)),
    }
