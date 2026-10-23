#!/usr/bin/env python3
"""Freeze bounded Oct23 sources and pending component scope; never claim closure.

No network, model execution, metric edits, runtime registration or watermark
mutation. Duplicate batches are rejected before writing any output.
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
BATCH = "2026-10-23-priority-components"
AUDIT_REL = Path("docs/research-audits/oct23-priority-components")
BASELINE_REL = Path("docs/research-audits/oct22-bulletin-components/source-coverage.json")
CATEGORIES = {"cs.AI", "cs.CL", "cs.CV", "cs.IR", "cs.LG", "cs.RO", "cs.SD", "eess.AS"}
COMPONENT_KEYS = {"gemma-priority-protocol", "openattention", "moezip", "aopd", "gift", "pair", "jev-dlc", "rkl-policy-distillation"}
REFERENCE_KEYS = {"onelatent"}
SELECTED = {
    "gemma-priority-protocol": ("foundation-models", "2609.30716"),
    "openattention": ("foundation-models", "2610.30951"),
    "moezip": ("foundation-models", "2610.30206"),
    "aopd": ("post-training", "2610.31563"),
    "gift": ("post-training", "2610.30796"),
    "pair": ("recommendation", "2610.30941"),
    "jev-dlc": ("foundation-models", "2610.31521"),
    "onelatent": ("recommendation", "2610.30675"),
    "rkl-policy-distillation": ("foundation-models", "2610.30844"),
}
TRACKS = {"foundation-models": "foundation-model", "post-training": "post-training",
          "recommendation": "recommendation"}
VERIFIED_PRIORITY_ORGANIZATIONS = {"gemma-priority-protocol": ["Google"],
                                   "rkl-policy-distillation": ["Google"]}
GOOGLE_DECISIONS = {
    "regional-policies-for-memory-tiering-systems": {
        "decision": "outside_topic_scope", "review_done": True,
        "reason": "REGENT is virtual-address-space memory tiering, not an accepted LLM/recommendation/agent algorithm. Official DIMES program lists first author Hayden Coffey at UW-Madison. Exact first public timestamp not established; no Oct23-first-publication claim.",
        "primary_source": "https://dimes.ws/program/", "first_publication_date": None},
    "%CF%80-flux-tuning-of-quantum-paramagnetism-in-the-triangular-lattice-hubbard-model": {
        "decision": "outside_topic_scope", "review_done": True,
        "reason": "Quantum condensed-matter physics; not in the accepted research tracks.",
        "first_publication_date": None},
    "stakes-adaptive-verification-and-origin-traced-rollback-in-autonomous-agent-workflows": {
        "decision": "archived_source_exception", "review_done": True,
        "full_text_review_done": False, "blocking": False, "automatic_retry": False,
        "reason": "Official TDC12058 metadata dates the defensive publication to Oct8. Linked full text returned403/HTML, not a valid PDF. Method and experimental claims are not declared fully reviewed and no implementation is invented.",
        "primary_source": "https://www.tdcommons.org/dpubs_series/12058/",
        "unavailable_full_text": "https://www.tdcommons.org/cgi/viewcontent.cgi?article=13422&context=dpubs_series",
        "first_publication_date": "2026-10-08", "exact_first_publication_timestamp": None},
    "words-speak-louder-than-order-a-behavioral-evaluation-of-gemma-4": {
        "decision": "selected_historical_backfill", "key": "gemma-priority-protocol",
        "review_done": True, "first_publication_date": "2026-09-25",
        "exact_first_publication_timestamp": "2026-09-25T02:43:40Z",
        "primary_source": "https://arxiv.org/abs/2609.30716v1",
        "reason": "Google author affiliation verified in full-text author block; bounded external-prediction protocol, not new model inference."},
    "nature-of-the-bosonic-edge-phase-in-a-double-quantum-spin-hall-insulator": {
        "decision": "outside_topic_scope", "review_done": True,
        "reason": "Quantum condensed-matter physics; not in the accepted research tracks.",
        "first_publication_date": None},
}
ADDITIONAL_DISPOSITIONS = [
    {"id": "2610.30423", "title": "When Agentic Retrieval Fails Silently: Framework and Production Evidence from a Creative AI Assistant",
     "source_url": "https://arxiv.org/html/2610.30423v1", "decision": "not_selected_under_industrial_evidence_gate",
     "review_done": True, "automatic_retry": False, "automatic_implementation_queue": False,
     "reason": "Adobe LARA is an observational production stratification/attribution framework. A controlled quantified online A/B result or qualifying full-traffic comparison was not established; production observation alone does not waive the industrial implementation gate."},
    {"id": "2610.30154", "title": "baseVultra: Compact Nonlinear Recurrence with Reallocated Capacity",
     "source_url": "https://arxiv.org/abs/2610.30154v1", "decision": "archived_identity_date_exception",
     "review_done": True, "full_text_review_done": False, "blocking": False,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "reason": "Observed Oct23 bulletin ID conflicts with the linked v1 page reporting Aug23. Identity/date conflict is archived, not forced into today's first-publication count or a new implementation."},
    {"id": "2610.30920", "title": "DConstrain: Compiling Context-Parameterized Transitions for Diffusion Language Model Constrained Decoding",
     "source_url": "https://arxiv.org/html/2610.30920v1", "decision": "affiliation_unconfirmed",
     "verified_priority_organizations": None, "full_text_review_done": False, "blocking": False,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "reason": "Targeted HTML author block unavailable. Google/Meta collaboration remains unknown, not a negative affiliation finding."},
    {"id": "2610.30934", "title": "Verbalizing Activation Differences with Natural Language Autoencoders",
     "source_url": "https://arxiv.org/html/2610.30934v1", "decision": "affiliation_unconfirmed",
     "verified_priority_organizations": None, "full_text_review_done": False, "blocking": False,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "reason": "Targeted HTML returned author names but no explicit institution. Google/Meta collaboration remains unknown, not a negative affiliation finding."},
    {"id": "2610.30880", "title": "One Teacher, Many Views: Reducing Reference Sensitivity in On-Policy Self-Distillation",
     "source_url": "https://arxiv.org/html/2610.30880v1", "decision": "not_reproduced_high_cost",
     "status": "deferred", "review_done": True, "original_published_at": "2026-10-22T07:59:48Z",
     "first_author": "Khouloud Saadi", "first_author_affiliation": "KAUST",
     "code": None, "code_status": "not_found_in_reviewed_primary_sources", "code_license": None,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "cost_assessment": {"source_url": "https://arxiv.org/html/2610.30880v1", "section": "Computational Cost / Table6",
         "available_resource": "One NVIDIA A100 or A30, or local Mac", "scale": "K=4 partial views; authors report4xA10080GB and1h36 for100steps", "measurement_owner": "authors, not local run"},
     "reason": "MCPD probability-mean multiview distillation reviewed; full training exceeds the single-device affordable scope. Review DONE, not reproduced, no automatic retry."},
    {"id": "2610.30351", "title": "Route-and-Generate: KL-Regularized Router Improvement for Reasoning Routing in LLMs",
     "source_url": "https://arxiv.org/html/2610.30351v1", "decision": "not_selected_method_ambiguity",
     "review_done": False, "blocking": False, "original_published_at": "2026-10-21T19:09:04Z",
     "first_author_affiliation": "Hanoi University of Science and Technology", "code": None,
     "code_status": "not_found_in_reviewed_primary_sources", "code_license": None,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "reason": "Router closed-form KL mechanism reviewed, but the format-conditioned mean is undefined for n_f=0 and author code was not found. Method ambiguity remains unresolved; no completed faithful reproduction claimed."},
    {"id": "2610.30167", "title": "IRAH: Hierarchical Agentic Tree Search for Retrieval Pipeline Optimization",
     "source_url": "https://arxiv.org/html/2610.30167v1", "decision": "deferred_not_selected",
     "review_done": False, "blocking": False, "original_published_at": "2026-10-16T17:03:17Z",
     "first_author_affiliation": "University of Virginia; work during Capital One internship", "code": None,
     "code_status": "not_verified", "code_license": None,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "reason": "Defining method requires LLM reflection mutation, two-stage UCT and offline meta-learned warm start. No heuristic stand-in or unmeasured high-cost claim; not selected in this fixed batch."},
    {"id": "2610.31401", "title": "HERD: Harness-Evolving Recursive Distillation for Continual Learning",
     "source_url": "https://arxiv.org/html/2610.31401v1", "decision": "source_unresolved_not_selected",
     "review_done": False, "blocking": False, "original_published_at": "2026-10-22T15:03:20Z",
     "first_author_affiliation": "Monash University", "code": "https://github.com/a1exsun/HERD",
     "observed_main_revision_not_paper_revision": "3ff1cf03d7a34565bcdbd510fae09aed7971286a",
     "paper_code_branch": "arr", "paper_code_revision": None, "code_license": None,
     "automatic_retry": False, "automatic_implementation_queue": False,
     "cost_assessment": {"source_url": "https://arxiv.org/html/2610.31401v1", "scale": "Qwen3.5-4B,25stages,32x32records per stage; authors report10723training seconds", "measurement_owner": "authors, not local run", "available_resource": "One NVIDIA A100 or A30, or local Mac"},
     "reason": "Main README says paper code is on arr branch, which was not retrieved. Main commit is not relabelled the paper revision; no implementation or full-source closure claimed."},
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def identity(value: str) -> str:
    match = re.fullmatch(r"(\d{4}\.\d{4,5})(?:v\d+)?", value)
    require(match is not None, f"invalid arXiv identity: {value}")
    return match.group(1)


def timestamp(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None, "timezone required")
    return result


def validate_capture(receipts: list[dict]) -> list[dict]:
    pages = [p for p in receipts if p["kind"] == "arxiv"]
    require(len(pages) == 8 and {p["source"] for p in pages} == CATEGORIES,
            "exactly eight distinct arXiv categories required")
    for page in pages:
        require(page.get("status") == "retrieved" and page.get("parse_complete") is True
                and page.get("announced_on") == "2026-10-23", "complete actual Oct23 announcements required")
        records = page.get("records", [])
        require(page.get("expected_entries") == page.get("parsed_entries") == len(records),
                "category entry totals mismatch")
        require(len({r["id"] for r in records}) == len(records), "duplicate category version")
        sections = page.get("sections", [])
        require(len(sections) == 3 and {s["kind"] for s in sections} == {"new", "cross-list", "replacement"},
                "all three sections required")
        counts = Counter(r["entry_kind"] for r in records)
        require(all(s["shown"] == s["expected"] == counts[s["kind"]] for s in sections),
                "section counts mismatch")
        require(re.fullmatch(r"[0-9a-f]{64}", page.get("sha256", "")) is not None, "page SHA256 required")
        timestamp(page["checked_at"])
        for row in records:
            identity(row["id"])
    return pages


def directory_deltas(receipts: list[dict], supplied: list[dict]) -> list[dict]:
    require(len(supplied) == 3 and {d["organization"] for d in supplied} == {"Google", "Meta", "Google DeepMind"},
            "three distinct priority organization deltas required")
    results = []
    for original in supplied:
        delta = deepcopy(original)
        rows = [r for r in receipts if r["kind"] == "official" and r["source"] == delta["organization"]]
        retrieved = [r for r in rows if r["status"] == "retrieved"]
        require(len(rows) == delta["attempted_pages"] and len(retrieved) == delta["retrieved_pages"],
                "directory receipt count mismatch")
        known = bool(rows) and len(rows) == len(retrieved)
        delta.update(all_sources_exhaustive=False, delta_known=known,
                     status="bounded_directory_difference_checked" if known else "source_unavailable_not_zero_delta",
                     page_receipts=[{k: v for k, v in r.items() if k != "records"} for r in rows])
        if not known:
            delta.update(new_directory_urls=None, changed_records=None)
        results.append(delta)
    return results


def google_dispositions(deltas: list[dict]) -> list[dict]:
    google = next(row for row in deltas if row["organization"] == "Google")
    if not google["delta_known"]:
        return []
    result = []
    for row in google["new_directory_urls"]:
        slug = row["url"].rstrip("/").split("/")[-1]
        require(slug in GOOGLE_DECISIONS, f"new Google URL requires explicit review: {row['url']}")
        result.append({**row, **deepcopy(GOOGLE_DECISIONS[slug]),
                       "directory_new_url_not_first_publication": True})
    return result


def build_reports(receipts: list[dict], baseline: dict, supplied: list[dict],
                  catalog: dict, raw_sha256: str) -> tuple[dict, dict, dict]:
    pages = validate_capture(receipts)
    current = {r["id"] for p in pages for r in p["records"]}
    old = {version for versions in baseline["bulletin_ids_by_category"].values() for version in versions}
    current_ids, old_ids = {identity(v) for v in current}, {identity(v) for v in old}
    baseline_end = max(baseline["retrieval_receipts"], key=lambda r: timestamp(r["checked_at"]))["checked_at"]
    observed = {}
    for page in pages:
        for row in page["records"]:
            entry = observed.setdefault(identity(row["id"]), {"versions": set(), "categories": set(), "kinds": set()})
            entry["versions"].add(row["id"])
            entry["categories"].add(page["source"])
            entry["kinds"].add(row["entry_kind"])
    selected = []
    for key, (domain, paper_id) in SELECTED.items():
        require(key in catalog, f"selected catalog record missing: {key}")
        item = catalog[key]
        require(item["domain"] == domain and paper_id in item["paper_url"], "selected catalog identity mismatch")
        historical = key == "gemma-priority-protocol"
        require(historical or paper_id in observed, f"selected identity absent from actual bulletin: {key}")
        evidence = observed.get(paper_id, {"versions": [], "categories": [], "kinds": []})
        component = key in COMPONENT_KEYS
        full_status = item.get("full_experiment_status", "not_reproduced_high_cost")
        selected.append({"id": paper_id, "key": key, "domain": domain, "title": item["title"],
            "paper_url": item["paper_url"], "detail_path": item["detail_path"], "priority": item["priority"],
            "first_author": item["first_author"], "first_author_affiliation": item["first_author_affiliation"],
            "verified_priority_organizations": VERIFIED_PRIORITY_ORGANIZATIONS.get(key, []),
            "original_published_at": item["published_at"],
            "intake_class": "historical-backfill" if historical else "new-to-repository-recent-first-publication",
            "first_publication_after_baseline_capture": timestamp(item["published_at"]) > timestamp(baseline_end),
            "observed_versions": sorted(evidence["versions"]), "bulletin_categories": sorted(evidence["categories"]),
            "bulletin_entry_kinds": sorted(evidence["kinds"]),
            "status": "accepted-unimplemented" if component else "deferred",
            "implementation_status": "component_validation_pending" if component else "deferred_high_cost",
            "delivery_status": "pending_component_verification" if component else "review_done_not_reproduced",
            "component_implemented": False, "component_accepted": False, "review_done": not component,
            "full_experiment_review_done": True, "full_experiment_status": full_status,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": item.get("requires_gpu_validation", False),
            "cost_assessment": {"source_url": item["paper_url"].replace("/abs/", "/html/"),
                "basis": "named method/resource passages and official author release; not measured complete-run time",
                "scale": item.get("deferral_reason", item["summary"]),
                "available_resource": "One NVIDIA A100 or A30, or local Mac"}})
    deltas = directory_deltas(receipts, supplied)
    directory_reviews = google_dispositions(deltas)
    counts = {"selected_papers": len(selected), "components_pending_verification": len(COMPONENT_KEYS),
        "reference_only_review_done": len(REFERENCE_KEYS), "historical_backfill": 1,
        "category_entries_including_crosslists_and_replacements": sum(len(p["records"]) for p in pages),
        "unique_bulletin_identities": len(current_ids),
        "snapshot_added_base_identities_not_new_paper_count": len(current_ids-old_ids),
        "snapshot_retained_base_identities": len(current_ids & old_ids),
        "snapshot_removed_base_identities": len(old_ids-current_ids),
        "snapshot_added_version_strings_not_revision_count": len(current-old),
        "snapshot_removed_version_strings": len(old-current),
        "new_section_unique_identities_not_exact_first_publication_count": sum("new" in x["kinds"] for x in observed.values()),
        "section_entry_counts": dict(Counter(r["entry_kind"] for p in pages for r in p["records"])),
        "selected_first_publication_after_baseline_capture": sum(x["first_publication_after_baseline_capture"] for x in selected),
        "google_directory_added_urls_not_new_paper_count": len(directory_reviews)}
    common = {"schema_version": 1, "batch": BATCH, "delivery_status": "pending_component_verification",
              "all_sources_exhaustive": False, "review_watermark_advanced": False}
    scope = {**common, "papers": selected, "fixed_component_keys": sorted(COMPONENT_KEYS),
             "reference_only_keys": sorted(REFERENCE_KEYS), "selected_scope_complete": False,
             "official_new_directory_dispositions": directory_reviews,
             "additional_dispositions": deepcopy(ADDITIONAL_DISPOSITIONS)}
    coverage = {**common, "checked_on": "2026-10-23", "scope_kind": "bounded-priority-bulletin-components",
        "raw_capture_sha256": raw_sha256, "baseline": "../oct22-bulletin-components/source-coverage.json",
        "baseline_raw_sha256": baseline["raw_capture_sha256"], "baseline_last_checked_at": baseline_end,
        "source_check_window_utc": {"first_checked_at": min(r["checked_at"] for r in receipts),
                                    "last_checked_at": max(r["checked_at"] for r in receipts)},
        "actual_announced_on": "2026-10-23", "all_eight_bulletins_complete": True,
        "full_bulletin_full_text_review_complete": False,
        "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"}, "counts": counts,
        "added_base_identities_snapshot_only": sorted(current_ids-old_ids),
        "retained_base_identities": sorted(current_ids & old_ids),
        "added_version_identities": sorted(current-old), "removed_version_identities": sorted(old-current),
        "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in pages},
        "retrieval_receipts": [{k: v for k, v in r.items() if k != "records"} for r in receipts],
        "official_directory_deltas": deltas, "official_new_directory_dispositions": directory_reviews,
        "additional_dispositions": deepcopy(ADDITIONAL_DISPOSITIONS),
        "limitations": ["Complete eight-category announcement parsing is not full-text review of all bulletin identities.",
            "Snapshot identity/version additions are not first-publication or revision counts; selected v1 timestamps are separate.",
            "Google directory delta uses its last successful423-record capture, not the immediately previous unavailable capture. Five new URLs are not five new papers.",
            "Meta six pages and DeepMind nine pages are bounded directory comparisons, not global organization exhaustiveness.",
            "Failed directory retrieval must remain unknown/null, never a zero delta.",
            "Eight components remain pending frozen execution/integration evidence; one high-cost reference is review DONE, not implemented.",
            "Gemma is historical protocol/log reanalysis without new model inference; its full run is not relabelled high-cost without a cost basis.",
            "TDC unavailable full text is an archived nonblocking source exception, not a full-method approval.",
            "Global review watermark remains2026-10-15; no whole-window review closure."]}
    ledger = {"batch": BATCH, "date": "2026-10-23", "scope_kind": "bounded-priority-bulletin-components",
              "source_artifact": "research-audits/oct23-priority-components/README.md", "counts": counts,
              "delivery_status": "pending_component_verification", "all_sources_exhaustive": False,
              "review_watermark_advanced": False, "official_new_directory_dispositions": directory_reviews,
              "additional_dispositions": deepcopy(ADDITIONAL_DISPOSITIONS),
              "candidates": [{**row, "doc": row["detail_path"], "catalog_key": row["key"],
                  "catalog_detail": row["detail_path"], "track": TRACKS[row["domain"]],
                  "resolution": "component_pending_verification" if row["key"] in COMPONENT_KEYS else "not_reproduced_high_cost",
                  "review_artifact": "research-audits/oct23-priority-components/task-scope.json",
                  "full_text_review": {"scope": "selected-method-and-resource-review",
                      "read_scope": "defining algorithm/protocol, relevant experiment/resource passages, author release and affiliation",
                      "full_article_read": False},
                  "source_provenance": [{"source_url": row["paper_url"],
                      "source_kind": "primary-method-resource-affiliation-review",
                      "organization": row["first_author_affiliation"]}]
                      + [{"source_url": row["paper_url"].replace("/abs/", "/html/"),
                          "source_kind": "verified-paper-author-affiliation", "organization": org}
                         for org in row["verified_priority_organizations"]],
                  "reason": "限定组件等待独立冻结验收；不提前声明能力实现或完整论文复现。" if row["key"] in COMPONENT_KEYS
                            else "完整实验成本过高，不复现（审查 DONE），不自动重试。"} for row in selected]}
    return coverage, scope, ledger


def append_batch(ledger: dict, batch: dict) -> dict:
    require(not any(row["batch"] == BATCH for row in ledger["batches"]),
            "batch already exists; refuse overwriting subsequent acceptance")
    result = deepcopy(ledger)
    result["batches"].append(batch)
    return result


def write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


def build(directory: Path, root: Path = ROOT) -> dict:
    raw = (directory/"retrieval.json").read_bytes()
    baseline = json.loads((root/BASELINE_REL).read_text())
    supplied = [json.loads((directory/f"{name}-delta.json").read_text())
                for name in ("google", "meta", "google-deepmind")]
    catalog = {key: json.loads((root/f"src/auto_research/paper_specs/catalog/{domain}/{key}.json").read_text())
               for key, (domain, _) in SELECTED.items()}
    coverage, scope, batch = build_reports(json.loads(raw), baseline, supplied, catalog,
                                          hashlib.sha256(raw).hexdigest())
    ledger_path = root/"docs/paper-discovery-ledger.json"
    updated = append_batch(json.loads(ledger_path.read_text()), batch)
    write(root/AUDIT_REL/"source-coverage.json", coverage)
    write(root/AUDIT_REL/"task-scope.json", scope)
    write(ledger_path, updated)
    return coverage["counts"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_directory", type=Path)
    print(json.dumps(build(parser.parse_args().capture_directory), ensure_ascii=False))
