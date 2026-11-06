from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
import hashlib
import json
import math
from pathlib import Path
import re

import pytest

from auto_research.agent_research import continual_autoresearch as car
from auto_research.agent_research import meta_square as meta
from auto_research.agent_research import runtime_tickets as rt


def evidence(step=1, terminal=False):
    return {"step": step, "trajectory_delta": [f"public observation {step}"],
            "workspace_observations": ["visible artifact missing"],
            "prior_edit_status": "none", "terminal_claim": terminal}


def test_meta_task_local_edits_accumulate_public_history_without_restarting():
    skill = meta.MetaSkill("Inspect evidence before intervening", ("train",))
    run = meta.DeploymentRun(skill, "heldout", "stable-environment", "Build a file")
    views = []
    def evolve(view):
        views.append(view)
        return meta.Edit("EVOLVE", "notice", "Check the output")
    run.checkpoint(evidence(1), evolve)
    run.checkpoint(evidence(2, True), evolve)
    assert not run.state["closed"]
    assert views[-1].trajectory == ("public observation 1", "public observation 2")
    assert views[-1].workspace_observations == ("visible artifact missing", "visible artifact missing")
    assert views[-1].edit_status_history == ("none", "none")
    assert views[-1].environment_id == views[0].environment_id
    assert len(views[-1].edits) == 1
    run.checkpoint(evidence(3, True), lambda _: meta.Edit("KEEP"))
    assert run.state["closed"]
    fresh = meta.DeploymentRun(skill, "another", "other-environment", "Another task")
    assert fresh.state["edits"] == () and fresh.skill.digest == run.skill.digest
    with pytest.raises(FrozenInstanceError):
        skill.text = "poisoned"


@pytest.mark.parametrize("field", ["hidden_verifier", "gold_answer", "test_score", "training_outcome"])
def test_meta_deployment_schema_rejects_privileged_fields(field):
    run = meta.DeploymentRun(meta.MetaSkill("Hold", ("train",)), "test", "env", "Do task")
    called = []
    with pytest.raises(ValueError):
        run.checkpoint(evidence() | {field: "secret"}, lambda x: called.append(x))
    assert not called and run.state["step"] == -1


def test_meta_rejects_train_overlap_oversized_and_failed_edits_atomically():
    skill = meta.MetaSkill("Hold", ("train",))
    with pytest.raises(ValueError):
        meta.DeploymentRun(skill, "train", "env", "task")
    run = meta.DeploymentRun(skill, "test", "env", "task", edit_limit=3)
    with pytest.raises(ValueError):
        run.checkpoint(evidence(), lambda _: meta.Edit("EVOLVE", "hook", "too long"))
    assert run.state["step"] == -1 and not run.state["edits"]
    with pytest.raises(ValueError):
        meta.Edit("KEEP", "notice", "hidden edit")


def test_car_formulae_and_first_selected_best_curve_are_distinct():
    assert car.normalized_reward(-2, "r2") == .25
    assert car.normalized_reward(3, "r2") == 1
    assert car.normalized_reward(6, "rmse", training_sd=2) == .25
    run = car.ClosedRun("t", 10, "accuracy", (car.Attempt("a", 2, .8), car.Attempt("b", 6, .5)), "b", True)
    values = car.score_run(run)
    assert values["initialization"] == .8 and values["outcome"] == .5
    assert values["search_utility"] == pytest.approx(.64)
    assert values["selection_regret"] == pytest.approx(.3)
    empty = car.ClosedRun("empty", 10, "accuracy", (), None, True)
    assert set(car.score_run(empty).values()) == {0.0}


def test_car_invalid_candidates_and_zero_before_first_valid_do_not_boost_auc():
    run = car.ClosedRun("t", 10, "accuracy", (car.Attempt("bad", 1, None, False),
        car.Attempt("a", 5, .5), car.Attempt("b", 10, 1.0)), "b", True)
    assert car.score_run(run)["search_utility"] == .25
    assert car.score_run(run)["initialization"] == .5


@pytest.mark.parametrize("kwargs", [dict(closed=False), dict(selected_id="oracle"),
    dict(attempts=(car.Attempt("a", 11, .8),)), dict(attempts=(car.Attempt("a", 5, .8), car.Attempt("b", 2, .9))),
    dict(attempts=(car.Attempt("a", 1, .8, False),)), dict(attempts=(car.Attempt("a", 1, math.nan),))])
def test_car_rejects_live_invalid_or_unselected_hidden_records(kwargs):
    fields = dict(task_id="t", budget=10, metric="accuracy", attempts=(car.Attempt("a", 2, .8),), selected_id="a", closed=True)
    with pytest.raises(ValueError):
        car.ClosedRun(**(fields | kwargs))


def test_car_excludes_first_task_and_balances_streams_not_task_counts():
    def run(task, value):
        return car.ClosedRun(task, 10, "accuracy", (car.Attempt("a", 0, value),), "a", True)
    stateful, reset = (run("t1", 1), run("t2", .6)), (run("t1", 0), run("t2", .5))
    gain = car.paired_stream(stateful, reset)
    assert gain["outcome"] == pytest.approx(10)
    assert car.family_balanced((gain, {k: 0 for k in gain}))["outcome"] == pytest.approx(5)
    with pytest.raises(ValueError):
        car.paired_stream(stateful, (reset[1], reset[0]))


def ticket(limit=4):
    skill = "Send approved objects only.\nDo not exceed the task amount."
    ref = rt.SourceRef(1, 2, skill)
    grant = rt.Grant("send", "report", frozenset({"approved", "other"}))
    return rt.compile_ticket(task_id="task", skill=skill, host_grants=(grant,), selected_grants=(grant,),
                             host_budget=10, recipient="approved", validator_id="object", limit=limit,
                             references={name: ref for name in rt.OBLIGATIONS})


def test_runtime_source_binding_and_grant_attenuation():
    t = ticket()
    with pytest.raises(FrozenInstanceError):
        t.limit = 20
    grant = rt.Grant("send", "report", frozenset({"approved"}))
    expanded = rt.Grant("send", "report", frozenset({"attacker"}))
    for selected, ref in [((expanded,), rt.SourceRef(1, 1, "source")), ((grant,), rt.SourceRef(1, 1, "not source"))]:
        with pytest.raises(ValueError):
            rt.compile_ticket(task_id="t", skill="source", host_grants=(grant,), selected_grants=selected,
                              host_budget=10, recipient="approved", validator_id="object", limit=4,
                              references={name: ref for name in rt.OBLIGATIONS})


def test_runtime_gate_denies_before_unknown_and_only_allow_spends():
    gate = rt.Gate(ticket(), {"object": lambda _: None}, audit_key=b"k" * 32)
    sent = []
    assert gate.dispatch(rt.Request("a", "send", "report", "approved", b"ok"), sent.append)["decision"] == "Defer"
    assert gate.dispatch(rt.Request("b", "send", "report", "other", b"ok"), sent.append)["decision"] == "Deny"
    assert gate.used == 0 and not sent


def test_runtime_replay_and_concurrent_quota_are_atomic_and_recorded_before_send():
    key = b"k" * 32
    gate = rt.Gate(ticket(limit=4), {"object": lambda _: True}, audit_key=key)
    observed = []
    def forward(request):
        assert gate.records[-1]["request_id"] == request.request_id
        observed.append(request.request_id)
    def submit(i):
        return gate.dispatch(rt.Request(str(i), "send", "report", "approved", b"ok"), forward)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = list(pool.map(submit, range(12)))
    assert sum(row["decision"] == "Allow" for row in results) == 2
    assert len(observed) == 2 and gate.used == 4
    again = submit(observed[0])
    assert again["replayed"] and not again["forwarded"] and len(observed) == 2
    assert rt.verify_records(gate.records, key, gate.ticket.ticket_id)
    corrupt = [dict(row) for row in gate.records]
    corrupt[0]["amount_bytes"] = 0
    assert not rt.verify_records(corrupt, key, gate.ticket.ticket_id)
    with pytest.raises(ValueError):
        gate.dispatch(rt.Request(observed[0], "send", "report", "approved", b"different"), forward)


def test_runtime_callback_failure_never_silently_resends_or_restores_quota():
    gate = rt.Gate(ticket(), {"object": lambda _: True}, audit_key=b"k" * 32)
    request = rt.Request("x", "send", "report", "approved", b"ok")
    def failed(_):
        raise RuntimeError("delivery outcome unknown")
    with pytest.raises(RuntimeError):
        gate.dispatch(request, failed)
    assert gate.used == 2 and len(gate.records) == 1
    assert gate.dispatch(request, failed)["replayed"]


@pytest.mark.parametrize("module", [meta, car, rt])
def test_fixed_components_remain_cpu_diagnostics(module):
    assert module.REQUIRES_GPU_VALIDATION is False
    for seed in (42, 43, 44):
        result = module.diagnostic(seed)
        assert result["seed"] == seed and result["diagnostic_only"]
        assert result["evaluation_tier"] == "l1_mechanism" and all(result["checks"].values())
    with pytest.raises(ValueError):
        module.diagnostic(device="cuda")


@pytest.mark.parametrize("key", ["meta-square", "continual-autoresearch", "runtime-tickets", "rsi-dojo"])
def test_agent_intake_has_complete_reviewed_bilingual_and_learning_sources(key):
    root = Path(__file__).resolve().parents[2]
    spec = json.loads((root / f"src/auto_research/paper_specs/catalog/agent-research/{key}.json").read_text())
    assert spec["review_done"] and spec["full_experiment_review_done"]
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert not spec["automatic_retry"] and not spec["automatic_implementation_queue"]
    assert not spec["evolve_integrated"] and not spec["promotion_eligible"]
    assert spec["code_status"] and spec["first_author_affiliation"] and spec["published_at"].endswith("Z")
    page = root / "docs" / spec["detail_path"]
    cn = page.read_bytes()
    english = page.with_name("README-en.md").read_text()
    assert f'<!-- source-sha256: {hashlib.sha256(cn).hexdigest()} -->' in english
    assert "[简体中文](README.md)" in english and (page.parent / "assets/paper-figure-01.png").is_file()
    for heading in ["论文信息", "核心公式", "高成本完整实验", "代码映射"]:
        assert heading in cn.decode()
    identity = "agent-research:" + key
    bank = json.loads((root / "docs/learning/questions/nov04b-agent.json").read_text())["papers"][identity]["questions"]
    overlay = json.loads((root / "docs/en/learning/translations/qa-nov04b-agent.json").read_text())["units"]
    assert {q["level"] for q in bank} == {"basics", "mechanism", "comparison", "implementation"}
    for q in bank:
        for section in q["source_sections"]:
            assert re.search(r"^#{1,6} " + re.escape(section) + r"$", cn.decode(), re.MULTILINE)
        translated = overlay[f"qa/{identity}/{q['id']}"]
        digest = hashlib.sha256(json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        assert translated["reviewed"] and translated["source_sha256"] == digest
        assert set(translated["fields"]) == {"question", "answer", "example"}
    if key == "rsi-dojo":
        assert spec["implementation_status"] == "deferred_high_cost" and spec["local_operator"] is None
        assert not (page.parent / "metrics").exists()
    else:
        assert spec["implementation_status"] == "component_only" and not spec["requires_gpu_validation"]
