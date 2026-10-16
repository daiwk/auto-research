#!/usr/bin/env python3
"""Read-only CLASHarness fixed-version import, public view and check aggregation."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.agent_research.clasharness import (
    POLICIES, ProtocolError, fetch_release, import_release, load_release, score_checks, solver_view,
)


def read_json(path: Path):
    cap = 2 * 1024 * 1024
    if path.is_symlink() or not path.is_file() or path.stat().st_size > cap:
        raise ProtocolError("input JSON capped at 2 MiB and must be a regular non-symlink file")
    with path.open("rb") as handle:
        data = handle.read(cap + 1)
    if len(data) > cap:
        raise ProtocolError("input JSON capped at 2 MiB")
    return json.loads(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    for name in ("fetch", "import-reference", "score-checks"):
        child = commands.add_parser(name)
        child.add_argument("--release-dir", type=Path, required=True)
        if name != "fetch":
            child.add_argument("--output", type=Path, required=True)
        if name == "score-checks":
            child.add_argument("--verdicts", type=Path, required=True)
            child.add_argument("--policy", choices=tuple(POLICIES), default="conservative")
            child.add_argument("--expected-checks", type=Path,
                               help="optional JSON array declaring the complete original index/role inventory; not official coverage attestation")
    child = commands.add_parser("solver-view")
    child.add_argument("--task", type=Path, required=True)
    child.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == "fetch":
            result = fetch_release(args.release_dir)
        else:
            if args.output.exists():
                raise ProtocolError("choose a fresh immutable output path")
            if args.action == "import-reference":
                result = import_release(args.release_dir)
            elif args.action == "solver-view":
                result = solver_view(read_json(args.task))
            else:
                row = read_json(args.verdicts)
                if not isinstance(row, dict):
                    raise ProtocolError("verdict input must be an object")
                if args.expected_checks is not None and "expected_checks" in row:
                    raise ProtocolError("provide expected_checks either in verdict JSON or via --expected-checks, not both")
                expected = read_json(args.expected_checks) if args.expected_checks is not None else row.get("expected_checks")
                audit = load_release(args.release_dir)["analysis/v8_check_fairness_audit.json"]
                result = score_checks(row["task_id"], row["checks"], audit=audit, policy=args.policy,
                                      expected_checks=expected)
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with args.output.open("x", encoding="utf-8") as handle:
                json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
                handle.write("\n")
        print(json.dumps({"action": args.action, "kind": result.get("kind"),
                          "local_agent_executed": False, "capability_claim": False}))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
