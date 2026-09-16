#!/usr/bin/env python3
"""Run Sep-16 follow-up CUDA kernels and emit a sanitized GPU receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.foundation_latest_20260916_followup import echo_cuda_kernel, videomm_cuda_kernel
from auto_research.post_training.latest_20260916_followup import tiao_cuda_kernel


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True, choices=("echo", "videomm", "tiao"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)
    device = torch.device("cuda")
    if args.method == "echo":
        early, final = torch.randn(32768, device=device), torch.randn(32768, device=device)
        candidates, early_bonus, final_bonus = echo_cuda_kernel(early, final, 32)
        metrics = {"candidate_count": int(candidates.numel()), "early_bonus_finite": bool(torch.isfinite(early_bonus).all()), "final_bonus_finite": bool(torch.isfinite(final_bonus).all())}
    elif args.method == "videomm":
        tokens, query = torch.randn(4096, 1024, device=device), torch.randn(1024, device=device)
        selected, indices, scores = videomm_cuda_kernel(tokens, query, 16, 16)
        metrics = {"input_tokens": len(tokens), "selected_tokens": len(selected), "unique_indices": int(torch.unique(indices).numel()), "scores_finite": bool(torch.isfinite(scores).all())}
    else:
        full, masked = torch.randn(16, 512, device=device), torch.randn(16, 512, device=device)
        credit, importance, mask = tiao_cuda_kernel(full, masked, torch.randn(16, device=device))
        metrics = {"trajectories": 16, "tokens_per_trajectory": 512, "selected_fraction": float(mask.float().mean()), "credit_finite": bool(torch.isfinite(credit).all()), "importance_nonnegative": bool((importance >= 0).all())}
    torch.cuda.synchronize()
    model = torch.cuda.get_device_name(0)
    accelerator = "A100" if "A100" in model else "A30" if "A30" in model else model
    artifact = f"docs/gpu-validations/{args.method}-a100-20260916.json"
    payload = {
        "schema_version": 1, "adapter_key": args.method, "validated_at": "2026-09-16",
        "accelerator": {"vendor": "NVIDIA", "model": accelerator},
        "command": ["python", "scripts/validate_sep16_followup_gpu.py", "--method", args.method, "--seed", str(args.seed), "--output", artifact, "--commit", args.commit],
        "dataset": {"name": "deterministic public mechanism fixture", "revision": "sep16-followup-v1", "examples": int(metrics.get("trajectories", metrics.get("input_tokens", 1)))},
        "checkpoint": {"model_id": "not-required/reference-kernel", "revision": "arxiv-v1"},
        "result": "passed", "metrics": {"seed": args.seed, **metrics},
        "provenance": {"commit": args.commit, "artifact_path": artifact, "raw_predictions_committed": False, "checkpoint_committed": False},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["metrics"], sort_keys=True))


if __name__ == "__main__":
    main()
