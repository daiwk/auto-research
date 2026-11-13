"""DS-STAR v1 routing/verification control, without a data-science actor.

Planner, coder/executor, semantic verifier and router are trusted external
callbacks. References below are not code execution or evidence certification.
The narrow local router uses zero-based indices; presentation prompts use Step 1.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import random
from typing import Literal

REQUIRES_GPU_VALIDATION = False


def _text(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"nonempty {label} required")
    return value


def _texts(values: Sequence[str], label: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise ValueError(f"explicit {label} sequence required")
    return tuple(_text(value, label) for value in values)


@dataclass(frozen=True)
class Execution:
    code_ref: str
    output_ref: str

    def __post_init__(self):
        _text(self.code_ref, "external code reference")
        _text(self.output_ref, "external execution-output reference")


@dataclass(frozen=True)
class PlanContext:
    query: str
    descriptions: tuple[str, ...]
    plan: tuple[str, ...]
    previous_execution: Execution | None

    def __post_init__(self):
        _text(self.query, "query")
        object.__setattr__(self, "descriptions", _texts(self.descriptions, "description"))
        object.__setattr__(self, "plan", _texts(self.plan, "plan step"))
        if self.previous_execution is not None and not isinstance(self.previous_execution, Execution):
            raise ValueError("typed previous external execution required")


@dataclass(frozen=True)
class State:
    query: str
    descriptions: tuple[str, ...]
    plan: tuple[str, ...]
    execution: Execution

    def __post_init__(self):
        context = PlanContext(self.query, self.descriptions, self.plan, None)
        object.__setattr__(self, "descriptions", context.descriptions)
        object.__setattr__(self, "plan", context.plan)
        if not self.plan or not isinstance(self.execution, Execution):
            raise ValueError("nonempty plan and typed external execution required")


@dataclass(frozen=True)
class Verification:
    sufficient: bool
    reason: str

    def __post_init__(self):
        if type(self.sufficient) is not bool:
            raise ValueError("explicit semantic sufficiency boolean required")
        _text(self.reason, "verification reason")


@dataclass(frozen=True)
class Route:
    action: Literal["add", "backtrack"]
    index: int | None = None

    def __post_init__(self):
        if self.action not in ("add", "backtrack"):
            raise ValueError("route must add or backtrack")
        if self.action == "add" and self.index is not None:
            raise ValueError("add route has no index")
        if self.action == "backtrack" and (type(self.index) is not int or self.index < 0):
            raise ValueError("backtrack requires a zero-based nonnegative index")


@dataclass(frozen=True)
class Observation:
    state: State
    verification: Verification


@dataclass(frozen=True)
class Result:
    state: State
    status: Literal["sufficient", "exhausted_unverified"]
    observations: tuple[Observation, ...]
    execution_calls: int
    routing_calls: int


def refine_plan(state: State, decision: Route,
                planner: Callable[[PlanContext], str]) -> tuple[str, ...]:
    """Remove the named step AND its suffix, or keep all, then append one step.

    As in Section 3.2 the planner sees the *last* output, even after truncation.
    This does not assert that that output belongs to the retained prefix.
    """
    if not isinstance(state, State) or not isinstance(decision, Route):
        raise ValueError("typed state and route required")
    if decision.action == "backtrack":
        if decision.index >= len(state.plan):
            raise ValueError("backtrack index outside current plan")
        prefix = state.plan[:decision.index]
    else:
        prefix = state.plan
    context = PlanContext(state.query, state.descriptions, prefix, state.execution)
    return prefix + (_text(planner(context), "external proposed step"),)


def run_plan(*, query: str, descriptions: Sequence[str],
             planner: Callable[[PlanContext], str],
             execute: Callable[[PlanContext], Execution],
             verifier: Callable[[State], Verification],
             router: Callable[[State], Route],
             max_verifications: int = 20) -> Result:
    """Execute Algorithm 1's bounded control with all semantic work external.

    There is one initial execution. Each insufficient verdict, including the
    final budgeted verdict, routes, proposes, and executes once more. The final
    unverified result is preserved but NEVER labelled sufficient. No gold input,
    file reader, Python executor, debugger, finalizer or sandbox is implemented.
    """
    if type(max_verifications) is not int or max_verifications < 0:
        raise ValueError("nonnegative integer verification budget required")
    if not all(callable(callback) for callback in (planner, execute, verifier, router)):
        raise ValueError("trusted external callable components required")
    initial = PlanContext(query, _texts(descriptions, "description"), (), None)
    plan = (_text(planner(initial), "external proposed step"),)

    def implement(steps, previous):
        result = execute(PlanContext(initial.query, initial.descriptions, steps, previous))
        if not isinstance(result, Execution):
            raise ValueError("executor must return a typed external Execution")
        return State(initial.query, initial.descriptions, steps, result)

    state = implement(plan, None)
    observations: list[Observation] = []
    for _ in range(max_verifications):
        verdict = verifier(state)
        if not isinstance(verdict, Verification):
            raise ValueError("verifier must return a typed Verification")
        observations.append(Observation(state, verdict))
        if verdict.sufficient:
            return Result(state, "sufficient", tuple(observations), len(observations), len(observations)-1)
        decision = router(state)
        steps = refine_plan(state, decision, planner)
        state = implement(steps, state.execution)
    return Result(state, "exhausted_unverified", tuple(observations), max_verifications+1, max_verifications)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Fixed routing truth tables only; seed permutes cases, not actor outcomes."""
    if type(seed) is not int:
        raise ValueError("integer seed required")
    if device != "cpu":
        raise ValueError("DS-STAR control diagnostic is CPU-only")
    initial = State("fixture query", ("external schema reference",),
                    ("load", "wrong join", "aggregate"), Execution("code-old", "output-old"))
    seen = []

    def propose(context):
        seen.append(context)
        return "replacement" if context.plan == ("load",) else "next"

    cases = [Route("backtrack", 1), Route("add"), Route("backtrack", 0)]
    random.Random(seed).shuffle(cases)
    outputs = {route.action + str(route.index): refine_plan(initial, route, propose) for route in cases}
    calls = []

    def execute(context):
        calls.append(context)
        return Execution(f"code-{len(calls)}", f"output-{len(calls)}")

    run = run_plan(query="fixture query", descriptions=("schema reference",),
                   planner=lambda context: "load" if not context.plan else "next",
                   execute=execute,
                   verifier=lambda state: Verification(len(state.plan) == 2, "fixed truth table"),
                   router=lambda state: Route("add"), max_verifications=3)
    exhausted = run_plan(query="fixture", descriptions=(), planner=lambda context: "step",
                        execute=lambda context: Execution("code", "output"),
                        verifier=lambda state: Verification(False, "fixed insufficient"),
                        router=lambda state: Route("add"), max_verifications=1)
    checks = {
        "backtrack_removes_error_and_suffix": outputs["backtrack1"] == ("load", "replacement"),
        "add_keeps_existing_prefix": outputs["addNone"] == initial.plan + ("next",),
        "first_step_can_be_replaced": outputs["backtrack0"] == ("next",),
        "last_output_preserved_for_planner": all(context.previous_execution == initial.execution for context in seen),
        "explicit_verifier_stops_before_router": run.status == "sufficient" and run.routing_calls == 1,
        "coder_receives_previous_code_reference": calls[1].previous_execution == Execution("code-1", "output-1"),
        "budget_end_not_capability_success": exhausted.status == "exhausted_unverified" and exhausted.execution_calls == 2,
    }
    return {"seed":seed, "diagnostic_only":True, "evaluation_tier":"l1_mechanism",
            "checks":checks, "metrics":{"control_checks":len(checks), "verified_rounds":len(run.observations),
                                       "routing_calls":run.routing_calls, "budgeted_unverified_executions":1}}
