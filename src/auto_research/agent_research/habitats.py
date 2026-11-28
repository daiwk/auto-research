"""Habitats paper-defined cross-fitness mathematics (arXiv:2611.31160v1).

CPU L1 diagnostic only: no reward synthesis, policy training, or agent evolution.
The paper's Appendix C normalization intentionally differs from the pinned
author repository (which includes the random baseline and maps constants to 1).
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np

REQUIRES_GPU_VALIDATION = False
EPSILON = 1e-8


def _numeric(value, *, ndim: int, name: str) -> np.ndarray:
    try:
        # Check before NumPy promotes a mixed [True, 1.0] sequence to float.
        if not isinstance(value, np.ndarray) and any(
                isinstance(item, (bool, np.bool_))
                for item in np.asarray(value, dtype=object).flat):
            raise ValueError(f"{name} must not contain booleans")
        raw = np.asarray(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a rectangular real numeric array") from exc
    if raw.ndim != ndim or raw.dtype.kind not in "iuf":
        raise ValueError(f"{name} must be a {ndim}D real numeric array, not bool/object/complex")
    result = raw.astype(np.float64, copy=True)
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite representable numbers")
    return result


def _square(value) -> np.ndarray:
    result = _numeric(value, ndim=2, name="cross-fitness")
    if not result.shape[0] or result.shape[0] != result.shape[1]:
        raise ValueError("cross-fitness must be nonempty and square")
    return result


def _vector(value, n: int, name: str, *, nonnegative: bool = False) -> np.ndarray:
    result = _numeric(value, ndim=1, name=name)
    if result.shape != (n,) or (nonnegative and np.any(result < 0)):
        raise ValueError(f"{name} must have length N" + (" and be nonnegative" if nonnegative else ""))
    return result


def mean_cross_fitness(returns) -> np.ndarray:
    """Eq.10: average already accumulated, undiscounted episode returns.

    Input axes are policy, reward, rollout. This is not an environment evaluator:
    the caller is responsible for real rollouts and isolated reward state.
    """
    values = _numeric(returns, ndim=3, name="episode returns")
    n, m, episodes = values.shape
    if n == 0 or n != m or episodes == 0:
        raise ValueError("episode returns require nonempty N x N x E axes")
    with np.errstate(over="ignore", invalid="ignore"):
        result = np.sum(values / episodes, axis=2)
    if not np.all(np.isfinite(result)):
        raise ValueError("episode-return mean exceeds numerical range")
    return result


def normalize_cross_fitness(fitness) -> np.ndarray:
    """Paper Eq.11: policy-only column min/max; constant columns become zero."""
    matrix = _square(fitness)
    low, high = matrix.min(axis=0), matrix.max(axis=0)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        normalized = (matrix - low) / (high - low + EPSILON)
    if not np.all(np.isfinite(normalized)):
        raise ValueError("normalization exceeds numerical range")
    return normalized


def survivor_mask(fitness, random_mean) -> tuple[bool, ...]:
    """Eq.3: own-column maximum (ties allowed) AND strictly above random."""
    matrix = _square(fitness)
    baseline = _vector(random_mean, len(matrix), "random mean")
    diagonal = np.diag(matrix)
    return tuple(bool(v) for v in ((diagonal == matrix.max(axis=0)) & (diagonal > baseline)))


def behavioral_diversity(normalized) -> float:
    """Eq.14: exclude zero profiles, then average epsilon-stabilized distances."""
    matrix = _numeric(normalized, ndim=2, name="normalized profiles")
    if not all(matrix.shape) or np.any(matrix < 0) or np.any(matrix > 1):
        raise ValueError("normalized profiles must be nonempty and within [0,1]")
    # hypot scales internally; squaring tiny but nonzero profiles would falsely
    # classify them as zero before the paper's epsilon-stabilized comparison.
    norms = np.array([math.hypot(*row) for row in matrix])
    selected = np.flatnonzero(norms > 0)
    if len(selected) < 2:
        return 0.0
    distances = [
        1.0 - float(np.dot(matrix[i], matrix[j])) / (float(norms[i] * norms[j]) + EPSILON)
        for pos, i in enumerate(selected) for j in selected[pos + 1:]
    ]
    return math.fsum(distances) / len(distances)


@dataclass(frozen=True)
class Summary:
    normalized: np.ndarray
    survivors: tuple[bool, ...]
    specialist_quality: float
    behavioral_diversity: float
    grounded: tuple[bool, ...]
    grounded_coverage: int


def summarize(fitness, random_mean, random_std, reward_valid) -> Summary:
    """Paper Eqs.3,11-19, without interpreting a metric as agent capability.

    Grounding is separate from survivor selection: it requires valid execution
    and standardized improvement > 0.5, not niche dominance. Random standard
    deviations are supplied observations; no distribution is fabricated here.
    """
    matrix = _square(fitness)
    n = len(matrix)
    baseline = _vector(random_mean, n, "random mean")
    deviation = _vector(random_std, n, "random standard deviation", nonnegative=True)
    try:
        valid = tuple(reward_valid)
    except TypeError as exc:
        raise ValueError("reward_valid requires N explicit booleans") from exc
    if len(valid) != n or any(type(v) not in (bool, np.bool_) for v in valid):
        raise ValueError("reward_valid requires N explicit booleans")
    normalized = normalize_cross_fitness(matrix)
    with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
        progress = (np.diag(matrix) - baseline) / (deviation + EPSILON)
    if not np.all(np.isfinite(progress)):
        raise ValueError("learning-progress score exceeds numerical range")
    grounded = tuple(bool(v and score > 0.5) for v, score in zip(valid, progress))
    # NumPy's decimal rounding is explicit; coverage is within this generation.
    profiles = {tuple(np.round(row, decimals=1)) for row, keep in zip(normalized, grounded) if keep}
    normalized.setflags(write=False)
    return Summary(normalized, survivor_mask(matrix, baseline),
                   float(np.mean(np.diag(normalized))), behavioral_diversity(normalized),
                   grounded, len(profiles))


def coverage_auc(coverages) -> int:
    """Eq.20: sum per-generation counts, not cross-generation profile union."""
    try:
        values = tuple(coverages)
    except TypeError as exc:
        raise ValueError("coverage history must be an iterable of counts") from exc
    if any(type(x) is not int or x < 0 for x in values):
        raise ValueError("coverage counts must be nonnegative Python integers")
    return sum(values)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or not 0 <= seed < 2**32 or device != "cpu":
        raise ValueError("32-bit nonnegative integer seed and CPU-only execution required")
    rng = np.random.default_rng(seed)
    # Explicit evaluator-only matrix controls, not agent-generated observations.
    fitness = np.array([[3., 0., 1.], [0., 4., 1.], [1., 1., 1.]])
    noise = rng.uniform(-0.05, 0.05, size=(3, 3))
    returns = np.stack((fitness + noise, fitness - noise), axis=2)
    measured = mean_cross_fitness(returns)
    result = summarize(measured, [-1., -1., -1.], [1., 1., 1.], [True, True, True])
    constant = summarize(np.ones((2, 2)), [0., 0.], [1., 1.], [True, True])
    duplicated = behavioral_diversity([[1., 0.], [1., 0.]])
    checks = {
        "episode_mean_matches_control": bool(np.allclose(measured, fitness, atol=1e-14, rtol=0)),
        "niche_ties_and_random_strictness": survivor_mask([[2., 1.], [2., 3.]], [2., 0.]) == (False, True),
        "constant_column_is_zero": bool(np.all(result.normalized[:, 2] == 0)),
        "quality_and_diversity_finite": math.isfinite(result.specialist_quality) and math.isfinite(result.behavioral_diversity),
        "duplicate_profiles_reduce_diversity": result.behavioral_diversity > duplicated,
        "constant_population_has_zero_quality_diversity": constant.specialist_quality == constant.behavioral_diversity == 0,
        "invalid_rewards_not_grounded": summarize(fitness, [-1., -1., -1.], [1., 1., 1.], [False] * 3).grounded_coverage == 0,
        "coverage_sums_generation_counts": coverage_auc([result.grounded_coverage, result.grounded_coverage]) == 2 * result.grounded_coverage,
        "input_not_mutated": bool(np.array_equal(fitness, [[3., 0., 1.], [0., 4., 1.], [1., 1., 1.]])),
    }
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"specialist_quality": result.specialist_quality,
            "behavioral_diversity": result.behavioral_diversity, "grounded_coverage": result.grounded_coverage,
            "survivor_count": sum(result.survivors), "control_mean_max_error": float(np.max(np.abs(measured - fitness)))}}
