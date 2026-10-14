#!/usr/bin/env python3
"""Strict CPU curation of one historical validation-only no-submit probe.

Emit a sanitized summary, never prompts, answers, token IDs or a GPU receipt.
Raw files stay private and immutable; no network, model generation or CUDA.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import types

ROOT = Path(__file__).resolve().parents[1]
ALGORITHM_COMMIT = "47f0e9cebc196e15c991d494dc4072367f53043b"
PROBE_COMMIT = "d5bf41b221b1f2aa8c09082792d8cb590235623b"
PROBE_SHA = "373df1c73b668c3f261c57241e946dbf4d9d06fa4cd331b70b670881b1dc0f12"
ALGORITHM_ARCHIVE_SHA = "063e7583614b5a1e75f7420c93871c920f18cc42f53cc22eddc2c4256cff8afb"
PROBE_ARCHIVE_SHA = "5f9fd1858f5fadede442e487d40e886077a4073f4ad690431e0a9f5286e973e8"
RAW_SHA = {
    "seed42.json": "a7042043c7c1c0eb9bcfef60334c8fdec123e9e7d51de095e5adaa90e484e0af",
    "seed42.partial.json": "ef3735ac2baebeeb76ffcf5a2b4ca99a73dddb3f6d05be0b41e5fed90b620486",
    "seed42.trace.jsonl": "1777f98145777026888817d0cf6e7a138178a2be94c9a7de21c98b9e612763ee",
    "exit.json": "2ef1f9f89007f2a7d19b85513246283761426b813e1a0f171ba9902de99ffd2d",
    "launcher.log": "c19e893523b69f5cafe8b76d8c9959e1b4c281d567645f579535a8c4bf0e4d45",
}
RESOURCE_SHA = {
    "probe-d5bf41b2.json": "e4bbc336251ada6bc815bf5013b351538b8e9ea45b30cd2a9c0f9fca855a06ed",
    "cpu-audit-d5bf41b2.json": "c2c85d45e0874a006897368be541605cdfa82c6a55fdce3bbe93bd10044f6394",
    "questions.jsonl": "6a3213a1941882e4d0787b903df170452f13ea13f52ad9dbc4e6cb6e418eca5e",
}
ARTIFACT = "docs/reproductions/2609.01642-skilldreamer/metrics/public-a100-validation-no-submit-seed42-47f0e9ce.json"


def sha(content):
    return hashlib.sha256(content).hexdigest()


def required(condition, message):
    if not condition:
        raise ValueError(message)


def pinned_files(directory, expected):
    records = {}
    for name, digest in expected.items():
        content = (directory / name).read_bytes()
        required(sha(content) == digest, "historical artifact bytes differ: " + name)
        records[name] = {"sha256": digest, "bytes": len(content), "public_copy": False}
    return records


def committed(name, commit):
    return subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT)


def load_namespace(name, content):
    loaded = types.ModuleType(name)
    loaded.__package__ = name.rsplit(".", 1)[0]
    sys.modules[name] = loaded
    exec(compile(content, name, "exec"), loaded.__dict__)
    return loaded


def validate_trace(events, *, expected_calls):
    required(len(events) == expected_calls * 2, "all attempts and responses must remain")
    attempts, responses = {}, {}
    for index in range(expected_calls):
        attempt, response = events[2 * index:2 * index + 2]
        call = index + 1
        required(attempt.get("event") == "generation_attempt" and response.get("event") == "generation_response"
            and type(attempt.get("call")) is int and type(response.get("call")) is int
            and attempt["call"] == response["call"] == call and attempt.get("id") == response.get("id")
            and isinstance(attempt.get("prompt"), str) and bool(attempt["prompt"].strip())
            and isinstance(response.get("response"), str), "unique ordered call/episode/response pair required")
        attempts[call], responses[call] = attempt, response["response"]
    return attempts, responses


def sanitize_guard(payload):
    forbidden_keys = {"prompt", "question", "answer", "submitted_answer", "token_ids", "input_ids",
        "response", "observations", "argv", "command", "hostname", "username", "driver_version",
        "accuracy", "pass_rate"}
    def visit(value):
        if isinstance(value, dict):
            required(not set(value).intersection(forbidden_keys), "private content or unmeasured accuracy must not be public")
            for key, item in value.items():
                required(not (key == "result" and item == "passed"), "negative probe is not passed evidence")
                visit(item)
        elif isinstance(value, list):
            for item in value: visit(item)
        elif isinstance(value, str):
            lowered = value.lower()
            required(not any(word in lowered for word in ("/tmp/", "/users/", "/home/", "forge-codex", "bytedance",
                "host.example", "cuda build", "driver version", "ssh ")), "private machine/build/path text must not be public")
        elif type(value) is float:
            required(math.isfinite(value), "public numeric values must be finite")
    visit(payload)


def replay(run, attempts, responses, source):
    namespace = "skill_negative47_cpu"
    previous = {name: module for name, module in sys.modules.items() if name == namespace or name.startswith(namespace + ".")}
    for name in (namespace, namespace + ".skilldreamer", namespace + ".state_opd"):
        package = types.ModuleType(name)
        package.__path__ = []
        sys.modules[name] = package
    try:
        environment = load_namespace(namespace + ".state_opd.environment", source["state_opd/environment.py"])
        algorithm = load_namespace(namespace + ".skilldreamer.algorithm", source["skilldreamer/algorithm.py"])
        gallery = {row["id"]: algorithm.Skill(**row) for row in json.loads(source["skilldreamer/gallery.json"])}
        steps, identifiers = [], []
        original_step = environment.ArithmeticEnvironment.step
        def counted_step(self, action):
            result = original_step(self, action)
            steps.append((action.get("tool"), result[0]))
            return result
        environment.ArithmeticEnvironment.step = counted_step
        for episode in run["episodes"]:
            if not episode.get("hsr_executed"):
                required(episode["id"] == "13" and episode["executed_actions"] == 0 and "failure" in episode, "PSG failure must remain")
                continue
            items = [item for item in attempts.values() if item["id"] == episode["id"] and "Loaded verified gallery skill procedures:" in item["prompt"]]
            required(bool(items), "actual runtime trace required")
            question = items[0]["prompt"].split("Task: ", 1)[1].split("\nObserved execution history: ", 1)[0]
            pending = iter(items)
            def generate(prompt):
                actual = next(pending)
                required(actual["prompt"] == prompt, "replayed runtime prompt differs from actual trace")
                return responses[actual["call"]]
            outcome = algorithm.execute_agent(question, generate, [gallery[name] for name in episode["retrieved_skills"]], action_budget=8)
            required(all(episode[key] == value for key, value in outcome.items()) and next(pending, None) is None,
                     "all original runtime calls and outcome fields must replay exactly")
            identifiers.append(episode["id"])
        required(len(steps) == 50 and all(tool == "calculator" for tool, _ in steps), "actual environment tool trace differs")
        successes = sum(observation.startswith("Calculator result:") for _, observation in steps)
        errors = sum(observation.startswith("Calculator error:") for _, observation in steps)
        required(successes == 46 and errors == 4, "successful calculations must not be confused with environment calls")
        return identifiers, successes, errors
    finally:
        for name in list(sys.modules):
            if name == namespace or name.startswith(namespace + "."): del sys.modules[name]
        sys.modules.update(previous)


def curate(directory, resources, algorithm_archive, probe_archive):
    originals = pinned_files(directory, RAW_SHA)
    resource_records = pinned_files(resources, RESOURCE_SHA)
    required(sha(algorithm_archive.read_bytes()) == ALGORITHM_ARCHIVE_SHA and sha(probe_archive.read_bytes()) == PROBE_ARCHIVE_SHA,
             "exact historical source archives required")
    runner_name = "scripts/probe_oct14_skilldreamer_validation.py"
    runner = committed(runner_name, PROBE_COMMIT)
    required(sha(runner) == PROBE_SHA, "actual frozen probe implementation differs")
    with tarfile.open(probe_archive) as archive:
        required(archive.extractfile(runner_name).read() == runner, "probe archive and executed git commit differ")
    # Reuse the historical strict probe's budget and question-only validators,
    # not a reduced reimplementation or current mutable runtime.
    probe = load_namespace("skill_negative47_frozen_probe", runner)
    config = json.loads((resources / "probe-d5bf41b2.json").read_text())
    probe.fixed_budget(config)
    rows, dataset = probe.questions_only(resources / "questions.jsonl")
    required(config["probe_source_commit"] == PROBE_COMMIT and config["probe_source_sha256"] == PROBE_SHA
        and config["algorithm_source_root"] == "/tmp/auto-research-oct14-47f0e9ce"
        and config["probe_source_root"] == "/tmp/auto-research-oct14-d5bf41b2"
        and config["source_sha256"] == probe.SOURCE_SHA256, "exact separate source-root and SHA bindings required")
    source = {}
    source_hashes = {}
    with tarfile.open(algorithm_archive) as archive:
        for short, expected in probe.SOURCE_SHA256.items():
            name = "src/auto_research/reproductions/" + short
            content = committed(name, ALGORITHM_COMMIT)
            required(sha(content) == expected and archive.extractfile(name).read() == content, "actual algorithm source/archive binding differs")
            source[short], source_hashes[name] = content, expected
        name = "scripts/run_skilldreamer.py"
        content = committed(name, ALGORITHM_COMMIT)
        required(sha(content) == "9b14997fef987797db879554966dccb6c5699496c4ca8a979cf027b17fbd421e"
                 and archive.extractfile(name).read() == content, "original full runner source differs")
        source_hashes[name] = sha(content)
    run = json.loads((directory / "seed42.json").read_text())
    partial = json.loads((directory / "seed42.partial.json").read_text())
    prior_audit = json.loads((resources / "cpu-audit-d5bf41b2.json").read_text())
    protocol = run["protocol"]
    required(run.get("status") == "completed_validation_probe" and run.get("scope") == "fixed_validation_format_probe"
        and run.get("diagnostic_only") is True and run.get("promotion_eligible") is False and run.get("capability_receipt") is False,
        "only original completed validation diagnostic is in scope")
    required([row["id"] for row in run["episodes"]] == list(probe.VALIDATION_IDS) == [row["id"] for row in rows]
        and all(episode.get("submitted_answer") is None for episode in run["episodes"]), "all eight original validation failures must remain")
    required(protocol["input"] == dataset == prior_audit["input"] and protocol["source_sha256"] == probe.SOURCE_SHA256
        and protocol["algorithm_commit"] == ALGORITHM_COMMIT
        and protocol["probe_source"] == {"commit": PROBE_COMMIT, "sha256": PROBE_SHA, "immutable_root_bound": True}
        and all(protocol[key] is False for key in ("gold_present", "scorer_present", "evaluation_ids_used", "capability_receipt")),
        "original question-only/source/role boundaries differ")
    for section, count in (("checkpoint", 11), ("encoder", 6)):
        required(protocol[section] == prior_audit[section] and len(protocol[section]["files"]) == count,
                 "actual prior complete resource-byte audit differs")
    required(protocol["budget"] == {name: config[name] for name in protocol["budget"]}
        and all(partial[key] == run[key] for key in partial if key not in ("status", "wall_seconds")),
        "actual budget or original partial episodes differ")
    exit_record = json.loads((directory / "exit.json").read_text())
    required(exit_record["exit_code"] == 0 and exit_record["algorithm_source_commit"] == ALGORITHM_COMMIT
        and exit_record["probe_source_commit"] == PROBE_COMMIT and exit_record["execution_config_sha256"] == RESOURCE_SHA["probe-d5bf41b2.json"]
        and exit_record["argv"] == ["timeout", "--kill-after=10s", "600s", "/tmp/jev-closeout-venv/bin/python",
            "/tmp/auto-research-oct14-d5bf41b2/scripts/probe_oct14_skilldreamer_validation.py", "--config",
            "/tmp/oct14-skill-deploy-d5bf41b2/probe-d5bf41b2.json", "--output",
            "/tmp/auto-research-oct14-d5bf41b2/runs/skill-validation-47f0e9ce-seed42/seed42.json"], "actual launch/source/config/exit binding differs")
    logged = [json.loads(line) for line in (directory / "launcher.log").read_text().splitlines() if line.startswith("{")]
    required(logged[-1] == exit_record and logged[-2] == {"status": run["status"], "checks": run["execution_checks"]}, "actual launcher completion/exit log differs")
    required(all(type(value) in (int, float) and math.isfinite(value) and 0 < value < 600
        for value in (run["wall_seconds"], exit_record["elapsed_seconds"])), "both actual elapsed bounds must be finite and under 600")
    required(run["model_calls"] == sum(row["model_calls_including_psg"] for row in run["episodes"]) == 163
        and run["generated_tokens"] == sum(row["generated_tokens_including_psg"] for row in run["episodes"]) == 19466,
        "actual episode call/token totals differ")
    events = [json.loads(line) for line in (directory / "seed42.trace.jsonl").read_text().splitlines()]
    attempts, responses = validate_trace(events, expected_calls=163)
    identifiers, successes, errors = replay(run, attempts, responses, source)
    checks = {"psg_episodes": sum(bool(row.get("psg_completed")) for row in run["episodes"]),
        "hsr_episodes": sum(bool(row.get("hsr_executed")) for row in run["episodes"]),
        "actual_csi_assessments": sum(len(row.get("capability_checks", [])) for row in run["episodes"]),
        "loaded_skill_episodes": sum(bool(row.get("loaded_skills")) for row in run["episodes"]),
        "executed_actions": sum(row["executed_actions"] for row in run["episodes"])}
    required(checks == run["execution_checks"] == {"psg_episodes": 7, "hsr_episodes": 7, "actual_csi_assessments": 58,
        "loaded_skill_episodes": 7, "executed_actions": 50}, "actual core counters differ")
    payload = {"schema_version": 2, "adapter_key": "skilldreamer", "manifest_ref": "reproduction:skilldreamer",
        "seeds": [42], "result": "native_core_executed_no_submission_validation_diagnostic",
        "measured_locally": True, "diagnostic_only": True, "promotion_eligible": False,
        "not_gpu_receipt": True, "gpu_validation_passed": False, "capability_receipt": False,
        "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"},
        "metrics": {"runner_wall_seconds": run["wall_seconds"], "invocation_elapsed_seconds": exit_record["elapsed_seconds"],
            "exit_code": 0, "model_calls": 163, "generated_tokens": 19466, "validation_episodes": 8,
            **{key: value for key, value in checks.items() if key != "executed_actions"},
            "env_step_calls": 50, "calculator_attempts": 50, "calculator_successes": successes,
            "calculator_errors": errors, "unknown_tool_calls": 0, "finish_calls": 0, "submitted_answers": 0},
        "execution_checks": checks, "dataset": dataset, "checkpoint": protocol["checkpoint"], "encoder": protocol["encoder"],
        "budget": protocol["budget"], "private_original_artifact_hashes": originals,
        "resource_audit_artifact_hashes": resource_records,
        "cpu_replay": {"exact_runtime_episode_ids": identifiers, "retained_psg_failure_episode_ids": ["13"],
            "runtime_prompts_and_all_outcome_fields_exact": True, "new_generation": False, "cuda_executed": False},
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": [42], "validation_only": True,
            "validation_ids": list(probe.VALIDATION_IDS), "formal_comparison": False, "gold_present": False,
            "scorer_present": False, "evaluation_ids_used": False, "official_test_opened": False,
            "test_used_for_selection": False, "claim_policy": "single-seed question-only validation negative: no correctness measurement, full evaluation, capability claim or promotion"},
        "provenance": {"code_commit": ALGORITHM_COMMIT, "probe_source": protocol["probe_source"],
            "artifact_path": ARTIFACT, "executed_source_sha256": source_hashes,
            "algorithm_archive_sha256": ALGORITHM_ARCHIVE_SHA, "probe_archive_sha256": PROBE_ARCHIVE_SHA,
            "execution_config_sha256": RESOURCE_SHA["probe-d5bf41b2.json"],
            "dataset_fingerprint": sha(json.dumps(dataset, sort_keys=True).encode())},
        "limitations": ["50 environment calls include 46 successful calculations and 4 calculator errors; no finish or submission.",
            "No external scorer or accuracy measurement; core mechanism invocation is not task success.",
            "Only the fixed eight validation inputs, not the 16-ID evaluation or a complete three-arm/three-seed run.",
            "Public record excludes original content and machine details; immutable local raw/config/log hashes remain bound.",
            "No causal effect of API wording is isolated; earlier failures stay bound to their historical sources."]}
    sanitize_guard(payload)
    return payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--resources", type=Path, required=True)
    parser.add_argument("--algorithm-archive", type=Path, required=True)
    parser.add_argument("--probe-archive", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(curate(args.input, args.resources, args.algorithm_archive, args.probe_archive), ensure_ascii=False, indent=2, allow_nan=False))
