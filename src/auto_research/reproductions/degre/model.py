from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, ridge, softmax


def train_degre(data, seed: int):
    """Train the offline list evaluator, mine beams, and distil dense prefix labels."""
    rng = np.random.default_rng(seed)
    evaluator_x, evaluator_y = [], []
    mined = []
    for user, target in enumerate(data.sequences.validation):
        history = data.sequences.train[user]
        candidates = np.argsort(-base_scores(data, history))[:30]
        for _ in range(24):
            slate = rng.choice(candidates, 6, replace=False)
            relevance = float(target in slate)
            diversity = float(np.mean(1.0 - data.cosine[np.ix_(slate, slate)]))
            novelty = float(np.mean(1.0 - data.popularity[slate]))
            evaluator_x.append([1.0, relevance, diversity, novelty])
            evaluator_y.append(3.0 * relevance + 0.4 * diversity + 0.25 * novelty)
    weights = ridge(np.asarray(evaluator_x), np.asarray(evaluator_y)[:, None]).ravel()

    dense = np.zeros((data.item_count, data.item_count), dtype=np.float64)
    for history, target in zip(data.sequences.train, data.sequences.validation):
        candidates = np.argsort(-base_scores(data, history))[:24]
        beams = [((), 0.0)]
        for _ in range(5):
            expanded = []
            for prefix, _ in beams:
                remaining = [item for item in candidates if item not in prefix]
                for item in remaining:
                    slate = np.asarray((*prefix, item))
                    features = np.asarray([1.0, float(target in slate),
                                           float(np.mean(1.0 - data.cosine[np.ix_(slate, slate)])),
                                           float(np.mean(1.0 - data.popularity[slate]))])
                    expanded.append(((*prefix, int(item)), float(features @ weights)))
            beams = sorted(expanded, key=lambda row: row[1], reverse=True)[:6]
        beam_weights = softmax(np.asarray([score for _, score in beams]) / 0.5)
        anchor = history[-1]
        for (slate, _), beam_weight in zip(beams, beam_weights):
            for position in range(len(slate)):
                remaining = np.asarray([item for item in candidates if item not in slate[:position]])
                values = []
                for item in remaining:
                    prefix = np.asarray((*slate[:position], int(item)))
                    x = np.asarray([1.0, float(target in prefix),
                                    float(np.mean(1.0 - data.cosine[np.ix_(prefix, prefix)])),
                                    float(np.mean(1.0 - data.popularity[prefix]))])
                    values.append(float(x @ weights))
                q = softmax(np.asarray(values))
                dense[anchor, remaining] += beam_weight * q
        mined.append(beams[0][1])
    dense /= np.maximum(dense.sum(1, keepdims=True), 1e-12)
    return weights, dense, {"evaluator_rmse": float(np.sqrt(np.mean((np.asarray(evaluator_x) @ weights - evaluator_y) ** 2))),
                            "mined_beam_value": float(np.mean(mined)), "beam_size": 6, "dense_kl_labels": True}


def score_degre(data, dense, history):
    anchor = history[-1]
    return 0.55 * base_scores(data, history) + 0.45 * dense[anchor]
