"""NEAR equations 1–4 and Appendix C, independent of relevance labels."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


def unit(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    return x / np.maximum(np.linalg.norm(x, axis=-1, keepdims=True), 1e-12)


def projection_residual(x: np.ndarray, reference: np.ndarray) -> np.ndarray:
    return x - np.sum(x * reference, axis=-1, keepdims=True) * reference


def score_scale(view: np.ndarray) -> float:
    """sqrt(mean row population variance), including each memory's self score."""
    mean = view.mean(axis=0)
    centered = view - mean
    covariance = centered.T @ centered / len(view)
    variance = np.einsum("nd,df,nf->n", view, covariance, view)
    return float(max(1e-6, np.sqrt(max(0.0, variance.mean()))))


def spherical_kmeans(x: np.ndarray, clusters: int, seed: int,
                     iterations: int = 50) -> tuple[np.ndarray, np.ndarray]:
    clusters = min(clusters, len(x))
    if clusters < 1:
        raise ValueError("nonempty memory bank and positive anchor count required")
    rng = np.random.default_rng(seed)
    centers = x[rng.choice(len(x), clusters, replace=False)].copy()
    for _ in range(iterations):
        labels = (x @ centers.T).argmax(axis=1)
        new = centers.copy()
        for group in range(clusters):
            members = x[labels == group]
            if len(members):
                new[group] = unit(members.mean(axis=0))
        if np.allclose(new, centers, atol=1e-9):
            centers = new
            break
        centers = new
    return centers, (x @ centers.T).argmax(axis=1)


@dataclass(frozen=True)
class ReferenceTable:
    anchors: np.ndarray
    directions: np.ndarray


class NEARIndex:
    """One fixed inner-product index, exact search at the bounded local scale.

    Labels and queries cannot enter fit(). The query routes only over the small
    reference table; search() performs exactly one memory-key inner product.
    """

    def __init__(self, *, depth: int = 1, normalize_residual: bool = False,
                 alpha: float = 1.0, neighbors: int = 50, anchors: int = 16,
                 routing: int = 4, beta: float = 10.0, seed: int = 42):
        if depth < 1 or alpha < 0 or min(neighbors, anchors, routing) < 1:
            raise ValueError("positive depth/neighborhood/table/routing and nonnegative alpha required")
        self.depth, self.normalize_residual, self.alpha = depth, normalize_residual, alpha
        self.neighbors, self.anchor_count, self.routing = neighbors, anchors, routing
        self.beta, self.seed = beta, seed
        self.views: list[np.ndarray] = []
        self.tables: list[ReferenceTable] = []
        self.scales: list[float] = []

    def fit(self, memory_embeddings: np.ndarray) -> NEARIndex:
        h = unit(memory_embeddings)
        if h.ndim != 2 or len(h) < 2 or not np.isfinite(h).all():
            raise ValueError("at least two finite memory embeddings required")
        self.views, self.tables = [h.copy()], []
        for layer in range(self.depth):
            sim = h @ h.T
            np.fill_diagonal(sim, -np.inf)
            k = min(self.neighbors, len(h) - 1)
            selected = np.argsort(-sim, axis=1, kind="stable")[:, :k]
            references = unit(h[selected].mean(axis=1))
            anchors, labels = spherical_kmeans(h, self.anchor_count, self.seed + layer)
            directions = np.stack([
                unit(references[labels == group].mean(axis=0))
                if (labels == group).any() else unit(references.mean(axis=0))
                for group in range(len(anchors))
            ])
            self.tables.append(ReferenceTable(anchors, directions))
            residual = projection_residual(h, references)
            h = unit(residual)
            self.views.append(h.copy() if self.normalize_residual else residual)
        self.scales = [score_scale(v) for v in self.views]
        weight = np.sqrt(self.alpha / self.depth)
        self.keys = np.concatenate([self.views[0], *[weight * v for v in self.views[1:]]], axis=1)
        return self

    def query_views(self, query: np.ndarray) -> list[np.ndarray]:
        h = unit(np.asarray(query).reshape(1, -1))
        views = [h.copy()]
        for table in self.tables:
            scores = h @ table.anchors.T
            selected = np.argsort(-scores[0], kind="stable")[:min(self.routing, len(table.anchors))]
            logits = self.beta * scores[0, selected]
            weights = np.exp(logits - logits.max())
            weights /= weights.sum()
            ref = unit(weights @ table.directions[selected]).reshape(1, -1)
            residual = projection_residual(h, ref)
            h = unit(residual)
            views.append(h.copy() if self.normalize_residual else residual)
        return views

    def query_key(self, query: np.ndarray) -> np.ndarray:
        views = self.query_views(query)
        weight = np.sqrt(self.alpha / self.depth)
        return np.concatenate([views[0] / self.scales[0], *[
            weight * v / scale for v, scale in zip(views[1:], self.scales[1:], strict=True)
        ]], axis=1)[0]

    def scores(self, query: np.ndarray) -> np.ndarray:
        return self.keys @ self.query_key(query)

    def search(self, query: np.ndarray, k: int = 10) -> np.ndarray:
        return np.argsort(-self.scores(query), kind="stable")[:k]
