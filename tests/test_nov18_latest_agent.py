"""Primary-equation controls; these are not agent benchmark scores."""

import importlib
import math

import pytest

from auto_research.agent_research.detourbench import Action, FiniteTask, State, access_budget
from auto_research.agent_research.sciresearch_eval import interval_score, parameter_score
from auto_research.agent_research.resolution_hypothesis import variance_components
from auto_research.agent_research.elite_eval_free import generation
from auto_research.agent_research.silentguard import (
    Condition,
    guarded_count,
    action_for_checks,
    AnswerGate,
)
from auto_research.agent_research.metaact import (
    Spec,
    View,
    Event,
    Episode,
    compile_guards,
    replay_report,
)


def task():
    return FiniteTask(
        (
            Action("r", "s", reveals=frozenset({"e"}), grants=frozenset({"c"})),
            Action(
                "end",
                "s",
                requires=frozenset({"e"}),
                credentials=frozenset({"c"}),
                terminal="success",
            ),
            Action("bad", "s", terminal="wrong"),
        ),
        State(frozenset({"s"})),
    )


def test_detour_exact_witness_residual_batch_charge_and_irreversible_failure():
    t = task()
    assert t.shortest() == (2, ("r", "end"))
    run = t.replay((("invalid", "end", "r"), ("r", "end", "bad")), budget=9)
    assert run["cost"] == 5 and run["invalid"] == 2 and run["duplicate"] == 1
    m = t.metrics(run)
    assert m["attainment"] == 0.4 and m["normalized_detour"] == 1.5
    assert m["redundant_ratio"] == 0.6
    partial = t.metrics(t.replay((("r",),), budget=1))
    assert partial["progress"] == 0.5 and partial["normalized_detour"] == 0
    wrong = t.metrics(t.replay((("bad", "r"),), budget=2))
    assert wrong["irreversible_failure"]
    assert all(
        wrong[k] is None for k in ("residual", "progress", "normalized_detour", "attainment")
    )
    assert access_budget(2, 5) == 8
    with pytest.raises(RuntimeError):
        t.shortest(max_states=1)
    with pytest.raises(ValueError):
        t.step(run["state"], "r")
    for x in (True, 0, float("nan")):
        with pytest.raises(ValueError):
            access_budget(2, 5, x)


def test_scientific_proper_score_units_noncoverage_and_invalid_intervals():
    assert interval_score(3, 0, 1) == 81
    assert interval_score(-1, 0, 1) == 41
    assert parameter_score({"k": (1, 10)}, {"k": 100})["parameter_coverage"] == 0
    assert parameter_score({"k": (1, 10)}, {"k": 100})["mean_parameter_interval_score"] == 41
    for prediction in [(0, 1), (2, 1), (1, float("nan")), (True, 1)]:
        with pytest.raises(ValueError):
            parameter_score({"k": prediction}, {"k": 1})
    with pytest.raises(ValueError):
        parameter_score({}, {"k": 1})


def test_resolution_balanced_independent_artifacts_and_unbiased_negative_component():
    r = variance_components([[0, 1], [0, 1]])
    assert r["run_variance_unbiased"] == -0.25 and r["run_sd"] == 0
    assert variance_components([[1, 1], [3, 3]])["run_variance_unbiased"] == 2
    for scores in ([[1]], [[1, 2], [3]], [[0, True], [0, 1]], [[0, math.inf], [0, 1]]):
        with pytest.raises(ValueError):
            variance_components(scores)


def test_elite_same_parent_real_callbacks_scope_strict_gate_and_acceptance_rollback():
    base = {"a.py": "x=0"}
    seen, requests = [], []

    def explore(parent, h):
        seen.append(dict(parent))
        with pytest.raises(TypeError):
            parent["a.py"] = "mutation"
        return {"a.py": parent["a.py"] + "\n" + h}

    def integrate(req):
        requests.append(req)
        return {"a.py": req.parent["a.py"] + "\ny=1"}

    args = dict(
        explore=explore,
        exploration_gate=lambda _: True,
        integrate=integrate,
        acceptance_gate=lambda _: True,
        allowed_paths=frozenset({"a.py"}),
    )
    result = generation(base, ("one", "two"), **args)
    assert result["accepted"] and seen == [base, base]
    assert dict(result["files"]) == {"a.py": "x=0\ny=1"}
    assert set(vars(requests[0])) == {"parent", "children"}
    args["acceptance_gate"] = lambda _: 1
    assert dict(generation(base, ("one",), **args)["files"]) == base
    args["explore"] = lambda p, h: {**p, "secret.py": "x=1"}
    assert generation(base, ("one",), **args)["valid_children"] == 0


def test_silentguard_retry_withhold_unknown_parameter_and_consistent_lie_limit():
    q = (Condition("a", "x"),)
    calls = []

    def fault(query):
        calls.append(query)
        return {"total_count": 10 if query == q else 0}

    r = guarded_count(q, fault)
    assert r["action"] == "withhold" and r["attempts"] == 2
    assert "total_count" not in r["response"]
    before = len(calls)
    assert guarded_count(q, fault, documented_parameters=frozenset({"other"}))["attempts"] == 0
    assert len(calls) == before
    # All-zero lies are algebraically consistent; do not claim universal detection.
    assert guarded_count(q, lambda _: {"total_count": 0})["action"] == "release"
    assert action_for_checks(((False, 97),)) == "warn"
    assert action_for_checks(((False, 98),)) == "withhold"
    assert action_for_checks(((False, None),)) == "withhold"
    assert guarded_count(q, lambda _: {"error": "503"})["action"] == "passthrough_error"


def test_silentguard_looser_verified_query_cannot_back_full_filter_answer():
    gate = AnswerGate()
    gate.observe((), {"action": "release", "response": {"total_count": 5}})
    gate.observe((Condition("a", "x"),), {"action": "withhold", "response": {}})
    assert [gate.submit(5) for _ in range(3)] == ["reject", "reject", "abstain"]


def test_metaact_effective_denominator_safe_trajectory_and_unknown_spec_rejected():
    rule = Spec("no_op_repeat", "replan")
    still = View((("look", "same"), ("look", "same")))
    failed = Episode((Event("look", still, False, True), Event("good", View(), True)), False, 0.8)
    success = Episode((Event("good", View(), True),), True, 1)
    report = replay_report((rule,), (failed, success), minimum_reference_score=0.5)
    assert report["accepted"] and report["effective_block_rate"] == 0
    unsafe = Episode((Event("look", still, True),), True, 1)
    report = replay_report((rule,), (failed, unsafe), minimum_reference_score=0.5)
    assert not report["accepted"] and report["success_block_rate"] == 1
    assert not compile_guards((Spec("idempotence_block", "already done"),))(
        View(done_options=frozenset({"red"})), "click[red]"
    )
    with pytest.raises(ValueError):
        Spec("unknown", "not silently ignored")
    with pytest.raises(ValueError):
        replay_report((rule,), (failed,), minimum_reference_score=0.5)


@pytest.mark.parametrize(
    "name",
    [
        "detourbench",
        "sciresearch_eval",
        "resolution_hypothesis",
        "elite_eval_free",
        "silentguard",
        "metaact",
    ],
)
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_exact_cpu_diagnostic_contract(name, seed):
    module = importlib.import_module("auto_research.agent_research." + name)
    result = module.diagnostic(seed)
    assert module.REQUIRES_GPU_VALIDATION is False and result["seed"] == seed
    assert result["diagnostic_only"] is True
    assert all(type(x) is bool and x for x in result["checks"].values())
    assert all(
        isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
        for x in result["metrics"].values()
    )
    with pytest.raises(ValueError):
        module.diagnostic(True)
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")
