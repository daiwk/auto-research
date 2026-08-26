from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TAGRState:
    transition: np.ndarray
    semantic_ids: np.ndarray
    item_features: np.ndarray
    popularity: np.ndarray


def _normalize_rows(values: np.ndarray) -> np.ndarray:
    return values / np.maximum(values.sum(1, keepdims=True), 1e-12)


def fit_tagr(data) -> TAGRState:
    items = data.item_count
    transition = np.full((items, items), 1e-3, dtype=np.float64)
    predecessor = np.full((items, items), 1e-3, dtype=np.float64)
    for sequence in data.train:
        for left, right in zip(sequence[:-1], sequence[1:]):
            transition[left, right] += 1.0
            predecessor[right, left] += 1.0
    transition = _normalize_rows(transition)
    features = data.features.astype(np.float64)
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-12)
    semantic_code = np.argmax(features, axis=1) % 8
    collaborative_code = np.argmax(predecessor, axis=1) % 8
    popularity = np.log1p(data.popularity.astype(np.float64))
    popularity /= max(float(popularity.max()), 1.0)
    # Stable two-level vocabulary; assignments can be refreshed without
    # changing the token inventory, matching LSID's serving constraint.
    semantic_ids = np.stack((semantic_code, collaborative_code), axis=1)
    return TAGRState(transition, semantic_ids, features, popularity)


def score_production_baseline(state: TAGRState, history) -> np.ndarray:
    return 0.72 * state.transition[history[-1]] + 0.28 * state.popularity


def score_tagr(state: TAGRState, history) -> np.ndarray:
    history = tuple(history)
    short = history[-3:]
    medium = history[-12:]
    long = history
    short_intent = state.transition[list(short)].mean(0)
    medium_intent = state.transition[list(medium)].mean(0)
    long_intent = state.transition[list(long)].mean(0)
    # Multi-scale intent weights adapt to the semantic drift of the latest ad.
    latest_feature = state.item_features[history[-1]]
    semantic = latest_feature @ state.item_features.T
    drift = float(np.std(semantic[list(history[-min(8, len(history)) :])]))
    short_weight = float(np.clip(0.48 + drift, 0.48, 0.72))
    intent = short_weight * short_intent + 0.30 * medium_intent
    intent += (0.70 - short_weight) * long_intent
    sid_match = (
        (state.semantic_ids[:, 0] == state.semantic_ids[history[-1], 0]).astype(float)
        + (state.semantic_ids[:, 1] == state.semantic_ids[history[-1], 1]).astype(float)
    ) / 2.0
    # IOPO analogue: behavior-aligned intent remains the anchor, while the
    # value branch (fresh engagement/popularity) contributes under a bounded gate.
    behavior = 0.68 * intent + 0.20 * np.maximum(semantic, 0.0) + 0.12 * sid_match
    value_gate = 1.0 / (1.0 + np.exp(-6.0 * (behavior - behavior.mean())))
    return (1.0 - 0.18 * value_gate) * behavior + 0.18 * value_gate * state.popularity
