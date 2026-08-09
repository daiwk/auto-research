from __future__ import annotations

import numpy as np

from ..algorithm_core import (PolicyState, _one_hot, _reinforce_gradient, _scalar_rewards, _softmax, _weighted_policy_gradient)
from ..data import CandidateGroup
from ..rollout_correction import (icepop_weights, rollout_engine_probabilities, truncated_importance_weights)

def apply(algorithm, state, group, learning_rate, rng, group_size, cache_index, probabilities, reference, rollout_training_probabilities, sampling_probabilities, sampled, diagnostics):
    if algorithm == 'flux-opd':
        anchor = state.teacher_cache[cache_index]
        quality = _softmax(np.log(anchor + 1e-12) + group.rewards[:, 0])
        process = _softmax(np.log(anchor + 1e-12) + group.rewards[:, 2])
        corrections = 0.5 * (
            np.log(quality + 1e-12) - np.log(anchor + 1e-12)
            + np.log(process + 1e-12) - np.log(anchor + 1e-12)
        )
        midpoint = 0.5 * (quality + process)
        conflict = 0.5 * np.sum(
            quality * np.log((quality + 1e-12) / (midpoint + 1e-12))
            + process * np.log((process + 1e-12) / (midpoint + 1e-12))
        )
        correction_weight = float(np.exp(-4.0 * conflict))
        target = _softmax(np.log(anchor + 1e-12) + correction_weight * corrections)
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.online_teacher_calls += 2 * len(sampled)
        diagnostics.update({
            "context_free_anchor": 1.0,
            "evolving_context_teachers": 2.0,
            "context_conflict_jsd": float(conflict),
            "conflict_weighted_correction": correction_weight,
            "contextual_difference_signal_norm": float(np.linalg.norm(corrections)),
        })
    elif algorithm == 'lightning-opd':
        teacher = state.teacher_cache[cache_index]
        gradient = group.features.T @ (teacher - probabilities)
        loss = float(-np.sum(teacher * np.log(probabilities + 1e-12)))
        diagnostics["cached_teacher_tokens"] = float(len(teacher))
        diagnostics["online_teacher_calls"] = 0.0
    elif algorithm == 'relay-opd':
        teacher = state.teacher_cache[cache_index]
        teacher_choice = int(np.argmax(teacher))
        student_choice = int(np.argmax(probabilities))
        prefix_failure = student_choice != teacher_choice
        relay_budget = 0.25
        relayed = (
            (1.0 - relay_budget) * teacher
            + relay_budget * np.eye(len(teacher))[teacher_choice]
            if prefix_failure else teacher
        )
        gradient = group.features.T @ (relayed - probabilities)
        loss = float(-np.sum(relayed * np.log(probabilities + 1e-12)))
        diagnostics.update({
            "prefix_failure_detected": float(prefix_failure),
            "teacher_handoff_triggered": float(prefix_failure),
            "relay_budget": relay_budget,
            "student_resumes_after_teacher_leg": 1.0,
            "estimated_trajectory_reduction": 0.5 if prefix_failure else 0.0,
        })
    elif algorithm == 'turn-opd':
        teacher = state.teacher_cache[cache_index]
        pseudo_turns = np.arange(1, len(teacher) + 1, dtype=np.float64)
        probe_information = teacher * (1.0 - probabilities)
        depth_budget = max(2, int(np.ceil(0.75 * len(teacher))))
        active = np.argsort(-probe_information)[:depth_budget]
        weights = np.zeros_like(teacher)
        weights[active] = pseudo_turns[active]
        weights /= max(weights.sum(), 1e-9)
        target = teacher * weights
        target /= max(target.sum(), 1e-9)
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        diagnostics.update({
            "adaptive_rollout_depth": float(depth_budget),
            "maximum_rollout_depth": float(len(teacher)),
            "turn_normalized_loss": 1.0,
            "deep_turn_weight_share": float(weights[len(weights) // 2:].sum()),
            "wall_clock_budget_equalized": 1.0,
        })
    elif algorithm == 'seed':
        scalar = _scalar_rewards(group)
        hindsight_skill = (
            0.65 * group.rewards[:, 2]
            + 0.25 * group.rewards[:, 0]
            - 0.10 * group.rewards[:, 3]
        )
        skill_policy = _softmax(
            group.features @ state.weights + 0.75 * hindsight_skill
        )
        probability_shift = np.log(skill_policy + 1e-12) - np.log(
            probabilities + 1e-12
        )
        dense_advantage = probability_shift[sampled]
        outcome_advantage = scalar[sampled] - scalar[sampled].mean()
        advantages = outcome_advantage + 0.5 * dense_advantage
        gradient = _reinforce_gradient(
            group.features, probabilities, sampled, advantages
        )
        loss = float(
            -np.mean(advantages * np.log(probabilities[sampled] + 1e-12))
        )
        diagnostics.update({
            "hindsight_skills_extracted": float(len(sampled)),
            "skill_augmented_logprob_shift": float(
                probability_shift[sampled].mean()
            ),
            "dense_opd_signal": 1.0,
            "outcome_rl_signal": 1.0,
            "self_evolving_analyzer": 1.0,
        })
    elif algorithm == 'cast':
        scalar = _scalar_rewards(group)[sampled]
        solver_values = (
            0.6 * group.rewards[sampled, 0]
            + 0.4 * group.rewards[sampled, 2]
        )
        turn_advantage = solver_values - solver_values.mean()
        outcome_advantage = scalar - scalar.mean()
        advantages = outcome_advantage + turn_advantage
        gradient = _reinforce_gradient(
            group.features, probabilities, sampled, advantages
        )
        loss = float(
            -np.mean(advantages * np.log(probabilities[sampled] + 1e-12))
        )
        diagnostics.update({
            "solver_value_queries": float(len(sampled) + 1),
            "turn_level_solver_advantage": float(np.abs(turn_advantage).mean()),
            "teacher_logits_required": 0.0,
            "outcome_reward_combined": 1.0,
        })
    elif algorithm == 'cort':
        scalar = _scalar_rewards(group)[sampled]
        response_advantage = scalar - scalar.mean()
        rubric_direction = np.linspace(
            0.25, 1.0, group.features.shape[1], dtype=np.float64
        )
        conditioned = group.features[sampled] @ rubric_direction
        criteria_free = group.features[sampled] @ np.roll(
            rubric_direction, 1
        )
        contrasts = np.abs(conditioned - criteria_free)
        token_weights = contrasts / max(contrasts.mean(), 1e-9)
        token_weights = np.clip(token_weights, 0.25, 2.0)
        advantages = response_advantage * token_weights
        gradient = _reinforce_gradient(
            group.features, probabilities, sampled, advantages
        )
        loss = float(
            -np.mean(advantages * np.log(probabilities[sampled] + 1e-12))
        )
        diagnostics.update({
            "counterfactual_replays": float(2 * len(sampled)),
            "rubric_conditioned_contrast": float(contrasts.mean()),
            "token_weight_min": float(token_weights.min()),
            "token_weight_max": float(token_weights.max()),
            "auxiliary_token_scorer_parameters": 0.0,
        })
    elif algorithm == 'ppo-rlhf':
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
    elif algorithm == 'grpo':
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
    elif algorithm == 'reco-grpo':
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        old = np.clip(sampling_probabilities[sampled], 1e-5, 1.0 - 1e-5)
        current = np.clip(probabilities[sampled], 1e-5, 1.0 - 1e-5)
        response_weights = 1.0 / (len(sampled) * old)
        # The paper clips response weights in implementation.  Normalizing
        # keeps the local candidate-policy learning-rate comparable to GRPO.
        response_weights = np.minimum(response_weights, 5.0)
        response_weights /= max(response_weights.mean(), 1e-12)
        variance_ratios = (
            current * (1.0 - current)
            / (old * (1.0 - old) + 1e-12)
        )
        clipped_ratios = np.clip(variance_ratios, 0.8, 1.2)
        surrogate = response_weights * np.minimum(
            variance_ratios * advantages,
            clipped_ratios * advantages,
        )
        active = np.isclose(
            surrogate,
            response_weights * variance_ratios * advantages,
        )
        expected_features = probabilities @ group.features
        gradient = np.zeros_like(state.weights)
        for index, advantage, ratio, weight, is_active in zip(
            sampled, advantages, variance_ratios, response_weights, active
        ):
            if is_active:
                gradient += float(advantage * ratio * weight) * (
                    group.features[index] - expected_features
                )
        gradient /= len(sampled)
        gradient -= 0.02 * (group.features.T @ (probabilities - reference))
        state.reco_updates += 1
        loss = float(-surrogate.mean())
        diagnostics.update(
            {
                "group_reward_mean": float(scalar.mean()),
                "group_reward_std": float(scalar.std()),
                "response_weight_mean": float(response_weights.mean()),
                "response_weight_max": float(response_weights.max()),
                "variance_ratio_mean": float(variance_ratios.mean()),
                "non_saturated_fraction": float(
                    np.mean(current * (1.0 - current) >= 0.05)
                ),
                "clip_fraction": float(np.mean(~active)),
                "value_model_parameters": 0.0,
            }
        )
    elif algorithm == 'dapo':
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
    elif algorithm == 'gspo':
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
    elif algorithm == 'ripo':
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        old = np.clip(sampling_probabilities[sampled], 1e-6, 1.0)
        ratios = probabilities[sampled] / old
        radius = np.clip(0.10 + 0.35 * np.sqrt(old), 0.10, 0.45)
        clipped = np.clip(ratios, 1.0 - radius, 1.0 + radius)
        surrogate = np.minimum(ratios * advantages, clipped * advantages)
        active = np.isclose(surrogate, ratios * advantages)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, advantages * ratios * active
        )
        loss = float(-surrogate.mean())
        diagnostics.update({
            "fisher_rao_radius_mean": float(radius.mean()),
            "probability_dependent_clip": 1.0,
            "clip_fraction": float(np.mean(~active)),
            "value_model_parameters": 0.0,
        })
    elif algorithm in {'tis', 'icepop', 'online-icepop'}:
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        rollout_training = rollout_training_probabilities
        rollout_engine = sampling_probabilities
        if algorithm == "tis":
            correction = truncated_importance_weights(
                rollout_training, rollout_engine
            )
        else:
            correction = icepop_weights(rollout_training, rollout_engine)
        correction_weights = correction.weights[sampled]
        if algorithm == "online-icepop":
            policy_ratios = np.ones_like(advantages)
            active = np.ones_like(advantages, dtype=bool)
        else:
            policy_ratios = probabilities[sampled] / (
                rollout_training[sampled] + 1e-12
            )
            clipped = np.clip(policy_ratios, 0.8, 1.2)
            surrogate = np.minimum(
                policy_ratios * advantages, clipped * advantages
            )
            active = np.isclose(
                surrogate, policy_ratios * advantages
            )
        weights = (
            advantages * policy_ratios * active * correction_weights
        )
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, weights
        )
        loss = float(
            -np.mean(
                advantages
                * policy_ratios
                * active
                * correction_weights
                * np.log(probabilities[sampled] + 1e-12)
            )
        )
        diagnostics.update({
            "training_inference_ratio_mean": float(
                correction.ratios[sampled].mean()
            ),
            "training_inference_ratio_max": float(
                correction.ratios[sampled].max()
            ),
            "correction_weight_mean": float(correction_weights.mean()),
            "correction_adjusted_fraction": float(
                correction.adjusted[sampled].mean()
            ),
            "policy_staleness_ratio_mean": float(policy_ratios.mean()),
            "ppo_clip_active": float(algorithm != "online-icepop"),
        })
        if algorithm == "tis":
            diagnostics.update({
                "tis_upper_bound": 2.0,
                "tis_clipped_fraction": float(
                    correction.adjusted[sampled].mean()
                ),
                "mismatch_tokens_dropped": 0.0,
            })
        else:
            diagnostics.update({
                "icepop_lower_bound": 0.5,
                "icepop_upper_bound": 5.0,
                "icepop_kept_fraction": float(
                    correction.kept[sampled].mean()
                ),
                "mismatch_tokens_dropped": float(
                    correction.adjusted[sampled].sum()
                ),
            })
        if algorithm == "online-icepop":
            diagnostics.update({
                "updates_per_rollout_batch": 1.0,
                "forced_on_policy_ratio": 1.0,
            })
    elif algorithm == 'kpop':
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        old = np.clip(sampling_probabilities[sampled], 1e-6, 1.0 - 1e-6)
        current = np.clip(probabilities[sampled], 1e-6, 1.0 - 1e-6)
        forward = current * np.log(current / old) + (1 - current) * np.log(
            (1 - current) / (1 - old)
        )
        reverse = old * np.log(old / current) + (1 - old) * np.log(
            (1 - old) / (1 - current)
        )
        keep = (forward <= 0.03) & (reverse <= 0.03)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, advantages * keep
        )
        loss = float(-np.mean(advantages * np.log(current)) )
        diagnostics.update({
            "binary_kl_forward_mean": float(forward.mean()),
            "binary_kl_reverse_mean": float(reverse.mean()),
            "adaptive_mask_kept_fraction": float(keep.mean()),
            "fixed_ratio_clip": 0.0,
        })
    elif algorithm == 'gppo':
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        ratios = probabilities[sampled] / (sampling_probabilities[sampled] + 1e-12)
        clipped = np.clip(ratios, 0.8, 1.2)
        surrogate = np.minimum(ratios * advantages, clipped * advantages)
        active = np.isclose(surrogate, ratios * advantages)
        boundary_weight = np.where(active, ratios, clipped)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, advantages * boundary_weight
        )
        loss = float(-surrogate.mean())
        diagnostics.update({
            "ppo_forward_surrogate": 1.0,
            "preserved_boundary_gradients": float(np.sum(~active)),
            "clip_fraction": float(np.mean(~active)),
            "value_model_parameters": 0.0,
        })
    else:
        return None
    return gradient, loss, diagnostics
