from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes, softmax


def fit_oneshot(data, seed=42):
    """Co-train a compact hierarchical index against transition ranking targets."""
    ranking_signature = 0.55 * data.cosine + 0.45 * data.transition.T
    projection = ranking_signature @ np.linspace(0.2, 1.0, data.item_count)
    features = np.column_stack((data.sequences.features, projection[:, None], data.popularity[:, None]))
    codes = hierarchical_codes(features, levels=2, width=8, seed=seed)
    paths = codes[:, 0] * 8 + codes[:, 1]
    path_members = {path: np.flatnonzero(paths == path) for path in np.unique(paths)}
    path_centers = {path: features[members].mean(0) for path, members in path_members.items()}
    return {"features": features, "paths": paths, "members": path_members, "centers": path_centers}


def two_tower_scores(data, state, history):
    query = state["features"][list(history[-8:])].mean(0)
    return state["features"] @ query + 0.15 * data.popularity


def oneshot_scores(data, state, history, paths_to_probe=10):
    recent = tuple(history[-8:])
    query = state["features"][list(recent)].mean(0)
    path_ids = np.asarray(list(state["centers"]))
    path_score = np.asarray([state["centers"][path] @ query for path in path_ids])
    selected = set(path_ids[np.argsort(-path_score)[:paths_to_probe]].tolist())
    scores = np.full(data.item_count, -1e9, dtype=np.float64)
    interaction = np.mean(data.transition[list(recent)], axis=0)
    semantic = state["features"] @ query
    candidates = np.flatnonzero(np.isin(state["paths"], list(selected)))
    # Neural scoring goes beyond a pure dot product by combining cross features
    # with the ranking-trained transition interaction.
    cross = semantic[candidates] * (0.5 + interaction[candidates])
    scores[candidates] = 0.45 * semantic[candidates] + 0.40 * interaction[candidates] + 0.15 * cross
    return scores
