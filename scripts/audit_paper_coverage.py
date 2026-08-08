#!/usr/bin/env python3
"""Fail closed when a paper-discovery batch is incomplete or undocumented."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
TERMINAL = {"implemented", "deferred", "rejected"}


def audit(strict: bool = False) -> list[str]:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for batch in data.get("batches", []):
        required = set(batch.get("required_tracks", []))
        present = {entry.get("track") for entry in batch.get("candidates", [])}
        if strict and required - present:
            errors.append(f"{batch['batch']}: tracks without candidates: {sorted(required - present)}")
        for entry in batch.get("candidates", []):
            identity = (batch["batch"], entry.get("id", ""))
            if identity in seen:
                errors.append(f"duplicate candidate: {identity}")
            seen.add(identity)
            status = entry.get("status")
            if status not in TERMINAL:
                errors.append(f"{identity}: non-terminal status {status!r}")
            if status in {"deferred", "rejected"} and not entry.get("reason"):
                errors.append(f"{identity}: {status} entry lacks reason")
            if status == "implemented":
                doc = ROOT / "docs" / entry.get("doc", "")
                if not doc.is_file():
                    errors.append(f"{identity}: missing doc {doc.relative_to(ROOT)}")
                    continue
                text = doc.read_text(encoding="utf-8")
                for marker in (entry["id"], f"`{entry['key']}`", "## 论文信息", "## 本地复现", "<!-- paper-figure:start -->"):
                    if marker not in text:
                        errors.append(f"{identity}: doc missing {marker}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    errors = audit(args.strict)
    if errors:
        raise SystemExit("\n".join(errors))
    print("paper coverage audit: closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
