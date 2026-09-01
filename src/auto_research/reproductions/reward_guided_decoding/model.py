from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, softmax


def reward_guided_distribution(
    generator_scores: np.ndarray,
    reward: np.ndarray,
    beta: float = 0.55,
) -> np.ndarray:
    prior = softmax(generator_scores)
    logits = np.log(np.maximum(prior, 1e-12)) + reward / beta
    return softmax(logits)


def business_reward(data, history) -> np.ndarray:
    novelty = 1.0 - data.popularity
    content = data.cosine[np.asarray(history[-8:], dtype=np.int64)].mean(0)
    return 0.60 * content + 0.40 * novelty


def score_generator(data, history) -> np.ndarray:
    return base_scores(data, history)


def score_reward_guided(data, history, beta: float = 0.55) -> np.ndarray:
    return reward_guided_distribution(
        score_generator(data, history),
        business_reward(data, history),
        beta,
    )


def rgd_diagnostics(data, history, beta: float = 0.55) -> dict[str, float]:
    prior = softmax(score_generator(data, history))
    guided = score_reward_guided(data, history, beta)
    reward = business_reward(data, history)
    kl = float(np.sum(guided * (np.log(np.maximum(guided, 1e-12)) - np.log(np.maximum(prior, 1e-12)))))
    return {
        "beta": float(beta),
        "prior_expected_reward": float(prior @ reward),
        "guided_expected_reward": float(guided @ reward),
        "kl_from_generator": kl,
        "generator_retrained": False,
    }
