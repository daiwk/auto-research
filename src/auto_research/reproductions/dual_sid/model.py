from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes, ridge


def train_dual_sid(data, levels: int = 3, width: int = 8):
    codes = hierarchical_codes(data.sequences.features, levels=levels, width=width)
    one_hot = np.concatenate([np.eye(width)[codes[:, level]] for level in range(levels)], axis=1)
    # Semantic Decoder: reconstruct content from collaborative identity codes.
    decoder = ridge(one_hot, data.sequences.features.astype(np.float64))
    reconstructed = one_hot @ decoder
    reconstructed /= np.maximum(np.linalg.norm(reconstructed, axis=1, keepdims=True), 1e-9)
    transition = []
    for level in range(levels):
        matrix = np.ones((width, width), dtype=float) * 1e-3
        for sequence in data.sequences.train:
            for left, right in zip(sequence, sequence[1:]):
                matrix[codes[left, level], codes[right, level]] += 1
        transition.append(matrix / matrix.sum(axis=1, keepdims=True))
    return {"codes": codes, "decoder": decoder, "reconstructed": reconstructed, "transition": transition}


def score_dual_sid(data, state, history):
    recent = np.asarray(history[-10:], dtype=np.int64)
    identity = np.zeros(data.item_count)
    for level, matrix in enumerate(state["transition"]):
        identity += matrix[state["codes"][recent[-1], level], state["codes"][:, level]]
    identity /= len(state["transition"])
    user_semantic = state["reconstructed"][recent].mean(axis=0)
    semantic = state["reconstructed"] @ user_semantic
    return 0.58 * identity + 0.42 * semantic
