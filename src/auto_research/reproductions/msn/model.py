from __future__ import annotations

import numpy as np

from ..p0_2026_common import normalized


def build_memory_scorer(data):
    features = data.sequences.features
    width = max(2, int(np.sqrt(data.item_count)))
    first = np.argmax(features[:, ::2], axis=1) % width
    second = np.argmax(features[:, 1::2], axis=1) % width
    memory = np.zeros((width, width, data.item_count))
    visits = np.zeros((width, width))
    for sequence in data.sequences.train:
        for left, target in zip(sequence, sequence[1:]):
            memory[first[left], second[left], target] += 1
            visits[first[left], second[left]] += 1
    memory /= np.maximum(memory.sum(-1, keepdims=True), 1.0)

    def scorer(history):
        recent = history[-1]
        query = features[recent]
        key_scores = np.outer(
            features[:, ::2].mean(0)[:width] if features.shape[1] >= width * 2 else np.linspace(1, 0, width),
            features[:, 1::2].mean(0)[:width] if features.shape[1] >= width * 2 else np.linspace(0, 1, width),
        )
        key_scores[first[recent], second[recent]] += 2.0
        flat = np.argpartition(key_scores.ravel(), -min(4, key_scores.size))[-4:]
        retrieved = memory.reshape(-1, data.item_count)[flat].mean(0)
        gate = 1.0 / (1.0 + np.exp(-(np.linalg.norm(query) - 0.5)))
        return gate * normalized(retrieved) + (1 - gate) * data.transition[recent]

    return scorer, {
        "product_key_width": width,
        "active_slots_per_request": 4,
        "total_memory_slots": width * width,
        "occupied_slots": int((visits > 0).sum()),
    }
