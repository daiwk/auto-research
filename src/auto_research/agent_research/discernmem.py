"""DiscernMem Eqs. 4--6, 9--11: measured replay and repair acceptance.

This CPU component consumes externally measured scores and explicit scope /
diagnosis decisions. It does not run an agent, invent a diagnosis, perform an
LLM repair, retrieve tasks, or establish the validity of supplied evidence.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


def _score(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError("finite measured score in [0, 1] required")
    return float(value)


def _tolerance(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value < 1:
        raise ValueError("finite tolerance in [0, 1) required")
    return float(value)


@dataclass(frozen=True)
class ReplayScore:
    task: str
    memory: str | None
    version: int | None
    owner: str | None
    seed: int
    configuration: str
    score: float

    def __post_init__(self):
        if not self.task or not self.configuration or type(self.seed) is not int:
            raise ValueError("task, execution configuration and integer seed required")
        if self.memory is None:
            if self.version is not None or self.owner is not None:
                raise ValueError("no-memory replay cannot carry an owner/version")
        elif not self.memory or not self.owner or type(self.version) is not int or self.version < 0:
            raise ValueError("isolated memory replay needs identity, owner and version")
        _score(self.score)


def paired_effect(with_memory: ReplayScore, without_memory: ReplayScore, *, epsilon: float = .01) -> tuple[float, str]:
    """Eq.4: isolated injection, not a multi-memory marginal contribution."""
    epsilon = _tolerance(epsilon)
    if with_memory.memory is None or without_memory.memory is not None:
        raise ValueError("one isolated memory replay and one no-memory replay required")
    if (with_memory.task, with_memory.seed, with_memory.configuration) != (
        without_memory.task, without_memory.seed, without_memory.configuration
    ):
        raise ValueError("paired replays must use the same task, seed and configuration")
    effect = with_memory.score - without_memory.score
    return effect, "positive" if effect > epsilon else "negative" if effect < -epsilon else "neutral"


def attribution(effect: float, *, use_match: bool, avoid_match: bool, supported_defect: bool,
                epsilon: float = .01) -> str:
    """Eqs.5--6: avoidance wins; a negative score alone is not a defect."""
    epsilon = _tolerance(epsilon)
    if not math.isfinite(effect) or not -1 <= effect <= 1:
        raise ValueError("finite paired effect in [-1, 1] required")
    if any(type(flag) is not bool for flag in (use_match, avoid_match, supported_defect)):
        raise ValueError("external explicit Boolean scope and diagnosis decisions required")
    if avoid_match or (effect < -epsilon and not use_match):
        return "scope"
    if effect < -epsilon and use_match and supported_defect:
        return "content"
    return "none"


@dataclass(frozen=True)
class RepairComparison:
    task: str
    parent: float
    no_memory: float
    candidate: float

    def __post_init__(self):
        if not self.task:
            raise ValueError("validation task identity required")
        for value in (self.parent, self.no_memory, self.candidate):
            _score(value)


def repair_gate(comparisons: list[RepairComparison], *, trigger: str, epsilon: float = .01,
                body_changed: bool, evidence_cited: bool, expected_correction: bool) -> dict:
    """Eq.9 pointwise retention AND Eq.10 complete-failure count.

    Comparisons must cover the caller's fixed trigger/retention/related set.
    This cannot certify that tasks were selected historically without leakage.
    Non-improving candidates need all three extra evidence conditions (A.2).
    """
    epsilon = _tolerance(epsilon)
    if any(type(flag) is not bool for flag in (body_changed, evidence_cited, expected_correction)):
        raise ValueError("explicit repair evidence decisions required")
    if not comparisons or len({row.task for row in comparisons}) != len(comparisons):
        raise ValueError("nonempty unique fixed validation comparisons required")
    rows = {row.task: row for row in comparisons}
    if trigger not in rows:
        raise ValueError("trigger task must be present")
    margins = [row.candidate - max(row.parent, row.no_memory) for row in comparisons]
    parent_failures = sum(row.parent <= 0 for row in comparisons)
    candidate_failures = sum(row.candidate <= 0 for row in comparisons)
    trigger_gain = rows[trigger].candidate - rows[trigger].parent
    improving = trigger_gain > epsilon
    non_improving_evidence = body_changed and evidence_cited and expected_correction
    # Compare the original inequality rather than adding a floating tolerance
    # to its measured margin: no hidden relaxation of the paper threshold.
    pointwise = all(row.candidate >= max(row.parent, row.no_memory) - epsilon for row in comparisons)
    accepted = pointwise and candidate_failures <= parent_failures and (improving or non_improving_evidence)
    return {"accepted": accepted, "improving": improving, "trigger_gain": trigger_gain,
            "worst_margin": min(margins), "parent_failures": parent_failures,
            "candidate_failures": candidate_failures, "pointwise_retention": pointwise}


@dataclass(frozen=True)
class MemoryVersion:
    memory: str
    owner: str
    version: int
    body: str
    source_task: str
    effects: tuple[tuple[str, float], ...] = ()
    corrections: tuple[str, ...] = ()

    def __post_init__(self):
        if not all(isinstance(x, str) and x for x in (self.memory, self.owner, self.body, self.source_task)):
            raise ValueError("nonempty memory identity/owner/body/source required")
        if type(self.version) is not int or self.version < 0:
            raise ValueError("nonnegative integer memory version required")
        if len({task for task, _ in self.effects}) != len(self.effects):
            raise ValueError("non-source task effects must be unique within a version")
        for task, effect in self.effects:
            if not task or task == self.source_task or not math.isfinite(effect) or not -1 <= effect <= 1:
                raise ValueError("finite non-source measured effect required")


def revised_version(parent: MemoryVersion, *, body: str, comparisons: list[RepairComparison], trigger: str,
                    related_tasks: tuple[str, ...], correction: str, evidence_cited: bool,
                    epsilon: float = .01) -> MemoryVersion:
    """Eq.11: accepted body changes reset old-version effects, not identity.

    Only an improving repair with a nonempty related set records a capability
    correction. Scope/retrieval and provisional lifecycle remain external.
    """
    if not body or not correction or parent.source_task in {row.task for row in comparisons}:
        raise ValueError("body/correction required and source task excluded from validation")
    if len(set(related_tasks)) != len(related_tasks) or not set(related_tasks) <= {row.task for row in comparisons} - {trigger}:
        raise ValueError("related tasks must be distinct measured historical validation tasks")
    result = repair_gate(comparisons, trigger=trigger, epsilon=epsilon, body_changed=body != parent.body,
                         evidence_cited=evidence_cited, expected_correction=bool(correction))
    if not result["accepted"]:
        raise ValueError("repair rejected; original memory must be retained")
    additions = (correction,) if result["improving"] and related_tasks else ()
    return MemoryVersion(parent.memory, parent.owner, parent.version + 1, body, parent.source_task,
                         (), parent.corrections + additions)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device != "cpu" or type(seed) is not int:
        raise ValueError("pure CPU numerical contract diagnostic; no GPU or model execution")
    baseline = ReplayScore("q", None, None, None, seed, "fixed-fixture-v1", .8)
    isolated = ReplayScore("q", "m", 0, "planner", seed, "fixed-fixture-v1", .4)
    effect, label = paired_effect(isolated, baseline)
    parent = MemoryVersion("m", "planner", 0, "old", "source", (("h", .2),))
    good = [RepairComparison("q", .4, .8, .9), RepairComparison("h", .8, .7, .8)]
    bad = [RepairComparison("q", .4, .8, .9), RepairComparison("h", .8, .7, .5)]
    boundary_failure = [RepairComparison("q", .005, 0, 0)]
    args = dict(trigger="q", body_changed=True, evidence_cited=True, expected_correction=True)
    accepted = repair_gate(good, **args)
    rejected = repair_gate(bad, **args)
    failure_rejected = repair_gate(boundary_failure, **args)
    updated = revised_version(parent, body="new", comparisons=good, trigger="q", related_tasks=("h",),
                              correction="keep historical guard", evidence_cited=True)
    return {"seed": seed, "diagnostic_only": True, "component": "discernmem_measured_repair_gate",
            "metrics": {"paired_effect": effect, "accepted_trigger_gain": accepted["trigger_gain"],
                        "regression_worst_margin": rejected["worst_margin"],
                        "parent_version_effects": len(parent.effects), "new_version_effects": len(updated.effects),
                        "failure_count_negative_control": failure_rejected["candidate_failures"]},
            "checks": {"isolated_effect_not_team_credit": effect == -.4 and label == "negative",
                       "negative_use_requires_supported_defect": attribution(effect, use_match=True, avoid_match=False, supported_defect=False) == "none",
                       "avoidance_precedes_content": attribution(effect, use_match=True, avoid_match=True, supported_defect=True) == "scope",
                       "repair_passes_both_references": accepted["accepted"],
                       "historical_regression_rejected": not rejected["accepted"],
                       "complete_failure_guard_not_tolerance_only": failure_rejected["pointwise_retention"] and not failure_rejected["accepted"],
                       "new_version_resets_old_evidence": updated.effects == () and parent.effects == (("h", .2),),
                       "identity_owner_and_corrections_preserved": updated.owner == parent.owner and updated.memory == parent.memory and len(updated.corrections) == 1}}
