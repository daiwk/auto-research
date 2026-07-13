from __future__ import annotations

import numpy as np

from ..mdcns.model import SequentialModel


class LONGERScorer:
    def __init__(self, model: SequentialModel, merge_weight: float, group_size: int = 4):
        self.model = model
        self.merge_weight = merge_weight
        self.group_size = group_size

    def recent_transformer_scores(self, history: tuple[int, ...]) -> np.ndarray:
        vectors = self.model.context[list(history[-12:])]
        return self.model.item @ np.average(
            vectors, axis=0, weights=np.geomspace(0.3, 1.0, len(vectors))
        )

    def longer_scores(self, history: tuple[int, ...]) -> np.ndarray:
        vectors = self.model.context[list(history)]
        groups = [vectors[i : i + self.group_size] for i in range(0, len(vectors), self.group_size)]
        # InnerTrans proxy: retain both the group center and within-group change.
        merged = np.stack([group.mean(axis=0) + 0.25 * (group[-1] - group[0]) for group in groups])
        global_token = vectors.mean(axis=0)
        recent_queries = vectors[-min(6, len(vectors)) :]
        query = 0.7 * recent_queries.mean(axis=0) + 0.3 * global_token
        attention = merged @ query
        attention = np.exp(attention - attention.max())
        attention /= max(attention.sum(), 1e-12)
        compressed = attention @ merged
        return self.recent_transformer_scores(history) + self.merge_weight * (self.model.item @ compressed)


def train_backbone(data, seed: int, epochs: int = 4) -> SequentialModel:
    rng = np.random.default_rng(seed)
    model = SequentialModel.create(data.item_count, 24, seed)
    pairs = np.asarray(
        [(left, right) for sequence in data.train for left, right in zip(sequence, sequence[1:])],
        dtype=np.int64,
    )
    for _ in range(epochs):
        rng.shuffle(pairs)
        for previous, positive in pairs:
            negative = int(rng.integers(data.item_count))
            if negative == positive:
                negative = (negative + 1) % data.item_count
            model.bpr_update(int(previous), int(positive), negative, 0.035, 0.002)
    return model
