from __future__ import annotations

import numpy as np


def build_pinclip_scorer(data):
    """Whitened content/graph contrastive alignment with neighbor positives."""
    content = data.sequences.features.astype(float)
    graph = data.transition + data.transition.T
    graph /= np.maximum(graph.sum(1, keepdims=True), 1e-12)
    neighbors = graph @ content
    left = content - content.mean(0)
    right = neighbors - neighbors.mean(0)
    covariance = left.T @ right
    u, singular, vt = np.linalg.svd(covariance, full_matrices=False)
    image_projection = u
    graph_projection = vt.T
    image = left @ image_projection
    neighbor = right @ graph_projection
    representation = image + neighbor
    representation /= np.maximum(
        np.linalg.norm(representation, axis=1, keepdims=True), 1e-12
    )

    def scorer(history):
        query = representation[np.asarray(history[-8:])].mean(0)
        return representation @ query

    return scorer, {
        "contrastive_pairs": int(np.count_nonzero(graph)),
        "neighbor_alignment": True,
        "canonical_correlations": singular[:8].tolist(),
    }
