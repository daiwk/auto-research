from __future__ import annotations

import numpy as np

from ..mdcns.model import SequentialModel


class MixFormerScorer:
    def __init__(self, model: SequentialModel, features: np.ndarray, cross_weight: float):
        self.model = model
        self.features = features
        self.cross_weight = cross_weight

    def stacked_scores(self, history: tuple[int, ...]) -> np.ndarray:
        sequence = self.model.context[list(history[-12:])]
        sequence_profile = np.average(sequence, axis=0, weights=np.geomspace(0.3, 1.0, len(sequence)))
        dense_profile = self.features[list(history)].mean(axis=0)
        dense_score = self.features @ dense_profile
        return self.model.item @ sequence_profile + 0.25 * dense_score

    def unified_scores(self, history: tuple[int, ...]) -> np.ndarray:
        base = self.stacked_scores(history)
        sequence = self.model.context[list(history[-12:])]
        dense = self.features[list(history[-12:])]
        # Shared-token proxy: dense semantics gate each sequential token before aggregation.
        token_gate = 0.5 + 0.5 * (dense @ dense.mean(axis=0))
        token_gate /= max(token_gate.sum(), 1e-12)
        mixed_profile = token_gate @ sequence
        candidate_gate = 1.0 + self.cross_weight * (self.features @ dense.mean(axis=0))
        return base + self.cross_weight * (self.model.item @ mixed_profile) * candidate_gate
