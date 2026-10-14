#!/usr/bin/env python3
"""Run a budget-capped WeGR public-data diagnostic; immutable output."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset-dir", type=Path, default=Path("data"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--max-users", type=int, default=64)
    parser.add_argument("--tokenizer-steps", type=int, default=24)
    parser.add_argument("--sft-steps", type=int, default=32)
    parser.add_argument("--stage-steps", type=int, default=6)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("choose a fresh output; existing evidence must not be overwritten")
    import torch
    from auto_research.reproductions.wegr.experiment import run, render
    torch.set_num_threads(4)
    result = run(args.dataset_dir, args.seed, device=args.device, max_users=args.max_users,
                 tokenizer_steps=args.tokenizer_steps, sft_steps=args.sft_steps,
                 stage_steps=args.stage_steps, batch_size=args.batch_size)
    args.output.mkdir(parents=True)
    (args.output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (args.output / "report.md").write_text(render(result))
    print(json.dumps({"method": result["method"], "elapsed_seconds": result["elapsed_seconds"],
                      "arms": {key: value["test"] for key, value in result["arms"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
