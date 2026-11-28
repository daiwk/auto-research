"""Close one historical Google identity follow-up, not an exhaustive new-paper scan."""
from __future__ import annotations

import argparse
import hashlib
import json

from PIL import Image

from oct18_frozen_sources import verify_sources
from run_nov28_habitats_component import AUDIT, BATCH, ROOT, load, source_hashes, validate_raw

DATE = "2026-11-28"
CACHE = ROOT / ".cache/nov28-latest"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def proposed():
    value = load(AUDIT / "paper-proposals-agent.json")["papers"]
    rows = list(value.values()) if isinstance(value, dict) else value
    if len(rows) != 1 or rows[0]["key"] != "habitats" or rows[0]["domain"] != "agent-research":
        raise ValueError("scope changed")
    return rows[0]


def coverage():
    api, bulletin = load(CACHE / "metadata-pool.json"), load(CACHE / "announcement-pool.json")
    previous = load(ROOT / "docs/research-audits/nov27-latest/metadata-index.json")
    old_pool = ROOT / ".cache/nov27-latest/metadata-pool.json"
    old = {r["canonical_id"]: r for r in load(old_pool)["papers"]}
    fields = ("title", "abstract", "authors", "published", "updated", "arxiv_id", "url")
    added = [r["canonical_id"] for r in api["papers"] if r["canonical_id"] not in old]
    changed = [r["canonical_id"] for r in api["papers"] if r["canonical_id"] in old and any(r.get(k) != old[r["canonical_id"]].get(k) for k in fields)]
    if added or changed or bulletin["identities"] != previous["announced_identities"]:
        raise ValueError("capture delta changed; compact unchanged-only inventory needs a new review")
    def fact_fingerprint(rows):
        values = [{"canonical_id": r["canonical_id"], **{k: r.get(k) for k in fields}}
                  for r in sorted(rows, key=lambda r: r["canonical_id"])]
        return hashlib.sha256(json.dumps(values, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    current_facts = fact_fingerprint(api["papers"])
    previous_facts = fact_fingerprint([old[r["canonical_id"]] for r in api["papers"]])
    if current_facts != previous_facts:
        raise ValueError("original paper fact comparison differs")
    github = load(CACHE / "github/receipts.json")
    queries = []
    for receipt in github["receipts"]:
        if receipt["status"] != "captured" or digest(ROOT / receipt["capture"]) != receipt["sha256"]:
            raise ValueError("source capture differs")
        if receipt["label"].endswith(("-created", "-pushed")):
            value = load(ROOT / receipt["capture"])
            queries.append({"label": receipt["label"], "total_count": value["total_count"],
                "incomplete_results": value.get("incomplete_results"), "repositories": [
                    {k: r.get(k) for k in ("full_name", "html_url", "created_at", "pushed_at")}
                    for r in value["items"]]})
    dump(AUDIT / "priority-source-captures.json", github | {"repository_queries": queries,
        "official_directories": {"planned_pages": 56, "retained_successful_pages": 0,
            "completed_request_count": None, "status": "source_exception_archived",
            "reason": "Directory transport stalled; own bounded sweep terminated (exit143). Separate Google monthly blog request timed out after15.010s with zero bytes (exit28). No56-page completion claim.",
            "automatic_retry": False}})
    baseline = ROOT / "docs/research-audits/nov27-latest/metadata-index.json"
    old_index = {r["canonical_id"]: r for r in previous["identities"]}
    status_delta = [{"canonical_id": r["canonical_id"], "previous": old_index[r["canonical_id"]].get("repository_status"),
                     "current": r.get("repository_status")}
                    for r in api["papers"] if old_index[r["canonical_id"]].get("repository_status") != r.get("repository_status")]
    dump(AUDIT / "metadata-index.json", {"schema_version": 2, "metadata_only": True,
        "captured_at": api["captured_at"], "requested_window": api["requested_window"],
        "overlap_start_utc": api["overlap_start_utc"], "categories": api["categories"],
        "coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
        "all_sources_exhaustive": False, "metadata_inventory_is_implementation_backlog": False,
        "receipts": api["receipts"], "identity_ids": sorted(r["canonical_id"] for r in api["papers"]),
        "baseline": baseline.relative_to(ROOT).as_posix(), "baseline_sha256": digest(baseline),
        "added_identity_ids": added, "changed_original_fact_identity_ids": changed,
        "announcement_receipts": bulletin["receipts"],
        "added_announcement_identity_ids": sorted(set(bulletin["identities"]) - set(previous["announced_identities"])),
        "baseline_index_fields": ["canonical_id", "title", "published", "updated"],
        "historical_baseline_extra_fields": ["repository_status"],
        "derived_repository_status_delta": status_delta,
        "repository_status_policy": "Baseline statuses are historical, not current publication facts. Apply the explicit derived-status delta for current capture bookkeeping; never infer paper revision from it.",
        "unchanged_index_fields_and_announcements_inherit_baseline": True,
        "raw_paper_fact_comparison": {"fields": list(fields),
            "current_pool": (CACHE / "metadata-pool.json").relative_to(ROOT).as_posix(),
            "current_pool_sha256": digest(CACHE / "metadata-pool.json"),
            "previous_pool": old_pool.relative_to(ROOT).as_posix(), "previous_pool_sha256": digest(old_pool),
            "canonical_serialization": "Sort923 common records by canonical_id, keep canonical_id plus listed fields, JSON ensure_ascii=False/sort_keys=True/separators=(',',':'), then UTF-8 SHA256.",
            "current_common_fields_sha256": current_facts, "previous_common_fields_sha256": previous_facts,
            "raw_captures_retained_privately": True,
            "all_seven_fields_present_in_public_baseline": False},
        "continuation": "Compact paper-fact delta. Only four listed index facts and identical announcement records inherit the SHA-bound Nov27 index. Repository status is historical with an explicit current-capture delta. Abstract/authors/arxiv_id/url are NOT stored in that public index; separate raw-pool SHA bindings and identical canonical seven-field fingerprints support their comparison. Raw captures are privately retained. Derived repository status is not a publication revision."})
    values = {"schema_version": 1, "reviewed_on": DATE, "window": api["requested_window"],
        "metadata_identities": len(api["papers"]), "announcement_identities": len(bulletin["identities"]),
        "baseline": "docs/research-audits/nov27-latest/metadata-index.json",
        "new_metadata_identities_relative_to_nov27": added, "changed_paper_fact_identities": changed,
        "compared_original_fields": list(fields), "derived_repository_status_not_a_publication_revision": True,
        "first_releases_in_requested_window": sum(api["requested_window"]["start"] <= r["published"][:10] <= api["requested_window"]["end"] for r in api["papers"]),
        "latest_original_publication_observed": max(r["published"] for r in api["papers"]),
        "latest_revision_observed": max(r["updated"] for r in api["papers"]),
        "announcement_dates_observed": sorted({r.get("announced_on") for r in bulletin["receipts"] if r.get("announced_on")}),
        "announcement_identity_delta_from_previous_batch": len(set(bulletin["identities"]) - set(previous["announced_identities"])),
        "official_directory_successful_captures": 0, "repository_event_queries": len(queries),
        "github_requests_captured": len(github["receipts"]),
        "metadata_coverage_complete_to_overlap_boundary": api["coverage_complete_to_overlap_boundary"],
        "all_sources_exhaustive": False, "watermark_advanced": False, "review_watermark_unchanged": "2026-11-15",
        "limits": ["Finite current-source follow-up, not full-source or per-paper selection closure.",
            "No new original release observed in the captured Nov27–28 window; not a global absence claim.",
            "Habitats is a Nov23 historical identity resolved by a newly added official citation, not today's new publication.",
            "4RROW has no verified primary paper/date; archived source exception, no fake algorithm or high-cost paper completion.",
            "Official directory transports failed; source exceptions do not imply no Google/Meta papers.",
            "Pushes, source artifacts, metadata pool membership and implementation delivery are distinct."]}
    dump(AUDIT / "source-coverage.json", values)
    return values


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepare", action="store_true")
    args = parser.parse_args()
    row = proposed()
    path = ROOT / f"src/auto_research/paper_specs/catalog/{row['domain']}/{row['key']}.json"
    if args.prepare:
        if path.exists() and load(path) != row:
            raise ValueError("refusing spec overwrite")
        dump(path, row)
        print("Installed one reviewed CPU-only spec; not an execution-completion claim.")
        return
    frozen = load(AUDIT / "frozen-sources.json")
    if source_hashes() != frozen["source_sha256"]:
        raise ValueError("executed source drift")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    validate_raw(load(AUDIT / "raw-cpu.json"), frozen)
    row = load(path)
    if row["full_experiment_status"] != "not_reproduced_high_cost" or row["full_experiment_review_done"] is not True or row["requires_gpu_validation"]:
        raise ValueError("cost/device scope changed")
    page = ROOT / "docs" / row["detail_path"]
    if f"<!-- source-sha256: {digest(page)} -->" not in page.with_name("README-en.md").read_text():
        raise ValueError("stale English")
    asset = page.parent / "assets/paper-figure-01.png"
    provenance = load(asset.with_name("provenance.json"))
    if "figures" in provenance:
        provenance = next(r for r in provenance["figures"] if r["file"] == asset.name)
    if digest(asset) not in {provenance.get("asset_sha256"), provenance.get("image_sha256"), provenance.get("sha256")}:
        raise ValueError("figure differs")
    width, height = Image.open(asset).size
    figure = {"page": page.relative_to(ROOT).as_posix(), "paper_url": row["paper_url"], "arxiv_id": "2611.31160",
        "figure": "Figure1", "original_caption": provenance.get("caption", ""),
        "source_url": "https://arxiv.org/pdf/2611.31160v1", "extraction": "original_source_reviewed",
        "asset": asset.relative_to(ROOT).as_posix(), "width": width, "height": height,
        "score": 0, "error": "", "asset_sha256": digest(asset)}
    figures = load(ROOT / "docs/paper-figures-manifest.json")
    dump(ROOT / "docs/paper-figures-manifest.json", [x for x in figures if x["page"] != figure["page"]] + [figure])
    row |= {"id": "2611.31160", "status": "implemented", "resolution": "bounded_component_accepted",
        "reason": row["summary"], "component_implemented": True, "full_capability_reproduced": False,
        "doc": row["detail_path"], "review_scope": "selected_primary_method_and_cost_review",
        "intake_class": "historical_identity_completed_from_new_author_citation"}
    counts = {"accepted_papers": 1, "low_cost_components": 1, "l1_mechanism_components": 1,
        "cuda_components": 0, "authored_bilingual_questions": 4, "same_topic_deep_dive_updates": 1,
        "full_capability_reproductions": 0, "full_experiments_terminal_high_cost": 1,
        "new_first_publications_today": 0, "historical_identity_followups": 1}
    scope = load(AUDIT / "intake-scope.json") | {"selected_scope_complete": True,
        "delivery_status": "fixed_scope_complete", "counts": counts, "papers": [row], "source_commit": frozen["commit"]}
    dump(AUDIT / "task-scope.json", scope)
    ledger = load(ROOT / "docs/paper-discovery-ledger.json")
    ledger["batches"] = [b for b in ledger["batches"] if b.get("batch") != BATCH] + [
        {k: v for k, v in scope.items() if k != "papers"} | {"candidates": [row]}]
    dump(ROOT / "docs/paper-discovery-ledger.json", ledger)
    cov = coverage()
    print(json.dumps({"accepted": 1, "captured_metadata": cov["metadata_identities"], "watermark_advanced": False}))


if __name__ == "__main__":
    main()
