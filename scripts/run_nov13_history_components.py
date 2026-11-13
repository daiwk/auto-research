"""Freeze and validate bounded CPU control diagnostics for six-paper backfill.

Four exact components run, two papers are review-only. No LLM, generated program,
scientific benchmark, API or CUDA job is executed by this evidence runner.
"""
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
AUDIT = ROOT / "docs/research-audits/nov13-history-repair"
BATCH = "2026-11-13-scientisttwo-history-repair"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "scientist-two": ("scientist_two", "2609.19644-scientist-two"),
    "ds-star": ("ds_star", "2509.21825-ds-star"),
    "era-flat-puct": ("era_flat_puct", "2509.06503-era-flat-puct"),
    "envharness": ("envharness", "2608.19880-envharness"),
}
FULL_STATUS = {key: ("not_reproduced_commercial_dependencies" if key == "ds-star"
                    else "not_reproduced_high_cost") for key in COMPONENTS}
MODULES = {key: f"src/auto_research/agent_research/{module}.py"
           for key, (module, _) in COMPONENTS.items()}
SOURCES = ["scripts/run_nov13_history_components.py", "scripts/oct18_frozen_sources.py",
           "docs/research-audits/nov13-history-repair/preflight.json", *MODULES.values()]


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


def metric_path(key):
    return ROOT / "docs/agent-research" / COMPONENTS[key][1] / "metrics/component-cpu-seeds42-44.json"


def validate(raw, frozen):
    if (frozen["source_sha256"] != source_hashes()
            or raw.get("source_sha256") != frozen["source_sha256"]
            or raw.get("code_commit") != frozen["commit"] or raw.get("batch") != BATCH
            or raw.get("device") != "cpu" or raw.get("accelerator") != "CPU"
            or raw.get("seeds") != SEEDS or raw.get("diagnostic_only") is not True
            or raw.get("evaluation_tier") != "l1_mechanism"
            or raw.get("formal_comparison") is not False
            or raw.get("promotion_eligible") is not False or raw.get("evolve_integrated") is not False
            or raw.get("pretrained_model_calls") != 0 or raw.get("api_calls") != 0
            or raw.get("full_experiments_executed") is not False or raw.get("automatic_retry") is not False
            or set(raw.get("components", {})) != set(COMPONENTS)):
        raise ValueError("CPU diagnostic scope or frozen source identity changed")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    elapsed = raw.get("elapsed_seconds")
    if (type(elapsed) not in (int, float) or not math.isfinite(elapsed)
            or not 0 <= elapsed <= load(AUDIT / "preflight.json")["maximum_run_seconds"]):
        raise ValueError("short CPU budget was exceeded or relabelled")
    for key, rows in raw["components"].items():
        if not isinstance(rows, list) or [row.get("seed") for row in rows] != SEEDS:
            raise ValueError(f"exact three actual seed rows required: {key}")
        keys = set(rows[0].get("metrics", {}))
        for row in rows:
            if (row.get("execution_device") != "cpu" or row.get("execution_accelerator") != "CPU"
                    or row.get("diagnostic_only") is not True or row.get("evaluation_tier") != "l1_mechanism"
                    or not row.get("checks") or any(v is not True for v in row["checks"].values())
                    or not keys or set(row.get("metrics", {})) != keys
                    or any(type(v) not in (int, float) or not math.isfinite(v) for v in row["metrics"].values())):
                raise ValueError(f"actual seed checks, finite mechanism metrics and CPU stamps required: {key}")


def metric(key, raw, frozen):
    rows = raw["components"][key]
    dataset = {"id": f"synthetic:{key}-control-contracts-v1", "kind": "explicit_control_truth_tables",
               "revision": "sha256:" + frozen["source_sha256"][MODULES[key]],
               "public_capability_benchmark": False,
               "source": "Explicit fixture callback outputs; no real model, research or environment capability"}
    aggregate = {name: math.fsum(row["metrics"][name] for row in rows) / len(SEEDS)
                 for name in sorted(rows[0]["metrics"])}
    return {"schema_version": 2, "method": key, "manifest_ref": "agent-research:" + key,
            "dataset": dataset, "seed": SEEDS, "seeds": SEEDS, "per_seed": rows, "metrics": aggregate,
            "diagnostic_only": True, "fixture_demo": True, "evaluation_tier": "l1_mechanism",
            "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                                    "claim_policy": "Control arithmetic and typed callback contracts only, not Agent or scientific capability"},
            "automatic_retry": False, "automatic_implementation_queue": False,
            "full_experiment_status": FULL_STATUS[key], "full_experiment_review_done": True,
            "provenance": {"commit": frozen["commit"], "accelerator": "CPU",
                           "artifact_path": metric_path(key).relative_to(ROOT).as_posix(),
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
        print("frozen four CPU execution components at " + commit)
        return
    frozen = load(AUDIT / "frozen-sources.json")
    if args.run:
        verify_sources(ROOT, frozen["commit"], source_hashes(), frozen["proof"])
        started, rows = time.monotonic(), {}
        for key, (module, _) in COMPONENTS.items():
            component = importlib.import_module("auto_research.agent_research." + module)
            if (Path(component.__file__).resolve() != ROOT / MODULES[key]
                    or component.REQUIRES_GPU_VALIDATION is not False):
                raise ValueError("frozen CPU-only component required")
            rows[key] = [component.diagnostic(seed, device="cpu")
                         | {"execution_device": "cpu", "execution_accelerator": "CPU"} for seed in SEEDS]
        raw = {"schema_version": 2, "batch": BATCH, "device": "cpu", "accelerator": "CPU", "seeds": SEEDS,
               "code_commit": frozen["commit"], "source_sha256": frozen["source_sha256"], "components": rows,
               "elapsed_seconds": time.monotonic() - started, "diagnostic_only": True,
               "evaluation_tier": "l1_mechanism", "formal_comparison": False, "promotion_eligible": False,
               "evolve_integrated": False, "pretrained_model_calls": 0, "api_calls": 0,
               "full_experiments_executed": False, "automatic_retry": False}
        validate(raw, frozen)
        write_new(args.run, raw)
        print(json.dumps({"components": list(rows), "seeds": SEEDS, "device": "cpu",
                          "elapsed_seconds": raw["elapsed_seconds"]}))
    elif args.admit:
        raw = load(args.admit)
        validate(raw, frozen)
        write_new(AUDIT / "raw-cpu.json", raw)
        for key in COMPONENTS:
            write_new(metric_path(key), metric(key, raw, frozen))
        print("accepted four CPU mechanism diagnostics; no model capability claim")
    else:
        raw = load(AUDIT / "raw-cpu.json")
        validate(raw, frozen)
        for key in COMPONENTS:
            if load(metric_path(key)) != metric(key, raw, frozen):
                raise ValueError("metric artifact differs from actual frozen execution: " + key)
        print("portable four-component CPU execution evidence passed")


if __name__ == "__main__":
    main()
