"""HoMe's CPU sampling and construction-reuse slice (2611.34624v1).

Host-owned score observations drive validation selection, not an agent policy.
No answers, source sessions, LLM diagnostician or harness optimizer live here.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
import random
from typing import Mapping

REQUIRES_GPU_VALIDATION = False


def _integer(value: int, name: str, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


def _unit(value: float, name: str) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError(f"{name} must be finite and within [0,1]")


@dataclass(frozen=True)
class Observation:
    loss: float | None = None
    count: int = 0
    last_selected: int | None = None
    last_error: int | None = None
    perfect_after_error: int = 0

    def __post_init__(self) -> None:
        _integer(self.count, "count")
        _integer(self.perfect_after_error, "perfect_after_error")
        if self.loss is not None:
            _unit(self.loss, "loss")
        for value in (self.last_selected, self.last_error):
            if value is not None:
                _integer(value, "round")
        if (self.count == 0) != (self.loss is None):
            raise ValueError("loss is present exactly when an observation exists")


def observe(record: Observation, score: float, round_id: int, alpha: float = 0.3) -> Observation:
    """Equations 6-7; infrastructure failures must not be passed as scores."""
    _unit(score, "score")
    _unit(alpha, "alpha")
    _integer(round_id, "round")
    loss = 1.0 - score
    return replace(
        record, loss=loss if record.loss is None else alpha * loss + (1 - alpha) * record.loss,
        count=record.count + 1,
        last_error=round_id if score < 1 else record.last_error,
        perfect_after_error=0 if score < 1 else record.perfect_after_error + int(record.last_error is not None),
    )


def probabilities(records: Mapping[str, Observation], round_id: int, epsilon: float = 0.2) -> dict[str, float]:
    """Equation 5: real uniform mixture, not an uncertainty/confidence estimate."""
    _integer(round_id, "round")
    _unit(epsilon, "epsilon")
    if not records or any(not isinstance(k, str) or not k for k in records):
        raise ValueError("nonempty identified sampling units required")
    priorities = {}
    for key, record in records.items():
        stale = round_id if record.last_selected is None else max(round_id - record.last_selected, 0)
        unresolved = 0.0 if record.last_error is None else (
            math.log1p(max(round_id - record.last_error, 0)) / (1 + record.perfect_after_error))
        priorities[key] = (0.5 if record.loss is None else record.loss) + 0.2 * math.log1p(stale) + (
            0.2 / math.sqrt(record.count + 1)) + 0.1 * unresolved
    maximum = max(priorities.values())
    weights = {key: math.exp(value - maximum) for key, value in priorities.items()}
    total = sum(weights.values())
    return {key: (1 - epsilon) * value / total + epsilon / len(weights) for key, value in weights.items()}


@dataclass(frozen=True)
class Case:
    case_id: str
    query_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.case_id, str) or not self.case_id or type(self.query_ids) is not tuple:
            raise ValueError("case ID and immutable query tuple required")
        if not self.query_ids or any(type(q) is not str or not q for q in self.query_ids):
            raise ValueError("nonempty query IDs required")
        if len(set(self.query_ids)) != len(self.query_ids):
            raise ValueError("duplicate query IDs")


@dataclass(frozen=True)
class Plan:
    round_id: int
    selected: tuple[tuple[str, tuple[str, ...]], ...]


def _order(weights: Mapping[str, float], rng: random.Random) -> list[str]:
    # Exponential race: weighted draws without replacement, numerically stable.
    return sorted(weights, key=lambda key: -math.log(max(rng.random(), 1e-300)) / weights[key])


def sample(cases: tuple[Case, ...], case_records: Mapping[str, Observation],
           query_records: Mapping[tuple[str, str], Observation], *, round_id: int,
           max_cases: int, max_queries: int | None = None, seed: int = 42) -> Plan:
    """Two levels with upstream fair-share query allocation; never reads gold."""
    _integer(max_cases, "max_cases", 1)
    _integer(seed, "seed")
    if max_queries is not None:
        _integer(max_queries, "max_queries", 1)
    if not cases or len({c.case_id for c in cases}) != len(cases):
        raise ValueError("nonempty unique cases required")
    by_id = {c.case_id: c for c in cases}
    rng = random.Random(seed)
    ordered = _order(probabilities({k: case_records.get(k, Observation()) for k in by_id}, round_id), rng)
    selected = []
    remaining = max_queries
    for case_id in ordered:
        if len(selected) == max_cases or remaining == 0:
            break
        query_ids = by_id[case_id].query_ids
        if remaining is not None:
            weights = probabilities({q: query_records.get((case_id, q), Observation()) for q in query_ids}, round_id)
            fair_share = math.ceil(remaining / (max_cases - len(selected)))
            query_ids = tuple(_order(weights, rng)[:min(len(query_ids), fair_share, remaining)])
            remaining -= len(query_ids)
        selected.append((case_id, query_ids))
    return Plan(round_id, tuple(selected))


def mark_selected(plan: Plan, case_records: Mapping[str, Observation],
                  query_records: Mapping[tuple[str, str], Observation]) -> tuple[dict, dict]:
    """Commit selection timestamps, without pretending selected units were scored."""
    updated_cases, updated_queries = dict(case_records), dict(query_records)
    for case_id, query_ids in plan.selected:
        updated_cases[case_id] = replace(updated_cases.get(case_id, Observation()), last_selected=plan.round_id)
        for query_id in query_ids:
            key = (case_id, query_id)
            updated_queries[key] = replace(updated_queries.get(key, Observation()), last_selected=plan.round_id)
    return updated_cases, updated_queries


@dataclass(frozen=True)
class ConstructionIdentity:
    dataset: str
    runtime: str
    construction: str
    model: str

    def __post_init__(self) -> None:
        if any(type(v) is not str or not v for v in (
                self.dataset, self.runtime, self.construction, self.model)):
            raise ValueError("complete host construction fingerprints required")


@dataclass(frozen=True)
class ReusableAncestor:
    commit: str
    distance: int
    identity: ConstructionIdentity
    snapshot_sha256: str
    completed: bool
    construction_unchanged: bool | None

    def __post_init__(self) -> None:
        _integer(self.distance, "ancestor distance", 1)
        if not self.commit or len(self.snapshot_sha256) != 64 or any(
                c not in "0123456789abcdef" for c in self.snapshot_sha256):
            raise ValueError("commit and sanitized snapshot hash required")
        if type(self.completed) is not bool or (
                self.construction_unchanged is not None and type(self.construction_unchanged) is not bool):
            raise ValueError("explicit host review and completion required")


def reuse_source(ancestors: tuple[ReusableAncestor, ...], identity: ConstructionIdentity,
                 *, seed: int = 42, probability: float = 0.6) -> ReusableAncestor | None:
    """Nearest host-approved compatible ancestor, then ONE 60/40 draw.

    Review decisions are trusted host inputs, not inferred by filename equality.
    Unknown equivalence always rebuilds. This does not execute an LLM reviewer.
    """
    _integer(seed, "seed")
    _unit(probability, "probability")
    eligible = [a for a in ancestors if a.completed and a.construction_unchanged is True and a.identity == identity]
    if not eligible:
        return None
    nearest = min(eligible, key=lambda a: (a.distance, a.commit))
    return nearest if random.Random(seed).random() < probability else None


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    failed = observe(Observation(), 0.0, 0)
    passed = observe(Observation(), 1.0, 0)
    weights = probabilities({"failed": failed, "passed": passed}, 2)
    cases = tuple(Case(f"c{i}", tuple(f"q{j}" for j in range(5))) for i in range(4))
    args = dict(round_id=2, max_cases=3, max_queries=6, seed=seed)
    plan = sample(cases, {}, {}, **args)
    identity = ConstructionIdentity("data-rev", "runtime-rev", "construction-rev", "model-rev")
    ancestor = ReusableAncestor("a", 1, identity, "a" * 64, True, True)
    invalid_rejected = False
    try:
        observe(failed, float("nan"), 2)
    except ValueError:
        invalid_rejected = True
    checks = {
        "failure_has_higher_priority": weights["failed"] > weights["passed"],
        "uniform_mass_preserved": all(p >= 0.1 for p in weights.values()),
        "normalized_probabilities": math.isclose(sum(weights.values()), 1.0),
        "invalid_score_rejected": invalid_rejected,
        "seeded_plan_repeatable": plan == sample(cases, {}, {}, **args),
        "case_draw_without_replacement": len({c for c, _ in plan.selected}) == len(plan.selected),
        "query_budget_enforced": sum(len(q) for _, q in plan.selected) <= 6,
        "unknown_equivalence_rebuilds": reuse_source((replace(ancestor, construction_unchanged=None),), identity) is None,
        "changed_construction_rebuilds": reuse_source((ancestor,), replace(identity, construction="changed")) is None,
        "approved_snapshot_can_reuse": reuse_source((ancestor,), identity, probability=1) == ancestor,
    }
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"selected_cases": len(plan.selected),
            "selected_queries": sum(len(q) for _, q in plan.selected), "failure_priority_mass": weights["failed"]}}
