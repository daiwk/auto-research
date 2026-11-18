"""Close the bounded Nov10--15 selection review without asserting implementation."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from auto_research.discovery_watermark import audit_review_watermark
from build_nov09_review_inventory import ledger_row
from prepare_nov15_review_closure import AUDIT, CACHE, MODES, ROOT, RUN, TRACKS, WINDOW, metadata_digest
from screen_nov09_p2_selection import apply_clarifications

SEMANTICS = "selection-screening-with-protected-primary-review"
BATCH = "2026-11-15-selection-review-closeout"
PRIOR = "research-audits/nov09-review-closure/closed-watermark-proposal.json"
REL = "research-audits/nov15-review-closure/"


def read(path: Path) -> dict:
    return json.loads(path.read_bytes())


def write(path: Path, value: dict, *, compact: str | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if compact:
        body = json.dumps({k: v for k, v in value.items() if k != compact}, ensure_ascii=False, indent=2)[:-2]
        rows = ",\n".join("    " + json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in value[compact])
        text = body + f',\n  "{compact}": [\n' + rows + "\n  ]\n}\n"
    else:
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def reviews() -> dict[str, dict]:
    result = {}
    for path in sorted(AUDIT.glob("*-primary-reviews.json")):
        for row in read(path)["reviews"]:
            reference = path.relative_to(ROOT / "docs").as_posix()
            value = ledger_row(row, reference)
            if row["id"] in result:
                raise ValueError(f"Overlapping primary ownership: {row['id']}")
            result[row["id"]] = value
    return result


def build(*, advance: bool = False) -> dict:
    frozen = read(CACHE / "frozen-inventory.json")
    if frozen["window"] != WINDOW:
        raise ValueError("wrong frozen review window")
    originals = {r["id"]: r for r in frozen["records"]}
    primary = reviews()
    clarifications = {}
    clarification_refs = []
    for path in sorted(AUDIT.glob("*-signal-clarifications.json")):
        payload = read(path)
        if payload["window"] != WINDOW:
            raise ValueError("wrong clarification window")
        clarification_refs.append({"path": path.relative_to(ROOT / "docs").as_posix(), "sha256": sha256(path.read_bytes()).hexdigest()})
        for row in payload["clarifications"]:
            clarifications.setdefault(row["id"], []).append(row)
    included = {i: r for i, r in originals.items() if r["routing"] != "outside_window_date_screen"}
    # Independent official-source backfills must not disappear just because they
    # were not part of one arXiv query matrix.
    for identity, review in primary.items():
        if identity not in originals:
            raise ValueError(f"Primary review lacks captured identity: {identity}")
        included[identity] = originals[identity]
        original = originals[identity]
        raw = original["metadata"]
        if (review["revision"] != original["revision"] or review["title"] != raw["title"]
                or review["published"] != raw["published"]
                or review["metadata_sha256"] != metadata_digest(raw)):
            raise ValueError(f"Primary review is stale: {identity}")
    always = {i: r["positive_signal_matches"]["policy_protected_identity"]
              for i, r in included.items() if "policy_protected_identity" in r["positive_signal_matches"]}
    policy = {
        "schema_version": 1, "window": WINDOW, "authorized_on": "2026-11-11",
        "authorization": {"source": "Continuing user authorization: Nov11 explicit P2 selection approval; Nov18 request to complete this subsequent review window under the existing review semantics.",
                          "answer": "允许 P2 选题级结案", "p2_selection_closure_allowed": True,
                          "new_answer_invented": False},
        "review_scope": "title-abstract-selection", "terminal_selection_decision": "not_selected_this_window_p2",
        "always_protected_identities": always,
        "meaning": "Window-only selection; not originality rejection, method/cost verification or implementation. Google/Meta, possible production and new-revision conflicts need primary review.",
        "input_sha256": sha256((CACHE / "frozen-inventory.json").read_bytes()).hexdigest(),
        "reopen_conditions": ["changed revision or metadata", "new institutional/production evidence", "user prioritization"],
    }
    write(AUDIT / "p2-selection-policy.json", policy)
    selected, register, unresolved = [], [], []
    for identity, item in sorted(included.items()):
        raw = item["metadata"]
        paper = {"id": identity, "title": raw["title"], "published": raw["published"],
                 "updated": raw.get("updated"), "revision": item["revision"],
                 "metadata_sha256": metadata_digest(raw), "captures": item["capture_refs"],
                 "automatic_implementation_queue": False, "implementation_status": "not_changed_by_review"}
        if identity in primary:
            review = primary[identity]
            paper |= {"status": "accepted" if review["decision"] == "accepted" else "reviewed_deferred" if review["decision"] == "reviewed_deferred" else "rejected_or_out_of_scope",
                      "review_scope": "bounded-original-source-sections", "reviews": [review],
                      "method_review_completed": review["fulltext_review_completed"],
                      "reason": review["reason"]}
        elif item["routing"] == "known":
            paper |= {"status": "known", "inherited_repository_record": item["inherited_repository_record"],
                      "review_scope": "inherited-terminal-not-new-method-or-implementation-review",
                      "method_review_completed": False,
                      "reason": "Reuse existing scoped terminal/cost/catalog decision; does not upgrade an implementation or claim a later revision was experimentally revalidated."}
        else:
            signals, used = apply_clarifications(raw, item["positive_signal_matches"], clarifications.get(identity, []))
            if signals:
                unresolved.append({"id": identity, "signals": signals})
                continue
            row = {"id": identity, "revision": item["revision"], "title": raw["title"], "published": raw["published"],
                   "updated": raw.get("updated"), "metadata_sha256": metadata_digest(raw),
                   "abstract_sha256": sha256(raw["abstract"].encode()).hexdigest(),
                   "title_witness": raw["title"], "abstract_witness": raw["abstract"].split(". ", 1)[0],
                   "tracks": item["tracks"], "captures": item["capture_refs"], "priority": "P2",
                   "scope": "title-abstract-selection", "decision": "not_selected_this_window_p2",
                   "selection_review_done": True, "method_verified": False, "method_review_completed": False,
                   "fulltext_review_completed": False, "high_cost": False, "implementation": False,
                   "originality_not_rejected": True, "automatic_retry": False, "automatic_implementation_queue": False,
                   "positive_signal_matches": item["positive_signal_matches"], "signal_clarifications": used,
                   "reason": "按本窗口研究优先级未纳入重点；标题摘要选题结案不否定新算法/基准，不等于方法、成本或能力已核验。"}
            selected.append(row)
            paper |= {k: row[k] for k in ("priority", "selection_review_done", "method_review_completed", "fulltext_review_completed", "originality_not_rejected", "reason")}
            paper |= {"status": "not_selected_p2", "review_scope": "title-abstract-selection",
                      "protected_priority_signal": False, "protected_production_signal": False}
        register.append(paper)
    if unresolved:
        write(CACHE / "unresolved.json", {"records": unresolved})
        raise ValueError(f"Unreviewed protected candidates: {len(unresolved)}")
    write(AUDIT / "p2-selection-screen.json", {
        "schema_version": 1, "window": WINDOW, "scope": "title-abstract-selection",
        "policy_sha256": sha256((AUDIT / "p2-selection-policy.json").read_bytes()).hexdigest(),
        "protected_records": [], "protected_ids": [], "signal_review_sources": clarification_refs,
        "method": "Deterministic title/abstract routing plus paper-specific semantic clarifications; no human whole-article read claimed",
        "global_substantive_ledger_write": False, "counts": {"selected_window_only": len(selected), "protected_pending_original": 0},
        "records": selected}, compact="records")
    # Keep the actual metadata needed to replay the selection. Outside-window
    # rows preserve identity/date/fingerprint only; they are not method reviews.
    index = []
    outside = []
    for identity, item in sorted(originals.items()):
        raw = item["metadata"]
        if identity in included:
            index.append({"id": identity, "revision": item["revision"], "metadata": raw,
                          "tracks": item["tracks"], "positive_signal_matches": item["positive_signal_matches"],
                          "routing": item["routing"], "capture_refs": item["capture_refs"]})
        else:
            outside.append({"id": identity, "revision": item["revision"], "published": raw["published"],
                            "updated": raw.get("updated"), "metadata_sha256": metadata_digest(raw),
                            "review_scope": "window-date-only-not-method-review"})
    write(AUDIT / "input-index.json", {"schema_version": 1, "window": WINDOW,
           "capture_receipts": frozen["capture_receipts"], "records": index}, compact="records")
    write(AUDIT / "outside-window.json", {"schema_version": 1, "window": WINDOW,
           "not_global_method_dispositions": True, "records": outside}, compact="records")
    write(AUDIT / "paper-register.json", {"schema_version": 2, "requested_window": WINDOW,
          "review_finalized_on": "2026-11-18", "candidate_review_complete": True,
          "review_semantics": SEMANTICS, "selection_review_complete": True, "method_review_complete": False,
          "all_sources_exhaustive": False, "implementation_complete": False, "source_exceptions": [],
          "counts": dict(Counter(r["status"] for r in register)), "unique_papers": len(register), "papers": register}, compact="papers")
    receipt_refs = []
    for track in TRACKS:
        for mode, prefix in MODES.items():
            path = CACHE / "captures" / RUN / f"{track}-paper-candidates" / f"paper-{prefix}-{track}.json"
            raw = read(path)
            proof = {"source_run": RUN, "artifact": f"{track}-paper-candidates", "file": path.name,
                     "sha256": sha256(path.read_bytes()).hexdigest(), "original_window": raw["window"],
                     "original_transport": raw["arxiv_transport"]}
            queries, replaced = [], []
            for query in raw["arxiv_transport"]["queries"]:
                if query["state"] == "exhausted" and query["coverage_complete"] and query["transport_complete"] and not query["cache_fallback_pages"]:
                    queries.append(query)
                elif track == "foundation-model" and mode == "late-index" and query["query"] == "LLM" and query["state"] == "capped":
                    replaced.append(query)
                    for month in ("2610", "2611"):
                        replacement = read(CACHE / f"llm-{month}-replacement.json")
                        queries.append(replacement["query"])
                else:
                    raise ValueError("unresolved failed/capped/cache-fallback query")
            if any(q["state"] != "exhausted" or not q["coverage_complete"] or not q["transport_complete"] or q["cache_fallback_pages"] for q in queries):
                raise ValueError("replacement query is not complete")
            candidates = {r["arxiv_id"].split("v")[0] for r in raw["candidates"]} & included.keys()
            if replaced:
                for month in ("2610", "2611"):
                    candidates |= {r["arxiv_id"].split("v")[0] for r in read(CACHE / f"llm-{month}-replacement.json")["papers"]} & included.keys()
            filename = f"{track}-{mode}-retrieval.json"
            write(AUDIT / filename, {"schema_version": 1, "track": track, "recall_mode": mode, "requested_window": WINDOW,
                  "containing_capture": proof, "original_capped_queries_preserved": replaced,
                  "candidate_payload_scope": "Window-date screened exact identities; not methods or implementation; all other raw IDs are in outside-window.json",
                  "arxiv_transport": {"coverage_complete": True, "transport_complete": True, "capped_queries": 0, "failed_queries": 0, "queries": queries},
                  "candidates": [{"arxiv_id": i, "revision": included[i]["revision"]} for i in sorted(candidates)]}, compact="candidates")
            receipt_refs.append({"track": track, "mode": mode, "artifact": REL + filename})
    source_refs, declared, archives = [], [], {}
    for slug in ("google", "google-deepmind", "meta"):
        filename = f"{slug}-source-review.json"
        source = read(AUDIT / filename)
        source_refs.append({"organization": source["organization"], "artifact": REL + filename})
        declared.append({"organization": source["organization"], "records": len(source["records"]), "pages": len(source.get("pages", []))})
        for row in [r for r in source["records"] if r["review_status"] == "explicit_exception"] + source.get("directory_exceptions", []):
            entry = row | {"organization": source["organization"], "status": "archived", "blocking": False}
            archives[entry["organization"], entry["url"], entry["exception_type"]] = entry
    write(AUDIT / "exception-archive.json", {"schema_version": 1, "archived_on": "2026-11-18",
           "blocking": False, "retry_policy": "on-new-evidence-only", "record_count": len(archives),
           "previous_archive": "../nov09-review-closure/exception-archive.json", "entries": list(archives.values())})
    counts = {"raw_unique_identities": len(originals), "outside_window_date_only": len(outside),
              "registered_unique_identities": len(register), "primary_decisions": len(primary),
              "p2_selection_only_closed": len(selected), "inherited_terminal": sum(r["status"] == "known" for r in register),
              "high_cost_review_done": sum(r["resolution"] == "not_reproduced_high_cost" for r in primary.values()),
              "accepted_low_cost_not_implemented": sum(r["decision"] == "accepted" for r in primary.values()),
              "protected_pending": 0, "implementations": 0, "gpu_runs": 0}
    state = {"schema_version": 2, "policy": "review-with-coverage-and-archived-exceptions-v2", "checked_on": "2026-11-18",
             "user_authorized_exceptions": True, "authorization_record": policy["authorization"]["source"],
             "window": WINDOW, "review_watermark": "2026-11-15", "review_as_of": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
             "review_semantics": SEMANTICS, "selection_review_complete": True, "method_review_complete": False,
             "all_sources_exhaustive": False, "implementation_complete": False,
             "selection_policy": REL + "p2-selection-policy.json", "candidate_register": REL + "paper-register.json",
             "retrieval_receipts": receipt_refs, "source_reviews": source_refs, "exception_archive": REL + "exception-archive.json",
             "previous_review_state": PRIOR, "previous_review_state_sha256": sha256((ROOT / "docs" / PRIOR).read_bytes()).hexdigest(),
             "next_scan_start_with_overlap": "2026-11-14", "exception_reopening_policy": "new evidence only; no automatic retries",
             "coverage_scope": {"tracks": list(TRACKS), "recall_modes": list(MODES), "official_sources": declared, "counts": counts,
             "limitations": ["Selection screening plus protected primary-source review, not verification or implementation of every method.",
                             "Containing Nov16 Actions captures and actual split-query replacements; no all-web or all-institution historical exhaustiveness.",
                             "Original first publication, later revision, source discovery and review date are distinct; outside-window date filtering is not method review.",
                             "High-cost full experiments are review DONE/not reproduced; no training, GPU runs or executable evolve promotion.",
                             "Official sources have per-record and pagination/date exceptions archived with actual attempts; no access failure means no-paper inference."]}}
    write(AUDIT / "closed-watermark-proposal.json", state)
    write(AUDIT / "review-inventory.json", {"schema_version": 1, "window": WINDOW, "counts": counts,
           "candidate_review_complete": True, "review_watermark_advanced": advance, "all_sources_exhaustive": False})
    if advance:
        path = ROOT / "docs/paper-discovery-watermark.json"
        previous = path.read_bytes()
        if read(path)["review_watermark"] not in {"2026-11-09", "2026-11-15"}:
            raise ValueError("unrelated current watermark")
        write(path, state)
        errors = audit_review_watermark(ROOT)
        if errors:
            path.write_bytes(previous)
            raise ValueError("; ".join(errors))
        ledger_path = ROOT / "docs/paper-discovery-ledger.json"
        ledger = read(ledger_path)
        entry = {"schema_version": 1, "batch": BATCH, "date": "2026-11-18", "window": WINDOW,
                 "scope_kind": "bounded-review-reconciliation", "source_artifact": REL + "README.md",
                 "delivery_status": "review_complete_implementation_separate", "selected_scope_complete": True,
                 "all_sources_exhaustive": False, "review_watermark_advanced": True,
                 "review_watermark": {"before": "2026-11-09", "after": "2026-11-15"},
                 "review_semantics": SEMANTICS, "counts": counts, "candidates": list(primary.values())}
        existing = next((b for b in ledger["batches"] if b["batch"] == BATCH), None)
        if existing is not None and existing != entry:
            raise ValueError("refusing to replace different completed decisions")
        if existing is None:
            ledger["batches"].append(entry)
            write(ledger_path, ledger)
        versions_path = ROOT / "docs/paper-discovery-versions.json"
        versions = read(versions_path)
        observed_versions = {r["arxiv_id"]: r for r in versions["papers"]}
        for identity, review in primary.items():
            before = observed_versions.get(identity)
            if before and before["revision"] > review["revision"]:
                continue
            observed_versions[identity] = {
                "arxiv_id": identity, "revision": review["revision"], "reviewed_at": "2026-11-18",
                "metadata_sha256": review["metadata_sha256"], "review_scope": "bounded_original_revision_evidence",
                "review_artifact": review["review_artifact"], "algorithm_acceptance_inferred": False,
                "implementation_acceptance": "not_upgraded_by_review",
                "source_evidence": [{"url": review["source_url"], "sha256": review["source_sha256"]}]}
        versions["papers"] = list(observed_versions.values())
        versions["reviewed_at"] = "2026-11-18"
        versions["coverage"] = (
            f"Only {len(versions['papers'])} explicitly observed/reviewed version baselines. "
            "Historical scopes and source evidence remain in the referenced review artifacts and Git history. "
            "The Nov15 closeout pins 72 necessary original-source decisions, including six explicitly protected revisions. "
            "None implies whole-article verification, implementation or GPU acceptance. Missing versions are never assumed v1."
        )
        write(versions_path, versions)
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--advance", action="store_true")
    print(json.dumps(build(advance=parser.parse_args().advance), ensure_ascii=False))
