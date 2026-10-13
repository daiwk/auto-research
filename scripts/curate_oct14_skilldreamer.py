#!/usr/bin/env python3
"""Curate measured train-derived arithmetic diagnostics, including failures."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import tarfile

from auto_research.gpu_validation import validate_gpu_receipt

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (42, 43, 44)
ARMS = ("no_skills", "direct", "skilldreamer")
DOC = "docs/reproductions/2609.01642-skilldreamer/metrics"


def curate(directory: Path, commit: str, source_archive: Path) -> dict:
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
    metrics = {f"{arm}.{key}": {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": 3}
               for arm in ARMS for key in runs[0]["variants"][arm]
               for values in [[run["variants"][arm][key] for run in runs]]}
    artifact = f"{DOC}/public-a30-seeds42-44.json"
    receipt_path = "docs/gpu-validations/oct13-skilldreamer-a30.json"
    raw = {}
    for seed in SEEDS:
        content = (directory / f"seed{seed}.json").read_bytes()
        relative = f"{DOC}/raw/seed{seed}.json"
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
    payload = {"schema_version": 2, "adapter_key": "skilldreamer", "manifest_ref": "reproduction:skilldreamer",
        "seeds": list(SEEDS), "diagnostic_only": True, "promotion_eligible": False, "measured_locally": True,
        "aggregate_metrics": metrics, "seed_results": runs, "raw_artifacts": raw,
        "evaluation_protocol": {"tier": "l2_public_dataset", "formal_comparison": False,
            "gold_visible_to_policy": False, "official_test_opened": False,
            "protocol": runs[0]["protocol"]},
        "provenance": {"code_commit": commit, "artifact_path": artifact}, "limitations": limitations}
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
        "accelerator": {"vendor": "NVIDIA", "model": "NVIDIA A30"},
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
    args = parser.parse_args()
    print(json.dumps(curate(args.input, args.executed_commit, args.source_archive), indent=2))
