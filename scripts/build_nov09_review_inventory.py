"""Reconcile overlapping discovery captures without turning recall into review."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata
from xml.etree import ElementTree
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
PRIMARY_FILES = (
    "priority-primary-reviews.json", "industrial-primary-reviews.json", "additional-primary-reviews.json",
    "revision-primary-reviews.json", "supplemental-priority-reviews.json", "late-index-primary-reviews.json",
    "continued-primary-reviews.json", "tail-industrial-primary-reviews.json",
    "tail-method-primary-reviews.json", "tail-lateindex-primary-reviews.json",
    "continued-google-meta-reviews.json", "continued-google-meta-followup-reviews.json",
    "continued-industrial-reviews.json", "continued-late-tail-primary-reviews.json",
    "continued-method-primary-reviews.json", "continued-industrial-secondary-reviews.json",
    "continued-signal-primary-reviews.json", "continued-google-meta-third-pass-reviews.json",
)


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


def record_reviewed_versions(report: dict, reviewed: dict[str, dict], *, reviewed_at: date) -> None:
    """Prevent already verified revisions from reappearing in the scanner."""
    path = ROOT / "docs/paper-discovery-versions.json"
    payload = read(path)
    indices = {row["arxiv_id"]: i for i, row in enumerate(payload["papers"])}
    captures = {
        f"{r['run_id']}/{r['artifact_name']}/{r['file']}" for r in report["capture_receipts"]
    }
    for identity, review in reviewed.items():
        if Path(review["review_artifact"]).name != "revision-primary-reviews.json":
            continue
        previous_revision = review["previous_reviewed_revision"]
        idx = indices[identity]
        before = payload["papers"][idx]
        if (review["revision"] <= previous_revision
                or before["revision"] not in {previous_revision, review["revision"]}
                or not START <= local_day(review["updated"]) <= END
                or review["metadata_capture"] not in captures
                or any(not re.fullmatch(r"[0-9a-f]{64}", review[field])
                       for field in ("metadata_sha256", "source_sha256"))):
            raise ValueError(f"{identity}: invalid reviewed version baseline")
        after = {
            "arxiv_id": identity, "revision": review["revision"], "reviewed_at": reviewed_at.isoformat(),
            "metadata_sha256": review["metadata_sha256"],
            "review_scope": "bounded_original_revision_evidence",
            "algorithm_acceptance_inferred": False, "review_artifact": review["review_artifact"],
            "implementation_acceptance": "not_upgraded_by_review",
            "source_evidence": [{"url": review["source_url"], "sha256": review["source_sha256"]}],
        }
        if before["revision"] == after["revision"] and before != after:
            raise ValueError(f"{identity}: refusing to overwrite a different version review")
        payload["papers"][idx] = after
    payload["reviewed_at"] = reviewed_at.isoformat()
    payload["coverage"] = (
        f"Only {len(payload['papers'])} explicitly observed/reviewed version baselines. "
        "October15 additions distinguish bounded method/cost/correction, historical metadata triage and "
        "attempted-source exceptions. The November continuation updates 17 of those baselines with pinned "
        "original revision evidence. None implies whole-article or implementation acceptance. "
        "Missing versions are never assumed v1."
    )
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def date_scope_rows(artifact: dict, observed: dict[str, dict], *, as_of: str) -> set[str]:
    """Close a window boundary, never the paper's substantive review."""
    if artifact["capture_as_of"] != as_of or artifact["requested_window"] != {
        "start": START.isoformat(), "end": END.isoformat(),
    }:
        raise ValueError("date-scope receipt has a different window")
    cutoff = datetime.fromisoformat(artifact["prior_review_as_of"])
    selected = set(artifact["terminal_ids"])
    result = set()
    for record in artifact["records"]:
        identity = record["id"]
        if identity not in selected:
            continue
        row = observed[identity]
        dates = tuple(record[key] for key in ("published", "updated"))
        if (identity in result or record["disposition"] != "pre_window_v1_no_post_cutoff_signal"
                or record["window_scope_review_done"] is not True or record["substantive_review_done"] is not False
                or record["signals"] or record["revision"] != row["rank"][0]
                or dates != (row["published"], row["updated"])
                or any(datetime.fromisoformat(value.replace("Z", "+00:00")) > cutoff for value in dates)):
            raise ValueError(f"{identity}: invalid or stale date-scope decision")
        result.add(identity)
    if result != selected:
        raise ValueError("date-scope records do not cover their declared terminal IDs")
    return result


def metadata_scope_rows(artifact: dict, observed: dict[str, dict], priorities: dict[str, set],
                        receipt_hashes: dict[str, str]) -> set[str]:
    if artifact["terminal_window_scope_only"] is not True or artifact["fulltext_or_cost_inferred"] is not False:
        raise ValueError("scope-only evidence cannot claim full-text review or cost")
    if artifact["source_receipts"] != receipt_hashes:
        raise ValueError("scope-only metadata captures do not match the recall receipts")
    result = set()
    for record in artifact["records"]:
        identity = record["id"]
        row = observed[identity]
        if (identity in result or priorities[identity] or record["decision"] != "out_of_scope"
                or record["review_done"] is not True or record["fulltext_review_completed"] is not False
                or record["automatic_retry"] is not False or record["automatic_implementation_queue"] is not False
                or not all(record.get(key) for key in ("metadata_sha256", "title_witness", "abstract_witness", "reason"))
                or record["capture"] not in receipt_hashes
                or record["revision"] != row["rank"][0]
                or any(record[key] != row.get(key) for key in ("published", "metadata_sha256", "title"))
                or record["title_witness"].casefold() not in row["title"].casefold()
                or record["abstract_witness"].casefold() not in row["abstract"].casefold()):
            raise ValueError(f"{identity}: invalid or stale scope-only metadata")
        result.add(identity)
    return result


def review_scope_text(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def continued_overlap_scope(source_dir: Path, receipt_hashes: dict[str, str]) -> dict[str, dict]:
    """Accept only individually verified scope decisions pinned to captured metadata."""
    artifact = read(AUDIT / "continued-late-tail-triage.json")
    if (artifact["terminal_window_scope_only"] is not True or artifact["fulltext_or_cost_inferred"] is not False
            or artifact["source_receipts"] != receipt_hashes):
        raise ValueError("overlap scope artifact does not match the frozen captures")
    exclusions = {}
    payloads = {}
    seen = set()
    for record in artifact["records"]:
        identity = record["id"]
        if identity in seen or record["lane"] not in {"late_index", "end_of_day_tail"}:
            raise ValueError(f"{identity}: duplicate or invalid overlap scope record")
        seen.add(identity)
        if record["disposition"] != "exclude_from_window_scope":
            continue
        path = record["source_file"]
        if (not record["window_scope_review_done"] or record["fulltext_review_completed"]
                or record["institutional_priority_signals"] or not record["reason"] or not record["abstract_witness"]
                or receipt_hashes.get(path) != record["source_sha256"]):
            raise ValueError(f"{identity}: invalid overlap scope decision")
        if record["lane"] == "late_index":
            if path not in payloads:
                payload = read(source_dir / path)
                payloads[path] = {canonical_arxiv_id(r["arxiv_id"]): r for r in
                                  payload.get("candidates", payload.get("papers", []))}
            source = payloads[path][identity]
            revision = source.get("revision")
            if revision is None:
                revision = int(source["arxiv_id"].split("v")[-1]) if "v" in source["arxiv_id"] else 1
            if revision != record["revision"]:
                raise ValueError(f"{identity}: scope decision uses a different captured revision")
            verify_overlap_scope_text(record, source)
        elif path != "nov09-tail-all-categories.atom":
            raise ValueError(f"{identity}: invalid tail source")
        exclusions[identity] = record
    return exclusions


def verify_overlap_scope_text(record: dict, source: dict) -> None:
    title, abstract = map(review_scope_text, (source["title"], source["abstract"]))
    fingerprint = sha256(f"{title}\0{abstract}".encode()).hexdigest()
    if (record["metadata_sha256"] != fingerprint or review_scope_text(record["title"]) != title
            or source["published"] != record["published"] or source["updated"] != record["updated"]
            or review_scope_text(record["abstract_witness"]) not in abstract):
        raise ValueError(f"{record['id']}: scope decision lacks matching title and abstract evidence")


def tail_inventory(source_dir: Path, reviewed: dict[str, dict], observed: dict[str, dict],
                   overlap_scope: dict[str, dict], *, as_of: str) -> dict:
    """Reconcile the supplemental Atom submission tail independently of the frozen captures."""
    artifact_path = AUDIT / "nov09-tail-source-receipt.json"
    artifact = read(artifact_path)
    response = artifact["source_response"]
    raw = (source_dir / "nov09-tail-all-categories.atom").read_bytes()
    if sha256(raw).hexdigest() != response["source_sha256"]:
        raise ValueError("tail Atom does not match its source receipt")
    start = datetime.fromisoformat(as_of)
    end = datetime.combine(END + timedelta(days=1), datetime.min.time(), tzinfo=SHANGHAI)
    if artifact["requested_tail_shanghai"] != {"after_exclusive": as_of, "before_exclusive": end.isoformat()}:
        raise ValueError("tail bounds do not match the frozen capture")
    feed = ElementTree.fromstring(raw)
    ns = {"a": "http://www.w3.org/2005/Atom", "o": "http://a9.com/-/spec/opensearch/1.1/"}
    entries = feed.findall("a:entry", ns)
    if (len(entries) != response["rows_received"] or len(entries) != response["total_results"]
            or int(feed.findtext("o:totalResults", namespaces=ns)) != len(entries)
            or int(feed.findtext("o:startIndex", namespaces=ns)) != 0):
        raise ValueError("tail Atom must contain the complete reported page")
    observed_tail = {}
    scope_excluded = []
    for entry in entries:
        published = entry.findtext("a:published", namespaces=ns)
        if not start < datetime.fromisoformat(published.replace("Z", "+00:00")) < end:
            continue
        identifier = entry.findtext("a:id", namespaces=ns).rsplit("/", 1)[-1]
        match = re.fullmatch(r"(2611\.\d{5})v(\d+)", identifier)
        title = " ".join(entry.findtext("a:title", namespaces=ns).split())
        if match is None or match[1] in observed_tail or match[1] in observed:
            raise ValueError(f"invalid, duplicate, or overlapping tail identity: {identifier}")
        observed_tail[match[1]] = (published, int(match[2]), title)
        if (record := overlap_scope.get(match[1])) is not None:
            if record["lane"] != "end_of_day_tail" or record["revision"] != int(match[2]):
                raise ValueError(f"{identifier}: stale tail scope decision")
            verify_overlap_scope_text(record, {"published": published, "title": title,
                                               "updated": entry.findtext("a:updated", namespaces=ns),
                                               "abstract": entry.findtext("a:summary", namespaces=ns)})
            scope_excluded.append(match[1])
    declared_tail = {
        row["id"]: (row["first_submission_utc"], row["revision"], row["title"]) for row in artifact["records"]
    }
    if (declared_tail != observed_tail or len(declared_tail) != artifact["exact_tail_unique_ids"]
            or len(declared_tail) != len(artifact["records"])):
        raise ValueError("tail inventory differs from the exact-date Atom rows")
    decided = []
    for identity, (published, revision, _) in observed_tail.items():
        review = reviewed.get(identity)
        if review and review["published"] == published and review["revision"] == revision:
            decided.append(identity)
    return {
        "receipt": artifact_path.name, "unique_identities": len(observed_tail),
        "primary_reviewed_ids": sorted(decided), "metadata_scope_only_excluded_ids": sorted(scope_excluded),
        "pending_ids": sorted(set(observed_tail) - set(decided) - set(scope_excluded)),
    }


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

    capture_hashes = {
        f"{r['run_id']}/{r['artifact_name']}/{r['file']}": r["artifact_sha256"] for r in receipts
    }
    late_scope = read(AUDIT / "late-index-scope.json")
    prior_register = docs / "research-audits/oct15-review-closure/paper-register.json"
    if (sha256(prior_register.read_bytes()).hexdigest() != late_scope["prior_register_sha256"]
            or read(prior_register)["review_as_of"] != late_scope["prior_review_as_of"]):
        raise ValueError("late-index scope uses the wrong prior review cutoff")
    if any(
        source["sha256"] != (
            capture_hashes[f"{source['run_id']}/{source['artifact_name']}/{source['file']}"]
            if "run_id" in source else sha256((source_dir / source["file"]).read_bytes()).hexdigest()
        ) for source in late_scope["sources"]
    ):
        raise ValueError("date-scope captures do not match their pinned sources")
    date_excluded = date_scope_rows(late_scope, rows, as_of=as_of)
    metadata_excluded = metadata_scope_rows(read(AUDIT / "abstract-scope-screen.json"), rows, priorities, capture_hashes)
    new_scope = metadata_scope_rows(read(AUDIT / "continued-in-window-scope.json"), rows, priorities, capture_hashes)
    if new_scope & (metadata_excluded | reviewed.keys()):
        raise ValueError("in-window scope exclusions overlap an existing decision")
    metadata_excluded |= new_scope
    overlap_hashes = capture_hashes | {f"llm-{r['month']}-replacement.json": r["source_sha256"] for r in replacements}
    overlap_hashes["nov09-tail-all-categories.atom"] = read(
        AUDIT / "nov09-tail-source-receipt.json",
    )["source_response"]["source_sha256"]
    overlap_scope = continued_overlap_scope(source_dir, overlap_hashes)
    late_metadata_excluded = {identity for identity, r in overlap_scope.items() if r["lane"] == "late_index"}
    if overlap_scope.keys() & (date_excluded | reviewed.keys()):
        raise ValueError("overlap scope exclusions overlap an existing decision")
    for identity in late_metadata_excluded:
        record, observed = overlap_scope[identity], rows[identity]
        if (priorities[identity] or record["revision"] != observed["rank"][0]
                or record["published"] != observed["published"] or local_day(record["published"]) >= START):
            raise ValueError(f"{identity}: stale or protected late metadata scope decision")
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
            if (PRIMARY_ID.fullmatch(identity) and identity not in statuses
                    and not decision_covers_version and identity not in date_excluded | late_metadata_excluded):
                overlap_ids.append(identity)
            continue
        if decision_covers_version:
            counts["new_primary_decisions"] += 1
        elif is_newer_known_revision:
            counts["newer_versions_pending"] += 1
            revision_rows.append([identity, latest_reviewed_version, version])
        elif identity in statuses:
            counts["existing_disposition"] += 1
        elif identity in metadata_excluded:
            counts["metadata_scope_only_excluded"] += 1
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

    tail = tail_inventory(source_dir, reviewed, rows, overlap_scope, as_of=as_of)
    routes_path = AUDIT / "continued-in-window-routing.json"
    route_artifact = read(routes_path)
    if (route_artifact["source_receipts"] != capture_hashes or route_artifact["terminal_decisions_created"] != 0
            or route_artifact["eligibility_or_cost_inferred"] is not False):
        raise ValueError("invalid title/abstract routing artifact")
    routes = {(r["id"], r["revision"]): r["route"] for r in route_artifact["records"]}
    if len(routes) != route_artifact["count"]:
        raise ValueError("duplicate title/abstract routes")
    remaining_routes = Counter(routes[identity, revision] for group in pending.values()
                               for identity, revision, _, _ in group)
    return {
        "schema_version": 1, "requested_window": {"start": START.isoformat(), "end": END.isoformat()},
        "as_of": as_of, "all_sources_exhaustive": False, "arxiv_recall_matrix_covered": True,
        "candidate_review_complete": not (pending or revision_rows or overlap_ids or tail["pending_ids"]),
        "review_watermark_advanced": False, "counts": {
            "raw_unique_identities": len(rows), "in_window_identities": sum(counts.values()),
            "late_index_or_missing_date_scope_triage_pending": len(overlap_ids),
            "late_index_date_scope_only_excluded": len(date_excluded),
            "late_index_metadata_scope_only_excluded": len(late_metadata_excluded),
            "post_capture_tail_identities": tail["unique_identities"],
            "post_capture_tail_review_pending": len(tail["pending_ids"]),
            "post_capture_tail_metadata_scope_only_excluded": len(tail["metadata_scope_only_excluded_ids"]),
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
        "post_capture_tail": tail,
        "scope_only_evidence": {
            "late_index": "late-index-scope.json", "in_window_metadata": "abstract-scope-screen.json",
            "continued_in_window_metadata": "continued-in-window-scope.json",
            "continued_overlap_metadata": "continued-late-tail-triage.json",
        },
        "in_window_title_abstract_routing": routes_path.name,
        "pending_in_window_counts_by_title_abstract_route": dict(sorted(remaining_routes.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--record-selected-reviews", action="store_true")
    parser.add_argument("--record-reviewed-versions-on", type=date.fromisoformat)
    args = parser.parse_args()
    reviewed = {}
    for filename in PRIMARY_FILES:
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
    if args.record_reviewed_versions_on:
        record_reviewed_versions(report, reviewed, reviewed_at=args.record_reviewed_versions_on)
    print(json.dumps(report["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
