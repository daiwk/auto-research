#!/usr/bin/env python3
"""Hash exactly the exported algorithm/runner files, without machine identifiers."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    "src/auto_research/reproductions/static_constraint_decoding/algorithm.py",
    "src/auto_research/reproductions/cross_task_relationships/model.py",
    "src/auto_research/reproductions/transx/technical_report.py",
    *[f"src/auto_research/foundation_models/{name}.py" for name in ("rope_relay", "cots")],
    *[f"src/auto_research/post_training/{name}.py" for name in
      ("tf_opd", "waypoint_opd", "ggpo", "stopd", "cce_opd", "sif")],
    "scripts/run_oct16_recommendation_components.py",
    "scripts/run_oct16_foundation_components.py",
    "scripts/run_oct16_post_components.py",
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.commit) or args.output.exists():
        raise ValueError("exact commit and fresh artifact path required")
    payload = {"commit": args.commit, "executed_source_sha256": {
        path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in SOURCES}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(payload, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
