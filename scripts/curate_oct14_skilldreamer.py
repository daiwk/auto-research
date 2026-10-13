#!/usr/bin/env python3
"""Curate measured train-derived arithmetic diagnostics, including failures."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import tarfile

from auto_research.gpu_validation import validate_gpu_receipt

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
ARMS = ("no_skills", "direct", "skilldreamer")
DOC = "docs/reproductions/2609.01642-skilldreamer/metrics"
MODEL_FILES = {"config.json", "generation_config.json", "merges.txt", "model.safetensors.index.json",
               "tokenizer.json", "tokenizer_config.json", "vocab.json", *[
                   f"model-{index:05d}-of-00004.safetensors" for index in range(1, 5)]}
ENCODER_FILES = {"model.safetensors", "config.json", "tokenizer.json", "tokenizer_config.json", "special_tokens_map.json", "vocab.txt"}
INSTRUMENTATION = {"original_call_forwarded_unchanged": True,
                   "temporary_call_instrumentation": True, "restored_after_run": True}


def a100_observers(directory, runs, commit, hashes, observer_commit, observer_archive, config_path):
    if (commit != "47f0e9cebc196e15c991d494dc4072367f53043b"
            or not re.fullmatch(r"[0-9a-f]{40}", observer_commit or "")
            or observer_archive is None or config_path is None):
        raise ValueError("A100 requires fixed 47f algorithm and independently frozen observer/config")
    observer_name = "scripts/observe_oct14_skilldreamer.py"
    committed = subprocess.check_output(["git", "show", f"{observer_commit}:{observer_name}"], cwd=ROOT)
    with tarfile.open(observer_archive) as archive:
        if archive.extractfile(observer_name).read() != committed:
            raise ValueError("observer deployed archive differs from its executed commit")
    observer_sha = hashlib.sha256(committed).hexdigest()
    config = json.loads(config_path.read_text())
    execution_sha = hashlib.sha256(config_path.read_bytes()).hexdigest()
    run_config = config.get("run_config", {})
    caps = {"max_queries": 24, "max_new_tokens": 256, "top_k": 3, "action_budget": 8}
    if (config.get("algorithm_commit") != commit or config.get("source_sha256") != hashes
            or config.get("observer_source_commit") != observer_commit or config.get("observer_source_sha256") != observer_sha
            or run_config.get("device") != "cuda"
            or any(type(run_config.get(key)) is not int or run_config[key] != value for key, value in caps.items())
            or type(config.get("wall_limit_seconds")) is not int or not 0 < config["wall_limit_seconds"] <= 14400):
        raise ValueError("actual fixed source/config and original A100 budget required")
    config_sha = hashlib.sha256(json.dumps(run_config, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    ids = sorted(map(str, range(24)), key=lambda value: hashlib.sha256(("skilldreamer-v1:" + value).encode()).hexdigest())
    records = []
    for seed, raw in zip(SEEDS, runs, strict=True):
        path = directory / f"observer-seed{seed}.json"
        record = json.loads(path.read_text())
        audit = record.get("audit", {})
        if (record.get("status") != "completed_original_three_arm_diagnostic" or record.get("seed") != seed
                or record.get("exit_code") != 0 or record.get("diagnostic_only") is not True
                or record.get("promotion_eligible") is not False
                or record.get("instrumentation") != INSTRUMENTATION
                or record.get("accelerator") != {"vendor": "NVIDIA", "model": "NVIDIA A100-SXM4-80GB"}
                or audit.get("algorithm_commit") != commit or audit.get("executed_source_sha256") != hashes
                or audit.get("observer_source") != {"commit": observer_commit, "sha256": observer_sha, "immutable_root_bound": True}
                or audit.get("run_config") != run_config or audit.get("run_config_sha256") != config_sha
                or record.get("execution_config_sha256") != execution_sha
                or audit.get("limits") != {"model_calls": 1248, "output_tokens": 319488, "wall_seconds": config["wall_limit_seconds"]}):
            raise ValueError("A100 observer accelerator/source/config binding differs")
        for key in ("peak_gpu_memory_allocated_bytes", "peak_gpu_memory_reserved_bytes"):
            if type(record.get(key)) is not int or record[key] <= 0:
                raise ValueError("actual positive finite integer allocator peaks required")
        if (record["peak_gpu_memory_reserved_bytes"] < record["peak_gpu_memory_allocated_bytes"]
                or type(record.get("wall_seconds")) not in (int, float)
                or not math.isfinite(record["wall_seconds"]) or not 0 < record["wall_seconds"] <= config["wall_limit_seconds"]):
            raise ValueError("actual allocator/wall bounds invalid")
        command = record.get("command")
        try:
            if (not isinstance(command, list) or command[command.index("--seed") + 1] != str(seed)
                    or not any(isinstance(value, str) and value.endswith(observer_name) for value in command)
                    or "--config" not in command or "--output" not in command):
                raise ValueError("actual observer invocation required")
        except (IndexError, TypeError) as exc:
            raise ValueError("actual observer invocation required") from exc
        protocol = raw["protocol"]
        if (raw.get("evaluation_tier") != "l2_public_dataset"
                or protocol.get("validation_ids") != ids[:8] or protocol.get("test_ids") != ids[8:]
                or any([episode.get("id") for episode in raw["episodes"][arm]] != ids[8:] for arm in ARMS)
                or protocol.get("raw_sha256") != "8f33a9f7a44067e362458e4daf0eb1ad629a2aac2f44ffefe731e36b19dcb8c1"
                or audit.get("dataset") != protocol["dataset"]
                or protocol["dataset"].get("public_id") != "openai/grade-school-math"
                or protocol["dataset"].get("revision") != "3101c7d5072418e28b9008a6636bde82a006892c"):
            raise ValueError("original complete 24-row split/dataset binding required")
        for section, expected_id, revision in (("checkpoint", "Qwen/Qwen2.5-7B-Instruct", "bb46c15ee4bb56c5b63245ef50fd7637234d6f75"),
                ("encoder", "sentence-transformers/all-MiniLM-L6-v2", "1110a243fdf4706b3f48f1d95db1a4f5529b4d41")):
            measured, audited = protocol[section], audit.get(section, {})
            full_files = MODEL_FILES if section == "checkpoint" else ENCODER_FILES
            selected_files = {name for name in MODEL_FILES if name.endswith((".safetensors", ".json"))} if section == "checkpoint" else {"model.safetensors", "config.json", "tokenizer.json"}
            if (measured.get("public_id") != expected_id or measured.get("revision") != revision
                    or audited.get("public_id") != expected_id or audited.get("revision") != revision
                    or set(measured.get("files", {})) != selected_files or set(audited.get("files", {})) != full_files
                    or any(not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest) for digest in audited.get("files", {}).values())
                    or any(audited["files"].get(name) != digest for name, digest in measured.get("files", {}).items())):
                raise ValueError("actual fixed model/encoder resource binding differs")
        trace_path = directory / f"trace-seed{seed}.jsonl"
        trace_content = trace_path.read_bytes()
        events = [json.loads(line) for line in trace_content.splitlines()]
        attempts = [row for row in events if row.get("event") == "generation_attempt"]
        responses = [row for row in events if row.get("event") == "generation_response"]
        # Every attempt has exactly one matching response/error immediately
        # afterwards; preserve errors instead of quietly dropping them.
        terminals = [row for row in events if row.get("event") in ("generation_response", "generation_error")]
        if (len(events) != 2 * len(attempts) or len(terminals) != len(attempts)
                or any(events[index].get("event") != "generation_attempt"
                       or events[index + 1].get("event") not in ("generation_response", "generation_error")
                       or type(events[index].get("call")) is not int
                       or type(events[index + 1].get("call")) is not int
                       or events[index].get("call") != events[index + 1].get("call")
                       for index in range(0, len(events), 2))):
            raise ValueError("each actual generation attempt must have one ordered response/error with the same call ID")
        calls = sum(row["model_calls"] for row in raw["variants"].values())
        tokens = sum(row["generated_tokens"] for row in raw["variants"].values())
        if (record.get("raw_sha256") != hashlib.sha256((directory / f"seed{seed}.json").read_bytes()).hexdigest()
                or record.get("trace_sha256") != hashlib.sha256(trace_content).hexdigest()
                or record.get("calls_attempted") != len(attempts) or record.get("generation_responses") != len(responses)
                or len(responses) != calls or record.get("generated_tokens") != tokens
                or sum(row["generated_tokens"] for row in responses) != tokens
                or len(attempts) > 1248 or tokens > 319488
                or [row["call"] for row in attempts] != list(range(1, len(attempts) + 1))
                or any(type(row.get("generated_tokens")) is not int or not 0 <= row["generated_tokens"] <= 256 for row in responses)):
            raise ValueError("actual raw/trace/call/token observation differs")
        records.append({"seed": seed, "wall_seconds": record["wall_seconds"], "model_calls": calls, "generated_tokens": tokens,
            "accelerator": record["accelerator"], "observer_source": audit["observer_source"],
            "instrumentation": record["instrumentation"],
            "execution_config_sha256": execution_sha, "run_config_sha256": config_sha,
            "peak_gpu_memory_allocated_bytes": record["peak_gpu_memory_allocated_bytes"],
            "peak_gpu_memory_reserved_bytes": record["peak_gpu_memory_reserved_bytes"],
            "original_observer_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "raw_sha256": record["raw_sha256"], "trace_sha256": record["trace_sha256"]})
    return records, run_config


def curate(directory: Path, commit: str, source_archive: Path, *, accelerator_model="NVIDIA A30",
           observer_commit=None, observer_archive=None, config_path=None) -> dict:
    if accelerator_model not in ("NVIDIA A30", "NVIDIA A100-SXM4-80GB"):
        raise ValueError("explicit supported accelerator model required")
    a100 = accelerator_model == "NVIDIA A100-SXM4-80GB"
    runs = [json.loads((directory / f"seed{seed}.json").read_text()) for seed in SEEDS]
    for seed, run in zip(SEEDS, runs, strict=True):
        if (run.get("paper") != "skilldreamer" or run.get("seed") != seed
                or run.get("device") != "cuda" or run.get("diagnostic_only") is not True
                or run.get("promotion_eligible") is not False or set(run["variants"]) != set(ARMS)):
            raise ValueError("matching actual CUDA diagnostic seed and three arms required")
        if run["protocol"].get("gold_visible_to_policy") is not False:
            raise ValueError("gold answers must stay outside the policy")
        source = run["protocol"]["dataset"]
        if source.get("source_split") != "train" or source.get("official_test_opened") is not False:
            raise ValueError("only verified train-derived inputs, no official test, are in scope")
        for arm in ARMS:
            if len(run["episodes"][arm]) != len(run["protocol"]["test_ids"]):
                raise ValueError("all episodes, including generation failures, must remain")
            episodes=run["episodes"][arm]
            if (sum(row.get("model_calls_including_psg",0) for row in episodes)!=run["variants"][arm]["model_calls"]
                    or sum(row.get("executed_actions",0) for row in episodes)!=run["variants"][arm]["executed_actions"]
                    or not all(type(value) in {int,float} and math.isfinite(value)
                               for value in run["variants"][arm].values())):
                raise ValueError("finite measured summaries must match actual episode calls/actions")
        episodes=run["episodes"]["skilldreamer"]
        if (sum(len(row.get("capability_checks",[])) for row in episodes)<1
                or not any(row.get("loaded_skills") for row in episodes)
                or sum(row.get("executed_actions",0) for row in episodes)<1):
            raise ValueError("GPU completion requires actual CSI assessment, gallery loading and tool execution in every seed")
    if any(run["protocol"] != runs[0]["protocol"] for run in runs[1:]):
        raise ValueError("all seeds must share exactly the same frozen input and protocol")
    paths = ["scripts/run_skilldreamer.py", "src/auto_research/reproductions/skilldreamer/experiment.py",
             "src/auto_research/reproductions/skilldreamer/algorithm.py",
             "src/auto_research/reproductions/skilldreamer/gallery.json",
             "src/auto_research/reproductions/near/data.py", "src/auto_research/reproductions/near/experiment.py",
             "src/auto_research/reproductions/state_opd/environment.py"]
    hashes = {}
    with tarfile.open(source_archive) as archive:
        for name in paths:
            committed = subprocess.check_output(["git", "show", f"{commit}:{name}"], cwd=ROOT)
            packed = archive.extractfile(name).read()
            if committed != packed:
                raise ValueError("deployed source archive and executed commit differ")
            hashes[name] = hashlib.sha256(packed).hexdigest()
    observer_records, actual_config = a100_observers(directory, runs, commit, hashes, observer_commit,
                                                    observer_archive, config_path) if a100 else ([], None)
    metrics = {f"{arm}.{key}": {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": 3}
               for arm in ARMS for key in runs[0]["variants"][arm]
               for values in [[run["variants"][arm][key] for run in runs]]}
    artifact = f"{DOC}/public-a100-seeds42-44-47f0e9ce.json" if a100 else f"{DOC}/public-a30-seeds42-44.json"
    receipt_path = "docs/gpu-validations/oct13-skilldreamer-a100.json" if a100 else "docs/gpu-validations/oct13-skilldreamer-a30.json"
    raw = {}
    for seed in SEEDS:
        content = (directory / f"seed{seed}.json").read_bytes()
        relative = f"{DOC}/raw/a100-47f0e9ce/seed{seed}.json" if a100 else f"{DOC}/raw/seed{seed}.json"
        target = ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != content:
            raise FileExistsError("immutable raw evidence differs")
        target.write_bytes(content)
        raw[str(seed)] = {"artifact_path": relative, "sha256": hashlib.sha256(content).hexdigest()}
    limitations = ["Train-derived 24-row arithmetic live-interaction diagnostic; not official GSM8K test.",
        "Not SkillUsage/SkillRet/SkillNet-Gym, original model scale, or original skill-gallery benchmark.",
        "All failed generations/tool episodes are kept; skill loading alone is not success.",
        "Three seeds do not establish formal capability comparison or authorize promotion."]
    if a100:
        limitations.append("Original runner tier l2_public_dataset is retained byte-for-byte in raw results; the envelope is assessed as L1 because restricted arithmetic and a local gallery replace the original skill benchmark.")
    payload = {"schema_version": 2, "adapter_key": "skilldreamer", "manifest_ref": "reproduction:skilldreamer",
        "seeds": list(SEEDS), "diagnostic_only": True, "promotion_eligible": False, "measured_locally": True,
        "aggregate_metrics": metrics, "seed_results": runs, "raw_artifacts": raw,
        "evaluation_protocol": {"tier": "l1_mechanism" if a100 else "l2_public_dataset", "formal_comparison": False,
            "seeds": list(SEEDS), "claim_policy": "measured mechanism diagnostic; accuracy is external-scored, not capability improvement or promotion",
            "gold_visible_to_policy": False, "official_test_opened": False,
            "protocol": runs[0]["protocol"]},
        "dataset": runs[0]["protocol"]["dataset"],
        "provenance": {"code_commit": commit, "artifact_path": artifact,
            "dataset_fingerprint": hashlib.sha256(json.dumps(runs[0]["protocol"]["dataset"], sort_keys=True).encode()).hexdigest()},
        "limitations": limitations}
    checks = {"completed_seeds": 3, "actual_model_calls": [sum(v["model_calls"] for v in run["variants"].values()) for run in runs],
        "executed_actions": [sum(v["executed_actions"] for v in run["variants"].values()) for run in runs],
        "actual_csi_assessments": [sum(len(episode.get("capability_checks", []))
            for episode in run["episodes"]["skilldreamer"]) for run in runs],
        "skilldreamer_loaded_skill_episodes": [sum(bool(episode.get("loaded_skills"))
            for episode in run["episodes"]["skilldreamer"]) for run in runs],
        "skilldreamer_executed_actions": [run["variants"]["skilldreamer"]["executed_actions"] for run in runs],
        "all_generation_failures_retained": True, "gold_visible_to_policy": False,
        "official_test_opened": False, "diagnostic_only": True, "promotion_eligible": False}
    receipt = {"schema_version": 1, "adapter_key": "skilldreamer",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "accelerator": {"vendor": "NVIDIA", "model": accelerator_model},
        "command": ["python", "scripts/run_skilldreamer.py", "--config", "data/skilldreamer.json",
                    "--seed", "42", "--output", "runs/skilldreamer/seed42.json"],
        "config": {"device": "cuda", "max_queries": 24, "max_new_tokens": 256, "top_k": 3, "action_budget": 8},
        "seeds": list(SEEDS), "dataset": runs[0]["protocol"]["dataset"],
        "checkpoint": {"generator": runs[0]["protocol"]["checkpoint"], "encoder": runs[0]["protocol"]["encoder"]},
        "result": "passed", "metrics": metrics, "execution_checks": checks,
        "raw_artifacts": raw, "executed_source_sha256": hashes,
        "executed_source_archive_sha256": hashlib.sha256(source_archive.read_bytes()).hexdigest(),
        "provenance": {"commit": commit, "artifact_path": receipt_path, "metrics_artifact": artifact,
                       "checkpoint_committed": False}, "limitations": limitations}
    if a100:
        payload["evaluation_protocol"]["original_runner_tier"] = "l2_public_dataset"
        payload["evaluation_protocol"]["assessed_scope_reason"] = "restricted arithmetic and a local skill gallery substitute for the original skill benchmark; measured mechanism diagnostic only, not capability comparison or promotion"
        payload["observer_records"] = observer_records
        checks["allocator_peak_allocated_bytes"] = [row["peak_gpu_memory_allocated_bytes"] for row in observer_records]
        checks["allocator_peak_reserved_bytes"] = [row["peak_gpu_memory_reserved_bytes"] for row in observer_records]
        receipt["command"] = ["python", "scripts/observe_oct14_skilldreamer.py", "--config", "data/skilldreamer-full7b.json",
                              "--seed", "42", "--output", "runs/skilldreamer/seed42"]
        receipt["all_sanitized_commands"] = [["python", "scripts/observe_oct14_skilldreamer.py", "--config", "data/skilldreamer-full7b.json",
            "--seed", str(seed), "--output", f"runs/skilldreamer/seed{seed}"] for seed in SEEDS]
        checks["call_instrumentation"] = [row["instrumentation"] for row in observer_records]
        receipt["config"] = {name: actual_config[name] for name in ("device", "max_queries", "max_new_tokens", "top_k", "action_budget")}
        receipt["observer_source"] = {"commit": observer_commit,
            "sha256": observer_records[0]["observer_source"]["sha256"],
            "archive_sha256": hashlib.sha256(observer_archive.read_bytes()).hexdigest()}
        receipt["execution_config_sha256"] = observer_records[0]["execution_config_sha256"]
    if errors := validate_gpu_receipt(receipt):
        raise ValueError(errors)
    for relative, document in ((artifact, payload), (receipt_path, receipt)):
        target = ROOT / relative
        if target.exists():
            raise FileExistsError("immutable curated evidence already exists")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    return {"metrics": metrics, "checks": checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--executed-commit", required=True)
    parser.add_argument("--source-archive", type=Path, required=True)
    parser.add_argument("--accelerator-model", choices=("NVIDIA A30", "NVIDIA A100-SXM4-80GB"), default="NVIDIA A30")
    parser.add_argument("--observer-commit")
    parser.add_argument("--observer-archive", type=Path)
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()
    print(json.dumps(curate(args.input, args.executed_commit, args.source_archive, accelerator_model=args.accelerator_model,
                           observer_commit=args.observer_commit, observer_archive=args.observer_archive, config_path=args.config), indent=2))
