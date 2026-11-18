"""Record the bounded Atom intake after checking its measured CPU artifacts."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json

from curate_nov04_components import write_new
from oct18_frozen_sources import verify_sources
from run_nov09_components import (
    AUDIT, BATCH, COMPONENTS, ROOT, artifact_path, load, spec_path, validate_metric,
)

LEDGER = ROOT / "docs/paper-discovery-ledger.json"
V1 = {
    "2611.09822": "2026-11-06T18:08:06Z",
    "2611.09501": "2026-11-06T14:22:43Z",
    "2611.09472": "2026-11-06T13:51:02Z",
    "2611.09448": "2026-11-06T13:22:42Z",
}


def record() -> None:
    coverage = load(AUDIT / "source-coverage.json")
    if (coverage["batch"] != BATCH or coverage["all_sources_exhaustive"]
            or coverage["new_announcement_date_verified"] or coverage["review_watermark_advanced"]):
        raise ValueError("Atom first-page intake cannot certify full announcement coverage")
    baseline = load(ROOT / "docs" / coverage["baseline_artifact"])
    cutoff = max(datetime.fromisoformat(row["checked_at"]) for row in baseline["retrieval_receipts"])
    prior_ids = {item["arxiv_id"].split("v", 1)[0] for row in baseline["retrieval_receipts"]
                 for item in row["identities"]}
    frozen = load(AUDIT / "frozen-sources.json")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    ledger = load(LEDGER)
    if any(batch["batch"] == BATCH for batch in ledger["batches"]):
        raise ValueError("Atom increment is already recorded")
    papers = []
    for key, (domain, identity, _) in COMPONENTS.items():
        spec = load(ROOT / spec_path(key))
        if (identity in prior_ids or identity <= coverage["baseline_highest_nonreplacement_id"]
                or spec["published_at"] != V1[identity] or spec.get("announced_on") is not None
                or not spec["review_done"] or not spec["full_experiment_review_done"]
                or spec["automatic_implementation_queue"] or spec["automatic_retry"]):
            raise ValueError(f"{key}: expected a closed Atom admission without inferred announcement")
        artifact = artifact_path(spec)
        validate_metric(key, load(ROOT / artifact), frozen)
        after_cutoff = datetime.fromisoformat(V1[identity].replace("Z", "+00:00")) > cutoff
        papers.append({
            **{field: spec[field] for field in (
                "domain", "key", "title", "paper_url", "detail_path", "published", "published_at",
                "first_author", "first_author_affiliation", "priority", "cost_assessment",
                "implementation_status", "full_experiment_status", "full_experiment_review_done",
                "requires_gpu_validation", "gpu_validation_passed", "promotion_eligible", "evolve_integrated",
                "automatic_retry", "automatic_implementation_queue", "review_done",
            )},
            "id": identity, "doc": spec["detail_path"], "catalog_key": key, "catalog_detail": spec["detail_path"],
            "track": {"foundation-models": "foundation-model"}.get(domain, domain),
            "intake_class": "official_atom_increment", "submitted_after_baseline_capture": after_cutoff,
            "status": "implemented", "resolution": "bounded_l1_component_accepted",
            "component_implemented": True, "component_accepted": True, "component_evidence": artifact.as_posix(),
            "source_provenance": [
                {"source_kind": "reviewed-fixed-primary-paper", "source_url": spec["reviewed_version_url"]},
                {"source_kind": "official-arxiv-atom", "source_url": coverage["official_atom_receipts"][0]["url"],
                 "retrieved_on": coverage["checked_on"], "listed_arxiv_id": identity + "v1"},
            ],
        })
    common = {
        "schema_version": 1, "batch": BATCH, "date": coverage["checked_on"],
        "all_sources_exhaustive": False, "review_watermark_advanced": False,
        "review_watermark": coverage["review_watermark"], "selected_scope_complete": True,
        "delivery_status": "bounded_scope_complete",
        "counts": {
            "selected_papers": len(papers), "component_implementations": len(papers),
            "cuda_validated_components": 0, "full_capability_reproductions": 0,
            "submitted_after_baseline_capture": sum(row["submitted_after_baseline_capture"] for row in papers),
        },
        "source_coverage_sha256": hashlib.sha256((AUDIT / "source-coverage.json").read_bytes()).hexdigest(),
        "source_artifact": "research-audits/nov09-atom-increment/README.md",
    }
    ledger["batches"].append(common | {"candidates": papers})
    write_new(AUDIT / "task-scope.json", common | {"papers": papers})
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    record()
