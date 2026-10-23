"""Record an unchanged Oct23 bulletin recheck and four bounded overlap deliveries.

Offline generation only. Source failures are unknown, not zero additions; this
does not advance the global review watermark or overwrite an accepted batch.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from build_oct23_source_audit import directory_deltas, identity, require, timestamp, validate_capture, write

ROOT = Path(__file__).resolve().parents[1]
BATCH = "2026-10-24-overlap-components"
AUDIT_REL = Path("docs/research-audits/oct24-overlap-components")
SELECTED = {
    "physical-engineering-exam": ("agent-research", "2610.30537"),
    "ttr-compressor": ("foundation-models", "2610.31574"),
    "userarena-optd": ("post-training", "2610.30932"),
    "moer": ("post-training", "2610.30873"),
}
TRACKS = {"agent-research": "agent", "foundation-models": "foundation-model", "post-training": "post-training"}
ADDITIONAL_DISPOSITIONS = [
    {"id": "2610.30933", "title": "ReflectPO", "source_url": "https://arxiv.org/html/2610.30933v1",
     "original_published_at": "2026-10-22T08:54:24Z", "first_author": "Rumei Li",
     "first_author_affiliation": "Meituan, China", "decision": "not_reproduced_high_cost",
     "review_done": True, "full_experiment_status": "not_reproduced_high_cost",
     "automatic_retry": False, "automatic_implementation_queue": False,
     "code": None, "code_status": "not_found_in_reviewed_primary_sources", "upstream_revision": None,
     "code_license": None, "read_scope": "defining algorithm and Appendix A.1 resources, not a full-method implementation approval",
     "cost_assessment": {"source": "Appendix A.1", "scale": "8xH800141GB; Qwen3-4B/8B;3epochs;8original trajectories/up to128contrast and64recovery;24576response cap;DeepSeek-V4-Pro guide",
        "available_resource": "One NVIDIA A100 or A30, or local Mac", "measurement_owner": "authors, not local run"},
     "reason": "完整实验成本过高，不复现（审查 DONE）。不能用普通奖励std替代canonical prefix-tree全局advantage std，不能只mask而不移除hint；zero-sigma边界未确认，不虚构组件。"},
    {"id": "2610.31276", "title": "RIPPLE", "source_url": "https://arxiv.org/html/2610.31276v1",
     "original_published_at": "2026-10-22T13:45:33Z", "first_author": "Jingxuan Xu",
     "first_author_affiliation": "National University of Singapore, Singapore", "decision": "not_reproduced_high_cost",
     "review_done": True, "full_experiment_status": "not_reproduced_high_cost",
     "automatic_retry": False, "automatic_implementation_queue": False,
     "code": None, "code_status": "not_found_in_reviewed_primary_sources", "upstream_revision": None,
     "code_license": None, "read_scope": "defining recovery/attribution algorithm and resource setup, not full capability reproduction",
     "cost_assessment": {"source": "paper experiment and method passages", "scale": "Qwen3.5-27B actor;SFT/learned GRM recovery teacher;frozen semantic consistency/attribution judge;150tool turns;3seeds and4repository benchmarks;exactGPU count not disclosed",
        "available_resource": "One NVIDIA A100 or A30, or local Mac", "measurement_owner": "authors, not local run"},
     "reason": "完整实验成本过高，不复现（审查 DONE）。学习式恢复教师与语义归因不可替换成规则；stage-sign gate只路由已有优势，不能给平奖励零优势组伪造学习信号。"},
]


def build_reports(receipts, baseline, supplied, catalog, raw_sha256, independent_receipts=None):
    pages = validate_capture(receipts)
    current = {r["id"] for p in pages for r in p["records"]}
    previous = {v for rows in baseline["bulletin_ids_by_category"].values() for v in rows}
    require(current == previous, "this overlap audit expects an unchanged actual Oct23 bulletin")
    require({p['source']: [r['id'] for r in p['records']] for p in pages} == baseline['bulletin_ids_by_category'],
            'unchanged bulletin requires each category version/order to match, not only their union')
    observed = {}
    for page in pages:
        for item in page["records"]:
            row = observed.setdefault(identity(item["id"]), {"versions": set(), "categories": set(), "kinds": set()})
            row["versions"].add(item["id"])
            row["categories"].add(page["source"])
            row["kinds"].add(item["entry_kind"])
    baseline_end = max(baseline["retrieval_receipts"], key=lambda r: timestamp(r["checked_at"]))["checked_at"]
    selected = []
    for key, (domain, paper_id) in SELECTED.items():
        item = catalog[key]
        require(item["domain"] == domain and item["paper_url"] == f"https://arxiv.org/abs/{paper_id}v1", "catalog paper identity")
        require(paper_id in observed and timestamp(item["published_at"]) <= timestamp(baseline_end), "overlap not new first publication")
        source = observed[paper_id]
        selected.append({"id": paper_id, "key": key, "domain": domain, "title": item["title"],
            "paper_url": item["paper_url"], "detail_path": item["detail_path"], "priority": item["priority"],
            "first_author": item["first_author"], "first_author_affiliation": item["first_author_affiliation"],
            "verified_priority_organizations": ["Google"] if key == "physical-engineering-exam" else [],
            "original_published_at": item["published_at"], "intake_class": "same-announcement-overlap-backfill",
            "first_publication_after_baseline_capture": False, "observed_versions": sorted(source["versions"]),
            "bulletin_categories": sorted(source["categories"]), "bulletin_entry_kinds": sorted(source["kinds"]),
            "status": "accepted-unimplemented", "implementation_status": "component_validation_pending",
            "delivery_status": "pending_component_verification", "component_implemented": False,
            "component_accepted": False, "review_done": False, "full_experiment_review_done": True,
            "full_experiment_status": item["full_experiment_status"], "cost_assessment": item["cost_assessment"],
            "requires_gpu_validation": item["requires_gpu_validation"], "automatic_retry": False,
            "automatic_implementation_queue": False, "promotion_eligible": False, "evolve_integrated": False})
    deltas = directory_deltas(receipts, supplied)
    counts = {"selected_papers": 4, "components_pending_verification": 4,
        "overlap_backfills": 4, "new_first_publications_after_previous_capture": 0,
        "category_entries_including_crosslists_and_replacements": sum(len(p["records"]) for p in pages),
        "unique_bulletin_identities": len(observed), "snapshot_added_base_identities_not_new_paper_count": 0,
        "snapshot_added_version_strings_not_revision_count": 0,
        "section_entry_counts": dict(Counter(r["entry_kind"] for p in pages for r in p["records"])),
        "official_directory_delta_unknown": sum(not d["delta_known"] for d in deltas)}
    common = {"schema_version": 1, "batch": BATCH, "delivery_status": "pending_component_verification",
        "all_sources_exhaustive": False, "review_watermark_advanced": False}
    scope = {**common, "fixed_component_keys": sorted(SELECTED), "reference_only_keys": [],
        "selected_scope_complete": False, "papers": selected, "additional_dispositions": deepcopy(ADDITIONAL_DISPOSITIONS)}
    coverage = {**common, "checked_on": "2026-10-24", "scope_kind": "unchanged-bulletin-overlap-component-backfill",
        "actual_announced_on": "2026-10-23", "new_announcement_batch_available": False,
        "raw_capture_sha256": raw_sha256, "baseline": "../oct23-priority-components/source-coverage.json",
        "baseline_raw_sha256": baseline["raw_capture_sha256"], "baseline_last_checked_at": baseline_end,
        "all_eight_bulletins_complete": True, "full_bulletin_full_text_review_complete": False,
        "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"}, "counts": counts,
        "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in pages},
        "retrieval_receipts": [{k: v for k, v in r.items() if k != "records"} for r in receipts],
        "official_directory_deltas": deltas, "independent_retry_receipts": independent_receipts or [],
        "additional_dispositions": deepcopy(ADDITIONAL_DISPOSITIONS),
        "limitations": ["Eight official arXiv pages still show Oct23; no Oct24 announcement or new identity is claimed.",
            "Four selected components are overlap backfills, not four papers published since the last batch.",
            "Unavailable Google/Meta directory differences remain unknown/null; no negative organization finding follows.",
            "DeepMind successful nine-page comparison is bounded, not whole-site exhaustiveness.",
            "Google PLE was independently found through its author repository and full-text affiliation, not a claimed directory delta.",
            "Four L1 components require frozen execution and integration before acceptance; no capability/full-paper claim.",
            "High-cost full experiments are terminal review DONE/not reproduced, without automatic retry or implementation queue.",
            "Global review watermark remains2026-10-15; this bounded delivery does not close a full review window."]}
    candidates = [{**row, "doc": row["detail_path"], "catalog_key": row["key"], "catalog_detail": row["detail_path"],
        "track": TRACKS[row["domain"]], "resolution": "component_pending_verification",
        "review_artifact": "research-audits/oct24-overlap-components/task-scope.json",
        "full_text_review": {"scope": "defining-method-resource-and-author-release-review", "full_article_read": False},
        "source_provenance": [{"source_url": row["paper_url"], "source_kind": "primary-method-resource-affiliation-review",
            "organization": row["first_author_affiliation"]}],
        "reason": "上一公告补漏，限定组件待冻源验收；完整高成本实验审查DONE，不提前宣称能力或GPU通过。"} for row in selected]
    batch = {**common, "date": "2026-10-24", "scope_kind": coverage["scope_kind"],
        "source_artifact": "research-audits/oct24-overlap-components/README.md", "selected_scope_complete": False,
        "counts": counts, "additional_dispositions": deepcopy(ADDITIONAL_DISPOSITIONS), "candidates": candidates}
    return coverage, scope, batch


def build(directory, independent_path=None, root=ROOT):
    ledger_path = root/"docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    require(not any(b["batch"] == BATCH for b in ledger["batches"]), "batch already exists; refuse accepted-state overwrite")
    raw = (directory/"retrieval.json").read_bytes()
    baseline = json.loads((root/"docs/research-audits/oct23-priority-components/source-coverage.json").read_text())
    deltas = [json.loads((directory/f"{name}-delta.json").read_text()) for name in ("google", "meta", "google-deepmind")]
    catalog = {key: json.loads((root/f"src/auto_research/paper_specs/catalog/{domain}/{key}.json").read_text())
               for key, (domain, _) in SELECTED.items()}
    independent = json.loads(independent_path.read_text()) if independent_path else []
    coverage, scope, batch = build_reports(json.loads(raw), baseline, deltas, catalog, hashlib.sha256(raw).hexdigest(), independent)
    updated = deepcopy(ledger)
    updated["batches"].append(batch)
    for path, value in ((root/AUDIT_REL/"source-coverage.json", coverage),
                        (root/AUDIT_REL/"task-scope.json", scope), (ledger_path, updated)):
        write(path, value)
    return coverage["counts"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_directory", type=Path)
    parser.add_argument("--independent-receipts", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.capture_directory, args.independent_receipts), ensure_ascii=False))
