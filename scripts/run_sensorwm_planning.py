"""Freeze, execute and verify a CPU-only SensorWM planning arithmetic diagnostic."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import math
from pathlib import Path
import subprocess
import time

from oct18_frozen_sources import capture_sources, verify_sources

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov12-refresh"
KEY = "sensorwm-planning"
BATCH = "2026-11-12-official-source-refresh"
MODULE = "src/auto_research/multimodal/sensorwm_planning.py"
METRIC = ROOT / "docs/multimodal-models/2611.08568-sensorwm-planning/metrics/component-cpu-seeds42-44.json"
SEEDS = [42, 43, 44]
SOURCES = ["scripts/run_sensorwm_planning.py", "scripts/oct18_frozen_sources.py", MODULE,
           "docs/research-audits/nov12-refresh/preflight.json"]


def load(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_new(path, payload):
    if path.exists():
        raise ValueError(f"refusing to overwrite accepted evidence: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def source_hashes():
    return {path: digest(ROOT / path) for path in SOURCES}


def validate(raw, frozen):
    if (frozen["source_sha256"] != source_hashes()
            or raw.get("source_sha256") != frozen["source_sha256"]
            or raw.get("code_commit") != frozen["commit"]
            or raw.get("batch") != BATCH or raw.get("component") != KEY
            or raw.get("device") != "cpu" or raw.get("accelerator") != "CPU"
            or raw.get("seeds") != SEEDS or raw.get("diagnostic_only") is not True
            or raw.get("evaluation_tier") != "l1_mechanism"
            or raw.get("formal_comparison") is not False
            or raw.get("promotion_eligible") is not False or raw.get("evolve_integrated") is not False
            or raw.get("pretrained_model_calls") != 0 or raw.get("api_calls") != 0
            or raw.get("full_experiments_executed") is not False or raw.get("automatic_retry") is not False):
        raise ValueError("CPU diagnostic scope or frozen source identity changed")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    preflight = load(AUDIT / "preflight.json")
    elapsed = raw.get("elapsed_seconds")
    if (type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not 0 <= elapsed <= preflight["maximum_run_seconds"]):
        raise ValueError("short CPU budget was exceeded or relabelled")
    rows = raw.get("per_seed", [])
    if [row.get("seed") for row in rows] != SEEDS:
        raise ValueError("the exact three actual seed rows are required")
    keys = set(rows[0].get("metrics", {}))
    for row in rows:
        if (row.get("execution_device") != "cpu" or row.get("execution_accelerator") != "CPU"
                or row.get("diagnostic_only") is not True or row.get("evaluation_tier") != "l1_mechanism"
                or not row.get("checks") or any(value is not True for value in row["checks"].values())
                or not keys or set(row.get("metrics", {})) != keys
                or any(type(v) not in (int, float) or not math.isfinite(v) for v in row["metrics"].values())):
            raise ValueError("actual seed checks, finite mechanism metrics and CPU stamps required")


def metric(raw, frozen):
    dataset = {"id": "synthetic:sensorwm-planning-arithmetic-v1",
               "revision": "sha256:" + frozen["source_sha256"][MODULE],
               "kind": "nonclinical_formula_fixtures", "public_capability_benchmark": False,
               "source": "Explicit endpoint/target fixtures; no observed participant or model-generated predictions"}
    aggregate = {key: math.fsum(row["metrics"][key] for row in raw["per_seed"]) / len(SEEDS)
                 for key in sorted(raw["per_seed"][0]["metrics"])}
    return {"schema_version": 2, "method": KEY, "manifest_ref": "multimodal-models:" + KEY,
            "dataset": dataset, "seed": SEEDS, "seeds": SEEDS, "per_seed": raw["per_seed"],
            "metrics": aggregate, "diagnostic_only": True, "fixture_demo": True,
            "evaluation_tier": "l1_mechanism", "formal_comparison": False,
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                                    "claim_policy": "Equation-level arithmetic and contract checks; not clinical, forecasting or Agent capability"},
            "promotion_eligible": False, "evolve_integrated": False, "automatic_retry": False,
            "automatic_implementation_queue": False, "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True,
            "provenance": {"commit": frozen["commit"], "accelerator": "CPU",
                           "artifact_path": METRIC.relative_to(ROOT).as_posix(),
                           "executed_source_sha256": frozen["source_sha256"],
                           "dataset_fingerprint": "sha256:" + hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest(),
                           "raw_runner_artifact_sha256": digest(AUDIT / "raw-cpu.json")}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--freeze", action="store_true")
    mode.add_argument("--run", type=Path, metavar="OUTPUT")
    mode.add_argument("--admit", type=Path, metavar="RAW")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        hashes, proof = source_hashes(), capture_sources(ROOT, commit, SOURCES)
        verify_sources(ROOT, commit, hashes, proof)
        write_new(AUDIT / "frozen-sources.json", {"schema_version": 1, "commit": commit,
                                                "source_sha256": hashes, "proof": proof})
        print("frozen four CPU execution files at " + commit)
        return
    frozen = load(AUDIT / "frozen-sources.json")
    if args.run:
        verify_sources(ROOT, frozen["commit"], source_hashes(), frozen["proof"])
        component = importlib.import_module("auto_research.multimodal.sensorwm_planning")
        if Path(component.__file__).resolve() != ROOT / MODULE or component.REQUIRES_GPU_VALIDATION is not False:
            raise ValueError("frozen CPU-only component required")
        started = time.monotonic()
        rows = [component.diagnostic(seed, device="cpu") | {"execution_device": "cpu", "execution_accelerator": "CPU"}
                for seed in SEEDS]
        raw = {"schema_version": 2, "batch": BATCH, "component": KEY, "device": "cpu", "accelerator": "CPU",
               "seeds": SEEDS, "code_commit": frozen["commit"], "source_sha256": frozen["source_sha256"],
               "per_seed": rows, "elapsed_seconds": time.monotonic() - started, "diagnostic_only": True,
               "evaluation_tier": "l1_mechanism", "formal_comparison": False, "promotion_eligible": False,
               "evolve_integrated": False, "pretrained_model_calls": 0, "api_calls": 0,
               "full_experiments_executed": False, "automatic_retry": False}
        validate(raw, frozen)
        write_new(args.run, raw)
        print(json.dumps({"component": KEY, "seeds": SEEDS, "device": "cpu", "elapsed_seconds": raw["elapsed_seconds"]}))
    elif args.admit:
        raw = load(args.admit)
        validate(raw, frozen)
        write_new(AUDIT / "raw-cpu.json", raw)
        write_new(METRIC, metric(raw, frozen))
        print("accepted CPU arithmetic evidence; no clinical or model capability claim")
    else:
        raw = load(AUDIT / "raw-cpu.json")
        validate(raw, frozen)
        if load(METRIC) != metric(raw, frozen):
            raise ValueError("metric artifact differs from actual frozen execution")
        print("portable CPU execution evidence passed; source web captures not reread")


if __name__ == "__main__":
    main()
