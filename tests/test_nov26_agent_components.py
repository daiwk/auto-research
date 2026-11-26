"""Formula, sampling, reuse and L0 memory-contract controls, not agent scores."""

from dataclasses import FrozenInstanceError, replace
import math

import pytest

from auto_research.agent_research import dualpm, home


def test_home_ema_unresolved_error_and_uniform_equations():
    failed = home.observe(home.Observation(), 0.2, 1)
    recovered = home.observe(failed, 1.0, 2)
    assert recovered.loss == pytest.approx(0.56)
    assert recovered.count == 2 and recovered.last_error == 1 and recovered.perfect_after_error == 1
    rival = replace(recovered, last_error=None)
    weights = home.probabilities({"error": recovered, "clear": rival}, 4)
    gap = 0.1 * math.log1p(3) / 2
    assert weights["error"] == pytest.approx(0.8 * math.exp(gap) / (1 + math.exp(gap)) + 0.1)
    assert sum(weights.values()) == pytest.approx(1)
    assert home.probabilities({"a": recovered, "b": rival}, 4, epsilon=1) == {"a": 0.5, "b": 0.5}


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -0.1, 1.01, True, "0.5"])
def test_home_invalid_score_does_not_mutate_record(value):
    record = home.Observation()
    with pytest.raises(ValueError):
        home.observe(record, value, 1)
    assert record == home.Observation()


def test_home_sampler_caps_fair_share_and_does_not_read_answers():
    cases = tuple(home.Case(str(i), tuple(str(j) for j in range(9))) for i in range(8))
    kwargs = dict(round_id=2, max_cases=4, max_queries=7, seed=42)
    plan = home.sample(cases, {}, {}, **kwargs)
    assert plan == home.sample(cases, {}, {}, **kwargs)
    assert len(plan.selected) == 4
    assert sum(len(q) for _, q in plan.selected) == 7
    assert all(len(q) == len(set(q)) for _, q in plan.selected)
    assert len({c for c, _ in plan.selected}) == 4
    observed_cases, observed_queries = home.mark_selected(plan, {}, {})
    assert set(observed_cases) == {c for c, _ in plan.selected}
    assert all(r.last_selected == 2 and r.count == 0 for r in observed_queries.values())
    assert set(home.Case.__dataclass_fields__) == {"case_id", "query_ids"}
    for bad in (0, -1, True):
        with pytest.raises(ValueError):
            home.sample(cases, {}, {}, round_id=1, max_cases=bad)
    with pytest.raises(ValueError):
        home.sample((cases[0], cases[0]), {}, {}, round_id=1, max_cases=2)
    with pytest.raises(ValueError):
        home.Case("x", ("q", "q"))


def test_home_nearest_equivalent_completed_ancestor_and_one_draw():
    identity = home.ConstructionIdentity("dataset", "runtime", "construction", "model")
    nearest = home.ReusableAncestor("near", 1, identity, "a" * 64, True, True)
    far = replace(nearest, commit="far", distance=4)
    assert home.reuse_source((far, nearest), identity, probability=1) == nearest
    assert home.reuse_source((far, nearest), identity, probability=0) is None
    for bad in (replace(nearest, completed=False), replace(nearest, construction_unchanged=None),
                replace(nearest, identity=replace(identity, model="different"))):
        assert home.reuse_source((bad,), identity, probability=1) is None
    with pytest.raises(ValueError):
        replace(nearest, snapshot_sha256="unknown")


def lesson(polarity="success", evidence=("visible output",)):
    return dualpm.Lesson(polarity, "Plan", "Use the observed output.", evidence, "tool: output visible", "low")


def episode(index=0):
    return dualpm.VisibleEpisode(str(index), "Public toy task", ("visible instruction",),
                                 ("tool response",), "observed result")


def callbacks():
    calls = []
    def reflect(value):
        calls.append(("reflect", value))
        return "reflection from " + value.visible_steps[0]
    def draft(request):
        calls.append(("draft", request))
        assert request.reflection == "reflection from tool response"
        return (lesson(), lesson("failure"))
    def maintain(request):
        calls.append(("maintain", request))
        assert all(d.lesson.polarity == request.polarity for _, d in request.drafts)
        return tuple(dualpm.MemoryClaim(d.lesson, (), (key,)) for key, d in request.drafts)
    return reflect, draft, maintain, calls


def test_dualpm_executes_reflection_then_draft_and_two_isolated_maintenance_calls():
    reflect, draft, maintain, calls = callbacks()
    flow = dualpm.DualPM(reflect, draft, maintain)
    frozen = flow.begin_block()
    assert frozen == () and flow.memory == ()
    first = flow.finish_block((episode(),))
    assert [kind for kind, _ in calls] == ["reflect", "draft", "maintain", "maintain"]
    assert len(first) == 2 and frozen == ()
    snapshot = flow.begin_block()
    assert snapshot == first
    flow.finish_block((episode(1),))
    assert snapshot == first
    with pytest.raises(FrozenInstanceError):
        snapshot[0].content = "mutation"
    with pytest.raises(TypeError):
        dualpm.VisibleEpisode(**{**episode().__dict__, "gold_plan": "secret"})
    with pytest.raises(ValueError):
        dualpm.VisibleEpisode("x", "task", (), ["mutable"], "answer")


@pytest.mark.parametrize("bad_kind", ["foreign_ref", "empty_lineage", "polarity", "evidence", "pool", "mutable"])
def test_dualpm_failed_maintenance_never_partially_commits(bad_kind):
    reflect, draft, _, _ = callbacks()
    def maintain(request):
        value = lesson(request.polarity)
        if request.polarity == "success":
            return (dualpm.MemoryClaim(value, (), ("D0",)),)
        if bad_kind == "foreign_ref":
            return (dualpm.MemoryClaim(value, (), ("D999",)),)
        if bad_kind == "empty_lineage":
            return (dualpm.MemoryClaim(value, (), ()),)
        if bad_kind == "polarity":
            value = lesson("success")
        if bad_kind == "evidence":
            value = lesson("failure", ("a", "b", "c", "d"))
        claims = (dualpm.MemoryClaim(value, (), ("D0",)),)
        if bad_kind == "pool":
            claims *= 11
        return list(claims) if bad_kind == "mutable" else claims
    flow = dualpm.DualPM(reflect, draft, maintain)
    flow.begin_block()
    with pytest.raises(ValueError):
        flow.finish_block((episode(),))
    assert flow.memory == ()


def test_dualpm_replay_draft_capacity_and_frozen_block_admission():
    reflect, draft, maintain, _ = callbacks()
    flow = dualpm.DualPM(reflect, draft, maintain)
    with pytest.raises(ValueError):
        flow.finish_block((episode(),))
    flow.begin_block()
    with pytest.raises(ValueError):
        flow.begin_block()
    flow.finish_block((episode(),))
    flow.begin_block()
    with pytest.raises(ValueError):
        flow.finish_block((episode(),))
    over = dualpm.DualPM(reflect, lambda request: (lesson(),) * 3, maintain)
    over.begin_block()
    with pytest.raises(ValueError):
        over.finish_block((episode(),))
    assert over.memory == ()


@pytest.mark.parametrize("module,tier", [(home, "l1_mechanism"), (dualpm, "l0_interface")])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_nov26_diagnostic_contract(module, tier, seed):
    result = module.diagnostic(seed, device="cpu")
    assert module.REQUIRES_GPU_VALIDATION is False
    assert result["seed"] == seed and result["device"] == "cpu"
    assert result["evaluation_tier"] == tier and result["diagnostic_only"] is True
    assert result["checks"] and all(type(value) is bool and value for value in result["checks"].values())
    assert result["metrics"] and all(type(value) in (int, float) and math.isfinite(value)
                                     for value in result["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, device="cuda")
    with pytest.raises(ValueError):
        module.diagnostic(True)
