#!/usr/bin/env python3
"""Classify a discovery artifact without silently dropping broad-query hits."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.discovery_review import classify_artifact


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    classified = classify_artifact(artifact)
    args.output.write_text(json.dumps(classified, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(classified["classification_counts"], ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
