#!/usr/bin/env python3
"""Stable maintenance entrypoint replacing one-off dated scripts."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="auto-research-maintain")
    parser.add_argument(
        "action", choices=("manifest", "catalogs", "audit", "sync-readme", "all")
    )
    parser.add_argument(
        "--manifest", type=Path, default=ROOT / ".auto-research" / "papers.json"
    )
    args = parser.parse_args(argv)
    commands = {
        "manifest": [
            sys.executable, "-m", "auto_research.cli", "reproduce",
            "--write-manifest", str(args.manifest),
        ],
        "catalogs": [sys.executable, "scripts/generate_research_catalogs.py"],
        "audit": [sys.executable, "scripts/audit_paper_coverage.py"],
        "sync-readme": [sys.executable, "scripts/sync_project_readme.py"],
    }
    selected = commands if args.action == "all" else {args.action: commands[args.action]}
    for name, command in selected.items():
        print(f"[{name}] {' '.join(command)}")
        completed = subprocess.run(command, cwd=ROOT, check=False)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
