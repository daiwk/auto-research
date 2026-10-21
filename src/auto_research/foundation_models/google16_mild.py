"""mild imbalanced deferral objective, arXiv:2604.27723v1 §5.3.

Only training accepts per-example expert costs. Routing accepts features alone.
No oracle expert, hidden answer, or expert output is passed to router inference.
"""
from __future__ import annotations

import numpy as np


def margin_schedule(counts, feature_bounds=None, *, total=1.0):
    counts = np.asarray(counts, dtype=float)
    bounds = np.ones_like(counts) if feature_bounds is None else np.asarray(feature_bounds, dtype=float)
    if (counts.ndim != 1 or counts.size < 2 or bounds.shape != counts.shape
            or not np.isfinite(counts).all() or not np.isfinite(bounds).all()
            or (counts <= 0).any() or (bounds <= 0).any() or not 0 < total <= 1):
        raise ValueError("positive represented counts/bounds and 0 < total <= 1 required")
    scale = np.cbrt(counts*bounds*bounds)
    return total*scale/scale.sum()


def surrogate_and_gradient(scores, expert_costs, margins):
    scores, costs, rho = map(lambda x: np.asarray(x, dtype=float),
                             (scores, expert_costs, margins))
    if (scores.ndim != 2 or scores.shape != costs.shape or not len(scores)
            or scores.shape[1] < 2 or rho.shape != (scores.shape[1],)
            or not all(np.isfinite(x).all() for x in (scores, costs, rho))
            or (costs < 0).any() or (costs > 1).any() or (rho <= 0).any()):
        raise ValueError("finite NxP scores/costs in [0,1] and positive P margins required")
    rewards = costs.sum(axis=1, keepdims=True)-costs  # Lemma3.1, §6 choice.
    loss = 0.0
    gradient = np.zeros_like(scores)
    for k in range(scores.shape[1]):
        scaled = (scores-scores[:, [k]])/rho[k]
        maximum = scaled.max(axis=1, keepdims=True)
        exp = np.exp(scaled-maximum)
        normalizer = exp.sum(axis=1, keepdims=True)
        loss += float(np.sum(rewards[:, k]*(maximum[:, 0]+np.log(normalizer[:, 0]))))
        local = rewards[:, [k]]*exp/normalizer/rho[k]
        local[:, k] -= rewards[:, k]/rho[k]
        gradient += local
    return loss/len(scores), gradient/len(scores)


def route(features, weights):
    x, w = np.asarray(features, dtype=float), np.asarray(weights, dtype=float)
    if x.ndim != 2 or w.ndim != 2 or x.shape[1] != w.shape[0] or w.shape[1] < 2:
        raise ValueError("compatible features and router weights required")
    if not np.isfinite(x).all() or not np.isfinite(w).all():
        raise ValueError("finite features/weights required")
    scores = x@w
    # The paper resolves score ties by the highest expert index.
    return scores.shape[1]-1-np.argmax(scores[:, ::-1], axis=1)


def fit_router(features, training_costs, margins, *, steps=100, lr=.02, regularization=.001):
    x = np.asarray(features, dtype=float)
    costs = np.asarray(training_costs, dtype=float)
    if (x.ndim != 2 or costs.ndim != 2 or len(x) != len(costs)
            or not np.isfinite(x).all() or not 1 <= steps <= 1000
            or not 0 < lr <= 1 or not 0 <= regularization <= 1):
        raise ValueError("finite training data and bounded optimizer settings required")
    weights = np.zeros((x.shape[1], costs.shape[1]))
    losses = []
    for _ in range(steps):
        loss, gradient = surrogate_and_gradient(x@weights, costs, margins)
        losses.append(loss+regularization*float(np.sum(weights*weights)))
        weights -= lr*(x.T@gradient+2*regularization*weights)
    return weights, losses
