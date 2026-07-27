from __future__ import annotations

import numpy as np

from ..industrial_2026 import hierarchical_codes


def train_glide(data, seed=42):
    codes = hierarchical_codes(data.sequences.features, levels=3, width=8, seed=seed)
    code_transition = np.ones((3, 8, data.item_count)) * 1e-3
    long_term = np.zeros((len(data.sequences.train), data.item_count))
    for user, sequence in enumerate(data.sequences.train):
        long_term[user, list(sequence)] = 1.0
        for left, target in zip(sequence, sequence[1:]):
            for level in range(3):
                code_transition[level, codes[left, level], target] += 1
    code_transition /= code_transition.sum(-1, keepdims=True)

    def scorer(history):
        recent = history[-1]
        semantic = np.mean([
            code_transition[level, codes[recent, level]] for level in range(3)
        ], axis=0)
        profile = np.mean(data.cosine[list(history)], axis=0)
        return 0.65 * semantic + 0.35 * profile

    return scorer, {
        "semantic_id_levels": 3,
        "codes_per_level": 8,
        "recent_history_prompt": True,
        "long_term_soft_prompt": True,
        "autoregressive_code_objective": True,
    }
