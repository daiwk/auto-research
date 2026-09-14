"""Candidate-policy analogues of post-training papers announced on 2026-09-11."""

from __future__ import annotations

import numpy as np

from .algorithm_core import _weighted_policy_gradient


ALGORITHMS = {"nsd", "adaptive-opd-gate", "locus", "tasco"}


def update_latest(
    algorithm,
    state,
    group,
    probabilities,
    reference,
    rollout_training_probabilities,
    sampled,
    rng,
):
    del state
    eps = 1e-12
    features = group.features
    sampled_policy = probabilities[sampled]
    rewards = group.rewards[sampled]
    scalar = rewards @ np.asarray((0.7, 0.05, 0.2, 0.05))

    if algorithm == "nsd":
        # A negative teacher is synthesized by preferring low-reward candidates.
        negative_logits = -scalar
        negative = np.exp(negative_logits - negative_logits.max())
        negative /= negative.sum()
        divergence = np.log(sampled_policy + eps) - np.log(negative + eps)
        reasoning_signal = np.abs(rewards[:, 0] - rewards[:, 2])
        gate = reasoning_signal / (reasoning_signal.mean() + eps)
        gate = np.clip(gate, 0.0, 1.0)
        weights = gate * (divergence - divergence.mean())
        diagnostics = {
            "negative_teacher_divergence": float(np.abs(divergence).mean()),
            "reasoning_gate_mean": float(gate.mean()),
            "protected_token_fraction": float((gate < 0.25).mean()),
        }
    elif algorithm == "adaptive-opd-gate":
        teacher = rollout_training_probabilities[sampled]
        entropy = -np.log(sampled_policy + eps)
        uncertainty = np.abs(scalar - scalar.mean())
        bias = np.abs(np.log(sampled_policy + eps) - np.log(reference[sampled] + eps))
        gap = np.abs(np.log(teacher + eps) - np.log(sampled_policy + eps))
        signals = np.stack((entropy, uncertainty, bias, gap), axis=1)
        normalized = (signals - signals.mean(0)) / (signals.std(0) + 1e-6)
        gate = 1.0 / (1.0 + np.exp(-(normalized @ np.asarray((0.30, 0.20, -0.15, 0.35)))))
        weights = gate * (np.log(teacher + eps) - np.log(sampled_policy + eps))
        weights -= weights.mean()
        diagnostics = {
            "adaptive_gate_mean": float(gate.mean()),
            "adaptive_gate_std": float(gate.std()),
            "teacher_student_gap": float(gap.mean()),
            "gate_signals": 4.0,
        }
    elif algorithm == "locus":
        centered = features[sampled] - features[sampled].mean(0)
        _, singular, vh = np.linalg.svd(centered, full_matrices=False)
        rank = max(1, min(2, len(singular)))
        basis = vh[:rank].T
        advantages = scalar - scalar.mean()
        full_gradient = np.mean(advantages[:, None] * centered, axis=0)
        gradient = basis @ (basis.T @ full_gradient)
        retained = np.linalg.norm(gradient) / (np.linalg.norm(full_gradient) + eps)
        loss = float(-np.mean(advantages * np.log(sampled_policy + eps)))
        return gradient, loss, {
            "subspace_rank": float(rank),
            "ambient_dimensions": float(features.shape[1]),
            "gradient_energy_retained": float(retained),
        }
    else:  # tasco
        perturbations = rng.normal(0.0, 0.03, size=(4, len(sampled_policy)))
        local = np.stack([
            np.exp(np.log(sampled_policy + eps) + delta)
            for delta in perturbations
        ])
        local /= local.sum(1, keepdims=True)
        variance = local.var(0)
        confidence = 1.0 - sampled_policy
        weights = (confidence - confidence.mean()) - 2.0 * (variance - variance.mean())
        diagnostics = {
            "local_stability_variance": float(variance.mean()),
            "perturbation_samples": float(len(local)),
            "stability_penalty": float(np.abs(variance - variance.mean()).mean()),
        }

    gradient = _weighted_policy_gradient(features, probabilities, sampled, weights)
    loss = float(-np.mean(weights * np.log(sampled_policy + eps)))
    diagnostics["update_weight_abs_mean"] = float(np.abs(weights).mean())
    return gradient, loss, diagnostics
