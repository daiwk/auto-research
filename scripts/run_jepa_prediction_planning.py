#!/usr/bin/env python3
"""Run the CPU-only frozen-decoder protocol on user-supplied JSON arrays."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.jepa_evaluation import run_protocol  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("output cannot overwrite the protocol inputs")
    if args.output.exists():
        parser.error("output already exists; use a fresh result path")
    if args.input.stat().st_size > 16 * 1024 * 1024:
        parser.error("16MB bounded protocol input ceiling exceeded")
    raw = args.input.read_bytes()
    if len(raw) > 16 * 1024 * 1024:
        parser.error("16MB bounded protocol input ceiling exceeded")
    payload = json.loads(raw)
    result = run_protocol(payload)
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "episodes": result["fidelity"]["episodes"],
                      "diagnostic_only": True}, ensure_ascii=False))


if __name__ == "__main__":
    main()
