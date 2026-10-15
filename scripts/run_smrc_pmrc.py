#!/usr/bin/env python3
"""Run bounded SMRC/PMRC formula and real parameter-update diagnostics."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", default="cpu", help="cpu, cuda or cuda:<index>; no fallback")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--steps", type=int, default=80)
    parser.add_argument("--max-seconds", type=float, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("select a fresh output; do not overwrite diagnostic evidence")
    import torch
    from auto_research.reproductions.smrc_pmrc.experiment import render, run_diagnostic
    torch.set_num_threads(1)
    result = run_diagnostic(device=args.device, seed=args.seed, steps=args.steps,
                            max_seconds=args.max_seconds)
    args.output.mkdir(parents=True)
    (args.output / "result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    (args.output / "report.md").write_text(render(result))
    print(json.dumps({"method": result["method"], "seed": result["seed"],
                      "elapsed_seconds": result["elapsed_seconds"],
                      "numeric_controls": result["numeric_controls"],
                      "diagnostic_only": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
