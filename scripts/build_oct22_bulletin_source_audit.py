#!/usr/bin/env python3
"""Build the bounded Oct22 bulletin audit; never infer new papers from snapshot deltas.

No network, training, model loading, runtime evidence curation or watermark
mutation. Component acceptance remains pending until the separate frozen
GPU/integration gate is completed. Existing ledger batches are preserved.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
BATCH = "2026-10-22-bulletin-components"
AUDIT_REL = Path("docs/research-audits/oct22-bulletin-components")
BASELINE_REL = Path("docs/research-audits/oct22-priority-backfill/source-coverage.json")
CATEGORIES = {"cs.AI", "cs.CL", "cs.CV", "cs.IR", "cs.LG", "cs.RO", "cs.SD", "eess.AS"}
COMPONENT_KEYS = {"alps", "asteroid", "cord", "csd", "jev-multicorrect"}
REFERENCE_KEYS = {"aw0", "right-on-q", "finesid"}
VERIFIED_PRIORITY_ORGANIZATIONS = {"alps": ["Google"], "asteroid": ["Meta"], "right-on-q": ["Meta"]}
SELECTED = {
    "alps": ("foundation-models", "2610.30120"),
    "asteroid": ("agent-research", "2610.30105"),
    "cord": ("post-training", "2610.29965"),
    "csd": ("post-training", "2610.28895"),
    "jev-multicorrect": ("foundation-models", "2610.29217"),
    "aw0": ("multimodal-models", "2610.30136"),
    "right-on-q": ("foundation-models", "2610.29378"),
    "finesid": ("recommendation", "2610.29138"),
}
TRACKS = {"foundation-models": "foundation-model", "post-training": "post-training",
          "agent-research": "agent", "multimodal-models": "multimodal",
          "recommendation": "recommendation"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(value) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()


def identity(version: str) -> str:
    match = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v\d+)?", version)
    require(match is not None, f"invalid arXiv identity: {version}")
    return match.group(1)


def timestamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "UTC offset required for publication/capture time")
    return result


def validate_capture(receipts: list[dict]) -> list[dict]:
    pages = [p for p in receipts if p["kind"] == "arxiv"]
    require(len(pages) == 8 and {p["source"] for p in pages} == CATEGORIES,
            "exactly eight distinct arXiv categories required")
    for page in pages:
        require(page.get("status") == "retrieved" and page.get("parse_complete") is True
                and page.get("announced_on") == "2026-10-22",
                "actual complete October22 announcement receipts required")
        records = page.get("records", [])
        require(page.get("expected_entries") == page.get("parsed_entries") == len(records),
                "category entry totals do not match parsed records")
        require(len({r["id"] for r in records}) == len(records), "duplicate version within a category")
        sections = page.get("sections", [])
        require(len(sections) == 3 and {s["kind"] for s in sections} == {"new", "cross-list", "replacement"},
                "all three bulletin sections must be accounted for")
        observed = Counter(r["entry_kind"] for r in records)
        require(all(s["shown"] == s["expected"] == observed[s["kind"]] for s in sections),
                "bulletin section counts do not match records")
        for record in records:
            identity(record["id"])
        require(re.fullmatch(r"[0-9a-f]{64}", page["sha256"]) is not None,
                "source page SHA256 missing")
        timestamp(page["checked_at"])
    return pages


def directory_deltas(receipts: list[dict], supplied: list[dict]) -> list[dict]:
    require({d["organization"] for d in supplied} == {"Google", "Meta", "Google DeepMind"},
            "three priority directory reports required")
    result = []
    for original in supplied:
        delta = deepcopy(original)
        rows = [r for r in receipts if r.get("source") == delta["organization"] and r["kind"] == "official"]
        require(len(rows) == delta["attempted_pages"], "directory attempted-page receipt mismatch")
        successful = [r for r in rows if r["status"] == "retrieved"]
        require(len(successful) == delta["retrieved_pages"], "directory retrieved-page receipt mismatch")
        delta["all_sources_exhaustive"] = False
        delta["page_receipts"] = [{k: v for k, v in row.items() if k != "records"} for row in rows]
        if len(successful) != len(rows):
            delta.update(status="source_unavailable_not_zero_delta", new_directory_urls=None,
                         changed_records=None, delta_known=False)
        else:
            delta.update(status="bounded_directory_difference_checked", delta_known=True)
        result.append(delta)
    return result


def selected_scope(catalog: dict, observed: dict, baseline_end: str) -> list[dict]:
    rows = []
    for key, (domain, paper_id) in SELECTED.items():
        require(key in catalog, f"missing selected catalog record: {key}")
        item = catalog[key]
        require(item["domain"] == domain and paper_id in item["paper_url"], "selected paper/catalog identity mismatch")
        require(paper_id in observed and "new" in observed[paper_id]["entry_kinds"],
                f"selected paper absent from actual new-section bulletin: {key}")
        component = key in COMPONENT_KEYS
        row = {"id": paper_id, "key": key, "domain": domain, "title": item["title"],
            "paper_url": f"https://arxiv.org/abs/{paper_id}v1", "detail_path": item["detail_path"],
            "first_author": item["first_author"], "first_author_affiliation": item["first_author_affiliation"],
            "verified_coauthor_priority_organizations": VERIFIED_PRIORITY_ORGANIZATIONS.get(key, []),
            "priority": item["priority"], "original_published_at": item["published_at"],
            "announced_on": "2026-10-22", "intake_class": "newly_announced",
            "first_publication_after_baseline_capture": timestamp(item["published_at"]) > timestamp(baseline_end),
            "observed_versions": sorted(observed[paper_id]["versions"]),
            "bulletin_categories": sorted(observed[paper_id]["categories"]),
            "status": "accepted-unimplemented" if component else "deferred",
            "implementation_status": "component_validation_pending" if component else "deferred_high_cost",
            "delivery_status": "pending_gpu_and_integration" if component else "review_done_not_reproduced",
            "component_implemented": False, "component_accepted": False,
            "review_done": not component, "full_experiment_review_done": True,
            "full_experiment_status": "not_reproduced_high_cost",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": bool(item.get("requires_gpu_validation", False)),
            "cost_assessment": {"source_url": f"https://arxiv.org/html/{paper_id}v1",
                "basis": "paper method/resource sections and linked author release; not measured complete-run time",
                "scale": item.get("deferral_reason", item["summary"]),
                "available_resource": "One NVIDIA A100 or A30, or local Mac"}}
        require(not component or item.get("evaluation_tier") == "l1_mechanism", "components must stay L1")
        rows.append(row)
    return rows


def build_reports(receipts: list[dict], baseline: dict, supplied_deltas: list[dict], catalog: dict,
                  raw_sha256: str) -> tuple[dict, dict, dict]:
    pages = validate_capture(receipts)
    old_versions = {v for values in baseline["bulletin_ids_by_category"].values() for v in values}
    current_versions = {r["id"] for p in pages for r in p["records"]}
    current_ids, old_ids = {identity(v) for v in current_versions}, {identity(v) for v in old_versions}
    observed = {}
    for page in pages:
        for record in page["records"]:
            row = observed.setdefault(identity(record["id"]), {"versions": set(), "categories": set(), "entry_kinds": set(), "titles": set()})
            row["versions"].add(record["id"])
            row["categories"].add(page["source"])
            row["entry_kinds"].add(record["entry_kind"])
            row["titles"].add(record["title"])
    baseline_end = max(r["checked_at"] for r in baseline["retrieval_receipts"])
    papers = selected_scope(catalog, observed, baseline_end)
    counts = {"selected_papers": len(papers), "components_pending_gpu_and_integration": len(COMPONENT_KEYS),
        "reference_only_review_done": len(REFERENCE_KEYS), "metadata_updates": 1,
        "category_entries_including_crosslists_and_replacements": sum(len(p["records"]) for p in pages),
        "unique_bulletin_identities": len(current_ids),
        "snapshot_added_base_identities_not_new_paper_count": len(current_ids-old_ids),
        "snapshot_retained_base_identities": len(current_ids & old_ids),
        "snapshot_removed_base_identities": len(old_ids-current_ids),
        "snapshot_added_version_strings_not_revision_count": len(current_versions-old_versions),
        "snapshot_removed_version_strings": len(old_versions-current_versions),
        "new_section_unique_identities_not_exact_first_publication_count": sum("new" in r["entry_kinds"] for r in observed.values()),
        "crosslist_unique_identities": sum("cross-list" in r["entry_kinds"] for r in observed.values()),
        "replacement_unique_identities": sum("replacement" in r["entry_kinds"] for r in observed.values()),
        "selected_first_publication_after_baseline_capture": sum(r["first_publication_after_baseline_capture"] for r in papers)}
    counts["section_entry_counts"] = dict(Counter(r["entry_kind"] for p in pages for r in p["records"]))
    meta_id = "2610.22671"
    require(meta_id in observed and "replacement" in observed[meta_id]["entry_kinds"], "MemoProAgent replacement absent")
    require(len(observed[meta_id]["titles"]) == 1, "conflicting MemoProAgent replacement titles")
    meta = {"id": meta_id, "key": "proper-agent", "observed_title": next(iter(observed[meta_id]["titles"])),
            "observed_versions": sorted(observed[meta_id]["versions"]), "new_paper": False,
            "change": "existing proper-agent v2 title/source metadata update; no new runtime or evidence-tier upgrade"}
    scope = {"schema_version": 1, "batch": BATCH, "delivery_status": "pending_gpu_and_integration",
             "papers": papers, "fixed_component_keys": sorted(COMPONENT_KEYS),
             "reference_only_keys": sorted(REFERENCE_KEYS), "metadata_updates": [meta],
             "selected_scope_complete": False, "all_sources_exhaustive": False}
    coverage = {"schema_version": 1, "checked_on": "2026-10-22", "scope_kind": "bounded-bulletin-selected-components",
        "batch": BATCH, "delivery_status": "pending_gpu_and_integration", "raw_capture_sha256": raw_sha256,
        "baseline": "../oct22-priority-backfill/source-coverage.json",
        "baseline_raw_sha256": baseline["raw_capture_sha256"], "baseline_last_checked_at": baseline_end,
        "source_check_window_utc": {"first_checked_at": min(r["checked_at"] for r in receipts),
                                    "last_checked_at": max(r["checked_at"] for r in receipts)},
        "actual_announced_on": "2026-10-22", "all_eight_bulletins_complete": True,
        "all_sources_exhaustive": False, "full_bulletin_full_text_review_complete": False,
        "review_watermark_advanced": False, "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"},
        "counts": counts,
        "added_base_identities_snapshot_only": sorted(current_ids-old_ids),
        "retained_base_identities": sorted(current_ids & old_ids),
        "added_version_identities": sorted(current_versions-old_versions),
        "removed_version_identities": sorted(old_versions-current_versions),
        "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in pages},
        "bulletin_category_identity_sha256": {p["source"]: digest([r["id"] for r in p["records"]]) for p in pages},
        "retrieval_receipts": [{k: v for k, v in r.items() if k != "records"} for r in receipts],
        "official_directory_deltas": directory_deltas(receipts, supplied_deltas),
        "limitations": [
            f"{len(current_ids)} bulletin identities and the {len(current_ids-old_ids)} added-base snapshot difference are not a new-paper count or full-text approvals.",
            "The new section, cross-listing and replacements overlap across categories; exact v1 dates are verified only for selected papers.",
            "Google/Meta directory retrieval failed: deltas unknown (null), never zero; DeepMind is a bounded successful directory comparison only.",
            "Eight selected papers plus one existing-paper metadata update are not whole-bulletin or whole-window review closure.",
            "Five L1 components are pending frozen GPU/integration acceptance; three high-cost references are review DONE, not implementations.",
            "Global review watermark remains 2026-10-15."]}
    ledger = {"batch": BATCH, "date": "2026-10-22", "scope_kind": "bounded-bulletin-selected-components",
        "source_artifact": "research-audits/oct22-bulletin-components/README.md", "counts": counts,
        "delivery_status": "pending_gpu_and_integration", "all_sources_exhaustive": False,
        "review_watermark_advanced": False, "metadata_updates": [meta], "candidates": []}
    for row in papers:
        component = row["key"] in COMPONENT_KEYS
        ledger["candidates"].append({**row, "doc": row["detail_path"], "catalog_key": row["key"],
            "catalog_detail": row["detail_path"], "track": TRACKS[row["domain"]],
            "resolution": "component_pending_gpu_and_integration" if component else "not_reproduced_high_cost",
            "reason": "已接受低成本L1组件范围，尚待冻结GPU/统一集成验收；不提前记已实现或交付DONE。完整实验高成本不复现。" if component else "成本过高，不复现（审查 DONE）；只保留方法、原图和来源，不生成runtime或能力指标。",
            "review_artifact": "research-audits/oct22-bulletin-components/task-scope.json",
            "full_text_review": {"scope": "full-text", "read_scope": "defining method, relevant resources/costs, author code and key figure",
                                 "full_article_read": False},
            "source_provenance": [{"source_url": row["paper_url"], "source_kind": "primary-method-and-cost-review",
                                   "organization": row["first_author_affiliation"]}]
                + [{"source_url": row["paper_url"].replace("/abs/", "/html/"),
                    "source_kind": "verified-paper-coauthor-affiliation", "organization": org}
                   for org in row["verified_coauthor_priority_organizations"]]})
    return coverage, scope, ledger


def append_batch(ledger: dict, batch: dict) -> dict:
    result = deepcopy(ledger)
    require(not any(b["batch"] == BATCH for b in result["batches"]),
            "batch already exists; do not overwrite a later acceptance decision")
    result["batches"].append(batch)
    return result


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def build(directory: Path, root: Path = ROOT) -> dict:
    raw_bytes = (directory/"retrieval.json").read_bytes()
    receipts = json.loads(raw_bytes)
    baseline = json.loads((root/BASELINE_REL).read_text())
    deltas = [json.loads((directory/f"{name}-delta.json").read_text()) for name in ("google", "meta", "google-deepmind")]
    catalog = {key: json.loads((root/f"src/auto_research/paper_specs/catalog/{domain}/{key}.json").read_text())
               for key, (domain, _) in SELECTED.items()}
    coverage, scope, batch = build_reports(receipts, baseline, deltas, catalog, hashlib.sha256(raw_bytes).hexdigest())
    ledger_path = root/"docs/paper-discovery-ledger.json"
    combined = append_batch(json.loads(ledger_path.read_text()), batch)
    write(root/AUDIT_REL/"source-coverage.json", coverage)
    write(root/AUDIT_REL/"task-scope.json", scope)
    write(ledger_path, combined)
    return coverage["counts"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.capture_directory), ensure_ascii=False))
