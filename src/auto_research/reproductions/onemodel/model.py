from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class OneModelState:
    global_transition: np.ndarray
    scenario_transition: np.ndarray
    scenario_prior: np.ndarray
    item_features: np.ndarray
    popularity: np.ndarray


def scenario_id(features: np.ndarray, item: int, scenarios: int = 3) -> int:
    """Derive a reproducible public-data scenario from the dominant genre."""
    row = features[item]
    return int(np.argmax(row) % scenarios) if row.size else int(item % scenarios)


def fit_onemodel(data, scenarios: int = 3) -> OneModelState:
    items = data.item_count
    global_transition = np.ones((items, items), dtype=np.float64) * 1e-3
    scenario_transition = np.ones((scenarios, items, items), dtype=np.float64) * 1e-3
    scenario_prior = np.ones((scenarios, items), dtype=np.float64) * 1e-3
    for sequence in data.train:
        for left, right in zip(sequence[:-1], sequence[1:]):
            current = scenario_id(data.features, right, scenarios)
            global_transition[left, right] += 1.0
            scenario_transition[current, left, right] += 1.0
            scenario_prior[current, right] += 1.0
    global_transition /= global_transition.sum(1, keepdims=True)
    scenario_transition /= scenario_transition.sum(2, keepdims=True)
    scenario_prior /= scenario_prior.sum(1, keepdims=True)
    features = data.features.astype(np.float64)
    features /= np.maximum(np.linalg.norm(features, axis=1, keepdims=True), 1e-9)
    popularity = np.log1p(data.popularity.astype(np.float64))
    popularity /= max(float(popularity.max()), 1.0)
    return OneModelState(
        global_transition, scenario_transition, scenario_prior, features, popularity
    )


def score_global(state: OneModelState, history) -> np.ndarray:
    recent = tuple(history[-8:])
    local = state.global_transition[recent[-1]]
    pooled = state.global_transition[list(recent)].mean(0)
    return 0.55 * local + 0.30 * pooled + 0.15 * state.popularity


def score_onemodel(state: OneModelState, history) -> np.ndarray:
    """SAIM-style scenario gate plus global/local stratified representation."""
    recent = tuple(history[-8:])
    scenario = scenario_id(state.item_features, recent[-1], len(state.scenario_prior))
    local = state.scenario_transition[scenario, recent[-1]]
    global_pool = state.global_transition[list(recent)].mean(0)
    semantic_pool = state.item_features[list(recent)].mean(0) @ state.item_features.T
    # The gate is scenario-conditioned and bounded, mirroring SAIM's sigmoid gate.
    gate = 1.0 / (1.0 + np.exp(-4.0 * (semantic_pool - semantic_pool.mean())))
    scenario_branch = 0.70 * local + 0.30 * state.scenario_prior[scenario]
    return gate * scenario_branch + (1.0 - gate) * (
        0.65 * global_pool + 0.20 * semantic_pool + 0.15 * state.popularity
    )
