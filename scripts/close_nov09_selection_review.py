"""Publish the explicitly authorized November selection-review closeout, not method completion."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from auto_research.discovery import repository_paper_records
from auto_research.discovery_watermark import audit_review_watermark
from auto_research.papers import canonical_arxiv_id
from build_nov09_review_inventory import (
    AUDIT, BATCH, CONTINUED_SCOPE_FILES, END, MODES, PRIMARY_FILES, ROOT, RUNS, START, TRACKS,
    closed_query, inventory, ledger_row, local_day, merge_review, read, record_selected_reviews, reviewable_query,
)

WINDOW = {"start": START.isoformat(), "end": END.isoformat()}
SEMANTICS = "selection-screening-with-protected-primary-review"


def write(path: Path, value: dict, *, compact_rows: str | None = None) -> None:
    if compact_rows:
        rest = {k: v for k, v in value.items() if k != compact_rows}
        prefix = json.dumps(rest, ensure_ascii=False, indent=2)[:-2]
        rows = value[compact_rows]
        content = prefix + f',\n  "{compact_rows}": [\n' + ",\n".join(
            "    " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows
        ) + "\n  ]\n}\n"
    else:
        content = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.write_text(content, encoding="utf-8")


def primary_reviews() -> dict[str, dict]:
    reviews: dict[str, dict] = {}
    for filename in PRIMARY_FILES:
        path = AUDIT / filename
        if path.is_file():
            for row in read(path)["reviews"]:
                if row.get("review_done") is True:
                    value = ledger_row(row, path.relative_to(ROOT / "docs").as_posix())
                    reviews[row["id"]] = merge_review(reviews.get(row["id"]), value)
    return reviews


def recall_inputs(source_dir: Path, report: dict) -> tuple[dict, dict]:
    """Preserve containing query bounds and replace, rather than bless, the capped query."""
    observed: dict[str, dict] = {}
    derived = {}
    for track in TRACKS:
        for mode, prefix in MODES.items():
            queries, sources, replacements = [], [], []
            candidate_ids, versions = set(), {}
            for run in RUNS:
                path = source_dir / run / f"{track}-paper-candidates" / f"paper-{prefix}-{track}.json"
                payload = read(path)
                key = path.relative_to(source_dir).as_posix()
                receipt = next(r for r in report["capture_receipts"] if
                               (r["run_id"], r["track"], r["mode"]) == (run, track, mode))
                if sha256(path.read_bytes()).hexdigest() != receipt["artifact_sha256"]:
                    raise ValueError("raw recall capture changed")
                sources.append(receipt)
                rows = [(row, key) for row in payload["candidates"]]
                for query in payload["arxiv_transport"]["queries"]:
                    if closed_query(query):
                        queries.append(reviewable_query(query) | {"source_capture": key})
                        continue
                    repaired = [r for r in report["query_replacements"] if
                                (r["replaces_run"], r["track"], r["mode"]) == (run, track, mode)]
                    if len(repaired) != 2 or query["query"] != "LLM" or query["state"] != "capped":
                        raise ValueError("unrepaired containing query")
                    for replacement in repaired:
                        replacement_path = source_dir / f"llm-{replacement['month']}-replacement.json"
                        fixed = read(replacement_path)
                        if sha256(replacement_path.read_bytes()).hexdigest() != replacement["source_sha256"]:
                            raise ValueError("replacement capture changed")
                        rows.extend((row, replacement_path.name) for row in fixed["papers"])
                        queries.append(replacement["query"] | {"source_capture": replacement_path.name})
                    replacements.append({"original_capture": key, "original_query_report": reviewable_query(query),
                                         "actual_replacement_receipts": repaired})
                for row, actual_capture in rows:
                    identity = canonical_arxiv_id(row["arxiv_id"])
                    revision = row.get("revision") or (int(row["arxiv_id"].rsplit("v", 1)[1])
                                                       if "v" in row["arxiv_id"] else 1)
                    candidate_ids.add(identity)
                    rank = (revision, row.get("updated", ""), row.get("published", ""))
                    if identity not in versions or rank > versions[identity]["rank"]:
                        versions[identity] = {"revision": revision, "capture": actual_capture, "rank": rank}
                    before = observed.get(identity)
                    if before is None or rank > before["rank"]:
                        observed[identity] = row | {"id": identity, "revision": revision, "rank": rank,
                                                    "capture": actual_capture}
            derived[track, mode] = {"queries": queries, "sources": sources, "replacements": replacements,
                                    "ids": candidate_ids, "versions": versions}
    tail = read(AUDIT / "nov09-tail-source-receipt.json")
    for row in tail["records"]:
        observed[row["id"]] = row | {"published": row["first_submission_utc"],
                                     "capture": "nov09-tail-all-categories.atom"}
    for (track, mode), value in derived.items():
        if mode == "submission-window":
            value["ids"].update(row["id"] for row in tail["records"])
            value["versions"].update({row["id"]: {"revision": row["revision"], "capture": "nov09-tail-all-categories.atom"}
                                      for row in tail["records"]})
    return observed, derived


def make_register(observed: dict, reviewed: dict, report: dict) -> dict:
    metadata = {}
    for filename in ("abstract-scope-screen.json", *CONTINUED_SCOPE_FILES):
        metadata.update({r["id"]: (r, filename) for r in read(AUDIT / filename)["records"]})
    overlap = read(AUDIT / "continued-late-tail-triage.json")
    metadata.update({r["id"]: (r, "continued-late-tail-triage.json") for r in overlap["records"]
                     if r["disposition"] == "exclude_from_window_scope"})
    p2 = {r["id"]: r for r in read(AUDIT / "p2-selection-screen.json")["records"]}
    known = repository_paper_records(ROOT / "docs/research-manifest.json", ROOT / "docs/paper-discovery-ledger.json")
    date_screen = set(read(AUDIT / "late-index-scope.json")["terminal_ids"])
    papers = []
    for identity in sorted(observed.keys() | reviewed.keys()):
        row = observed.get(identity, reviewed.get(identity))
        paper = {k: row[k] for k in ("title", "published", "revision") if k in row}
        paper |= {"id": identity, "capture": row.get("capture", row.get("source_file")),
                  "automatic_implementation_queue": False, "implementation_status": "not_changed_by_review"}
        if identity in reviewed:
            review = reviewed[identity]
            if review.get("original_publication"):
                paper["original_publication"] = review["original_publication"]
            paper |= {"status": "accepted" if review["decision"] == "accepted" else
                      "reviewed_deferred" if review["decision"] == "reviewed_deferred" else "rejected_or_out_of_scope",
                      "review_scope": ("bounded-original-source-sections" if review.get("fulltext_review_completed")
                                       else "bounded-source-check"), "reviews": [{
                          k: review[k] for k in ("decision", "resolution", "review_done", "fulltext_review_completed",
                                               "reason", "source_url", "source_sha256", "review_artifact") if k in review}],
                      "method_review_completed": review.get("fulltext_review_completed") is True}
        elif identity in p2:
            decision = p2[identity]
            paper |= {"title": decision["title"], "published": decision["published"],
                      "status": "not_selected_p2", "priority": "P2", "selection_review_done": True,
                      "review_scope": "title-abstract-selection", "method_review_completed": False,
                      "fulltext_review_completed": False, "originality_not_rejected": True,
                      "protected_priority_signal": False, "protected_production_signal": False,
                      "metadata_sha256": decision["metadata_sha256"],
                      "reason": decision["reason"], "selection_artifact": "p2-selection-screen.json"}
        elif identity in metadata:
            decision, reference = metadata[identity]
            paper |= {"status": "window_scope_excluded", "review_scope": "title-abstract-scope",
                      "method_review_completed": False, "reason": decision["reason"], "review_artifact": reference}
        elif identity in known:
            paper |= {"status": "known", "review_scope": "inherited-disposition-not-new-method-review",
                      "inherited_repository_status": known[identity]["repository_status"],
                      "review_artifacts": ["../../paper-discovery-ledger.json", "../../research-manifest.json"]}
        elif identity in date_screen or (row.get("published") and not START <= local_day(row["published"]) <= END):
            paper |= {"status": "outside_window_date_screen", "review_scope": "identity-date-only",
                      "method_review_completed": False,
                      "reason": "Outside this first-publication window; captured updates/version dispositions remain separately pinned.",
                      "review_artifact": "late-index-scope.json" if identity in date_screen else "review-inventory.json"}
        else:
            raise ValueError(f"{identity}: candidate has no authorized terminal disposition")
        papers.append(paper)
    return {"schema_version": 2, "requested_window": WINDOW, "review_finalized_on": "2026-11-11",
            "review_as_of": report["as_of"], "review_semantics": SEMANTICS,
            "candidate_review_complete": True, "selection_review_complete": True, "method_review_complete": False,
            "all_sources_exhaustive": False, "implementation_complete": False,
            "selection_policy": "p2-selection-policy.json", "unique_papers": len(papers),
            "date_semantics": "published is the captured arXiv v1 submission, not a verified original first-publication date; reprints retain source-review date corrections",
            "counts": dict(sorted(Counter(r["status"] for r in papers).items())),
            "source_exceptions": [], "papers": papers}


def build(source_dir: Path, *, advance: bool) -> dict:
    previous_state = read(ROOT / "docs/paper-discovery-watermark.json")
    if previous_state["review_watermark"] not in {"2026-10-15", END.isoformat()}:
        raise ValueError("refusing to overwrite an unrelated/newer review watermark")
    reviewed = primary_reviews()
    report = inventory(source_dir, reviewed, as_of="2026-11-09T18:23:24+08:00")
    if not report["candidate_review_complete"]:
        raise ValueError(f"selection/priority review still open: {report['counts']}")
    observed, derived = recall_inputs(source_dir, report)
    register = make_register(observed, reviewed, report)
    register_ids = {r["id"] for r in register["papers"]}
    official = read(AUDIT / "p2-official-source-closure.json")
    if {k: official["window"][k] for k in WINDOW} != WINDOW:
        raise ValueError("official source review has a different window")
    archives, source_refs, declared = {}, [], []
    for source in official["sources"]:
        slug = source["organization"].lower().replace(" ", "-")
        filename = f"{slug}-source-review.json"
        for row in source["records"]:
            if row["review_status"] == "reviewed" and not register_ids.intersection(row.get("arxiv_ids", [])):
                raise ValueError(f"{row['url']}: reviewed official record lacks its candidate")
            if row["review_status"] == "reviewed" and not any(
                reviewed.get(identity, {}).get("fulltext_review_completed") is True
                for identity in row.get("arxiv_ids", [])
            ):
                raise ValueError(f"{row['url']}: priority original cannot be replaced by P2 selection")
        payload = source | {"window": WINDOW, "expected_records": len(source["records"]),
                            "all_sources_exhaustive": False}
        write(AUDIT / filename, payload)
        source_refs.append({"organization": source["organization"], "artifact": f"research-audits/nov09-review-closure/{filename}"})
        declared.append({"organization": source["organization"], "records": len(source["records"]),
                         "pages": len(source.get("pages", []))})
        for row in [r for r in source["records"] if r["review_status"] == "explicit_exception"] + source.get("directory_exceptions", []):
            entry = row | {"organization": source["organization"], "status": "archived", "blocking": False}
            archives[entry["organization"], entry["url"], entry["exception_type"]] = entry
    write(AUDIT / "paper-register.json", register, compact_rows="papers")
    write(AUDIT / "exception-archive.json", {"schema_version": 1, "archived_on": "2026-11-11",
          "blocking": False, "retry_policy": "on-new-evidence-only", "record_count": len(archives),
          "entries": list(archives.values()), "previous_archive": "../oct15-review-closure/exception-archive.json",
          "note": "Current bounded source exceptions only; earlier evidence is retained, not relabeled or deleted."})
    receipt_refs = []
    for (track, mode), value in derived.items():
        filename = f"{track}-{mode}-retrieval.json"
        payload = {"schema_version": 1, "track": track, "recall_mode": mode, "requested_window": WINDOW,
                   "candidate_payload_scope": "identity/version references, not algorithm review",
                   "candidates": [{"arxiv_id": identity,
                                   "revision": value["versions"][identity]["revision"],
                                   "source_capture": value["versions"][identity]["capture"]}
                                  for identity in sorted(value["ids"])],
                   "arxiv_transport": {"coverage_complete": True, "transport_complete": True,
                                       "capped_queries": 0, "failed_queries": 0, "queries": value["queries"]},
                   "derived_from": {"actual_query_bounds_preserved": True, "source_receipts": value["sources"],
                                    "query_replacements": value["replacements"]},
                   "supplemental_atom": read(AUDIT / "nov09-tail-source-receipt.json") if mode == "submission-window" else None}
        write(AUDIT / filename, payload)
        receipt_refs.append({"track": track, "mode": mode, "artifact": f"research-audits/nov09-review-closure/{filename}"})
    state = {"schema_version": 2, "policy": previous_state["policy"], "checked_on": "2026-11-11",
             "user_authorized_exceptions": True,
             "authorization_record": "2026-10-10 retired source-exhaustiveness; 2026-10-15 high-cost no reproduction is review DONE; "
             "2026-11-11 user explicitly approved P2 title/abstract selection closure, not verification of every method. "
             "Google/Meta and possible production A/B still require priority primary review.",
             "window": WINDOW, "review_watermark": END.isoformat(), "review_as_of": report["as_of"],
             "review_semantics": SEMANTICS, "selection_review_complete": True, "method_review_complete": False,
             "selection_policy": "research-audits/nov09-review-closure/p2-selection-policy.json",
             "all_sources_exhaustive": False, "implementation_complete": False,
             "candidate_register": "research-audits/nov09-review-closure/paper-register.json",
             "retrieval_receipts": receipt_refs, "source_reviews": source_refs,
             "exception_archive": "research-audits/nov09-review-closure/exception-archive.json",
             "next_scan_start_with_overlap": "2026-11-08",
             "exception_reopening_policy": "Only new identity/date/document/independent source evidence reopens archived sources; no automatic retry. "
             "New priority/production or changed metadata can reopen a P2 selection; it is not an originality rejection.",
             "coverage_scope": {"tracks": list(TRACKS), "recall_modes": list(MODES), "official_sources": declared,
               "counts": report["counts"] | {"registered_unique_identities": len(register_ids), "primary_decisions": len(reviewed)},
               "limitations": ["Review watermark is selection screening plus protected primary-source decisions, not method verification for every paper.",
                  "Fixed four-track/two-mode containing recall with actual split replacements; no all-web or all-site exhaustiveness.",
                  "Late-index captures have the pinned intraday cutoff; the official Atom adds first releases to November 9 midnight, not all later revisions.",
                  "P2 nonselection is window-only, preserves novelty and does not establish actual affiliation absence from abstract evidence.",
                  "No new implementation, training, GPU receipt, capability gain, or executable evolve integration is implied.",
                  *("Official-source subreview: " + item for item in official.get("limitations", []))]}}
    write(AUDIT / "review-inventory.json", report)
    record_selected_reviews(report, reviewed)
    write(AUDIT / "closed-watermark-proposal.json", state)
    if advance:
        write(ROOT / "docs/paper-discovery-watermark.json", state)
        errors = audit_review_watermark(ROOT)
        if errors:
            write(ROOT / "docs/paper-discovery-watermark.json", previous_state)
            raise ValueError("; ".join(errors))
        report["review_watermark_advanced"] = True
        write(AUDIT / "review-inventory.json", report)
        ledger = read(ROOT / "docs/paper-discovery-ledger.json")
        batch = next(b for b in ledger["batches"] if b["batch"] == BATCH)
        batch["review_watermark"] = {"before": "2026-10-15", "after": END.isoformat()}
        batch["review_watermark_advanced"] = True
        write(ROOT / "docs/paper-discovery-ledger.json", ledger)
    return {"counts": report["counts"], "register_counts": register["counts"], "exceptions": len(archives),
            "advanced": advance, "method_review_complete": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--advance", action="store_true", help="Apply this user-authorized closeout only after all guards pass")
    args = parser.parse_args()
    print(json.dumps(build(args.source_dir, advance=args.advance), ensure_ascii=False))


if __name__ == "__main__":
    main()
