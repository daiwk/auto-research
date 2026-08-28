"""Post-training objectives selected from the 2026-08-27 announcement."""

from __future__ import annotations

import numpy as np


ALGORITHMS = {"ttpo", "weak-guide-rlvr", "uc-mopd", "spear"}


def update_latest(algorithm, state, group, probabilities, reference,
                  rollout_training_probabilities, sampled, rng):
    del state
    features = group.features
    rewards = group.rewards[sampled]
    sampled_probabilities = probabilities[sampled]
    expected = probabilities @ features

    if algorithm == "ttpo":
        pseudo = int(np.argmax(group.rewards[:, 0] + group.rewards[:, 3]))
        agrees = sampled == pseudo
        confidence = np.max(probabilities) - np.partition(probabilities, -2)[-2]
        distill = np.log((reference[sampled] + 1e-12) / (sampled_probabilities + 1e-12))
        grouped_rl = rewards[:, 0] - rewards[:, 0].mean()
        advantages = np.where(agrees, distill, grouped_rl * (0.5 + confidence))
        diagnostics = {
            "pseudo_label_agreement": float(agrees.mean()),
            "asymmetric_distillation_fraction": float(agrees.mean()),
            "confident_error_penalty": float((~agrees).mean() * confidence),
        }
    elif algorithm == "weak-guide-rlvr":
        weak_logits = np.log(reference + 1e-12) + 0.35 * group.rewards[:, 2]
        weak = np.exp(weak_logits - weak_logits.max())
        weak /= weak.sum()
        guided = 0.75 * probabilities + 0.25 * weak
        prefix_surprise = -np.log(guided[sampled] + 1e-12)
        advantages = rewards[:, 0] - rewards[:, 0].mean() + 0.12 * (
            prefix_surprise - prefix_surprise.mean()
        )
        diagnostics = {
            "weak_prefix_fraction": 0.25,
            "prefix_surprise_mean": float(prefix_surprise.mean()),
            "guided_entropy": float(-np.sum(guided * np.log(guided + 1e-12))),
        }
    elif algorithm == "uc-mopd":
        temperature = 1.35
        hot = np.power(probabilities, 1.0 / temperature)
        hot /= hot.sum()
        teacher_advantage = np.log(reference[sampled] + 1e-12) - np.log(
            sampled_probabilities + 1e-12
        )
        positive_density = float((teacher_advantage > 0).mean())
        centered_ll = np.log(reference[sampled] + 1e-12) - np.mean(np.log(reference + 1e-12))
        endorsement = 1.0 / (1.0 + np.exp(-centered_ll))
        keep = rng.random(len(sampled)) < endorsement
        advantages = np.where(keep, np.maximum(teacher_advantage, 0.0), 0.0)
        advantages -= advantages.mean()
        diagnostics = {
            "dual_temperature": temperature,
            "positive_advantage_density": positive_density,
            "cll_retention_rate": float(keep.mean()),
            "hot_sampling_entropy": float(-np.sum(hot * np.log(hot + 1e-12))),
        }
    elif algorithm == "spear":
        # Candidate process/format axes stand in for ordered symbolic milestones.
        milestones = group.rewards[:, [2, 3]]
        teacher_order = np.argsort(-(milestones @ np.asarray([0.7, 0.3])))
        ranks = np.empty(len(teacher_order), dtype=float)
        ranks[teacher_order] = np.arange(len(teacher_order))
        lcs_proxy = 1.0 - ranks[sampled] / max(1, len(teacher_order) - 1)
        advantages = lcs_proxy - lcs_proxy.mean()
        diagnostics = {
            "symbolic_milestone_count": float(milestones.shape[1]),
            "lcs_alignment_reward": float(lcs_proxy.mean()),
            "neural_prm_calls": 0.0,
        }
    else:  # pragma: no cover
        raise ValueError(f"unsupported 20260829 algorithm: {algorithm}")

    gradient = np.stack([
        float(advantage) * (features[index] - expected)
        for index, advantage in zip(sampled, advantages)
    ]).mean(0)
    loss = float(-np.mean(advantages * np.log(sampled_probabilities + 1e-12)))
    return gradient, loss, diagnostics
