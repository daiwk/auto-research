"""Bind actual short CPU/CUDA runs without promoting diagnostic evidence."""

from __future__ import annotations
import argparse
import hashlib
import json
import math
from oct18_frozen_sources import verify_sources
from run_nov18_latest_components import (
    AUDIT,
    ROOT,
    SEEDS,
    config,
    load,
    source_hashes,
    validate_raw,
)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path, payload, check):
    if check:
        if load(path) != payload:
            raise ValueError("accepted evidence differs from frozen execution: " + str(path))
        return
    if path.exists():
        if load(path) != payload:
            raise ValueError("refusing to overwrite immutable evidence: " + str(path))
        return  # exact idempotent admission after a partial integration, never an overwrite
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def metric(key, item, spec, raw, frozen):
    rows = raw["components"][key]["per_seed"]
    device = raw["device"]
    dataset = {
        "id": f"synthetic:nov18-latest-{key}-component-v1",
        "kind": "explicit_protocol_or_mechanism_fixtures",
        "revision": "sha256:" + frozen["source_sha256"]["src/auto_research/" + item["module"]],
        "public_capability_benchmark": False,
        "source": "Seeded small tensors or explicit deterministic evaluator/control cases; no pretrained output or public capability measurement",
    }
    artifact = "docs/" + spec["detail_path"].replace(
        "README.md", f"metrics/component-{device}-seeds42-44.json"
    )
    return {
        "schema_version": 2,
        "method": key,
        "manifest_ref": item["domain"] + ":" + key,
        "dataset": dataset,
        "seed": SEEDS,
        "seeds": SEEDS,
        "per_seed": rows,
        "metrics": {
            name: math.fsum(r["metrics"][name] for r in rows) / len(rows)
            for name in sorted(rows[0]["metrics"])
        },
        "diagnostic_only": True,
        "fixture_demo": True,
        "evaluation_tier": item["evaluation_tier"],
        "formal_comparison": False,
        "promotion_eligible": False,
        "evolve_integrated": False,
        "evaluation_protocol": {
            "tier": item["evaluation_tier"],
            "seeds": SEEDS,
            "formal_comparison": False,
            "claim_policy": "Operator/interface controls only; not a complete model, agent, public benchmark or production comparison",
        },
        "full_experiment_status": spec["full_experiment_status"],
        "full_experiment_review_done": True,
        "automatic_retry": False,
        "automatic_implementation_queue": False,
        "provenance": {
            "commit": frozen["commit"],
            "accelerator": raw["accelerator"],
            "artifact_path": artifact,
            "executed_source_sha256": frozen["source_sha256"],
            "dataset_fingerprint": "sha256:"
            + hashlib.sha256(json.dumps(dataset, sort_keys=True).encode()).hexdigest(),
            "raw_runner_artifact_sha256": digest(AUDIT / f"raw-{device}.json"),
        },
    }


def receipt(key, spec, payload, frozen):
    return {
        "schema_version": 1,
        "adapter_key": key,
        "validated_at": "2026-11-18",
        "accelerator": {
            "vendor": "NVIDIA",
            "model": payload["provenance"]["accelerator"],
            "count": 1,
        },
        "command": [
            "timeout",
            "180",
            "python3",
            "scripts/run_nov18_latest_components.py",
            "--device",
            "cuda",
            "--source-commit",
            frozen["commit"],
            "--output",
            "raw-cuda.json",
        ],
        "dataset": {
            "id": payload["dataset"]["id"],
            "revision": payload["dataset"]["revision"],
            "recipe": payload["dataset"]["source"],
            "capability_benchmark": False,
        },
        "checkpoint": {
            "public_id": "none-seeded-component-initialization",
            "revision": frozen["commit"],
            "pretrained": False,
        },
        "seeds": SEEDS,
        "result": "passed",
        "metrics": payload["metrics"],
        "diagnostic_only": True,
        "evaluation_tier": payload["evaluation_tier"],
        "promotion_eligible": False,
        "evolve_integrated": False,
        "full_experiment_status": spec["full_experiment_status"],
        "provenance": payload["provenance"]
        | {
            "artifact_path": spec["gpu_validation_artifact"],
            "metric_artifact_path": payload["provenance"]["artifact_path"],
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    frozen = load(AUDIT / "frozen-sources.json")
    if frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source changed after real run")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    raw = {device: load(AUDIT / f"raw-{device}.json") for device in ("cpu", "cuda")}
    for value in raw.values():
        validate_raw(value, frozen)
    for key, item in config()["components"].items():
        path = ROOT / f"src/auto_research/paper_specs/catalog/{item['domain']}/{key}.json"
        spec = load(path)
        if (
            spec["evaluation_tier"] != item["evaluation_tier"]
            or spec["requires_gpu_validation"] is not item["cuda"]
        ):
            raise ValueError("spec tier/device contradicts actual scope: " + key)
        if item["cuda"]:
            expected = f"docs/gpu-validations/{key}-a100-20261118-latest.json"
            if spec.get("gpu_validation_artifact", expected) != expected:
                raise ValueError("wrong receipt binding: " + key)
            spec["gpu_validation_artifact"] = expected
        for device in ("cpu", "cuda") if item["cuda"] else ("cpu",):
            payload = metric(key, item, spec, raw[device], frozen)
            put(ROOT / payload["provenance"]["artifact_path"], payload, args.check)
            if device == "cuda":
                put(
                    ROOT / spec["gpu_validation_artifact"],
                    receipt(key, spec, payload, frozen),
                    args.check,
                )
        if item["cuda"]:
            if args.check:
                if spec.get("gpu_validation_passed") is not True:
                    raise ValueError("actual GPU receipt not bound: " + key)
            else:
                spec["gpu_validation_passed"] = True
                path.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n")
    print(
        json.dumps(
            {
                "cpu_components": len(config()["components"]),
                "cuda_components": sum(x["cuda"] for x in config()["components"].values()),
                "capability_promotions": 0,
            }
        )
    )


if __name__ == "__main__":
    main()
