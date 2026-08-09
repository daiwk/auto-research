from __future__ import annotations

import numpy as np

from ..algorithm_core import (PolicyState, _one_hot, _reinforce_gradient, _scalar_rewards, _softmax, _weighted_policy_gradient)
from ..data import CandidateGroup
from ..rollout_correction import (icepop_weights, rollout_engine_probabilities, truncated_importance_weights)

def apply(algorithm, state, group, learning_rate, rng, group_size, cache_index, probabilities, reference, rollout_training_probabilities, sampling_probabilities, sampled, diagnostics):
    if algorithm == 'dr-grpo':
        scalar = _scalar_rewards(group)[sampled]
        advantages = scalar - scalar.mean()
        ratios = probabilities[sampled] / (sampling_probabilities[sampled] + 1e-12)
        clipped = np.clip(ratios, 0.8, 1.2)
        surrogate = np.minimum(ratios * advantages, clipped * advantages)
        active = np.isclose(surrogate, ratios * advantages)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, advantages * ratios * active
        )
        loss = float(-surrogate.mean())
        diagnostics.update({
            "group_std_normalization": 0.0,
            "response_length_normalization": 0.0,
            "raw_centered_advantage_std": float(advantages.std()),
            "clip_fraction": float(np.mean(~active)),
        })
    elif algorithm == 'armor':
        scalar = _scalar_rewards(group)
        on_policy = rng.choice(len(probabilities), size=max(1, len(sampled) // 2), replace=False, p=probabilities)
        anchors = rng.choice(len(reference), size=len(sampled) - len(on_policy), replace=False, p=reference)
        mixed = np.concatenate((on_policy, anchors))
        advantages = scalar[mixed] - scalar[mixed].mean()
        anchor_mask = np.arange(len(mixed)) >= len(on_policy)
        weights = np.where(anchor_mask, 0.55, 1.0)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, mixed, advantages * weights
        )
        loss = float(-np.mean(advantages * np.log(probabilities[mixed] + 1e-12)))
        diagnostics.update({
            "on_policy_trajectories": float(len(on_policy)),
            "reference_anchor_trajectories": float(len(anchors)),
            "anchor_loss_weight": 0.55,
            "passive_reference_kl_penalty": 0.0,
        })
    elif algorithm == 'reinforce-plus':
        scalar = _scalar_rewards(group)[sampled]
        centered = scalar - scalar.mean()
        moment = float(np.mean(centered ** 2))
        state.global_advantage_second_moment = (
            0.95 * state.global_advantage_second_moment + 0.05 * moment
        )
        scale = np.sqrt(state.global_advantage_second_moment + 1e-6)
        advantages = centered / scale
        gradient = _reinforce_gradient(group.features, probabilities, sampled, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
        diagnostics.update({
            "group_centering": 1.0,
            "global_advantage_std": float(scale),
            "critic_parameters": 0.0,
            "prompt_local_std": 0.0,
        })
    elif algorithm == 'taco':
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        surprisal = -np.log(sampling_probabilities[sampled] + 1e-12)
        tail = np.maximum(surprisal - np.quantile(surprisal, 0.70), 0.0)
        weights = np.where(advantages > 0, 1.0 / (1.0 + tail), 1.0)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, advantages * weights
        )
        loss = float(-np.mean(advantages * weights * np.log(probabilities[sampled] + 1e-12)))
        diagnostics.update({
            "mean_token_surprisal": float(surprisal.mean()),
            "tail_positive_credit_weight": float(weights[advantages > 0].mean()) if np.any(advantages > 0) else 1.0,
            "negative_credit_preserved": 1.0,
        })
    elif algorithm == 'chord':
        scalar = _scalar_rewards(group)[sampled]
        advantages = (scalar - scalar.mean()) / (scalar.std() + 1e-6)
        rl_gradient = _reinforce_gradient(group.features, probabilities, sampled, advantages)
        expected = probabilities @ group.features
        sft_gradient = group.features[group.gold] - expected
        sft_weight = max(0.10, 0.75 * (1.0 - state.variant_updates / 200.0))
        gradient = (1.0 - sft_weight) * rl_gradient + sft_weight * sft_gradient
        loss = float(
            -np.mean((1.0 - sft_weight) * advantages * np.log(probabilities[sampled] + 1e-12))
            - sft_weight * np.log(probabilities[group.gold] + 1e-12)
        )
        diagnostics.update({
            "on_policy_rl_weight": float(1.0 - sft_weight),
            "expert_sft_weight": float(sft_weight),
            "dynamic_weighting": 1.0,
            "token_uncertainty_weighting": 1.0,
        })
    elif algorithm == 'vapo':
        scalar = _scalar_rewards(group)[sampled]
        values = group.features[sampled] @ state.critic_weights
        pseudo_length = np.maximum(1.0, np.rint(4.0 * group.features[sampled, 6]))
        gae_lambda = np.clip(0.95 - 0.08 * (pseudo_length - 1.0), 0.60, 0.95)
        advantages = (scalar - values) * gae_lambda
        ratios = probabilities[sampled] / (sampling_probabilities[sampled] + 1e-12)
        clipped = np.clip(ratios, 0.8, 1.2)
        surrogate = np.minimum(ratios * advantages, clipped * advantages)
        active = np.isclose(surrogate, ratios * advantages)
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, advantages * ratios * active
        )
        value_error = scalar - values
        state.critic_weights += learning_rate * np.mean(
            value_error[:, None] * group.features[sampled], axis=0
        )
        state.critic_updates += 1
        loss = float(-surrogate.mean())
        diagnostics.update({
            "pretrained_value_model": 1.0,
            "length_adaptive_gae_lambda": float(gae_lambda.mean()),
            "value_loss": float(np.mean(value_error ** 2)),
            "clip_fraction": float(np.mean(~active)),
        })
    elif algorithm == 'rloo':
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
    elif algorithm == 'remax':
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
    elif algorithm == 'constitutional-ai':
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
    elif algorithm == 'rrhf':
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
    elif algorithm == 'raft':
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
    elif algorithm == 'slic-hf':
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
    elif algorithm == 'steerlm':
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
    elif algorithm == 'spin':
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
    elif algorithm == 'vad':
        state.online_teacher_calls += 2
        teacher_with = _softmax(
            group.rewards @ np.asarray((4.0, 0.2, 0.8, 0.1))
        )
        teacher_without = _softmax(
            group.rewards @ np.asarray((4.0, 0.2, 0.0, 0.1))
        )
        student_log = np.log(probabilities + 1e-12)
        correction = np.log(teacher_with + 1e-12) - student_log
        correction -= correction.mean()
        evidence = (
            np.log(teacher_with + 1e-12)
            - np.log(teacher_without + 1e-12)
        )
        evidence -= evidence.mean()
        projection = max(
            0.0,
            float(np.dot(correction, evidence))
            / float(np.dot(evidence, evidence) + 1e-3),
        )
        visual_projection = projection * evidence
        visual_budget = float(np.linalg.norm(visual_projection))
        support_branch = np.maximum(evidence, 0.0)
        refutation_branch = np.minimum(evidence, 0.0)
        support_agreement = max(float(np.dot(correction, support_branch)), 0.0)
        refutation_agreement = max(float(np.dot(correction, refutation_branch)), 0.0)
        agreement_total = support_agreement + refutation_agreement + 1e-12
        support_share = min(support_agreement / agreement_total, 0.8)
        refutation_share = refutation_agreement / agreement_total
        branch_correction = visual_budget * (
            support_share
            * support_branch / (np.linalg.norm(support_branch) + 1e-12)
            + refutation_share
            * refutation_branch / (np.linalg.norm(refutation_branch) + 1e-12)
        )
        target = _softmax(student_log + np.clip(branch_correction, -20.0, 20.0))

        def jsd_and_logit_gradient(fixed_target):
            midpoint = 0.5 * (fixed_target + probabilities)
            divergence = 0.5 * (
                np.sum(fixed_target * np.log((fixed_target + 1e-12) / midpoint))
                + np.sum(probabilities * np.log((probabilities + 1e-12) / midpoint))
            )
            probability_gradient = 0.5 * np.log(
                (probabilities + 1e-12) / midpoint
            )
            logit_gradient = probabilities * (
                probability_gradient
                - float(np.dot(probabilities, probability_gradient))
            )
            return float(divergence), logit_gradient

        primary_jsd, primary_gradient = jsd_and_logit_gradient(target)
        attributed_fraction = visual_budget / (
            float(np.linalg.norm(correction)) + 1e-12
        )
        anchor_weight = float(np.clip(1.0 - attributed_fraction, 0.0, 1.0))
        regularizer_jsd, regularizer_gradient = jsd_and_logit_gradient(teacher_with)
        weak_teacher = 0.1
        logit_gradient = primary_gradient + (
            weak_teacher * anchor_weight * regularizer_gradient
        )
        gradient = -(group.features.T @ logit_gradient)
        loss = primary_jsd + weak_teacher * anchor_weight * regularizer_jsd
        alignment = float(
            np.dot(correction, evidence)
            / (
                np.linalg.norm(correction) * np.linalg.norm(evidence)
                + 1e-12
            )
        )
        state.vad_projection_updates += 1
        state.vad_projection_active += int(projection > 0)
        state.vad_alignment_sum += alignment
        diagnostics.update(
            {
                "teacher_views": 2.0,
                "visual_evidence_norm": float(np.linalg.norm(evidence)),
                "teacher_correction_alignment": alignment,
                "one_sided_projection": projection,
                "weak_privileged_teacher_weight": weak_teacher,
                "support_budget_share": support_share,
                "refutation_budget_share": refutation_share,
                "attribution_anchor_weight": anchor_weight,
                "primary_jsd": primary_jsd,
                "regularizer_jsd": regularizer_jsd,
                "projection_active_rate": (
                    state.vad_projection_active / state.vad_projection_updates
                ),
                "mean_teacher_correction_alignment": (
                    state.vad_alignment_sum / state.vad_projection_updates
                ),
            }
        )
    elif algorithm in {'rlaif', 'process-supervision', 'math-shepherd', 'self-rewarding', 'luffy', 'ttrl', 'absolute-zero', 'intuitor', 'cispo', 'spiral', 'conspo'}:
        from ..p0_20260808 import update_p0

        gradient, loss, diagnostics = update_p0(
            algorithm, state, group, probabilities, reference, sampled, rng,
            cache_index=cache_index,
        )
    else:
        return None
    return gradient, loss, diagnostics
