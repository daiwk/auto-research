"""Recent OPD and test-time RL mechanisms reviewed through 2026-09-12.

The common candidate-policy runner cannot reproduce full token-level training.
These updates therefore preserve each paper's defining probability operation on
candidate distributions and remain explicitly diagnostic-only in the runner.
"""

from __future__ import annotations

import numpy as np

from .algorithm_core import _weighted_policy_gradient


ALGORITHMS = {"oprd", "route-opd", "compass-opd", "probe-erpo"}


def _center(values: np.ndarray) -> np.ndarray:
    return values - values.mean()


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
    del state, rng
    eps = 1e-12
    sampled_policy = probabilities[sampled]
    sampled_rollout = rollout_training_probabilities[sampled]
    sampled_reference = reference[sampled]
    scalar_reward = group.rewards[sampled] @ np.asarray((0.7, 0.05, 0.2, 0.05))

    if algorithm == "oprd":
        # OPRD uses on-policy student samples, while the teacher's policy shift
        # relative to its reference determines how strongly a verified sample
        # should move the student.  The rollout/reference pair is the compact
        # runner's fixed teacher/reference surrogate.
        teacher_shift = _center(
            np.log(rollout_training_probabilities + eps) - np.log(reference + eps)
        )
        direction = teacher_shift / max(np.linalg.norm(teacher_shift), eps)
        advantages = _center(scalar_reward)
        logit_gradient = np.zeros_like(probabilities)
        alignments = []
        for index, advantage in zip(sampled, advantages):
            verifier_gradient = -probabilities.copy()
            verifier_gradient[index] += 1.0
            verifier_gradient *= float(advantage)
            alignment = float(direction @ verifier_gradient)
            # Equation 2.6: (I + lambda d d^T)g, with lambda=1 in
            # this fixed-budget mechanism runner.
            logit_gradient += verifier_gradient + alignment * direction
            alignments.append(alignment)
        logit_gradient /= len(sampled)
        gradient = group.features.T @ logit_gradient
        loss = float(-np.mean(advantages * np.log(sampled_policy + eps)))
        diagnostics = {
            "teacher_shift_abs_mean": float(np.abs(teacher_shift).mean()),
            "teacher_direction_norm": float(np.linalg.norm(direction)),
            "alignment_abs_mean": float(np.abs(alignments).mean()),
        }
    elif algorithm == "route-opd":
        # RouteOPD converts the teacher/student discrepancy into an explicit
        # source -> destination probability transport instead of applying a
        # dense token-wise distillation loss.
        discrepancy = np.log(sampled_rollout + eps) - np.log(sampled_policy + eps)
        source_local = int(np.argmin(discrepancy))
        destination_local = int(np.argmax(discrepancy))
        weights = np.zeros(len(sampled), dtype=np.float64)
        transported_mass = float(min(sampled_policy[source_local], sampled_rollout[destination_local]))
        weights[source_local] = -transported_mass
        weights[destination_local] = transported_mass
        diagnostics = {
            "transported_mass": transported_mass,
            "source_destination_gap": float(
                discrepancy[destination_local] - discrepancy[source_local]
            ),
        }
    elif algorithm == "compass-opd":
        # CompassOPD compares likelihood *changes* within each model family.
        # Centering cancels family-wide calibration offsets, which is the key
        # operation that permits cross-family distillation.
        teacher_change = np.log(sampled_rollout + eps) - np.log(sampled_reference + eps)
        student_change = np.log(sampled_policy + eps) - np.log(sampled_reference + eps)
        raw_gap = teacher_change - student_change
        weights = _center(raw_gap)
        diagnostics = {
            "raw_cross_family_gap": float(np.abs(raw_gap).mean()),
            "centered_cross_family_gap": float(np.abs(weights).mean()),
            "removed_family_offset": float(raw_gap.mean()),
        }
    else:  # probe-erpo
        # Probe consensus is represented by the process-verifier reward axis.
        # Low-consensus samples receive a negative signal; rank masking keeps
        # the update focused and entropy regularization prevents collapse.
        consensus = group.rewards[sampled, 2]
        threshold = float(np.median(consensus))
        rank_signal = scalar_reward.argsort().argsort().astype(np.float64)
        rank_signal /= max(1.0, float(len(rank_signal) - 1))
        rank_signal -= rank_signal.mean()
        negative_mask = consensus < threshold
        weights = rank_signal.copy()
        weights[negative_mask] -= 0.5
        entropy_direction = -np.log(sampled_policy + eps)
        weights += 0.05 * _center(entropy_direction)
        weights = _center(weights)
        diagnostics = {
            "probe_consensus_mean": float(consensus.mean()),
            "negative_probe_fraction": float(negative_mask.mean()),
            "rank_masked_samples": float(np.count_nonzero(negative_mask)),
        }

    if algorithm != "oprd":
        gradient = _weighted_policy_gradient(
            group.features, probabilities, sampled, weights
        )
        loss = float(-np.mean(weights * np.log(sampled_policy + eps)))
        diagnostics["update_weight_abs_mean"] = float(np.abs(weights).mean())
    return gradient, loss, diagnostics
