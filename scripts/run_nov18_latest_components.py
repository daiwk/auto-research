"""Frozen-source, three-seed diagnostics for the finite November16–18 intake.

No pretrained checkpoint, public dataset or provider is downloaded/called. One
visible A100/A30 and a180-second device budget bound actual CUDA execution.
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
AUDIT = ROOT / "docs/research-audits/nov18-latest"
BATCH = "2026-11-18-latest-components"
SEEDS = [42, 43, 44]


def load(path):
    return json.loads(Path(path).read_text())


def config():
    value = load(AUDIT / "preflight.json")
    if (
        value["batch"] != BATCH
        or value["seeds"] != SEEDS
        or value["maximum_run_seconds"] != 180
        or value["maximum_cuda_devices"] != 1
        or value["model_and_dataset_downloads"] != 0
        or value["api_calls"] != 0
        or value["automatic_retry"] is not False
    ):
        raise ValueError("wrong accepted device/cost scope")
    for key, row in value["components"].items():
        if (
            row["evaluation_tier"] not in {"l0_interface", "l1_mechanism"}
            or type(row["cuda"]) is not bool
            or not (ROOT / "src/auto_research" / row["module"]).is_file()
        ):
            raise ValueError("invalid fixed component scope: " + key)
    return value


def execution_files():
    return [
        "scripts/run_nov18_latest_components.py",
        "scripts/oct18_frozen_sources.py",
        "docs/research-audits/nov18-latest/preflight.json",
        "src/auto_research/post_training/_nov18_contracts.py",
        *(
            "src/auto_research/" + p
            for p in (
                "__init__.py",
                "foundation_models/__init__.py",
                "post_training/__init__.py",
                "agent_research/__init__.py",
                "reproductions/__init__.py",
            )
        ),
        *("src/auto_research/" + row["module"] for row in config()["components"].values()),
    ]


def source_hashes():
    return {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in execution_files()}


def write_new(path, value):
    path = Path(path)
    if path.exists():
        raise ValueError("refusing to overwrite actual execution evidence: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def validate_diagnostic(row, seed, key):
    if (
        not isinstance(row, dict)
        or row.get("seed") != seed
        or row.get("diagnostic_only") is not True
        or row.get("evaluation_tier") != config()["components"][key]["evaluation_tier"]
    ):
        raise ValueError("wrong diagnostic identity/tier: " + key)
    checks, metrics = row.get("checks"), row.get("metrics")
    if (
        not isinstance(checks, dict)
        or not checks
        or any(value is not True for value in checks.values())
    ):
        raise ValueError("diagnostic checks failed: " + key)
    if (
        not isinstance(metrics, dict)
        or not metrics
        or any(
            isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
            for v in metrics.values()
        )
    ):
        raise ValueError("finite scalar metrics required: " + key)


def validate_raw(raw, frozen):
    cfg = config()
    device = raw.get("device")
    expected = {key for key, row in cfg["components"].items() if device == "cpu" or row["cuda"]}
    required = {
        "schema_version": 2,
        "batch": BATCH,
        "seeds": SEEDS,
        "diagnostic_only": True,
        "formal_comparison": False,
        "promotion_eligible": False,
        "evolve_integrated": False,
        "full_experiments_executed": False,
        "pretrained_model_calls": 0,
        "api_calls": 0,
        "automatic_retry": False,
    }
    if (
        device not in {"cpu", "cuda"}
        or any(type(raw.get(k)) is not type(v) or raw.get(k) != v for k, v in required.items())
        or raw.get("source_sha256") != frozen["source_sha256"]
        or raw.get("code_commit") != frozen["commit"]
        or set(raw.get("components", {})) != expected
        or not 0 <= raw.get("elapsed_seconds", math.inf) <= cfg["maximum_run_seconds"]
    ):
        raise ValueError("raw execution differs from frozen bounded scope")
    if device == "cuda" and not raw.get("accelerator", "").startswith(
        ("NVIDIA A100", "NVIDIA A30")
    ):
        raise ValueError("real A100/A30 required")
    for key, entry in raw["components"].items():
        rows = entry.get("per_seed", [])
        if (
            len(rows) != 3
            or entry.get("evaluation_tier") != cfg["components"][key]["evaluation_tier"]
        ):
            raise ValueError("wrong actual seed/tier scope")
        names = set(rows[0].get("metrics", {}))
        for seed, row in zip(SEEDS, rows, strict=True):
            validate_diagnostic(row, seed, key)
            if (
                set(row["metrics"]) != names
                or row.get("execution_device") != device
                or row.get("execution_accelerator") != raw["accelerator"]
                or ("device" in row and row["device"] != device)
            ):
                raise ValueError("inconsistent execution provenance")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path, default=AUDIT / "frozen-sources.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    cfg = config()
    if args.freeze:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        hashes = source_hashes()
        proof = capture_sources(ROOT, commit, execution_files())
        verify_sources(ROOT, commit, hashes, proof)
        write_new(
            args.frozen_proof,
            {"schema_version": 1, "commit": commit, "source_sha256": hashes, "proof": proof},
        )
        print(json.dumps({"commit": commit, "execution_files": len(hashes)}))
        return
    if args.output is None or args.source_commit is None:
        parser.error("--output and --source-commit required")
    frozen = load(args.frozen_proof)
    if frozen["commit"] != args.source_commit or frozen["source_sha256"] != source_hashes():
        raise ValueError("execution source changed since freeze")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    import torch

    torch.set_num_threads(2)
    accelerator = "CPU"
    if args.device == "cuda":
        if not torch.cuda.is_available() or torch.cuda.device_count() != 1:
            raise ValueError("exactly one visible CUDA device required")
        accelerator = torch.cuda.get_device_name(0)
        if not accelerator.startswith(("NVIDIA A100", "NVIDIA A30")):
            raise ValueError("actual A100/A30 required")
        torch.cuda.synchronize()
    started = time.monotonic()
    results = {}
    for key, item in cfg["components"].items():
        if args.device == "cuda" and not item["cuda"]:
            continue
        module = importlib.import_module("auto_research." + item["module"][:-3].replace("/", "."))
        if (
            Path(module.__file__).resolve() != ROOT / "src/auto_research" / item["module"]
            or module.REQUIRES_GPU_VALIDATION is not item["cuda"]
        ):
            raise ValueError("wrong imported source/GPU contract: " + key)
        rows = []
        for seed in SEEDS:
            row = module.diagnostic(seed, device=args.device)
            validate_diagnostic(row, seed, key)
            rows.append(
                row | {"execution_device": args.device, "execution_accelerator": accelerator}
            )
            if time.monotonic() - started > cfg["maximum_run_seconds"]:
                raise TimeoutError("preflight budget exceeded; no automatic retry")
        results[key] = {"per_seed": rows, "evaluation_tier": item["evaluation_tier"]}
    if args.device == "cuda":
        torch.cuda.synchronize()
    raw = {
        "schema_version": 2,
        "batch": BATCH,
        "seeds": SEEDS,
        "device": args.device,
        "accelerator": accelerator,
        "source_sha256": frozen["source_sha256"],
        "code_commit": frozen["commit"],
        "components": results,
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
    write_new(args.output, raw)
    print(
        json.dumps(
            {
                "components": len(results),
                "device": args.device,
                "accelerator": accelerator,
                "elapsed_seconds": raw["elapsed_seconds"],
            }
        )
    )


if __name__ == "__main__":
    main()
