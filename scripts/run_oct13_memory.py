#!/usr/bin/env python3
"""Run actual NEAR/Beyond public retrieval with local pinned MiniLM resources."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main():
    from auto_research.reproductions.near.experiment import run_near
    from auto_research.reproductions.beyond_final_embedding.experiment import run_beyond
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", choices=("near", "beyond-final-embedding"), required=True)
    parser.add_argument("--raw-data", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-queries", type=int, default=30)
    parser.add_argument("--max-length", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--adapter-epochs", type=int, default=2)
    parser.add_argument("--split-policy", choices=("bank-disjoint", "query-disjoint-shared-bank"),
                        default="bank-disjoint")
    parser.add_argument("--diagnostic-only", action="store_true",
                        help="explicitly forbid capability promotion, including bounded strict-bank diagnostics")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("immutable output already exists")
    config = {"raw_data": str(args.raw_data), "model_dir": str(args.model_dir),
              "device": args.device, "max_queries": args.max_queries,
              "max_length": args.max_length, "batch_size": args.batch_size,
              "adapter_epochs": args.adapter_epochs, "split_policy": args.split_policy,
              "diagnostic_only": args.diagnostic_only}
    result = (run_near if args.paper == "near" else run_beyond)(config, args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"paper": result["paper"], "seed": args.seed,
                      "test": result["test"], "baseline": result["baseline"]}))


if __name__ == "__main__":
    main()
