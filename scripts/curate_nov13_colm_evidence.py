"""Admit actual bounded CPU/CUDA runs without upgrading their evidence tier."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from oct18_frozen_sources import verify_sources
from run_nov13_colm_components import (
    AUDIT, COMPONENTS, CUDA_KEYS, ROOT, SEEDS, load, source_hashes, tier, validate_raw,
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_admission(raw, frozen):
    """Reject contradictory evidence rather than rewriting its labels on admission.

    The frozen runner proves actual execution. This separate admission gate can
    be tightened without changing or rerunning those already executed sources.
    """
    validate_raw(raw, frozen)
    expected = {"schema_version": 2, "diagnostic_only": True,
                "evaluation_tier": "mixed_l0_interface_l1_mechanism",
                "formal_comparison": False, "promotion_eligible": False,
                "evolve_integrated": False, "pretrained_model_calls": 0,
                "full_experiments_executed": False, "automatic_retry": False}
    if any(type(raw.get(key)) is not type(value) or raw.get(key) != value for key, value in expected.items()):
        raise ValueError("raw execution contradicts the bounded diagnostic claim")
    device = raw["device"]
    for key, value in raw["components"].items():
        names = set(value["per_seed"][0]["metrics"])
        if value.get("evaluation_tier") != tier(key):
            raise ValueError("component tier contradicts actual scope")
        for row in value["per_seed"]:
            if "device" in row and row["device"] != device:
                raise ValueError("component-reported device contradicts execution stamp")
            if set(row["metrics"]) != names:
                raise ValueError("metric names differ across actual seeds")


def put(path, payload, check):
    if check:
        if load(path) != payload:
            raise ValueError("accepted evidence differs from frozen execution: " + str(path))
        return
    if path.exists():
        raise ValueError("refusing to overwrite execution evidence: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def metric(key, spec, raw, frozen):
    domain, module = COMPONENTS[key]
    device = raw["device"]
    rows = raw["components"][key]["per_seed"]
    names = set(rows[0]["metrics"])
    if any(set(row["metrics"]) != names for row in rows):
        raise ValueError("metric keys changed across seeds")
    dataset = {"id": f"synthetic:colm-{key}-component-v1", "kind": "explicit_mechanism_or_protocol_fixtures",
               "revision": "sha256:" + frozen["source_sha256"]["src/auto_research/" + module],
               "public_capability_benchmark": False,
               "source": "Seeded tensors or explicit evaluator/control examples; no pretrained output, public dataset or model capability score"}
    artifact = "docs/" + spec["detail_path"].replace("README.md", f"metrics/component-{device}-seeds42-44.json")
    return {"schema_version": 2, "method": key, "manifest_ref": domain + ":" + key,
            "dataset": dataset, "seed": SEEDS, "seeds": SEEDS, "per_seed": rows,
            "metrics": {name: math.fsum(row["metrics"][name] for row in rows) / len(rows) for name in sorted(names)},
            "diagnostic_only": True, "fixture_demo": True, "evaluation_tier": tier(key),
            "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
            "evaluation_protocol": {"tier": tier(key), "seeds": SEEDS, "formal_comparison": False,
                                    "claim_policy": "Exact operator arithmetic and interface checks only; not a complete model, agent or benchmark comparison"},
            "automatic_retry": False, "automatic_implementation_queue": False,
            "full_experiment_status": spec["full_experiment_status"], "full_experiment_review_done": True,
            "provenance": {"commit": frozen["commit"], "accelerator": raw["accelerator"],
                           "artifact_path": artifact, "executed_source_sha256": frozen["source_sha256"],
                           "dataset_fingerprint": "sha256:" + hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest(),
                           "raw_runner_artifact_sha256": digest(AUDIT / f"raw-{device}.json")}}


def gpu_receipt(key, spec, payload, frozen):
    return {"schema_version": 1, "adapter_key": key, "validated_at": "2026-11-13",
            "accelerator": {"vendor": "NVIDIA", "model": payload["provenance"]["accelerator"], "count": 1},
            "command": ["timeout", "180", "python3", "scripts/run_nov13_colm_components.py", "--device", "cuda",
                        "--source-commit", frozen["commit"], "--output", "raw-cuda.json"],
            "dataset": {"id": payload["dataset"]["id"], "revision": payload["dataset"]["revision"],
                        "recipe": payload["dataset"]["source"], "capability_benchmark": False},
            "checkpoint": {"public_id": "none-seeded-component-initialization", "revision": frozen["commit"], "pretrained": False},
            "seeds": SEEDS, "result": "passed", "metrics": payload["metrics"],
            "diagnostic_only": True, "evaluation_tier": tier(key), "promotion_eligible": False,
            "evolve_integrated": False, "full_experiment_status": spec["full_experiment_status"],
            "provenance": payload["provenance"] | {"artifact_path": spec["gpu_validation_artifact"],
                                                     "metric_artifact_path": payload["provenance"]["artifact_path"]}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source changed after freeze")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    raw = {device: load(AUDIT / f"raw-{device}.json") for device in ("cpu", "cuda")}
    for report in raw.values():
        validate_admission(report, frozen)
    for key, (domain, _) in COMPONENTS.items():
        path = ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json"
        spec = load(path)
        if spec.get("evaluation_tier") != tier(key) or spec.get("requires_gpu_validation") is not (key in CUDA_KEYS):
            raise ValueError("spec tier/device differs from actual component: " + key)
        for device in (("cpu", "cuda") if key in CUDA_KEYS else ("cpu",)):
            payload = metric(key, spec, raw[device], frozen)
            put(ROOT / payload["provenance"]["artifact_path"], payload, args.check)
            if device == "cuda":
                put(ROOT / spec["gpu_validation_artifact"], gpu_receipt(key, spec, payload, frozen), args.check)
        if key in CUDA_KEYS:
            if args.check:
                if spec.get("gpu_validation_passed") is not True:
                    raise ValueError("accepted CUDA receipt not bound by spec: " + key)
            else:
                spec["gpu_validation_passed"] = True
                path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    print("verified 23 CPU and 7 real CUDA three-seed components; no capability promotion")


if __name__ == "__main__":
    main()
