"""Real CPU protocol execution, not model/Agent capability evidence."""
from dataclasses import replace
import importlib.util
import math
from pathlib import Path

import pytest

from auto_research.agent_research import aria_repair as aria
from auto_research.agent_research import coda, diviner, jev_agent_harness as jev, memscope, torsi


def _ledger():
    return diviner.EvidenceLedger(diviner.InvestigationScope("incident", "ranking", 10., 20., 22.))


def _evidence(**changes):
    return replace(diviner.Evidence("e", "incident", "ranking", 10., 20., 21., "data", "public-fixture"),
                   **changes)


@pytest.mark.parametrize("changes,reason", [
    ({"status": "timeout"}, "incomplete_or_failed_tool"),
    ({"status": "partial"}, "incomplete_or_failed_tool"),
    ({"available_at": 23.}, "future_evidence"),
    ({"window_start": 9.}, "window_mismatch"),
    ({"target": "ads"}, "scope_mismatch"),
    ({"available_at": math.nan}, "nonfinite_time"),
])
def test_diviner_rejects_invalid_evidence_and_keeps_reason(changes, reason):
    ledger = _ledger()
    assert not ledger.admit(_evidence(**changes))
    assert ledger.rejected == {"e": reason}
    with pytest.raises(ValueError, match="unadmitted"):
        ledger.update_hypothesis("root", "supported", ["e"])


def test_diviner_empty_is_not_positive_and_owner_cannot_be_impersonated():
    ledger = _ledger()
    assert ledger.admit(_evidence(status="valid_empty"))
    with pytest.raises(ValueError, match="valid-empty"):
        ledger.update_hypothesis("positive", "supported", ["e"])
    ledger.update_hypothesis("absent", "refuted", ["e"])
    update = diviner.KnowledgeUpdate("skill", "service-owner", 1, 2)
    for variant in (update, replace(update, replay_passed=True, approved_by="agent")):
        with pytest.raises(ValueError, match="approval"):
            diviner.publish_update(variant)
    assert diviner.publish_update(replace(update, replay_passed=True, approved_by="service-owner")) == 2


def test_diviner_admission_snapshots_mutable_tool_payload():
    ledger = _ledger()
    payload = {"observed_count": [2]}
    assert ledger.admit(_evidence(payload=payload))
    payload["observed_count"][0] = 999
    assert ledger.observations["e"].payload == {"observed_count": [2]}
    with pytest.raises(ValueError, match="unique"):
        ledger.admit(_evidence())


def test_torsi_live_clock_preserves_scheduling_delay():
    assert torsi.ActionTiming(1., 3., 4.).measurements() == {"response_latency": 2., "action_age": 3.}
    with pytest.raises(ValueError):
        torsi.ActionTiming(1., 3., 2.).measurements()
    assert torsi.normalized_progress(12., 10.) == 100.


def test_torsi_strict_paired_acceptance_and_test_isolation():
    scores = {"v1": 1., "v2": 2.}
    assert not torsi.select_guidance("old", "new", scores, scores).accepted
    result = torsi.select_guidance("old", "new", scores, {"v1": 0., "v2": 4.})
    assert result.accepted and result.guidance == "new" and result.paired_validation_gain == .5
    for kwargs in ({"split": "test"}, {"test_task_ids": ["v1"]}, {"feedback_task_ids": ["v2"]}):
        with pytest.raises(ValueError):
            torsi.select_guidance("old", "new", scores, scores, **kwargs)
    with pytest.raises(ValueError):
        torsi.select_guidance("old", "new", scores, {"v1": 1.})
    seen = []
    trace = torsi.FeedbackTrace("feedback", ({"public": 1},), ("left",), (torsi.ActionTiming(0, 1, 2),))
    assert torsi.propose_guidance("old", [trace], lambda state, traces: seen.extend(traces) or "new") == "new"
    assert seen == [trace] and not hasattr(trace, "gold")


def _events():
    return (aria.Event("e1", "user", "message", "public task"),
            aria.Event("e2", "assistant", "message", "wrong branch"),
            aria.Event("e3", "tool", "tool_result", "observable result"))


def test_aria_cut_retains_prefix_and_drops_suffix():
    replacement = aria.Event("new", "assistant", "tool_call", "check_current_metric")
    patch = aria.RepairPatch("wrong branch", "e1", (replacement,))
    assert aria.apply_repair(_events(), patch, first_bad_event_id="e2") == (_events()[0], replacement)
    assert aria.verified_repair(fresh_control_passed=False, patched_execution_passed=True)
    assert not aria.verified_repair(fresh_control_passed=True, patched_execution_passed=True)


@pytest.mark.parametrize("replacement,cut", [
    (aria.Event("e1", "assistant", "message", "collision"), "e1"),
    (aria.Event("new", "tool", "tool_result", "invented observation"), "e1"),
    (aria.Event("new", "assistant", "message", "late patch"), "e2"),
])
def test_aria_rejects_id_collision_fabricated_tools_and_late_cuts(replacement, cut):
    with pytest.raises(ValueError):
        aria.apply_repair(_events(), aria.RepairPatch("diagnosis", cut, (replacement,)),
                          first_bad_event_id="e2")


def test_coda_freezes_retrieval_and_rejects_unselected_rewrites():
    bank = [coda.Skill("a", {"trigger": "query"}, {"steps": "do x"}),
            coda.Skill("b", {"trigger": "other"}, {"steps": "do y"})]
    result = coda.rewrite_selected(bank, ["a"], {"a": {"steps": "do x differently"}})
    assert result[0].retrieval_fields == bank[0].retrieval_fields and result[1] == bank[1]
    assert bank[0].content_fields["steps"] == "do x"
    with pytest.raises(ValueError):
        coda.rewrite_selected(bank, ["a"], {"b": {"steps": "invalid"}})
    with pytest.raises(ValueError):
        coda.rewrite_selected(bank, ["a"], {"a": {"trigger": "invalid"}})


def test_coda_pairs_flips_and_rr_uses_full_denominator():
    outcomes = {"delivered": {"a": True, "b": False, "c": True, "d": False},
                "repeat": {"a": True, "b": False, "c": True, "d": False},
                "reword": {"a": False, "b": True, "c": True, "d": False},
                "incomplete": {"a": True, "b": False, "c": False, "d": False},
                "misleading": {"a": False, "b": False, "c": False, "d": False},
                "no_skill": {"a": True, "b": True, "c": False, "d": False}}
    metrics = coda.audit(outcomes)
    assert metrics["consistency_rate"] == .5 and metrics["resistance_incomplete"] == .25
    assert metrics["noise_floor_consistency"] == 1 and metrics["peak_to_worst_drop"] == .5
    del outcomes["misleading"]["d"]
    with pytest.raises(ValueError, match="same task"):
        coda.audit(outcomes)


CODE = "def retrieve(memory, query):\n    threshold = 0.70\n    return memory.get(query) if threshold < 1 else None\n"


def test_memscope_local_success_retains_memory_and_identity():
    provider, memory = memscope.Provider("p", "v1", CODE), {"key": {"value": 2}}
    seen = []
    def probe(candidate, copy):
        seen.append((candidate.provider_id, candidate.schema_version))
        copy["key"]["value"] = 999
        return True
    result = memscope.patch_provider(provider, memory, old="0.70", new="0.80", probe=probe)
    assert result.accepted and result.provider.provider_id == "p" and "0.80" in result.provider.code
    assert result.memory == memory == {"key": {"value": 2}} and seen == [("p", "v1")]


@pytest.mark.parametrize("old,new,probe,stage", [
    ("missing", "x", lambda *a: True, "localized_edit"),
    ("retrieve(memory, query)", "retrieve(memory)", lambda *a: True, "syntax_interface"),
    ("0.70", "0.80", lambda *a: False, "compatibility_probe"),
])
def test_memscope_failed_patch_rolls_back_code_and_bank(old, new, probe, stage):
    provider = memscope.Provider("p", "v1", CODE)
    memory = {"known": [1, 2]}
    result = memscope.patch_provider(provider, memory, old=old, new=new, probe=probe)
    assert not result.accepted and result.failure_stage == stage
    assert result.provider == provider and result.memory == memory


def _shadow():
    return [jev.ShadowDecision(f"cal-{i}", "tool", confidence, correct, True, .1)
            for i, (confidence, correct) in enumerate(((.55, False), (.55, False), (.9, True), (.9, True)))]


def test_jev_shadow_fit_is_not_a_constant_threshold_and_no_test_labels():
    fit = jev.calibrate(_shadow(), min_bin=2)
    assert fit.thresholds["tool"] == .9
    changed = [replace(x, decision_correct=True) for x in _shadow()]
    assert jev.calibrate(changed, min_bin=2).thresholds["tool"] == .55
    with pytest.raises(ValueError):
        jev.calibrate(_shadow(), split="test")
    with pytest.raises(ValueError):
        jev.calibrate(_shadow(), excluded_task_ids=["cal-1"])


def test_jev_thresholds_are_fitted_separately_for_each_decision_class():
    rows = _shadow() + [replace(x, decision_class="arguments", decision_correct=True) for x in _shadow()]
    result = jev.calibrate(rows, min_bin=2)
    assert result.thresholds == {"tool": .9, "arguments": .55}
    assert result.bins["tool"][0][1] < 0 and result.bins["arguments"][0][1] > 0


def test_jev_route_accept_fallback_failure_and_costs_without_gold():
    fit = jev.calibrate(_shadow(), min_bin=2)
    public = jev.PublicDecision("held-out", "tool", "public task", ("a", "b"))
    seen = []
    def strong(request):
        assert set(request.__dataclass_fields__) == {"task_id", "decision_class", "context", "options"}
        seen.append(request)
        return 1
    accepted = jev.route(public, fit, decision_model=lambda x: (.95, .05), strong_model=strong,
                         decision_cost=.1, strong_cost=2.)
    fallback = jev.route(public, fit, decision_model=lambda x: (.6, .4), strong_model=strong,
                         decision_cost=.1, strong_cost=2.)
    failure = jev.route(public, fit, decision_model=lambda x: (math.nan, .2), strong_model=strong,
                        decision_cost=.1, strong_cost=2.)
    assert accepted.source == "decision_model" and accepted.total_cost == .1
    assert fallback.source == "strong_model" and fallback.total_cost == 2.1
    assert failure.fallback_reason == "decision_model_failure" and len(seen) == 2


def test_jev_underfilled_bins_and_unseen_classes_always_defer():
    fit = jev.calibrate(_shadow(), min_bin=5)
    assert fit.thresholds["tool"] is None
    result = jev.route(jev.PublicDecision("test", "other", "public", ("a",)), fit,
                       decision_model=lambda x: pytest.fail("must not be called"), strong_model=lambda x: 0,
                       decision_cost=1., strong_cost=2.)
    assert result.total_cost == 2. and result.fallback_reason == "unfitted_class"


def test_runner_methods_and_seeded_negative_controls():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("oct18_agent_runner", root / "scripts/run_oct18_agent_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert set(module.FUNCTIONS) == {"diviner", "torsi", "aria", "coda", "memscope", "jev-agent-harness"}
    for function in module.FUNCTIONS.values():
        first, second = function(42), function(43)
        assert first["fixture_sha256"] != second["fixture_sha256"]
        assert first["metrics"] and first["seed"] == 42 and second["seed"] == 43
        assert all(type(v) in (int, float, bool) for v in first["metrics"].values())
