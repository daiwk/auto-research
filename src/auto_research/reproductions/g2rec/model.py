from __future__ import annotations

import numpy as np


class G2RecScorer:
    def __init__(self, item_graph: np.ndarray, membership: np.ndarray, beta: float):
        self.item_graph = item_graph
        self.membership = membership
        self.beta = beta

    def item_only_scores(
        self, history: tuple[int, ...], candidates: np.ndarray | None = None
    ) -> np.ndarray:
        recent = history[-min(3, len(history)) :]
        weights = np.geomspace(0.4, 1.0, len(recent))
        if self.item_graph.shape[0] == self.item_graph.shape[1]:
            scores = np.average(self.item_graph[list(recent)], axis=0, weights=weights)
            return scores if candidates is None else scores[candidates]
        context = np.average(self.item_graph[list(recent)], axis=0, weights=weights)
        items = self.item_graph if candidates is None else self.item_graph[candidates]
        return items @ context

    def interest_token_scores(
        self, history: tuple[int, ...], candidates: np.ndarray | None = None
    ) -> np.ndarray:
        base = self.item_only_scores(history, candidates)
        recent = history[-min(10, len(history)) :]
        profile = np.mean(self.membership[list(recent)], axis=0)
        members = self.membership if candidates is None else self.membership[candidates]
        interest = members @ profile
        base = base / max(np.linalg.norm(base), 1e-12)
        interest = interest / max(np.linalg.norm(interest), 1e-12)
        return (1.0 - self.beta) * base + self.beta * interest


def build_graph_tokens(data, dimensions: int = 12) -> tuple[np.ndarray, np.ndarray]:
    if data.item_count > 2500:
        return _sketched_graph_tokens(data, dimensions)
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


def _sketched_graph_tokens(data, dimensions: int) -> tuple[np.ndarray, np.ndarray]:
    """Spectral co-engagement features without materializing an O(items²) graph."""
    sketch_dimensions = max(4 * dimensions, 48)
    rng = np.random.default_rng(260620554)
    projection = rng.normal(0.0, 1.0 / np.sqrt(sketch_dimensions),
                            (data.item_count, sketch_dimensions)).astype(np.float32)
    sketch = np.zeros_like(projection)
    degree = np.zeros(data.item_count, dtype=np.float32)
    for sequence in data.train:
        unique = np.asarray(sorted(set(sequence)), dtype=np.int64)
        if len(unique) < 2:
            continue
        pooled = projection[unique].sum(axis=0)
        sketch[unique] += pooled - projection[unique]
        degree[unique] += len(unique) - 1
    sketch /= np.sqrt(np.maximum(degree[:, None], 1.0))
    left, singular, _ = np.linalg.svd(sketch, full_matrices=False)
    embeddings = left[:, :dimensions] * singular[:dimensions]
    embeddings /= np.maximum(np.linalg.norm(embeddings, axis=1, keepdims=True), 1e-12)
    membership = np.abs(embeddings)
    membership /= np.maximum(membership.sum(axis=1, keepdims=True), 1e-12)
    return embeddings.astype(np.float32), membership.astype(np.float32)
