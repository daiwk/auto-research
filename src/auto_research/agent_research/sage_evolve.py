"""AdaObs control mathematics, arXiv:2611.26132v1 Eq.1--4 and Appendix B.

CPU L1 mechanism component, not the seven-stage training harness. Scores and
validated concrete observation proposals are explicit caller inputs. No model,
dataset, evaluation item, gold answer, scheduler or checkpoint is accessed.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False
LEVERS = ("L1", "L2", "L3")


def _finite(value: float) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def marginal_return(previous: float, current: float, retained_examples: int) -> float:
    """Eq.1 in score points per 10k retained examples; never invent a zero denominator.

The paper does not fully spell out a rejected increment's denominator. Callers
must supply a valid positive retained-data comparison, or supply an independently
defined marginal return directly to ``PlateauMonitor.observe``.
"""
    if not _finite(previous) or not _finite(current):
        raise ValueError("finite same-observation scores required")
    if not isinstance(retained_examples, int) or isinstance(retained_examples, bool) or retained_examples <= 0:
        raise ValueError("positive explicit retained-example count required")
    result = (current - previous) / (retained_examples / 10_000)
    if not math.isfinite(result):
        raise ValueError("nonfinite marginal return")
    return result


@dataclass
class PlateauMonitor:
    phase_id: str
    alpha: float = 0.3
    epsilon: float = 0.1
    window: int = 3

    def __post_init__(self):
        if not isinstance(self.phase_id, str) or not self.phase_id.strip():
            raise ValueError("named observation phase required")
        if not _finite(self.alpha) or not 0 < self.alpha <= 1:
            raise ValueError("alpha must be in (0,1]")
        if not _finite(self.epsilon) or self.epsilon < 0:
            raise ValueError("nonnegative finite epsilon required")
        if not isinstance(self.window, int) or isinstance(self.window, bool) or self.window < 1:
            raise ValueError("positive integer window required")
        self._history: list[float] = []

    @property
    def history(self) -> tuple[float, ...]:
        return tuple(self._history)

    @property
    def plateau(self) -> bool:
        return len(self._history) >= self.window and max(self._history[-self.window:]) < self.epsilon

    def observe(self, marginal: float, *, phase_id: str) -> bool:
        if phase_id != self.phase_id:
            raise ValueError("observation changed: start a new phase before scoring")
        if not _finite(marginal):
            raise ValueError("finite explicit marginal return required")
        # The first value initializes the EMA; no undocumented zero warm-start.
        smoothed = marginal if not self._history else self._history[-1] + self.alpha * (marginal - self._history[-1])
        if not math.isfinite(smoothed):
            raise ValueError("nonfinite smoothed return")
        self._history.append(smoothed)
        return self.plateau

    def start_phase(self, phase_id: str) -> None:
        if not isinstance(phase_id, str) or not phase_id.strip() or phase_id == self.phase_id:
            raise ValueError("a distinct named observation phase is required")
        self.phase_id = phase_id
        self._history.clear()


def retain_increment(previous_active: float, candidate_active: float,
                     previous_anchor: float, candidate_anchor: float,
                     *, anchor_tolerance: float = 0.5) -> bool:
    """Strict score improvement and inclusive maximum anchor regression."""
    values = (previous_active, candidate_active, previous_anchor, candidate_anchor, anchor_tolerance)
    if not all(_finite(value) for value in values) or anchor_tolerance < 0:
        raise ValueError("finite scores and nonnegative anchor tolerance required")
    return ((candidate_active > previous_active or candidate_anchor > previous_anchor)
            and candidate_anchor >= previous_anchor - anchor_tolerance)


@dataclass(frozen=True)
class Observation:
    benchmarks: tuple[str, ...]
    tiers: tuple[str, ...]
    diagnostic: str

    def __post_init__(self):
        for collection in (self.benchmarks, self.tiers):
            if not isinstance(collection, tuple) or not collection or any(
                    not isinstance(value, str) or not value.strip() for value in collection) or len(set(collection)) != len(collection):
                raise ValueError("unique nonempty benchmark/tier names required")
        if not isinstance(self.diagnostic, str) or not self.diagnostic.strip():
            raise ValueError("nonempty diagnostic name required")


@dataclass(frozen=True)
class Proposal:
    lever: str
    configuration: str
    observation: Observation

    def __post_init__(self):
        if self.lever not in LEVERS or not isinstance(self.configuration, str) or not self.configuration.strip():
            raise ValueError("concrete named L1/L2/L3 proposal required")
        if not isinstance(self.observation, Observation):
            raise ValueError("typed observation required")


def validate_update(current: Observation, proposal: Proposal) -> None:
    """Only one observation axis changes; earlier tasks/tiers remain active."""
    target = proposal.observation
    if proposal.lever == "L1":
        valid = (target.benchmarks == current.benchmarks and target.tiers == current.tiers
                 and target.diagnostic != current.diagnostic)
    elif proposal.lever == "L2":
        valid = (target.benchmarks == current.benchmarks and target.diagnostic == current.diagnostic
                 and set(current.tiers) < set(target.tiers) and len(target.tiers) == len(current.tiers) + 1)
    else:
        valid = (set(current.benchmarks) < set(target.benchmarks) and target.tiers == current.tiers
                 and len(target.benchmarks) == len(current.benchmarks) + 1 and target.diagnostic == current.diagnostic)
    if not valid:
        raise ValueError("proposal must change exactly its permitted axis cumulatively")


def first_feasible(current: Observation, proposals: Sequence[Proposal], *, gap: str,
                   failed: frozenset[tuple[str, str, str]] = frozenset()) -> Proposal | None:
    """B.1: reject only the concrete failed (gap, lever, configuration).

Feasibility and semantic diagnostic construction remain external. Input order
breaks ties within a lever, since the paper does not specify that selection.
"""
    if not isinstance(gap, str) or not gap.strip():
        raise ValueError("named current gap required")
    for proposal in proposals:
        if not isinstance(proposal, Proposal):
            raise ValueError("typed proposals required")
        validate_update(current, proposal)
    for lever in LEVERS:
        for proposal in proposals:
            if proposal.lever == lever and (gap, lever, proposal.configuration) not in failed:
                return proposal
    return None


def hardest_informative(tiers: Sequence[tuple[str, float]], *, low: float = 0.2,
                        high: float = 0.6) -> str | None:
    """Eq.4; tiers are explicitly supplied easiest-to-hardest by the caller."""
    if not _finite(low) or not _finite(high) or not 0 <= low <= high <= 1:
        raise ValueError("valid inclusive pass-rate band required")
    names = set()
    eligible = []
    for name, rate in tiers:
        if not isinstance(name, str) or not name.strip() or name in names or not _finite(rate) or not 0 <= rate <= 1:
            raise ValueError("unique named tiers and pass rates in [0,1] required")
        names.add(name)
        if low <= rate <= high:
            eligible.append(name)
    return eligible[-1] if eligible else None


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU-only component; no CUDA path advertised")
    monitor = PlateauMonitor("anchor")
    for value in (0.05, 0.05, 0.05):
        monitor.observe(value, phase_id="anchor")
    plateau_before = monitor.plateau
    observation = Observation(("anchor",), ("easy",), "aggregate")
    one = Proposal("L1", "by-format", Observation(("anchor",), ("easy",), "format"))
    other = Proposal("L1", "by-length", Observation(("anchor",), ("easy",), "length"))
    two = Proposal("L2", "harder", Observation(("anchor",), ("easy", "hard"), "aggregate"))
    failed = frozenset({("gap-a", "L1", "by-format")})
    selected = first_feasible(observation, [two, one, other], gap="gap-a", failed=failed)
    monitor.start_phase("format")
    wrong_phase_rejected = False
    try:
        monitor.observe(0, phase_id="anchor")
    except ValueError:
        wrong_phase_rejected = True
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"score_points_per_10k": marginal_return(60, 61, 20_000),
                        "retained_gate_cases": 2, "rejected_gate_cases": 2},
            "checks": {"three_point_plateau": plateau_before,
                         "phase_change_resets_ema": monitor.history == () and not monitor.plateau,
                         "cross_phase_rejected": wrong_phase_rejected,
                         "failed_config_not_entire_lever": selected == other,
                         "gap_specific_memory": first_feasible(observation, [one], gap="gap-b", failed=failed) == one,
                         "hardest_in_band": hardest_informative([("a", .6), ("b", .2), ("c", .1)]) == "b",
                         "anchor_tolerance_inclusive": retain_increment(50, 51, 60, 59.5),
                         "anchor_improvement_retained": retain_increment(50, 49, 60, 61),
                         "anchor_regression_rejected": not retain_increment(50, 51, 60, 59.49),
                         "no_gain_rejected": not retain_increment(50, 50, 60, 60)}}
