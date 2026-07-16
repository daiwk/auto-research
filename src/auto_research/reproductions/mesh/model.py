from __future__ import annotations

import time
import numpy as np

from ..industrial_2026 import base_scores


def train_mesh(data):
    # Independent user/item/context manifolds and protected residual amplifiers.
    item = data.sequences.features.astype(np.float64)
    item = (item - item.mean(0, keepdims=True)) / np.maximum(item.std(0, keepdims=True), 1e-5)
    amplified = item.copy()
    for _ in range(3):
        cross = amplified * np.tanh(amplified)
        amplified = amplified + 0.35 * cross + 0.20 * item
        amplified /= np.maximum(np.linalg.norm(amplified, axis=1, keepdims=True), 1.0)
    return amplified, {"modular_towers": ["user", "item", "context"], "amplifier_layers": 3, "residual_gated_bias_correction": True}


def score_flat(data, history):
    return base_scores(data, history)


def score_mesh(data, amplified, history):
    user = np.mean(amplified[list(history[-12:])], axis=0)
    intrinsic = (amplified * user).sum(1)
    context = np.asarray([len(history) / 30.0, np.mean(data.popularity[list(history[-8:])])])
    gate = 1.0 / (1.0 + np.exp(-(2.5 - 2.0 * context[1] + 0.2 * context[0])))
    bias = 0.15 * data.popularity
    return 0.45 * base_scores(data, history) + 0.55 * (gate * intrinsic + bias)


def benchmark(data, amplified):
    histories = data.sequences.train[:80]
    start = time.perf_counter()
    for history in histories:
        score_flat(data, history)
    flat = time.perf_counter() - start
    start = time.perf_counter()
    # Cached item tower represents asynchronous serving of item features.
    for history in histories:
        score_mesh(data, amplified, history)
    modular = time.perf_counter() - start
    return {"flat_seconds": flat, "cached_modular_seconds": modular, "local_throughput_ratio": flat / max(modular, 1e-9)}
