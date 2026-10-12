#!/usr/bin/env python3
"""Execute actual VLM inputs for Oct-12 transition SFT/reward diagnostics."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from auto_research.multimodal.oct12_reward_transition import run_umrm, run_woven
from auto_research.reproductions.oct12_foundation_multimodal import render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", choices=["woven", "umrm"], required=True)
    parser.add_argument("--dataset-dir", type=Path, default=Path("data/oct12-multimodal"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--device", default="cpu")
    parser.add_argument("--checkpoint-path", type=Path, default=None,
                        help="hash-verified offline public checkpoint mirror with provenance.json")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--maximum", type=int, default=80)
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--lora-rank", type=int, default=16)
    parser.add_argument("--evaluation-rotations", type=int, choices=[1, 4], default=1)
    parser.add_argument("--layers", default=None, help="comma-separated INTERMEDIATE layer indices")
    parser.add_argument("--bootstrap-prompts", type=int, default=8)
    parser.add_argument("--bootstrap-candidates", type=int, default=4)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("use a fresh immutable evidence directory")
    if args.paper == "woven":
        result = run_woven(args.dataset_dir, args.seed, device=args.device, maximum=args.maximum,
                           steps=args.steps or 24, rank=args.lora_rank,
                           evaluation_rotations=args.evaluation_rotations, checkpoint_path=args.checkpoint_path)
    else:
        layers = None if args.layers is None else [int(x) for x in args.layers.split(",")]
        result = run_umrm(args.dataset_dir, args.seed, device=args.device, maximum=args.maximum,
                          steps=args.steps or 200, layers=layers, bootstrap_prompts=args.bootstrap_prompts,
                          bootstrap_candidates=args.bootstrap_candidates, checkpoint_path=args.checkpoint_path)
    args.output.mkdir(parents=True)
    (args.output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (args.output / "report.md").write_text(render(result))
    print(json.dumps({"paper": args.paper, "baseline": result["baseline"],
                      "method": result["method"], "diagnostic_only": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
