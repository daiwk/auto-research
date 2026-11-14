"""CoRD v1 Eq. (2) and Algorithm 1, a CPU categorical reference.

Inputs are fixed same-vocabulary next-token probabilities. This component
does not call a language model, train on coupled states, or measure pass@k.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math
from random import Random
from typing import NamedTuple


REQUIRES_GPU_VALIDATION = False


class CoupledDraw(NamedTuple):
    proposal: int
    token: int

    @property
    def replaced(self) -> bool:
        return self.proposal != self.token


def _probabilities(values: Sequence[float]) -> tuple[float, ...]:
    values = tuple(values)
    if not values or any(
        type(value) not in (float, int) or not math.isfinite(value) or not 0 <= value <= 1
        for value in values
    ):
        raise ValueError("nonempty finite nonnegative probability vector required")
    total = math.fsum(values)
    if not math.isclose(total, 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("probabilities must sum to 1")
    return tuple(value / total for value in values)


def _categorical(weights: tuple[float, ...], total: float, rng: Random) -> int:
    remaining = total * rng.random()
    last_positive = None
    for index, mass in enumerate(weights):
        if mass > 0:
            last_positive = index
            if remaining < mass:
                return index
            remaining -= mass
    if last_positive is None:
        raise ValueError("categorical distribution has no positive mass")
    # Roundoff at the last bucket must not select a zero-weight token.
    return last_positive


@dataclass(frozen=True)
class Coupling:
    student: tuple[float, ...]
    target: tuple[float, ...]
    keep_probabilities: tuple[float, ...]
    residual: tuple[float, ...]
    replacement_probability: float

    def draw(self, rng: Random) -> CoupledDraw:
        """Propose from the student and keep or sample only the positive residual."""
        proposal = _categorical(self.student, 1.0, rng)
        keep = self.keep_probabilities[proposal]
        # In particular, alpha=0 uses exactly the student draw, with no extra RNG call.
        if keep >= 1 or (keep > 0 and rng.random() < keep):
            return CoupledDraw(proposal, proposal)
        return CoupledDraw(proposal, _categorical(self.residual, self.replacement_probability, rng))


def maximal_coupling(student: Sequence[float], teacher: Sequence[float], alpha: float) -> Coupling:
    """Prepare the exact same-prefix CoRD categorical step.

    At intermediate alpha the target is normalized over the support intersection.
    Disjoint supports then have no target; an endpoint, by contrast, is defined.
    """
    p, t = _probabilities(student), _probabilities(teacher)
    if len(p) != len(t):
        raise ValueError("student and teacher must share a vocabulary")
    if type(alpha) not in (float, int) or not 0 <= alpha <= 1:
        raise ValueError("alpha must lie in [0, 1]")
    if alpha == 0 or p == t:
        q = p
    elif alpha == 1:
        q = t
    else:
        logs = tuple(
            (1 - alpha) * math.log(a) + alpha * math.log(b) if a and b else -math.inf
            for a, b in zip(p, t, strict=True)
        )
        peak = max(logs)
        if peak == -math.inf:
            raise ValueError("intermediate target is undefined for disjoint supports")
        weights = tuple(math.exp(value - peak) for value in logs)
        normalizer = math.fsum(weights)
        q = tuple(weight / normalizer for weight in weights)
    keep = tuple(min(1.0, b / a) if a and b < a else 1.0 for a, b in zip(p, q, strict=True))
    residual = tuple(max(b - a, 0.0) for a, b in zip(p, q, strict=True))
    return Coupling(p, q, keep, residual, math.fsum(residual))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Check Proposition 1, endpoint behavior, and a seeded categorical experiment."""
    if device != "cpu":
        raise ValueError("CoRD categorical reference is CPU-only")
    p, t, alpha = (0.6, 0.3, 0.1), (0.2, 0.3, 0.5), 0.6
    coupled = maximal_coupling(p, t, alpha)
    weights = [a ** (1 - alpha) * b ** alpha for a, b in zip(p, t, strict=True)]
    target = [w / math.fsum(weights) for w in weights]
    theory_tv = 0.5 * math.fsum(abs(a - b) for a, b in zip(p, target, strict=True))
    analytic_error = max(
        abs(a * keep + residual - b)
        for a, keep, residual, b in zip(p, coupled.keep_probabilities, coupled.residual, target, strict=True)
    )
    rng = Random(seed)
    n = 4096
    histogram = [0] * len(p)
    replacements = 0
    valid = True
    for _ in range(n):
        draw = coupled.draw(rng)
        histogram[draw.token] += 1
        replacements += draw.replaced
        valid &= not draw.replaced or (
            coupled.residual[draw.proposal] == 0 and coupled.residual[draw.token] > 0
        )
    marginal_error = max(abs(count / n - want) for count, want in zip(histogram, target, strict=True))
    rejection_error = abs(replacements / n - theory_tv)
    student_only = maximal_coupling(p, t, 0)
    teacher_only = maximal_coupling(p, t, 1)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "analytic_max_abs_error": analytic_error,
            "sampled_marginal_max_abs_error": marginal_error,
            "sampled_replacement_abs_error": rejection_error,
            "replacement_probability": coupled.replacement_probability,
            "draws": n,
        },
        "checks": {
            "emission_marginal_equals_target": analytic_error <= 1e-12,
            "replacement_probability_equals_tv": abs(coupled.replacement_probability - theory_tv) <= 1e-12,
            "residual_only_interventions": valid,
            "sampled_marginal_and_replacements": marginal_error < 0.04 and rejection_error < 0.04,
            "alpha_endpoints": student_only.target == p and student_only.replacement_probability == 0
            and teacher_only.target == t,
        },
    }
