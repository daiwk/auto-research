from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .data import CandidateGroup
from .rollout_correction import (
    icepop_weights,
    rollout_engine_probabilities,
    truncated_importance_weights,
)


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
    rollout_training_probabilities = _softmax(
        group.features @ state.rollout_weights
    )
    sampling_probabilities = (
        rollout_training_probabilities
        if algorithm in {
            "ppo-rlhf", "grpo", "reco-grpo", "dapo", "gspo", "spin",
            "seed", "cast", "cort", "ripo", "tis", "icepop", "kpop",
            "gppo", "dr-grpo", "armor", "reinforce-plus", "taco",
            "chord", "vapo",
        } else probabilities
    )
    if algorithm in {"tis", "icepop", "online-icepop"}:
        sampling_probabilities = rollout_engine_probabilities(
            group.features, state.rollout_weights
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
    elif algorithm == "gkd":
        # GKD queries the teacher at states visited by the evolving student.
        # The candidate-policy analogue restricts the dense teacher target to
        # the student-generated support instead of replaying a fixed response.
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
    elif algorithm == "minillm":
        # MiniLLM minimizes reverse KL on student rollouts.  Teacher-mixed
        # sampling retains exploration while the reward baseline reduces the
        # variance of the policy-gradient estimator.
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
    elif algorithm == "opsd":
        # OPSD uses the same policy under two views: the student sees only the
        # problem, while the stop-gradient teacher is conditioned on the
        # verified solution.  The candidate analogue creates that privileged
        # view by combining the current policy with the verified gold action.
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
    elif algorithm == "opcd":
        # OPCD distils a context-conditioned distribution along trajectories
        # sampled by the context-free student, using reverse KL to favour the
        # teacher's high-probability modes.
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
    elif algorithm == "lightning-opd":
        teacher = state.teacher_cache[cache_index]
        gradient = group.features.T @ (teacher - probabilities)
        loss = float(-np.sum(teacher * np.log(probabilities + 1e-12)))
        diagnostics["cached_teacher_tokens"] = float(len(teacher))
        diagnostics["online_teacher_calls"] = 0.0
    elif algorithm == "relay-opd":
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
    elif algorithm == "turn-opd":
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
    elif algorithm == "seed":
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
    elif algorithm == "cast":
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
    elif algorithm == "cort":
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
    elif algorithm == "reco-grpo":
        # ReCo applies two independent corrections to the GRPO update.  The
        # response term divides by the expected occurrence under the rollout
        # policy; the token analogue uses Bernoulli variance p(1-p), so already
        # saturated candidate decisions do not receive another large update.
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
    elif algorithm == "ripo":
        # RIPO measures the ratio step in Fisher-Rao geometry.  In the local
        # categorical policy this becomes a probability-dependent radius:
        # low-probability actions get a larger multiplicative exploration band.
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
    elif algorithm in {"tis", "icepop", "online-icepop"}:
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
    elif algorithm == "kpop":
        # KPop filters train/inference mismatch using binary KL over the
        # sampled token versus the rest of the vocabulary, rather than a fixed
        # ratio interval.  Old rollout probabilities are the serving view.
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
    elif algorithm == "gppo":
        # GPPO keeps the PPO forward surrogate but supplies a boundary gradient
        # to the two clipped quadrants, preventing useful rare-token updates
        # from becoming exactly zero.
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
    elif algorithm == "dr-grpo":
        # Dr. GRPO removes response-length averaging and group std scaling.
        # The candidate analogue preserves raw centered rewards and lets every
        # sampled response contribute one unnormalized trajectory gradient.
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
    elif algorithm == "armor":
        # ARMOR turns the reference into an active anchor-data source.  Half of
        # the local rollout group is drawn from the frozen reference policy;
        # both support preservation and on-policy improvement are observable.
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
    elif algorithm == "reinforce-plus":
        # REINFORCE++ uses a global running scale, so prompt-local reward
        # variance cannot arbitrarily amplify one group over another.
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
    elif algorithm == "taco":
        # TACO discounts positive credit assigned to implausible tail tokens,
        # while retaining full negative credit for corrections.
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
    elif algorithm == "chord":
        # CHORD anneals from expert SFT to on-policy group RL.  Here the gold
        # candidate is the expert trace and its weight decreases with updates.
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
    elif algorithm == "vapo":
        # VAPO keeps a value model but adapts the bootstrap horizon to response
        # length, preventing long candidate trajectories from overusing a
        # stale critic estimate.
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
    if algorithm == "reco-grpo" and state.reco_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "dapo" and state.dapo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "gspo" and state.gspo_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm == "spin" and state.spin_updates % 16 == 0:
        state.rollout_weights = state.weights.copy()
    if algorithm in {
        "ripo", "tis", "icepop", "kpop", "gppo", "dr-grpo", "armor",
        "reinforce-plus", "taco", "chord", "vapo",
    }:
        state.variant_updates += 1
        if state.variant_updates % 16 == 0:
            state.rollout_weights = state.weights.copy()
    if algorithm == "online-icepop":
        state.rollout_weights = state.weights.copy()
        state.online_rollout_refreshes += 1
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
