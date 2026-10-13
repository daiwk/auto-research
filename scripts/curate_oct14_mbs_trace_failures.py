#!/usr/bin/env python3
"""Fail-closed CPU curation of immutable failed MBS runs; never a receipt."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

COMMITS = {"b9086275": "b90862754bf51b1beeb5add3f7dc2a51ca00ace4",
           "5c863ab8": "5c863ab8fdee702ddb1abcda6b6255646dc832fd",
           "773da4e3": "773da4e31f5ee3de2b7e4b03b524d61a1513cbdf"}
JOBS = {"b9086275": "magicbeanstalk-trace", "5c863ab8": "magicbeanstalk-selfcontained",
        "773da4e3": "magicbeanstalk-json-contract"}
FILENAMES = {"b9086275": "public-a100-trace-failed-seed42-b9086275.json",
             "5c863ab8": "public-a100-selfcontained-failed-seed42-5c863ab8.json",
             "773da4e3": "public-a100-json-contract-failed-seed42-773da4e3.json"}
CONFIG_SHA = "0dd390a3b6aedb3b0bfb57d24d869cc1b108169aead88e2ea01f7f6cf33e5d9f"
LAUNCHER_SHA = "186a47f0e8a53b17595a52625dafdd0c8d24406c7ffe4631aa182338abd4cf30"
RUN_IDS = {"b9086275": "oct14-mbs-trace42-b908-attempt03", "5c863ab8": "oct14-mbs-selfcontained42-5c-attempt04",
           "773da4e3": "oct14-mbs-json-contract42-773-attempt05"}
ERROR = "no actual effectivity-validated, novel, verified, target-Goldilocks MBS descendant"
PATH_FIELDS = {"student_path", "teacher_path", "train_path", "validation_path", "split_manifest"}
CONFIG = {"student_id": "Qwen/Qwen2.5-0.5B-Instruct", "student_revision": "7ae557604adf67be50417f59c2c2f167def9a775",
          "teacher_id": "Qwen/Qwen2.5-7B-Instruct", "teacher_revision": "bb46c15ee4bb56c5b63245ef50fd7637234d6f75",
          "dataset_revision": "3101c7d5072418e28b9008a6636bde82a006892c", "context_limit": 4096,
          "device": "cuda", "train_examples": 16, "validation_examples": 4, "max_tokens": 1024,
          "learning_rate": 1e-5, "group": 4, "depth": 1, "decomposition_retries": 2,
          "synthesis_retries": 2, "teacher_attempts": 2, "steps": 2, "hard_root_limit": 4}
LAUNCH_BUDGET = {"budget_kind": "configured_upper_bounds_not_measured_cost", "response_cap": 1024,
                 "context_cap": 4096, "train_examples": 16, "validation_examples": 4,
                 "teacher_generated_tokens_upper": 303104, "student_generated_tokens_upper": 290816,
                 "student_scored_response_tokens_upper": 32768, "calibrated_seed_candidates_upper": 16,
                 "tree_construction_roots_upper": 4, "method_and_control_optimizer_steps_upper": 4}
DATASET = {"verified": True, "test_read": False, "source_id": "openai/grade-school-math",
           "source_revision": CONFIG["dataset_revision"],
           "source_sha256": "17f347dc51477c50d4efb83959dbb7c56297aba886e5544ee2aaed3024813465",
           "partition_sha256": {"train": "6b8672439c8cf6f6b6e65bf5f0e515fbf4c497c9066eefb62a6a6a61ced158e3",
                                "validation": "2cf1119ad7b2e31e825274487ef32c073e03a8ed44f08ecd3e0366c1f40ebdb7"},
           "partition": "normalized-question sha256 unsigned-prefix / 2^64 < 0.1 validation"}
TOKENIZER_SHA = "c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539"
WEIGHTS = {"student": {"model.safetensors": "fdf756fa7fcbe7404d5c60e26bff1a0c8b8aa1f72ced49e7dd0210fe288fb7fe"},
           "teacher": {"model-00001-of-00004.safetensors": "a1333e6293854747c481288ea83b348226af178dd565c49b6f9495ba1966aba7",
                       "model-00002-of-00004.safetensors": "f5d25a2772cb825164a2a2c0fb6d51a87e282abf21e4dd75bc5cfb3cd0ea6185",
                       "model-00003-of-00004.safetensors": "8efdec4c1bc12317ae1a38dc42b595ce777738a64deea3fcb8a0a91381bcdfd5",
                       "model-00004-of-00004.safetensors": "1a72d403cdf0c1ec3cb7f289f17b394a01e64394c2e9b3c0f94dbce3faf879bd"}}
COMMON_FILES = {"config.json", "generation_config.json", "merges.txt", "tokenizer.json", "tokenizer_config.json", "vocab.json"}
RESOURCE_FILES = {"student": COMMON_FILES | set(WEIGHTS["student"]),
                  "teacher": COMMON_FILES | set(WEIGHTS["teacher"]) | {"model.safetensors.index.json"}}
GOLD_SCOPES = {"target_calibration": "question-only-no-answer-or-trace",
               "construction_verification": "question-only-no-answer-or-trace",
               "effectivity_student": "question-only-no-answer-or-trace",
               "effectivity_teacher": "question-only-no-answer-or-trace",
               "construction_teacher": "training-construction-context"}
SOURCE_PATHS = {"scripts/prepare_soar_catalog_qa.py", "scripts/run_oct13_post_training.py",
                "scripts/diagnose_oct14_post_training.py", "scripts/diagnose_oct14_soar_format.py",
                "src/auto_research/oct12_public_sources.py", "src/auto_research/public_holdout.py"}
SOURCE_PATHS |= {"src/auto_research/post_training/" + p + ".py" for p in
                 ("oct10_checkpoint", "oct13_common", "proximal_checkpoint", "response_policy")}
for key in ("gppo_framework", "grpo_difficulty_curriculum", "magicbeanstalk", "progressive_contraction",
            "soar", "state_opd", "synthself", "tapo_trajectory", "upturn"):
    prefix = "src/auto_research/reproductions/" + key + "/"
    SOURCE_PATHS |= {prefix + p for p in ("__init__.py", "adapter.py", "paper.yaml")}
    SOURCE_PATHS.add(prefix + ("objective.py" if key in {"gppo_framework", "tapo_trajectory"} else "algorithm.py"))
    if key not in {"gppo_framework", "tapo_trajectory"}:
        SOURCE_PATHS.add(prefix + "checkpoint.py")
SOURCE_PATHS.add("src/auto_research/reproductions/state_opd/environment.py")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(value):
    return hashlib.sha256(value).hexdigest()


def hash_string(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def finite_tree(value):
    if isinstance(value, float):
        require(math.isfinite(value), "non-finite evidence")
    elif isinstance(value, dict):
        for child in value.values():
            finite_tree(child)
    elif isinstance(value, list):
        for child in value:
            finite_tree(child)


def first_json_value(text):
    """Exactly the executed historical first-decodable-value parser; no repair."""
    for i, character in enumerate(text):
        if character in "[{":
            try:
                return json.JSONDecoder().raw_decode(text[i:])[0]
            except json.JSONDecodeError:
                pass
    return None


def schema_valid_problem(value):
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) and value[k].strip()
                                             for k in ("question", "trace")):
        return False
    answer = value.get("answer")
    if type(answer) in (int, float):
        return not isinstance(answer, float) or math.isfinite(answer)
    return isinstance(answer, str) and bool(answer.strip())


def curate_bundle(*, launch, exit_record, failure, contract, audit, config_sha256, git_hashes, raw_hashes):
    """Pure checked transform; CLI supplies independently computed Git/raw hashes."""
    for record in (launch, exit_record, failure, contract, audit):
        finite_tree(record)
    commit = contract["source_commit"]
    short = next((s for s, c in COMMITS.items() if c == commit), None)
    require(short is not None, "only the actually executed immutable sources are supported")
    hashes = contract["source_file_sha256"]
    require(set(hashes) == SOURCE_PATHS and len(hashes) == 54 and all(hash_string(h) for h in hashes.values()),
            "exact 54-file frozen source scope required")
    require(git_hashes == hashes, "every source must match its executed Git blob")
    for record in (launch, audit):
        require(record.get("source_commit") == commit and record.get("source_file_sha256") == hashes,
                "source contract/audit/launch mismatch")
        require(record.get("execution_config_sha256") == config_sha256 == CONFIG_SHA, "canonical config mismatch")
    require(audit.get("source_hashes_verified") is True and audit.get("cuda_initialized") is False
            and audit.get("model_instantiated") is False and audit.get("exact_vocabulary_match") is True,
            "independent CPU source/resource audit required")
    require(audit.get("public_train_only_holdout") == DATASET, "fixed training-only public split identity required")
    c = launch["effective_config"]
    require(set(c) == set(CONFIG) | PATH_FIELDS and all(c[k] == v and type(c[k]) is type(v) for k, v in CONFIG.items()),
            "unchanged 16/group4/cap1024/depth1/two-retry/two-step budget required")
    require(all(isinstance(c[k], str) and c[k] for k in PATH_FIELDS), "explicit resource path bindings required")
    require(launch.get("seed") == 42 and launch.get("diagnostic_only") is True
            and launch.get("formal_comparison") is False and launch.get("gpu_grant_received") is True
            and launch.get("gpu_slot_grant") == "A100-post-training-explicit-slot"
            and launch.get("launcher_source_sha256") == LAUNCHER_SHA,
            "actual authorized seed42 diagnostic launch required")
    job = launch["job"]
    require(job.get("key") == JOBS[short] and job.get("method") == "magicbeanstalk"
            and job.get("overrides") == {} and job.get("timeout_seconds") == 1800, "original job/wall budget required")
    require(all(launch["budget"].get(k) == v for k, v in LAUNCH_BUDGET.items()), "launcher budget drift")
    command = launch["command"]
    require(isinstance(command, list) and len(command) == 11
            and all(isinstance(x, str) for x in command) and command[0].endswith("/jev-closeout-venv/bin/python")
            and command[1] == "-u"
            and command[2].endswith("/auto-research-oct14-" + short + "/scripts/run_oct13_post_training.py")
            and command[3:5] == ["--method", "magicbeanstalk"]
            and command[5] == "--config" and command[6].endswith("/auto-research-post-training-" + short + "/queue/oct14_execution-mbs-bounded-v1.json")
            and command[7:9] == ["--seed", "42"] and command[9] == "--output"
            and command[10].endswith("/auto-research-oct14-" + short + "/runs/post-training-oct14/" + RUN_IDS[short]
                                      + "/" + JOBS[short] + "-s42/evidence"), "exact actual argv; no extra or overridden flags")
    require(type(exit_record.get("exit_code")) is int and exit_record.get("exit_code") == 1
            and exit_record.get("not_a_gpu_validation_receipt") is True
            and type(exit_record.get("elapsed_seconds")) in (int, float)
            and 0 < exit_record.get("elapsed_seconds", 0) <= 1800, "actual bounded failure exit/wall required")
    require(failure.get("status") == "failed" and failure.get("diagnostic_only") is True and failure.get("error") == ERROR,
            "original construction failure cannot be relabeled")
    require(set(failure) == {"status", "diagnostic_only", "error", "construction_audits",
                            "construction_response_audits", "hard_root_selection", "cost"},
            "construction failed before RL; no training/result payload allowed")
    checkpoint = {}
    for role in ("student", "teacher"):
        resource = audit["resources"][role]
        files = resource["file_sha256"]
        require(resource.get("verified") is True and resource.get("public_id") == CONFIG[role + "_id"]
                and resource.get("revision") == CONFIG[role + "_revision"] and set(files) == RESOURCE_FILES[role]
                and all(hash_string(h) for h in files.values()) and files.get("tokenizer.json") == TOKENIZER_SHA
                and all(files.get(k) == v for k, v in WEIGHTS[role].items()), "public checkpoint identity/weights mismatch")
        require(hash_string(resource.get("vocabulary_sha256")), "verified vocabulary hash required")
        checkpoint[role] = {k: resource[k] for k in ("public_id", "revision", "file_sha256")}
    require(audit["resources"]["student"]["vocabulary_sha256"] == audit["resources"]["teacher"]["vocabulary_sha256"],
            "same exact student/teacher vocabulary required")
    selection = failure["hard_root_selection"]
    require(set(selection) == {"hard_root_limit", "calibrated_training_candidates", "calibration_audits",
            "verified_hard_roots_selected", "tree_construction_attempts", "selected_training_root_indices",
            "paired_rl_root_indices", "method_and_control_use_same_root_pairs", "precalibration_reused_without_duplicate_sampling"},
            "only sanitized selection fields may be published")
    require(selection.get("hard_root_limit") == 4 and selection.get("calibrated_training_candidates") == 16
            and selection.get("verified_hard_roots_selected") == selection.get("tree_construction_attempts") == 3
            and selection.get("selected_training_root_indices") == [4, 7, 8]
            and selection.get("paired_rl_root_indices") == []
            and selection.get("method_and_control_use_same_root_pairs") is True
            and selection.get("precalibration_reused_without_duplicate_sampling") is True, "actual three hard roots and empty paired set required")
    calibrations = selection["calibration_audits"]
    require(len(calibrations) == 16, "all 16 calibration attempts must remain visible")
    require(len({row["root_question_sha256"] for row in calibrations}) == 16, "distinct calibrated training questions required")
    for i, row in enumerate(calibrations):
        require(set(row) == {"training_index", "root_question_sha256", "accepted", "rewards", "truncated"},
                "only sanitized calibration fields may be published")
        rewards, truncated = row["rewards"], row["truncated"]
        require(row["training_index"] == i and hash_string(row["root_question_sha256"])
                and len(rewards) == len(truncated) == 4 and all(x in (0, 1) for x in rewards)
                and all(type(x) is bool for x in truncated)
                and row["accepted"] is (not any(rewards) and not any(truncated)), "calibration hard gate mismatch")
    require([x["training_index"] for x in calibrations if x["accepted"]] == [4, 7, 8], "hard roots must derive from actual outcomes")
    traces = failure["construction_response_audits"]
    roles = Counter()
    token_cost = Counter()
    safe_traces, proposals = [], []
    for response in traces:
        role = response["role"]
        tokens = response["response_token_ids"]
        require(role in GOLD_SCOPES and response.get("input_gold_scope") == GOLD_SCOPES[role], "actual gold access role mismatch")
        require(isinstance(response["response_text"], str)
                and sha(response["response_text"].encode()) == response.get("response_text_sha256")
                and isinstance(tokens, list) and 0 < len(tokens) <= 1024
                and all(type(t) is int and t >= 0 for t in tokens)
                and type(response["generated_tokens"]) is int and len(tokens) == response["generated_tokens"]
                and type(response["truncated"]) is bool, "actual response SHA/token/termination mismatch")
        roles[role] += 1
        token_cost[role] += len(tokens)
        if role != "construction_teacher":
            require(hash_string(response.get("question_sha256")), "response must bind actual question hash")
        if role in {"target_calibration", "effectivity_student", "effectivity_teacher"}:
            require(response.get("reward") in (0, 1) and (not response["truncated"] or response["reward"] == 0),
                    "actual external outcome mismatch")
        if role.startswith("effectivity_"):
            require(response.get("worked_example_count") == 0, "only actual unconditioned baseline was reached")
        if role == "construction_verification":
            require(response.get("verification_completed") is True and type(response.get("accepted")) is bool
                    and response.get("attempt") in (1, 2), "actual completed bounded verification required")
            reason = None if response["accepted"] else ("truncated_independent_solution" if response["truncated"] else "incorrect_independent_solution")
            require(response.get("reject_reason") == reason and not (response["accepted"] and response["truncated"]),
                    "independent verification result mismatch")
        if role == "construction_teacher":
            require(response.get("operation") == "propose_children" and response.get("parsing_completed") is True,
                    "only the two actual decomposition proposals were reached")
            value = None if response["truncated"] else first_json_value(response["response_text"])
            expected_reason = "truncated_json_response" if response["truncated"] else ("no_json_value" if value is None else None)
            count = min(3, sum(schema_valid_problem(v) for v in value)) if isinstance(value, list) else 0
            require(response.get("parsed_json_kind") == type(value).__name__
                    and response.get("proposed_problem_count") == (len(value) if isinstance(value, list) else 0)
                    and response.get("schema_valid_problem_count") == count
                    and response.get("reject_reason") == expected_reason
                    and response.get("schema_reject_reason") == (None if count else "no_schema_valid_child"),
                    "historical first-value parsing cannot be repaired or relabeled")
            try:
                json.loads(response["response_text"])
                outer_valid = True
            except json.JSONDecodeError:
                outer_valid = False
            proposals.append({"outer_json_valid": outer_valid, "historical_first_value_kind": type(value).__name__,
                              "schema_valid_children": count})
        safe = {k: response[k] for k in ("role", "input_gold_scope", "response_text_sha256", "generated_tokens", "truncated")}
        for k in ("question_sha256", "attempt", "reward", "accepted", "reject_reason", "operation"):
            if k in response:
                safe[k] = response[k]
        safe_traces.append(safe)
    expected_verify = 10 if short == "b9086275" else 5
    require(roles == {"target_calibration": 64, "effectivity_student": 4, "effectivity_teacher": 4,
                      "construction_verification": expected_verify, "construction_teacher": 2}, "complete actual response role counts required")
    for row in calibrations:
        actual = [t for t in traces if t["role"] == "target_calibration" and t["question_sha256"] == row["root_question_sha256"]]
        require([x["reward"] for x in actual] == row["rewards"] and [x["truncated"] for x in actual] == row["truncated"],
                "calibration must match its actual four responses")
    verified_count = sum(x["accepted"] for x in traces if x["role"] == "construction_verification")
    require(verified_count == (2 if short == "b9086275" else 1), "actual accepted verification count mismatch")
    for root in (4, 7, 8):
        actual = [x for x in traces if x["role"] == "construction_verification"
                  and x["question_sha256"] == calibrations[root]["root_question_sha256"]]
        require(([x["accepted"] for x in actual] == [True] and [x["attempt"] for x in actual] == [1]) if root == 4 else
                ([x["accepted"] for x in actual] == [False, False] and [x["attempt"] for x in actual] == [1, 2]),
                "root decision must match its actual independent verification responses")
    audits = failure["construction_audits"]
    require(len(audits) == 7 and [x["phase"] for x in audits] ==
            ["seed-hardness-calibration", "decomposition", "decomposition", "seed-hardness-calibration", "verify", "seed-hardness-calibration", "verify"],
            "failed construction stage sequence changed; no downstream stages or RL")
    for index in (0, 3, 5):
        require(set(audits[index]) == {"phase", "accepted", "rewards", "truncated", "actual_precalibration_reused_without_resampling"}
                and audits[index].get("accepted") is True and audits[index].get("rewards") == [0.] * 4
                and audits[index].get("truncated") == [False] * 4
                and audits[index].get("actual_precalibration_reused_without_resampling") is True, "hard-root calibration reuse mismatch")
    for i in (1, 2):
        require(set(audits[i]) == {"phase", "attempt", "depth", "accepted", "reject_reason", "proposed_children", "verified_children"}
                and audits[i].get("accepted") is False and audits[i].get("attempt") == i and audits[i].get("depth") == 0
                and audits[i].get("reject_reason") == "fewer_than_two_verified_children"
                and audits[i].get("proposed_children") == (2 if short == "b9086275" else 0)
                and audits[i].get("verified_children") == (1 if short == "b9086275" else 0), "actual two decomposition rejections required")
    for i, root in ((4, 7), (6, 8)):
        require(set(audits[i]) == {"phase", "accepted", "depth", "reject_reason", "question_sha256"}
                and audits[i].get("accepted") is False and audits[i].get("depth") == 0
                and audits[i].get("reject_reason") == "independent_verification_failed"
                and audits[i].get("question_sha256") == calibrations[root]["root_question_sha256"], "actual root verification rejection mismatch")
    require(all(x["schema_valid_children"] == (2 if short == "b9086275" else 0) for x in proposals)
            and all(x["outer_json_valid"] is (short == "b9086275") for x in proposals), "distinct actual parser outcomes required")
    cost = failure["cost"]
    require(set(cost) == {"generation_calls", "generated_tokens", "scored_response_tokens", "frozen_encoder_forward_calls",
            "frozen_encoder_input_tokens_including_prompt", "scope", "includes_rejected_and_profiling_generations"}
            and cost["scope"] == "entire invocation, including training controls, profiling and evaluation",
            "only sanitized complete cost fields may be published")
    calls = {"evaluation": 4, "target_calibration": 16, "construction_verification": expected_verify,
             "effectivity_student": 1, "effectivity_teacher": 1, "construction_teacher": 2}
    require(cost.get("generation_calls") == calls and set(cost["generated_tokens"]) == set(calls)
            and cost.get("scored_response_tokens") == {} and cost.get("frozen_encoder_forward_calls") == 0
            and cost.get("frozen_encoder_input_tokens_including_prompt") == 0
            and cost.get("includes_rejected_and_profiling_generations") is True, "actual complete pre-RL cost required")
    for role, tokens in cost["generated_tokens"].items():
        require(type(tokens) is int and 0 < tokens <= calls[role] * (4 if role in {"target_calibration", "effectivity_student", "effectivity_teacher"} else 1) * 1024,
                "measured token count exceeds unchanged bound")
        if role != "evaluation":
            require(tokens == token_cost[role], "generation cost must exactly equal actual response lengths")
    require(set(raw_hashes) == {"launch", "exit", "runtime", "failure"} and all(hash_string(h) for h in raw_hashes.values()),
            "all immutable raw byte hashes required")
    metrics = {"verified_hard_roots": 3, "construction_attempts": 3, "paired_rl_roots": 0,
               "method_rl_updates": 0, "control_rl_updates": 0, "decomposition_proposal_calls": 2,
               "schema_valid_proposed_children": sum(x["schema_valid_children"] for x in proposals),
               "invalid_outer_json_proposals": sum(not x["outer_json_valid"] for x in proposals),
               "independent_verification_calls": expected_verify, "accepted_independent_verifications": verified_count,
               "rejected_independent_verifications": expected_verify - verified_count,
               "generated_response_tokens": sum(cost["generated_tokens"].values()),
               "invocation_elapsed_seconds": exit_record["elapsed_seconds"]}
    path = "docs/reproductions/2610.12659-magicbeanstalk/metrics/" + FILENAMES[short]
    sanitized_command = ["python", "-u", "scripts/run_oct13_post_training.py", "--method", "magicbeanstalk",
                         "--config", "<config>/oct14_execution-mbs-bounded-v1.json", "--seed", "42", "--output", "<run>/evidence"]
    # Explicit whitelist: neither raw response text/token IDs nor machine/config
    # paths, package versions, or arbitrary extra audit fields enter publication.
    return {"schema_version": 2, "adapter_key": "magicbeanstalk", "manifest_ref": "reproduction:magicbeanstalk",
            "method": "magicbeanstalk", "measured_locally": True, "diagnostic_only": True, "promotion_eligible": False,
            "not_gpu_receipt": True, "whole_method_gpu_validation_passed": False, "seeds": [42],
            "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"},
            "seed_results": [{"seed": 42, "device": "cuda", "diagnostic_only": True, "return_code": 1,
                              "execution_status": "failed-construction", "metrics": metrics}],
            "aggregate_metrics": {k: {"mean": v, "std": 0., "n": 1} for k, v in metrics.items()},
            "dataset": DATASET, "checkpoint": checkpoint, "executed_source_sha256": hashes,
            "execution_checks": {"return_code": 1, "configured_wall_cap_seconds": 1800,
                "invocation_elapsed_seconds": exit_record["elapsed_seconds"], "configured_budget": CONFIG,
                "hard_root_selection": selection, "construction_audits": audits,
                "sanitized_response_audits": safe_traces, "proposal_parsing": proposals, "measured_cost": cost,
                "method_rl_updates": 0, "control_rl_updates": 0, "gold_access_roles": GOLD_SCOPES,
                "hard_root_count_scope": "zero-success nontruncated target-policy calibration, not proof that all three independent teacher verifications passed",
                "effectivity_conditioned_test_reached": False, "synthesis_reached": False,
                "target_policy_goldilocks_reached": False, "baseline_validation_generation_calls": 4},
            "failure_interpretation": ("Two valid JSON decomposition proposals each produced two schema-valid children but only one verified child; roots7/8 independently failed verification."
                if short == "b9086275" else
                "Both decomposition outer JSON responses were invalid; the unchanged historical parser decoded an inner dict, not an array, yielding zero proposed children. No response repair was performed; roots7/8 independently failed verification."
                if short == "5c863ab8" else
                "Both decomposition outer JSON responses remained invalid after the serialization prompt: the historical parser returned no JSON value once and an inner dict once, yielding zero proposed children. No response repair or extra retry was performed; roots7/8 independently failed verification."),
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": [42], "formal_comparison": False,
                "promotion_eligible": False, "test_used_for_selection": False,
                "claim_policy": "failed bounded construction diagnostic; no surviving descendant, no RL update, no capability claim",
                "train_only_scope": "calibration/construction only; the original invocation also executed four validation baseline generations"},
            "provenance": {"code_commit": commit, "artifact_path": path, "execution_config_sha256": config_sha256,
                "dataset_fingerprint": sha(json.dumps(DATASET, sort_keys=True).encode()), "raw_results_sha256": raw_hashes,
                "actual_command_sanitized": sanitized_command, "command_path_relocations_only": True,
                "checkpoint_committed": False, "raw_responses_and_token_ids_committed": False},
            "limitations": ["One seed failed real CUDA construction, not a passed GPU validation receipt or formal comparison.",
                "Training construction teacher sees parent/candidate training answers and traces; independent verification sees only the question.",
                "The historical parser and strict numeric verifier were not repaired or relaxed; all negative outcomes remain visible.",
                "Baseline validation generation cost is included, but no post-training assessment or training/control update occurred."]}


def curate(directory, contract_path, audit_path, config_path, *, repo):
    """Read immutable evidence and verify all Git blobs; never open heldout data."""
    read = lambda p: json.loads(Path(p).read_text())
    contract = read(contract_path)
    commit = contract["source_commit"]
    git_hashes = {p: sha(subprocess.check_output(["git", "show", commit + ":" + p], cwd=repo)) for p in contract["source_file_sha256"]}
    directory = Path(directory)
    files = {"launch": directory / "launch.json", "exit": directory / "exit.json",
             "runtime": directory / "runtime.log", "failure": directory / "evidence/failure.json"}
    raw_hashes = {k: sha(p.read_bytes()) for k, p in files.items()}
    return curate_bundle(launch=read(files["launch"]), exit_record=read(files["exit"]), failure=read(files["failure"]),
                         contract=contract, audit=read(audit_path), git_hashes=git_hashes, raw_hashes=raw_hashes,
                         config_sha256=sha(json.dumps(read(config_path), sort_keys=True).encode()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("directory", "contract", "audit", "config", "repo"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.directory, args.contract, args.audit, args.config, repo=args.repo),
                     ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
