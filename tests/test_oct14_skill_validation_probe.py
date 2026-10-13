"""Validation-only protocol guards; CPU fixtures are not model evidence."""
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
import time

import pytest

spec = importlib.util.spec_from_file_location("skill_probe", Path(__file__).resolve().parents[1] / "scripts/probe_oct14_skilldreamer_validation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture_questions(tmp_path, monkeypatch):
    rows = [{"id": identifier, "question": "CPU fixture question"} for identifier in module.VALIDATION_IDS]
    path = tmp_path / "questions.jsonl"
    content = "".join(json.dumps(row) + "\n" for row in rows).encode()
    digest = hashlib.sha256(content).hexdigest()
    monkeypatch.setattr(module, "QUESTIONS_SHA256", digest)
    source = {"files": {path.name: digest}, "public_id": "openai/grade-school-math",
              "revision": "3101c7d5072418e28b9008a6636bde82a006892c", "source_split": "train",
              "parent_24_rows_sha256": "8f33a9f7a44067e362458e4daf0eb1ad629a2aac2f44ffefe731e36b19dcb8c1",
              "validation_ids": list(module.VALIDATION_IDS), "scope": "fixed_original_validation_only",
              "gold_present": False, "scorer_present": False, "evaluation_ids_used": False, "official_test_opened": False}
    path.write_bytes(content)
    (tmp_path / "provenance.json").write_text(json.dumps(source))
    return path, rows, source


def test_exact_eight_question_only_validation_ids_are_accepted(tmp_path, monkeypatch):
    path, rows, source = fixture_questions(tmp_path, monkeypatch)
    assert module.questions_only(path) == (rows, source)


@pytest.mark.parametrize("failure", ["answer", "evaluation_id", "changed_question", "gold_flag", "scorer_flag", "evaluation_flag"])
def test_gold_evaluation_ids_or_unverified_inputs_cannot_enter_probe(tmp_path, monkeypatch, failure):
    path, rows, source = fixture_questions(tmp_path, monkeypatch)
    if failure == "answer":
        rows[0]["answer"] = "forbidden fixture gold"
    elif failure == "evaluation_id":
        rows[0]["id"] = "19"
    elif failure == "changed_question":
        rows[0]["question"] = "substituted question"
    else:
        source[{"gold_flag": "gold_present", "scorer_flag": "scorer_present", "evaluation_flag": "evaluation_ids_used"}[failure]] = True
    content = "".join(json.dumps(row) + "\n" for row in rows).encode()
    if failure in {"answer", "evaluation_id"}:
        digest = hashlib.sha256(content).hexdigest()
        monkeypatch.setattr(module, "QUESTIONS_SHA256", digest)
        source["files"][path.name] = digest
    path.write_bytes(content)
    (tmp_path / "provenance.json").write_text(json.dumps(source))
    with pytest.raises(ValueError):
        module.questions_only(path)


def budget():
    return {"seed": 42, "max_new_tokens": 256, "action_budget": 8, "top_k": 3,
            "question_limit": 8, "calls_limit_per_episode": 30, "calls_limit_total": 240,
            "total_wall_limit_seconds": 600, "device": "cuda", "algorithm_commit": module.ALGORITHM_COMMIT}


def test_original_psg_and_csi_call_limits_are_preserved():
    config = budget()
    module.fixed_budget(config)
    assert config["calls_limit_per_episode"] == 1 + 5 + 8 * 3
    assert config["calls_limit_total"] == config["calls_limit_per_episode"] * 8


@pytest.mark.parametrize("field,value", [("max_new_tokens", 257), ("action_budget", 9), ("top_k", 4),
                                       ("calls_limit_total", 241), ("total_wall_limit_seconds", 601), ("seed", True)])
def test_probe_cannot_raise_original_fixed_budget_or_change_seed(field, value):
    config = budget()
    config[field] = value
    with pytest.raises(ValueError):
        module.fixed_budget(config)


def bound_runner(tmp_path, monkeypatch):
    commit = "a" * 40
    root = tmp_path / ("auto-research-oct14-" + commit[:8])
    path = root / "scripts/probe_oct14_skilldreamer_validation.py"
    path.parent.mkdir(parents=True)
    path.write_text("CPU source binding fixture only")
    (root / ".source-commit").write_text(commit + "\n")
    monkeypatch.setattr(module, "__file__", str(path))
    return {"probe_source_commit": commit, "probe_source_root": str(root),
            "probe_source_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}, path


def test_probe_runner_is_bound_separately_from_original_algorithm(tmp_path, monkeypatch):
    config, _ = bound_runner(tmp_path, monkeypatch)
    actual = module.runner_binding(config)
    assert actual["commit"] == config["probe_source_commit"]
    assert actual["commit"] != module.ALGORITHM_COMMIT
    assert actual["sha256"] == config["probe_source_sha256"]


@pytest.mark.parametrize("failure", ["outer", "marker", "sha", "commit"])
def test_unfrozen_or_changed_probe_runner_is_rejected(tmp_path, monkeypatch, failure):
    config, path = bound_runner(tmp_path, monkeypatch)
    if failure == "outer":
        monkeypatch.setattr(module, "__file__", str(tmp_path / "dirty-outer/scripts/probe.py"))
    elif failure == "marker":
        (path.parents[1] / ".source-commit").write_text("b" * 40)
    elif failure == "sha":
        path.write_text("changed uncommitted fixture")
    else:
        config["probe_source_commit"] = "b" * 40
    with pytest.raises(ValueError):
        module.runner_binding(config)


def test_hard_deadline_interrupts_one_blocking_call_and_restores_signal():
    previous = signal.getsignal(signal.SIGALRM)
    start = time.monotonic()
    with pytest.raises(TimeoutError):
        with module.hard_wall(0.03):
            time.sleep(1)
    assert time.monotonic() - start < 0.5
    assert signal.getsignal(signal.SIGALRM) == previous
    assert signal.getitimer(signal.ITIMER_REAL)[0] == 0


@pytest.mark.parametrize("failure", ["runtime", "timeout"])
def test_failure_preserves_partial_trace_and_never_signs_completed(tmp_path, monkeypatch, failure):
    output = tmp_path / "probe.json"
    original_deadline = module.hard_wall
    supplied = []

    def short_fixture_deadline(seconds):
        supplied.append(seconds)
        return original_deadline(0.03)

    def failed_execution(config, target):
        module.persist(target.with_suffix(".partial.json"), {"status": "running", "episodes": [{"id": "13", "model_calls": 1}]})
        target.with_suffix(".trace.jsonl").write_text('{"event":"CPU fixture attempt retained"}\n')
        if failure == "runtime":
            raise RuntimeError("CPU fixture generation failure")
        time.sleep(1)

    monkeypatch.setattr(module, "hard_wall", short_fixture_deadline)
    monkeypatch.setattr(module, "_execute_probe", failed_execution)
    with pytest.raises((RuntimeError, TimeoutError)):
        module.run(budget(), output)
    assert supplied == [600]  # production budget is not relaxed for tests
    retained = json.loads(output.read_text())
    assert retained["status"] == ("failed" if failure == "runtime" else "timed_out")
    assert retained["episodes"] == [{"id": "13", "model_calls": 1}]
    assert retained["capability_receipt"] is False
    assert output.with_suffix(".trace.jsonl").read_text() == '{"event":"CPU fixture attempt retained"}\n'
    assert json.loads(output.with_suffix(".partial.json").read_text()) == retained
