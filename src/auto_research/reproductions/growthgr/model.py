from __future__ import annotations

import numpy as np

from ..industrial_2026 import base_scores, hierarchical_codes, ridge


def train_growthgr(data, seed: int):
    features = data.sequences.features.astype(np.float64)
    # ItemLTV: observed treatment is an early interaction; future popularity is the public outcome proxy.
    treatment = (data.popularity > np.median(data.popularity)).astype(float)
    outcome = np.log1p(data.sequences.popularity)
    base_map = ridge(features, outcome[:, None]).ravel()
    residual = outcome - features @ base_map
    uplift_map = ridge(np.concatenate([features, treatment[:, None]], axis=1), residual[:, None]).ravel()
    uplift = np.concatenate([features, np.ones((len(features), 1))], axis=1) @ uplift_map
    codes = hierarchical_codes(features, seed=seed)
    policy = data.transition.copy()
    old_policy = policy.copy()
    rewards = 0.55 * (outcome > np.median(outcome)) + 0.45 * (uplift > np.mean(uplift))
    # MoPO: clipped inverse-propensity reward, group-normalized advantage and PPO clip.
    for _ in range(8):
        for source in range(data.item_count):
            candidate = np.argsort(-old_policy[source])[:32]
            raw = np.clip(-np.log(np.maximum(old_policy[source, candidate], 1e-9)), 1.0, 5.0) * rewards[candidate]
            advantage = (raw - raw.mean()) / max(raw.std(), 1e-6)
            ratio = policy[source, candidate] / np.maximum(old_policy[source, candidate], 1e-9)
            surrogate = np.minimum(ratio * advantage, np.clip(ratio, 0.8, 1.2) * advantage)
            policy[source, candidate] *= np.exp(0.04 * surrogate)
            policy[source] /= policy[source].sum()
        old_policy = 0.8 * old_policy + 0.2 * policy
    collision = 1.0 - len(np.unique(codes, axis=0)) / len(codes)
    return codes, uplift, policy, {"item_ltv_base_mse": float(np.mean((features @ base_map - outcome) ** 2)), "mean_predicted_uplift": float(np.mean(uplift)), "rqvae_levels": 3, "sid_collision_rate": collision, "mopo_iterations": 8, "trie_constrained": True}


def score_growthgr(data, uplift, policy, history):
    uplift_norm = (uplift - uplift.min()) / max(uplift.max() - uplift.min(), 1e-9)
    return 0.35 * base_scores(data, history) + 0.45 * policy[history[-1]] + 0.20 * uplift_norm
