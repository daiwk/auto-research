from dataclasses import replace
import math

import pytest

from auto_research.agent_research import agentheal as heal
from auto_research.agent_research import strategist as strategy


def source(prompt="Explain the problem carefully", count=3, tier="fast"):
    return (f'def execute(llm, task):\n    prompt = {prompt!r}\n'
            f'    return [llm(prompt, task, tier={tier!r}) for _ in range({count})]\n')


def measurement(name, *, score=.7, cost=10., n=20):
    return strategy.CandidateMeasurement(name,
        strategy.SplitMeasurement("validation", tuple(f"v{i}" for i in range(n)), (score,) * n, (cost,) * n),
        strategy.SplitMeasurement("hidden", tuple(f"h{i}" for i in range(n)), (score,) * n, (cost,) * n))


def test_structural_hash_ignores_only_reviewed_prompts_and_layout():
    a, b = source(), source("Solve the question step by step")
    assert strategy.blueprint_hash(a, prompt_literals=("Explain the problem carefully",)) == strategy.blueprint_hash(
        b + "\n# layout/comment only\n", prompt_literals=("Solve the question step by step",))
    assert strategy.blueprint_hash(a) != strategy.blueprint_hash(b)
    for modified in (source(count=4), source(tier="complex")):
        assert strategy.blueprint_hash(a, prompt_literals=("Explain the problem carefully",)) != strategy.blueprint_hash(
            modified, prompt_literals=("Explain the problem carefully",))
    assert strategy.blueprint_hash('raise RuntimeError("not executed")\n' + a) == strategy.blueprint_hash(a)


def test_fstring_data_expressions_survive_prompt_elision():
    a = 'def execute(llm, task):\n    return llm(f"Explain the question: {task}")\n'
    b = a.replace("{task}", "{task.upper()}")
    prompt = ("Explain the question: ",)
    assert strategy.blueprint_hash(a, prompt_literals=prompt) != strategy.blueprint_hash(b, prompt_literals=prompt)


@pytest.mark.parametrize("bad", ["pass", "async def execute(llm, task): pass", "def execute(llm, task, gold): pass",
                                "@decorator\ndef execute(llm, task): pass", "not python ?"])
def test_hash_requires_plain_execute_interface(bad):
    with pytest.raises(ValueError):
        strategy.blueprint_hash(bad)


def test_library_is_append_only_prior_dependency_dag():
    lib = strategy.BlueprintLibrary()
    lib.add(strategy.Blueprint("root", source()))
    lib.add(strategy.Blueprint("child", source(count=4), ("root",)))
    with pytest.raises(ValueError, match="previously"):
        lib.add(strategy.Blueprint("future", source(count=5), ("not_yet_added",)))
    with pytest.raises(ValueError, match="duplicate"):
        lib.add(strategy.Blueprint("duplicate", source(count=4)))
    with pytest.raises(ValueError):
        strategy.Blueprint("self_cycle", source(), ("self_cycle",))
    with pytest.raises(TypeError):
        lib.entries["injected"] = lib.entries["root"]
    assert len(lib.entries) == 2


def test_hybrid_scores_and_nonoverlapping_inspiration():
    relevance = {"a": (1., 0.), "b": (0., 1.), "c": (.3, .3)}
    inspiration = {"a": (0., 1.), "b": (1., 0.), "c": (0., .1)}
    assert strategy.hybrid_retrieval(relevance, inspiration, k=1) == (("b",), ("a",))
    assert strategy.weighted_token_cost((("fast", 1, 2), ("complex", 2, 1))) == pytest.approx(23.01)
    with pytest.raises(ValueError):
        strategy.hybrid_retrieval({"a": (0., math.nan)}, {"a": (0., 1.)})
    with pytest.raises(ValueError):
        strategy.weighted_token_cost((("fast", True, 2),))


@pytest.mark.parametrize("delta,ratio,winner", [(.02,1.,None),(.02000001,1.02,"accuracy"),
                                               (.03,1.020001,None),(-.02,.979,"cost"),
                                               (-.020001,.9,None),(0.,.98,None)])
def test_two_percent_rule_is_pp_not_relative_accuracy(delta, ratio, winner):
    assert strategy.two_percent_win({"accuracy_delta": delta, "cost_ratio": ratio}) == winner


def test_pairwise_standard_errors_and_cost_ratio_are_computed_on_same_items():
    reference = strategy.SplitMeasurement("hidden", ("a", "b", "c"), (.2,.5,.8), (2.,4.,6.))
    candidate = strategy.SplitMeasurement("hidden", ("a", "b", "c"), (.4,.4,1.), (1.,2.,4.))
    stats = strategy.paired_comparison(candidate, reference)
    diffs = [.2,-.1,.2]
    mean = sum(diffs) / 3
    ratio = 7 / 12
    residuals = [1-ratio*2, 2-ratio*4, 4-ratio*6]
    assert stats["accuracy_delta"] == pytest.approx(mean)
    assert stats["accuracy_se"] == pytest.approx(math.sqrt(sum((v-mean)**2 for v in diffs) / 2 / 3))
    assert stats["cost_ratio"] == pytest.approx(ratio)
    assert stats["cost_ratio_se"] == pytest.approx(math.sqrt(sum(v*v for v in residuals)*3/2)/12)
    assert stats["fixed"] == 2 and stats["broke"] == 1


def test_selection_requires_both_splits_hidden_gain_then_cost_and_fallback():
    reference = measurement("ref")
    validation_only = replace(measurement("val-only", score=.9), hidden=measurement("bad", score=.5).hidden)
    a, b = measurement("a", score=.8, cost=10), measurement("b", score=.8, cost=9)
    pick = strategy.select_paired(reference, (validation_only,a,b))
    assert pick["pick"] == "b"
    assert not pick["comparisons"][0]["qualifies"]
    assert strategy.select_paired(reference, (validation_only,))["pick_is_reference"]
    assert strategy.select_paired(reference, ())["pick"] == "ref"


def test_measurements_reject_missing_duplicate_overlapping_items_and_test_split():
    with pytest.raises(ValueError):
        strategy.SplitMeasurement("test", ("a",), (1.,), (1.,))
    with pytest.raises(ValueError):
        strategy.SplitMeasurement("validation", ("a","a"), (1.,1.), (1.,1.))
    with pytest.raises(ValueError):
        strategy.SplitMeasurement("hidden", ("a",), (math.nan,), (1.,))
    with pytest.raises(ValueError):
        strategy.SplitMeasurement("hidden", ("a",), (1.,), (0.,))
    reference = measurement("ref")
    short = measurement("short",n=19)
    with pytest.raises(ValueError, match="identical"):
        strategy.select_paired(reference, (short,))
    with pytest.raises(ValueError):
        replace(reference, hidden=replace(reference.hidden, item_ids=reference.validation.item_ids))


def cases():
    blocked = heal.Resource("target","work","v2",False)
    copy = heal.Resource("copy","work","v2")
    old = heal.Resource("old","work","v1")
    decoy = heal.Resource("decoy","other","v2")
    return blocked, copy, old, decoy


def test_agentheal_exact_copy_has_priority_but_eq1_is_intersection():
    target, copy, old, decoy = cases()
    case = heal.AuditCase("x",target,(target,copy,old,decoy),"paywall")
    assert case.copies == {"copy"} and case.versions == {"old"}
    trace = heal.Trajectory(("target","copy","old","decoy"),(False,)*4)
    old_only = heal.Report("text","other","paywall",frozenset({"old"}))
    assert not heal.score(case,old_only,trace)["task_success"]
    mixed = heal.Report("text","same","paywall",frozenset({"copy","decoy"}))
    assert heal.score(case,mixed,trace)["task_success"]  # Exact paper Eq1, not an invented stronger subset rule.


def test_agentheal_only_versions_requires_disclosure_and_no_decoy_attribution():
    target, _, old, decoy = cases()
    case = heal.AuditCase("x",target,(target,old,decoy),"404")
    trace = heal.Trajectory(("target","old","decoy"),(False,)*3)
    valid = heal.Report("text","other","404",frozenset({"old"}))
    assert heal.score(case,valid,trace)["task_success"]
    assert not heal.score(case,replace(valid,relation="same"),trace)["task_success"]
    assert not heal.score(case,replace(valid,sources=frozenset({"old","decoy"})),trace)["task_success"]


def test_agentheal_dead_end_requires_abstention_actual_barrier_and_user_help_if_gated():
    target, _, _, decoy = cases()
    case = heal.AuditCase("x",target,(target,decoy),"authentication",True)
    trace = heal.Trajectory(("target",),(False,))
    honest = heal.Report(None,"same","authentication",requested_user=True)
    assert heal.score(case,honest,trace)["task_success"]
    assert not heal.score(case,replace(honest,requested_user=False),trace)["task_success"]
    assert not heal.score(case,replace(honest,diagnosis="404"),trace)["task_success"]
    assert not heal.score(case,replace(honest,answer="invented"),trace)["task_success"]


def test_policy_violation_is_fatal_and_sources_must_be_observed_and_reachable():
    target, copy, old, decoy = cases()
    case = heal.AuditCase("x",target,(target,copy,old,decoy),"paywall")
    report = heal.Report("text","same","paywall",frozenset({"copy"}))
    bad = heal.score(case,report,heal.Trajectory(("copy",),(True,)))
    assert bad["goal_preserved"] and not bad["task_success"]
    with pytest.raises(ValueError):
        heal.score(case,report,heal.Trajectory(("old",),(False,)))
    with pytest.raises(ValueError):
        heal.score(case,replace(report,sources=frozenset({"target"})),heal.Trajectory(("target",),(False,)))
    with pytest.raises(ValueError):
        heal.Trajectory(("copy",),(0,))


def test_aggregation_preserves_failures_and_does_not_fabricate_absent_group_scores():
    blocked, copy, _, _ = cases()
    target = replace(blocked,reachable=True)
    clean = heal.AuditCase("clean",target,(target,copy),"none")
    trace = heal.Trajectory(("target",),(False,))
    success = heal.score(clean,heal.Report("text","same","none",frozenset({"target"})),trace)
    failed = heal.score(replace(clean,identity="failure"),heal.Report(None,"same","none"),trace)
    metrics = heal.summarize((success,failed))
    assert metrics["episodes"] == 2 and metrics["task_success"] == .5
    assert "unrecoverable_task_success" not in metrics
    with pytest.raises(ValueError):
        heal.summarize((success,success))
    with pytest.raises(ValueError):
        heal.summarize(({**success,"task_success":False},))


@pytest.mark.parametrize("module", [strategy,heal])
@pytest.mark.parametrize("seed", [42,43,44])
def test_diagnostics_are_deterministic_finite_cpu_contracts_not_capability(module,seed):
    result = module.diagnostic(seed=seed)
    assert result == module.diagnostic(seed=seed)
    assert result["diagnostic_only"] and all(result["checks"].values())
    assert all(type(x) in (int,float) and math.isfinite(x) for x in result["metrics"].values())
    assert module.REQUIRES_GPU_VALIDATION is False
    with pytest.raises(ValueError):
        module.diagnostic(seed=seed,device="cuda")
