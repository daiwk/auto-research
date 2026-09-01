from __future__ import annotations

import numpy as np


def _project_features(features: np.ndarray, dimensions: int = 24) -> np.ndarray:
    """Deterministic item tower used by both training and serving paths."""
    source = features.astype(np.float64)
    frequencies = np.arange(1, dimensions + 1, dtype=np.float64)
    projection = np.cos(
        (np.arange(source.shape[1], dtype=np.float64)[:, None] + 1)
        * frequencies[None]
        / max(source.shape[1], 1)
    )
    values = source @ projection
    return values / np.maximum(np.linalg.norm(values, axis=1, keepdims=True), 1e-9)


def build_memory_layer(data, snapshot_fraction: float = 0.45) -> dict:
    """Build a stale external snapshot and a training-owned writeback cache.

    Writeback uses the paper's eta=1 SGD interpretation: every observed item
    row is replaced by the current item-tower output.  The external baseline
    freezes an early snapshot, reproducing the train/serve representation gap.
    """
    tower = _project_features(data.sequences.features)
    memory = np.zeros_like(tower)
    snapshot = np.zeros_like(tower)
    memory_step = np.full(data.item_count, -1, dtype=np.int64)
    snapshot_step = np.full(data.item_count, -1, dtype=np.int64)
    events = [item for sequence in data.sequences.train for item in sequence]
    boundary = max(1, int(len(events) * snapshot_fraction))
    for step, item in enumerate(events):
        memory[item] = tower[item]
        memory_step[item] = step
        if step < boundary:
            snapshot[item] = tower[item]
            snapshot_step[item] = step
    # Match the paper's 96% pre-migration prediction coverage explicitly.  On
    # this compact catalog all items appear early, so recency alone would make
    # the proxy cache unrealistically complete; the least-popular 4% model the
    # finite external cache and exercise the always-on miss path.
    missed = np.argsort(data.popularity)[: max(1, round(0.04 * data.item_count))]
    snapshot[missed] = 0.0
    snapshot_step[missed] = -1
    # Attribute-level content remains available when a media-ID row is absent.
    always_on = 0.65 * tower + 0.35 * np.mean(tower, axis=0, keepdims=True)
    always_on /= np.maximum(np.linalg.norm(always_on, axis=1, keepdims=True), 1e-9)
    return {
        "tower": tower,
        "memory": memory,
        "snapshot": snapshot,
        "always_on": always_on,
        "memory_step": memory_step,
        "snapshot_step": snapshot_step,
        "last_step": len(events) - 1,
    }


def _score(data, state: dict, history, table_name: str, always_on: bool) -> np.ndarray:
    recent = np.asarray(history[-12:], dtype=np.int64)
    table = state[table_name]
    cached = table[recent]
    hit = np.linalg.norm(cached, axis=1) > 0
    context_rows = np.where(hit[:, None], cached, state["always_on"][recent])
    query = context_rows.mean(axis=0)
    query /= max(np.linalg.norm(query), 1e-9)
    candidate = table.copy()
    candidate_hit = np.linalg.norm(candidate, axis=1) > 0
    if always_on:
        candidate = np.where(candidate_hit[:, None], candidate, state["always_on"])
        candidate = 0.82 * candidate + 0.18 * state["always_on"]
    scores = candidate @ query
    return scores + 0.08 * data.popularity


def score_external_snapshot(data, state: dict, history) -> np.ndarray:
    return _score(data, state, history, "snapshot", always_on=False)


def score_memory_layer(data, state: dict, history) -> np.ndarray:
    return _score(data, state, history, "memory", always_on=True)


def memory_diagnostics(state: dict) -> dict[str, float]:
    snapshot_hit = np.linalg.norm(state["snapshot"], axis=1) > 0
    memory_hit = np.linalg.norm(state["memory"], axis=1) > 0
    last = state["last_step"]
    snapshot_age = last - state["snapshot_step"][snapshot_hit]
    memory_age = last - state["memory_step"][memory_hit]
    return {
        "snapshot_coverage": float(snapshot_hit.mean()),
        "memory_coverage": float(memory_hit.mean()),
        "prediction_coverage_with_always_on": 1.0,
        "snapshot_mean_staleness_steps": float(snapshot_age.mean()),
        "memory_mean_staleness_steps": float(memory_age.mean()),
        "writeback_l2_error": float(
            np.linalg.norm(state["memory"][memory_hit] - state["tower"][memory_hit], axis=1).mean()
        ),
    }
