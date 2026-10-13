"""Prompt/parser interface tests; CPU fixtures are not capability evidence."""
import json
import hashlib
from pathlib import Path

import pytest

from auto_research.reproductions.skilldreamer.algorithm import (
    capability_context, execute_agent, parse_capability_assessment, parse_object,
)


DECISIONS = ("MATCH", "PARTIAL_MATCH", "NO_MATCH", "NO_CAPABILITY_GAP")


def test_prompt_explicitly_states_every_strict_csi_format_requirement():
    prompt = capability_context("QUESTION_ONLY", [], [], {}, 0, 8)
    assert "five nonempty" in prompt
    assert "LABEL: value" in prompt
    assert "DECISION must start with exactly one of MATCH, PARTIAL_MATCH, NO_MATCH, NO_CAPABILITY_GAP" in prompt
    assert "After these five lines, output one JSON object" in prompt
    assert '"tool":"calculator","arguments":{"expression":"..."}' in prompt
    assert '"tool":"finish","arguments":{"answer":"..."}' in prompt
    assert "Do not search/install/create skills" in prompt
    assert "Pseudo skills are not available here" in prompt


@pytest.mark.parametrize("decision", DECISIONS)
def test_placeholder_template_covers_all_decisions_without_preselecting_one(decision):
    prompt = capability_context("QUESTION_ONLY", [], [], {}, 0, 8)
    lines = [line for line in prompt.splitlines() if line.startswith(
        ("SUBGOAL:", "EVIDENCE:", "CAPABILITY:", "DECISION:", "NEXT:"))]
    assert len(lines) == 5
    assert all(line.split(":", 1)[1].strip().startswith("<") for line in lines)
    values = {"SUBGOAL": "fixture subgoal", "EVIDENCE": "fixture observation",
              "CAPABILITY": "fixture requirement", "DECISION": decision, "NEXT": "fixture next action"}
    response = "\n".join(line.split(":", 1)[0] + ": " + values[line.split(":", 1)[0]] for line in lines)
    assessment = parse_capability_assessment(response)
    assert assessment["DECISION"] == decision


@pytest.mark.parametrize("decision", ["Load the arithmetic skill.", "Use the rates skill to calculate the reduced hourly wage."])
def test_historical_natural_language_decisions_remain_rejected(decision):
    response = ("SUBGOAL: fixture\nEVIDENCE: fixture\nCAPABILITY: fixture\nDECISION: " + decision
                + '\nNEXT: fixture\n{"skill_id":null,"tool":"calculator","arguments":{"expression":"2+3"}}')
    assert parse_object(response)["tool"] == "calculator"
    with pytest.raises(ValueError, match="unknown capability decision"):
        parse_capability_assessment(response)


@pytest.mark.parametrize("failure", ["missing_next", "empty_next", "bare_label", "bad_json"])
def test_prompt_fix_does_not_relax_existing_parsers_or_execute_invalid_output(failure):
    lines = ["SUBGOAL: fixture", "EVIDENCE: fixture", "CAPABILITY: fixture", "DECISION: MATCH", "NEXT: fixture"]
    action = json.dumps({"skill_id": None, "tool": "calculator", "arguments": {"expression": "2+3"}})
    if failure == "missing_next":
        lines.pop()
    elif failure == "empty_next":
        lines[-1] = "NEXT:"
    elif failure == "bare_label":
        lines[0] = "SUBGOAL"
    else:
        action = "skill_id=null tool=calculator arguments={expression:2+3}"
    response = "\n".join([*lines, action])
    outcome = execute_agent("QUESTION_ONLY", lambda _: response, [], action_budget=8)
    assert outcome["generation_errors"] == outcome["model_calls"] == 24
    assert outcome["executed_actions"] == 0 and outcome["submitted_answer"] is None


def test_public_negative_probe_preserves_actual_cost_scope_and_old_source():
    root = Path(__file__).resolve().parents[1]
    path = root / "docs/reproductions/2609.01642-skilldreamer/metrics/public-a100-validation-negative-d8603f65.json"
    artifact = json.loads(path.read_text())
    assert artifact["schema_version"] == 2 and artifact["manifest_ref"] == "reproduction:skilldreamer"
    assert artifact["diagnostic_only"] is True and artifact["promotion_eligible"] is False
    assert artifact["not_gpu_receipt"] is True and artifact["gpu_validation_passed"] is False
    assert artifact["provenance"]["code_commit"] == "0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e"
    assert artifact["provenance"]["probe_source"]["commit"] == "d8603f65b207e5345f156621f840c69a24ecace2"
    protocol = artifact["evaluation_protocol"]
    assert protocol["seeds"] == [42] and protocol["formal_comparison"] is False
    assert protocol["validation_ids"] == ["13", "1", "4", "6", "23", "21", "14", "15"]
    assert protocol["validation_only"] is True
    assert all(protocol[name] is False for name in ("gold_present", "scorer_present", "evaluation_ids_used", "official_test_opened"))
    assert artifact["provenance"]["dataset_fingerprint"] == hashlib.sha256(json.dumps(artifact["dataset"], sort_keys=True).encode()).hexdigest()
    records = artifact["raw_artifacts"]
    for record in records.values():
        content = (root / record["artifact_path"]).read_bytes()
        assert hashlib.sha256(content).hexdigest() == record["sha256"]
        assert all(word not in content.lower() for word in (b"/users/", b"/home/", b"forge-codex", b"bytedance", b"hostname", b"driver_version", b"ssh "))
    raw = json.loads((root / records["seed42.json"]["artifact_path"]).read_text())
    assert raw["status"] == "completed_validation_probe"  # completed invocation, not successful core execution
    assert artifact["execution_checks"] == raw["execution_checks"] == {
        "psg_episodes": 7, "hsr_episodes": 7, "actual_csi_assessments": 2,
        "loaded_skill_episodes": 2, "executed_actions": 0}
    assert artifact["metrics"]["model_calls"] == raw["model_calls"] == 210
    assert artifact["metrics"]["generated_tokens"] == raw["generated_tokens"] == 29194
    assert artifact["metrics"]["wall_seconds"] == raw["wall_seconds"] < 600
    assert all(row.get("submitted_answer") is None for row in raw["episodes"])
    assert artifact["diagnosis"]["complete_valid_csi_with_rejected_action_json"] == 0


def test_skill_prompt_explicitly_shares_baseline_tool_semantics():
    prompt = capability_context("QUESTION_ONLY", [], [], {}, 0, 8)
    assert "Only calculator and finish are environment tools." in prompt
    assert "Only arithmetic expressions are supported." in prompt
    assert "calculator returns a value but does not submit an answer" in prompt
    assert "finish submits the answer you derive from the question and observed results, then terminates the episode" in prompt
    assert "Completing the task requires you to explicitly choose finish; no automatic submission occurs" in prompt


def test_skill_loading_and_assessment_are_not_additional_environment_tools():
    prompt = capability_context("QUESTION_ONLY", [], [], {}, 0, 8)
    assert "Capability assessment is the five assessment lines, not a tool" in prompt
    assert "A candidate skill_id is loaded by the executor" in prompt
    assert "asks for a fresh action after showing the verified gallery procedure" in prompt
    assert "load_skill and assess_capability are not tools" in prompt


@pytest.mark.parametrize("tool", ["calculator", "load_skill", "assess_capability"])
def test_api_wording_does_not_auto_correct_tools_or_force_finish(tool):
    response = ("SUBGOAL: fixture\nEVIDENCE: fixture\nCAPABILITY: fixture\nDECISION: NO_CAPABILITY_GAP\nNEXT: fixture\n"
                + json.dumps({"skill_id": None, "tool": tool, "arguments": {"expression": "2+3"}}))
    outcome = execute_agent("QUESTION_ONLY", lambda _: response, [], action_budget=8)
    assert outcome["executed_actions"] == outcome["model_calls"] == 8
    assert outcome["submitted_answer"] is None
    assert outcome["tool_errors"] == (0 if tool == "calculator" else 8)
    assert outcome["generation_errors"] == 0
