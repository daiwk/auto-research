from __future__ import annotations

import numpy as np


def _weighted_residual_codes(features, weights, levels=3, width=8, seed=42):
    rng = np.random.default_rng(seed)
    residual = features.astype(float).copy()
    codes = []
    for _ in range(levels):
        centers = residual[rng.choice(len(residual), width, replace=False)].copy()
        for _ in range(12):
            distance = ((residual[:, None] - centers[None]) ** 2).sum(-1)
            assignment = distance.argmin(1)
            for index in range(width):
                mask = assignment == index
                if mask.any():
                    centers[index] = np.average(
                        residual[mask], axis=0, weights=weights[mask]
                    )
        codes.append(assignment)
        residual -= centers[assignment]
    return np.stack(codes, 1)


def build_pin_scale_scorer(data):
    """Engagement-aware residual codebooks prioritize high-value semantics."""
    weights = 0.25 + 0.75 * data.popularity
    codes = _weighted_residual_codes(
        data.sequences.features, weights, levels=3, width=8
    )
    similarity = (codes[:, None] == codes[None]).mean(-1)

    def scorer(history):
        recent = np.asarray(history[-12:])
        engagement = data.transition[recent].mean(0)
        return 0.65 * similarity[recent].mean(0) + 0.35 * engagement

    return scorer, {
        "engagement_weighted_codebook": True,
        "semantic_id_levels": 3,
        "weight_range": [float(weights.min()), float(weights.max())],
    }
