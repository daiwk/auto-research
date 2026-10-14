"""CPU-only guards for a sanitized historical eight-question negative probe."""
import importlib.util
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def module():
    spec = importlib.util.spec_from_file_location("negative47", ROOT / "scripts/curate_oct14_skill_validation_negative_47f.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def trace():
    return [{"event": "generation_attempt", "call": 1, "id": "13", "prompt": "CPU fixture question, never public"},
            {"event": "generation_response", "call": 1, "id": "13", "response": "CPU fixture response, never public"}]


def test_trace_exact_pairing_retains_no_public_content():
    attempts, responses = module().validate_trace(trace(), expected_calls=1)
    assert attempts[1]["id"] == "13" and responses[1].startswith("CPU fixture")


@pytest.mark.parametrize("failure", ["duplicate", "unknown_response", "id", "order", "missing", "event", "empty_prompt", "bool_call"])
def test_trace_invalid_call_or_episode_binding_rejected(failure):
    events = trace()
    if failure == "duplicate": events += trace()
    elif failure == "unknown_response": events[1]["call"] = 2
    elif failure == "id": events[1]["id"] = "1"
    elif failure == "order": events.reverse()
    elif failure == "missing": events.pop()
    elif failure == "event": events[1]["event"] = "untracked"
    elif failure == "empty_prompt": events[0]["prompt"] = ""
    else: events[0]["call"] = True
    with pytest.raises(ValueError): module().validate_trace(events, expected_calls=1)


@pytest.mark.parametrize("field,value", [("accuracy", 0), ("prompt", "private"), ("token_ids", [1]),
    ("command", ["python", "/tmp/private"]), ("text", "host.example"), ("text", "/home/user"),
    ("text", "CUDA build"), ("result", "passed")])
def test_public_negative_record_rejects_forbidden_content_or_claim(field, value):
    with pytest.raises(ValueError): module().sanitize_guard({field: value})


def test_public_negative_record_actual_metrics_and_scope():
    path = ROOT / "docs/reproductions/2609.01642-skilldreamer/metrics/public-a100-validation-no-submit-seed42-47f0e9ce.json"
    payload = json.loads(path.read_text())
    module().sanitize_guard(payload)
    assert payload["not_gpu_receipt"] is True and payload["gpu_validation_passed"] is False
    assert payload["evaluation_protocol"]["tier"] == "l1_mechanism"
    assert payload["evaluation_protocol"]["validation_only"] is True
    assert payload["evaluation_protocol"]["formal_comparison"] is False
    assert payload["evaluation_protocol"]["scorer_present"] is False
    assert payload["provenance"]["code_commit"] == module().ALGORITHM_COMMIT
    assert payload["provenance"]["probe_source"]["commit"] == module().PROBE_COMMIT
    expected = {"model_calls": 163, "generated_tokens": 19466, "actual_csi_assessments": 58,
        "loaded_skill_episodes": 7, "env_step_calls": 50, "calculator_attempts": 50,
        "calculator_successes": 46, "calculator_errors": 4, "unknown_tool_calls": 0,
        "finish_calls": 0, "submitted_answers": 0}
    assert all(payload["metrics"][key] == value for key, value in expected.items())
    assert payload["metrics"]["runner_wall_seconds"] == 404.9072179440409
    assert payload["metrics"]["invocation_elapsed_seconds"] == 405.8045824728906
    assert payload["cpu_replay"]["exact_runtime_episode_ids"] == ["1", "4", "6", "23", "21", "14", "15"]
    assert payload["cpu_replay"]["runtime_prompts_and_all_outcome_fields_exact"] is True
    assert payload["private_original_artifact_hashes"]["seed42.trace.jsonl"]["sha256"] == "1777f98145777026888817d0cf6e7a138178a2be94c9a7de21c98b9e612763ee"
    assert set(payload["private_original_artifact_hashes"]) == set(module().RAW_SHA)
    assert all(not record["public_copy"] for record in payload["private_original_artifact_hashes"].values())
    assert payload["provenance"]["execution_config_sha256"] == module().RESOURCE_SHA["probe-d5bf41b2.json"]
    assert payload["provenance"]["algorithm_archive_sha256"] == module().ALGORITHM_ARCHIVE_SHA
    assert payload["provenance"]["probe_archive_sha256"] == module().PROBE_ARCHIVE_SHA
    assert len(payload["checkpoint"]["files"]) == 11 and len(payload["encoder"]["files"]) == 6


@pytest.mark.parametrize("failure", ["result", "partial", "trace", "exit", "launcher", "config", "audit", "questions"])
def test_any_pinned_input_byte_change_fails_closed(tmp_path, failure):
    curator = module()
    path = tmp_path / failure
    content = b"CPU fixture original bytes, never model evidence"
    path.write_bytes(content)
    expected = {failure: hashlib.sha256(content).hexdigest()}
    assert curator.pinned_files(tmp_path, expected)[failure]["public_copy"] is False
    path.write_bytes(content + b"changed")
    with pytest.raises(ValueError, match="historical artifact bytes differ"):
        curator.pinned_files(tmp_path, expected)


def test_public_record_has_no_raw_content_arrays_or_device_build():
    payload = json.loads((ROOT / module().ARTIFACT).read_text())
    content = json.dumps(payload).lower()
    for field in ('"episodes"', '"prompt"', '"question"', '"answer"', '"response"', '"token_ids"', '"input_ids"', '"argv"'):
        assert field not in content
    assert all(fragment not in content for fragment in ("/tmp/", "/users/", "/home/", "bytedance", "forge-codex", "torch2.", "driver_version"))
