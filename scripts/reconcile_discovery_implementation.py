#!/usr/bin/env python3
"""Generate/check current implementation observations without rewriting reviews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.discovery_implementation import reconcile_review, render_reconciliation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    state = json.loads((ROOT / "docs/paper-discovery-watermark.json").read_text())
    register_path = (ROOT / "docs" / state["candidate_register"]).resolve()
    if not register_path.is_relative_to((ROOT / "docs").resolve()):
        raise ValueError("review register must remain inside docs")
    directory = register_path.parent
    register = json.loads(register_path.read_text())
    manifest = json.loads((ROOT / "docs/research-manifest.json").read_text())
    payload = reconcile_review(register, manifest, ROOT)
    generated = {
        directory / "implementation-status.json": json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        directory / "implementation-status.md": render_reconciliation(payload),
    }
    for path, content in generated.items():
        if args.check:
            if not path.is_file() or path.read_text() != content:
                raise SystemExit(f"stale reconciliation: {path.relative_to(ROOT)}")
        else:
            path.write_text(content)
    print(json.dumps(payload["accepted_counts"], sort_keys=True))


if __name__ == "__main__":
    main()
