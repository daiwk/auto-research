from __future__ import annotations

import pytest

from auto_research.agent_research.ds_star import (
    Execution, PlanContext, Route, State, Verification, diagnostic, refine_plan, run_plan,
)


def state():
    return State("query", ("schema",), ("load", "bad join", "sum"), Execution("old-code", "old-output"))


@pytest.mark.parametrize("index,prefix", [(0, ()), (1, ("load",)), (2, ("load", "bad join"))])
def test_backtrack_removes_selected_step_and_all_dependants(index, prefix):
    seen = []
    def propose(context):
        seen.append(context)
        return "regenerated"
    assert refine_plan(state(), Route("backtrack", index), propose) == prefix + ("regenerated",)
    assert seen[0].plan == prefix
    assert seen[0].previous_execution == state().execution
    assert seen[0].descriptions == ("schema",)


def test_add_preserves_complete_plan_and_one_new_step():
    assert refine_plan(state(), Route("add"), lambda context: "print") == state().plan + ("print",)


@pytest.mark.parametrize("route", [Route("backtrack", 3), Route("backtrack", 100)])
def test_backtrack_out_of_bounds_never_calls_planner(route):
    with pytest.raises(ValueError, match="outside"):
        refine_plan(state(), route, lambda context: pytest.fail("must not plan"))


@pytest.mark.parametrize("action,index", [("add", 0), ("replace", None), ("backtrack", None), ("backtrack", True), ("backtrack", -1)])
def test_invalid_route_types(action, index):
    with pytest.raises(ValueError):
        Route(action, index)


def test_success_stops_without_router_or_further_generation():
    result = run_plan(query="q", descriptions=["d"], planner=lambda c: "load",
                      execute=lambda c: Execution("code", "output"),
                      verifier=lambda s: Verification(True, "external judgment"),
                      router=lambda s: pytest.fail("sufficient cannot route"), max_verifications=5)
    assert result.status == "sufficient"
    assert result.execution_calls == 1 and result.routing_calls == 0


def test_actual_callback_flow_retains_last_output_after_backtracking():
    planning, coding, verified = [], [], []
    steps = iter(["load", "bad join", "revised load"])
    def planner(context):
        planning.append(context)
        return next(steps)
    def execute(context):
        coding.append(context)
        return Execution(f"code-{len(coding)}", f"output-{len(coding)}")
    def verify(current):
        verified.append(current)
        return Verification(len(verified) == 3, "external sufficiency")
    routes = iter([Route("add"), Route("backtrack", 0)])
    result = run_plan(query="q", descriptions=["schema"], planner=planner,
                      execute=execute, verifier=verify, router=lambda s: next(routes), max_verifications=3)
    assert result.state.plan == ("revised load",)
    assert planning[-1].plan == ()
    assert planning[-1].previous_execution == Execution("code-2", "output-2")
    assert coding[-1].previous_execution == Execution("code-2", "output-2")
    assert result.status == "sufficient"
    assert result.execution_calls == 3 and result.routing_calls == 2


@pytest.mark.parametrize("budget", [0, 1, 3])
def test_algorithm_one_final_result_is_unverified_when_budget_expires(budget):
    result = run_plan(query="q", descriptions=(), planner=lambda c: "step",
                      execute=lambda c: Execution("code", "output"),
                      verifier=lambda s: Verification(False, "external insufficient"),
                      router=lambda s: Route("add"), max_verifications=budget)
    assert result.status == "exhausted_unverified"
    assert len(result.observations) == budget
    assert result.execution_calls == budget + 1
    assert result.routing_calls == budget
    assert len(result.state.plan) == budget + 1


def test_executor_is_external_and_its_exception_is_not_fabricated_as_a_result():
    def fail(context):
        raise RuntimeError("real external failure")
    with pytest.raises(RuntimeError, match="real external failure"):
        run_plan(query="q", descriptions=(), planner=lambda c: "step", execute=fail,
                 verifier=lambda s: Verification(True, "unused"), router=lambda s: Route("add"))


@pytest.mark.parametrize("kind", ["executor", "verifier", "planner", "router"])
def test_untyped_external_output_is_rejected(kind):
    callbacks = {"planner": lambda c: "step", "execute": lambda c: Execution("code", "output"),
                 "verifier": lambda s: Verification(False, "insufficient"), "router": lambda s: Route("add")}
    key = "execute" if kind == "executor" else kind
    callbacks[key] = lambda c: True
    with pytest.raises(ValueError):
        run_plan(query="q", descriptions=(), max_verifications=1, **callbacks)


@pytest.mark.parametrize("budget", [True, -1, 1.5])
def test_invalid_budget_rejected_before_callbacks(budget):
    with pytest.raises(ValueError, match="budget"):
        run_plan(query="q", descriptions=(), planner=lambda c: "step",
                 execute=lambda c: Execution("c", "o"), verifier=lambda s: Verification(True, "yes"),
                 router=lambda s: Route("add"), max_verifications=budget)


def test_references_and_semantic_decisions_are_explicitly_typed():
    with pytest.raises(ValueError):
        Execution("", "output")
    with pytest.raises(ValueError):
        Verification(1, "not explicit bool")
    with pytest.raises(ValueError):
        PlanContext("q", "not a sequence of descriptions", (), None)
    with pytest.raises(ValueError):
        State("q", (), (), Execution("code", "output"))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_only_a_control_truth_table(seed):
    result = diagnostic(seed)
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(result["checks"].values())
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, "cuda")
