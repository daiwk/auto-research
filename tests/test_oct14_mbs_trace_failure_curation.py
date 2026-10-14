"""Pure synthetic fixtures: no local runs, models, CUDA, or dataset contents."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/curate_oct14_mbs_trace_failures.py"


def curator():
    spec = importlib.util.spec_from_file_location("mbs_failure_curator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(short="b9086275"):
    m = curator()
    commit = m.COMMITS[short]
    hashes = {p: hashlib.sha256(p.encode()).hexdigest() for p in m.SOURCE_PATHS}
    contract = {"source_commit": commit, "source_file_sha256": hashes}
    c = {**m.CONFIG, **{k: "/private/" + k for k in m.PATH_FIELDS}}
    command = ["/private/jev-closeout-venv/bin/python", "-u", f"/private/auto-research-oct14-{short}/scripts/run_oct13_post_training.py",
               "--method", "magicbeanstalk", "--config", f"/private/auto-research-post-training-{short}/queue/oct14_execution-mbs-bounded-v1.json",
               "--seed", "42", "--output", f"/private/auto-research-oct14-{short}/runs/post-training-oct14/{m.RUN_IDS[short]}/{m.JOBS[short]}-s42/evidence"]
    launch = {**copy.deepcopy(contract), "seed": 42, "effective_config": c, "execution_config_sha256": m.CONFIG_SHA,
              "command": command, "job": {"key": m.JOBS[short], "method": "magicbeanstalk",
              "overrides": {}, "timeout_seconds": 1800}, "budget": dict(m.LAUNCH_BUDGET),
              "diagnostic_only": True, "formal_comparison": False, "gpu_grant_received": True,
              "gpu_slot_grant": "A100-post-training-explicit-slot", "launcher_source_sha256": m.LAUNCHER_SHA}
    resources = {}
    for role in ("student", "teacher"):
        files = {name: "a" * 64 for name in m.RESOURCE_FILES[role]}
        files.update(m.WEIGHTS[role])
        files["tokenizer.json"] = m.TOKENIZER_SHA
        resources[role] = {"public_id": c[role + "_id"], "revision": c[role + "_revision"],
                           "verified": True, "file_sha256": files, "vocabulary_sha256": "b" * 64}
    audit = {**copy.deepcopy(contract), "source_hashes_verified": True, "cuda_initialized": False,
             "model_instantiated": False, "exact_vocabulary_match": True,
             "execution_config_sha256": m.CONFIG_SHA, "public_train_only_holdout": dict(m.DATASET),
             "resources": resources}
    calibration = [{"training_index": i, "root_question_sha256": hashlib.sha256(str(i).encode()).hexdigest(),
                    "accepted": i in (4, 7, 8), "rewards": [0.] * 4 if i in (4, 7, 8) else [1.] * 4,
                    "truncated": [False] * 4} for i in range(16)]
    selection = {"hard_root_limit": 4, "calibrated_training_candidates": 16,
                 "calibration_audits": calibration, "verified_hard_roots_selected": 3,
                 "tree_construction_attempts": 3, "selected_training_root_indices": [4, 7, 8],
                 "paired_rl_root_indices": [], "method_and_control_use_same_root_pairs": True,
                 "precalibration_reused_without_duplicate_sampling": True}
    traces = []

    def trace(role, text="fixture response", **extra):
        x = {"role": role, "input_gold_scope": m.GOLD_SCOPES[role], "response_text": text,
             "response_token_ids": [1, 2], "generated_tokens": 2, "truncated": False,
             "response_text_sha256": hashlib.sha256(text.encode()).hexdigest(), **extra}
        traces.append(x)
        return x

    for row in calibration:
        for reward in row["rewards"]:
            trace("target_calibration", question_sha256=row["root_question_sha256"], reward=reward)
    for role in ("effectivity_student", "effectivity_teacher"):
        for _ in range(4):
            trace(role, question_sha256=calibration[4]["root_question_sha256"], reward=0., worked_example_count=0)
    nverify = 10 if short == "b9086275" else 5
    for i in range(nverify):
        accepted = i < (2 if short == "b9086275" else 1)
        root = 4 if i == 0 else 7 if i in (nverify - 4, nverify - 3) else 8 if i >= nverify - 2 else None
        attempt = (1 if i == (nverify - 4 if root == 7 else nverify - 2) else 2) if root in (7, 8) else (1 if i in (0, 1, 2, 4) else 2)
        trace("construction_verification", attempt=attempt,
              question_sha256=calibration[root]["root_question_sha256"] if root is not None else "c" * 64,
              verification_completed=True, accepted=accepted,
              reject_reason=None if accepted else "incorrect_independent_solution")
    children = [{"question": "independent question", "answer": "7", "trace": "worked solution"}] * 2
    for i in range(2):
        text = json.dumps(children) if short == "b9086275" else ('not JSON' if short == "773da4e3" and i == 0 else '[invalid outer ' + json.dumps(children[0]))
        trace("construction_teacher", text, operation="propose_children", parsing_completed=True,
              parsed_json_kind="list" if short == "b9086275" else ("NoneType" if text == "not JSON" else "dict"),
              reject_reason="no_json_value" if text == "not JSON" else None,
              proposed_problem_count=2 if short == "b9086275" else 0,
              schema_valid_problem_count=2 if short == "b9086275" else 0,
              schema_reject_reason=None if short == "b9086275" else "no_schema_valid_child")
    hard = [{"phase": "seed-hardness-calibration", "accepted": True, "rewards": [0.] * 4,
             "truncated": [False] * 4, "actual_precalibration_reused_without_resampling": True} for _ in range(3)]
    decomposition = [{"phase": "decomposition", "attempt": i + 1, "depth": 0, "accepted": False,
                      "reject_reason": "fewer_than_two_verified_children",
                      "proposed_children": 2 if short == "b9086275" else 0,
                      "verified_children": 1 if short == "b9086275" else 0} for i in range(2)]
    verify = [{"phase": "verify", "accepted": False, "depth": 0,
               "reject_reason": "independent_verification_failed",
               "question_sha256": calibration[i]["root_question_sha256"]} for i in (7, 8)]
    calls = {"evaluation": 4, "target_calibration": 16, "construction_verification": nverify,
             "effectivity_student": 1, "effectivity_teacher": 1, "construction_teacher": 2}
    tokens = {role: sum(x["generated_tokens"] for x in traces if x["role"] == role) for role in calls}
    tokens["evaluation"] = 8
    failure = {"status": "failed", "diagnostic_only": True, "error": m.ERROR,
               "construction_audits": [hard[0], *decomposition, hard[1], verify[0], hard[2], verify[1]],
               "construction_response_audits": traces, "hard_root_selection": selection,
               "cost": {"generation_calls": calls, "generated_tokens": tokens, "scored_response_tokens": {},
                        "frozen_encoder_forward_calls": 0, "frozen_encoder_input_tokens_including_prompt": 0,
                        "scope": "entire invocation, including training controls, profiling and evaluation",
                        "includes_rejected_and_profiling_generations": True}}
    return m, {"launch": launch, "exit_record": {"exit_code": 1, "elapsed_seconds": 10.,
                "not_a_gpu_validation_receipt": True}, "failure": failure, "contract": contract, "audit": audit,
                "config_sha256": m.CONFIG_SHA, "git_hashes": dict(hashes),
                "raw_hashes": {k: "d" * 64 for k in ("launch", "exit", "runtime", "failure")}}


@pytest.mark.parametrize("short", ["b9086275", "5c863ab8", "773da4e3"])
def test_both_negative_sources_have_measured_counts_without_receipt_or_private_trace(short):
    m, args = fixture(short)
    r = m.curate_bundle(**args)
    assert r["not_gpu_receipt"] and not r["whole_method_gpu_validation_passed"]
    assert r["diagnostic_only"] and not r["promotion_eligible"]
    assert r["aggregate_metrics"]["method_rl_updates"]["mean"] == 0
    assert r["aggregate_metrics"]["verified_hard_roots"]["mean"] == 3
    assert r["aggregate_metrics"]["invalid_outer_json_proposals"]["mean"] == (0 if short == "b9086275" else 2)
    assert len(r["executed_source_sha256"]) == 54
    output = json.dumps(r)
    assert "/private/" not in output and "response_text\"" not in output and "response_token_ids" not in output
    assert r["execution_checks"]["gold_access_roles"]["construction_teacher"] == "training-construction-context"


@pytest.mark.parametrize("case", ["commit", "git_sha", "audit_sha", "source_count", "seed", "argv_seed",
    "argv_extra", "budget", "steps", "config_sha", "paired", "root", "calibration", "rl", "rc0", "wall",
    "nan", "response_sha", "response_token", "tokens_length", "role", "scope", "cost", "parse_repair",
    "weight", "dataset", "pass", "decomposition", "argv_source", "argv_config", "argv_output", "launcher",
    "grant", "cost_extra", "selection_extra", "audit_extra", "verify_question"])
def test_fail_closed_on_wrong_binding_budget_trace_or_fake_success(case):
    m, args = fixture("5c863ab8")
    args = copy.deepcopy(args)
    l, r, a = args["launch"], args["failure"], args["audit"]
    if case == "commit": l["source_commit"] = "f" * 40
    elif case == "git_sha": args["git_hashes"][next(iter(args["git_hashes"]))] = "f" * 64
    elif case == "audit_sha": a["source_file_sha256"][next(iter(a["source_file_sha256"]))] = "f" * 64
    elif case == "source_count": args["contract"]["source_file_sha256"].pop(next(iter(args["contract"]["source_file_sha256"])))
    elif case == "seed": l["seed"] = 43
    elif case == "argv_seed": l["command"][l["command"].index("--seed") + 1] = "43"
    elif case == "argv_extra": l["command"] += ["--steps", "8"]
    elif case == "budget": l["job"]["timeout_seconds"] = 1801
    elif case == "steps": l["effective_config"]["steps"] = 3
    elif case == "config_sha": args["config_sha256"] = "f" * 64
    elif case == "paired": r["hard_root_selection"]["paired_rl_root_indices"] = [4]
    elif case == "root": r["hard_root_selection"]["selected_training_root_indices"] = [4, 7]
    elif case == "calibration": r["hard_root_selection"]["calibration_audits"][4]["truncated"][0] = True
    elif case == "rl": r["training"] = [{"optimizer_update_executed": True}]
    elif case == "rc0": args["exit_record"]["exit_code"] = 0
    elif case == "wall": args["exit_record"]["elapsed_seconds"] = 1801
    elif case == "nan": args["exit_record"]["elapsed_seconds"] = float("nan")
    elif case == "response_sha": r["construction_response_audits"][0]["response_text"] += "changed"
    elif case == "response_token": r["construction_response_audits"][0]["response_token_ids"][0] = -1
    elif case == "tokens_length": r["construction_response_audits"][0]["generated_tokens"] += 1
    elif case == "role": r["construction_response_audits"][0]["role"] = "mbs_rlvr"
    elif case == "scope": r["construction_response_audits"][0]["input_gold_scope"] = "parent-gold"
    elif case == "cost": r["cost"]["generated_tokens"]["target_calibration"] += 1
    elif case == "parse_repair": r["construction_response_audits"][-1]["parsed_json_kind"] = "list"
    elif case == "weight": a["resources"]["student"]["file_sha256"]["model.safetensors"] = "f" * 64
    elif case == "dataset": a["public_train_only_holdout"]["test_read"] = True
    elif case == "pass": r["status"] = "passed"
    elif case == "decomposition": r["construction_audits"][1]["verified_children"] = 2
    elif case == "argv_source": l["command"][2] = l["command"][2].replace("5c863ab8", "b9086275")
    elif case == "argv_config": l["command"][6] = l["command"][6].replace("5c863ab8", "b9086275")
    elif case == "argv_output": l["command"][10] = "/private/other/evidence"
    elif case == "launcher": l["launcher_source_sha256"] = "f" * 64
    elif case == "grant": l["gpu_slot_grant"] = "ungranted"
    elif case == "cost_extra": r["cost"]["hostname"] = "PRIVATE_HOST"
    elif case == "selection_extra": r["hard_root_selection"]["hostname"] = "PRIVATE_HOST"
    elif case == "audit_extra": r["construction_audits"][0]["hostname"] = "PRIVATE_HOST"
    elif case == "verify_question": next(x for x in r["construction_response_audits"] if x["role"] == "construction_verification")["question_sha256"] = "f" * 64
    with pytest.raises(ValueError):
        m.curate_bundle(**args)
