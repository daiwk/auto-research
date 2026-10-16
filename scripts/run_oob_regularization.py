#!/usr/bin/env python3
"""Bounded paired OOB/SimCLR training on already cached official CIFAR TRAIN."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch

from auto_research.reproductions.oob_regularization.experiment import run_comparison
from auto_research.runtime import exclusive_file_lock


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--training-examples", type=int, default=512)
    parser.add_argument("--validation-examples", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--refresh-interval", type=int, default=10)
    parser.add_argument("--maximum-seconds", type=float, default=120)
    parser.add_argument("--threads", type=int, default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        parser.error("choose a new immutable output path")
    if not 1 <= args.threads <= 4:
        parser.error("bounded run supports 1..4 CPU threads")
    torch.set_num_threads(args.threads)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with exclusive_file_lock(args.output):
        if args.output.exists():
            raise FileExistsError("output already exists")
        try:
            result = run_comparison(
                args.dataset_dir, seed=args.seed, device=args.device, steps=args.steps,
                training_examples=args.training_examples, validation_examples=args.validation_examples,
                batch_size=args.batch_size, refresh_interval=args.refresh_interval,
                maximum_seconds=args.maximum_seconds,
            )
        except Exception as error:
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump({"status": "failed", "seed": args.seed, "error_type": type(error).__name__,
                           "error": str(error), "diagnostic_only": True,
                           "promotion_eligible": False}, handle, ensure_ascii=False, indent=2)
            raise
        with args.output.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
            handle.write("\n")
    print(json.dumps({"output": str(args.output), "elapsed_seconds": result["elapsed_seconds"],
                      "paired_validation_differences": result["paired_validation_differences"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
