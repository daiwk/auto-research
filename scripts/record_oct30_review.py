"""Record a bounded overlap delivery from actual captures, never a new-day claim."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from curate_oct30_components import (  # noqa: E402
    AUDIT, BATCH, COMPONENTS, catalogue, check_evidence, metric_path, require, validate_scope, write,
)

BASE = ROOT / "docs/research-audits/oct29-components"
CATEGORIES = {"cs.AI", "cs.CL", "cs.IR", "cs.LG", "cs.CV", "cs.RO", "cs.SD", "eess.AS"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identities(values):
    return {value.split("v", 1)[0] for value in values}


def directory_records(payload):
    result = {}
    for page in payload["pages"]:
        for row in page["records"]:
            identity = (page["organization"], row["url"])
            require(identity not in result, "one official-directory record per organization/URL")
            result[identity] = row
    return result


def record(capture_path, inventory_path, priority_path, primary_path, activity_path):
    check_evidence()
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    require(not any(b["batch"] == BATCH for b in ledger["batches"]), "immutable reviewed batch already recorded")
    capture = json.loads(capture_path.read_text())
    pages = [p for p in capture if p["kind"] == "arxiv-new"]
    recent = [p for p in capture if p["kind"] == "arxiv-recent"]
    require(len(capture) == 16 and len(pages) == len(recent) == 8
            and {p["source"] for p in pages} == {p["source"] for p in recent} == CATEGORIES, "sixteen bounded category captures")
    require(all(p["status"] == "retrieved" and p["parse_complete"] is True
                and p["expected_entries"] == p["parsed_entries"] == len(p["records"]) for p in capture), "complete source transfer and parse")
    require({p["announced_on"] for p in pages} == {"2026-10-28"}, "actual visible bulletin, not wall-clock date")
    old = json.loads((BASE / "source-coverage.json").read_text())
    current_ids = {p["source"]: [r["id"] for r in p["records"]] for p in pages}
    previous_ids = old["bulletin_ids_by_category"]
    added = {category: sorted(identities(current_ids[category]) - identities(previous_ids[category])) for category in CATEGORIES}
    removed = {category: sorted(identities(previous_ids[category]) - identities(current_ids[category])) for category in CATEGORIES}
    require(not any(added.values()) and not any(removed.values()), "this record is explicitly a zero-delta overlap batch")
    recent_ids = {p["source"]: {s["date"]: [r["id"] for r in p["records"] if r["announced_on"] == s["date"]]
                               for s in p["sections"]} for p in recent}
    shared_recent_delta = {}
    for category, days in old["recent_ids_by_category_and_date"].items():
        for day, ids in days.items():
            now = identities(recent_ids[category][day])
            before = identities(ids)
            shared_recent_delta[category + ":" + day] = {"added": sorted(now - before), "removed": sorted(before - now)}
    require(all(not d["added"] and not d["removed"] for d in shared_recent_delta.values()), "shared recent dates have zero identity delta")

    inventory = json.loads(inventory_path.read_text())
    baseline_path = BASE / "official-source-inventory.json"
    baseline = json.loads(baseline_path.read_text())
    require(len(inventory["pages"]) == 44 and all(p["status"] == "retrieved" for p in inventory["pages"]), "44 bounded official directory pages")
    current_records, previous_records = directory_records(inventory), directory_records(baseline)
    require(current_records == previous_records, "zero official parsed-record delta, not an exhaustion claim")
    official = {"schema_version": 1, "checked_at": inventory["checked_at"],
        "baseline": "docs/research-audits/oct29-components/official-source-inventory.json", "baseline_sha256": sha(baseline_path),
        "current_canonical_records_equal_baseline": True, "new_urls": 0, "removed_urls": 0, "changed_records": 0,
        "record_counts": {org: sum(key[0] == org for key in current_records) for org in ("Google", "Meta", "Google DeepMind")},
        "pages": [{**{k: v for k, v in p.items() if k != "records"}, "parsed_records": len(p["records"])} for p in inventory["pages"]],
        "all_sources_exhaustive": False,
        "limitation": "Unchanged bounded directories and public-repo search do not prove no new paper exists elsewhere; Meta remains a six-page slice."}
    priority = json.loads(priority_path.read_text())
    priority["artifacts"] = {"publication_inventory": "official-directory-check.json", "primary_page_receipts": "official-primary-receipts.json", "bounded_repo_activity": "official-repo-activity.json"}
    priority.pop("implementation_authorization", None)
    for paper in priority.get("papers", []):
        paper.pop("component_owner", None)

    catalog, rows = catalogue(), []
    before_capture = min(datetime.fromisoformat(p["checked_at"].replace("Z", "+00:00")) for p in old["retrieval_receipts"])
    for key in sorted(COMPONENTS):
        item = catalog[key]
        require(item["review_done"] is True and item["full_experiment_review_done"] is True
                and item["full_experiment_status"] == "not_reproduced_high_cost", "actual component accepted and full cost terminal")
        row = {field: item[field] for field in ("domain", "key", "title", "paper_url", "detail_path", "priority", "first_author",
                "first_author_affiliation", "published_at", "cost_assessment", "implementation_status")}
        identifier = item["paper_url"].split("/")[-1].split("v", 1)[0]
        provenance = [{"source_kind": "reviewed-fixed-primary-paper", "source_url": item.get("reviewed_version_url", item["paper_url"])}]
        if key == "crop":
            provenance.append({"source_kind": "historical-google-directory-backfill", "source_url": "https://research.google/pubs/crop-token-efficient-reasoning-in-large-language-models-via-regularized-prompt-optimization/"})
        for page in capture:
            matches = [r for r in page["records"] if r["id"].split("v", 1)[0] == identifier]
            if matches:
                provenance.append({"source_kind": page["kind"], "source_url": page["url"], "announced_dates": sorted({r.get("announced_on", page.get("announced_on")) for r in matches})})
        require(len(provenance) > 1 or key == "crop", "current official listing or explicit historical Google source")
        row.update(id=identifier, intake_class=item["intake_class"], status="implemented",
            first_publication_after_previous_capture=datetime.fromisoformat(item["published_at"].replace("Z", "+00:00")) > before_capture,
            component_accepted=True, component_implemented=True, review_done=True,
            full_experiment_status="not_reproduced_high_cost", full_experiment_review_done=True,
            resolution="bounded_l1_component_accepted", requires_gpu_validation=COMPONENTS[key][1] == "cuda",
            gpu_validation_passed=COMPONENTS[key][1] == "cuda", component_evidence=metric_path(key, catalog).as_posix(),
            automatic_retry=False, automatic_implementation_queue=False, promotion_eligible=False, evolve_integrated=False,
            source_provenance=provenance)
        rows.append(row)
    counts = {"selected_papers": 10, "components_accepted": 10, "gpu_validated_components": 6,
        "cpu_only_components": 4, "reference_only_high_cost_done": 0, "components_pending_verification": 0,
        "capability_reproductions_claimed": 0, "latest_category_entries": sum(p["parsed_entries"] for p in pages),
        "latest_unique_identities": len({v for ids in current_ids.values() for v in identities(ids)}),
        "new_bulletin_identities_since_previous_capture": 0,
        "selected_first_publications_after_previous_capture": sum(r["first_publication_after_previous_capture"] for r in rows),
        "selected_historical_official_source_backfills": 1, "selected_recent_overlap_backfills": 9}
    require(counts["selected_first_publications_after_previous_capture"] == 0, "no paper is newly first-published since previous capture")
    common = {"schema_version": 1, "batch": BATCH, "counts": counts, "selected_scope_complete": True,
        "delivery_status": "bounded_scope_complete", "all_sources_exhaustive": False,
        "review_watermark_advanced": False, "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"}}
    scope = {**common, "fixed_component_keys": sorted(COMPONENTS), "reference_only_keys": [], "papers": rows,
        "updated_existing_keys": [], "additional_dispositions": []}
    batch = {**common, "date": "2026-10-30", "source_artifact": "research-audits/oct30-overlap-components/README.md",
        "candidates": [{**r, "doc": r["detail_path"], "catalog_key": r["key"], "catalog_detail": r["detail_path"],
            "track": {"agent-research": "agent", "foundation-models": "foundation-model"}.get(r["domain"], r["domain"])} for r in rows]}
    coverage = {**common, "checked_on": "2026-10-30", "actual_announced_on": "2026-10-28", "raw_capture_sha256": sha(capture_path),
        "baseline": "docs/research-audits/oct29-components/source-coverage.json", "baseline_sha256": sha(BASE / "source-coverage.json"),
        "retrieval_receipts": [{k: v for k, v in p.items() if k != "records"} for p in capture],
        "bulletin_ids_by_category": current_ids, "recent_ids_by_category_and_date": recent_ids,
        "bulletin_delta": {"added": added, "removed": removed}, "shared_recent_date_delta": shared_recent_delta,
        "priority_review": "priority-review.json", "full_bulletin_full_text_review_complete": False,
        "limitations": ["Latest observed bulletin is Oct28; no Oct29/30 batch is invented.",
            "This is ten accepted overlap/history components, not ten new papers from today.",
            "Official directories are bounded; unreviewed broad-capture identities are not claimed fully reviewed.",
            "All full expensive experiments are terminal not reproduced; L1 receipts do not establish capability or Evolve integration.",
            "Global review watermark is unchanged at Oct15."]}
    primary_receipts = json.loads(primary_path.read_text())
    validate_scope(scope, batch, catalog, coverage=coverage, primary_receipts=primary_receipts)
    updated = deepcopy(ledger)
    updated["batches"].append(batch)
    for filename, payload in (("official-directory-check.json", official), ("priority-review.json", priority),
                             ("official-primary-receipts.json", primary_receipts),
                             ("official-repo-activity.json", json.loads(activity_path.read_text())),
                             ("source-coverage.json", coverage), ("task-scope.json", scope)):
        write(AUDIT / filename, payload)
    write(ledger_path, updated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ("capture", "inventory", "priority", "primary", "activity"):
        parser.add_argument("--" + flag, type=Path, required=True)
    args = parser.parse_args()
    record(args.capture, args.inventory, args.priority, args.primary, args.activity)
