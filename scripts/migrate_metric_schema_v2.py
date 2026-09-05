#!/usr/bin/env python3
"""Migrate committed metric artifacts to the auditable result-schema v2.

The migration is deliberately lossless: existing measurements are retained and
only protocol/provenance metadata is added.  Historical single-seed artifacts
remain smoke evidence; the migration never invents additional runs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.reproductions.registry import list_adapters


MIGRATION_ID = "historical-metrics-v2-2026-08-09"


def metric_paths() -> list[Path]:
    paths = set((ROOT / "docs").glob("**/metrics/*.json"))
    paths.update((ROOT / "docs" / "experiments").glob("*.json"))
    return sorted(path for path in paths if path.is_file())


def _adapter_for(path: Path):
    folder = path.parent.parent.name
    for adapter in list_adapters():
        if folder.startswith(f"{adapter.paper.arxiv_id}-"):
            return adapter
    return None


def _integer_seeds(payload: dict[str, Any], path: Path) -> list[int]:
    candidates: Any = payload.get("seeds", payload.get("seed"))
    for container in ("evaluation_protocol", "protocol", "setup"):
        value = payload.get(container)
        if candidates is None and isinstance(value, dict):
            candidates = value.get("seeds", value.get("seed"))
    if isinstance(candidates, int):
        return [candidates]
    if isinstance(candidates, list):
        result = [int(value) for value in candidates if isinstance(value, int)]
        if result:
            return sorted(set(result))
    match = re.search(r"-seeds?(\d+)(?:-(\d+))?$", path.stem)
    if match:
        start = int(match.group(1))
        end = int(match.group(2) or start)
        return list(range(start, end + 1))
    return [42]


def _manifest_ref(path: Path, adapter) -> str:
    if adapter is not None:
        return f"reproduction:{adapter.key}"
    relative = path.relative_to(ROOT / "docs")
    domain = relative.parts[0] if relative.parts else "experiment"
    key = str(path.stem).removesuffix("-metrics")
    return f"{domain}:{key}"


def migrate_payload(path: Path, payload: dict[str, Any]) -> dict[str, Any]:
    seeds = _integer_seeds(payload, path)
    already_v2 = payload.get("schema_version") == 2
    protocol = dict(payload.get("evaluation_protocol") or {})
    # An adapter declares the strongest/default tier for new runs, while an
    # individual artifact records the tier that run actually reached.  Keep
    # an explicit artifact protocol authoritative so a historical L1 proxy is
    # not silently relabelled L2 when the adapter later gains a real dataset
    # implementation.
    tier = protocol.get("tier")
    adapter = None
    if not tier:
        adapter = _adapter_for(path)
        tier = (
            payload.get("evaluation_tier")
            or (adapter.evaluation_tier.value if adapter else None)
            or "l1_mechanism"
        )
    protocol.update({
        "tier": tier,
        "seeds": seeds,
    })
    # Keep an explicit per-artifact comparison declaration authoritative.
    # Multiple seeds improve stability, but do not turn an L1 mechanism
    # diagnostic into a formal capability comparison.
    protocol.setdefault("formal_comparison", len(seeds) >= 3)
    protocol.setdefault(
        "claim_policy",
        "formal multi-seed comparison" if protocol["formal_comparison"] else
        "single/few-seed smoke result; do not claim a stable improvement",
    )
    provenance = dict(payload.get("provenance") or {})
    provenance["artifact_path"] = str(path.relative_to(ROOT))
    # Early v2 artifacts sometimes carried only ``artifact_path``.  The
    # migration must remain a repairable, idempotent contract rather than
    # treating every v2 marker as proof that provenance is complete.
    provenance.setdefault(
        "dataset_fingerprint", "not recorded in historical artifact"
    )
    if not already_v2:
        provenance.update({
            "historical_migration": MIGRATION_ID,
            "original_code_commit": provenance.get("original_code_commit", "not recorded"),
        })
    migrated = dict(payload)
    migrated["schema_version"] = 2
    if not payload.get("manifest_ref") and adapter is None:
        adapter = _adapter_for(path)
    migrated["manifest_ref"] = payload.get("manifest_ref") or _manifest_ref(path, adapter)
    migrated["evaluation_protocol"] = protocol
    migrated["provenance"] = provenance
    return migrated


def migrate(*, write: bool) -> tuple[int, int]:
    changed = 0
    paths = metric_paths()
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise TypeError(f"metric artifact must be an object: {path}")
        migrated = migrate_payload(path, payload)
        rendered = json.dumps(migrated, ensure_ascii=False, indent=2) + "\n"
        if rendered != path.read_text(encoding="utf-8"):
            changed += 1
            if write:
                path.write_text(rendered, encoding="utf-8")
    return len(paths), changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    total, changed = migrate(write=args.write)
    verb = "updated" if args.write else "would update"
    print(f"audited {total} metric artifacts; {verb} {changed}")
    return 0 if args.write or changed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
