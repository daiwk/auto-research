"""Extracted unchanged from auto_research.post_training.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def rfpo_advantages(critic_values, *, gamma=0.99, gae_lambda=0.95, length_bias=0.0):
    """Frozen-critic reward, debiasing, binarization and GAE."""
    import numpy as np

    values = np.asarray(critic_values, dtype=np.float64)
    if values.ndim != 1 or len(values) < 2:
        raise ValueError("critic values require at least two prefix states")
    debiased = values - length_bias * np.arange(len(values))
    rewards = (debiased[1:] >= 0.5).astype(np.float64)
    deltas = rewards + gamma * debiased[1:] - debiased[:-1]
    advantages = np.zeros_like(deltas)
    running = 0.0
    for index in range(len(deltas) - 1, -1, -1):
        running = deltas[index] + gamma * gae_lambda * running
        advantages[index] = running
    return advantages, {"positive_rewards": int(rewards.sum()), "critic_frozen": True}
