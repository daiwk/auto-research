from __future__ import annotations

import numpy as np

from ..algorithm_core import (PolicyState, _one_hot, _reinforce_gradient, _scalar_rewards, _softmax, _weighted_policy_gradient)
from ..data import CandidateGroup
from ..rollout_correction import (icepop_weights, rollout_engine_probabilities, truncated_importance_weights)

def apply(algorithm, state, group, learning_rate, rng, group_size, cache_index, probabilities, reference, rollout_training_probabilities, sampling_probabilities, sampled, diagnostics):
    if algorithm == 'dpo':
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
    elif algorithm == 'kto':
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
    elif algorithm == 'orpo':
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
    elif algorithm == 'gkd':
        teacher = state.teacher_cache[cache_index]
        support = np.zeros_like(teacher)
        support[sampled] = 1.0
        on_policy_target = teacher * support
        on_policy_target /= max(on_policy_target.sum(), 1e-12)
        off_policy_target = np.zeros_like(teacher)
        off_policy_target[group.gold] = 1.0
        on_policy_fraction = 0.75
        target = (
            on_policy_fraction * on_policy_target
            + (1.0 - on_policy_fraction) * off_policy_target
        )
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.online_teacher_calls += len(sampled)
        diagnostics.update(
            {
                "student_generated_rollouts": float(len(sampled)),
                "on_policy_fraction": on_policy_fraction,
                "teacher_forward_passes": float(len(sampled)),
                "student_support_fraction": float(support.mean()),
                "divergence_jsd_beta": 0.0,
            }
        )
    elif algorithm == 'minillm':
        teacher = state.teacher_cache[cache_index]
        teacher_mix = 0.2
        mixed_sampling = (
            (1.0 - teacher_mix) * probabilities + teacher_mix * teacher
        )
        rollout = rng.choice(
            len(probabilities),
            size=min(group_size, len(probabilities)),
            replace=False,
            p=mixed_sampling,
        )
        log_ratio = np.log(probabilities[rollout] + 1e-12) - np.log(
            teacher[rollout] + 1e-12
        )
        baseline = float(log_ratio.mean())
        reverse_kl_advantage = -(log_ratio - baseline)
        gradient = _reinforce_gradient(
            group.features, probabilities, rollout, reverse_kl_advantage
        )
        loss = float(np.mean(log_ratio))
        state.online_teacher_calls += len(rollout)
        diagnostics.update(
            {
                "reverse_kl": float(
                    np.sum(
                        probabilities
                        * np.log((probabilities + 1e-12) / (teacher + 1e-12))
                    )
                ),
                "teacher_mixed_sampling": teacher_mix,
                "student_generated_rollouts": float(len(rollout)),
                "variance_reduction_baseline": baseline,
                "length_normalized_objective": 1.0,
            }
        )
    elif algorithm == 'opsd':
        privileged = 0.35 * probabilities.copy()
        privileged[group.gold] += 0.65
        mixture = 0.5 * (privileged + probabilities)
        teacher_pointwise = privileged * np.log(
            (privileged + 1e-12) / (mixture + 1e-12)
        )
        student_pointwise = probabilities * np.log(
            (probabilities + 1e-12) / (mixture + 1e-12)
        )
        clip_threshold = 0.12
        clipped = np.minimum(
            0.5 * teacher_pointwise + 0.5 * student_pointwise,
            clip_threshold,
        )
        clipping_rate = float(np.mean(
            (0.5 * teacher_pointwise + 0.5 * student_pointwise)
            > clip_threshold
        ))
        gradient = group.features.T @ (privileged - probabilities)
        loss = float(np.sum(clipped))
        state.online_teacher_calls += len(sampled)
        diagnostics.update(
            {
                "student_generated_rollouts": float(len(sampled)),
                "shared_teacher_student_parameters": 1.0,
                "privileged_solution_conditioning": 1.0,
                "dense_token_teacher_calls": float(len(sampled)),
                "pointwise_divergence_clip": clip_threshold,
                "pointwise_clip_rate": clipping_rate,
                "jsd_beta": 0.5,
            }
        )
    elif algorithm == 'dash':
        privileged = 0.25 * probabilities.copy()
        privileged[group.gold] += 0.75
        local_divergence = privileged * np.log(
            (privileged + 1e-12) / (probabilities + 1e-12)
        )
        clip_threshold = 0.08
        clipped = np.minimum(local_divergence, clip_threshold)
        centered = clipped - clipped.mean()
        kappa = 18.0
        gates = 1.0 / (1.0 + np.exp(kappa * centered[:-1]))
        coefficients = np.ones_like(clipped)
        for index in range(len(coefficients) - 2, -1, -1):
            coefficients[index] += gates[index] * coefficients[index + 1]
        target = privileged * coefficients
        target /= max(target.sum(), 1e-12)
        gradient = group.features.T @ (target - probabilities)
        loss = float(np.sum(coefficients * clipped) / len(clipped))
        state.online_teacher_calls += len(sampled)
        diagnostics.update(
            {
                "student_generated_rollouts": float(len(sampled)),
                "shared_teacher_student_parameters": 1.0,
                "privileged_solution_conditioning": 1.0,
                "dense_token_teacher_calls": float(len(sampled)),
                "local_divergence_clip": clip_threshold,
                "local_clip_rate": float(np.mean(local_divergence > clip_threshold)),
                "adaptive_gate_mean": float(gates.mean()) if len(gates) else 0.0,
                "backward_horizon_mean": float(coefficients.mean()),
                "extra_teacher_forward_passes": 0.0,
            }
        )
    elif algorithm == 'beta-opsd':
        privileged = 0.25 * probabilities.copy()
        privileged[group.gold] += 0.75
        beta = 0.35
        target_logits = (
            beta * np.log(reference + 1e-12)
            + np.log(privileged + 1e-12)
        ) / (1.0 + beta)
        target = _softmax(target_logits)
        returns = np.linspace(0.35, 1.0, len(target), dtype=np.float64)
        target = target * returns
        target /= target.sum()
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.online_teacher_calls += len(sampled)
        diagnostics.update({
            "beta_reference_anchor": beta,
            "closed_form_geometric_target": 1.0,
            "return_to_go_min": float(returns.min()),
            "return_to_go_max": float(returns.max()),
            "privileged_teacher_calls": float(len(sampled)),
        })
    elif algorithm == 'distilled-rl':
        teacher = state.teacher_cache[cache_index]
        ratio = probabilities / np.maximum(teacher, 1e-12)
        clipped_ratio = np.clip(ratio, 0.5, 2.0)
        rewards = group.rewards[:, 0]
        reset = rewards <= np.median(rewards)
        distilled = np.where(reset, teacher, teacher * clipped_ratio)
        distilled /= max(distilled.sum(), 1e-12)
        geometric = float(np.exp(np.mean(np.log(clipped_ratio + 1e-12))))
        target = 0.35 * _one_hot(len(probabilities), group.gold) + 0.65 * distilled
        gradient = geometric * (group.features.T @ (target - probabilities))
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "reverse_ratio_clip_rate": float(np.mean(ratio != clipped_ratio)),
            "negative_sample_resets": float(reset.sum()),
            "sequence_geometric_normalizer": geometric,
            "unconditional_teacher_matching": 0.0,
        })
    elif algorithm == 'u-opsd':
        draws = rng.choice(
            len(probabilities), size=max(5, group_size * 2),
            replace=True, p=probabilities,
        )
        counts = np.bincount(draws, minlength=len(probabilities))
        pseudo = int(np.argmax(counts))
        confidence = float(counts[pseudo] / len(draws))
        target = probabilities.copy()
        if confidence >= 0.25:
            target *= 0.35
            target[pseudo] += 0.65
        target /= target.sum()
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "self_consistency_votes": float(len(draws)),
            "pseudo_solution_confidence": confidence,
            "external_supervision": 0.0,
            "repair_target_is_gold": float(pseudo == group.gold),
        })
    elif algorithm == 'rp-opsd':
        teacher = state.teacher_cache[cache_index]
        reference_view = 0.55 * teacher + 0.45 * _one_hot(len(teacher), group.gold)
        ablated_view = 0.75 * probabilities + 0.25 * teacher
        pivot = np.abs(np.log(reference_view + 1e-12) - np.log(ablated_view + 1e-12))
        pivot /= max(pivot.max(), 1e-12)
        target = probabilities + pivot * (reference_view - probabilities)
        target = np.maximum(target, 1e-12)
        target /= target.sum()
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "reasoning_pivot_mass": float(pivot.mean()),
            "privileged_positions": float(np.sum(pivot >= np.median(pivot))),
            "reference_anchor": 0.45,
        })
    elif algorithm == 'pcsd':
        teacher = state.teacher_cache[cache_index]
        support = np.log(teacher + 1e-12) - np.log(probabilities + 1e-12)
        persistent = np.zeros_like(support)
        running = 0.0
        for index, value in enumerate(support):
            running = 0.72 * running + 0.28 * value
            trend = value - (support[index - 1] if index else value)
            persistent[index] = running * (1.0 if trend >= 0 else 0.5)
        gate = 1.0 / (1.0 + np.exp(-persistent))
        target = probabilities + gate * (teacher - probabilities)
        target = np.maximum(target, 1e-12)
        target /= target.sum()
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "persistent_gate_mean": float(gate.mean()),
            "adaptive_window": float(min(4, len(gate))),
            "trend_attenuated_positions": float(np.sum(np.diff(support) < 0)),
        })
    elif algorithm == 'adrs':
        teacher = state.teacher_cache[cache_index]
        privileged = (teacher - teacher.mean()) / max(teacher.std(), 1e-6)
        returns = group.rewards[:, 0]
        normalized_returns = (returns - returns.mean()) / max(returns.std(), 1e-6)
        association = float(np.tanh(np.mean(privileged * normalized_returns)))
        gate = max(0.0, association)
        advantages = normalized_returns + gate * privileged
        gradient = _reinforce_gradient(group.features, probabilities, sampled, advantages[sampled])
        loss = float(-np.mean(advantages[sampled] * np.log(probabilities[sampled] + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "teacher_value_advantage_gate": gate,
            "within_step_score_mean": float(privileged.mean()),
            "return_teacher_association": association,
            "inference_time_skill": 0.0,
        })
    elif algorithm == 'mopd':
        domain_teachers = np.stack([
            _softmax(group.rewards[:, axis] * 3.0)
            for axis in range(group.rewards.shape[1])
        ])
        domain_strength = np.maximum(group.rewards.max(axis=0), 0.0) + 1e-3
        mixture_weights = domain_strength / domain_strength.sum()
        target = mixture_weights @ domain_teachers
        support = np.zeros_like(target)
        support[sampled] = 1.0
        target = target * (0.2 + 0.8 * support)
        target /= max(target.sum(), 1e-12)
        gradient = group.features.T @ (target - probabilities)
        loss = float(-np.sum(target * np.log(probabilities + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "domain_teachers": float(len(domain_teachers)),
            "student_rollout_support": float(support.mean()),
            "teacher_merge_parameters": 0.0,
            "largest_domain_weight": float(mixture_weights.max()),
        })
    elif algorithm == 'opd-lm':
        teacher = state.teacher_cache[cache_index]
        bidirectional = (
            teacher + np.roll(teacher, 1) + np.roll(teacher, -1)
        ) / 3.0
        denoised = 0.7 * bidirectional + 0.3 * _one_hot(len(teacher), group.gold)
        denoised /= denoised.sum()
        gradient = group.features.T @ (denoised - probabilities)
        loss = float(-np.sum(denoised * np.log(probabilities + 1e-12)))
        state.variant_updates += 1
        diagnostics.update({
            "bidirectional_teacher": 1.0,
            "autoregressive_anchor": 0.7,
            "diffusion_denoising_views": 2.0,
            "teacher_trainable": 0.0,
        })
    elif algorithm == 'opcd':
        cached_teacher = state.teacher_cache[cache_index]
        experience = np.zeros_like(probabilities)
        experience[group.gold] = 1.0
        context_teacher = 0.7 * cached_teacher + 0.3 * experience
        rollout = rng.choice(
            len(probabilities),
            size=min(group_size, len(probabilities)),
            replace=False,
            p=probabilities,
        )
        log_ratio = np.log(probabilities[rollout] + 1e-12) - np.log(
            context_teacher[rollout] + 1e-12
        )
        baseline = float(log_ratio.mean())
        gradient = _reinforce_gradient(
            group.features, probabilities, rollout, -(log_ratio - baseline)
        )
        loss = float(np.sum(
            probabilities
            * np.log((probabilities + 1e-12) / (context_teacher + 1e-12))
        ))
        state.online_teacher_calls += len(rollout)
        diagnostics.update(
            {
                "student_generated_rollouts": float(len(rollout)),
                "context_conditioned_teacher_calls": float(len(rollout)),
                "context_free_student_view": 1.0,
                "experience_context_fraction": 0.3,
                "reverse_kl": loss,
                "experience_internalization_updates": 1.0,
            }
        )
    else:
        return None
    return gradient, loss, diagnostics
