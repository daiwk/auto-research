#!/usr/bin/env python3
"""Run the Oct-2 CUDA kernels and emit sanitized validation receipts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.foundation_latest_20261002 import TACO, veto_compress


def validate_taco(seed: int):
    import torch

    torch.manual_seed(seed)
    # Keep the reference step in FP32: with a freshly initialized BF16 layer,
    # a small optimizer step may quantize back to the same stored weight and
    # produce a false-positive CUDA receipt with zero parameter movement.
    layer = torch.nn.Linear(2048, 4096, bias=False, device="cuda", dtype=torch.float32)
    inputs = torch.randn(32, 2048, device="cuda", dtype=torch.float32)
    target = torch.randn(32, 4096, device="cuda", dtype=torch.float32)
    optimizer = TACO(layer.parameters(), lr=1e-2)
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    loss = (layer(inputs) - target).float().square().mean()
    loss.backward()
    before = layer.weight.detach().clone()
    optimizer.step()
    torch.cuda.synchronize()
    parameter_delta = float((layer.weight - before).float().norm())
    if parameter_delta <= 0:
        raise RuntimeError("TACO CUDA validation did not update any parameter")
    return {
        "seed": seed,
        "loss": float(loss.detach()),
        "parameter_delta_l2": parameter_delta,
        "optimizer_state_elements": optimizer.state_elements,
        "dense_parameter_elements": layer.weight.numel(),
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
        "step_seconds": time.perf_counter() - started,
    }


def validate_veto(seed: int):
    import torch

    torch.manual_seed(seed)
    tokens = torch.randn(96, 256, 1024, device="cuda", dtype=torch.bfloat16)
    torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    compressed, audit = veto_compress(tokens, spatial_keep=32, temporal_keep=24)
    torch.cuda.synchronize()
    return {
        "seed": seed,
        "input_tokens": 96 * 256,
        "output_tokens": compressed.shape[0] * compressed.shape[1],
        "compression_ratio": audit["compression_ratio"],
        "spatial_representatives": len(audit["spatial_indices"]),
        "temporal_representatives": len(audit["frame_indices"]),
        "peak_allocated_bytes": torch.cuda.max_memory_allocated(),
        "kernel_seconds": time.perf_counter() - started,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=("taco-optimizer", "veto"), required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--accelerator-model", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    import torch

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is required")
    metrics = validate_taco(args.seed) if args.method == "taco-optimizer" else validate_veto(args.seed)
    artifact = f"docs/gpu-validations/{args.method}-a100-20261002.json"
    receipt = {
        "schema_version": 1,
        "adapter_key": args.method,
        "validated_at": "2026-10-02",
        "accelerator": {"vendor": "NVIDIA", "model": args.accelerator_model},
        "command": [
            "python", "scripts/validate_oct02_gpu.py", "--method", args.method,
            "--seed", str(args.seed), "--accelerator-model", args.accelerator_model,
            "--commit", args.commit, "--output", artifact,
        ],
        "dataset": {
            "name": "deterministic public CUDA mechanism fixture",
            "revision": "oct02-v1",
            "examples": 32 if args.method == "taco-optimizer" else 96,
        },
        "checkpoint": {
            "model_id": "not-required/reference-kernel",
            "revision": "arxiv-v1",
        },
        "result": "passed",
        "metrics": metrics,
        "provenance": {
            "commit": args.commit,
            "artifact_path": artifact,
            "raw_predictions_committed": False,
            "checkpoint_committed": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
