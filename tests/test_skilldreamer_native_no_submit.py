"""Public fixed-source CPU replay; tool invocations are not task success."""
import hashlib
import importlib
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/reproductions/2609.01642-skilldreamer/metrics"
ARTIFACT = json.loads((BASE / "public-a100-validation-no-submit-5c07ef42.json").read_text())
RAW = {name: ROOT / record["artifact_path"] for name, record in ARTIFACT["raw_artifacts"].items()}
RUN = json.loads(RAW["seed42.json"].read_text())
TRACE = [json.loads(line) for line in RAW["seed42.trace.jsonl"].read_text().splitlines()]
ATTEMPTS = {row["call"]: row for row in TRACE if row["event"] == "generation_attempt"}
RESPONSES = {row["call"]: row["response"] for row in TRACE if row["event"] == "generation_response"}


def test_native_no_submit_evidence_remains_validation_only_and_hash_bound():
    assert ARTIFACT["diagnostic_only"] is True and ARTIFACT["promotion_eligible"] is False
    assert ARTIFACT["not_gpu_receipt"] is True and ARTIFACT["capability_receipt"] is False
    assert ARTIFACT["gpu_validation_passed"] is False
    assert ARTIFACT["provenance"]["code_commit"] == "701f45007be75cf6153f98812ef94e087c94a8f0"
    assert ARTIFACT["provenance"]["probe_source"]["commit"] == "5c07ef42bbb008e7adc3fc03fd5e85695c2bcc86"
    protocol = ARTIFACT["evaluation_protocol"]
    assert protocol["validation_only"] is True and protocol["formal_comparison"] is False
    assert protocol["validation_ids"] == ["13", "1", "4", "6", "23", "21", "14", "15"]
    assert all(protocol[key] is False for key in ("gold_present", "scorer_present", "evaluation_ids_used", "official_test_opened"))
    assert ARTIFACT["provenance"]["dataset_fingerprint"] == hashlib.sha256(json.dumps(ARTIFACT["dataset"], sort_keys=True).encode()).hexdigest()
    for record in [*ARTIFACT["raw_artifacts"].values(), *ARTIFACT["cpu_replay_source"].values()]:
        content = (ROOT / record["artifact_path"]).read_bytes()
        assert hashlib.sha256(content).hexdigest() == record["sha256"]
        assert all(word not in content.lower() for word in (b"/users/", b"/home/", b"forge-codex", b"bytedance", b"hostname", b"driver_version", b"ssh "))
    assert len(ATTEMPTS) == len(RESPONSES) == RUN["model_calls"] == 159
    assert RUN["generated_tokens"] == 19369
    assert ARTIFACT["metrics"]["finish_calls"] == ARTIFACT["metrics"]["submitted_answers"] == 0
    assert ARTIFACT["metrics"]["env_step_calls"] == 56
    assert ARTIFACT["metrics"]["calculator_attempts"] == 54
    assert ARTIFACT["metrics"]["calculator_successes"] == 48
    assert ARTIFACT["metrics"]["calculator_errors"] == 6
    assert ARTIFACT["metrics"]["unknown_tool_calls"] == 2
    exit_record = json.loads(RAW["exit.sanitized.json"].read_text())
    assert exit_record["exit_code"] == 0 and exit_record["elapsed_seconds"] < 600
    assert all(row.get("submitted_answer") is None for row in RUN["episodes"])
    analysis = json.loads(RAW["submission-analysis.json"].read_text())
    for identifier, successes, errors, unknown in (("1", 1, 6, 1), ("4", 7, 0, 1)):
        rows = [row for row in analysis["calls"] if row["id"] == identifier and row["stage"] == "environment_step"]
        assert sum(row["actual_added_observation"].startswith("Calculator result:") for row in rows) == successes
        assert sum(row["actual_added_observation"].startswith("Calculator error:") for row in rows) == errors
        assert sum(row["actual_added_observation"].startswith("Invalid action schema.") for row in rows) == unknown


@pytest.mark.parametrize("identifier", ["1", "4", "6", "23", "21", "14", "15"])
def test_independent_frozen_source_replays_actual_calls_and_observations(monkeypatch, identifier):
    # Import byte-identical 701f source in an isolated namespace, not the current
    # potentially clarified prompt. CPU replay is not a fresh model experiment.
    algorithm_path = ROOT / ARTIFACT["cpu_replay_source"]["skilldreamer/algorithm.py"]["artifact_path"]
    monkeypatch.syspath_prepend(str(algorithm_path.parents[2]))
    algorithm = importlib.import_module("skill_probe_701f.skilldreamer.algorithm")
    environment = importlib.import_module("skill_probe_701f.state_opd.environment")
    assert Path(algorithm.__file__).resolve() == algorithm_path.resolve()
    environment_path = ROOT / ARTIFACT["cpu_replay_source"]["state_opd/environment.py"]["artifact_path"]
    assert Path(environment.__file__).resolve() == environment_path.resolve()
    gallery_path = ROOT / "src/auto_research/reproductions/skilldreamer/gallery.json"
    assert hashlib.sha256(gallery_path.read_bytes()).hexdigest() == RUN["protocol"]["source_sha256"]["skilldreamer/gallery.json"]
    gallery = {row["id"]: algorithm.Skill(**row) for row in json.loads(gallery_path.read_text())}
    episode = next(row for row in RUN["episodes"] if row["id"] == identifier)
    calls = iter(call for call, item in ATTEMPTS.items() if item["id"] == identifier and "Loaded verified gallery skill procedures:" in item["prompt"])
    first = next(row for row in ATTEMPTS.values() if row["id"] == identifier and "Loaded verified gallery skill procedures:" in row["prompt"])
    question = first["prompt"].split("Task: ", 1)[1].split("\nObserved execution history: ", 1)[0]

    def generate(prompt):
        call = next(calls)
        assert ATTEMPTS[call]["prompt"] == prompt
        return RESPONSES[call]

    replay = algorithm.execute_agent(question, generate, [gallery[name] for name in episode["retrieved_skills"]], action_budget=8)
    assert all(episode[key] == value for key, value in replay.items())
    assert replay["executed_actions"] == 8 and replay["submitted_answer"] is None
    assert next(calls, None) is None
