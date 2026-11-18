"""CPU report protocol for arXiv:2610.03713v2; not an adaptation algorithm.

Probes are externally produced predictions on held-out queries. This module has no
model or policy and cannot improve retention by reading their targets.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from statistics import median
from typing import Sequence

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class ProbeRound:
    """A stable, held-out concept panel after one adaptation round."""

    round_id: int
    probe_ids: tuple[str, ...]
    passed: tuple[bool, ...]


def invariant_retention(
    rounds: Sequence[ProbeRound], *, adaptation_ids: Sequence[str] = ()
) -> dict[str, object]:
    """Report minimum accuracy and negative flips, not disagreement with a teacher.

Identical probe IDs and ordering across rounds are required: a changed panel is
not evidence that a previously correct invariant was preserved.
    """
    if not rounds:
        raise ValueError("at least one held-out probe round is required")
    panel = rounds[0].probe_ids
    if not panel or len(set(panel)) != len(panel):
        raise ValueError("probe IDs must be nonempty and unique")
    if set(panel).intersection(adaptation_ids):
        raise ValueError("adaptation examples must not be held-out probes")
    previous_id = -1
    for row in rounds:
        if row.round_id <= previous_id or row.probe_ids != panel:
            raise ValueError("round IDs must increase and the probe panel must stay fixed")
        if len(row.passed) != len(panel) or any(type(x) is not bool for x in row.passed):
            raise ValueError("each probe requires a boolean result")
        previous_id = row.round_id
    accuracy = [sum(r.passed) / len(panel) for r in rounds]
    flips = [
        sum(before and not after for before, after in zip(a.passed, b.passed, strict=True))
        for a, b in zip(rounds[:-1], rounds[1:], strict=True)
    ]
    corrections = sum(
        not before and after
        for a, b in zip(rounds[:-1], rounds[1:], strict=True)
        for before, after in zip(a.passed, b.passed, strict=True)
    )
    return {
        "round_accuracy": accuracy,
        "minimum_retention": min(accuracy),
        "negative_flips_by_round": flips,
        "negative_flips": sum(flips),
        "corrected_initial_or_intermediate_errors": corrections,
        "probe_count": len(panel),
    }


@dataclass(frozen=True)
class ChangeTrace:
    """Scores on new-episode held-out queries after each relevant observation.

``new_minus_old`` is the externally measured preference for the changed fact.
The list counts observations of the changed region, not arbitrary time steps.
``censored`` denotes a change too near the stream end for its declared horizon.
    """

    change_id: str
    stratum: str
    new_minus_old: tuple[float, ...]
    query_episode: str
    adaptation_episode: str
    horizon: int
    censored: bool = False


def revision_report(
    traces: Sequence[ChangeTrace], *, margin: float = 0.1, consecutive: int = 2
) -> dict[str, dict[str, object]]:
    """Keep revision latency, never-revised and censored counts separate."""
    if not math.isfinite(margin) or margin <= 0 or consecutive < 1:
        raise ValueError("positive finite margin and consecutive count required")
    if len({t.change_id for t in traces}) != len(traces):
        raise ValueError("change IDs must be unique")
    result: dict[str, dict[str, object]] = {}
    for trace in traces:
        if trace.stratum not in {"regularity", "instance"}:
            raise ValueError("only revisable regularity/instance strata have latency")
        if trace.query_episode == trace.adaptation_episode:
            raise ValueError("revision probes must come from a new held-out episode")
        if trace.horizon < consecutive or len(trace.new_minus_old) > trace.horizon:
            raise ValueError("invalid observation horizon")
        if any(not math.isfinite(x) for x in trace.new_minus_old):
            raise ValueError("preference scores must be finite")
        if len(trace.new_minus_old) < trace.horizon and not trace.censored:
            raise ValueError("truncated traces must be explicitly censored")
        row = result.setdefault(trace.stratum, {"latencies": [], "never_revised": 0, "censored": 0})
        streak = 0
        latency = None
        for observation, gap in enumerate(trace.new_minus_old, start=1):
            streak = streak + 1 if gap >= margin else 0
            if streak == consecutive:
                latency = observation
                break
        if latency is not None:
            row["latencies"].append(latency)
        elif trace.censored:
            row["censored"] += 1
        else:
            row["never_revised"] += 1
    for row in result.values():
        row["median_latency"] = median(row["latencies"]) if row["latencies"] else None
    return result


def false_revision_rate(flipped_on_reverting_perturbation: Sequence[bool]) -> float:
    """Evaluator-supplied unchanged-regularity false alarms; no composite score."""
    if not flipped_on_reverting_perturbation:
        raise ValueError("at least one transient perturbation is required")
    if any(type(x) is not bool for x in flipped_on_reverting_perturbation):
        raise ValueError("false-alarm labels must be boolean")
    return sum(flipped_on_reverting_perturbation) / len(flipped_on_reverting_perturbation)


def diagnostic(seed: int, device: str = "cpu") -> dict[str, object]:
    """Deterministic counterexamples; no world model is trained or evaluated."""
    if device != "cpu":
        raise ValueError("this report-only protocol supports CPU only")
    probes = ("gravity", "permanence", "collision")
    retained = invariant_retention([
        ProbeRound(0, probes, (True, False, True)),
        ProbeRound(1, probes, (False, True, True)),
        ProbeRound(2, probes, (True, True, True)),
    ])
    revisions = revision_report([
        ChangeTrace("door", "instance", (-0.3, 0.2, 0.3, 0.3), "probe-new", "adapt", 4),
        ChangeTrace("frozen", "instance", (-0.3,) * 4, "probe-new", "adapt", 4),
        ChangeTrace("late-change", "instance", (-0.3,), "probe-new", "adapt", 4, True),
    ])
    rejected = False
    try:
        invariant_retention([ProbeRound(0, probes, (True,) * 3)], adaptation_ids=["gravity"])
    except ValueError:
        rejected = True
    instance = revisions["instance"]
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
        "checks": {
            "transient_invariant_failure_not_hidden_by_final_recovery": retained["negative_flips"] == 1,
            "correcting_an_error_is_not_forgetting": retained["corrected_initial_or_intermediate_errors"] == 2,
            "latency_requires_consecutive_new_episode_preferences": instance["latencies"] == [3],
            "frozen_and_censored_cases_are_distinct": instance["never_revised"] == instance["censored"] == 1,
            "adaptation_probe_overlap_rejected": rejected,
        },
        "metrics": {
            "minimum_invariant_probe_fraction": retained["minimum_retention"],
            "negative_flip_count": retained["negative_flips"],
            "instance_observation_latency": instance["median_latency"],
            "false_revision_fraction": false_revision_rate([False, True, False]),
        },
    }
