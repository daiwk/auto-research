"""Bait fixed-v1 Eqs.3--5: defensive reward-gap detection and sign inversion.

This module receives numeric rewards and defender-private probe membership only.
It cannot generate probes, harmful text, attacks, a reward model or RL updates.
Eq.6/Algorithm1 advantage-normalization discrepancy is deliberately not guessed.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class DefenseResult:
    divergence: tuple[float, ...]
    detected: tuple[bool, ...]
    transformed_rewards: tuple[tuple[float, ...], ...]
    policy_only_rewards: tuple[tuple[float, ...], ...]


def transform_rewards(rewards, probe_mask) -> DefenseResult:
    """Only probed groups: delta>=0 flips every reward; probes are not policy data.

    Algorithm1's no-probe coin branch is outside this conditional kernel. Empty
    probe/policy partitions are rejected rather than turning their NaN into a
    benign decision. Reward provenance and semantic harmfulness remain external.
    """
    values, probes = np.asarray(rewards), np.asarray(probe_mask)
    if (
        values.ndim != 2
        or values.dtype.kind not in "fiu"
        or min(values.shape) < 1
        or not np.isfinite(values).all()
        or probes.shape != values.shape
        or probes.dtype != bool
    ):
        raise ValueError(
            "finite numeric [group,response] rewards and same-shape Boolean private probe mask required"
        )
    counts = probes.sum(axis=1)
    if (counts == 0).any() or (counts == values.shape[1]).any():
        raise ValueError("each group needs at least one probe and one policy response")
    values = values.astype(float)
    delta = (values * probes).sum(axis=1) / counts - (values * ~probes).sum(axis=1) / (~probes).sum(
        axis=1
    )
    detected = delta >= 0
    transformed = np.where(detected[:, None], -values, values)
    return DefenseResult(
        tuple(delta.tolist()),
        tuple(detected.tolist()),
        tuple(tuple(row.tolist()) for row in transformed),
        tuple(tuple(row[~mask].tolist()) for row, mask in zip(transformed, probes, strict=True)),
    )


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only numeric defense kernel required")
    values = np.array([[8.0, 9.0, 1.0, 2.0], [1.0, 2.0, 8.0, 9.0], [2.0, 4.0, 1.0, 5.0]])
    probes = np.array([[True, True, False, False]] * 3)
    order = np.random.default_rng(seed).permutation(4)
    result = transform_rewards(values[:, order], probes[:, order])
    transformed = np.asarray(result.transformed_rewards)
    checks = {
        "nonnegative_boundary_is_positive_detection": result.detected == (True, False, True),
        "exact_divergence": result.divergence == (7.0, -7.0, 0.0),
        "flip_applies_to_whole_group": bool(np.array_equal(transformed[0], -values[0, order])),
        "negative_gap_keeps_rewards": bool(np.array_equal(transformed[1], values[1, order])),
        "probes_excluded_from_policy_output": all(
            len(row) == 2 for row in result.policy_only_rewards
        ),
        "input_arrays_unchanged": bool(np.array_equal(values[0], [8.0, 9.0, 1.0, 2.0])),
    }
    return {
        "seed": seed,
        "device": device,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": checks,
        "metrics": {
            "fixture_groups": 3,
            "detected_fixture_groups": sum(result.detected),
            "policy_only_items": sum(len(row) for row in result.policy_only_rewards),
            "boundary_divergence": result.divergence[2],
            "model_calls": 0,
            "training_steps": 0,
        },
    }
