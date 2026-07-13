from __future__ import annotations

import numpy as np


class PLUMScorer:
    def __init__(self, backbone, semantic_prior: np.ndarray, item_codes: np.ndarray, features: np.ndarray, semantic_weight: float):
        self.backbone = backbone
        self.semantic_prior = semantic_prior
        self.item_codes = item_codes
        self.features = features
        self.semantic_weight = semantic_weight
        self.items = np.arange(len(item_codes))

    def large_embedding_scores(self, history: tuple[int, ...]) -> np.ndarray:
        return self.backbone.scores(history[-1], self.items)

    def generative_semantic_id_scores(self, history: tuple[int, ...]) -> np.ndarray:
        base = self.large_embedding_scores(history)
        source_code = self.item_codes[history[-1]]
        code_score = self.semantic_prior[source_code, self.item_codes]
        language_space = self.features @ self.features[list(history[-10:])].mean(axis=0)
        semantic = code_score + 0.35 * language_space
        semantic = semantic / max(np.std(semantic), 1e-12)
        return base + self.semantic_weight * semantic


def build_semantic_ids(data) -> tuple[np.ndarray, np.ndarray]:
    item_codes = np.argmax(data.item_features, axis=1)
    code_count = data.item_features.shape[1]
    transitions = np.ones((code_count, code_count), dtype=np.float64)
    for sequence in data.train:
        for left, right in zip(sequence, sequence[1:]):
            transitions[item_codes[left], item_codes[right]] += 1.0
    transitions /= transitions.sum(axis=1, keepdims=True)
    return item_codes, np.log(transitions + 1e-12)
