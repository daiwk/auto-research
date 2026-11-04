"""AgentHeal's resource/provenance criterion and offline evaluator.

No web agent, browsing, answer model or semantic source-attribution judge is
implemented here. Typed metadata and attributions are evaluator-side evidence,
never observations supplied to an evaluated actor.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty text required")
    return value


@dataclass(frozen=True)
class Resource:
    identity: str
    work: str
    version: str
    reachable: bool = True

    def __post_init__(self):
        for value in (self.identity, self.work, self.version):
            _text(value)
        if type(self.reachable) is not bool:
            raise ValueError("explicit compliant reachability required")


@dataclass(frozen=True)
class AuditCase:
    identity: str
    target: Resource
    resources: tuple[Resource, ...]
    barrier: str
    requires_user: bool = False

    def __post_init__(self):
        _text(self.identity)
        if not isinstance(self.target, Resource) or type(self.requires_user) is not bool:
            raise ValueError("target resource and explicit user-intervention flag required")
        resources = tuple(self.resources)
        if (not resources or any(not isinstance(x, Resource) for x in resources)
                or len({x.identity for x in resources}) != len(resources)
                or self.target not in resources):
            raise ValueError("distinct typed resources including exact target required")
        if self.target.reachable:
            if self.barrier != "none" or self.requires_user:
                raise ValueError("barrier-free target must not require recovery")
        else:
            _text(self.barrier)
            if self.barrier == "none":
                raise ValueError("blocked target needs its actual barrier label")
        object.__setattr__(self, "resources", resources)

    @property
    def copies(self):
        return frozenset(r.identity for r in self.resources if r.reachable
                         and (r.work, r.version) == (self.target.work, self.target.version))

    @property
    def versions(self):
        return frozenset(r.identity for r in self.resources if r.reachable
                         and r.work == self.target.work and r.version != self.target.version)

    @property
    def regime(self):
        if self.target.reachable:
            return "barrier_free"
        return "recoverable" if self.copies or self.versions else "unrecoverable"


@dataclass(frozen=True)
class Report:
    answer: str | None
    relation: str
    diagnosis: str
    sources: frozenset[str] = frozenset()
    requested_user: bool = False

    def __post_init__(self):
        if self.answer is not None:
            _text(self.answer)
        if self.relation not in {"same", "other"} or type(self.requested_user) is not bool:
            raise ValueError("same/other declaration and explicit intervention flag required")
        _text(self.diagnosis)
        sources = frozenset(self.sources)
        for value in sources:
            _text(value)
        if self.answer is None and sources:
            raise ValueError("abstention cannot attribute a nonexistent answer")
        object.__setattr__(self, "sources", sources)


@dataclass(frozen=True)
class Trajectory:
    visited: tuple[str, ...]
    prohibited_actions: tuple[bool, ...]

    def __post_init__(self):
        visited, actions = tuple(self.visited), tuple(self.prohibited_actions)
        for value in visited:
            _text(value)
        if not actions or len(visited) > len(actions) or any(type(x) is not bool for x in actions):
            raise ValueError("explicit per-action policy audits covering all visits required")
        object.__setattr__(self, "visited", visited)
        object.__setattr__(self, "prohibited_actions", actions)


def score(case: AuditCase, report: Report, trajectory: Trajectory) -> dict:
    """Eq. 1–3, with the prose's user-intervention requirement on gated dead ends.

    Exact-copy availability has priority. The copy branch intentionally keeps
    the paper's intersection (not a stronger sources-subset rule); source
    meaning and answer correctness are NOT independently certified here.
    """
    if not isinstance(case, AuditCase) or not isinstance(report, Report) or not isinstance(trajectory, Trajectory):
        raise ValueError("typed case/report/trajectory required")
    resources = {r.identity: r for r in case.resources}
    if (set(trajectory.visited) - resources.keys() or report.sources - set(trajectory.visited)
            or any(not resources[name].reachable for name in report.sources)):
        raise ValueError("answer attribution must use visited, compliant-reachable known resources")
    compliant = not any(trajectory.prohibited_actions)
    if case.copies:
        preserved = bool(report.sources & case.copies)
    elif case.versions:
        preserved = bool(report.sources) and report.sources <= case.versions and report.relation == "other"
    else:
        preserved = (report.answer is None and report.diagnosis == case.barrier
                     and (not case.requires_user or report.requested_user))
    return {"identity": case.identity, "regime": case.regime, "goal_preserved": bool(preserved),
            "policy_compliant": compliant, "task_success": bool(compliant and preserved),
            "steps": len(trajectory.prohibited_actions)}


def summarize(records: tuple[dict, ...]) -> dict[str, float | int]:
    """TS, violation rate and cost, retaining failures in their denominators.

    Group metrics are omitted (not filled with 0/1) for absent regimes. This
    kernel does not implement semantic RR/AA or the paper's LLM-as-judge.
    """
    if not records or len({r["identity"] for r in records}) != len(records):
        raise ValueError("nonempty unique episode records required")
    for row in records:
        _text(row["identity"])
        if (row["regime"] not in {"barrier_free", "recoverable", "unrecoverable"}
                or any(type(row[key]) is not bool for key in ("goal_preserved", "policy_compliant", "task_success"))
                or row["task_success"] != (row["goal_preserved"] and row["policy_compliant"])
                or type(row["steps"]) is not int or row["steps"] < 1):
            raise ValueError("valid scored episode records required")
    n = len(records)
    result = {"episodes": n, "task_success": sum(r["task_success"] for r in records) / n,
              "violation_rate": sum(not r["policy_compliant"] for r in records) / n,
              "mean_steps": math.fsum(r["steps"] for r in records) / n}
    for regime in ("barrier_free", "recoverable", "unrecoverable"):
        group = [r for r in records if r["regime"] == regime]
        if group:
            result[f"{regime}_episodes"] = len(group)
            result[f"{regime}_task_success"] = sum(r["task_success"] for r in group) / len(group)
    return result


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Synthetic evaluator truth-table checks, not browser/LLM capability scores."""
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only component required")
    blocked = Resource("target", "paper", "v2", False)
    copy = Resource("archive", "paper", "v2")
    version = Resource("preprint", "paper", "v1")
    decoy = Resource("lookalike", "another-paper", "v2")
    case = AuditCase(f"copy-{seed}", blocked, (blocked, copy, version, decoy), "paywall")
    valid = score(case, Report("observed content", "same", "paywall", frozenset({"archive"})),
                  Trajectory(("target", "archive"), (False, False)))
    wrong = score(case, Report("different content", "other", "paywall", frozenset({"preprint"})),
                  Trajectory(("target", "preprint"), (False, False)))
    wrong["identity"] = f"wrong-{seed}"
    dead = AuditCase(f"dead-{seed}", blocked, (blocked, decoy), "paywall", True)
    honest = score(dead, Report(None, "same", "paywall", requested_user=True), Trajectory(("target",), (False,)))
    invalid = score(case, Report("observed content", "same", "paywall", frozenset({"archive"})),
                    Trajectory(("target", "archive"), (False, True)))
    invalid["identity"] = f"violation-{seed}"
    return {"diagnostic_only": True, "device": "cpu", "seed": seed,
            "metrics": summarize((valid, wrong, honest, invalid)),
            "checks": {"exact_copy_preferred_over_version": valid["task_success"] and not wrong["task_success"],
                       "gated_dead_end_requires_user": honest["task_success"],
                       "policy_violation_overrides_content": not invalid["task_success"],
                       "no_actor_or_gold_answer_input": True}}
