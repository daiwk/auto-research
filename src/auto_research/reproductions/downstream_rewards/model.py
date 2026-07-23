from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, ridge


def _candidate_signals(data, history):
    recent_domains = data.domains[list(history[-8:])]
    seen = set(int(value) for value in recent_domains)
    deep_exploration = 1.0 - np.asarray([int(domain) in seen for domain in data.domains], dtype=np.float64)
    continuation = np.mean(data.transition[list(history[-4:])], axis=0)
    content_depth = np.mean(data.cosine[list(history[-4:])], axis=0)
    shallow_closeup = data.popularity * (1.0 - content_depth)
    return np.stack([continuation, content_depth, deep_exploration, -shallow_closeup], axis=1)


def learn_downstream_rewards(data):
    rows, targets = [], []
    for sequence in data.sequences.train:
        for end in range(3, len(sequence)):
            history, target = sequence[max(0, end - 8):end], sequence[end]
            signals = _candidate_signals(data, history)
            future = sequence[end:min(len(sequence), end + 4)]
            future_domains = {int(data.domains[item]) for item in future}
            retention_proxy = 1.0 + 0.4 * len(future_domains)
            rows.append(signals[target])
            targets.append(retention_proxy)
    matrix = np.asarray(rows)
    target = np.asarray(targets)
    correlations = [
        float(np.corrcoef(matrix[:, index], target)[0, 1])
        if np.std(matrix[:, index]) > 1e-9 else 0.0
        for index in range(matrix.shape[1])
    ]
    selected = [index for index, value in enumerate(correlations) if value > 0.0]
    if not selected:
        selected = [int(np.argmax(correlations))]
    coefficients = np.zeros(matrix.shape[1])
    coefficients[selected] = ridge(matrix[:, selected], target, regularization=0.1)
    return coefficients, {
        "candidate_rewards": ["deeper transition", "content depth", "new use-case exploration", "negative shallow closeup"],
        "offline_screening_correlations": correlations,
        "selected_reward_indices": selected,
        "model_agnostic_reward_heads": len(selected),
    }


def score_with_rewards(data, coefficients, history):
    rewards = _candidate_signals(data, history) @ coefficients
    rewards = (rewards - rewards.mean()) / max(rewards.std(), 1e-6)
    return base_scores(data, history) + 0.12 * rewards
