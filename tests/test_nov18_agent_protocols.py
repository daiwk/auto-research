"""Negative controls for four explicitly non-capability CPU interfaces."""

from dataclasses import FrozenInstanceError, replace
import importlib
import math

import pytest

from auto_research.foundation_models.typed_inbox_protocol import (
    ValidationAction, fit_action_threshold, freeze_email, grouped_folds,
)
from auto_research.agent_research.askalcf_protocol import (
    Evidence, ExpansionCache, Revisions, repair_noise_report, reviewed_action, route,
    two_scope_sufficiency,
)
from auto_research.agent_research.prodpilot_protocol import (
    Rule, audit, deploy_gate, gated_deploy, repair,
)
from auto_research.multimodal.fend_protocol import (
    DetectorEvent, acoustic_null_gate, arbitrate, evaluate,
)


def email(identity="a", subject="Topic", sender="a@example.org", **kwargs):
    return freeze_email(email_id=identity, sender=sender, subject=subject,
                        body=kwargs.get("body", "body"), channel="email",
                        received_at="2026-11-18", secrets=kwargs.get("secrets", ()))


def test_inbox_snapshot_exact_redacted_and_immutable():
    view = email(body="secret " + "x" * 1500, secrets=("secret",))
    assert len(view.body) == 1500 and view.body.startswith("[REDACTED]")
    assert view.view_sha256 == email(body="secret " + "x" * 1500, secrets=("secret",)).view_sha256
    assert view.view_sha256 != email(body="other").view_sha256
    with pytest.raises(FrozenInstanceError):
        view.body = "new"
    with pytest.raises(TypeError):
        freeze_email(email_id="x", sender="a", subject="s", body="x", channel="email",
                     received_at="today", gold_label=True)


def test_thread_groups_cannot_leak_across_folds_and_duplicate_ids_fail():
    messages = [email("a", "Topic"), email("b", "Re: FWD: Topic"),
                email("c", "topic", "A@EXAMPLE.ORG"), email("d", "Other")]
    a = grouped_folds(messages, folds=3, seed=43)
    assert a["a"] == a["b"] == a["c"]
    assert a == grouped_folds(list(reversed(messages)), folds=3, seed=43)
    assert messages[0].thread_key != messages[3].thread_key
    with pytest.raises(ValueError):
        grouped_folds([messages[0], messages[0]])
    with pytest.raises(ValueError):
        grouped_folds(messages, folds=True)


def test_action_threshold_uses_validation_cost_and_rejects_test_fitting():
    rows = [ValidationAction(0.2, True), ValidationAction(0.3, False), ValidationAction(0.8, True)]
    conservative = fit_action_threshold(rows, split="validation", missed_action_cost=10)
    cheap_miss = fit_action_threshold(rows, split="validation", missed_action_cost=0.1)
    assert conservative.threshold == 0.2 and cheap_miss.threshold == 0.8
    assert conservative.predict(0.2)
    with pytest.raises(ValueError, match="never fit on test"):
        fit_action_threshold(rows, split="test")
    for value in (float("nan"), -0.1, 1.1, True):
        with pytest.raises(ValueError):
            conservative.predict(value)
    all_negative = fit_action_threshold([ValidationAction(1.0, False)], split="validation")
    assert not all_negative.predict(1.0)


@pytest.mark.parametrize("evidence,expected", [
    (Evidence(tool_error=True, policy_failure=True), "tools_mcp"),
    (Evidence(policy_failure=True, production_sufficient=False, corpus_sufficient=False), "prompt"),
    (Evidence(production_sufficient=False, corpus_sufficient=False, correct=False), "knowledge"),
    (Evidence(production_sufficient=False, corpus_sufficient=True, correct=False), "retrieval"),
    (Evidence(production_sufficient=True, faithful=False), "model"),
    (Evidence(production_sufficient=True, faithful=True, correct=False), "model"),
    (Evidence(production_sufficient=True, faithful=True, correct=True), "no_failure"),
    (Evidence(), "unknown"),
    (Evidence(production_sufficient=True, faithful=True, correct=True, conflicting_signals=True), "unknown"),
])
def test_sufficiency_pivot_precedes_answer_quality(evidence, expected):
    assert route(evidence) == expected


def test_answer_blind_probe_receives_separate_scopes_and_refuses_bad_signal():
    requests = []

    def evaluator(request):
        requests.append(request)
        return bool(request.passages)

    assert two_scope_sufficiency("question", [], ["doc"], evaluator) == (False, True)
    assert {r.scope for r in requests} == {"production", "corpus"}
    assert all(set(vars(r)) == {"question", "passages", "scope"} for r in requests)
    with pytest.raises(TypeError):
        two_scope_sufficiency("q", [], [], lambda r: 1)
    with pytest.raises(TypeError):
        Evidence(correct=0.5)


def test_cache_dependencies_and_null_bypass_execute_actual_callback():
    calls = []
    cache = ExpansionCache()
    rev = Revisions("m", "p", "c", "r", "t", "e")

    def expand(q):
        calls.append(q)
        return (x for x in [q, str(len(calls))])

    assert cache.get("q", rev, expand) == cache.get("q", rev, expand)
    assert len(calls) == 1
    for dependency in vars(rev):
        cache.get("q", replace(rev, **{dependency: "changed"}), expand)
    cache.get("q", rev, expand, bypass=True)
    assert len(calls) == 8
    assert cache.get("q", rev, expand) == ("q", "1")
    with pytest.raises(ValueError):
        replace(rev, corpus="")


def test_zero_net_null_drift_does_not_hide_opposing_flips_or_human_decline():
    result = repair_noise_report([False, True], [True, True], [True, False])
    assert result["null_rate_drift"] == 0 and result["null_flip_count"] == 2
    assert not result["clears_local_noise_gate"]
    assert repair_noise_report([False] * 3, [True] * 3, [False] * 3)["clears_local_noise_gate"]
    calls = []
    assert not reviewed_action("decline", lambda: calls.append(1), lambda: calls.append(2))["executed"]
    assert calls == []
    assert not reviewed_action("ship", lambda: "claimed success", lambda: True)["succeeded"]


def test_prodpilot_checker_not_report_and_bounded_retries():
    calls = []

    def fake_fix(p):
        calls.append("claimed")
        return p  # A reported application without a real change.

    rule = Rule("health", 0, "static", ("health",), lambda p: p.get("health") == "ok", fake_fix)
    result = repair({}, [rule])
    assert calls == ["claimed"] * 3 and result["manual_review"] == ["health"]
    assert all(e["event"] == "rejected_checker" for e in result["events"])
    assert not deploy_gate({}, [rule], probability=1.0, build_determined=True)["allowed"]


def test_prodpilot_rolls_back_regressions_boundary_violations_and_exceptions():
    guard = Rule("guard", 0, "static", ("g",), lambda p: p.get("g") == "ok")
    new = Rule("new", 1, "delegated", ("n", "g"), lambda p: p.get("n") == "ok",
               lambda p: {**p, "g": "broken", "n": "ok"})
    result = repair({"g": "ok"}, [guard, new])
    assert result["project"] == {"g": "ok"}
    assert result["events"][0]["event"] == "reverted_regression"
    escaped = replace(new, allowed_files=("n",))
    result = repair({"g": "ok"}, [guard, escaped])
    assert result["project"] == {"g": "ok"}
    assert result["events"][0]["error_type"] == "PermissionError"
    with pytest.raises(ValueError):
        repair({}, [guard], max_cycles=6)
    with pytest.raises(ValueError):
        repair({}, [guard], max_attempts=4)


def test_prodpilot_idempotence_unknown_inputs_and_smoke_failure():
    rule = Rule("x", 0, "parametric", ("x",), lambda p: p.get("x") == "ok",
                lambda p: {**p, "x": "ok"})
    repaired = repair({}, [rule])
    assert repair(repaired["project"], [rule])["events"] == []
    for prob in (None, float("nan"), -1, True):
        assert not deploy_gate(repaired["project"], [rule], probability=prob, build_determined=True)["allowed"]
    gate = deploy_gate(repaired["project"], [rule], probability=0.369, build_determined=True)
    calls = []

    def deploy():
        calls.append("deploy")
        return "local"

    assert not gated_deploy(gate, approved=False, deploy=deploy, smoke=lambda x: True)["deployed"]
    assert calls == []
    run = gated_deploy(gate, approved=True, deploy=deploy, smoke=lambda x: False)
    assert run["deployed"] and not run["verified"] and calls == ["deploy"]
    assert audit({}, [replace(rule, check=lambda p: 1)])["x"] == "error"


def test_prodpilot_deploy_exception_does_not_claim_no_external_side_effect():
    attempted = []

    def deploy_then_disconnect():
        attempted.append("external action may have started")
        raise TimeoutError("connection lost")

    outcome = gated_deploy({"allowed": True}, approved=True, deploy=deploy_then_disconnect,
                           smoke=lambda x: True)
    assert attempted and outcome["deployed"] is None
    assert outcome["deployment_status"] == "unknown"
    assert outcome["events"] == ["deploy_called"] and not outcome["verified"]


def test_fend_accumulates_priority_until_deadline_instead_of_first_firing():
    events = [DetectorEvent(1, "ai", "a"), DetectorEvent(20, "voicemail", "b"),
              DetectorEvent(21, "ivr", "late")]
    assert arbitrate(events)["label"] == "voicemail"
    assert arbitrate(events, deadline=19)["label"] == "ai"
    assert arbitrate([])["label"] == "human"
    assert arbitrate(events)["ignored_late"] == 1
    with pytest.raises(ValueError):
        DetectorEvent(float("nan"), "ai", "a")
    with pytest.raises(ValueError):
        DetectorEvent(1, "human", "a")


def test_fend_human_fpr_denominator_and_undefined_null_are_explicit():
    gold = {"h1": "human", "h2": "human", "v": "voicemail", "i": "ivr"}
    pred = {"h1": "ai", "h2": "human", "v": "voicemail", "i": "human"}
    result = evaluate(gold, pred)
    assert result["human_fpr"] == 0.5 and result["accuracy"] == 0.5
    with pytest.raises(ValueError, match="undefined"):
        evaluate({"v": "voicemail"}, {"v": "voicemail"})
    with pytest.raises(ValueError):
        evaluate(gold, {"h1": "human"})
    assert acoustic_null_gate([0, 1, 2, 3], [0, 1, 2, 3])["admitted"]
    assert not acoustic_null_gate([0, 1, 2, 3], [10, 11, 12, 13])["admitted"]
    with pytest.raises(ValueError, match="IQR"):
        acoustic_null_gate([1] * 4, [2] * 4)


@pytest.mark.parametrize("module_name", [
    "auto_research.foundation_models.typed_inbox_protocol",
    "auto_research.agent_research.askalcf_protocol",
    "auto_research.agent_research.prodpilot_protocol",
    "auto_research.multimodal.fend_protocol",
])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_all_cpu_protocols_are_bounded_diagnostics(module_name, seed):
    module = importlib.import_module(module_name)
    report = module.diagnostic(seed)
    assert module.REQUIRES_GPU_VALIDATION is False and report["diagnostic_only"] is True
    assert report["seed"] == seed
    assert report["evaluation_tier"] in {"l0_interface", "l1_mechanism"}
    assert all(type(x) is bool and x for x in report["checks"].values())
    assert all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
               for x in report["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, device="cuda:0")
