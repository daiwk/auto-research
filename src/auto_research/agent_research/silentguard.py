"""SilentGuard exact filtered-count enforcement and cutoff (§3/Appendix B).

No model, network or repair is embedded. The count API callback is genuinely
invoked; a consistent lie can satisfy all equations and is not detectable here.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Condition:
    field: str
    value: str
    negated: bool = False

    def __post_init__(self):
        if not self.field or not isinstance(self.value, str) or type(self.negated) is not bool:
            raise ValueError("typed filter condition required")


def count_identity(
    query: tuple[Condition, ...], count: int, execute: Callable[[tuple[Condition, ...]], dict]
) -> bool:
    if type(count) is not int or count < 0:
        return False
    for i, condition in enumerate(query):
        other = query[:i] + query[i + 1 :]
        complement = other + (Condition(condition.field, condition.value, not condition.negated),)
        total, missing = execute(other), execute(complement)
        if total.get("error") or missing.get("error"):
            return False
        t, m = total.get("total_count"), missing.get("total_count")
        if type(t) is not int or type(m) is not int or min(t, m) < 0 or count + m != t:
            return False
    return True


def action_for_checks(checks: tuple[tuple[bool, int | None], ...], cutoff: float = 0.01) -> str:
    """None clean-count denotes an exact invariant; n observations gives1/(n+2)."""
    if not math.isfinite(cutoff) or not 0 < cutoff < 1:
        raise ValueError("cutoff in (0,1) required")
    for passed, n in checks:
        if type(passed) is not bool or (n is not None and (type(n) is not int or n < 0)):
            raise ValueError("strict check verdict and nonnegative clean sample count required")
    failed = [(0.0 if n is None else 1 / (n + 2)) for passed, n in checks if not passed]
    return "release" if not failed else "withhold" if min(failed) <= cutoff else "warn"


def guarded_count(
    query: tuple[Condition, ...],
    execute: Callable[[tuple[Condition, ...]], dict],
    *,
    documented_parameters: frozenset[str] | None = None,
) -> dict:
    if not isinstance(query, tuple) or any(not isinstance(x, Condition) for x in query):
        raise TypeError("immutable typed query required")
    if documented_parameters is not None and any(
        x.field not in documented_parameters for x in query
    ):
        return {
            "action": "reject_request",
            "response": {"error": "unknown_parameter"},
            "attempts": 0,
        }
    for attempt in (1, 2):
        response = execute(query)
        if not isinstance(response, dict):
            raise TypeError("API callback must return response mapping")
        if response.get("error"):
            return {"action": "passthrough_error", "response": dict(response), "attempts": attempt}
        if count_identity(query, response.get("total_count"), execute):
            return {"action": "release", "response": dict(response), "attempts": attempt}
    sanitized = {k: v for k, v in response.items() if k != "total_count"}
    sanitized["verification"] = "count withheld after exact consistency failure twice; do not guess"
    return {"action": "withhold", "response": sanitized, "attempts": 2}


class AnswerGate:
    """Paper's count provenance rule and bounded rejection, not an answer generator."""

    def __init__(self):
        self.max_conditions = 0
        self.verified: list[tuple[int, int]] = []
        self.rejections = 0

    def observe(self, query: tuple[Condition, ...], result: dict):
        self.max_conditions = max(self.max_conditions, len(query))
        if result["action"] == "release":
            self.verified.append((len(query), result["response"]["total_count"]))

    def submit(self, count: int) -> str:
        if type(count) is int and any(
            n >= self.max_conditions and c == count for n, c in self.verified
        ):
            return "accept"
        if self.rejections >= 2:
            return "abstain"
        self.rejections += 1
        return "reject"


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    records = ({"a": "x", "b": "y"}, {"a": "z", "b": "y"}, {"a": "x", "b": "n"})
    calls = []

    def api(query):
        calls.append(query)
        return {
            "total_count": sum(
                all((row[c.field] == c.value) != c.negated for c in query) for row in records
            )
        }

    q = (Condition("a", "x"), Condition("b", "y"))
    clean = guarded_count(q, api)

    def faulty(query):
        result = api(query)
        if query == q:
            result["total_count"] = 90
        return result

    fault = guarded_count(q, faulty)
    gate = AnswerGate()
    gate.observe(q, fault)
    verdicts = [gate.submit(90) for _ in range(3)]
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "clean_released": clean["action"] == "release",
            "fault_retried_once": fault["attempts"] == 2,
            "failed_count_unavailable": "total_count" not in fault["response"],
            "answer_gate_abstains": verdicts == ["reject", "reject", "abstain"],
            "weak_learned_warns": action_for_checks(((False, 3),)) == "warn",
            "cutoff_inclusive": action_for_checks(((False, 98),)) == "withhold",
        },
        "metrics": {
            "actual_api_callbacks": len(calls),
            "fault_attempts": fault["attempts"],
            "clean_count": clean["response"]["total_count"],
        },
    }
