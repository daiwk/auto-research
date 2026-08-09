#!/usr/bin/env python3
"""Fail closed when a paper-discovery batch is incomplete or undocumented."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
TERMINAL = {"implemented", "deferred", "rejected"}
PRIORITIES = {"P0", "P1", "P2"}
TOP_PRIORITY_INSTITUTIONS = {"Google", "Meta"}


def audit(strict: bool = False) -> list[str]:
    data = json.loads(LEDGER.read_text(encoding="utf-8"))
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()
    for batch in data.get("batches", []):
        required = set(batch.get("required_tracks", []))
        present = {entry.get("track") for entry in batch.get("candidates", [])}
        if strict and required - present:
            errors.append(f"{batch['batch']}: tracks without candidates: {sorted(required - present)}")
        if batch.get("scope_kind") == "global":
            required_subtopics = {
                (entry["track"], entry["subtopic"])
                for entry in batch.get("required_subtopics", [])
            }
            present_subtopics = {
                (entry.get("track"), entry.get("subtopic"))
                for entry in batch.get("candidates", [])
            }
            if not required_subtopics:
                errors.append(f"{batch['batch']}: global audit lacks required_subtopics")
            if strict and required_subtopics - present_subtopics:
                errors.append(
                    f"{batch['batch']}: subtopics without a reviewed candidate: "
                    f"{sorted(required_subtopics - present_subtopics)}"
                )
        if batch.get("scope_kind") == "institution-priority":
            required_institutions = set(batch.get("priority_institutions", []))
            if required_institutions != TOP_PRIORITY_INSTITUTIONS:
                errors.append(
                    f"{batch['batch']}: institution-priority audit must cover "
                    f"{sorted(TOP_PRIORITY_INSTITUTIONS)}"
                )
            sweeps = batch.get("institution_sweeps", [])
            swept = {entry.get("organization") for entry in sweeps}
            if required_institutions - swept:
                errors.append(
                    f"{batch['batch']}: missing institution sweeps: "
                    f"{sorted(required_institutions - swept)}"
                )
            candidate_ids = {entry.get("id") for entry in batch.get("candidates", [])}
            for sweep in sweeps:
                if not sweep.get("queries"):
                    errors.append(
                        f"{batch['batch']}: {sweep.get('organization')} sweep lacks queries"
                    )
                missing = set(sweep.get("candidate_ids", [])) - candidate_ids
                if missing:
                    errors.append(
                        f"{batch['batch']}: swept candidates lack terminal records: "
                        f"{sorted(missing)}"
                    )
        for entry in batch.get("candidates", []):
            identity = (batch["batch"], entry.get("id", ""))
            if identity in seen:
                errors.append(f"duplicate candidate: {identity}")
            seen.add(identity)
            status = entry.get("status")
            if batch.get("scope_kind") == "global" and not entry.get("subtopic"):
                errors.append(f"{identity}: global-audit entry lacks subtopic")
            if entry.get("priority") not in PRIORITIES:
                errors.append(f"{identity}: invalid priority {entry.get('priority')!r}")
            if status not in TERMINAL:
                errors.append(f"{identity}: non-terminal status {status!r}")
            if batch.get("scope_kind") == "institution-priority":
                if not entry.get("organization"):
                    errors.append(f"{identity}: priority candidate lacks organization")
                if not entry.get("evidence_gate"):
                    errors.append(f"{identity}: priority candidate lacks evidence gate")
                if not entry.get("priority_reason"):
                    errors.append(f"{identity}: priority candidate lacks priority reason")
                if entry.get("priority") != "P0":
                    errors.append(f"{identity}: Google/Meta eligible candidate is not P0")
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
