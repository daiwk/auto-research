from __future__ import annotations

import numpy as np

from ..mdcns.model import SequentialModel


class CMSLScorer:
    def __init__(self, model: SequentialModel, assignments: np.ndarray, alpha: float):
        self.model = model
        self.assignments = assignments
        self.alpha = alpha

    def single_sequence_scores(self, history: tuple[int, ...]) -> np.ndarray:
        weights = np.geomspace(0.25, 1.0, len(history))
        profile = np.average(self.model.context[list(history)], axis=0, weights=weights)
        return self.model.item @ profile

    def multi_sequence_scores(self, history: tuple[int, ...]) -> np.ndarray:
        vectors = self.model.context[list(history)]
        weights = np.geomspace(0.25, 1.0, len(history))
        profiles = []
        for cluster in np.unique(self.assignments[list(history)]):
            mask = self.assignments[list(history)] == cluster
            strand = vectors[mask]
            strand_weights = weights[mask]
            query = strand[-1]
            # Degree-two polynomial feature approximation mirrors CMSL linear attention.
            attention = np.maximum(0.05, 1.0 + strand @ query + 0.5 * (strand @ query) ** 2)
            profiles.append(np.average(strand, axis=0, weights=strand_weights * attention))
        strand_scores = np.stack([self.model.item @ profile for profile in profiles])
        constructed = np.max(strand_scores, axis=0)
        return (1.0 - self.alpha) * self.single_sequence_scores(history) + self.alpha * constructed


def semantic_assignments(features: np.ndarray, clusters: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    centers = features[rng.choice(len(features), clusters, replace=False)].copy()
    assignments = np.zeros(len(features), dtype=np.int64)
    for _ in range(15):
        similarity = features @ centers.T
        assignments = np.argmax(similarity, axis=1)
        for index in range(clusters):
            members = features[assignments == index]
            if len(members):
                center = members.mean(axis=0)
                centers[index] = center / max(np.linalg.norm(center), 1e-12)
    return assignments


def train_backbone(data, seed: int, factors: int = 24, epochs: int = 5) -> SequentialModel:
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
