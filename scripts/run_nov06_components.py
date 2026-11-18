"""Run the fixed Nov 6 L1 cohort on frozen source; never launch complete experiments."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

from oct18_frozen_sources import capture_sources, verify_sources
from run_nov04_components import validate_diagnostic

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov06-priority-components"
RUNNER = "scripts/run_nov06_components.py"
PREFLIGHT = AUDIT / "preflight.json"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "convpe": ("foundation_models/convpe.py", "cuda"),
    "cord-rollout": ("post_training/cord_rollout.py", "cpu"),
    "envopt": ("agent_research/envopt.py", "cpu"),
    "ice": ("reproductions/ice_components.py", "cuda"),
    "pipnn-ii": ("foundation_models/pipnn_ii.py", "cpu"),
    "ragcompass": ("post_training/ragcompass.py", "cpu"),
    "ured": ("reproductions/ured_components.py", "cpu"),
}
CUDA_KEYS = {key for key, (_, device) in COMPONENTS.items() if device == "cuda"}


def sources() -> list[str]:
    return [RUNNER, PREFLIGHT.relative_to(ROOT).as_posix(), "scripts/oct18_frozen_sources.py",
            "scripts/run_nov04_components.py",
            *sorted("src/auto_research/" + file for file, _ in COMPONENTS.values())]


def source_hashes() -> dict[str, str]:
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in sources()}


def preflight() -> dict:
    data = json.loads(PREFLIGHT.read_text())
    if (data["seeds"] != SEEDS or set(data["component_keys"]) != set(COMPONENTS)
            or set(data["cuda_keys"]) != CUDA_KEYS or data["maximum_run_seconds"] != 300
            or data["data_and_checkpoint_downloads"] != 0 or data["pretrained_model_or_api_calls"] != 0
            or data["full_experiments_executed"] is not False or data["automatic_retry"] is not False):
        raise ValueError("preflight must retain the fixed cheap experiment scope")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("refusing to overwrite experiment evidence")
    commit = args.source_commit or subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    hashes = source_hashes()
    if args.frozen_proof:
        frozen = json.loads(args.frozen_proof.read_text())
        if frozen["commit"] != commit or frozen["source_sha256"] != hashes:
            parser.error("frozen commit/source scope mismatch")
        proof = frozen["proof"]
    else:
        proof = capture_sources(ROOT, commit, sources())
    verify_sources(ROOT, commit, hashes, proof)
    budget = preflight()
    import torch

    torch.set_num_threads(1)
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA requested, no CPU fallback")
    accelerator = torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU"
    if args.device == "cuda" and not accelerator.startswith(("NVIDIA A100", "NVIDIA A30")):
        parser.error("real A100 or A30 required")
    started = time.monotonic()
    components = {}
    for key, (relative, required) in COMPONENTS.items():
        if args.device == "cuda" and key not in CUDA_KEYS:
            continue
        name = "_nov06_" + key.replace("-", "_")
        spec = importlib.util.spec_from_file_location(name, ROOT / "src/auto_research" / relative)
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        if module.REQUIRES_GPU_VALIDATION is not (required == "cuda"):
            raise ValueError(f"{key} device declaration differs from preflight")
        rows = []
        for seed in SEEDS:
            if time.monotonic() - started > budget["maximum_run_seconds"]:
                raise TimeoutError("component run exceeded preflight budget")
            result = module.diagnostic(seed, device=args.device)
            if args.device == "cuda":
                torch.cuda.synchronize()
            validate_diagnostic(result, seed)
            rows.append(result | {"execution_device": args.device, "execution_accelerator": accelerator})
        components[key] = {"per_seed": rows}
    elapsed = time.monotonic() - started
    if elapsed > budget["maximum_run_seconds"]:
        raise TimeoutError("component run exceeded preflight budget")
    output = {
        "schema_version": 2, "code_commit": commit, "source_sha256": hashes,
        "device": args.device, "accelerator": accelerator, "seeds": SEEDS, "components": components,
        "elapsed_seconds": elapsed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "pretrained_model_calls": 0, "full_experiments_executed": False, "formal_comparison": False,
        "promotion_eligible": False, "evolve_integrated": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(output, handle, ensure_ascii=False, allow_nan=False, indent=2)
        handle.write("\n")
    print(json.dumps({"device": args.device, "components": sorted(components), "elapsed_seconds": elapsed}))


if __name__ == "__main__":
    main()
