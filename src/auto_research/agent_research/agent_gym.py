"""Agent Gym ALF collect/plan/execute and human-admission kernel; no LLM.

arXiv:2608.15591v3 sections 3.4.3 and 3.5. This independent CPU component
supports eight documented condition operators, not the full author engine.
Semantic continuation/patching are explicit external callbacks, never inferred.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
import hashlib
import json
import math

REQUIRES_GPU_VALIDATION = False
OPERATORS = {"equals", "not_equals", "contains", "starts_with", "greater_than", "less_than", "in_list", "is_null"}
RESUME_ORDER = {"phase2": 0, "phase3": 1, "phase4": 2, "transformer": 3}


def _json(value):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("nonfinite case data")
    if value is None or type(value) in {str, int, float, bool}:
        return
    if isinstance(value, list):
        for item in value:
            _json(item)
        return
    if isinstance(value, dict) and all(isinstance(key, str) for key in value):
        for item in value.values():
            _json(item)
        return
    raise ValueError("plain finite JSON values required")


def resolve(data: dict, path: str):
    if not isinstance(path, str) or not path or any(not part for part in path.split(".")):
        raise ValueError("nonempty dotted field path required")
    item = data
    for part in path.split("."):
        if not isinstance(item, dict) or part not in item:
            return None
        item = item[part]
    return item


@dataclass(frozen=True)
class Condition:
    field: str
    operator: str
    value: object = None

    def __post_init__(self):
        if self.operator not in OPERATORS:
            raise ValueError("unsupported operator; this component does not claim all 21")
        resolve({}, self.field)
        _json(self.value)

    def matches(self, context: dict) -> bool:
        actual, expected = resolve(context, self.field), self.value
        if isinstance(expected, str) and expected.startswith("_DYNAMIC_") and expected.endswith("_"):
            expected = resolve(context, expected[len("_DYNAMIC_"):-1])
        if self.operator == "is_null":
            return actual is None
        if self.operator in {"equals", "not_equals"}:
            equal = (actual.strip().lower() == expected.strip().lower()
                     if isinstance(actual, str) and isinstance(expected, str) else actual == expected)
            return equal if self.operator == "equals" else not equal
        if self.operator in {"contains", "starts_with"}:
            if actual is None:
                return False
            left, right = str(actual).lower(), str(expected).lower()
            return right in left if self.operator == "contains" else left.startswith(right)
        if self.operator == "in_list":
            return isinstance(expected, list) and (str(actual).lower() in [str(x).lower() for x in expected]
                                                   if isinstance(actual, str) else actual in expected)
        try:
            left = float(actual) if actual is not None else 0.
            right = float(expected) if expected is not None else 0.
            return left > right if self.operator == "greater_than" else left < right
        except (TypeError, ValueError):
            return False


@dataclass(frozen=True)
class Action:
    tier: int
    edits: tuple[tuple[str, object], ...] = ()
    target_fields: tuple[str, ...] = ()
    resume_from: str = "phase2"
    context: str = ""

    def __post_init__(self):
        if type(self.tier) is not int or self.tier not in {1, 2, 3}:
            raise ValueError("ALF action tier must be 1, 2, or 3")
        if self.tier == 1 and (not self.edits or self.target_fields):
            raise ValueError("tier 1 needs explicit deterministic field edits")
        if self.tier == 2 and (not self.target_fields or self.edits):
            raise ValueError("tier 2 needs named patch targets, not predetermined answers")
        if self.tier == 3 and (self.edits or self.target_fields or self.resume_from not in RESUME_ORDER):
            raise ValueError("tier 3 needs a known continuation point")
        for path, value in self.edits:
            resolve({}, path)
            _json(value)
        if len(set(path for path, _ in self.edits)) != len(self.edits):
            raise ValueError("duplicate deterministic target")
        for path in self.target_fields:
            resolve({}, path)


@dataclass(frozen=True)
class Rule:
    identity: str
    scope: str
    priority: int
    conditions: tuple[Condition, ...]
    actions: tuple[Action, ...]

    def __post_init__(self):
        if (not self.identity or not self.scope or type(self.priority) is not int
                or not self.conditions or not self.actions):
            raise ValueError("identified scoped rule needs nonempty conditions/actions")

    @property
    def digest(self) -> str:
        return hashlib.sha256(json.dumps(asdict(self), sort_keys=True, allow_nan=False).encode()).hexdigest()

    def matches(self, context: dict) -> bool:
        return all(condition.matches(context) for condition in self.conditions)


@dataclass(frozen=True)
class Impact:
    rule_digest: str
    target_id: str
    target_matched: bool
    collateral_ids: tuple[str, ...]


def assess_impact(rule: Rule, cases: dict[str, dict], target_id: str, *, split: str = "adaptation") -> Impact:
    if split != "adaptation" or target_id not in cases:
        raise ValueError("target and adaptation cases required; held-out/test cases cannot train rules")
    for case in cases.values():
        _json(case)
    return Impact(rule.digest, target_id, rule.matches(cases[target_id]),
                  tuple(key for key, case in cases.items() if key != target_id and rule.matches(case)))


@dataclass(frozen=True)
class ApprovedRule:
    rule: Rule
    approver: str
    approved_digest: str


def admit(rule: Rule, impact: Impact, *, approver: str | None,
          approve: bool, acknowledge_collateral: bool = False) -> ApprovedRule:
    """Consume explicit external human approval, never create or authenticate it.

    After repeated narrowing the paper permits approval with a collateral
    warning. This kernel requires explicit acknowledgement of that warning.
    LLM generation/three-attempt auto-tightening are NOT implemented.
    """
    if impact.rule_digest != rule.digest or not impact.target_matched:
        raise ValueError("approved rule must match the assessed target and exact rule bytes")
    if type(approve) is not bool or not approve or not isinstance(approver, str) or not approver.strip():
        raise ValueError("explicit named human approval required")
    if impact.collateral_ids and not acknowledge_collateral:
        raise ValueError("unresolved collateral warning requires explicit human acknowledgement")
    return ApprovedRule(rule, approver, rule.digest)


def _edit(output: dict, path: str, value) -> None:
    parent = output
    parts = path.split(".")
    for part in parts[:-1]:
        if not isinstance(parent.get(part), dict):
            raise ValueError("edit path does not exist in the output schema")
        parent = parent[part]
    if parts[-1] not in parent or type(parent[parts[-1]]) is not type(value):
        raise ValueError("field edit must preserve an existing field's exact JSON type")
    _json(value)
    parent[parts[-1]] = deepcopy(value)


def execute(output: dict, context: dict, rules: tuple[ApprovedRule, ...], *, continuation=None, patcher=None) -> dict:
    """Actual collect-plan-execute; callbacks supply results, not success labels.

    One merged continuation and one merged patch callback at most. Deterministic
    edits run last. No LLM, source-code execution, persistence, or semantic judge.
    """
    _json(output)
    _json(context)
    identities, priorities, scopes, selected, trace = set(), set(), set(), [], []
    for approved in sorted(rules, key=lambda item: item.rule.priority):
        rule = approved.rule
        if not approved.approver or approved.approved_digest != rule.digest:
            raise ValueError("missing or stale approval")
        if rule.identity in identities or (rule.scope, rule.priority) in priorities:
            raise ValueError("duplicate ID or same-scope priority collision")
        identities.add(rule.identity)
        priorities.add((rule.scope, rule.priority))
        matched = rule.matches(context)
        applied = matched and rule.scope not in scopes
        trace.append({"rule": rule.identity, "matched": matched, "selected": applied})
        if applied:
            scopes.add(rule.scope)
            selected.append(rule)
    actions = [action for rule in selected for action in rule.actions]
    continues = [action for action in actions if action.tier == 3]
    patches = [action for action in actions if action.tier == 2]
    result = deepcopy(output)
    order = []
    if continues:
        if continuation is None:
            raise ValueError("external continuation result callback is required")
        earliest = min((action.resume_from for action in continues), key=RESUME_ORDER.__getitem__)
        result = continuation(deepcopy(result), earliest, tuple(action.context for action in continues))
        if not isinstance(result, dict):
            raise ValueError("continuation must return a complete JSON output object")
        _json(result)
        result = deepcopy(result)
        order.append(3)
    if patches:
        if patcher is None:
            raise ValueError("external surgical patch callback is required")
        fields = tuple(dict.fromkeys(path for action in patches for path in action.target_fields))
        values = patcher(deepcopy(result), fields, tuple(action.context for action in patches))
        if not isinstance(values, dict) or set(values) != set(fields):
            raise ValueError("patch result must supply exactly the declared fields")
        for path, value in values.items():
            _edit(result, path, value)
        order.append(2)
    for action in actions:
        if action.tier == 1:
            for path, value in action.edits:
                _edit(result, path, value)
            order.append(1)
    return {"output": result, "trace": trace, "execution_order": order,
            "external_callback_calls": int(bool(continues)) + int(bool(patches)),
            "semantic_correctness_verified": False}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("Agent Gym ALF control kernel is CPU-only")
    condition = (Condition("amount", "less_than", 2000),)
    early = Rule("resume", "flow", 10, condition, (Action(3, resume_from="phase2"),))
    suppressed = Rule("suppressed", "flow", 20, condition, (Action(1, edits=(("status", "wrong"),)),))
    patch = Rule("patch", "details", 10, condition, (Action(2, target_fields=("status",)),))
    edit = Rule("edit", "final", 10, condition, (Action(1, edits=(("status", "approved-exception"),)),))
    cases = {"target": {"amount": 1000}, "other": {"amount": 3000}}
    approved = tuple(admit(rule, assess_impact(rule, cases, "target"), approver="external-SME-fixture", approve=True)
                     for rule in (early, suppressed, patch, edit))
    output = {"status": "rejected", "steps": 0}
    result = execute(output, cases["target"], approved,
                     continuation=lambda before, resume, reasons: {**before, "status": "continued", "steps": 1},
                     patcher=lambda before, fields, reasons: {"status": "patched"})
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"selected_rules": sum(row["selected"] for row in result["trace"]),
                        "external_callback_calls": result["external_callback_calls"],
                        "continuation_steps": result["output"]["steps"]},
            "checks": {"scope_mutual_exclusion": not result["trace"][3]["selected"] if len(result["trace"]) == 4 else False,
                       "three_two_one_order": result["execution_order"] == [3, 2, 1],
                       "deterministic_edit_last": result["output"]["status"] == "approved-exception",
                       "continuation_state_really_updated": result["output"]["steps"] == 1,
                       "caller_output_unchanged": output == {"status": "rejected", "steps": 0},
                       "not_a_semantic_judge": result["semantic_correctness_verified"] is False}}
