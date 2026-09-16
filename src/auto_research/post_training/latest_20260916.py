"""Executable reference kernels for the 2026-09-12--15 post-training batch.

The shared candidate-policy runner is intentionally an L1 mechanism suite: it
executes each paper's defining weighting/target transition without pretending
to be a full language-model training run.
"""

from __future__ import annotations

import numpy as np

from .algorithm_core import _softmax


def discounted_credit(token_advantages, gamma: float = 0.92):
    """Gamma-OPD discounted future credit, computed backwards in time."""
    values = np.asarray(token_advantages, dtype=np.float64)
    output = np.zeros_like(values)
    running = 0.0
    for index in range(len(values) - 1, -1, -1):
        running = float(values[index]) + gamma * running
        output[index] = running
    return output


def reward_bounded_mix(opd_advantage, reward_advantage, bound: float = 1.0):
    """RBM: add outcome feedback without allowing it to dominate OPD credit."""
    opd = np.asarray(opd_advantage, dtype=np.float64)
    reward = np.asarray(reward_advantage, dtype=np.float64)
    return opd + np.clip(reward, -bound, bound) * np.minimum(1.0, np.abs(opd) + 0.1)


def turn_multiscale_weights(scores, turns: int = 3):
    """tlm-DRE turn weights and asymmetric positive/negative density ratios."""
    scores = np.asarray(scores, dtype=np.float64)
    groups = np.array_split(np.arange(len(scores)), min(turns, len(scores)))
    weights = np.zeros_like(scores)
    turn_means = np.asarray([scores[group].mean() for group in groups])
    turn_probs = _softmax(turn_means)
    for turn, group in enumerate(groups):
        local = scores[group]
        centered = local - np.median(local)
        density_ratio = np.exp(np.clip(centered, -4.0, 4.0))
        # Negative space is deliberately amplified, matching the paper's
        # asymmetric token treatment instead of a symmetric per-turn average.
        asymmetric = np.where(centered >= 0, density_ratio, 1.5 / density_ratio)
        weights[group] = turn_probs[turn] * asymmetric / (asymmetric.sum() + 1e-12)
    return weights, turn_probs


def stride_prefix(log_teacher, threshold: float = -4.0):
    """STRIDE adaptive stop and weakest-correct-turn restart index."""
    values = np.asarray(log_teacher, dtype=np.float64)
    cumulative = np.cumsum(values)
    failed = np.flatnonzero(cumulative < threshold)
    stop = int(failed[0] + 1) if len(failed) else len(values)
    prefix = values[:stop]
    restart = int(np.argmin(prefix)) if len(prefix) else 0
    return stop, restart


def data_free_questions(reference, rng, count: int = 8):
    """DF-OPD teacher-side self-generation proxy in policy feature space."""
    reference = np.asarray(reference, dtype=np.float64)
    axes = rng.normal(size=(count, len(reference)))
    axes /= np.linalg.norm(axes, axis=1, keepdims=True) + 1e-12
    difficulty = np.linspace(0.25, 1.0, count)[:, None]
    return reference + difficulty * axes


def visual_preference_target(real_logits, null_logits, floor: float = 1e-6):
    """OPD-Aha target reconstruction from teacher(real)-teacher(null)."""
    real = _softmax(np.asarray(real_logits, dtype=np.float64))
    null = _softmax(np.asarray(null_logits, dtype=np.float64))
    corrective = np.maximum(real - null, 0.0)
    target = corrective + floor * real
    return target / target.sum()


def depth_coupled_acceptance(draft_probabilities, accepted_depth: int):
    """GrowMTP learns only the accepted draft path up to first rejection."""
    probs = np.clip(np.asarray(draft_probabilities, dtype=np.float64), 1e-9, 1.0)
    depth = max(1, min(int(accepted_depth), len(probs)))
    weights = np.arange(depth, 0, -1, dtype=np.float64)
    loss = -float(np.sum(weights * np.log(probs[:depth])) / weights.sum())
    mask = np.zeros_like(probs)
    mask[:depth] = weights / weights.sum()
    return loss, mask


def update_latest(
    algorithm, state, group, probabilities, reference,
    rollout_training_probabilities, sampled, rng,
):
    expected = probabilities @ group.features
    teacher_log_ratio = np.log(reference[sampled] + 1e-12) - np.log(
        probabilities[sampled] + 1e-12
    )
    rewards = group.rewards[sampled] @ np.asarray((0.7, 0.05, 0.2, 0.05))
    diagnostics = {}

    if algorithm == "gamma-opd":
        credit = discounted_credit(teacher_log_ratio)
        reward_adv = rewards - rewards.mean()
        advantages = reward_bounded_mix(credit, reward_adv)
        diagnostics.update(discounted_credit_span=float(credit.max() - credit.min()), rbm_bound=1.0)
    elif algorithm == "tlm-dre":
        weights, turn_probs = turn_multiscale_weights(teacher_log_ratio)
        advantages = weights - weights.mean()
        diagnostics.update(turn_weight_entropy=float(-(turn_probs * np.log(turn_probs + 1e-12)).sum()), asymmetric_token_weights=float(np.std(weights)))
    elif algorithm == "stride-opd":
        stop, restart = stride_prefix(np.log(reference[sampled] + 1e-12))
        selected = np.arange(len(sampled)) < stop
        advantages = np.where(selected, teacher_log_ratio, 0.0)
        advantages -= advantages.mean()
        diagnostics.update(adaptive_stop=float(stop), prefix_restart=float(restart), saved_rollout_fraction=float(1 - stop / len(sampled)))
    elif algorithm == "df-opd":
        synthetic = data_free_questions(state.reference, rng)
        synthetic_scores = synthetic @ state.reference
        advantages = teacher_log_ratio + 0.1 * (synthetic_scores[: len(sampled)] - synthetic_scores[: len(sampled)].mean())
        diagnostics.update(self_generated_questions=float(len(synthetic)), external_questions=0.0)
    elif algorithm == "opd-aha":
        target = visual_preference_target(np.log(reference + 1e-12), np.log(rollout_training_probabilities + 1e-12))
        advantages = target[sampled] - probabilities[sampled]
        diagnostics.update(visual_preference_mass=float(np.maximum(reference - rollout_training_probabilities, 0).sum()), reconstructed_target_entropy=float(-(target * np.log(target + 1e-12)).sum()))
    elif algorithm == "growmtp":
        accepted = max(1, int(np.sum(reference[sampled] >= probabilities[sampled])))
        draft_loss, mask = depth_coupled_acceptance(reference[sampled], accepted)
        advantages = mask - mask.mean()
        diagnostics.update(draft_acceptance_depth=float(accepted), depth_coupled_loss=draft_loss, detached_backbone=1.0)
    else:  # pragma: no cover - dispatch contract prevents this branch
        raise ValueError(algorithm)

    gradient = np.zeros_like(state.weights)
    for index, advantage in zip(sampled, advantages):
        gradient += float(advantage) * (group.features[index] - expected)
    gradient /= max(1, len(sampled))
    loss = float(-np.mean(advantages * np.log(probabilities[sampled] + 1e-12)))
    return gradient, loss, diagnostics
