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
    constitutional_critiques: int = 0
    constitutional_revisions: int = 0
    spin_updates: int = 0


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
        if algorithm in {"ppo-rlhf", "grpo", "dapo", "gspo", "spin"} else probabilities
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
    elif algorithm == "constitutional-ai":
        # Candidate-level analogue of Constitutional AI's two phases:
        # critique/revision SFT first moves probability toward the response
        # that best satisfies an explicit constitution, then an AI-generated
        # preference adds a reference-relative ranking update.
        constitution = np.asarray((0.55, 0.10, 0.25, 0.10))
        constitutional_scores = group.rewards @ constitution
        initial = int(np.argmax(probabilities))
        revised = int(np.argmax(constitutional_scores))
        rejected = int(np.argmin(constitutional_scores))
        expected = probabilities @ group.features
        revision_gradient = group.features[revised] - expected
        margin = (
            np.log(probabilities[revised] + 1e-12)
            - np.log(probabilities[rejected] + 1e-12)
            - np.log(reference[revised] + 1e-12)
            + np.log(reference[rejected] + 1e-12)
        )
        beta = 0.2
        preference_strength = beta / (1.0 + np.exp(beta * margin))
        preference_gradient = preference_strength * (
            group.features[revised] - group.features[rejected]
        )
        gradient = revision_gradient + preference_gradient
        loss = float(
            -np.log(probabilities[revised] + 1e-12)
            + np.logaddexp(0.0, -beta * margin)
        )
        diagnostics.update(
            {
                "constitutional_principles": float(len(constitution)),
                "critique_violation": float(
                    constitutional_scores[revised] - constitutional_scores[initial]
                ),
                "revision_changed": float(initial != revised),
                "ai_preference_margin": float(margin),
                "human_preference_labels": 0.0,
            }
        )
        state.constitutional_critiques += 1
        state.constitutional_revisions += int(initial != revised)
        diagnostics["cumulative_critiques"] = float(state.constitutional_critiques)
        diagnostics["cumulative_revisions"] = float(state.constitutional_revisions)
    elif algorithm == "rrhf":
        # RRHF ranks every sampled response by reward and enforces the same
        # ordering on sequence log-probabilities, while retaining SFT on the
        # best response. Candidate probabilities stand in for normalized
        # response log-likelihoods in this auditable L1 model.
        scalar = _scalar_rewards(group)
        response_scores = np.log(probabilities + 1e-12)
        expected = probabilities @ group.features
        best = int(np.argmax(scalar))
        ranking_gradient = np.zeros_like(state.weights)
        violations = 0
        pairs = 0
        ranking_loss = 0.0
        for preferred in range(len(scalar)):
            for dispreferred in range(len(scalar)):
                if scalar[preferred] <= scalar[dispreferred]:
                    continue
                pairs += 1
                violation = response_scores[dispreferred] - response_scores[preferred]
                if violation > 0:
                    violations += 1
                    ranking_loss += float(violation)
                    ranking_gradient += (
                        group.features[preferred] - group.features[dispreferred]
                    )
        gradient = (group.features[best] - expected) + ranking_gradient / max(1, pairs)
        loss = float(-response_scores[best] + ranking_loss / max(1, pairs))
        diagnostics.update(
            {
                "ranked_responses": float(len(scalar)),
                "ranking_pairs": float(pairs),
                "ranking_violations": float(violations),
                "best_of_n_reward": float(scalar[best]),
                "sft_best_nll": float(-response_scores[best]),
            }
        )
    elif algorithm == "raft":
        # RAFT repeatedly samples from the current policy, reward-ranks that
        # batch, keeps its best response, and performs ordinary fine-tuning on
        # the filtered response. Unlike RRHF, discarded samples contribute no
        # pairwise loss.
        scalar = _scalar_rewards(group)
        selected = int(sampled[np.argmax(scalar[sampled])])
        expected = probabilities @ group.features
        gradient = group.features[selected] - expected
        loss = float(-np.log(probabilities[selected] + 1e-12))
        diagnostics.update(
            {
                "sampled_responses": float(len(sampled)),
                "kept_responses": 1.0,
                "kept_fraction": float(1.0 / len(sampled)),
                "selected_reward": float(scalar[selected]),
                "selected_reward_quantile": float(
                    np.mean(scalar <= scalar[selected])
                ),
                "reward_model_used_for_selection": 1.0,
            }
        )
    elif algorithm == "slic-hf":
        # SLiC-HF calibrates response sequence likelihoods to preference
        # ordering with a margin loss, while supervised cross-entropy on the
        # reference target preserves the pretrained/SFT behavior.
        chosen = group.gold
        rejected = int(
            np.argmax(probabilities + (np.arange(len(probabilities)) == chosen) * -2)
        )
        log_gap = float(
            np.log(probabilities[chosen] + 1e-12)
            - np.log(probabilities[rejected] + 1e-12)
        )
        margin = 0.5
        violation = max(0.0, margin - log_gap)
        calibration_gradient = (
            group.features[chosen] - group.features[rejected]
            if violation > 0 else np.zeros_like(state.weights)
        )
        expected = probabilities @ group.features
        regularization_gradient = group.features[chosen] - expected
        regularization_weight = 0.1
        gradient = calibration_gradient + regularization_weight * regularization_gradient
        sft_regularization_nll = float(-np.log(probabilities[chosen] + 1e-12))
        loss = float(violation + regularization_weight * sft_regularization_nll)
        diagnostics.update(
            {
                "calibration_margin": margin,
                "sequence_log_likelihood_gap": log_gap,
                "margin_violation": violation,
                "sft_regularization_nll": sft_regularization_nll,
                "reference_model_parameters": 0.0,
                "off_policy_preferences": 1.0,
            }
        )
    elif algorithm == "steerlm":
        # The four reward axes are explicit local annotations analogous to
        # SteerLM's helpfulness/correctness/coherence/complexity attributes.
        # The target attribute vector is supplied to candidate selection, then
        # ordinary SFT conditions the policy on the selected attribute profile.
        target_attributes = np.asarray((1.0, 0.4, 0.8, 0.2))
        target_attributes /= np.linalg.norm(target_attributes)
        normalized = group.rewards / (
            np.linalg.norm(group.rewards, axis=1, keepdims=True) + 1e-12
        )
        attribute_match = normalized @ target_attributes
        conditioned = int(np.argmax(attribute_match))
        expected = probabilities @ group.features
        gradient = group.features[conditioned] - expected
        loss = float(-np.log(probabilities[conditioned] + 1e-12))
        diagnostics.update(
            {
                "attribute_dimensions": float(group.rewards.shape[1]),
                "annotated_responses": float(len(group.rewards)),
                "target_attribute_match": float(attribute_match[conditioned]),
                "attribute_conditioned_sft": 1.0,
                "reward_model_parameters": 0.0,
            }
        )
    elif algorithm == "spin":
        # SPIN treats the previous-iteration policy as an opponent: a human
        # demonstration is preferred over a response sampled from that frozen
        # opponent, and the opponent is refreshed only at iteration boundaries.
        opponent = _softmax(group.features @ state.rollout_weights)
        chosen = group.gold
        rejected = int(rng.choice(len(opponent), p=opponent))
        if rejected == chosen:
            rejected = int(
                np.argmax(opponent + (np.arange(len(opponent)) == chosen) * -2)
            )
        logit = float(
            np.log(probabilities[chosen] + 1e-12)
            - np.log(opponent[chosen] + 1e-12)
            - np.log(probabilities[rejected] + 1e-12)
            + np.log(opponent[rejected] + 1e-12)
        )
        beta = 0.2
        coefficient = beta / (1.0 + np.exp(beta * logit))
        gradient = coefficient * (
            group.features[chosen] - group.features[rejected]
        )
        loss = float(np.logaddexp(0.0, -beta * logit))
        state.spin_updates += 1
        diagnostics.update(
            {
                "self_play_logit": logit,
                "opponent_response_probability": float(opponent[rejected]),
                "human_demonstration_probability": float(probabilities[chosen]),
                "opponent_iteration": float(state.spin_updates // 16),
                "external_preference_labels": 0.0,
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
    if algorithm == "spin" and state.spin_updates % 16 == 0:
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
