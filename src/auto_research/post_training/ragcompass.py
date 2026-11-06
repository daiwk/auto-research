"""RAGCompass §3.1 utility supervision, not a trained retriever router."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math
import random


REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class RoutingObjective:
    """One query's KL objective and analytic gradient with respect to scores."""

    loss: float
    prediction: tuple[float, ...]
    target: tuple[float, ...]
    score_gradient: tuple[float, ...]


def _finite(value: float, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number")
    try:
        value = float(value)
    except OverflowError as exc:
        raise ValueError(f"{label} must be a finite number") from exc
    if not math.isfinite(value):
        raise ValueError(f"{label} must be a finite number")
    return value


def _utilities(answer_f1: Sequence[float]) -> tuple[float, ...]:
    utilities = tuple(_finite(value, "answer F1") for value in answer_f1)
    if len(utilities) < 2 or any(not 0.0 <= value <= 1.0 for value in utilities):
        raise ValueError("at least two answer F1 scores in [0, 1] are required")
    return utilities


def _scores(scores: Sequence[float]) -> tuple[float, ...]:
    values = tuple(_finite(value, "routing score") for value in scores)
    if not values:
        raise ValueError("at least one routing score is required")
    return values


def _log_softmax(values: tuple[float, ...], temperature: float) -> tuple[float, ...]:
    peak = max(values)
    centered = tuple((value - peak) / temperature for value in values)
    normalizer = math.log(math.fsum(math.exp(value) for value in centered))
    return tuple(value - normalizer for value in centered)


def distillation_objective(
    scores: Sequence[float],
    answer_f1: Sequence[float],
    *,
    temperature: float,
) -> RoutingObjective:
    """Compute KL(softmax(F1/τ) || softmax(scores)) and p − u (Eqs. 2–3).

    The input F1 vector is supplied by an offline evaluator, in the same
    candidate order as the model scores. It is never used by select_retriever.
    This reference does not encode passages, train a reranker or call a reader.
    """
    values = _scores(scores)
    utility = _utilities(answer_f1)
    tau = _finite(temperature, "temperature")
    if tau <= 0.0 or len(values) != len(utility):
        raise ValueError("positive temperature and matching candidate counts required")
    log_p, log_u = _log_softmax(values, 1.0), _log_softmax(utility, tau)
    prediction = tuple(math.exp(value) for value in log_p)
    target = tuple(math.exp(value) for value in log_u)
    try:
        loss = math.fsum(
            weight * (log_target - log_pred)
            for weight, log_target, log_pred in zip(target, log_u, log_p, strict=True)
            if weight > 0.0
        )
    except OverflowError as exc:
        raise ValueError("KL objective is outside finite floating-point range") from exc
    if not math.isfinite(loss):
        raise ValueError("KL objective is outside finite floating-point range")
    gradient = tuple(p - u for p, u in zip(prediction, target, strict=True))
    return RoutingObjective(loss, prediction, target, gradient)


def eligible_query(answer_f1: Sequence[float], *, minimum_gap: float = 0.05) -> bool:
    """Offline §4 filtering only; this gate must not be called at inference."""
    utility = _utilities(answer_f1)
    gap = _finite(minimum_gap, "minimum gap")
    if not 0.0 <= gap <= 1.0:
        raise ValueError("minimum gap must be in [0, 1]")
    first, second = sorted(utility, reverse=True)[:2]
    return first - second >= gap


def select_retriever(scores: Sequence[float]) -> int:
    """Return the candidate index from supplied scores alone (first tie wins)."""
    values = _scores(scores)
    return max(range(len(values)), key=values.__getitem__)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Check the objective on a seeded candidate set, with no model or data."""
    if device != "cpu":
        raise ValueError("RAGCompass objective reference is CPU-only")
    rng = random.Random(seed)
    scores = [rng.uniform(-3.0, 3.0) for _ in range(5)]
    answer_f1 = [rng.random() for _ in scores]
    tau = 0.3
    obj = distillation_objective(scores, answer_f1, temperature=tau)
    matched = distillation_objective([x / tau for x in answer_f1], answer_f1, temperature=tau)
    reverse = distillation_objective(scores[::-1], answer_f1[::-1], temperature=tau)
    step = 1e-5
    finite_difference = []
    for index in range(len(scores)):
        above, below = scores.copy(), scores.copy()
        above[index] += step
        below[index] -= step
        high = distillation_objective(above, answer_f1, temperature=tau).loss
        low = distillation_objective(below, answer_f1, temperature=tau).loss
        finite_difference.append((high - low) / (2.0 * step))
    max_error = max(abs(a - b) for a, b in zip(obj.score_gradient, finite_difference, strict=True))
    norm_error = max(abs(math.fsum(obj.prediction) - 1.0), abs(math.fsum(obj.target) - 1.0))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "objective": obj.loss,
            "gradient_finite_difference_max_error": max_error,
            "probability_sum_max_error": norm_error,
        },
        "checks": {
            "gradient_matches_finite_difference": max_error < 1e-8,
            "probabilities_normalized": norm_error < 1e-14,
            "matching_distributions_zero_kl": abs(matched.loss) < 1e-14,
            "candidate_permutation_preserves_loss": abs(obj.loss - reverse.loss) < 1e-14,
            "offline_filter_distinguishes_gap": eligible_query([0.8, 0.5]) and not eligible_query([0.5, 0.51]),
            "score_only_inference": select_retriever([-1.0, 2.0, 0.0]) == 1,
        },
    }
