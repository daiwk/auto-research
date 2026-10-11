"""Forged-output tests only; fixture payloads never become measured metrics."""

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.agent_research.memento3 import Memento3


spec = importlib.util.spec_from_file_location("memento3_curator", Path(__file__).parents[2] / "scripts/curate_memento3_evidence.py")
curator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(curator)

SOURCE = '''def initialise(observation):
    return observation
def step(state, action):
    return state
def observe(state):
    return state
def goal(state):
    return state["completed"]
'''
INITIAL = {"grid": [[4, 3]], "completed": False, "terminated": False}


def fixture():
    calls = []
    def generate(role, prompt):
        text = json.dumps({"rulebook": {"rulebook": "Fixture state unchanged and completion preserved."},
                           "compile": {"source": SOURCE},
                           "faithfulness": {"faithful": True, "reason": "fixture"}}[role])
        calls.append({"role": role, "text": text, "input_tokens": 10, "output_tokens": 10,
                      "output_budget": 100, "budget_reached": False})
        return text
    controller = Memento3(generate, (0, 1, 2, 3), population=1, repair_attempts=1)
    controller.start(INITIAL)
    controller.update()
    raw = {"status": "completed", "paper": "2610.11794", "method": "memento3",
           "protocol": {"underlying_llm_frozen": True, "gold_plan_read": False,
                        "environment_source_read_by_policy": False, "test_read": False,
                        "code_as_model_not_handwritten_fallback": True, "semantic_judge_human_calibrated": False},
           "evaluation_tier": "l1_core_mechanism", "diagnostic_only": True,
           "formal_comparison": False, "paper_benchmark_reproduced": False,
           "checkpoint": {"model_id": curator.LARGE_MODEL, "revision": curator.LARGE_REVISION},
           "environment": {"id": "Gymnasium/FrozenLake-v1", "version": "1.1.1", "map_seed": 42,
                           "slippery": False, "size": 4},
           "implementation_commit": "a" * 40,
           "source_sha256": {p: hashlib.sha256(b"fixture").hexdigest() for p in curator.SOURCES},
           "checkpoint_calls": [{"input_tokens": 10, "output_tokens": 10} for _ in calls],
           "run": {"seed": 42, "population": 1, "initial_observation": INITIAL, "real_actions": 0,
                   "real_action_budget": 8, "goal_completed": False, "terminated": False,
                   "interactions": [], "calls": calls, "accepted_versions": 1,
                   "versions": controller.versions, "valid_final_members": 1, "events": controller.events}}
    return copy.deepcopy(raw)


def check(raw):
    return curator.curate(raw, git_show=lambda commit, path: b"fixture")


def test_curator_retains_diagnostic_failure_and_no_capability_claim():
    result = check(fixture())
    assert result["metrics"]["goal_completed"] == 0
    assert result["evaluation_protocol"]["diagnostic_only"] is True
    assert result["evaluation_protocol"]["formal_comparison"] is False


def test_false_source_commit_and_checkpoint_identity_rejected():
    raw = fixture()
    raw["source_sha256"][next(iter(curator.SOURCES))] = "0" * 64
    with pytest.raises(ValueError, match="source differs"):
        check(raw)
    raw = fixture()
    raw["checkpoint"]["revision"] = "0" * 40
    with pytest.raises(ValueError, match="checkpoint identity"):
        check(raw)


def test_handwritten_runtime_fallback_missing_from_checkpoint_calls_rejected():
    raw = fixture()
    raw["run"]["calls"][1]["text"] = '{"source":"different source"}'
    with pytest.raises(ValueError, match="not generated"):
        check(raw)


def test_semantic_reject_cannot_be_promoted_as_accepted():
    raw = fixture()
    raw["run"]["events"][0]["faithful"] = False
    with pytest.raises(ValueError, match="semantic"):
        check(raw)


def test_cell_mismatch_cannot_be_promoted_as_replay_consistent():
    raw = fixture()
    raw["run"].update(real_actions=1, valid_final_members=1)
    raw["run"]["interactions"] = [{"action": 0, "observation": {**INITIAL, "grid": [[3, 4]]}}]
    with pytest.raises(ValueError, match="final replay"):
        check(raw)


def test_full_benchmark_or_gold_exposure_rejected():
    raw = fixture()
    raw["paper_benchmark_reproduced"] = True
    with pytest.raises(ValueError, match="promoted"):
        check(raw)
    raw = fixture()
    raw["protocol"]["gold_plan_read"] = True
    with pytest.raises(ValueError, match="isolation"):
        check(raw)


def test_no_accepted_model_preserved_explicitly():
    raw = fixture()
    raw["run"].update(accepted_versions=0, versions=[], valid_final_members=0)
    raw["run"]["events"] = []
    result = check(raw)
    assert result["learning_status"] == "no_accepted_model"


def test_initially_accepted_but_falsified_model_never_labelled_as_success():
    raw = fixture()
    raw["run"].update(real_actions=1, valid_final_members=0)
    raw["run"]["interactions"] = [{"action": 0, "observation": {**INITIAL, "grid": [[3, 4]]}}]
    result = check(raw)
    assert result["learning_status"] == "falsified_generated_model"
    assert result["metrics"]["accepted_versions"] == 1
    assert result["metrics"]["valid_final_members"] == 0


def test_gpu_receipt_passed_is_execution_only_not_capability_success():
    raw = fixture()
    raw["accelerator"] = "NVIDIA A100-SXM4-80GB"
    raw["run"].update(real_actions=1, valid_final_members=0)
    raw["run"]["interactions"] = [{"action": 0, "observation": {**INITIAL, "grid": [[3, 4]]}}]
    result = curator.gpu_receipt(raw, check(raw))
    assert result["result"] == "passed"
    assert result["validation_scope"] == "mechanism_executed_only"
    assert result["capability_passed"] is False
    assert result["learning_status"] == "falsified_generated_model"


def test_gpu_receipt_cannot_pass_without_real_generated_model_interaction():
    raw = fixture()
    raw["accelerator"] = "NVIDIA A100-SXM4-80GB"
    with pytest.raises(ValueError, match="real interaction"):
        curator.gpu_receipt(raw, check(raw))


def test_executed_checkpoint_call_token_counter_mismatch_rejected():
    raw = fixture()
    raw["checkpoint_calls"][0]["output_tokens"] += 1
    with pytest.raises(ValueError, match="token budget"):
        check(raw)
