"""Mechanism-specific objectives from the 2026-08 post-training P0 audit."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {
    "rlaif", "process-supervision", "math-shepherd", "self-rewarding",
    "luffy", "ttrl", "absolute-zero", "intuitor", "cispo", "spiral",
    "conspo",
}


def update_p0(algorithm, state, group, probabilities, reference, sampled, rng, cache_index=0):
    features = group.features
    expected = probabilities @ features
    diagnostics = {}

    def reinforce(indices, advantages):
        gradient = np.zeros(features.shape[1], dtype=np.float64)
        for index, advantage in zip(indices, advantages):
            gradient += float(advantage) * (features[index] - expected)
        return gradient / max(1, len(indices))

    if algorithm == "rlaif":
        # AI labeler compares both orders; averaging cancels position bias.
        ai_scores = group.rewards @ np.asarray((0.55, 0.05, 0.30, 0.10))
        forward = ai_scores + 0.08 * np.linspace(1, -1, len(ai_scores))
        reverse = ai_scores - 0.08 * np.linspace(1, -1, len(ai_scores))
        debiased = 0.5 * (forward + reverse)
        chosen, rejected = int(np.argmax(debiased)), int(np.argmin(debiased))
        margin = np.log(probabilities[chosen] + 1e-12) - np.log(probabilities[rejected] + 1e-12)
        coefficient = 1.0 / (1.0 + np.exp(margin))
        gradient = coefficient * (features[chosen] - features[rejected])
        loss = float(np.logaddexp(0.0, -margin))
        diagnostics = {"ai_preference_pairs": 2.0, "position_swap_debiased": 1.0, "preference_margin": float(margin)}
    elif algorithm == "process-supervision":
        outcome = group.rewards[:, 0]
        process = group.rewards[:, 2]
        uncertainty = 1.0 - np.abs(process - 0.5) * 2.0
        active = sampled[np.argsort(-uncertainty[sampled])]
        advantages = process[active] - process[active].mean()
        gradient = reinforce(active, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[active] + 1e-12)))
        diagnostics = {"step_labels": float(len(active)), "active_learning_priority": float(uncertainty[active].mean()), "outcome_only_gap": float((process - outcome).mean())}
    elif algorithm == "math-shepherd":
        # Monte-Carlo continuation consistency supplies automatic step labels.
        continuations = np.clip(group.rewards[:, 0, None] + rng.normal(0, 0.15, (len(probabilities), 6)), 0, 1)
        step_labels = (continuations > 0.5).mean(1)
        advantages = step_labels[sampled] - step_labels[sampled].mean()
        gradient = reinforce(sampled, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"mc_continuations": float(continuations.size), "automatic_process_labels": float(len(step_labels)), "step_label_mean": float(step_labels.mean())}
    elif algorithm == "self-rewarding":
        judge = group.rewards @ np.asarray((0.45, 0.10, 0.35, 0.10))
        judge += 0.1 * np.log(probabilities + 1e-12)
        chosen, rejected = int(np.argmax(judge)), int(np.argmin(judge))
        margin = np.log(probabilities[chosen] + 1e-12) - np.log(probabilities[rejected] + 1e-12)
        gradient = (features[chosen] - features[rejected]) / (1.0 + np.exp(margin))
        loss = float(np.logaddexp(0.0, -margin))
        diagnostics = {"self_judged_pairs": 1.0, "judge_policy_shared": 1.0, "iterative_preference_round": float(state.variant_updates // 16 + 1)}
    elif algorithm == "luffy":
        teacher = state.teacher_cache[cache_index]
        off_policy = np.argsort(-teacher)[: max(2, len(sampled) // 2)]
        support = np.unique(np.concatenate((sampled, off_policy)))
        ratio = probabilities[support] / (teacher[support] + 1e-12)
        shaped = (group.rewards[support, 0] - 0.5) * np.clip(ratio, 0.5, 2.0)
        shaped -= shaped.mean()
        gradient = reinforce(support, shaped) - 0.02 * (features.T @ (probabilities - reference))
        loss = float(-np.mean(shaped * np.log(probabilities[support] + 1e-12)))
        diagnostics = {"on_policy_rollouts": float(len(sampled)), "off_policy_guidance": float(len(off_policy)), "regularized_is_mean": float(np.mean(np.clip(ratio, 0.5, 2.0)))}
    elif algorithm == "ttrl":
        # No gold reward: consensus among test-time samples is the pseudo label.
        bins = np.argmax(group.features[sampled, : min(3, features.shape[1])], axis=1)
        majority = int(np.bincount(bins, minlength=3).argmax())
        pseudo = (bins == majority).astype(float)
        advantages = pseudo - pseudo.mean()
        gradient = reinforce(sampled, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"ground_truth_labels": 0.0, "majority_vote_size": float(len(sampled)), "consensus_rate": float(pseudo.mean())}
    elif algorithm == "absolute-zero":
        difficulty = 1.0 - group.rewards[:, 0]
        generated = sampled[np.argsort(-difficulty[sampled])]
        verifier = (group.rewards[generated, 0] > 0.5).astype(float)
        curriculum = 1.0 - np.abs(difficulty[generated] - 0.5)
        advantages = verifier * curriculum - (verifier * curriculum).mean()
        gradient = reinforce(generated, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[generated] + 1e-12)))
        diagnostics = {"human_curated_examples": 0.0, "self_generated_tasks": float(len(generated)), "verifier_calls": float(len(generated)), "curriculum_score": float(curriculum.mean())}
    elif algorithm == "intuitor":
        uniform_logp = -np.log(len(probabilities))
        self_certainty = np.log(probabilities[sampled] + 1e-12) - uniform_logp
        advantages = self_certainty - self_certainty.mean()
        gradient = reinforce(sampled, advantages)
        loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"external_reward_calls": 0.0, "self_certainty_mean": float(self_certainty.mean()), "intrinsic_kl_to_uniform": float(np.sum(probabilities * (np.log(probabilities + 1e-12) - uniform_logp)))}
    elif algorithm == "cispo":
        rollout = np.maximum(state.rollout_weights, state.reference)
        rollout_p = np.exp(features @ rollout - np.max(features @ rollout)); rollout_p /= rollout_p.sum()
        ratio = probabilities[sampled] / (rollout_p[sampled] + 1e-12)
        rewards = group.rewards[sampled, 0]
        advantages = (rewards - rewards.mean()) / (rewards.std() + 1e-6)
        clipped = np.clip(ratio, 0.8, 1.2)
        gradient = reinforce(sampled, advantages * clipped)
        loss = float(-np.mean(advantages * clipped * np.log(probabilities[sampled] + 1e-12)))
        diagnostics = {"importance_ratio_mean": float(ratio.mean()), "clipped_ratio_fraction": float(np.mean(ratio != clipped)), "token_level_is_clip": 1.0}
    elif algorithm == "spiral":
        half = max(1, len(sampled) // 2)
        role_a, role_b = sampled[:half], sampled[half:]
        if not len(role_b): role_b = role_a
        reward_a = group.rewards[role_a, 0]
        reward_b = 1.0 - group.rewards[role_b, 0]
        adv_a, adv_b = reward_a - reward_a.mean(), reward_b - reward_b.mean()
        gradient = 0.5 * (reinforce(role_a, adv_a) + reinforce(role_b, adv_b))
        loss = float(-0.5 * (np.mean(adv_a * np.log(probabilities[role_a] + 1e-12)) + np.mean(adv_b * np.log(probabilities[role_b] + 1e-12))))
        diagnostics = {"self_play_roles": 2.0, "role_conditioned_advantages": float(len(role_a) + len(role_b)), "human_reward_calls": 0.0}
    else:  # conspo
        rewards = group.rewards[sampled, 0]
        lengths = 1.0 + np.arange(len(sampled)) % 4
        sequence_scores = np.log(probabilities[sampled] + 1e-12) / lengths
        temperature = 0.2
        contrastive = np.exp(sequence_scores / temperature)
        target = np.exp((rewards - rewards.max()) / temperature); target /= target.sum()
        predicted = contrastive / contrastive.sum()
        logit_gradient = target - predicted
        gradient = reinforce(sampled, logit_gradient)
        loss = float(-np.sum(target * np.log(predicted + 1e-12)))
        diagnostics = {"length_normalized_sequence_scores": float(len(sampled)), "infonce_group_size": float(len(sampled)), "curriculum_margin": float(min(1.0, 0.1 + state.variant_updates / 100.0)), "reward_gap_std": float(rewards.std())}

    state.variant_updates += 1
    return gradient, loss, diagnostics
