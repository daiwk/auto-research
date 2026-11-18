"""Append the bounded priority backfill after its CPU evidence is recorded."""
from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from curate_nov04_components import write_new
from oct18_frozen_sources import verify_sources
from run_nov07_components import AUDIT, BATCH, COMPONENTS, ROOT, load, metric_path, spec_for, validate_metric

BASELINE = ROOT / "docs/research-audits/nov06-priority-components/source-coverage.json"
LEDGER = ROOT / "docs/paper-discovery-ledger.json"
DAY = "2026-11-07"
PRIOR_DAY = "2026-11-06"
META_ALTERNATE = "https://ai.meta.com/results/?content_types%5B0%5D=publication&page=1"
EXTRA_SOURCES = {
    "ginger": ["https://github.com/google/ginger"],
    "gslm2": [META_ALTERNATE, "https://github.com/facebookresearch/gslm2"],
    "emoreward": ["https://github.com/Tencent-Hunyuan/EmoReward"],
}
ANNOUNCED = {"ginger": "2026-11-06", "gslm2": "2026-11-03", "emoreward": "2026-11-05"}
PUBLICATION_UTC = {
    "ginger": "2026-11-05T17:09:45+00:00",
    "gslm2": "2026-10-31T17:31:45+00:00",
    "emoreward": "2026-11-04T13:43:09+00:00",
}


def validate_bulletin(rows: list[dict], baseline: dict) -> datetime:
    """Fail rather than assert a zero increment on partial or stale retrieval."""
    prior = {(row["category"], row["route"]): row for row in baseline["retrieval_receipts"]}
    observed = {(row["category"], row["route"]): row for row in rows}
    if len(rows) != 16 or set(observed) != set(prior):
        raise ValueError("need the same sixteen official routes")
    cutoff = max(datetime.fromisoformat(row["checked_at"]) for row in prior.values())
    for key, row in observed.items():
        checked_at = datetime.fromisoformat(row["checked_at"])
        if (row["url"] != prior[key]["url"] or row["status"] != "retrieved"
                or row["parse_complete"] is not True or row["latest_announcement"] != PRIOR_DAY
                or checked_at.tzinfo is None or checked_at <= cutoff
                or checked_at.astimezone(ZoneInfo("Asia/Shanghai")).date().isoformat() != DAY):
            raise ValueError("route was not freshly and completely retrieved: " + str(key))
        section = row if row["route"] == "new" else next(
            section for section in row["sections"] if section["announced_on"] == PRIOR_DAY
        )
        if any(section[field] != [] for field in (
            "added_identities", "removed_identities", "versioned_entries_changed",
        )):
            raise ValueError("bulletin actually changed: " + str(key))
        baseline_count = prior[key].get("parsed_entries") if row["route"] == "new" else next(
            item["parsed_entries"] for item in prior[key]["sections"] if item["announced_on"] == PRIOR_DAY
        )
        if not section["parsed_entries"] == section["expected_entries"] == baseline_count:
            raise ValueError("comparison counts differ: " + str(key))
    return cutoff


def admission(key: str, cutoff: datetime, rows: list[dict], baseline: dict, frozen: dict) -> dict:
    domain, identity, _ = COMPONENTS[key]
    spec = spec_for(key)
    timestamp = datetime.fromisoformat(spec["published_at"])
    if (
        spec["key"] != key or spec["domain"] != domain
        or spec["paper_url"].rsplit("/", 1)[-1] not in {identity, identity + "v1"}
        or spec["published"] != timestamp.date().isoformat()
        or timestamp != datetime.fromisoformat(PUBLICATION_UTC[key]) or timestamp >= cutoff
        or spec["implementation_status"] != "component_only"
        or not spec["review_done"] or not spec["full_experiment_review_done"]
        or spec["full_experiment_status"] != "not_reproduced_high_cost"
        or not spec["local_operator"] or not spec["cost_assessment"]
        or any(spec[flag] is not False for flag in (
            "requires_gpu_validation", "gpu_validation_passed", "promotion_eligible",
            "evolve_integrated", "automatic_retry", "automatic_implementation_queue",
        ))
    ):
        raise ValueError(f"{key}: expected a dated, closed CPU component record")
    expected_day = ANNOUNCED[key]
    seen = [
        {"source_kind": "official-arxiv-announcement", "source_url": row["url"],
         "announced_on": expected_day, "retrieved_at": row["checked_at"]}
        for row in baseline["retrieval_receipts"]
        if any(item["arxiv_id"] == identity + "v1" and item["announced_on"] == expected_day
               and item["entry_kind"] != "replacement" for item in row["identities"])
    ]
    if not seen:
        seen = [
            {"source_kind": "official-arxiv-announcement", "source_url": row["url"],
             "announced_on": expected_day, "retrieved_at": row["checked_at"]}
            for row in rows if row["route"] == "recent"
            and any(section["announced_on"] == expected_day and identity in section["matched_backfills"]
                    for section in row["sections"])
        ]
    if not seen:
        raise ValueError(f"{key}: no actual announcement evidence")
    artifact = metric_path(spec)
    validate_metric(key, load(ROOT / artifact), frozen)
    return {
        **{field: spec[field] for field in (
            "domain", "key", "title", "paper_url", "detail_path", "published", "published_at",
            "first_author", "first_author_affiliation", "priority", "cost_assessment",
            "implementation_status", "full_experiment_status", "full_experiment_review_done",
            "requires_gpu_validation", "gpu_validation_passed", "promotion_eligible", "evolve_integrated",
            "automatic_retry", "automatic_implementation_queue", "review_done",
        )},
        "id": identity, "doc": spec["detail_path"], "catalog_key": key, "catalog_detail": spec["detail_path"],
        "track": {"foundation-models": "foundation-model", "multimodal-models": "multimodal"}.get(domain, domain),
        "intake_class": "priority_overlap_backfill", "announced_on": expected_day,
        "first_publication_after_previous_capture": False, "status": "implemented",
        "resolution": "bounded_l1_component_accepted", "component_implemented": True,
        "component_accepted": True, "component_evidence": artifact.as_posix(),
        "source_provenance": [
            {"source_kind": "reviewed-fixed-primary-paper", "source_url": f"https://arxiv.org/html/{identity}v1"},
            *seen,
            *({"source_kind": "institution-directory-or-author-code", "source_url": url}
              for url in EXTRA_SOURCES[key]),
        ],
    }


def record(snapshot: Path) -> None:
    baseline = load(BASELINE)
    routes = load(snapshot)
    cutoff = validate_bulletin(routes, baseline)
    ledger = load(LEDGER)
    if any(batch["batch"] == BATCH for batch in ledger["batches"]):
        raise ValueError("audit batch already committed")
    frozen = load(AUDIT / "frozen-sources.json")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    papers = [admission(key, cutoff, routes, baseline, frozen) for key in COMPONENTS]
    watermark = load(ROOT / "docs/paper-discovery-watermark.json")["review_watermark"]
    coverage = {
        "schema_version": 1, "batch": BATCH, "checked_on": DAY, "timezone": "Asia/Shanghai",
        "baseline": BASELINE.relative_to(ROOT).as_posix(),
        "baseline_sha256": hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
        "baseline_last_checked_at": cutoff.isoformat(), "retrieval_receipts": routes,
        "latest_announcement_on_observed_routes": PRIOR_DAY, "observed_new_announcement_days": [],
        "compared_bulletin_changed": False, "all_sources_exhaustive": False,
        "full_bulletin_full_text_review_complete": False, "review_watermark_advanced": False,
        "review_watermark": {"before": watermark, "after": watermark},
        "institutional_review": "priority-review.json",
    }
    common = {
        key: coverage[key] for key in (
            "schema_version", "batch", "all_sources_exhaustive", "review_watermark_advanced", "review_watermark",
        )
    } | {
        "date": DAY, "selected_scope_complete": True, "delivery_status": "bounded_scope_complete",
        "counts": {"selected_papers": 3, "component_implementations": 3, "cuda_validated_components": 0,
                   "first_publications_after_previous_capture": 0, "full_capability_reproductions": 0},
    }
    ledger["batches"].append(common | {
        "source_artifact": "research-audits/nov07-priority-backfill/README.md", "candidates": papers,
    })
    ledger_json = json.dumps(ledger, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    if any((AUDIT / name).exists() for name in ("source-coverage.json", "task-scope.json")):
        raise ValueError("refusing to overwrite review evidence")
    write_new(AUDIT / "source-coverage.json", coverage)
    write_new(AUDIT / "task-scope.json", common | {"papers": papers})
    LEDGER.write_text(ledger_json, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    record(parser.parse_args().snapshot)
