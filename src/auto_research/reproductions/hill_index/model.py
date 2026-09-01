from __future__ import annotations

import numpy as np

from ..industrial_2026 import softmax


def _kmeans(
    values: np.ndarray, width: int, rng: np.random.Generator
) -> tuple[np.ndarray, np.ndarray]:
    width = min(width, len(values))
    if width == 0:
        return np.empty(0, dtype=np.int64), np.empty((0, values.shape[1]))
    centers = values[rng.choice(len(values), width, replace=False)].copy()
    for _ in range(16):
        distance = ((values[:, None] - centers[None]) ** 2).sum(axis=-1)
        assignment = distance.argmin(axis=1)
        for index in range(width):
            members = values[assignment == index]
            if len(members):
                centers[index] = members.mean(axis=0)
    # Degenerate public fixtures can leave an initialized centroid empty.
    # Compact those nodes so every returned parent/child owns at least one
    # item and hierarchical traversal can never select an empty branch.
    used = np.unique(assignment)
    remap = np.full(width, -1, dtype=np.int64)
    remap[used] = np.arange(len(used))
    return remap[assignment], centers[used]


def build_hill(data, seed: int = 42, coarse_width: int = 6, fine_width: int = 6) -> dict:
    """Residual hierarchical index with attention-soft assignment.

    The coarse layer learns over item embeddings.  Every child layer quantizes
    the residual left by its parent, mirroring HILL cross-layer residual learning.
    """
    rng = np.random.default_rng(seed)
    features = data.sequences.features.astype(np.float64)
    coarse, coarse_centers = _kmeans(features, coarse_width, rng)
    residual = features - coarse_centers[coarse]
    fine = np.zeros(data.item_count, dtype=np.int64)
    fine_centers: dict[int, np.ndarray] = {}
    leaves: dict[tuple[int, int], np.ndarray] = {}
    for parent in range(len(coarse_centers)):
        members = np.flatnonzero(coarse == parent)
        assignment, centers = _kmeans(residual[members], fine_width, rng)
        fine[members] = assignment
        fine_centers[parent] = centers
        for child in range(len(centers)):
            leaves[(parent, child)] = members[assignment == child]
    return {
        "features": features,
        "coarse": coarse,
        "coarse_centers": coarse_centers,
        "fine": fine,
        "fine_centers": fine_centers,
        "leaves": leaves,
    }


def _query(data, history) -> np.ndarray:
    recent = np.asarray(history[-12:], dtype=np.int64)
    weights = softmax(np.linspace(-1.5, 1.5, len(recent)))
    value = weights @ data.sequences.features[recent]
    return value / max(np.linalg.norm(value), 1e-9)


def hill_candidates(
    data, state: dict, history, coarse_beam: int = 3, fine_beam: int = 2
) -> np.ndarray:
    query = _query(data, history)
    coarse_scores = state["coarse_centers"] @ query
    parents = np.argsort(-coarse_scores)[:coarse_beam]
    candidates = []
    for parent in parents:
        residual_query = query - state["coarse_centers"][parent]
        child_scores = state["fine_centers"][int(parent)] @ residual_query
        for child in np.argsort(-child_scores)[:fine_beam]:
            candidates.extend(state["leaves"][(int(parent), int(child))].tolist())
    return np.asarray(sorted(set(candidates)), dtype=np.int64)


def score_hill(data, state: dict, history, hierarchical: bool = True) -> tuple[np.ndarray, int]:
    query = _query(data, history)
    exact = (
        0.72 * (state["features"] @ query)
        + 0.20 * data.transition[history[-1]]
        + 0.08 * data.popularity
    )
    if hierarchical:
        candidates = hill_candidates(data, state, history)
    else:
        # Same coarse-node budget without the residual child layer.
        coarse_scores = state["coarse_centers"] @ query
        parents = np.argsort(-coarse_scores)[:1]
        candidates = np.flatnonzero(np.isin(state["coarse"], parents))
    masked = np.full(data.item_count, -np.inf, dtype=np.float64)
    masked[candidates] = exact[candidates]
    return masked, len(candidates)
