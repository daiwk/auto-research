"""CPU protocol correctness and failure isolation; no model-capability claims."""
from dataclasses import asdict, replace
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys

import pytest

from auto_research.agent_research import agent_perturb as perturb, alpha_diana as diana


@pytest.mark.parametrize("changes", [
    {"memory_scope": "unknown"}, {"workers": 0}, {"workers": True}, {"max_retries": -1},
    {"memory_scope": "frozen", "memory_writable": True},
    {"memory_scope": "cross_task", "workers": 2},
    {"memory_scope": "within_task", "memory_writable": True, "max_retries": 1},
])
def test_alpha_rejects_unsafe_or_invalid_session_contracts(changes):
    with pytest.raises(ValueError):
        diana.SessionPolicy(**changes)


def test_alpha_retry_keeps_sample_identity_and_counts_failed_attempt_cost():
    runner = diana.ProtocolRunner(diana.SessionPolicy(max_retries=1))
    calls = []

    def actor(public, session):
        assert set(asdict(public)) == {"task_id", "problem"}
        assert not session.workspace and not session.memory
        calls.append(public)
        session.workspace["x"] = 1
        session.memory["x"] = 1
        if len(calls) == 1:
            raise diana.ExecutionFailure(output_tokens=5)
        return diana.AgentOutput("7", 11)

    runner.run_sample(diana.PublicTask("t", "compute 3+4"), "s", actor=actor,
                      grader=lambda answer, reference: answer == reference, reference="7")
    assert len(runner.records) == 2
    assert {r.sample_id for r in runner.records} == {"s"}
    assert [r.attempt for r in runner.records] == [0, 1]
    result = diana.summarize(runner.records, requested_samples=[("t", "s")])
    assert result["correct_samples"] == 1 and result["known_output_tokens_all_attempts"] == 16
    assert result["complete_output_tokens_per_correct"] == 16
    with pytest.raises(ValueError, match="already requested"):
        runner.run_sample(diana.PublicTask("t", "public"), "s", actor=actor,
                          grader=lambda *a: True, reference="secret")


@pytest.mark.parametrize("scope", ["within_task", "cross_task"])
def test_alpha_failed_shared_write_is_not_rolled_back_or_retried(scope):
    runner = diana.ProtocolRunner(diana.SessionPolicy(memory_scope=scope, memory_writable=True))
    seen = []

    def actor(public, session):
        assert not session.workspace
        seen.append(dict(session.memory))
        session.memory["count"] = session.memory.get("count", 0)+1
        session.workspace["scratch"] = True
        if public.problem == "fail":
            raise diana.ExecutionFailure(output_tokens=2)
        return diana.AgentOutput("ok", 1)

    runner.run_sample(diana.PublicTask("a", "fail"), "1", actor=actor, grader=lambda *a: True, reference=None)
    runner.run_sample(diana.PublicTask("a", "pass"), "2", actor=actor, grader=lambda *a: True, reference=None)
    runner.run_sample(diana.PublicTask("b", "pass"), "1", actor=actor, grader=lambda *a: True, reference=None)
    assert seen[:2] == [{}, {"count": 1}]
    assert seen[2] == ({"count": 2} if scope == "cross_task" else {})
    assert len(runner.records) == 3
    runner.run_sample(diana.PublicTask("a", "pass"), "3", actor=actor, grader=lambda *a: True, reference=None)
    assert seen[-1] == ({"count": 3} if scope == "cross_task" else {})


def test_alpha_frozen_memory_and_private_reference_never_reach_actor():
    runner = diana.ProtocolRunner(diana.SessionPolicy(memory_scope="frozen"), initial_memory={"public_note": 1})
    secret = {"ground_truth": "not actor data"}
    captured = []

    def actor(public, session):
        captured.append((asdict(public), dict(session.memory)))
        session.memory["public_note"] = 999
        return diana.AgentOutput("prediction")

    for index in range(2):
        runner.run_sample(diana.PublicTask(str(index), "public"), "s", actor=actor,
                          grader=lambda answer, ref: ref == secret, reference=secret)
    assert all(memory == {"public_note": 1} for _, memory in captured)
    assert all(set(public) == {"task_id", "problem"} for public, _ in captured)
    result = diana.summarize(runner.records, requested_samples=[("0", "s"), ("1", "s")])
    assert result["token_recording_coverage"] == 0 and result["complete_output_tokens_per_correct"] is None


def _record(attempt=0, **changes):
    return replace(diana.AttemptRecord("t", "s", attempt, "completed", "scored", True, 2, .1), **changes)


def test_alpha_latest_not_best_and_requested_missing_denominator():
    rows = [_record(), _record(1, correct=False)]
    result = diana.summarize(rows, requested_samples=[("t", "s"), ("missing", "s")])
    assert result["correct_samples"] == 0 and result["missing_samples"] == 1
    assert result["unscored_samples"] == 1 and result["score_coverage"] == .5
    assert result["known_output_tokens_all_attempts"] == 4
    assert diana.summarize(rows[::-1], requested_samples=[("t", "s")])["correct_samples"] == 0
    for bad in ([rows[0], rows[0]], [_record(2)]):
        with pytest.raises(ValueError, match="contiguous"):
            diana.summarize(bad, requested_samples=[("t", "s")])
    with pytest.raises(ValueError, match="outside"):
        diana.summarize(rows, requested_samples=[("other", "s")])


def test_alpha_grader_failure_retained_not_actor_failure():
    runner = diana.ProtocolRunner(diana.SessionPolicy())

    def grader(*args):
        raise RuntimeError("outage")

    record = runner.run_sample(diana.PublicTask("t", "public"), "s", actor=lambda *a: diana.AgentOutput("x", 3),
                               grader=grader, reference="private")
    assert record.execution_status == "completed" and record.score_status == "unscored"
    assert record.correct is None and record.failure_kind == "grader:RuntimeError"
    with pytest.raises(ValueError):
        _record(execution_status="failed")
    with pytest.raises(ValueError):
        _record(elapsed_seconds=math.nan)


def _instance():
    return perturb.PublicInstance("t", "add 3 4", "use addition", "backup_y=4", {"add": "two integers"})


def _pair(**changes):
    kwargs = dict(target="U", kind="redundant", replacement="add 3 4 irrelevant",
                  generator_id="generator", verifier_id="independent-verifier",
                  semantic_verifier=lambda *a: perturb.SemanticChecks(True, True, True, True),
                  native_validator=lambda *a: True, evaluation_annotation={"private_recovery": "ask first"})
    kwargs.update(changes)
    return perturb.prepare_pair(_instance(), **kwargs)


@pytest.mark.parametrize("changes", [
    {"target": "unknown"}, {"kind": "unknown"}, {"replacement": "add 3 4"},
    {"verifier_id": "generator"}, {"native_validator": lambda *a: False},
    {"semantic_verifier": lambda *a: perturb.SemanticChecks(True, False, True, True)},
    {"semantic_verifier": lambda *a: perturb.SemanticChecks(True, True, False, True)},
    {"semantic_verifier": lambda *a: perturb.SemanticChecks(True, True, True, False)},
    {"semantic_verifier": lambda *a: perturb.SemanticChecks(1, True, True, True)},
])
def test_perturb_rejects_invalid_unverified_or_nonindependent_pairs(changes):
    with pytest.raises(ValueError):
        _pair(**changes)


def test_perturb_verifier_failure_closed_and_cannot_mutate_saved_surfaces():
    def failing(*args):
        raise RuntimeError("verifier unavailable")

    with pytest.raises(ValueError, match="failed closed"):
        _pair(semantic_verifier=failing)

    def editing(clean, candidate, *args):
        clean.tool_contract.clear()
        candidate.tool_contract["forged"] = "not retained"
        return perturb.SemanticChecks(True, True, True, True)

    pair = _pair(semantic_verifier=editing)
    assert pair.clean.tool_contract == pair.perturbed.tool_contract == _instance().tool_contract
    assert pair.clean.procedural_spec == pair.perturbed.procedural_spec


def test_perturb_actor_receives_neither_gold_nor_condition_or_clean_pair():
    seen, graded = [], []
    reference = {"gold": "7"}

    def actor(public):
        seen.append(asdict(public))
        public.tool_contract["mutation"] = "actor local"
        return perturb.ActorOutput("7", 5)

    def grader(answer, private):
        graded.append(private)
        private["gold"] = "mutated scorer copy"
        return .75

    pair = _pair()
    result = perturb.evaluate_pair(pair, actor=actor, native_grader=grader, reference=reference)
    assert len(seen) == 2 and all(set(public) == {"task_id", *perturb.SURFACES.values()} for public in seen)
    assert reference == {"gold": "7"} and len(graded) == 2
    assert "mutation" not in pair.clean.tool_contract and result.clean.score == .75


@pytest.mark.parametrize("surface", ["tool_contract", "evaluation_annotation"])
def test_perturb_rejects_mutation_after_semantic_verification(surface):
    pair = _pair()
    if surface == "tool_contract":
        pair.perturbed.tool_contract["after_verification"] = "changed"
    else:
        pair.evaluation_annotation["after_verification"] = "changed"
    with pytest.raises(ValueError, match="changed after verification"):
        perturb.evaluate_pair(pair, actor=lambda public: perturb.ActorOutput("7"),
                              native_grader=lambda *a: 1., reference="private")


def test_perturb_coverage_bounds_retain_failed_and_unscored_pairs():
    good = perturb.EpisodeOutcome("completed", 1., 5)
    wrong = perturb.EpisodeOutcome("completed", 0., 3)
    unscored = perturb.EpisodeOutcome("completed", None, 7)
    failed = perturb.EpisodeOutcome("failed", None, None)
    rows = [perturb.PairedOutcome("a", "U", "missing", good, wrong),
            perturb.PairedOutcome("b", "U", "missing", good, unscored),
            perturb.PairedOutcome("c", "U", "missing", failed, good)]
    scope = [(row.task_id, row.target, row.kind) for row in rows]
    result = perturb.paired_metrics(rows, requested_pairs=scope)
    assert result["requested_pairs"] == 3 and result["pair_coverage"] == 1/3
    assert result["clean_unscored"] == result["perturbed_unscored"] == 1
    assert result["paired_drop_observed"] == 1
    assert result["paired_drop_all_requested_lower_bound"] == 0
    assert result["paired_drop_all_requested_upper_bound"] == 2/3
    assert result["known_recorded_tokens_all_episodes"] == 25
    with pytest.raises(ValueError, match="duplicate"):
        perturb.paired_metrics(rows+rows[:1], requested_pairs=scope)
    missing = perturb.paired_metrics(rows[:1], requested_pairs=scope)
    assert missing["requested_pairs"] == 3 and missing["missing_pair_records"] == 2
    assert missing["clean_unscored"] == missing["perturbed_unscored"] == 2
    assert missing["pair_coverage"] == 1/3
    with pytest.raises(ValueError, match="outside"):
        perturb.paired_metrics(rows, requested_pairs=scope[:1])
    for value in (math.nan, 1.1, -1, True):
        with pytest.raises(ValueError):
            perturb.EpisodeOutcome("completed", value, 0)


def _runner_module():
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location("oct19_agent_runner", root / "scripts/run_oct19_agent_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_seeded_runner_executes_records_and_nonconstant_negative_controls():
    module = _runner_module()
    assert set(module.FUNCTIONS) == {"alpha-diana", "agent-perturb"}
    for function in module.FUNCTIONS.values():
        first, second = function(42), function(43)
        assert first["fixture_sha256"] != second["fixture_sha256"]
        assert first["metrics"] != second["metrics"] and first["protocol_records"]
        assert any("negative_control" in key and value > 0 for key, value in first["metrics"].items())
    alpha = module.alpha_diana_diagnostic(44)
    assert alpha["metrics"]["gold_fields_exposed_to_actor"] == 0
    assert module.agent_perturb_diagnostic(44)["metrics"]["perturbation_families"] == 12


def test_runner_output_immutable_and_source_hash_scope(tmp_path):
    module = _runner_module()
    output = tmp_path / "fresh.json"
    command = [sys.executable, str(module.ROOT / "scripts/run_oct19_agent_components.py"),
               "--seeds", "42,43,44", "--code-commit", "a"*40, "--output", str(output)]
    subprocess.run(command, cwd=module.ROOT, check=True, capture_output=True, text=True)
    result = json.loads(output.read_text())
    assert set(result["executed_source_sha256"]) == set(module.SOURCE_PATHS)
    assert result["device"] == "cpu" and result["diagnostic_only"]
    assert not result["promotion_eligible"] and not result["evolve_integrated"]
    assert all(c["full_experiment_status"] == "not_reproduced_high_cost" for c in result["components"].values())
    original = output.read_bytes()
    repeated = subprocess.run(command, cwd=module.ROOT, capture_output=True, text=True)
    assert repeated.returncode != 0 and output.read_bytes() == original
