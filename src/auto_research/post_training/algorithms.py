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
    dapo_updates: int = 0
    gspo_updates: int = 0
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
        if algorithm in {"ppo-rlhf", "grpo", "dapo", "gspo"} else probabilities
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
    elif algorithm == "kto":
        chosen = group.gold
        rejected = int(np.argmax(probabilities + (np.arange(len(probabilities)) == chosen) * -2))
        log_ratio = np.log(probabilities + 1e-12) - np.log(reference + 1e-12)
        observed_kl = float(np.sum(probabilities * log_ratio))
        state.reference_kl_ema = 0.9 * state.reference_kl_ema + 0.1 * observed_kl
        beta = 0.2
        desirable = 1.0 / (
            1.0 + np.exp(-beta * (log_ratio[chosen] - state.reference_kl_ema))
        )
        undesirable = 1.0 / (
            1.0 + np.exp(-beta * (state.reference_kl_ema - log_ratio[rejected]))
        )
        expected = probabilities @ group.features
        chosen_score = group.features[chosen] - expected
        rejected_score = group.features[rejected] - expected
        gradient = (
            beta * desirable * (1.0 - desirable) * chosen_score
            - beta * undesirable * (1.0 - undesirable) * rejected_score
        )
        loss = float(2.0 - desirable - undesirable)
        diagnostics.update(
            {
                "desirable_utility": float(desirable),
                "undesirable_utility": float(undesirable),
                "reference_kl_ema": state.reference_kl_ema,
                "pairwise_preferences_required": 0.0,
            }
        )
    elif algorithm == "orpo":
        chosen = group.gold
        rejected = int(np.argmax(probabilities + (np.arange(len(probabilities)) == chosen) * -2))
        expected = probabilities @ group.features
        chosen_score = group.features[chosen] - expected
        rejected_score = group.features[rejected] - expected
        log_odds_margin = float(
            np.log(probabilities[chosen] + 1e-12)
            - np.log(1.0 - probabilities[chosen] + 1e-12)
            - np.log(probabilities[rejected] + 1e-12)
            + np.log(1.0 - probabilities[rejected] + 1e-12)
        )
        preference_strength = 1.0 / (1.0 + np.exp(log_odds_margin))
        odds_gradient = (
            chosen_score / (1.0 - probabilities[chosen] + 1e-12)
            - rejected_score / (1.0 - probabilities[rejected] + 1e-12)
        )
        gradient = chosen_score + 0.1 * preference_strength * odds_gradient
        loss = float(
            -np.log(probabilities[chosen] + 1e-12)
            + 0.1 * np.logaddexp(0.0, -log_odds_margin)
        )
        diagnostics.update(
            {
                "log_odds_margin": log_odds_margin,
                "reference_model_parameters": 0.0,
                "sft_nll": float(-np.log(probabilities[chosen] + 1e-12)),
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
    elif algorithm == "dapo":
        scalar = _scalar_rewards(group)[sampled]
        pseudo_lengths = np.maximum(
            1.0, np.rint(4.0 * group.features[sampled, 6])
        )
        overlong_penalty = 0.05 * np.maximum(pseudo_lengths - 3.0, 0.0)
        shaped = scalar - overlong_penalty
        reward_std = float(shaped.std())
        diagnostics.update(
            {
                "clip_low": 0.2,
                "clip_high": 0.28,
                "mean_pseudo_tokens": float(pseudo_lengths.mean()),
                "overlong_penalty": float(overlong_penalty.mean()),
            }
        )
        if reward_std < 1e-8:
            gradient = np.zeros_like(state.weights)
            loss = 0.0
            diagnostics["dynamic_sample_skipped"] = 1.0
            diagnostics["clip_fraction"] = 0.0
        else:
            advantages = (shaped - shaped.mean()) / (reward_std + 1e-6)
            ratios = probabilities[sampled] / (sampling_probabilities[sampled] + 1e-12)
            clipped = np.clip(ratios, 0.8, 1.28)
            surrogate = np.minimum(ratios * advantages, clipped * advantages)
            active = np.isclose(surrogate, ratios * advantages)
            token_weights = pseudo_lengths / pseudo_lengths.sum()
            expected = probabilities @ group.features
            gradient = np.zeros_like(state.weights)
            for index, advantage, ratio, is_active, weight in zip(
                sampled, advantages, ratios, active, token_weights
            ):
                if is_active:
                    gradient += float(weight * advantage * ratio) * (
                        group.features[index] - expected
                    )
            gradient -= 0.02 * (group.features.T @ (probabilities - reference))
            loss = float(-np.sum(token_weights * surrogate))
            diagnostics.update(
                {
                    "dynamic_sample_skipped": 0.0,
                    "clip_fraction": float(np.mean(~active)),
                }
            )
        state.dapo_updates += 1
    elif algorithm == "gspo":
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        pseudo_lengths = np.maximum(
            1.0, np.rint(4.0 * group.features[sampled, 6])
        )
        log_sequence_ratio = (
            np.log(probabilities[sampled] + 1e-12)
            - np.log(sampling_probabilities[sampled] + 1e-12)
        ) / pseudo_lengths
        sequence_ratios = np.exp(log_sequence_ratio)
        clipped = np.clip(sequence_ratios, 0.8, 1.2)
        surrogate = np.minimum(
            sequence_ratios * advantages, clipped * advantages
        )
        active = np.isclose(surrogate, sequence_ratios * advantages)
        expected = probabilities @ group.features
        gradient = np.zeros_like(state.weights)
        for index, advantage, ratio, is_active, length in zip(
            sampled, advantages, sequence_ratios, active, pseudo_lengths
        ):
            if is_active:
                gradient += float(advantage * ratio / length) * (
                    group.features[index] - expected
                )
        gradient /= len(sampled)
        gradient -= 0.02 * (group.features.T @ (probabilities - reference))
        state.gspo_updates += 1
        loss = float(-surrogate.mean())
        diagnostics.update(
            {
                "sequence_ratio_mean": float(sequence_ratios.mean()),
                "sequence_ratio_std": float(sequence_ratios.std()),
                "clip_fraction": float(np.mean(~active)),
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
    if algorithm == "dapo" and state.dapo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "gspo" and state.gspo_updates % 16 == 0:
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
