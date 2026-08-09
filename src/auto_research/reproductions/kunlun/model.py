from __future__ import annotations

import numpy as np

from ..industrial_2026 import softmax


def score_kunlun(data, history, layers: int = 4):
    sequence = np.asarray(history[-32:], dtype=np.int64)
    values = data.sequences.features[sequence].astype(np.float64)
    # Hierarchical seed pooling condenses event groups before deep interaction.
    seeds = []
    for width in (2, 4, 8):
        chunks = [values[i:i + width].mean(axis=0) for i in range(0, len(values), width)]
        seeds.append(np.mean(chunks, axis=0))
    state = np.mean(seeds, axis=0)
    expert_trace = []
    for layer in range(layers):
        # GDPA: content dot product is gated by recency and event affinity.
        logits = values @ state / np.sqrt(max(values.shape[1], 1))
        recency = np.linspace(-1.0, 0.0, len(values))
        gate = 1.0 / (1.0 + np.exp(-(logits + recency)))
        attention = softmax(logits + np.log(gate + 1e-9))
        attended = attention @ values
        experts = np.stack([attended, np.tanh(attended), attended * state])
        route = softmax(np.asarray([state.mean(), state.std(), abs(state).mean()]))
        update = route @ experts
        # CompSkip: normalized residual prevents depth from erasing the seed.
        state = 0.65 * state + 0.35 * update
        state /= max(np.linalg.norm(state), 1.0)
        expert_trace.append(route.tolist())
    return data.sequences.features @ state + 0.15 * data.popularity, expert_trace
