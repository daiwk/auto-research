from __future__ import annotations

import numpy as np

from ..mdcns.model import SequentialModel


class LLaTTEScorer:
    def __init__(
        self, model: SequentialModel, upstream_weight: float, target_aware_weight: float = 0.5
    ):
        self.model = model
        self.upstream_weight = upstream_weight
        self.target_aware_weight = target_aware_weight

    def short_sequence_scores(self, history: tuple[int, ...]) -> np.ndarray:
        vectors = self.model.context[list(history[-5:])]
        weights = np.geomspace(0.4, 1.0, len(vectors))
        profile = np.average(vectors, axis=0, weights=weights)
        return self.model.item @ profile

    def two_stage_scores(self, history: tuple[int, ...]) -> np.ndarray:
        # Online stage: target-aware attention over a pyramidal recent-token window.
        online_vectors = self.model.context[list(history[-12:])]
        scores = self.model.item @ online_vectors.T
        logits = scores - scores.max(axis=1, keepdims=True)
        attention = np.exp(logits)
        attention /= np.maximum(attention.sum(axis=1, keepdims=True), 1e-12)
        target_aware = np.sum(attention * scores, axis=1)

        # Upstream stage: asynchronously cached user-only summary of the full history.
        upstream = self.model.context[list(history)].mean(axis=0)
        upstream_scores = self.model.item @ upstream
        return (
            self.short_sequence_scores(history)
            + self.target_aware_weight * target_aware
            + self.upstream_weight * upstream_scores
        )


def train_sequence_backbone(data, seed: int, factors: int = 24, epochs: int = 5):
    rng = np.random.default_rng(seed)
    model = SequentialModel.create(data.item_count, factors, seed)
    pairs = np.asarray([(a, b) for sequence in data.train for a, b in zip(sequence, sequence[1:])], dtype=np.int64)
    for _ in range(epochs):
        rng.shuffle(pairs)
        for previous, positive in pairs:
            negative = int(rng.integers(data.item_count))
            if negative == positive:
                negative = (negative + 1) % data.item_count
            model.bpr_update(int(previous), int(positive), negative, 0.035, 0.002)
    return model
