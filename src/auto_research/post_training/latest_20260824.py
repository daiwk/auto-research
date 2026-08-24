"""GCPO geometric constraint selected by the 2026-08-24 audit."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"gcpo"}


def update_gcpo(state, group, probabilities, reference, sampled):
    features = group.features
    rewards = group.rewards[sampled] @ np.asarray((0.70, 0.05, 0.20, 0.05))
    advantages = (rewards - rewards.mean()) / (rewards.std() + 1e-6)
    expected = probabilities @ features
    contributions = np.stack([
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(sampled, advantages)
    ])
    raw = contributions.mean(0)

    # The full paper constrains both sides of matrix-valued layer updates.  This
    # linear policy proxy constructs the empirical update covariance and removes
    # its dominant rollout-coupled singular subspace before applying the vector update.
    drift = (probabilities - reference)[:, None] * (features - expected)
    _u, singular, vh = np.linalg.svd(drift, full_matrices=False)
    rank = min(2, int(np.sum(singular > 1e-9)))
    basis = vh[:rank].T
    projector = np.eye(features.shape[1]) - basis @ basis.T
    gradient = projector @ raw
    gradient -= 0.02 * (features.T @ (probabilities - reference))
    loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, {
        "constrained_subspace_rank": float(rank),
        "raw_gradient_norm": float(np.linalg.norm(raw)),
        "projected_gradient_norm": float(np.linalg.norm(gradient)),
        "principal_overlap_removed": float(
            np.linalg.norm(basis.T @ raw) / max(np.linalg.norm(raw), 1e-12)
        ) if rank else 0.0,
    }
