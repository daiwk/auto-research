"""Freeze and run only the late-discovered EgoJev CPU postprocessing component.

The previously executed17-component CPU/7-component A100 group stays immutable.
This separate source proof avoids rewriting those measurements when a read-only
cross-topic review discovers one additional affordable CPU operator.
"""

from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import time
from oct18_frozen_sources import capture_sources, verify_sources

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov19-latest"
MODULE = "src/auto_research/system_one/egojev_components.py"
SEEDS = [42, 43, 44]
PATHS = [
    "scripts/run_nov19_egojev_cpu.py",
    "scripts/oct18_frozen_sources.py",
    MODULE,
    "src/auto_research/__init__.py",
    "src/auto_research/system_one/__init__.py",
]


def load(path):
    return json.loads(path.read_text())


def hashes():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in PATHS}


def write_new(path, value):
    if path.exists():
        raise ValueError("actual evidence is immutable: " + str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def validate_raw(raw, frozen):
    if (
        raw.get("batch") != "2026-11-19-egojev-cpu-supplement"
        or raw.get("device") != "cpu"
        or raw.get("accelerator") != "CPU"
        or raw.get("seeds") != SEEDS
        or raw.get("source_sha256") != frozen["source_sha256"]
        or raw.get("code_commit") != frozen["commit"]
        or raw.get("diagnostic_only") is not True
        or raw.get("promotion_eligible") is not False
        or raw.get("full_experiments_executed") is not False
        or raw.get("pretrained_model_calls") != 0
        or raw.get("api_calls") != 0
        or raw.get("automatic_retry") is not False
        or not 0 <= raw.get("elapsed_seconds", math.inf) <= 30
        or set(raw.get("components", {})) != {"egojev"}
    ):
        raise ValueError("wrong supplemental scope or source provenance")
    entry = raw["components"]["egojev"]
    if entry.get("evaluation_tier") != "l1_mechanism" or len(entry.get("per_seed", [])) != 3:
        raise ValueError("wrong supplemental tier/seeds")
    for seed, row in zip(SEEDS, entry["per_seed"], strict=True):
        if (
            row.get("seed") != seed
            or row.get("evaluation_tier") != "l1_mechanism"
            or row.get("diagnostic_only") is not True
            or row.get("execution_device") != "cpu"
            or not row.get("checks")
            or any(v is not True for v in row["checks"].values())
            or not row.get("metrics")
            or any(
                isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
                for v in row["metrics"].values()
            )
        ):
            raise ValueError("supplemental diagnostic failed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    proof_path = AUDIT / "frozen-egojev-sources.json"
    if args.freeze:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        source_hashes = hashes()
        proof = capture_sources(ROOT, commit, PATHS)
        verify_sources(ROOT, commit, source_hashes, proof)
        write_new(
            proof_path,
            {"schema_version": 1, "commit": commit, "source_sha256": source_hashes, "proof": proof},
        )
        print(json.dumps({"supplement_commit": commit, "execution_files": len(PATHS)}))
        return
    frozen = load(proof_path)
    if hashes() != frozen["source_sha256"]:
        raise ValueError("supplemental source changed after freeze")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    module_spec = importlib.util.spec_from_file_location("egojev_frozen_cpu", ROOT / MODULE)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    if (
        Path(module.__file__).resolve() != ROOT / MODULE
        or module.REQUIRES_GPU_VALIDATION is not False
    ):
        raise ValueError("wrong supplemental import/device contract")
    started = time.monotonic()
    rows = [
        module.diagnostic(seed, device="cpu")
        | {"execution_device": "cpu", "execution_accelerator": "CPU"}
        for seed in SEEDS
    ]
    raw = {
        "schema_version": 2,
        "batch": "2026-11-19-egojev-cpu-supplement",
        "device": "cpu",
        "accelerator": "CPU",
        "seeds": SEEDS,
        "components": {"egojev": {"evaluation_tier": "l1_mechanism", "per_seed": rows}},
        "source_sha256": frozen["source_sha256"],
        "code_commit": frozen["commit"],
        "elapsed_seconds": time.monotonic() - started,
        "diagnostic_only": True,
        "formal_comparison": False,
        "promotion_eligible": False,
        "evolve_integrated": False,
        "full_experiments_executed": False,
        "pretrained_model_calls": 0,
        "api_calls": 0,
        "automatic_retry": False,
    }
    validate_raw(raw, frozen)
    write_new(AUDIT / "raw-egojev-cpu.json", raw)
    print(
        json.dumps(
            {"component": "egojev", "elapsed_seconds": raw["elapsed_seconds"], "model_calls": 0}
        )
    )


if __name__ == "__main__":
    main()
