#!/usr/bin/env python3
"""Offline pinned author-code LeWAM/SmolWAM evaluation, not VQA proxies."""
from __future__ import annotations
import argparse
import json
from pathlib import Path


def main():
    from auto_research.reproductions.lewam.external import execute
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper", choices=("lewam", "smolwam"), required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--phase", choices=("eval", "train"), default="eval")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("immutable result already exists")
    result = execute({**json.loads(args.config.read_text()), "phase": args.phase}, args.seed, args.paper)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"paper": args.paper, "seed": args.seed, "variants": result["variants"]}))


if __name__ == "__main__":
    main()
