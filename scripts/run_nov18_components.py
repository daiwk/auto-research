"""Run the fixed November refresh components under one 180-second device budget.

These are source-bound interface/mechanism diagnostics, not model benchmarks.
No checkpoint, media, API call or training campaign is downloaded or launched.
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
AUDIT = ROOT / "docs/research-audits/nov18-components"
BATCH = "2026-11-18-affordable-components"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "typed-inbox-protocol": ("system-one", "foundation_models/typed_inbox_protocol.py"),
    "askalcf-protocol": ("agent-research", "agent_research/askalcf_protocol.py"),
    "prodpilot-protocol": ("agent-research", "agent_research/prodpilot_protocol.py"),
    "fend-protocol": ("multimodal-models", "multimodal/fend_protocol.py"),
    "stratified-retention-protocol": ("foundation-models", "foundation_models/stratified_retention_protocol.py"),
    "tokenization-premium": ("foundation-models", "foundation_models/tokenization_premium.py"),
    "rslivebench-uav-protocol": ("multimodal-models", "multimodal/rslivebench_uav_protocol.py"),
    "multimodal-library-protocol": ("multimodal-models", "multimodal/library_retrieval_protocol.py"),
    "luce-similarity-audit": ("post-training", "post_training/luce_similarity_audit.py"),
    "runway-inference-protocol": ("foundation-models", "foundation_models/runway_inference_protocol.py"),
    "smart-model-routing": ("foundation-models", "foundation_models/smart_model_routing.py"),
    "calibrated-judges-protocol": ("post-training", "post_training/calibrated_judges_protocol.py"),
    "hvmap": ("foundation-models", "foundation_models/hvmap.py"),
    "mixed-signals-weights": ("foundation-models", "foundation_models/mixed_signals_weights.py"),
}
CUDA_KEYS = {"hvmap", "mixed-signals-weights"}
INTERFACE_KEYS = {"typed-inbox-protocol", "fend-protocol", "stratified-retention-protocol", "rslivebench-uav-protocol", "multimodal-library-protocol", "mixed-signals-weights"}
EXECUTION_FILES = ["scripts/run_nov18_components.py", "scripts/oct18_frozen_sources.py",
                   "docs/research-audits/nov18-components/preflight.json",
                   *("src/auto_research/" + module for _, module in COMPONENTS.values())]


def load(path):
    return json.loads(Path(path).read_text())


def write_new(path, payload):
    path = Path(path)
    if path.exists():
        raise ValueError("refusing to overwrite execution evidence: " + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def tier(key):
    return "l0_interface" if key in INTERFACE_KEYS else "l1_mechanism"


def preflight():
    return json.loads('''{
  "schema_version": 1,
  "batch": "2026-11-18-affordable-components",
  "component_keys": ["typed-inbox-protocol", "askalcf-protocol", "prodpilot-protocol", "fend-protocol", "stratified-retention-protocol", "tokenization-premium", "rslivebench-uav-protocol", "multimodal-library-protocol", "luce-similarity-audit", "runway-inference-protocol", "smart-model-routing", "calibrated-judges-protocol", "hvmap", "mixed-signals-weights"],
  "cuda_keys": ["hvmap", "mixed-signals-weights"],
  "seeds": [42, 43, 44],
  "maximum_run_seconds": 180,
  "maximum_cuda_devices": 1,
  "model_and_dataset_downloads": 0,
  "pretrained_model_calls": 0,
  "api_calls": 0,
  "full_experiments_executed": false,
  "automatic_retry": false,
  "input_scope": "Finite explicit protocol examples and seeded small tensors only; no capability benchmark, model editor, production mailbox, cloud deployment or provider calls.",
  "scope_note": "Fourteen accepted low-cost opportunities from the closed Nov15 review. Each source determines its L0/L1 boundary. Stratified Retention is a proposed evaluation framework, not an empirical campaign. Other costly full campaigns are not reproduced and do not block review closure. No new source-coverage watermark claim."
}''')


def source_hashes():
    return {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in EXECUTION_FILES}


def validate_diagnostic(row, seed, key):
    if (not isinstance(row, dict) or row.get("seed") != seed or row.get("diagnostic_only") is not True
            or row.get("evaluation_tier") != tier(key)):
        raise ValueError(key + ": wrong diagnostic identity or tier")
    checks = row.get("checks")
    if not isinstance(checks, dict) or not checks or any(value is not True for value in checks.values()):
        raise ValueError(key + ": diagnostic checks failed")
    metrics = row.get("metrics")
    if not isinstance(metrics, dict) or not metrics or any(
            isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value)
            for value in metrics.values()):
        raise ValueError(key + ": finite numeric diagnostic metrics required")


def validate_raw(raw, frozen):
    device = raw.get("device")
    expected = CUDA_KEYS if device == "cuda" else set(COMPONENTS)
    if (device not in {"cpu", "cuda"} or raw.get("batch") != BATCH
            or raw.get("source_sha256") != frozen["source_sha256"]
            or raw.get("code_commit") != frozen["commit"] or raw.get("seeds") != SEEDS
            or set(raw.get("components", {})) != expected
            or raw.get("full_experiments_executed") is not False
            or raw.get("promotion_eligible") is not False or raw.get("formal_comparison") is not False
            or not 0 <= raw.get("elapsed_seconds", math.inf) <= preflight()["maximum_run_seconds"]):
        raise ValueError("raw run does not match frozen short-budget scope")
    if device == "cuda" and not raw.get("accelerator", "").startswith(("NVIDIA A100", "NVIDIA A30")):
        raise ValueError("actual A100/A30 required")
    for key, value in raw["components"].items():
        rows = value.get("per_seed", [])
        if len(rows) != len(SEEDS):
            raise ValueError("exact three seed rows required")
        for seed, row in zip(SEEDS, rows, strict=True):
            validate_diagnostic(row, seed, key)
            if row.get("execution_device") != device or row.get("execution_accelerator") != raw["accelerator"]:
                raise ValueError("device provenance mismatch")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    parser.add_argument("--freeze", action="store_true")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--source-commit")
    parser.add_argument("--frozen-proof", type=Path, default=AUDIT / "frozen-sources.json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.prepare:
        write_new(AUDIT / "preflight.json", preflight())
        return
    if load(AUDIT / "preflight.json") != preflight():
        raise ValueError("preflight differs from the accepted fixed short-budget scope")
    if args.freeze:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        hashes = source_hashes()
        proof = capture_sources(ROOT, commit, EXECUTION_FILES)
        verify_sources(ROOT, commit, hashes, proof)
        write_new(args.frozen_proof, {"schema_version": 1, "commit": commit,
                                    "source_sha256": hashes, "proof": proof})
        print(json.dumps({"frozen_commit": commit, "execution_files": len(hashes)}))
        return
    if args.output is None or args.source_commit is None:
        parser.error("--output and --source-commit required for actual execution")
    frozen = load(args.frozen_proof)
    if frozen["commit"] != args.source_commit or frozen["source_sha256"] != source_hashes():
        raise ValueError("execution sources differ from frozen commit")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    import torch
    torch.set_num_threads(2)
    accelerator = "CPU"
    if args.device == "cuda":
        if not torch.cuda.is_available():
            raise ValueError("actual CUDA unavailable")
        accelerator = torch.cuda.get_device_name(0)
        if not accelerator.startswith(("NVIDIA A100", "NVIDIA A30")) or torch.cuda.device_count() != 1:
            raise ValueError("fixed budget requires one visible real A100/A30")
        torch.cuda.synchronize()
    started, results = time.monotonic(), {}
    for key, (_, module_path) in COMPONENTS.items():
        if args.device == "cuda" and key not in CUDA_KEYS:
            continue
        module = importlib.import_module("auto_research." + module_path[:-3].replace("/", "."))
        if (Path(module.__file__).resolve() != ROOT / "src/auto_research" / module_path
                or module.REQUIRES_GPU_VALIDATION is not (key in CUDA_KEYS)):
            raise ValueError(key + ": wrong imported source or GPU contract")
        rows = []
        for seed in SEEDS:
            row = module.diagnostic(seed, device=args.device)
            validate_diagnostic(row, seed, key)
            rows.append(row | {"execution_device": args.device, "execution_accelerator": accelerator})
            if time.monotonic() - started > preflight()["maximum_run_seconds"]:
                raise TimeoutError("short-budget diagnostics exceeded preflight; no automatic retry")
        results[key] = {"per_seed": rows, "evaluation_tier": tier(key)}
    if args.device == "cuda":
        torch.cuda.synchronize()
    raw = {"schema_version": 2, "batch": BATCH, "device": args.device, "accelerator": accelerator,
           "seeds": SEEDS, "code_commit": frozen["commit"], "source_sha256": frozen["source_sha256"],
           "components": results, "elapsed_seconds": time.monotonic() - started,
           "diagnostic_only": True, "evaluation_tier": "mixed_l0_interface_l1_mechanism",
           "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
           "pretrained_model_calls": 0, "full_experiments_executed": False, "automatic_retry": False}
    validate_raw(raw, frozen)
    write_new(args.output, raw)
    print(json.dumps({"components": len(results), "device": args.device, "accelerator": accelerator,
                      "elapsed_seconds": raw["elapsed_seconds"]}))


if __name__ == "__main__":
    main()
