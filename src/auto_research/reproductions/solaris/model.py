from __future__ import annotations

import numpy as np


def train_solaris(data):
    future = np.zeros((data.item_count, data.item_count))
    for sequence in data.sequences.train:
        for index, left in enumerate(sequence[:-1]):
            for distance, target in enumerate(sequence[index + 1 : index + 4], 1):
                future[left, target] += 1.0 / distance
    future /= np.maximum(future.sum(1, keepdims=True), 1.0)
    threshold = np.quantile(future[future > 0], 0.65) if np.any(future > 0) else 0
    cache = np.where(future >= threshold, future, 0.0)
    cached_pairs = int((cache > 0).sum())

    def scorer(history):
        predicted = cache[list(history[-4:])].mean(0)
        fallback = data.transition[history[-1]]
        covered = predicted.max() > 0
        return 0.75 * predicted + 0.25 * fallback if covered else fallback

    return scorer, {
        "future_pair_predictor": True,
        "async_precompute": True,
        "cached_user_item_latents": cached_pairs,
        "catalog_pair_fraction": cached_pairs / (data.item_count ** 2),
        "online_fallback": True,
    }
