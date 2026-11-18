"""Bounded verified-repair and fail-closed deploy-gate protocol for ProdPilot.

Callbacks operate on in-memory project files, not real clouds. No claim is made
to implement the paper's 50-rule JavaScript checker catalog or trained model.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False
Project = Mapping[str, str]


@dataclass(frozen=True)
class Rule:
    key: str
    priority: int
    fix_type: str
    allowed_files: tuple[str, ...]
    check: Callable[[Project], bool | None]
    fix: Callable[[Project], Project] | None = None

    def __post_init__(self) -> None:
        if (not self.key or type(self.priority) is not int or not 0 <= self.priority <= 5
                or self.fix_type not in {"static", "parametric", "delegated"}):
            raise ValueError("invalid rule contract")
        if len(set(self.allowed_files)) != len(self.allowed_files):
            raise ValueError("duplicate allowed files")


def _project(project: Project) -> dict[str, str]:
    if not isinstance(project, Mapping) or any(not isinstance(k, str) or not isinstance(v, str)
                                              for k, v in project.items()):
        raise TypeError("project must map filenames to text")
    return dict(project)


def audit(project: Project, rules: Sequence[Rule]) -> dict[str, str]:
    if not rules or len({r.key for r in rules}) != len(rules):
        raise ValueError("nonempty unique rule ids required")
    results = {}
    for rule in rules:
        try:
            value = rule.check(_project(project))
            results[rule.key] = "na" if value is None else "pass" if value is True else "fail"
            if value is not None and type(value) is not bool:
                results[rule.key] = "error"
        except Exception:
            results[rule.key] = "error"
    return results


def audit_score(results: Mapping[str, str], rules: Sequence[Rule]) -> float:
    applicable = [r for r in rules if results[r.key] != "na"]
    total = sum(2 ** (5 - r.priority) for r in applicable)
    return 100 * sum(2 ** (5 - r.priority) for r in applicable
                     if results[r.key] == "pass") / total if total else 0.0


def repair(project: Project, rules: Sequence[Rule], *, max_attempts: int = 3,
           max_cycles: int = 5) -> dict:
    if (type(max_attempts) is not int or not 1 <= max_attempts <= 3
            or type(max_cycles) is not int or not 1 <= max_cycles <= 5):
        raise ValueError("at most three attempts per issue and five cycles")
    current = _project(project)
    states = audit(current, rules)
    attempts = {r.key: 0 for r in rules}
    manual: set[str] = set()
    events = []
    for cycle in range(max_cycles):
        pending = [r for r in sorted(rules, key=lambda r: (r.priority, r.key))
                   if states[r.key] not in {"pass", "na"} and r.key not in manual]
        if not pending:
            break
        for rule in pending:
            if states[rule.key] in {"pass", "na"}:
                continue
            if rule.fix is None:
                manual.add(rule.key)
                events.append({"rule": rule.key, "cycle": cycle, "event": "manual_no_executor",
                               "callback_executed": False})
                continue
            while attempts[rule.key] < max_attempts:
                before, old_states = dict(current), dict(states)
                attempts[rule.key] += 1
                event = {"rule": rule.key, "cycle": cycle, "fix_type": rule.fix_type,
                         "attempt": attempts[rule.key], "callback_executed": True}
                try:
                    proposed = _project(rule.fix(dict(before)))
                    changed = {key for key in set(before) | set(proposed)
                               if before.get(key) != proposed.get(key)}
                    if not changed <= set(rule.allowed_files):
                        raise PermissionError("fix exceeded declared file boundary")
                    new_states = audit(proposed, rules)
                    regressions = [key for key, state in old_states.items()
                                   if state == "pass" and new_states[key] != "pass"]
                    if regressions:
                        event.update(event="reverted_regression", regressions=regressions)
                        manual.add(rule.key)
                    elif new_states[rule.key] != "pass":
                        event.update(event="rejected_checker")
                    else:
                        current, states = proposed, new_states
                        event.update(event="accepted")
                except Exception as error:
                    event.update(event="rejected_exception", error_type=type(error).__name__)
                events.append(event)
                if event["event"] == "accepted" or rule.key in manual:
                    break
            if states[rule.key] != "pass":
                manual.add(rule.key)
        states = audit(current, rules)
    return {"project": current, "audit": states, "score": audit_score(states, rules),
            "manual_review": sorted(manual), "events": events, "attempts": attempts}


def deploy_gate(project: Project, rules: Sequence[Rule], *,
                probability: float | None, build_determined: bool) -> dict:
    states = audit(project, rules)  # A fresh audit, never trust the repair log.
    score = audit_score(states, rules)
    if any(r.priority == 0 and states[r.key] not in {"pass", "na"} for r in rules):
        reason = "critical_rule"
    elif score < 90:
        reason = "audit_score"
    elif build_determined is not True:
        reason = "undetermined_build"
    elif (isinstance(probability, bool) or not isinstance(probability, (int, float))
          or not math.isfinite(probability) or not 0 <= probability <= 1):
        reason = "missing_model_input"
    elif probability < 0.369:
        reason = "deployability_probability"
    else:
        reason = "accepted"
    return {"allowed": reason == "accepted", "reason": reason, "audit": states, "score": score}


def gated_deploy(gate: Mapping, *, approved: bool, deploy: Callable[[], object],
                 smoke: Callable[[object], bool]) -> dict:
    """An explicit local callback interface, not Render/GitHub integration."""
    events = []
    if gate.get("allowed") is not True or approved is not True:
        return {"deployed": False, "verified": False, "events": events}
    try:
        events.append("deploy_called")
        handle = deploy()
        events.append("smoke_called")
        verified = smoke(handle) is True
        return {"deployed": True, "verified": verified, "events": events}
    except Exception as error:
        return {"deployed": True if "smoke_called" in events else None,
                "deployment_status": "returned" if "smoke_called" in events else "unknown",
                "verified": False,
                "events": events, "error_type": type(error).__name__}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU protocol only")
    calls = []

    def fix(project: Project) -> Project:
        calls.append("fix")
        return {**project, "health": "ok"}

    rule = Rule("health", 0, "static", ("health",), lambda p: p.get("health") == "ok", fix)
    result = repair({}, [rule])
    refused = deploy_gate({}, [rule], probability=1.0, build_determined=True)
    gate = deploy_gate(result["project"], [rule], probability=0.8, build_determined=True)
    attempted = []

    def deploy() -> str:
        attempted.append("local_handle")
        return "local_handle"

    denied = gated_deploy(refused, approved=True, deploy=deploy, smoke=lambda x: True)
    done = gated_deploy(gate, approved=True, deploy=deploy, smoke=lambda x: x == "local_handle")
    guard = Rule("guard", 0, "static", ("guard",), lambda p: p.get("guard") == "ok")
    bad = Rule("new", 1, "delegated", ("new", "guard"), lambda p: p.get("new") == "ok",
               lambda p: {**p, "new": "ok", "guard": "bad"})
    regression = repair({"guard": "ok"}, [guard, bad])
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"checker_accepts_actual_edit": result["audit"]["health"] == "pass"
                       and calls == ["fix"],
                       "critical_gate_not_overridden": not refused["allowed"],
                       "regression_rolled_back": regression["project"] == {"guard": "ok"}
                       and regression["events"][0]["event"] == "reverted_regression",
                       "callback_only_after_gate": not denied["deployed"] and attempted == ["local_handle"],
                       "smoke_not_deploy_claim": done["verified"]},
            "metrics": {"repair_callbacks": len(calls), "deploy_callbacks": len(attempted),
                        "audit_score": result["score"], "rolled_back_changes": len(regression["events"])}}
