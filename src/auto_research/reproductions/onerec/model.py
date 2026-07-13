from __future__ import annotations

import numpy as np


class OneRecScorer:
    def __init__(self, backbone, features: np.ndarray, popularity: np.ndarray, session_weight: float, preference_weight: float):
        self.backbone = backbone
        self.features = features
        self.popularity = popularity / max(popularity.max(), 1.0)
        self.session_weight = session_weight
        self.preference_weight = preference_weight
        self.items = np.arange(len(popularity))

    def pointwise_scores(self, history: tuple[int, ...]) -> np.ndarray:
        return self.backbone.scores(history[-1], self.items)

    def session_scores(self, history: tuple[int, ...]) -> np.ndarray:
        base = self.pointwise_scores(history)
        session = history[-min(5, len(history)) :]
        sequence_scores = np.stack([self.backbone.scores(item, self.items) for item in session])
        coherence = np.average(sequence_scores, axis=0, weights=np.geomspace(0.25, 1.0, len(session)))
        return base + self.session_weight * coherence

    def aligned_scores(self, history: tuple[int, ...]) -> np.ndarray:
        session = self.session_scores(history)
        user_interest = self.features[list(history[-20:])].mean(axis=0)
        reward = self.features @ user_interest - 0.15 * self.popularity
        reward = reward / max(np.std(reward), 1e-12)
        # DPO proxy: reward-margin re-ranking against the frozen session generator.
        return session + self.preference_weight * reward
