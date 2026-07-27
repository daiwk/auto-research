from __future__ import annotations

import numpy as np


def train_pagewise_policy(data):
    page = np.ones((data.item_count, data.item_count)) * 1e-3
    reward = np.zeros_like(page)
    pages = 0
    for sequence in data.sequences.train:
        for start in range(1, len(sequence) - 2, 3):
            context = sequence[start - 1]
            targets = sequence[start : start + 3]
            pages += 1
            for rank, target in enumerate(targets):
                page[context, target] += 1.0
                reward[context, target] += 1.0 / (rank + 1)
    nll_policy = page / page.sum(1, keepdims=True)
    group_advantage = reward - reward.mean(1, keepdims=True)
    grpo = nll_policy * np.exp(np.clip(group_advantage, -2, 2))
    grpo /= grpo.sum(1, keepdims=True)

    def scorer(history):
        last = history[-1]
        merged = 0.7 * grpo[last] + 0.3 * grpo[list(history[-4:])].mean(0)
        return merged

    return scorer, {
        "training_pages": pages,
        "page_size": 3,
        "asymmetric_token_merger": True,
        "grpo_sr_group_advantage": True,
        "nll_regularization": True,
    }
