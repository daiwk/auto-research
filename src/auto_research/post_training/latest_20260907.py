"""Sparse token supervision from arXiv:2609.04565."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"sparse-opd"}


def update_latest(algorithm, state, group, probabilities, reference,
                  rollout_training_probabilities, sampled, rng):
    del algorithm, state, reference, rng
    rewards = group.rewards[sampled, 0]
    advantages = rewards - rewards.mean()
    # Candidate rows stand in for generated-token positions.  Preserve the
    # paper's central intervention by supervising only the one or two largest
    # teacher/student discrepancies rather than every sampled position.
    discrepancy = np.abs(
        np.log(probabilities[sampled] + 1e-12)
        - np.log(rollout_training_probabilities[sampled] + 1e-12)
    )
    keep = np.argsort(discrepancy)[-min(2, len(sampled)):]
    chosen = sampled[keep]
    chosen_advantages = advantages[keep]
    expected = probabilities @ group.features
    gradient = np.stack([
        float(advantage) * (group.features[index] - expected)
        for index, advantage in zip(chosen, chosen_advantages)
    ]).mean(0)
    loss = float(-np.mean(chosen_advantages * np.log(probabilities[chosen] + 1e-12)))
    return gradient, loss, {
        "supervised_positions": float(len(chosen)),
        "sampled_positions": float(len(sampled)),
        "supervision_fraction": float(len(chosen) / max(1, len(sampled))),
        "selected_discrepancy": float(discrepancy[keep].mean()),
    }
