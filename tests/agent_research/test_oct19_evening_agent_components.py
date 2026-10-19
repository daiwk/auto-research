from dataclasses import fields, replace
import importlib.util
import math
from pathlib import Path

import pytest

from auto_research.agent_research import drago, harness_decomposition as hda, proper_agent as proper

ROOT = Path(__file__).resolve().parents[2]


def memory_graph():
    facts = [proper.MemoryFact("past", "milk", "needs", "restock", 1, "event-1", "Buy milk", open_loop=True),
             proper.MemoryFact("future", "milk", "state", "full", 20, "event-2", "Already bought milk")]
    vectors = {"milk": (1., 0., 0.), "restock": (0., 1., 0.), "full": (0., 0., 1.)}
    return proper.MemoryGraph(facts, embed=vectors.__getitem__)


def test_proper_pagerank_causal_provenance_and_actor_isolation():
    graph = memory_graph()
    obs = proper.Observation(3., "shop", ("milk",))
    assert [f.key for f in graph.retrieve(obs)] == ["past"]
    assert graph.retrieve(replace(obs, timestamp=0.)) == ()
    received = []
    def actor(view):
        received.append(view)
        assert not {"window", "gold", "reference", "judge"} & {f.name for f in fields(view)}
        return view.evidence.text if view.evidence and not view.already_spoken else None
    result = proper.run_stream(graph, (obs, replace(obs, timestamp=5.)),
        gate=lambda _o, candidates: proper.GateEvidence((candidates[0].key,), candidates[0].passage), actor=actor)
    assert result == (proper.Intervention(3., "Buy milk"),)
    assert received[1].already_spoken == ((3., "Buy milk"),)


def test_proper_bad_gate_fails_before_actor():
    with pytest.raises(ValueError, match="provenance"):
        proper.run_stream(memory_graph(), [proper.Observation(3., "shop", ("milk",))],
            gate=lambda _o, _c: proper.GateEvidence(("future",), "fabricated"),
            actor=lambda _view: pytest.fail("actor must not execute"))


def test_proper_multihop_graph_reaches_remote_evidence_not_unconnected_hub():
    facts = [proper.MemoryFact("link", "carton", "related", "shopping", 0, "one", "Shopping plan"),
             proper.MemoryFact("remote", "shopping", "related", "milk", 0, "two", "Restock milk"),
             proper.MemoryFact("unrelated", "dog", "related", "door", 0, "three", "Close door")]
    names = ("carton", "shopping", "milk", "dog", "door")
    vectors = {name: tuple(float(i == j) for i in range(5)) for j, name in enumerate(names)}
    graph = proper.MemoryGraph(facts, embed=vectors.__getitem__)
    observed = proper.Observation(1., "public observation", ("carton",))
    assert {f.key for f in graph.retrieve(observed, limit=2)} == {"link", "remote"}


@pytest.mark.parametrize("times", [(3., 3.), (4., 3.), (math.nan, 4.)])
def test_proper_rejects_noncausal_timestamps(times):
    with pytest.raises(ValueError):
        proper.run_stream(memory_graph(), [proper.Observation(t, "shop", ("milk",)) for t in times],
                          gate=lambda _o, _c: None, actor=lambda _v: None)


def test_proper_exact_timing_joint_metrics_silence_and_unknown():
    fire = proper.Intervention(4., "Buy milk")
    assert proper.score_clip([fire], window=(2., 2.), judge=lambda _: True)["perfect"]
    late = proper.score_clip([replace(fire, timestamp=4.01)], window=(2., 2.), judge=lambda _: True)
    assert late["late"] and not late["perfect"]
    repeated = proper.score_clip([fire, replace(fire, timestamp=5.)], window=(2., 4.), judge=lambda _: True)
    assert repeated["hit"] and repeated["over_trigger"] and not repeated["perfect"]
    assert proper.score_clip([], window=None, judge=lambda _: pytest.fail())["perfect"]
    assert proper.score_clip([fire], window=None, judge=lambda _: True)["silent_clip_false_trigger"]
    assert proper.score_clip([fire], window=(2., 4.), judge=lambda _: None)["perfect"] is None


def hda_arms():
    ids = tuple(f"x{i}" for i in range(20))
    return tuple(hda.Arm(ids, (score,)*20, cost, str(i)*64)
                 for i, score, cost in ((1, .1, 1.), (2, .8, 4.), (3, .3, 4.), (4, .5, 4.)))


REVIEW = hda.ReviewedControl("human", "control procedure and code reviewed", True)


def test_hda_actual_decomposition_and_paired_bootstrap():
    result = hda.attribute(*hda_arms(), compute_review=REVIEW, neutralization_review=REVIEW, resamples=100)
    assert result["attributed"] and result["significant"]
    assert result["test_time_scaling"] == pytest.approx(.2)
    assert result["detected_overfitting"] == pytest.approx(.3)
    assert result["residual_upper_bound"] == pytest.approx(.2)
    assert result["raw_identity_error"] < 1e-12
    assert sum(result[k] for k in ("overfitting_share", "scaling_share", "residual_share")) == pytest.approx(1)


def test_hda_no_gain_no_attribution_and_no_extra_compute_contract():
    base = hda_arms()[0]
    result = hda.attribute(base, base, base, base, compute_review=REVIEW,
                           neutralization_review=REVIEW, resamples=100)
    assert not result["attributed"] and "residual_upper_bound" not in result
    with pytest.raises(ValueError, match="equal baseline"):
        hda.attribute(base, base, replace(base, harness_sha256="2"*64), base,
                      compute_review=REVIEW, neutralization_review=REVIEW)


@pytest.mark.parametrize("mutation", ["pair", "budget", "review", "nan"])
def test_hda_invalid_control_rejection(mutation):
    arms, review = list(hda_arms()), REVIEW
    if mutation == "pair":
        arms[2] = replace(arms[2], item_ids=tuple(reversed(arms[2].item_ids)))
    elif mutation == "budget":
        arms[2] = replace(arms[2], mean_inference_cost=2.)
    elif mutation == "review":
        review = replace(review, approved=False)
    else:
        arms[3] = replace(arms[3], scores=(math.nan,)*20)
    with pytest.raises(ValueError):
        hda.attribute(*arms, compute_review=review, neutralization_review=REVIEW)


def test_hda_raw_signed_components_not_clipped():
    arms = list(hda_arms())
    arms[2] = replace(arms[2], scores=(1.2,)*20)
    result = hda.attribute(*arms, compute_review=REVIEW, neutralization_review=REVIEW, resamples=100)
    assert result["residual_upper_bound"] < 0
    assert result["residual_share"] == 0
    assert result["raw_identity_error"] < 1e-12


def corridor():
    domain = drago.Domain("walk", (("at", 1),), (
        drago.Action("move", frozenset({("at", "a")}), frozenset({("at", "b")}), frozenset({("at", "a")})),))
    problem = drago.Problem("walk", (("a", "room"), ("b", "room")),
                            frozenset({("at", "a")}), frozenset({("at", "b")}))
    return domain, problem


def test_drago_relaxation_search_and_joint_failure_are_distinct():
    domain, problem = corridor()
    assert drago.diagnose(domain, problem).weight == 0
    assert drago.diagnose(domain, problem).search_status == "solvable"
    joint = drago.diagnose(domain, replace(problem, goals=problem.initial | problem.goals))
    assert joint.search_status == "exhausted"
    assert {f.axis for f in joint.findings} == {"joint_unsolvable"}
    unreachable = drago.diagnose(domain, replace(problem, initial=frozenset()))
    assert {f.axis for f in unreachable.findings} == {"reachability", "joint_unsolvable"}
    limited = drago.diagnose(domain, problem, search_budget=1)
    assert limited.search_status == "budget_exhausted" and not limited.findings


def test_drago_contract_and_statement_counts():
    domain, problem = corridor()
    for changed in (replace(problem, domain="other"), replace(problem, goals=frozenset({("bogus", "a")})),
                    replace(problem, initial=frozenset({("at", "unknown")})),
                    replace(problem, objects=problem.objects+(problem.objects[0],))):
        assert drago.diagnose(domain, changed).search_status == "invalid"
    counted = drago.diagnose(domain, problem, expected_counts=(("room", 3),))
    assert counted.weight == 1 and counted.findings[0].axis == "count"


def test_drago_repair_progress_rollback_and_no_gold():
    domain, repaired = corridor()
    initial = replace(repaired, initial=frozenset())
    exposed = []
    def proposer(public, diagnosis):
        exposed.append({f.name for f in fields(public)})
        assert diagnosis.weight > 0
        return repaired
    final, trace = drago.repair_loop(domain, initial, proposer=proposer)
    assert final == repaired and trace[0]["accepted"]
    assert not {"gold", "reference", "answer"} & exposed[0]
    final, trace = drago.repair_loop(domain, initial,
                                    proposer=lambda p, _: replace(p, goals=frozenset()))
    assert final == initial and trace[0]["reason"] == "goal_weakening"


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_runner_three_seed_real_mechanisms(seed):
    spec = importlib.util.spec_from_file_location("oct19_evening_agent_runner",
                                                 ROOT/"scripts/run_oct19_evening_agent_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for key, function in module.FUNCTIONS.items():
        result = function(seed)
        assert result["seed"] == seed and len(result["fixture_sha256"]) == 64
        assert result["protocol_records"]
        assert all(type(v) in (float, int, bool) and math.isfinite(v) for v in result["metrics"].values())
        if key == "proper-agent":
            assert result["metrics"]["retained_unscored_clips"] > 0
            assert result["metrics"]["future_memory_exposures"] == 0
        elif key == "harness-decomposition":
            assert result["metrics"]["rejected_invalid_controls"] == 3
            assert result["metrics"]["noise_control_attributed"] == 0
        else:
            assert result["metrics"]["blocked_goal_weakening_repairs"] > 0
