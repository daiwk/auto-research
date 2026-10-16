#!/usr/bin/env python3
"""Compact a real local session; optional bounded download of one MIT public session."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

from auto_research.agent_research.transparent_compact import compact, load_session

PUBLIC_FILE = "thomasmustier-pi-extensions-sessions-2026-01-09T04-23-41-908Z_d587978d-2228-46c3-aac4-7950c2055680.jsonl"
PUBLIC_REVISION = "8c59325"
PUBLIC_URL = ("https://huggingface.co/datasets/MaxDevv/real-pi-coding-agent-traces-sessions/resolve/"
              f"{PUBLIC_REVISION}/{PUBLIC_FILE}")
PUBLIC_SHA256 = "ccc9199e0af18c80f15960f9239dcdc7873d619f06ae17197e624cb62f8d5990"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--leaf-id")
    parser.add_argument("--max-prose-characters", type=int)
    parser.add_argument("--fetch-public-example", action="store_true")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must be a new immutable path")
    if args.fetch_public_example:
        if not args.input.exists():
            with urlopen(PUBLIC_URL, timeout=30) as response:
                data = response.read(4 * 1024 * 1024 + 1)
            if len(data) > 4 * 1024 * 1024 or hashlib.sha256(data).hexdigest() != PUBLIC_SHA256:
                parser.error("public session size/hash mismatch")
            args.input.parent.mkdir(parents=True, exist_ok=True)
            with args.input.open("xb") as handle:
                handle.write(data)
        if hashlib.sha256(args.input.read_bytes()).hexdigest() != PUBLIC_SHA256:
            parser.error("cached public session hash mismatch")
    messages = load_session(args.input, leaf_id=args.leaf_id)
    checkpoint = compact(messages, max_prose_characters=args.max_prose_characters)
    result = checkpoint.to_dict()
    result["input_file_sha256"] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    result["messages_count"] = len(messages)
    result["exact_recovery_verified"] = all(
        checkpoint.recover(key) == row["payload"] for key, row in checkpoint.recovery.items()
    )
    if args.fetch_public_example:
        result["public_source"] = {"url": PUBLIC_URL, "revision": PUBLIC_REVISION, "license": "MIT"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    print(json.dumps({"metrics": result["metrics"], "messages": len(messages),
                      "source_sha256": result["input_file_sha256"],
                      "exact_recovery_verified": result["exact_recovery_verified"],
                      "model_calls": 0}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
