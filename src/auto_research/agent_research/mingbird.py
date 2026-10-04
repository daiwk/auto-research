"""Mingbird's portable M1/M3/M4/M5 mechanisms and bounded tool loop.

No shell/tool authority is supplied by this module: callers register executors.
The original Windows GUI, speech and system-operation guards are out of scope.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
import json
from typing import Callable, Mapping


def flat_prefill(tools: Mapping[str, dict], *, domain: str, budget_bytes: int) -> str:
    """Route domains and flatten schemas, retaining all required parameters."""
    if budget_bytes < 1:
        raise ValueError("budget must be positive")
    rows = []
    for name, tool in tools.items():
        if domain not in tool.get("domains", ()):
            continue
        parameters = tool.get("parameters", {})
        required = set(tool.get("required", ()))
        if not required <= parameters.keys():
            raise ValueError("required parameter missing from schema")
        chosen = (
            parameters
            if len(parameters) <= 8
            else {k: v for k, v in parameters.items() if k in required}
        )
        rows.append(
            name
            + ": "
            + json.dumps(chosen, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        )
    result = "\n".join(rows)
    if len(result.encode("utf-8")) > budget_bytes:
        raise ValueError("prefill byte budget exceeded; re-route or compress tool definitions")
    return result


@dataclass
class LoopMonitor:
    identical_limit: int = 6
    no_output_limit: int = 15
    counts: Counter = field(default_factory=Counter)
    no_output: int = 0

    def record(self, tool: str, arguments: Mapping, *, produced_output: bool) -> str | None:
        if self.identical_limit < 1 or self.no_output_limit < 1:
            raise ValueError("loop limits must be positive")
        signature = tool + json.dumps(
            arguments, sort_keys=True, ensure_ascii=False, separators=(",", ":")
        )
        self.counts[signature] += 1
        self.no_output = 0 if produced_output else self.no_output + 1
        if self.counts[signature] >= self.identical_limit:
            return "repeated-call: revise tool arguments or the plan"
        if self.no_output >= self.no_output_limit:
            return "no-output: re-read the task and choose a different action"
        return None


def rescue_tool_call(text: str, allowed_tools: set[str]) -> dict:
    """Decode bounded JSON/plain-text JSON or doubly quoted JSON, never eval."""
    candidate = text.strip()
    if candidate.startswith("```json") and candidate.endswith("```"):
        candidate = candidate[7:-3].strip()
    try:
        value = json.loads(candidate)
        if isinstance(value, str):
            value = json.loads(value)
    except (ValueError, TypeError) as exc:
        raise ValueError("unrecognized tool-call structure") from exc
    if not isinstance(value, dict) or set(value) != {"tool", "arguments"}:
        raise ValueError("expected tool and arguments fields")
    if (
        not isinstance(value["tool"], str)
        or value["tool"] not in allowed_tools
        or not isinstance(value["arguments"], dict)
    ):
        raise ValueError("unknown tool or malformed arguments")
    return value


def finish_gate(task: str, plan: str, checks: Mapping[str, Callable[[], bool]]) -> dict:
    """Reinject original criteria and actual check failures on every finish."""
    if not task.strip() or not checks:
        raise ValueError("task and executable acceptance checks are required")
    failures = []
    for name, check in checks.items():
        try:
            if not check():
                failures.append(name + ": acceptance check failed")
        except Exception as exc:
            failures.append(name + ": " + type(exc).__name__ + ": " + str(exc))
    return {
        "complete": not failures,
        "task": task,
        "plan": plan,
        "failures": failures,
        "next_action": "repair the failed acceptance checks" if failures else "finish",
    }


def run_task(
    policy, tools: Mapping[str, Callable], checks, *, task: str, plan: str = "", max_turns: int = 30
) -> dict:
    """Execute structured calls and feed verified failures back to the policy.

    Acceptance checks stay outside policy input until a finish request. Trace
    records effects and feedback; it never treats a completion claim as proof.
    """
    if max_turns < 1:
        raise ValueError("max_turns must be positive")
    monitor, trace = LoopMonitor(), []
    for _ in range(max_turns):
        action = policy({"task": task, "plan": plan, "trace": list(trace)})
        if action == "finish":
            verdict = finish_gate(task, plan, checks)
            trace.append({"kind": "finish", **verdict})
            if verdict["complete"]:
                return {"complete": True, "trace": trace}
            continue
        try:
            call = rescue_tool_call(action, set(tools))
            # Check the signature before executing a repeated operation.
            previous_no_output = monitor.no_output
            hint = monitor.record(call["tool"], call["arguments"], produced_output=True)
            monitor.no_output = previous_no_output
            if hint:
                trace.append({"kind": "correction", "message": hint})
                continue
            output = tools[call["tool"]](**call["arguments"])
            if output is not None and str(output):
                monitor.no_output = 0
            else:
                monitor.no_output += 1
            trace.append({"kind": "tool", **call, "output": str(output)})
        except Exception as exc:
            monitor.no_output += 1
            trace.append({"kind": "error", "message": type(exc).__name__ + ": " + str(exc)})
        if monitor.no_output >= monitor.no_output_limit:
            trace.append(
                {
                    "kind": "correction",
                    "message": "no-output: re-read the task and choose a different action",
                }
            )
            # A correction starts a new observation window. Otherwise every
            # future action would be blocked before it could produce output.
            monitor.no_output = 0
    return {"complete": False, "trace": trace, "reason": "turn budget exhausted"}
