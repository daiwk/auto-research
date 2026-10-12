#!/usr/bin/env python3
"""Run an actual public-data Oct-12 foundation diagnostic; never forge receipts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.reproductions.oct12_foundation_multimodal import (
    render, run_dualquant, run_foundation_training,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", required=True, choices=["msar", "orthros", "dualquant"])
    parser.add_argument("--dataset-dir", type=Path, default=Path("data/oct12-wikitext"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--checkpoint-path", type=Path, default=None,
                        help="hash-verified offline public checkpoint mirror with provenance.json")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=40)
    parser.add_argument("--width", type=int, default=64)
    parser.add_argument("--layers", type=int, default=2)
    parser.add_argument("--sequence-length", type=int, default=64)
    parser.add_argument("--window", type=int, default=16)
    parser.add_argument("--train-bytes", type=int, default=32768)
    parser.add_argument("--eval-bytes", type=int, default=4096)
    parser.add_argument("--iterations", type=int, default=15)
    parser.add_argument("--max-linear-layers", type=int, default=4,
                        help="0 quantizes every eligible decoder linear; default is a bounded partial diagnostic")
    parser.add_argument("--scale-format", choices=["bf16", "e8m0"], default="bf16")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("use a fresh output directory; prior evidence is immutable")
    if args.paper == "dualquant":
        result = run_dualquant(args.dataset_dir, args.seed, device=args.device,
                              iterations=args.iterations, max_linear_layers=args.max_linear_layers,
                              scale_format=args.scale_format, eval_bytes=args.eval_bytes,
                              checkpoint_path=args.checkpoint_path)
    else:
        result = run_foundation_training(args.paper, args.dataset_dir, args.seed, device=args.device,
                                         steps=args.steps, width=args.width, layers=args.layers,
                                         sequence_length=args.sequence_length, window=args.window,
                                         train_bytes=args.train_bytes, eval_bytes=args.eval_bytes)
    args.output.mkdir(parents=True)
    (args.output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (args.output / "report.md").write_text(render(result))
    print(json.dumps({"paper": args.paper, "baseline": result["baseline"],
                      "method": result["method"], "diagnostic_only": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
