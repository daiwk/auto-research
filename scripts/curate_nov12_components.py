"""Admit the fixed November 12 L1 runs, preserving cost and evidence boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from curate_nov04_components import (
    aggregate_metrics, evaluation_protocol, generated_input_fingerprint, metrics, write_new,
)
from oct18_frozen_sources import verify_sources
from run_nov04_components import validate_diagnostic
from run_nov12_components import AUDIT, BATCH, COMPONENTS, CUDA_KEYS, ROOT, SEEDS, preflight, source_hashes


def validate_raw(raw: dict, device: str, frozen: dict) -> None:
    expected = set(COMPONENTS) if device == "cpu" else CUDA_KEYS
    elapsed = raw.get("elapsed_seconds")
    if (device not in {"cpu", "cuda"} or raw.get("device") != device
            or raw.get("schema_version") != 2 or raw.get("batch") != BATCH
            or set(raw.get("components", {})) != expected or raw.get("seeds") != SEEDS
            or raw.get("code_commit") != frozen["commit"]
            or raw.get("source_sha256") != frozen["source_sha256"]
            or frozen["source_sha256"] != source_hashes()
            or raw.get("diagnostic_only") is not True or raw.get("evaluation_tier") != "l1_mechanism"
            or raw.get("formal_comparison") is not False or raw.get("pretrained_model_calls") != 0
            or raw.get("full_experiments_executed") is not False or raw.get("promotion_eligible") is not False
            or raw.get("evolve_integrated") is not False or raw.get("automatic_retry") is not False
            or type(elapsed) not in {int, float} or not math.isfinite(elapsed)
            or not 0 <= elapsed <= preflight()["maximum_run_seconds"]):
        raise ValueError("raw evidence differs from the frozen short-budget scope")
    accelerator = raw.get("accelerator", "")
    if (device == "cpu" and accelerator != "CPU") or (
            device == "cuda" and not accelerator.startswith("NVIDIA A100")):
        raise ValueError("this cohort's receipt filenames require actual A100 execution")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    for record in raw["components"].values():
        rows = record["per_seed"]
        if [row["seed"] for row in rows] != SEEDS:
            raise ValueError("each component needs the exact actual seed rows")
        for row, seed in zip(rows, SEEDS, strict=True):
            validate_diagnostic(row, seed)
            if (row.get("diagnostic_only") is not True or row.get("evaluation_tier") != "l1_mechanism"
                    or row.get("execution_device") != device
                    or row.get("execution_accelerator") != accelerator or not metrics(row)):
                raise ValueError("per-seed execution contract differs")


def ingest(cpu: Path, cuda: Path) -> None:
    from auto_research.gpu_validation import validate_gpu_receipt

    frozen = json.loads((AUDIT / "frozen-sources.json").read_text())
    blobs = {"cpu": cpu.read_bytes(), "cuda": cuda.read_bytes()}
    runs = {device: json.loads(blob) for device, blob in blobs.items()}
    for device, raw in runs.items():
        validate_raw(raw, device, frozen)
    specifications = {}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        spec = json.loads(path.read_text())
        if spec["key"] in COMPONENTS:
            if spec["key"] in specifications:
                raise ValueError("ambiguous catalog key")
            specifications[spec["key"]] = (path, spec)
    if set(specifications) != set(COMPONENTS):
        raise ValueError("the fixed component catalog is incomplete")
    pending = []
    for key, (domain, module) in COMPONENTS.items():
        device = "cuda" if key in CUDA_KEYS else "cpu"
        spec_path, spec = specifications[key]
        if (spec.get("domain") != domain or spec.get("requires_gpu_validation") is not (device == "cuda")
                or spec.get("implementation_status") != "component_only"
                or spec.get("full_experiment_status") != (
                    "not_applicable_theory_only" if key == "apmd-reference-reset" else "not_reproduced_high_cost")
                or spec.get("full_experiment_review_done") is not True
                or spec.get("promotion_eligible") is not False or spec.get("evolve_integrated") is not False):
            raise ValueError(f"catalog evidence/cost boundary differs: {key}")
        raw = runs[device]
        seed_rows = raw["components"][key]["per_seed"]
        summary = aggregate_metrics(seed_rows)
        artifact = Path("docs") / Path(spec["detail_path"]).parent / f"metrics/component-{device}-seeds42-44.json"
        dataset = {
            "id": f"synthetic:nov12-{key}-v1",
            "revision": "sha256:" + frozen["source_sha256"]["src/auto_research/" + module],
            "recipe": preflight()["input_scope"], "capability_benchmark": False,
        }
        provenance = {
            "commit": frozen["commit"], "artifact_path": artifact.as_posix(), "accelerator": raw["accelerator"],
            "executed_source_sha256": frozen["source_sha256"],
            "dataset_fingerprint": generated_input_fingerprint(dataset, frozen["source_sha256"]),
            "raw_runner_artifact_sha256": hashlib.sha256(blobs[device]).hexdigest(),
        }
        result = {
            "schema_version": 2, "method": key, "manifest_ref": f"{domain}:{key}",
            "dataset": dataset, "seed": SEEDS, "seeds": SEEDS, "per_seed": seed_rows, "metrics": summary,
            "diagnostic_only": True, "fixture_demo": True, "formal_comparison": False,
            "evaluation_tier": "l1_mechanism", "evaluation_protocol": evaluation_protocol(),
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": spec["full_experiment_status"], "full_experiment_review_done": True,
            "automatic_retry": False, "automatic_implementation_queue": False, "provenance": provenance,
        }
        pending.append((ROOT / artifact, result))
        if device == "cuda":
            receipt_path = f"docs/gpu-validations/{key}-a100-20261112.json"
            if spec.get("gpu_validation_artifact") != receipt_path:
                raise ValueError(f"GPU receipt target differs: {key}")
            receipt = {
                "schema_version": 1, "adapter_key": key, "validated_at": "2026-11-12",
                "accelerator": {"vendor": "NVIDIA", "model": raw["accelerator"], "count": 1},
                "command": ["timeout", "180", "python3", "scripts/run_nov12_components.py",
                            "--device", "cuda", "--source-commit", frozen["commit"],
                            "--frozen-proof", "docs/research-audits/nov12-components/frozen-sources.json",
                            "--output", "raw-cuda.json"],
                "dataset": dataset,
                "checkpoint": {"public_id": "none-seeded-component-initialization",
                               "revision": frozen["commit"], "pretrained": False},
                "seeds": SEEDS, "result": "passed", "metrics": summary, "diagnostic_only": True,
                "promotion_eligible": False, "evolve_integrated": False,
                "full_experiment_status": spec["full_experiment_status"],
                "provenance": provenance | {"artifact_path": receipt_path,
                                             "metric_artifact_path": artifact.as_posix()},
            }
            if errors := validate_gpu_receipt(receipt):
                raise ValueError(str(errors))
            pending.append((ROOT / receipt_path, receipt))
        specifications[key] = (spec_path, spec | {"gpu_validation_passed": device == "cuda"})
    pending.extend((AUDIT / f"raw-{device}.json", raw) for device, raw in runs.items())
    if any(path.exists() for path, _ in pending):
        raise ValueError("accepted execution artifacts must not be overwritten")
    for path, record in pending:
        write_new(path, record)
    for path, spec in specifications.values():
        path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    print("accepted eight L1 components, including three actual A100 executions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpu", type=Path, required=True)
    parser.add_argument("--cuda", type=Path, required=True)
    args = parser.parse_args()
    ingest(args.cpu, args.cuda)
