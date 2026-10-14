#!/usr/bin/env python3
"""Two immutable schema-failure branches; no model/GPU, repair or rebinding."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

COMMITS = {"f92413aa": "f92413aabaef0a7d84dcddcb3d4064f5c2d464a3",
           "ce4a4a34": "ce4a4a34520419a50fb730d93967aaed5024fa77"}
JOBS = {"f92413aa": "magicbeanstalk-schema", "ce4a4a34": "magicbeanstalk-schema-order"}
CONFIG_SHA = "6717f5dd647b812e5fc6dcdcd91b3f089e2a55003bc6ee68ac76d88319a7b1df"
LAUNCHER_SHA = "ca10aeb13530aff36e2ba29ae097ed3a11ee235c023ffedfaa2c84a8413cf8f9"
RUN_IDS = {"f92413aa": "oct14-mbs-schema42-attempt06", "ce4a4a34": "oct14-mbs-schema-order42-attempt07"}
PINNED = {"xgrammar": "0.2.8", "apache-tvm-ffi": "0.1.11", "pydantic": "2.12.5",
          "pydantic-core": "2.41.5", "annotated-types": "0.7.0", "typing-inspection": "0.4.2", "typing-extensions": "4.15.0"}
# Frozen actual sorted serialization; never derive from newer live source.
SCHEMA_SHAS = {"blueprint_and_novelty": "73e3e05f28e47881109e697b3f8ea64b1a8cadafb1231fab0d952b66aedb2ca5",
               "compose": "3c44af604a1fac7a22e27b09d529becb8e33c26ec3cecda014035066aba6f086",
               "harder_leaf": "3c44af604a1fac7a22e27b09d529becb8e33c26ec3cecda014035066aba6f086",
               "propose_children": "0a4eeac64e58ec46fc6333fa3bbd125e53bb62be08f63cf6aa2af3bc0a3d5f43",
               "scaffold_safe": "120398dbde513fb336619f2e3535be7b21ac22f055a8886f2e12dfa5f0fd0e67"}
ORDERED_SCHEMA_SHAS = {"blueprint_and_novelty": "c4f8a00e63a0417315216e6e6afd0333324604f38dfa5a823dc267a131efc3bf",
                      "compose": "8768cc6bbb0654c28b9b457654cddb07fde9ae9e7a7a11f8198cf41856835e55",
                      "harder_leaf": "8768cc6bbb0654c28b9b457654cddb07fde9ae9e7a7a11f8198cf41856835e55",
                      "propose_children": "b60afb6eb71743e2e47aec78354124df48a40d97b48591592c0214c0c30b29d4",
                      "scaffold_safe": "deb8fa68986813699f24e819d86090e5a964f48dffb3937a6388ef08de11e9c6"}
ERROR = "no actual effectivity-validated, novel, verified, target-Goldilocks MBS descendant"
PATH_FIELDS = {"student_path", "teacher_path", "train_path", "validation_path", "split_manifest"}
CONFIG = {"student_id": "Qwen/Qwen2.5-0.5B-Instruct", "student_revision": "7ae557604adf67be50417f59c2c2f167def9a775",
          "teacher_id": "Qwen/Qwen2.5-7B-Instruct", "teacher_revision": "bb46c15ee4bb56c5b63245ef50fd7637234d6f75",
          "dataset_revision": "3101c7d5072418e28b9008a6636bde82a006892c", "context_limit": 4096,
          "device": "cuda", "train_examples": 16, "validation_examples": 4, "max_tokens": 1024,
          "learning_rate": 1e-5, "group": 4, "depth": 1, "decomposition_retries": 2,
          "synthesis_retries": 2, "teacher_attempts": 2, "steps": 2, "hard_root_limit": 4, "construction_json_schema": True}
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


def schema_valid_problem(value):
    if not isinstance(value, dict) or not all(isinstance(value.get(k), str) and value[k].strip()
                                             for k in ("question", "trace")):
        return False
    answer = value.get("answer")
    if type(answer) in (int, float):
        return not isinstance(answer, float) or math.isfinite(answer)
    return isinstance(answer, str) and bool(answer.strip())


def curate_bundle(*, launch, exit_record, failure, contract, audit, dependency_audit, grammar_audit,
                  config_sha256, git_hashes, raw_hashes):
    """Pure checked transform; CLI supplies independently computed Git/raw hashes."""
    for record in (launch, exit_record, failure, contract, audit, dependency_audit, grammar_audit):
        finite_tree(record)
    commit = contract["source_commit"]
    short = next((s for s, c in COMMITS.items() if c == commit), None)
    require(short is not None, "only the actually executed immutable sources are supported")
    ordered = short == "ce4a4a34"
    schema_shas = ORDERED_SCHEMA_SHAS if ordered else SCHEMA_SHAS
    property_order = ["question", "trace", "answer"] if ordered else ["answer", "question", "trace"]
    launcher_sha = "8595c54dd0b675e83acc20d92c07bb562a76968037492824262f9a1796a6acbc" if ordered else LAUNCHER_SHA
    slot_grant = "A100-post-training-schema-order-explicit-slot" if ordered else "A100-post-training-schema-explicit-slot"
    config_directory = "oct14-mbs-order-" if ordered else "oct14-mbs-schema-"
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
    packages = dependency_audit["packages"]
    require(set(packages) == set(PINNED) and all(packages[k].get("version") == v for k, v in PINNED.items())
            and dependency_audit.get("dependency_fingerprint") == sha(json.dumps(packages, sort_keys=True).encode())
            and launch.get("schema_dependency_binding") == dependency_audit
            and dependency_audit.get("not_gpu_receipt") is True and dependency_audit.get("cuda_initialized") is False
            and dependency_audit.get("dependency_modules_imported_by_audit") is False
            and dependency_audit.get("model_instantiated_by_audit") is False,
            "actual fixed dependency CPU audit/launch binding required")
    overlay_files = {}
    for package in packages.values():
        files = package.get("package_file_sha256", {})
        require(files and all(hash_string(h) for h in files.values()), "all audited dependency bytes required")
        overlay_files.update(files)
    require(grammar_audit.get("algorithm_commit") == commit and grammar_audit.get("source_file_sha256") == hashes
            and grammar_audit.get("cuda_initialized") is False and grammar_audit.get("model_loaded") is False
            and grammar_audit.get("tokenizer_sha256") == TOKENIZER_SHA and grammar_audit.get("vocab_size") == 152064
            and grammar_audit.get("versions") == PINNED and len(grammar_audit.get("overlay_file_sha256", {})) == 203
            and all(overlay_files.get(p) == h for p, h in grammar_audit["overlay_file_sha256"].items())
            and grammar_audit.get("operations") == {op: {"actual_compilation_completed": True, "schema_sha256": h}
                                                    for op, h in schema_shas.items()}
            and launch.get("schema_grammar_binding") == grammar_audit
            and launch.get("schema_grammar_cpu_audit_sha256") == raw_hashes.get("grammar_audit"),
            "actual frozen-source five-schema grammar compilation binding required")
    require(launch.get("construction_schema_only") is True
            and launch.get("independent_verifier_and_student_unconstrained") is True
            and launch.get("actual_accelerator_name") == "NVIDIA A100-SXM4-80GB"
            and launch.get("base_launcher_source_sha256") == "186a47f0e8a53b17595a52625dafdd0c8d24406c7ffe4631aa182338abd4cf30",
            "construction-only schema, original launcher and actual accelerator required")
    pythonpath = launch.get("runner_pythonpath", "").split(":")
    require(len(pythonpath) == 2 and pythonpath[0].endswith("/auto-research-oct14-" + short + "/src")
            and pythonpath[1] == dependency_audit.get("overlay_root"), "actual frozen source/explicit overlay import order required")
    c = launch["effective_config"]
    require(set(c) == set(CONFIG) | PATH_FIELDS and all(c[k] == v and type(c[k]) is type(v) for k, v in CONFIG.items()),
            "unchanged 16/group4/cap1024/depth1/two-retry/two-step budget required")
    require(all(isinstance(c[k], str) and c[k] for k in PATH_FIELDS), "explicit resource path bindings required")
    require(launch.get("seed") == 42 and launch.get("diagnostic_only") is True
            and launch.get("formal_comparison") is False and launch.get("gpu_grant_received") is True
            and launch.get("gpu_slot_grant") == slot_grant
            and launch.get("launcher_source_sha256") == launcher_sha,
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
            and command[5] == "--config" and command[6].endswith("/" + config_directory + short + "-queue/oct14_execution-mbs-schema-v1.json")
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
            require(response.get("json_schema_constrained") is True and response.get("json_schema_backend") == "xgrammar-hf"
                    and response.get("xgrammar_version") == PINNED["xgrammar"]
                    and response.get("json_schema_sha256") == schema_shas["propose_children"],
                    "actual executed schema metadata must not be rebound")
            try:
                value = None if response["truncated"] else json.loads(response["response_text"])
            except json.JSONDecodeError:
                value = None
            expected_reason = "truncated_json_response" if response["truncated"] else ("no_json_value" if value is None else None)
            count = min(3, sum(schema_valid_problem(v) for v in value)) if isinstance(value, list) else 0
            require(response.get("parsed_json_kind") == type(value).__name__
                    and response.get("proposed_problem_count") == (len(value) if isinstance(value, list) else 0)
                    and response.get("schema_valid_problem_count") == count
                    and response.get("reject_reason") == expected_reason
                    and response.get("schema_reject_reason") == (None if count else "no_schema_valid_child"),
                    "actual strict schema parsing cannot be repaired or relabeled")
            try:
                json.loads(response["response_text"])
                outer_valid = True
            except json.JSONDecodeError:
                outer_valid = False
            require(isinstance(value, list) and len(value) == 2
                    and all(isinstance(child, dict) and list(child) == property_order for child in value),
                    "actual two-child compiler property order required")
            proposals.append({"outer_json_valid": outer_valid, "strict_parsed_value_kind": type(value).__name__,
                              "schema_valid_children": count})
        safe = {k: response[k] for k in ("role", "input_gold_scope", "response_text_sha256", "generated_tokens", "truncated")}
        for k in ("question_sha256", "attempt", "reward", "accepted", "reject_reason", "operation", "json_schema_constrained",
                  "json_schema_backend", "json_schema_sha256", "xgrammar_version"):
            if k in response:
                safe[k] = response[k]
        safe_traces.append(safe)
    expected_verify = 12 if ordered else 13
    require(roles == {"target_calibration": 64, "effectivity_student": 4, "effectivity_teacher": 4,
                      "construction_verification": expected_verify, "construction_teacher": 2}, "complete actual response role counts required")
    for row in calibrations:
        actual = [t for t in traces if t["role"] == "target_calibration" and t["question_sha256"] == row["root_question_sha256"]]
        require([x["reward"] for x in actual] == row["rewards"] and [x["truncated"] for x in actual] == row["truncated"],
                "calibration must match its actual four responses")
    verified_count = sum(x["accepted"] for x in traces if x["role"] == "construction_verification")
    require(verified_count == (2 if ordered else 1), "actual accepted verification count mismatch")
    for root in (4, 7, 8):
        actual = [x for x in traces if x["role"] == "construction_verification"
                  and x["question_sha256"] == calibrations[root]["root_question_sha256"]]
        require(([x["accepted"] for x in actual] == [True] and [x["attempt"] for x in actual] == [1]) if root == 4 else
                ([x["accepted"] for x in actual] == [False, False] and [x["attempt"] for x in actual] == [1, 2]),
                "root decision must match its actual independent verification responses")
    child_questions = []
    for response in traces:
        if response["role"] == "construction_teacher":
            child_questions.extend(sha(child["question"].encode()) for child in json.loads(response["response_text"]))
    root_hashes = {calibrations[root]["root_question_sha256"] for root in (4, 7, 8)}
    child_verifications = [r for r in traces if r["role"] == "construction_verification" and r["question_sha256"] not in root_hashes]
    if ordered:
        require(len(child_questions) == len(set(child_questions)) == 4
                and set(r["question_sha256"] for r in child_verifications) == set(child_questions),
                "all four actual ordered child questions must bind independent verification")
        for index, question in enumerate(child_questions):
            actual = [r for r in child_verifications if r["question_sha256"] == question]
            require([r["attempt"] for r in actual] == ([1] if index == 3 else [1, 2])
                    and [r["accepted"] for r in actual] == ([True] if index == 3 else [False, False]),
                    "actual first three failed twice/fourth accepted once must remain visible")
    else:
        child_counts = Counter(child_questions)
        require(Counter(r["question_sha256"] for r in child_verifications) == Counter({k: 2 * n for k, n in child_counts.items()})
                and all(not r["accepted"] for r in child_verifications), "all four child questions must bind their two real failed verifications")
        for question, count in child_counts.items():
            require(Counter(r["attempt"] for r in child_verifications if r["question_sha256"] == question) == {1: count, 2: count},
                    "unchanged two independent attempts for each proposed child required")
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
                and audits[i].get("proposed_children") == 2
                and audits[i].get("verified_children") == (1 if ordered and i == 2 else 0), "actual two decomposition rejections required")
    for i, root in ((4, 7), (6, 8)):
        require(set(audits[i]) == {"phase", "accepted", "depth", "reject_reason", "question_sha256"}
                and audits[i].get("accepted") is False and audits[i].get("depth") == 0
                and audits[i].get("reject_reason") == "independent_verification_failed"
                and audits[i].get("question_sha256") == calibrations[root]["root_question_sha256"], "actual root verification rejection mismatch")
    require(all(x["schema_valid_children"] == 2 and x["outer_json_valid"] is True for x in proposals), "actual valid JSON proposals required")
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
    require(set(raw_hashes) == {"launch", "exit", "runtime", "failure", "source_contract", "resource_audit", "config", "grammar_audit", "dependency_audit"}
            and all(hash_string(h) for h in raw_hashes.values()),
            "all immutable raw byte hashes required")
    metrics = {"verified_hard_roots": 3, "construction_attempts": 3, "paired_rl_roots": 0,
               "method_rl_updates": 0, "control_rl_updates": 0, "decomposition_proposal_calls": 2,
               "schema_valid_proposed_children": sum(x["schema_valid_children"] for x in proposals),
               "invalid_outer_json_proposals": sum(not x["outer_json_valid"] for x in proposals),
               "independent_verification_calls": expected_verify, "accepted_independent_verifications": verified_count,
               "rejected_independent_verifications": expected_verify - verified_count,
               "generated_response_tokens": sum(cost["generated_tokens"].values()),
               "invocation_elapsed_seconds": exit_record["elapsed_seconds"]}
    path = "docs/reproductions/2610.12659-magicbeanstalk/metrics/" + (
        "public-a100-schema-order-failed-seed42-ce4a4a34.json" if ordered else "public-a100-schema-failed-seed42-f92413aa.json")
    sanitized_command = ["python", "-u", "scripts/run_oct13_post_training.py", "--method", "magicbeanstalk",
                         "--config", "<config>/oct14_execution-mbs-schema-v1.json", "--seed", "42", "--output", "<run>/evidence"]
    # Explicit whitelist: neither raw response text/token IDs nor machine/config
    # paths, build strings, or arbitrary extra audit fields enter the draft.
    return {"schema_version": 2, "adapter_key": "magicbeanstalk", "manifest_ref": "reproduction:magicbeanstalk",
            "method": "magicbeanstalk", "measured_locally": True, "diagnostic_only": True, "promotion_eligible": False,
            "not_gpu_receipt": True, "whole_method_gpu_validation_passed": False, "seeds": [42],
            "curation_state": "sanitized-negative-record",
            "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"},
            "seed_results": [{"seed": 42, "device": "cuda", "diagnostic_only": True, "return_code": 1,
                              "execution_status": "failed-construction", "metrics": metrics}],
            "aggregate_metrics": {k: {"mean": v, "std": 0., "n": 1} for k, v in metrics.items()},
            "dataset": DATASET, "checkpoint": checkpoint, "executed_source_sha256": hashes,
            "execution_checks": {"return_code": 1, "configured_wall_cap_seconds": 1800,
                "invocation_elapsed_seconds": exit_record["elapsed_seconds"], "configured_budget": CONFIG,
                "hard_root_selection": selection, "construction_audits": audits,
                "sanitized_response_audits": safe_traces, "proposal_parsing": proposals, "measured_cost": cost,
                "compiled_property_order": property_order,
                "schema_sha256": schema_shas, "dependency_versions": PINNED,
                "dependency_fingerprint": dependency_audit["dependency_fingerprint"],
                "method_rl_updates": 0, "control_rl_updates": 0, "gold_access_roles": GOLD_SCOPES,
                "hard_root_count_scope": "zero-success nontruncated target-policy calibration, not proof that all three independent teacher verifications passed",
                "effectivity_conditioned_test_reached": False, "synthesis_reached": False,
                "target_policy_goldilocks_reached": False, "baseline_validation_generation_calls": 4},
            "failure_interpretation": ("Both ordered constrained responses were valid two-child JSON; the first proposal had zero verified children and the second had one. Roots7/8 also failed verification. The corrected question, trace, answer order did not complete construction in this one seed; no capability or general causal conclusion follows. No extra retry or response repair occurred."
                if ordered else "Both constrained responses were valid two-child JSON, but all four children failed independent verification; roots7/8 also failed. The executed sorted schema forced answer before question and trace. This integration defect does not establish the cause of all content or verification errors. No extra retry or response repair occurred."),
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
                "The strict JSON parser and numeric verifier were not repaired or relaxed; all negative outcomes remain visible.",
                "This single negative attempt cannot identify the general cause of missing facts, trace/answer inconsistencies, or independent solver errors."
                if ordered else "Field ordering is a verified structure constraint, not proof that it explains every missing fact, trace/answer inconsistency, or independent solver error.",
                "Baseline validation generation cost is included, but no post-training assessment or training/control update occurred."]}


def curate(directory, contract_path, audit_path, config_path, dependency_path, grammar_path, *, repo):
    """Read immutable evidence and verify all Git blobs; never open heldout data."""
    read = lambda p: json.loads(Path(p).read_text())
    contract = read(contract_path)
    commit = contract["source_commit"]
    git_hashes = {p: sha(subprocess.check_output(["git", "show", commit + ":" + p], cwd=repo)) for p in contract["source_file_sha256"]}
    directory = Path(directory)
    files = {"launch": directory / "launch.json", "exit": directory / "exit.json",
             "runtime": directory / "runtime.log", "failure": directory / "evidence/failure.json",
             "source_contract": Path(contract_path), "resource_audit": Path(audit_path), "config": Path(config_path),
             "dependency_audit": Path(dependency_path), "grammar_audit": Path(grammar_path)}
    raw_hashes = {k: sha(p.read_bytes()) for k, p in files.items()}
    return curate_bundle(launch=read(files["launch"]), exit_record=read(files["exit"]), failure=read(files["failure"]),
                         contract=contract, audit=read(audit_path), git_hashes=git_hashes, raw_hashes=raw_hashes,
                         dependency_audit=read(dependency_path), grammar_audit=read(grammar_path),
                         config_sha256=sha(json.dumps(read(config_path), sort_keys=True).encode()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("directory", "contract", "audit", "config", "dependency", "grammar", "repo"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.directory, args.contract, args.audit, args.config, args.dependency, args.grammar, repo=args.repo),
                     ensure_ascii=False, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
