"""Execute eight fixed low-cost components; no model, API, or dataset campaign."""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import time

from oct18_frozen_sources import capture_sources, verify_sources
from run_nov04_components import validate_diagnostic

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov12-components"
BATCH = "2026-11-12-overlap-components"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "agent-gym": ("agent-research", "agent_research/agent_gym.py"),
    "bats": ("agent-research", "agent_research/bats.py"),
    "bopd": ("post-training", "post_training/bopd.py"),
    "apmd-reference-reset": ("post-training", "post_training/apmd_reference_reset.py"),
    "lcs-reference-opd": ("post-training", "post_training/lcs_reference_opd.py"),
    "real-loss": ("foundation-models", "foundation_models/real_loss.py"),
    "c2-routing": ("multimodal-models", "multimodal/c2_routing.py"),
    "onlyact": ("multimodal-models", "multimodal/onlyact.py"),
}
CUDA_KEYS = {"bopd", "real-loss", "onlyact"}
EXECUTION_FILES = [
    "scripts/run_nov12_components.py", "scripts/run_nov04_components.py",
    "scripts/oct18_frozen_sources.py", "docs/research-audits/nov12-components/preflight.json",
    *("src/auto_research/" + module for _, module in COMPONENTS.values()),
]


def read(path):
    return json.loads(Path(path).read_text())


def write_new(path, payload):
    path = Path(path)
    if path.exists():
        raise ValueError(f"refusing to overwrite execution evidence: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def source_hashes():
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in EXECUTION_FILES}


def preflight():
    return {
        "schema_version": 1, "batch": BATCH, "component_keys": list(COMPONENTS),
        "cuda_keys": sorted(CUDA_KEYS), "seeds": SEEDS, "maximum_run_seconds": 180,
        "model_and_dataset_downloads": 0, "pretrained_model_calls": 0, "api_calls": 0,
        "full_experiments_executed": False, "automatic_retry": False,
        "input_scope": "small seeded tensors, exact finite-policy operators, and explicit control/evaluator contracts; no capability benchmark",
        "theory_only_paper": "apmd-reference-reset",
        "theory_note": "Theoretical operators are checked numerically; no nonexistent large empirical protocol is labeled high-cost or reproduced.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path, default=AUDIT / "frozen-sources.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if read(AUDIT / "preflight.json") != preflight():
        raise ValueError("fixed short-budget scope differs")
    if args.freeze:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        hashes = source_hashes()
        proof = capture_sources(ROOT, commit, EXECUTION_FILES)
        verify_sources(ROOT, commit, hashes, proof)
        write_new(AUDIT / "frozen-sources.json", {
            "schema_version": 1, "commit": commit, "source_sha256": hashes, "proof": proof})
        print(json.dumps({"frozen_commit": commit, "files": len(hashes)}))
        return
    if args.output is None or args.source_commit is None:
        parser.error("--output and --source-commit required for actual execution")
    frozen = read(args.frozen_proof)
    if frozen["commit"] != args.source_commit or frozen["source_sha256"] != source_hashes():
        raise ValueError("execution sources differ from the frozen commit")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    import torch
    torch.set_num_threads(2)
    if args.device == "cuda":
        if not torch.cuda.is_available():
            raise ValueError("actual CUDA unavailable")
        accelerator = torch.cuda.get_device_name(0)
        if not accelerator.startswith(("NVIDIA A100", "NVIDIA A30")):
            raise ValueError("this scope requires a single real A100 or A30")
        torch.cuda.synchronize()
    else:
        accelerator = "CPU"
    started = time.monotonic()
    results = {}
    for key, (_, module_path) in COMPONENTS.items():
        if args.device == "cuda" and key not in CUDA_KEYS:
            continue
        module = importlib.import_module("auto_research." + module_path[:-3].replace("/", "."))
        if (Path(module.__file__).resolve() != ROOT / "src/auto_research" / module_path
                or module.REQUIRES_GPU_VALIDATION is not (key in CUDA_KEYS)):
            raise ValueError(f"{key}: not the frozen device contract")
        rows = []
        for seed in SEEDS:
            row = module.diagnostic(seed, device=args.device)
            validate_diagnostic(row, seed)
            rows.append(row | {"execution_device": args.device, "execution_accelerator": accelerator,
                               "diagnostic_only": True, "evaluation_tier": "l1_mechanism"})
            if time.monotonic() - started > preflight()["maximum_run_seconds"]:
                raise TimeoutError("short-budget component run exceeded preflight")
        results[key] = {"per_seed": rows}
    if args.device == "cuda":
        torch.cuda.synchronize()
    raw = {
        "schema_version": 2, "batch": BATCH, "device": args.device, "accelerator": accelerator,
        "seeds": SEEDS, "code_commit": frozen["commit"], "source_sha256": frozen["source_sha256"],
        "components": results, "elapsed_seconds": time.monotonic() - started,
        "diagnostic_only": True, "evaluation_tier": "l1_mechanism", "formal_comparison": False,
        "promotion_eligible": False, "evolve_integrated": False, "pretrained_model_calls": 0,
        "full_experiments_executed": False, "automatic_retry": False,
    }
    write_new(args.output, raw)
    print(json.dumps({"components": list(results), "device": args.device,
                      "accelerator": accelerator, "elapsed_seconds": raw["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
