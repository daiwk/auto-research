"""Run the fixed historical COLM components under one 180-second device budget.

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
AUDIT = ROOT / "docs/research-audits/nov13-colm-remaining"
BATCH = "2026-11-13-colm-historical-review"
SEEDS = [42, 43, 44]
COMPONENTS = {
    "rosetta-unification": ("foundation-models", "foundation_models/rosetta_unification.py"),
    "lidas": ("foundation-models", "foundation_models/lidas.py"),
    "thinking-to-recall": ("foundation-models", "foundation_models/thinking_to_recall.py"),
    "latent-generalization": ("foundation-models", "foundation_models/latent_generalization.py"),
    "planning-optimality": ("agent-research", "agent_research/planning_optimality.py"),
    "llm-stochasticity": ("foundation-models", "foundation_models/llm_stochasticity.py"),
    "ecg-rag": ("foundation-models", "foundation_models/ecg_rag.py"),
    "continuousbench": ("foundation-models", "foundation_models/continuousbench.py"),
    "clarification-sgp": ("agent-research", "agent_research/clarification_sgp.py"),
    "social-meta-learning": ("post-training", "post_training/social_meta_learning.py"),
    "mt-pingeval": ("agent-research", "agent_research/mt_pingeval.py"),
    "maple-icl": ("post-training", "post_training/maple_icl.py"),
    "policybank": ("agent-research", "agent_research/policybank.py"),
    "co-director": ("agent-research", "agent_research/co_director.py"),
    "instruct-to-act": ("agent-research", "agent_research/instruct_to_act.py"),
    "qe-length-normalization": ("foundation-models", "foundation_models/qe_length_normalization.py"),
    "cultural-cue": ("foundation-models", "foundation_models/cultural_cue.py"),
    "decoding-constrained-beam": ("foundation-models", "foundation_models/decoding_constrained_beam.py"),
    "storyscope": ("foundation-models", "foundation_models/storyscope.py"),
    "behavioral-canaries": ("post-training", "post_training/behavioral_canaries.py"),
    "rlmf": ("post-training", "post_training/rlmf.py"),
    "avmeme-exam": ("multimodal-models", "multimodal/avmeme_exam.py"),
    "mmeb-v3": ("multimodal-models", "multimodal/mmeb_v3.py"),
}
CUDA_KEYS = {"lidas", "ecg-rag", "social-meta-learning", "instruct-to-act",
             "cultural-cue", "behavioral-canaries", "rlmf"}
INTERFACE_KEYS = {"policybank", "avmeme-exam", "mmeb-v3"}
EXECUTION_FILES = ["scripts/run_nov13_colm_components.py", "scripts/oct18_frozen_sources.py",
                   "docs/research-audits/nov13-colm-remaining/preflight.json",
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
    return {"schema_version": 1, "batch": BATCH, "component_keys": list(COMPONENTS),
            "cuda_keys": sorted(CUDA_KEYS), "seeds": SEEDS,
            "evaluation_tiers": {key: tier(key) for key in COMPONENTS},
            "maximum_run_seconds": 180, "maximum_cuda_devices": 1,
            "model_and_dataset_downloads": 0, "pretrained_model_calls": 0, "api_calls": 0,
            "full_experiments_executed": False, "automatic_retry": False,
            "input_scope": "seeded small tensors, exact finite examples and external-output evaluator protocols; no model capability comparison",
            "scope_note": "23 source-bound components from 24 reviewed identities; one empirical social-behavior application is excluded with sourceful rationale. Full-experiment dispositions are per-paper, not inferred from a diagnostic pass."}


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
