from __future__ import annotations

import numpy as np


def fit_next(data):
    items = len(data.item_texts)
    transition = np.ones((items, items), dtype=np.float64) * 1e-3
    for sequence in data.train:
        for left, right in zip(sequence, sequence[1:]):
            transition[left, right] += 1.0
    transition /= transition.sum(1, keepdims=True)
    genres = sorted({genre for labels in data.item_genres for genre in labels})
    columns = {genre: index for index, genre in enumerate(genres)}
    semantic = np.zeros((items, len(columns)), dtype=np.float64)
    for item, labels in enumerate(data.item_genres):
        for label in labels:
            semantic[item, columns[label]] = 1.0
    semantic /= np.maximum(np.linalg.norm(semantic, axis=1, keepdims=True), 1.0)
    # Offline NKG: retain transitions that are supported by both behavior and a
    # semantic next-intent relation, mirroring NEXT generation + verification.
    compatibility = semantic @ semantic.T
    verified = transition * (compatibility >= 0.25)
    verified /= np.maximum(verified.sum(1, keepdims=True), 1e-12)
    popularity = np.log1p(data.popularity.astype(np.float64))
    popularity /= max(float(popularity.max()), 1.0)
    return {"transition": transition, "semantic": semantic, "verified_nkg": verified, "popularity": popularity}


def production_baseline(state, history):
    recent = tuple(history[-8:])
    return 0.65 * state["transition"][list(recent)].mean(0) + 0.20 * (state["semantic"][list(recent)].mean(0) @ state["semantic"].T) + 0.15 * state["popularity"]


def next_scores(state, history):
    base = production_baseline(state, history)
    current = history[-1]
    directed = state["verified_nkg"][current]
    intent = state["semantic"][current] @ state["semantic"].T
    return 0.70 * base + 0.20 * directed + 0.10 * intent
