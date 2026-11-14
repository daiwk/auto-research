"""SensorWM Eq.55--56 CPU ranking arithmetic, not health forecasts or advice.

Candidate endpoints and feasibility decisions MUST come from external sources.
This module neither provides the private SensorWM nor validates clinical safety.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math
from numbers import Real
import random

REQUIRES_GPU_VALIDATION = False
EFFORT_FLOORS = (500.0, 15.0, 10.0)
MINIMUM_GAIN = 0.1


def _finite(value: Real, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite real number, not a boolean")
    return float(value)


@dataclass(frozen=True)
class Actions:
    """Paper action order/units: daily steps, sleep minutes, cardio minutes."""
    steps: float
    sleep_minutes: float
    cardio_minutes: float

    def __post_init__(self):
        for name in ("steps", "sleep_minutes", "cardio_minutes"):
            value = _finite(getattr(self, name), name)
            if value < 0:
                raise ValueError("action values and standard deviations must be nonnegative")
            object.__setattr__(self, name, value)

    def values(self) -> tuple[float, float, float]:
        return self.steps, self.sleep_minutes, self.cardio_minutes


@dataclass(frozen=True)
class Candidate:
    candidate_id: str
    targets: Actions
    projected_endpoint: float
    feasible: bool

    def __post_init__(self):
        if (not isinstance(self.candidate_id, str) or not self.candidate_id.strip()
                or not isinstance(self.targets, Actions) or type(self.feasible) is not bool):
            raise ValueError("identified actions and an explicit external boolean feasibility decision required")
        object.__setattr__(self, "projected_endpoint", _finite(self.projected_endpoint, "projected endpoint"))


@dataclass(frozen=True)
class RankedScore:
    """Only identity and mathematical scores: no targets or advice are emitted."""
    candidate_id: str
    gain: float
    effort: float
    score: float


def personalized_effort(targets: Actions, baseline: Actions, user_sigma: Actions) -> float:
    """Eq.55: floor historical within-user sigma, then square standardized change."""
    if not all(isinstance(x, Actions) for x in (targets, baseline, user_sigma)):
        raise ValueError("typed action targets, baseline and historical user standard deviations required")
    try:
        value = math.fsum(((target - base) / max(sigma, floor)) ** 2
                          for target, base, sigma, floor in zip(
                              targets.values(), baseline.values(), user_sigma.values(), EFFORT_FLOORS,
                              strict=True))
    except OverflowError as exc:
        raise ValueError("effort exceeds finite arithmetic range") from exc
    if not math.isfinite(value):
        raise ValueError("effort exceeds finite arithmetic range")
    return value


def rank_candidates(candidates: Sequence[Candidate], baseline: Actions, user_sigma: Actions,
                    status_quo_endpoint: float) -> list[RankedScore]:
    """Eq.56 future-versus-future gain, strict gain>0.1, external feasible filter.

    No encoder, decoder, grid, rollout, safety screening, or pathway grouping is
    supplied. Scores descend; IDs break ties as a local deterministic convention.
    """
    anchor = _finite(status_quo_endpoint, "status-quo future endpoint")
    if (not isinstance(candidates, Sequence) or isinstance(candidates, (str, bytes))
            or not all(isinstance(x, Candidate) for x in candidates)):
        raise ValueError("a sequence of typed external candidates required")
    if len({x.candidate_id for x in candidates}) != len(candidates):
        raise ValueError("candidate identities must be unique")
    # Check the baseline contract even if no candidates are supplied.
    personalized_effort(baseline, baseline, user_sigma)
    ranked = []
    for candidate in candidates:
        if not candidate.feasible:
            continue
        gain = anchor - candidate.projected_endpoint
        if not math.isfinite(gain):
            raise ValueError("gain exceeds finite arithmetic range")
        if gain <= MINIMUM_GAIN:
            continue
        effort = personalized_effort(candidate.targets, baseline, user_sigma)
        ranked.append(RankedScore(candidate.candidate_id, gain, effort, gain / (1 + effort)))
    return sorted(ranked, key=lambda x: (-x.score, x.candidate_id))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Explicit arithmetic fixtures; endpoint numbers are NOT model predictions."""
    if device != "cpu":
        raise ValueError("CPU arithmetic only; no CUDA health model exists in this component")
    if type(seed) is not int:
        raise ValueError("integer diagnostic seed required")
    baseline, sigma = Actions(1000, 400, 20), Actions(0, 0, 0)
    candidates = [Candidate("status-quo", baseline, 10, True),
                  Candidate("one", Actions(1500, 415, 30), 9.5, True),
                  Candidate("two", Actions(2000, 400, 20), 9, True),
                  Candidate("externally-rejected", baseline, 8, False)]
    random.Random(seed).shuffle(candidates)
    ranked = rank_candidates(candidates, baseline, sigma, 10)
    boundary = rank_candidates([Candidate("boundary", baseline, 0, True)], baseline, sigma, .1)
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "metrics": {"input_candidates": len(candidates), "ranked_candidates": len(ranked),
                    "best_fixture_score": ranked[0].score,
                    "three_floor_effort": personalized_effort(Actions(1500, 415, 30), baseline, sigma)},
        "checks": {"three_sigma_floors_applied": personalized_effort(Actions(1500, 415, 30), baseline, sigma) == 3,
                   "future_status_quo_anchor": ranked[0].gain == 1,
                   "score_divides_by_one_plus_effort": ranked[0].score == .2,
                   "expected_effort_adjusted_order": [x.candidate_id for x in ranked] == ["two", "one"],
                   "strict_gain_threshold": boundary == [],
                   "external_infeasible_excluded": all(x.candidate_id != "externally-rejected" for x in ranked),
                   "status_quo_gain_zero_excluded": all(x.candidate_id != "status-quo" for x in ranked),
                   "identities_and_scores_only": set(RankedScore.__dataclass_fields__)
                   == {"candidate_id", "gain", "effort", "score"}},
    }
