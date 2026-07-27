from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes


def build_rankgraph2(data, seed=42):
    debiased = data.transition.copy()
    keep = 1.0 / np.sqrt(1.0 + data.popularity)
    debiased *= keep[None, :]
    debiased /= np.maximum(debiased.sum(1, keepdims=True), 1e-12)
    state = np.eye(data.item_count)
    ppr = 0.2 * state
    walk = state
    for power in range(1, 6):
        walk = walk @ debiased
        ppr += 0.2 * (0.8 ** power) * walk
    codes = hierarchical_codes(ppr, levels=2, width=8, seed=seed)

    def scorer(history):
        graph = ppr[list(history[-6:])].mean(0)
        recent_codes = codes[list(history[-6:])]
        first = np.bincount(recent_codes[:, 0], minlength=8).argmax()
        second = np.bincount(recent_codes[:, 1], minlength=8).argmax()
        cluster_prior = 0.65 * (codes[:, 0] == first) + 0.35 * (
            (codes[:, 0] == first) & (codes[:, 1] == second)
        )
        return 0.85 * graph + 0.15 * cluster_prior

    return scorer, {
        "popularity_corrected_edges": True,
        "ppr_hops": 5,
        "residual_index_levels": 2,
        "residual_index_width": 8,
        "precomputed_graph_rows": data.item_count,
    }
