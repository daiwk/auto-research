"""Reconcile overlapping discovery captures without turning recall into review."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from auto_research.discovery import repository_paper_statuses, repository_paper_versions
from auto_research.discovery_review import classify_candidate
from auto_research.papers import canonical_arxiv_id

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov09-review-closure"
RUNS = ("39731868655", "40832864995", "42582487347")
TRACKS = ("recommendation", "foundation-model", "post-training", "agent")
MODES = {"submission-window": "candidates", "late-index": "late-index"}
START, END = date(2026, 10, 16), date(2026, 11, 9)
SHANGHAI = ZoneInfo("Asia/Shanghai")
PRIMARY_ID = re.compile(r"26(?:10|11)\.\d{5}")
BATCH = "2026-11-09-bounded-review-reconciliation"
HIGH_COST = "not_reproduced_high_cost"


def read(path: Path) -> dict:
    return json.loads(path.read_bytes())


def local_day(timestamp: str) -> date:
    return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(SHANGHAI).date()


def closed_query(report: dict) -> bool:
    return (report["state"] == "exhausted" and report["coverage_complete"] is True
            and report["transport_complete"] is True and report["cache_fallback_pages"] == 0)


def reviewable_query(report: dict) -> dict:
    return {key: report[key] for key in (
        "query", "categories", "match", "date_from", "date_to", "identifier_months",
        "state", "coverage_complete", "transport_complete", "cache_fallback_pages", "next_offset",
    )}


def ledger_row(row: dict, source_path: str) -> dict:
    """Write actual dispositions only; a retained lead is never a ledger terminal."""
    decision = row.get("decision")
    resolution = row.get("resolution")
    if (row.get("review_done") is not True
            or row.get("automatic_retry") is not False
            or row.get("automatic_implementation_queue") is not False
            or decision not in {"reviewed_deferred", "rejected", "out_of_scope", "accepted"}
            or not resolution or not row.get("reason")
            or row.get("track") not in TRACKS or row.get("priority") not in {"P0", "P1", "P2"}):
        raise ValueError(f"{row.get('id')}: incomplete or nonterminal reviewed disposition")
    if resolution == HIGH_COST:
        required = ("source_url", "basis", "scale", "available_resource", "cost_type")
        if (decision != "reviewed_deferred" or row.get("fulltext_review_completed") is not True
                or not all(row.get("cost_assessment", {}).get(field) for field in required)):
            raise ValueError(f"{row['id']}: high-cost decision lacks scoped original evidence")
    if decision == "accepted" and (row.get("fulltext_review_completed") is not True
                                    or (row["track"] == "recommendation" and row.get("production_gate_passed") is not True)):
        raise ValueError(f"{row['id']}: acceptance lacks original evidence")
    if row.get("implementation_status") in {"implemented", "component_only"}:
        raise ValueError(f"{row['id']}: review cannot deliver implementation")
    return row | {
        "status": "rejected" if decision in {"rejected", "out_of_scope"} else "deferred",
        "review_decision": decision,
        "full_experiment_review_done": resolution == HIGH_COST,
        "implementation_status": "not_implemented_by_review",
        "review_artifact": source_path,
        "full_text_review": {
            "scope": "full-text" if row.get("fulltext_review_completed") else "bounded-source-check",
            "source_locations": row.get("locations", []),
        },
        "source_provenance": [
            {"source_kind": "fixed-primary-source", "source_url": row["source_url"]},
        ],
    }


def merge_review(previous: dict | None, current: dict) -> dict:
    if previous is None:
        return current
    # Separate reviewers can reach the same rejection through different
    # eligibility checks. Do not silently choose between conflicting decisions.
    if any(previous[key] != current[key] for key in ("id", "revision", "decision", "source_url")):
        raise ValueError(f"conflicting primary dispositions: {current['id']}")
    if previous["resolution"] != current["resolution"] and current["status"] != "rejected":
        raise ValueError(f"conflicting review resolutions: {current['id']}")
    return current | {"corroborating_reviews": [*previous.get("corroborating_reviews", []), {
        "review_artifact": previous["review_artifact"], "resolution": previous["resolution"],
        "reason": previous["reason"],
    }]}


def record_selected_reviews(report: dict, reviewed: dict[str, dict]) -> None:
    path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = read(path)
    watermark = read(ROOT / "docs/paper-discovery-watermark.json")["review_watermark"]
    existing = next((batch for batch in ledger["batches"] if batch["batch"] == BATCH), None)
    if existing:
        if (existing["delivery_status"] != "partial_review_pending"
                or any(reviewed.get(row["id"]) != row for row in existing["candidates"])):
            raise ValueError("cannot overwrite reviewed decisions or a completed batch")
        ledger["batches"].remove(existing)
    ledger["batches"].append({
        "schema_version": 1, "batch": BATCH, "date": END.isoformat(),
        "window": report["requested_window"], "scope_kind": "bounded-review-reconciliation",
        "source_artifact": "research-audits/nov09-review-closure/README.md",
        "delivery_status": "partial_review_pending", "selected_scope_complete": False,
        "all_sources_exhaustive": False, "review_watermark_advanced": False,
        "review_watermark": {"before": watermark, "after": watermark},
        "counts": {
            "primary_decisions": len(reviewed),
            "high_cost_review_done": sum(row["resolution"] == HIGH_COST for row in reviewed.values()),
            "implementations": 0, "gpu_runs": 0,
        },
        "candidates": list(reviewed.values()),
    })
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def inventory(source_dir: Path, reviewed: dict[str, dict], *, as_of: str) -> dict:
    if local_day(as_of) != END:
        raise ValueError("expected an explicit November 9 local intraday cutoff")
    docs = ROOT / "docs"
    statuses = repository_paper_statuses(docs / "research-manifest.json", docs / "paper-discovery-ledger.json")
    versions = repository_paper_versions(docs / "paper-discovery-versions.json")
    rows: dict[str, dict] = {}
    tracks: dict[str, set] = defaultdict(set)
    priorities: dict[str, set] = defaultdict(set)
    query_matches: dict[tuple[str, str], set] = defaultdict(set)
    receipts, replacements = [], []
    submission_days: dict[str, set] = defaultdict(set)
    late_months: dict[str, set] = defaultdict(set)

    def observe(row: dict, track: str) -> None:
        identity = canonical_arxiv_id(row["arxiv_id"])
        if not identity:
            raise ValueError("candidate lacks identity")
        rank = (row.get("revision") or 1, row.get("updated") or "", row.get("published") or "")
        if identity not in rows or rank > rows[identity]["rank"]:
            rows[identity] = row | {"rank": rank}
        tracks[identity].add(track)
        priorities[identity].update(row.get("priority_source_matches", []))
        priorities[identity].update(row.get("priority_query_matches", []))
        query_matches[identity, track].update(row.get("matched_queries", []))

    for run in RUNS:
        for track in TRACKS:
            for mode, prefix in MODES.items():
                source = source_dir / run / f"{track}-paper-candidates" / f"paper-{prefix}-{track}.json"
                value = read(source)
                if (value["track"], value["recall_mode"]) != (track, mode):
                    raise ValueError(f"capture has wrong scope: {source.name}")
                transport = value["arxiv_transport"]
                if not transport["queries"] or len(transport["queries"]) != transport["query_count"]:
                    raise ValueError(f"incomplete query reports: {source.name}")
                failures = [q for q in transport["queries"] if not closed_query(q)]
                if failures:
                    if (run, track, mode) != (RUNS[-1], "foundation-model", "late-index") or len(failures) != 1:
                        raise ValueError(f"unrepaired query failure: {source.name}")
                    cap = failures[0]
                    if cap["state"] != "capped" or cap["query"] != "LLM":
                        raise ValueError("replacement does not match the original capped LLM query")
                    for month in cap["identifier_months"]:
                        path = source_dir / f"llm-{month}-replacement.json"
                        rerun = read(path)
                        report = rerun["arxiv_transport"]
                        if (not closed_query(report) or report["identifier_months"] != [month]
                                or any(report[key] != cap[key] for key in ("query", "match", "categories"))
                                or len(rerun["papers"]) != report["next_offset"]):
                            raise ValueError(f"invalid replacement query: {path.name}")
                        replacements.append({
                            "replaces_run": run, "track": track, "mode": mode, "month": month,
                            "source_sha256": sha256(path.read_bytes()).hexdigest(), "query": reviewable_query(report),
                        })
                        for paper in rerun["papers"]:
                            if not canonical_arxiv_id(paper["arxiv_id"]).startswith(month + "."):
                                raise ValueError("split query returned an out-of-month identity")
                            observe(paper | {"revision": int(paper["arxiv_id"].rsplit("v", 1)[1])
                                             if "v" in paper["arxiv_id"] else 1}, track)
                if mode == "submission-window":
                    for query in transport["queries"]:
                        first, last = map(date.fromisoformat, (query["date_from"], query["date_to"]))
                        if (first.isoformat(), last.isoformat()) != (value["window"]["start"], value["window"]["end"]):
                            raise ValueError("submission query dates do not match effective capture bounds")
                    low, high = map(date.fromisoformat, (value["window"]["start"], value["window"]["end"]))
                    submission_days[track].update(low + timedelta(days=i) for i in range((high - low).days + 1))
                else:
                    expected_months = set(transport["queries"][0]["identifier_months"])
                    if any(set(q["identifier_months"]) != expected_months for q in transport["queries"]):
                        raise ValueError("late-index query scope is inconsistent")
                    late_months[track].update(expected_months)
                for candidate in value["candidates"]:
                    observe(candidate, track)
                receipts.append({
                    "run_id": run, "track": track, "mode": mode,
                    "artifact_name": f"{track}-paper-candidates", "file": source.name,
                    "artifact_sha256": sha256(source.read_bytes()).hexdigest(),
                    "requested_window": value["requested_window"], "effective_window": value["window"],
                    "candidate_rows": len(value["candidates"]), "raw_capped_queries": len(failures),
                    "queries": [reviewable_query(q) for q in transport["queries"]],
                })

    # UTC scan dates contain the Shanghai window including Oct 15 16:00 UTC.
    required_days = {START + timedelta(days=i) for i in range(-1, (END - START).days + 1)}
    if not all(required_days <= submission_days[t] and {"2610", "2611"} <= late_months[t] for t in TRACKS):
        raise ValueError("recall lanes do not cover the requested dates and months")

    counts = Counter()
    pending: dict[str, list] = defaultdict(list)
    pending_buckets: Counter = Counter()
    overlap_ids, revision_rows, priority_rows = [], [], []
    for identity, row in sorted(rows.items()):
        published = row.get("published")
        version = row["rank"][0]
        decision = reviewed.get(identity, {})
        prior = versions.get(identity, {})
        decision_covers_version = decision.get("revision", 0) >= version
        latest_reviewed_version = max(decision.get("revision", 0), prior.get("revision", 0))
        is_newer_known_revision = bool(latest_reviewed_version and version > latest_reviewed_version)
        if not published or not START <= local_day(published) <= END:
            if is_newer_known_revision and row.get("updated") and START <= local_day(row["updated"]) <= END:
                revision_rows.append([identity, latest_reviewed_version, version])
            if PRIMARY_ID.fullmatch(identity) and identity not in statuses and identity not in reviewed:
                overlap_ids.append(identity)
            continue
        if decision_covers_version:
            counts["new_primary_decisions"] += 1
        elif is_newer_known_revision:
            counts["newer_versions_pending"] += 1
            revision_rows.append([identity, latest_reviewed_version, version])
        elif identity in statuses:
            counts["existing_disposition"] += 1
        else:
            counts["pending_identity_review"] += 1
            day = local_day(published).isoformat()
            options = {
                classify_candidate(track, row | {
                    "repository_status": "new", "priority_review_required": bool(priorities[identity]),
                    "matched_queries": sorted(query_matches[identity, track]),
                })["review_bucket"] for track in tracks[identity]
            }
            bucket = next(name for name in (
                "revision-fulltext-review", "priority-fulltext-review", "industrial-fulltext-review",
                "historical-fulltext-review", "manual-review", "p2-deferred-review", "query-collision",
            ) if name in options)
            pending[day].append([identity, version, sorted(tracks[identity]), bucket])
            pending_buckets[bucket] += 1
            if priorities[identity]:
                priority_rows.append({"id": identity, "title": row["title"], "signals": sorted(priorities[identity])})

    return {
        "schema_version": 1, "requested_window": {"start": START.isoformat(), "end": END.isoformat()},
        "as_of": as_of, "all_sources_exhaustive": False, "arxiv_recall_matrix_covered": True,
        "candidate_review_complete": not (pending or revision_rows or overlap_ids),
        "review_watermark_advanced": False, "counts": {
            "raw_unique_identities": len(rows), "in_window_identities": sum(counts.values()),
            "late_index_or_missing_date_scope_triage_pending": len(overlap_ids),
            **dict(sorted(counts.items())),
        },
        "capture_receipts": receipts, "query_replacements": replacements,
        "primary_reviewed_ids": sorted(reviewed),
        "pending_bucket_counts": dict(sorted(pending_buckets.items())),
        "pending_identity_columns": ["arxiv_id", "latest_observed_revision", "recall_tracks", "triage_bucket"],
        "pending_identities_by_local_first_publication": dict(sorted(pending.items())),
        "pending_revision_columns": ["arxiv_id", "known_revision", "observed_revision"],
        "pending_revisions": revision_rows, "pending_priority_signals": priority_rows,
        "pending_late_index_scope_triage": overlap_ids,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--record-selected-reviews", action="store_true")
    args = parser.parse_args()
    reviewed = {}
    for filename in ("priority-primary-reviews.json", "industrial-primary-reviews.json", "additional-primary-reviews.json"):
        path = AUDIT / filename
        if path.is_file():
            for row in read(path)["reviews"]:
                if row.get("review_done") is True:
                    normalized = ledger_row(row, path.relative_to(ROOT / "docs").as_posix())
                    reviewed[row["id"]] = merge_review(reviewed.get(row["id"]), normalized)
    report = inventory(args.source_dir, reviewed, as_of=args.as_of)
    args.output.write_text(json.dumps(report, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    if args.record_selected_reviews:
        record_selected_reviews(report, reviewed)
    print(json.dumps(report["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
