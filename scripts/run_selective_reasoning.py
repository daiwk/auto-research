#!/usr/bin/env python3
"""Fetch pinned small release or recompute official statistics, never run an LLM."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.system_one.selective_reasoning import fetch_release, replay_official


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    fetch = actions.add_parser("fetch")
    fetch.add_argument("--release-dir", type=Path, required=True)
    replay = actions.add_parser("replay")
    replay.add_argument("--release-dir", type=Path, required=True)
    replay.add_argument("--output", type=Path, required=True)
    replay.add_argument("--maximum-seconds", type=int, default=180)
    args = parser.parse_args()
    if args.action == "fetch":
        result = fetch_release(args.release_dir)
    else:
        result = replay_official(args.release_dir, args.output, maximum_seconds=args.maximum_seconds)
        result = {"metrics": result["metrics"], "local_capability_score": None,
                  "model_inference_performed": False, "output": str(args.output)}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
