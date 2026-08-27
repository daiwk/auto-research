from __future__ import annotations

import numpy as np


def objective_scores(data, history):
    """Return calibrated transition, semantic, popularity and value proxies."""
    item_count = data.item_count
    transition = np.zeros(item_count, dtype=np.float64)
    for left, right in zip(history[:-1], history[1:]):
        transition[right] += 1.0 + 0.25 * (left == history[-1])
    if transition.max() > 0:
        transition /= transition.max()
    semantic = data.features @ data.features[list(history[-6:])].mean(0)
    semantic = (semantic - semantic.min()) / max(np.ptp(semantic), 1e-9)
    popularity = np.log1p(data.popularity.astype(np.float64))
    popularity /= max(popularity.max(), 1e-9)
    value = np.sqrt(np.maximum(popularity * semantic, 0.0))
    return np.stack([transition, semantic, popularity, value], axis=1)


def score_fixed(data, history):
    proxies = objective_scores(data, history)
    return np.log(np.maximum(proxies, 1e-6)).mean(1)


def actor_weights(data, history):
    """Context-dependent simplex actor used by the serving path."""
    recent = data.features[list(history[-8:])]
    diversity = float(np.mean(np.std(recent, axis=0)))
    activity = min(len(history) / 30.0, 1.0)
    logits = np.array([
        1.1 - 0.4 * activity,
        0.8 + 1.8 * diversity,
        0.9 - 0.7 * diversity,
        0.6 + 0.8 * activity,
    ])
    weights = np.exp(logits - logits.max())
    return weights / weights.sum()


def score_dceo(data, history):
    proxies = objective_scores(data, history)
    weights = actor_weights(data, history)
    proxy = proxies @ weights
    # The causal-effect intervention is applied only in offline training.  At
    # serving, DCEO contributes one calibrated proxy to the existing formula.
    fixed = score_fixed(data, history)
    return fixed + 0.75 * np.log(np.maximum(proxy, 1e-6))


def causal_diagnostics(data):
    proxy, outcome = [], []
    for history, target in zip(data.train, data.validation):
        scores = objective_scores(data, history) @ actor_weights(data, history)
        proxy.append(float(scores[target]))
        outcome.append(float(data.popularity[target]))
    proxy = np.asarray(proxy)
    outcome = np.asarray(outcome)
    correlation = float(np.corrcoef(proxy, outcome)[0, 1])
    delta = 0.10
    critic_before = outcome.mean() + correlation * (proxy - proxy.mean())
    critic_after = outcome.mean() + correlation * ((1 + delta) * proxy - proxy.mean())
    return {
        "proxy_outcome_correlation": correlation,
        "estimated_relative_causal_effect": float(
            (critic_after - critic_before).mean() / max(abs(critic_before.mean()), 1e-9)
        ),
        "serving_critic_calls": 0,
    }
