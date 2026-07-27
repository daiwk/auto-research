from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes, softmax


def build_hisac_scorer(data):
    """Hierarchical voting creates sparse interest agents for each history."""
    features = data.sequences.features.astype(float)
    codes = hierarchical_codes(features, levels=3, width=8)

    def scorer(history):
        recent = np.asarray(history[-64:])
        agents = []
        weights = []
        for level in range(codes.shape[1]):
            values, counts = np.unique(codes[recent, level], return_counts=True)
            for code, count in zip(values, counts):
                members = recent[codes[recent, level] == code]
                agents.append(features[members].mean(0))
                weights.append(count / (level + 1))
        agents = np.asarray(agents)
        weights = softmax(np.asarray(weights))
        query = features[recent[-1]]
        routing = softmax(agents @ query) * weights
        routing /= routing.sum()
        interest = (routing[:, None] * agents).sum(0)
        return features @ interest

    return scorer, {
        "rq_levels": 3,
        "hierarchical_voting": True,
        "soft_routing": True,
        "maximum_history": 64,
    }
