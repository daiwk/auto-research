from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes


def build_cq_sid(data, seed=42):
    # Stage 1: category-constrained first code plus residual semantic codes.
    category = data.domains
    residual_codes = hierarchical_codes(
        np.concatenate(
            (data.sequences.features, data.transition), axis=1
        ),
        levels=2,
        width=8,
        seed=seed,
    )
    codes = np.column_stack((category, residual_codes))
    unique_clusters = len({tuple(row) for row in codes})

    # Stage 2-4: item/query/personalized/ranker-aligned translation statistics.
    cluster_transition: dict[tuple[int, ...], np.ndarray] = {}
    for source in range(data.item_count):
        key = tuple(codes[source])
        cluster_transition.setdefault(
            key, np.zeros(data.item_count, dtype=np.float64)
        )
        cluster_transition[key] += data.transition[source]
    for key in cluster_transition:
        cluster_transition[key] /= max(
            cluster_transition[key].sum(), 1e-12
        )

    def feature_matrix(history):
        recent = tuple(history[-8:])
        query = np.mean(data.sequences.features[list(recent)], axis=0)
        semantic = data.sequences.features @ query
        transition = np.mean(
            [cluster_transition[tuple(codes[item])] for item in recent], axis=0
        )
        category_vote = np.bincount(
            category[list(recent)], minlength=int(category.max()) + 1
        ).argmax()
        constrained = (category == category_vote).astype(np.float64)
        return np.stack(
            (semantic, constrained, transition, 1.0 - data.popularity), axis=1
        )

    # EG-GRPO: every sampled group explicitly contains the ground-truth item.
    # Group-relative advantages learn the final signal combination.
    rng = np.random.default_rng(seed)
    weights = np.zeros(4, dtype=np.float64)
    losses = []
    rows = [
        (sequence[max(0, index - 8):index], sequence[index])
        for sequence in data.sequences.train
        for index in range(2, len(sequence))
    ]
    for _ in range(240):
        history, target = rows[int(rng.integers(len(rows)))]
        negatives = rng.choice(
            np.delete(np.arange(data.item_count), target), 7, replace=False
        )
        group = np.concatenate(([target], negatives))
        features = feature_matrix(history)[group]
        reward = np.asarray(
            [1.0] + [
                0.2 * data.transition[history[-1], item]
                + 0.1 * (1.0 - data.popularity[item])
                for item in negatives
            ]
        )
        advantage = (reward - reward.mean()) / (reward.std() + 1e-6)
        logits = features @ weights
        probability = np.exp(logits - logits.max())
        probability /= probability.sum()
        expected = probability @ features
        gradient = np.mean(
            advantage[:, None] * (features - expected), axis=0
        )
        weights += 0.08 * np.clip(gradient, -2.0, 2.0)
        losses.append(float(-np.sum(probability * advantage)))

    def scorer(history):
        return feature_matrix(history) @ weights

    return scorer, {
        "sid_levels": 3,
        "category_constrained_first_level": True,
        "residual_code_width": 8,
        "semantic_clusters": unique_clusters,
        "progressive_stages": 4,
        "expert_injected_group_reward": True,
        "eg_grpo_updates": len(losses),
        "policy_weights": weights.tolist(),
        "final_group_objective": losses[-1],
    }
