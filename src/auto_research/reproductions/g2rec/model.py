from __future__ import annotations

import numpy as np


class G2RecScorer:
    def __init__(self, item_graph: np.ndarray, membership: np.ndarray, beta: float):
        self.item_graph = item_graph
        self.membership = membership
        self.beta = beta

    def item_only_scores(self, history: tuple[int, ...]) -> np.ndarray:
        recent = history[-min(3, len(history)) :]
        weights = np.geomspace(0.4, 1.0, len(recent))
        return np.average(self.item_graph[list(recent)], axis=0, weights=weights)

    def interest_token_scores(self, history: tuple[int, ...]) -> np.ndarray:
        base = self.item_only_scores(history)
        recent = history[-min(10, len(history)) :]
        profile = np.mean(self.membership[list(recent)], axis=0)
        interest = self.membership @ profile
        base = base / max(np.linalg.norm(base), 1e-12)
        interest = interest / max(np.linalg.norm(interest), 1e-12)
        return (1.0 - self.beta) * base + self.beta * interest


def build_graph_tokens(data, dimensions: int = 12) -> tuple[np.ndarray, np.ndarray]:
    graph = np.zeros((data.item_count, data.item_count), dtype=np.float32)
    for sequence in data.train:
        unique = np.asarray(sorted(set(sequence)), dtype=np.int64)
        graph[np.ix_(unique, unique)] += 1.0
    np.fill_diagonal(graph, 0.0)
    graph = np.log1p(graph)
    degree = np.sqrt(np.maximum(graph.sum(axis=1), 1.0))
    normalized = graph / degree[:, None] / degree[None, :]
    values, vectors = np.linalg.eigh(normalized)
    membership = np.abs(vectors[:, -dimensions:] * values[-dimensions:])
    membership /= np.maximum(membership.sum(axis=1, keepdims=True), 1e-12)
    return normalized, membership
