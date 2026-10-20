#!/usr/bin/env python3
"""Reconcile the bounded priority-source audit without rewriting frozen reviews."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from auto_research.discovery import repository_paper_statuses
from auto_research.discovery_review import metadata_only_disposition, pending_implementation_disposition
from auto_research.papers import canonical_arxiv_id

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / "docs/research-audits/harness2-priority-repair"


def build_inventory(google: dict, meta: dict, ledger: dict, statuses: dict[str, str]) -> dict:
    scoped: dict[str, set[str]] = {}

    def add(identity, organization):
        if identity:
            scoped.setdefault(canonical_arxiv_id(str(identity)), set()).add(organization)

    for row in google["official_pool"]:
        for identity in row.get("ids", []):
            add(identity, "Google/DeepMind official source")
    for row in google["substantive_reviews"]:
        add(row["id"], "Google collaboration confirmed in author block")
    for row in [*meta["directory_inventory"], *meta["known_deferred_ledger_inventory"]]:
        add(row.get("id"), "Meta official source or named prior review")
    add("2610.14224", "Google official repository; first author Northwestern University")
    metadata: dict[str, list[dict]] = {}
    pending: dict[str, dict] = {}
    for batch in ledger.get("batches", []):
        for row in batch.get("candidates", []):
            if not row.get("id"):
                continue
            identity = canonical_arxiv_id(str(row["id"]))
            pointer = {"batch": batch.get("batch"), "id": identity,
                       "title": row.get("title"), "track": row.get("track"),
                       "review_artifact": row.get("review_artifact")}
            if metadata_only_disposition(row):
                metadata.setdefault(identity, []).append(pointer)
            if pending_implementation_disposition(row):
                pending[identity] = pointer
    rows = [{"id": identity, "priority_source_signals": sorted(signals),
             "current_repository_status": statuses.get(identity, "new"),
             "historical_metadata_observations": metadata.get(identity, []),
             "pending_delivery_observation": pending.get(identity)
                 if statuses.get(identity) == "accepted-unimplemented" else None}
            for identity, signals in sorted(scoped.items())]
    return {
        "schema_version": 2, "reviewed_on": "2026-10-21",
        "scope": "Recorded priority historical source inventory, not all papers or all sources",
        "all_sources_exhaustive": False, "review_watermark_advanced": False,
        "frozen_review_snapshots_modified": False,
        "automatic_implementation_queue": False,
        "counts": {
            "scoped_identified_papers": len(rows),
            "scoped_current_statuses": dict(sorted(Counter(r["current_repository_status"] for r in rows).items())),
            "all_ledger_date_only_unique_identities": len(metadata),
            "all_ledger_accepted_unimplemented_identities": sum(
                status == "accepted-unimplemented" for status in statuses.values()),
            "all_ledger_review_deferred_identities": sum(
                status == "review-deferred" for status in statuses.values()),
        },
        "papers": rows,
        "interpretation": [
            "new means no substantive terminal decision or current catalog, not newly published today.",
            "accepted-unimplemented means review acceptance, not an authorized delivery queue.",
            "review-deferred and free-text next-batch suggestions are not acceptance.",
            "catalogued means a catalog record, not full capability reproduction.",
            "reviewed high-cost papers remain terminal; no costly experiment is automatically retried.",
            "The historical ledger-wide pending count is exposed, not accepted as work to implement in this MR.",
            "Official organization signals do not replace first-author affiliation verification.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    result = build_inventory(
        json.loads((DIRECTORY / "google-audit.json").read_text()),
        json.loads((DIRECTORY / "meta-audit.json").read_text()),
        json.loads(ledger_path.read_text()),
        repository_paper_statuses(ROOT / "docs/research-manifest.json", ledger_path),
    )
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    output = DIRECTORY / "backfill-inventory.json"
    if args.check:
        if not output.is_file() or output.read_text() != content:
            raise SystemExit("stale priority backfill inventory")
    else:
        output.write_text(content)
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
