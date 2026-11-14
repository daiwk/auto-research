"""Run frozen Nov 9 CPU mechanism checks and write standalone evidence."""
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
AUDIT = ROOT / "docs/research-audits/nov09-atom-increment"
BATCH = "2026-11-09-atom-increment"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "verified-quantum-wiki": ("agent-research", "2611.09822", "agent_research.verified_quantum_wiki"),
    "e-means": ("foundation-models", "2611.09501", "foundation_models.e_means"),
    "engram-consolidation": ("agent-research", "2611.09472", "agent_research.engram_consolidation"),
    "rcea": ("post-training", "2611.09448", "post_training.rcea"),
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def spec_path(key: str) -> str:
    return f"src/auto_research/paper_specs/catalog/{COMPONENTS[key][0]}/{key}.json"


def module_path(key: str) -> str:
    return "src/auto_research/" + COMPONENTS[key][2].replace(".", "/") + ".py"


def artifact_path(spec: dict) -> Path:
    return Path("docs") / Path(spec["detail_path"]).parent / "metrics/component-cpu-seeds42-44.json"


def validate_metric(key: str, value: dict, frozen: dict) -> None:
    rows, provenance, dataset = value["per_seed"], value["provenance"], value["dataset"]
    hashes = frozen["source_sha256"]
    if (
        value["method"] != key or value["manifest_ref"] != f"{COMPONENTS[key][0]}:{key}"
        or value["seeds"] != SEEDS or [row["seed"] for row in rows] != SEEDS
        or value["metrics"] != aggregate_metrics(rows)
        or value["evaluation_tier"] != "l1_mechanism" or value["diagnostic_only"] is not True
        or value["full_experiment_status"] != "not_reproduced_high_cost"
        or value["full_experiment_review_done"] is not True
        or any(value[flag] is not False for flag in (
            "formal_comparison", "promotion_eligible", "evolve_integrated", "automatic_retry",
        ))
        or provenance["accelerator"] != "CPU" or provenance["commit"] != frozen["commit"]
        or provenance["executed_source_sha256"] != hashes
        or dataset["revision"] != "sha256:" + hashes[module_path(key)]
        or dataset["capability_benchmark"] is not False
        or provenance["dataset_fingerprint"] != generated_input_fingerprint(dataset, hashes)
    ):
        raise ValueError(f"{key}: inconsistent bounded CPU evidence")
    for seed, row in zip(SEEDS, rows, strict=True):
        validate_diagnostic(row, seed)
        if (row["execution_device"], row["execution_accelerator"]) != ("cpu", "CPU"):
            raise ValueError(f"{key}: unexpected device")


def main() -> None:
    preflight_path = AUDIT / "preflight.json"
    if load(preflight_path) != {
        "batch": BATCH, "component_keys": list(COMPONENTS), "seeds": SEEDS, "device": "cpu",
        "maximum_run_seconds": 120, "data_and_checkpoint_downloads": 0,
        "pretrained_model_or_api_calls": 0, "full_experiments_executed": False, "automatic_retry": False,
    }:
        raise ValueError("expected the fixed CPU-only preflight")
    paths = [
        "scripts/run_nov09_components.py", "scripts/oct18_frozen_sources.py",
        "scripts/curate_nov04_components.py", "scripts/run_nov04_components.py",
        preflight_path.relative_to(ROOT).as_posix(),
        *(module_path(key) for key in COMPONENTS), *(spec_path(key) for key in COMPONENTS),
    ]
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    hashes = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}
    proof = capture_sources(ROOT, commit, paths)
    verify_sources(ROOT, commit, hashes, proof)
    frozen = {"schema_version": 1, "commit": commit, "source_sha256": hashes, "proof": proof}
    specs = {key: load(ROOT / spec_path(key)) for key in COMPONENTS}
    frozen_path = AUDIT / "frozen-sources.json"
    if frozen_path.exists() or any((ROOT / artifact_path(spec)).exists() for spec in specs.values()):
        raise ValueError("refusing to overwrite accepted evidence")
    started = time.monotonic()
    results = []
    for key, spec in specs.items():
        if (spec["implementation_status"] != "component_only"
                or spec["full_experiment_status"] != "not_reproduced_high_cost"
                or spec["full_experiment_review_done"] is not True
                or spec["requires_gpu_validation"] is not False or spec["gpu_validation_passed"] is not False):
            raise ValueError(f"{key}: not a CPU-only closed component")
        module = importlib.import_module("auto_research." + COMPONENTS[key][2])
        if Path(module.__file__).resolve() != ROOT / module_path(key) or module.REQUIRES_GPU_VALIDATION is not False:
            raise ValueError(f"{key}: module must use the frozen CPU source")
        rows = [
            module.diagnostic(seed, device="cpu") | {
                "execution_device": "cpu", "execution_accelerator": "CPU",
                "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            }
            for seed in SEEDS
        ]
        dataset = {
            "id": f"synthetic:nov09-{key}-v1", "revision": "sha256:" + hashes[module_path(key)],
            "recipe": "Seeded numerical or control-rule fixtures; not an upstream capability benchmark",
            "capability_benchmark": False,
        }
        artifact = artifact_path(spec)
        value = {
            "schema_version": 2, "method": key, "manifest_ref": f"{spec['domain']}:{key}",
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
    if elapsed > 120:
        raise TimeoutError("CPU preflight time limit exceeded")
    frozen["execution"] = {
        "device": "cpu", "seeds": SEEDS, "elapsed_seconds": elapsed,
        "command": ["python", "scripts/run_nov09_components.py"], "pretrained_model_or_api_calls": 0,
        "full_experiments_executed": False,
    }
    for path, value in results:
        write_new(path, value)
    write_new(frozen_path, frozen)
    print(json.dumps({"components": list(COMPONENTS), "elapsed_seconds": elapsed, "device": "cpu"}))


if __name__ == "__main__":
    main()
