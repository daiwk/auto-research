from __future__ import annotations

import numpy as np


def build_podcast_mtl_scorer(data):
    """Shared low-rank representation jointly fits stream and ad objectives."""
    examples, stream, promotion = [], [], []
    cold = data.popularity <= np.quantile(data.popularity, 0.35)
    for sequence in data.sequences.train:
        for end in range(2, len(sequence)):
            history = np.asarray(sequence[max(0, end - 8):end])
            target = sequence[end]
            context = data.sequences.features[history].mean(0)
            examples.append(context)
            stream.append(data.sequences.features[target])
            promotion.append(
                data.sequences.features[target] * (1.0 + 0.5 * cold[target])
            )
    x = np.asarray(examples)
    targets = np.concatenate(
        (np.asarray(stream), np.asarray(promotion)), axis=1
    )
    weights = np.linalg.solve(
        x.T @ x + 1e-2 * np.eye(x.shape[1]), x.T @ targets
    )
    u, singular, vt = np.linalg.svd(weights, full_matrices=False)
    rank = min(8, len(singular))
    shared = u[:, :rank] @ np.diag(singular[:rank]) @ vt[:rank]
    width = data.sequences.features.shape[1]

    def scorer(history):
        context = data.sequences.features[np.asarray(history[-8:])].mean(0)
        outputs = context @ shared
        stream_vector = outputs[:width]
        promotion_vector = outputs[width:]
        return (
            data.sequences.features @ (0.6 * stream_vector + 0.4 * promotion_vector)
            + 0.15 * cold
        )

    return scorer, {
        "tasks": ("organic_stream", "ad_promotion"),
        "shared_rank": rank,
        "cold_item_fraction": float(cold.mean()),
        "gradient_balancing_proxy": "equalized target blocks",
    }
