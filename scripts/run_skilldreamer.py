#!/usr/bin/env python3
"""Run actual PSG/HSR/CSI arithmetic diagnostic with verified local resources."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main():
    from auto_research.reproductions.skilldreamer.experiment import run_skilldreamer
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("immutable result already exists")
    result = run_skilldreamer(json.loads(args.config.read_text()), args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"paper": "skilldreamer", "seed": args.seed, "variants": result["variants"]}))


if __name__ == "__main__":
    main()
