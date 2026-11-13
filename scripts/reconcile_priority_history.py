#!/usr/bin/env python3
"""Reconcile a saved bounded historical source inventory; no network or reproduction."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from auto_research.discovery_checkpoint import atomic_json
from auto_research.discovery_history import reconcile_priority_history
from auto_research.discovery_sources import load_sources


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path("docs/research-manifest.json"))
    parser.add_argument("--ledger", type=Path, default=Path("docs/paper-discovery-ledger.json"))
    parser.add_argument("--source-config", type=Path, default=Path("configs/paper-discovery-sources.json"))
    parser.add_argument("--track", default="agent", choices=("recommendation", "foundation-model", "post-training", "agent"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    stats = artifact.get("cross_source", artifact).get("source_stats", [])
    payload = reconcile_priority_history(stats, args.manifest, args.ledger,
                                        expected_sources=load_sources(args.source_config, args.track))
    if args.output:
        atomic_json(args.output, payload)
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
