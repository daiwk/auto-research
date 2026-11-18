"""Run three bounded CPU backfills and write immutable per-paper diagnostics."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import time

from curate_nov04_components import (
    aggregate_metrics, evaluation_protocol, generated_input_fingerprint, write_new,
)
from oct18_frozen_sources import capture_sources, verify_sources
from run_nov04_components import validate_diagnostic

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov07-priority-backfill"
BATCH = "2026-11-07-priority-backfill"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "ginger": ("foundation-models", "2611.08306", "foundation_models.ginger"),
    "gslm2": ("multimodal-models", "2611.01143", "multimodal.gslm2"),
    "emoreward": ("post-training", "2611.06518", "post_training.emoreward"),
}


def module_path(module: str) -> str:
    return "src/auto_research/" + module.replace(".", "/") + ".py"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def spec_for(key: str) -> dict:
    domain, _, _ = COMPONENTS[key]
    return load(ROOT / "src/auto_research/paper_specs/catalog" / domain / f"{key}.json")


def metric_path(spec: dict) -> Path:
    return Path("docs") / Path(spec["detail_path"]).parent / "metrics/component-cpu-seeds42-44.json"


def validate_metric(key: str, value: dict, frozen: dict) -> None:
    domain, _, module = COMPONENTS[key]
    rows = value["per_seed"]
    provenance = value["provenance"]
    if (
        value["method"] != key or value["manifest_ref"] != f"{domain}:{key}"
        or value["seeds"] != SEEDS or [row["seed"] for row in rows] != SEEDS
        or value["evaluation_tier"] != "l1_mechanism" or value["diagnostic_only"] is not True
        or value["metrics"] != aggregate_metrics(rows)
        or value["full_experiment_status"] != "not_reproduced_high_cost"
        or value["full_experiment_review_done"] is not True
        or any(value[flag] is not False for flag in (
            "formal_comparison", "promotion_eligible", "evolve_integrated", "automatic_retry",
        ))
        or provenance["accelerator"] != "CPU" or provenance["commit"] != frozen["commit"]
        or provenance["executed_source_sha256"] != frozen["source_sha256"]
        or value["dataset"]["revision"] != "sha256:" + frozen["source_sha256"][module_path(module)]
        or value["dataset"]["capability_benchmark"] is not False
        or provenance["dataset_fingerprint"] != generated_input_fingerprint(
            value["dataset"], frozen["source_sha256"],
        )
    ):
        raise ValueError(f"{key}: invalid bounded CPU component evidence")
    for row, seed in zip(rows, SEEDS, strict=True):
        validate_diagnostic(row, seed)
        if (row["execution_device"] != "cpu" or row["execution_accelerator"] != "CPU"
                or row["diagnostic_only"] is not True or row["evaluation_tier"] != "l1_mechanism"):
            raise ValueError(f"{key}: invalid per-seed device or tier")


def main() -> None:
    preflight_path = AUDIT / "preflight.json"
    preflight = load(preflight_path)
    if (
        preflight["batch"] != BATCH or preflight["seeds"] != SEEDS or preflight["device"] != "cpu"
        or set(preflight["component_keys"]) != set(COMPONENTS)
        or preflight["maximum_run_seconds"] != 120 or preflight["data_and_checkpoint_downloads"] != 0
        or preflight["pretrained_model_or_api_calls"] != 0
        or preflight["full_experiments_executed"] is not False or preflight["automatic_retry"] is not False
    ):
        raise ValueError("expected fixed CPU-only, no-download preflight")
    paths = [
        "scripts/run_nov07_components.py", "scripts/oct18_frozen_sources.py",
        "scripts/curate_nov04_components.py", "scripts/run_nov04_components.py",
        preflight_path.relative_to(ROOT).as_posix(),
        *(module_path(module) for _, _, module in COMPONENTS.values()),
        *(f"src/auto_research/paper_specs/catalog/{domain}/{key}.json"
          for key, (domain, _, _) in COMPONENTS.items()),
    ]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}
    proof = capture_sources(ROOT, commit, paths)
    verify_sources(ROOT, commit, hashes, proof)
    frozen = {"schema_version": 1, "commit": commit, "source_sha256": hashes, "proof": proof}
    specs = {key: spec_for(key) for key in COMPONENTS}
    results = []
    for key in COMPONENTS:
        spec = specs[key]
        if (spec["implementation_status"] != "component_only"
                or spec["full_experiment_status"] != "not_reproduced_high_cost"
                or not spec["full_experiment_review_done"] or spec["requires_gpu_validation"]
                or spec["gpu_validation_passed"] or spec.get("gpu_validation_artifact")):
            raise ValueError(f"{key}: not a bounded CPU component")
    frozen_path = AUDIT / "frozen-sources.json"
    if frozen_path.exists() or any((ROOT / metric_path(spec)).exists() for spec in specs.values()):
        raise ValueError("refusing to overwrite accepted evidence")
    started = time.monotonic()
    for key, (domain, _, module_name) in COMPONENTS.items():
        module = importlib.import_module("auto_research." + module_name)
        if module.REQUIRES_GPU_VALIDATION is not False:
            raise ValueError(f"{key}: diagnostic must not advertise CUDA")
        rows = []
        for seed in SEEDS:
            if time.monotonic() - started >= preflight["maximum_run_seconds"]:
                raise TimeoutError("diagnostic preflight limit exceeded")
            rows.append(module.diagnostic(seed, device="cpu") | {
                "execution_device": "cpu", "execution_accelerator": "CPU",
            })
        dataset = {
            "id": f"synthetic:nov07-{key}-v1",
            "revision": "sha256:" + hashes[module_path(module_name)],
            "recipe": "small seeded arithmetic fixtures; not an upstream capability benchmark",
            "capability_benchmark": False,
        }
        artifact = metric_path(specs[key])
        value = {
            "schema_version": 2, "method": key, "manifest_ref": f"{domain}:{key}",
            "dataset": dataset, "seed": SEEDS, "seeds": SEEDS, "per_seed": rows,
            "metrics": aggregate_metrics(rows), "diagnostic_only": True, "fixture_demo": True,
            "evaluation_tier": "l1_mechanism", "evaluation_protocol": evaluation_protocol(),
            "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "provenance": {
                "commit": commit, "artifact_path": artifact.as_posix(), "accelerator": "CPU",
                "executed_source_sha256": hashes, "dataset_fingerprint": generated_input_fingerprint(dataset, hashes),
            },
        }
        validate_metric(key, value, frozen)
        results.append((ROOT / artifact, value))
    elapsed = time.monotonic() - started
    if elapsed > preflight["maximum_run_seconds"]:
        raise TimeoutError("diagnostic preflight limit exceeded")
    frozen["execution"] = {
        "device": "cpu", "seeds": SEEDS, "elapsed_seconds": elapsed,
        "command": ["python", "scripts/run_nov07_components.py"],
        "pretrained_model_or_api_calls": 0, "full_experiments_executed": False,
    }
    for path, value in results:
        write_new(path, value)
    write_new(frozen_path, frozen)
    print(json.dumps({"component_keys": list(COMPONENTS), "elapsed_seconds": elapsed, "device": "cpu"}))


if __name__ == "__main__":
    main()
