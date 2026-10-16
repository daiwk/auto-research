#!/usr/bin/env python3
"""CTXGAP CPU frozen-score reproduction and gold-free public task export."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.agent_research.ctxgap import (
    ProtocolError, PublicProbe, fetch_release, observer_input, reproduce_release, score_public_labels,
    validate_public_plan,
)


def read_json(path: Path):
    cap = 16 * 1024 * 1024
    if path.is_symlink() or not path.is_file() or path.stat().st_size > cap:
        raise ProtocolError("public input JSON capped at 16 MiB and must be a regular non-symlink file")
    with path.open("rb") as handle:
        data = handle.read(cap + 1)
    if len(data) > cap:
        raise ProtocolError("public input JSON capped at 16 MiB")
    return json.loads(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for name in ("fetch", "reproduce"):
        child = commands.add_parser(name)
        child.add_argument("--release-dir", type=Path, required=True)
        if name == "reproduce":
            child.add_argument("--output", type=Path, required=True)
            child.add_argument("--bootstrap", type=int, default=10000)
    for name in ("export-observer-inputs", "score-labels"):
        child = commands.add_parser(name)
        child.add_argument("--probes", type=Path, required=True,
                           help="JSON array of PublicProbe fields; references stay on scorer side")
        child.add_argument("--output", type=Path, required=True)
        if name == "score-labels":
            child.add_argument("--labels", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == "fetch":
            result = fetch_release(args.release_dir)
        else:
            if args.output.exists():
                raise ProtocolError("choose a fresh immutable output path")
            if args.action == "reproduce":
                result = reproduce_release(args.release_dir, draws=args.bootstrap)
            else:
                raw = read_json(args.probes)
                if not isinstance(raw, list) or not 1 <= len(raw) <= 10000:
                    raise ProtocolError("use 1..10000 explicit public probes")
                if any(not isinstance(row, dict) for row in raw):
                    raise ProtocolError("public probe entries must be objects")
                probes = [PublicProbe(**row) for row in raw]
                validate_public_plan(probes)
                result = ({"condition": "U_public", "tasks": [observer_input(p) for p in probes],
                           "contains_references": False, "local_execution_performed": False}
                          if args.action == "export-observer-inputs" else
                          score_public_labels(probes, read_json(args.labels)))
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
                handle.write("\n")
        print(json.dumps({k: v for k, v in result.items() if k not in {"tasks", "input_sha256"}}, ensure_ascii=False))
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
