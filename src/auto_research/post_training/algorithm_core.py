from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .data import CandidateGroup

@dataclass
class PolicyState:
    weights: np.ndarray
    reference: np.ndarray
    rollout_weights: np.ndarray
    critic_weights: np.ndarray
    reward_axis_weights: np.ndarray
    outcome_ema: float = 0.0
    reference_kl_ema: float = 0.0
    teacher_cache: tuple[np.ndarray, ...] = ()
    teacher_calls: int = 0
    drift_events: int = 0
    ppo_updates: int = 0
    grpo_updates: int = 0
    reco_updates: int = 0
    dapo_updates: int = 0
    gspo_updates: int = 0
    critic_updates: int = 0
    constitutional_critiques: int = 0
    constitutional_revisions: int = 0
    spin_updates: int = 0
    online_teacher_calls: int = 0
    variant_updates: int = 0
    online_rollout_refreshes: int = 0
    global_advantage_second_moment: float = 1.0
    vad_projection_updates: int = 0
    vad_projection_active: int = 0
    vad_alignment_sum: float = 0.0

def initialize(feature_count: int, groups: tuple[CandidateGroup, ...]) -> PolicyState:
    weights = np.zeros(feature_count, dtype=np.float64)
    # Lightning OPD's teacher is fixed and cached before optimization. The
    # teacher combines outcome and process quality; no live teacher is called.
    cache = tuple(_softmax(group.rewards @ np.asarray((4.0, 0.2, 0.8, 0.1))) for group in groups)
    return PolicyState(
        weights=weights,
        reference=weights.copy(),
        rollout_weights=weights.copy(),
        critic_weights=np.zeros(feature_count, dtype=np.float64),
        reward_axis_weights=np.ones(4, dtype=np.float64) / 4,
        teacher_cache=cache,
        teacher_calls=len(groups),
    )

def metrics(state: PolicyState, groups: tuple[CandidateGroup, ...]) -> dict[str, float]:
    correct, reward, entropy, kl = 0, 0.0, 0.0, 0.0
    for group in groups:
        policy = _softmax(group.features @ state.weights)
        reference = _softmax(group.features @ state.reference)
        selected = int(np.argmax(policy))
        correct += int(selected == group.gold)
        reward += float(_scalar_rewards(group)[selected])
        entropy += float(-np.sum(policy * np.log(policy + 1e-12)))
        kl += float(np.sum(policy * np.log((policy + 1e-12) / (reference + 1e-12))))
    size = max(1, len(groups))
    return {
        "accuracy": correct / size,
        "mean_reward": reward / size,
        "entropy": entropy / size,
        "kl_from_reference": kl / size,
    }

def _softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - values.max()
    exponent = np.exp(shifted)
    return exponent / exponent.sum()

def _one_hot(size: int, index: int) -> np.ndarray:
    values = np.zeros(size, dtype=np.float64)
    values[index] = 1.0
    return values

def _scalar_rewards(group: CandidateGroup) -> np.ndarray:
    return group.rewards @ np.asarray((0.7, 0.05, 0.2, 0.05))

def _reinforce_gradient(
    features: np.ndarray,
    probabilities: np.ndarray,
    sampled: np.ndarray,
    advantages: np.ndarray,
) -> np.ndarray:
    expected_features = probabilities @ features
    gradient = np.zeros(features.shape[1], dtype=np.float64)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (features[index] - expected_features)
    return gradient / len(sampled)

def _weighted_policy_gradient(
    features: np.ndarray,
    probabilities: np.ndarray,
    sampled: np.ndarray,
    weights: np.ndarray,
) -> np.ndarray:
    """Policy gradient with an explicit per-rollout weight/mask."""

    expected_features = probabilities @ features
    gradient = np.zeros(features.shape[1], dtype=np.float64)
    for index, weight in zip(sampled, weights):
        gradient += float(weight) * (features[index] - expected_features)
    return gradient / max(1, len(sampled))
