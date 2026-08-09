from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes, softmax


def build_mfli(data):
    semantic = hierarchical_codes(data.sequences.features, levels=2, width=8)
    freshness = np.digitize(data.popularity, np.quantile(data.popularity, [0.25, 0.5, 0.75]))
    facets = np.stack([data.domains, semantic[:, 0], semantic[:, 1], freshness], axis=1)
    transitions = []
    for facet in range(facets.shape[1]):
        width = int(facets[:, facet].max()) + 1
        matrix = np.ones((width, width)) * 1e-3
        for sequence in data.sequences.train:
            for left, right in zip(sequence, sequence[1:]):
                matrix[facets[left, facet], facets[right, facet]] += 1
        transitions.append(matrix / matrix.sum(axis=1, keepdims=True))
    return {"facets": facets, "transitions": transitions}


def score_mfli(data, state, history):
    recent = np.asarray(history[-6:], dtype=np.int64)
    # Query-dependent facet allocation replaces one static ANN geometry.
    unique = np.asarray([len(np.unique(state["facets"][recent, i])) for i in range(4)])
    allocation = softmax(1.5 / np.maximum(unique, 1))
    score = np.zeros(data.item_count)
    for facet, matrix in enumerate(state["transitions"]):
        source = state["facets"][recent[-1], facet]
        score += allocation[facet] * matrix[source, state["facets"][:, facet]]
    return score
