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
    teacher_cache: tuple[np.ndarray, ...] = ()
    teacher_calls: int = 0
    drift_events: int = 0
    ppo_updates: int = 0
    grpo_updates: int = 0
    critic_updates: int = 0


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


def update(
    algorithm: str,
    state: PolicyState,
    group: CandidateGroup,
    learning_rate: float,
    rng: np.random.Generator,
    group_size: int,
    cache_index: int,
) -> tuple[float, dict[str, float]]:
    probabilities = _softmax(group.features @ state.weights)
    reference = _softmax(group.features @ state.reference)
    sampling_probabilities = (
        _softmax(group.features @ state.rollout_weights)
        if algorithm in {"ppo-rlhf", "grpo"} else probabilities
    )
    sampled = rng.choice(
        len(probabilities), size=min(group_size, len(probabilities)),
        replace=False, p=sampling_probabilities,
    )
    diagnostics: dict[str, float] = {}

    if algorithm == "dpo":
        chosen = group.gold
        rejected = int(np.argmax(probabilities + (np.arange(len(probabilities)) == chosen) * -2))
        margin = (
            np.log(probabilities[chosen] + 1e-12)
            - np.log(probabilities[rejected] + 1e-12)
            - np.log(reference[chosen] + 1e-12)
            + np.log(reference[rejected] + 1e-12)
        )
        beta = 0.2
        coefficient = beta / (1.0 + np.exp(beta * margin))
        gradient = coefficient * (group.features[chosen] - group.features[rejected])
        loss = float(np.logaddexp(0.0, -beta * margin))
        diagnostics.update(
            {
                "preference_margin": float(margin),
                "chosen_probability": float(probabilities[chosen]),
                "rejected_probability": float(probabilities[rejected]),
                "reward_model_parameters": 0.0,
            }
        )
    elif algorithm == "lightning-opd":
        teacher = state.teacher_cache[cache_index]
        gradient = group.features.T @ (teacher - probabilities)
        loss = float(-np.sum(teacher * np.log(probabilities + 1e-12)))
        diagnostics["cached_teacher_tokens"] = float(len(teacher))
        diagnostics["online_teacher_calls"] = 0.0
    elif algorithm == "ppo-rlhf":
        scalar = _scalar_rewards(group)[sampled]
        values = group.features[sampled] @ state.critic_weights
        advantages = scalar - values
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-6)
        ratios = probabilities[sampled] / (sampling_probabilities[sampled] + 1e-12)
        clipped_ratios = np.clip(ratios, 0.8, 1.2)
        surrogate = np.minimum(ratios * advantages, clipped_ratios * advantages)
        active = np.isclose(surrogate, ratios * advantages)
        expected_features = probabilities @ group.features
        gradient = np.zeros_like(state.weights)
        for index, advantage, ratio, is_active in zip(sampled, advantages, ratios, active):
            if is_active:
                gradient += float(advantage * ratio) * (
                    group.features[index] - expected_features
                )
        gradient /= len(sampled)
        gradient -= 0.02 * (group.features.T @ (probabilities - reference))
        value_error = scalar - values
        state.critic_weights += learning_rate * np.mean(
            value_error[:, None] * group.features[sampled], axis=0
        )
        state.critic_updates += 1
        state.ppo_updates += 1
        loss = float(-surrogate.mean())
        diagnostics.update(
            {
                "clip_fraction": float(np.mean(~active)),
                "importance_ratio": float(ratios.mean()),
                "value_loss": float(np.mean(value_error ** 2)),
                "critic_updates": float(state.critic_updates),
            }
        )
    elif algorithm == "grpo":
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        ratios = probabilities[sampled] / (sampling_probabilities[sampled] + 1e-12)
        clipped_ratios = np.clip(ratios, 0.8, 1.2)
        surrogate = np.minimum(ratios * advantages, clipped_ratios * advantages)
        active = np.isclose(surrogate, ratios * advantages)
        expected_features = probabilities @ group.features
        gradient = np.zeros_like(state.weights)
        for index, advantage, ratio, is_active in zip(sampled, advantages, ratios, active):
            if is_active:
                gradient += float(advantage * ratio) * (
                    group.features[index] - expected_features
                )
        gradient /= len(sampled)
        gradient -= 0.02 * (group.features.T @ (probabilities - reference))
        state.grpo_updates += 1
        loss = float(-surrogate.mean())
        diagnostics.update(
            {
                "group_reward_mean": float(scalar.mean()),
                "group_reward_std": float(scalar.std()),
                "clip_fraction": float(np.mean(~active)),
                "importance_ratio": float(ratios.mean()),
                "value_model_parameters": 0.0,
            }
        )
    elif algorithm == "rloo":
        scalar = _scalar_rewards(group)[sampled]
        shaped = scalar - 0.02 * np.log(
            (probabilities[sampled] + 1e-12) / (reference[sampled] + 1e-12)
        )
        advantages = np.asarray(
            [
                reward - (shaped.sum() - reward) / max(1, len(shaped) - 1)
                for reward in shaped
            ]
        )
        gradient = _reinforce_gradient(group.features, probabilities, sampled, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
        diagnostics.update(
            {
                "leave_one_out_samples": float(len(sampled)),
                "leave_one_out_variance": float(np.var(advantages)),
                "value_model_parameters": 0.0,
            }
        )
    elif algorithm == "remax":
        scalar = _scalar_rewards(group)
        greedy = int(np.argmax(probabilities))
        advantages = scalar[sampled] - scalar[greedy]
        gradient = _reinforce_gradient(group.features, probabilities, sampled, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
        diagnostics.update(
            {
                "greedy_baseline_reward": float(scalar[greedy]),
                "sample_reward": float(scalar[sampled].mean()),
                "value_model_parameters": 0.0,
            }
        )
    else:
        rewards = group.rewards[sampled]
        if algorithm == "gprl":
            normalized = (rewards - rewards.mean(0)) / (rewards.std(0) + 1e-6)
            advantages = normalized @ state.reward_axis_weights
            # A normalized axis always has zero mean, so drift must be measured
            # before normalization. Compare each axis' operating point with the
            # group-wide reward level to detect an exploitable dominant axis.
            axis_drift = np.abs(rewards.mean(0) - rewards.mean())
            if float(axis_drift.max()) > 0.25:
                state.reward_axis_weights = 1.0 / (axis_drift + 0.25)
                state.reward_axis_weights /= state.reward_axis_weights.sum()
                state.drift_events += 1
            diagnostics["preference_axes"] = 4.0
            diagnostics["drift_events"] = float(state.drift_events)
        elif algorithm == "tcr":
            outcome = rewards[:, 0]
            process = rewards[:, 2]
            state.outcome_ema = 0.9 * state.outcome_ema + 0.1 * float(outcome.mean())
            thinking_surplus = process - state.outcome_ema
            advantages = outcome + 0.5 * thinking_surplus
            advantages -= advantages.mean()
            diagnostics["outcome_ema"] = state.outcome_ema
            diagnostics["thinking_surplus"] = float(thinking_surplus.mean())
        else:  # Defensive fallback; config rejects unknown algorithms.
            scalar = rewards @ np.asarray((0.7, 0.05, 0.2, 0.05))
            advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        gradient = np.zeros_like(state.weights)
        expected_features = probabilities @ group.features
        for index, advantage in zip(sampled, advantages):
            gradient += float(advantage) * (group.features[index] - expected_features)
        gradient /= len(sampled)
        kl_gradient = group.features.T @ (probabilities - reference)
        gradient -= 0.02 * kl_gradient
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))

    state.weights += learning_rate * np.clip(gradient, -5.0, 5.0)
    if algorithm == "ppo-rlhf" and state.ppo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "grpo" and state.grpo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    diagnostics["loss"] = loss
    diagnostics["policy_entropy"] = float(-np.sum(probabilities * np.log(probabilities + 1e-12)))
    return loss, diagnostics


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
