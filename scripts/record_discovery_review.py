#!/usr/bin/env python3
"""Atomically append a fully decided discovery artifact to the audit ledger."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

from auto_research.papers import canonical_arxiv_id
from auto_research.discovery_review import (
    metadata_only_disposition, pending_implementation_disposition, priority_review_signal,
)


TERMINAL = {"implemented", "rejected", "deferred"}


def build_batch(artifact: dict, decisions: dict, *, batch_name: str) -> dict:
    decision_map = {
        canonical_arxiv_id(str(item["id"])): item
        for item in decisions.get("decisions", [])
    }
    pending = [
        item for item in artifact.get("candidates", [])
        if item.get("repository_status") == "new" or item.get("revision_review_required")
        or item.get("historical_review_required") or item.get("implementation_review_required")
        or (item.get("repository_status") in {"accepted-unimplemented", "review-deferred", "catalogued", "reviewed"}
            and item.get("arxiv_id") in decision_map)
    ]
    missing = [item["arxiv_id"] for item in pending if item["arxiv_id"] not in decision_map]
    if missing:
        raise ValueError(f"new candidates lack terminal decisions: {missing}")
    rows = []
    for candidate in pending:
        decision = dict(decision_map[candidate["arxiv_id"]])
        if metadata_only_disposition(decision):
            raise ValueError(
                f"{candidate['arxiv_id']}: metadata-only identity/date triage cannot be a "
                "terminal method/cost decision; retain it as a discovery observation"
            )
        accepted_unimplemented = pending_implementation_disposition(decision)
        if accepted_unimplemented and not (
            decision.get("review_done") is True
            and decision.get("automatic_implementation_queue") is False
            and decision.get("implementation_status") in {
                "not_implemented", "not_implemented_by_review", "not_implemented_in_this_review",
            }
        ):
            raise ValueError(f"{candidate['arxiv_id']}: accepted-unimplemented requires completed review, "
                             "explicit non-delivery and no automatic implementation queue")
        status = decision.get("status")
        if status not in TERMINAL:
            raise ValueError(f"{candidate['arxiv_id']}: non-terminal status {status!r}")
        priority = decision.get("priority")
        if priority not in {"P0", "P1", "P2"}:
            raise ValueError(f"{candidate['arxiv_id']}: invalid priority {priority!r}")
        if status != "implemented" and not decision.get("reason"):
            raise ValueError(f"{candidate['arxiv_id']}: {status} requires reason")
        priority_hit = priority_review_signal(candidate)
        review = decision.get("full_text_review", {})
        exception = decision.get("source_exception", {})
        archived_source = (
            decision.get("resolution") in {"source_unavailable_archived", "source_exception_archived"}
            and isinstance(exception, dict)
            and all(exception.get(key) for key in ("source_url", "attempted_at", "error", "archive_reason"))
        )
        substantive = (isinstance(review, dict) and review.get("scope") == "full-text"
                       and bool(review.get("source_locations")))
        if (decision.get("resolution") in {"source_unavailable_archived", "source_exception_archived"}
                and not archived_source):
            raise ValueError(f"{candidate['arxiv_id']}: source exception requires actual source_exception attempt evidence")
        if (priority_hit or accepted_unimplemented) and status != "implemented" and not archived_source and not substantive:
            raise ValueError(
                f"{candidate['arxiv_id']}: Google/Meta or acceptance requires "
                "full_text_review.scope=full-text and source_locations (or a documented source exception)"
            )
        rows.append({
            **decision,
            "id": candidate["arxiv_id"],
            "title": candidate["title"],
            "track": artifact["track"],
            "matched_queries": candidate.get("matched_queries", []),
            "source_provenance": candidate.get("source_provenance", []),
        })
    return {
        "batch": batch_name,
        "date": str(dt.date.today()),
        "scope_kind": "automated-review-closure",
        "required_tracks": [artifact["track"]] if rows else [],
        "source_artifact": decisions.get("source_artifact", "external artifact"),
        "window": artifact.get("window"),
        "candidates": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, default=Path("docs/paper-discovery-ledger.json"))
    parser.add_argument("--batch", required=True)
    args = parser.parse_args()
    artifact = json.loads(args.artifact.read_text(encoding="utf-8"))
    decisions = json.loads(args.decisions.read_text(encoding="utf-8"))
    ledger = json.loads(args.ledger.read_text(encoding="utf-8"))
    if any(item.get("batch") == args.batch for item in ledger.get("batches", [])):
        raise ValueError(f"duplicate batch name: {args.batch}")
    ledger.setdefault("batches", []).append(build_batch(artifact, decisions, batch_name=args.batch))
    temporary = args.ledger.with_suffix(args.ledger.suffix + ".tmp")
    temporary.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(args.ledger)
    print(f"recorded review decisions {args.batch}; acceptance does not assert implementation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
