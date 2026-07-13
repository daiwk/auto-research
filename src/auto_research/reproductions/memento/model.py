from __future__ import annotations

import numpy as np


class MementoScorer:
    def __init__(self, embeddings: np.ndarray, relevance_weight: float, retrieved: int = 8):
        self.embeddings = embeddings
        self.relevance_weight = relevance_weight
        self.retrieved = retrieved

    def last_n_scores(self, history: tuple[int, ...], last_n: int = 5) -> np.ndarray:
        profile = self.embeddings[list(history[-last_n:])].mean(axis=0)
        return self.embeddings @ profile

    def rag_scores(self, history: tuple[int, ...]) -> np.ndarray:
        recent = history[-3:]
        documents = history[:-3]
        if not documents:
            return self.last_n_scores(history)
        query = self.embeddings[list(recent)].mean(axis=0)
        selected = maximal_marginal_relevance(
            self.embeddings[list(documents)], query, self.relevance_weight, self.retrieved
        )
        retrieved_items = [documents[index] for index in selected]
        recent_profile = self.embeddings[list(recent)].mean(axis=0)
        memory_profile = self.embeddings[retrieved_items].mean(axis=0)
        profile = 0.6 * recent_profile + 0.4 * memory_profile
        return self.embeddings @ profile


def maximal_marginal_relevance(
    documents: np.ndarray,
    query: np.ndarray,
    relevance_weight: float,
    limit: int,
) -> list[int]:
    relevance = documents @ query
    selected: list[int] = []
    remaining = set(range(len(documents)))
    while remaining and len(selected) < limit:
        best_index, best_score = -1, -np.inf
        for index in remaining:
            redundancy = (
                max(float(documents[index] @ documents[other]) for other in selected)
                if selected
                else 0.0
            )
            score = relevance_weight * relevance[index] - (1.0 - relevance_weight) * redundancy
            if score > best_score:
                best_index, best_score = index, float(score)
        selected.append(best_index)
        remaining.remove(best_index)
    return selected


def collaborative_embeddings(data, dimensions: int = 24) -> np.ndarray:
    graph = np.zeros((data.item_count, data.item_count), dtype=np.float32)
    for sequence in data.train:
        for left, right in zip(sequence, sequence[1:]):
            graph[left, right] += 1
            graph[right, left] += 1
    graph += 0.15 * (data.item_features @ data.item_features.T)
    values, vectors = np.linalg.eigh(graph)
    embedding = vectors[:, -dimensions:] * np.sqrt(np.maximum(values[-dimensions:], 0.0))
    embedding /= np.maximum(np.linalg.norm(embedding, axis=1, keepdims=True), 1e-12)
    return embedding
