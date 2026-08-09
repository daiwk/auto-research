from __future__ import annotations

import numpy as np

from ..industrial_2026 import softmax


def score_ultra_hstu(data, history, layers: int = 6, window: int = 8):
    sequence = np.asarray(history[-48:], dtype=np.int64)
    values = data.sequences.features[sequence].astype(np.float32)
    state = values[-1].astype(np.float64)
    transducer_trace = []
    for layer in range(layers):
        # Semi-local attention alternates local windows and landmark summaries.
        local = values[-window:]
        landmarks = np.stack([values[i:i + window].mean(0) for i in range(0, len(values), window)])
        keys = np.concatenate([local, landmarks], axis=0).astype(np.float64)
        attention = softmax(keys @ state / np.sqrt(max(keys.shape[1], 1)))
        attended = attention @ keys
        # LBSL broadens receptive field without making every layer fully global.
        broad = values[-min(len(values), window * (layer + 1)):].mean(0)
        transducers = np.stack([attended, broad, np.tanh(attended + broad)])
        route = softmax(np.asarray([state.mean(), state.std(), np.dot(attended, broad)]))
        state = 0.55 * state + 0.45 * (route @ transducers)
        state /= max(np.linalg.norm(state), 1.0)
        transducer_trace.append(route.tolist())
    return data.sequences.features @ state + 0.10 * data.popularity, transducer_trace
