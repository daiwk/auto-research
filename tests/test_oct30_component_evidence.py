"""Frozen ten-component delivery, real device evidence and anti-tamper gates."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from scripts import curate_oct30_components as c
from scripts.run_oct30_components import execution_spec

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/oct30-overlap-components"
FIXED_GPU = {"merlin", "fold-bias", "swim", "mpopd", "pinger", "pinterest-rlbp"}
FIXED_CPU = {"concur", "crop", "emma", "evalalloc"}
FIXED_ALL = FIXED_GPU | FIXED_CPU
WATERMARK = {"before": "2026-10-15", "after": "2026-10-15"}


def raw_results():
    return {d: json.loads((AUDIT / f"raw-{d}.json").read_text()) for d in ("cpu", "cuda")}


def scope_and_batch():
    scope = json.loads((AUDIT / "task-scope.json").read_text())
    batches = [b for b in json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())["batches"]
               if b["batch"] == c.BATCH]
    assert len(batches) == 1
    return scope, batches[0]


def test_fixed_ten_components_are_executed_and_full_cost_done_not_capability():
    c.check()
    raw = raw_results()
    assert set(c.COMPONENTS) == FIXED_ALL
    assert set(raw["cpu"]["components"]) == FIXED_ALL
    assert set(raw["cuda"]["components"]) == FIXED_GPU
    assert raw["cuda"]["accelerator"].startswith(("NVIDIA A100", "NVIDIA A30"))
    assert raw["cpu"]["accelerator"] == "CPU"
    scope, batch = scope_and_batch()
    assert scope["fixed_component_keys"] == sorted(FIXED_ALL)
    assert scope.get("reference_only_keys", []) == []
    assert len(scope["papers"]) == len(batch["candidates"]) == 10
    assert {p["key"] for p in scope["papers"]} == FIXED_ALL
    counts = scope["counts"]
    assert {k: counts[k] for k in (
        "selected_papers", "components_accepted", "gpu_validated_components", "cpu_only_components",
        "reference_only_high_cost_done", "components_pending_verification", "capability_reproductions_claimed"
    )} == {
        "selected_papers": 10, "components_accepted": 10, "gpu_validated_components": 6,
        "cpu_only_components": 4, "reference_only_high_cost_done": 0,
        "components_pending_verification": 0, "capability_reproductions_claimed": 0,
    }
    assert scope["review_watermark"] == batch["review_watermark"] == WATERMARK
    assert scope["review_watermark_advanced"] is False
    catalogue = c.catalogue()
    for paper in scope["papers"]:
        assert paper["component_accepted"] is paper["component_implemented"] is True
        assert paper["review_done"] is paper["full_experiment_review_done"] is True
        assert paper["full_experiment_status"] == "not_reproduced_high_cost"
        assert paper["resolution"] == "bounded_l1_component_accepted"
        assert paper["promotion_eligible"] is paper["evolve_integrated"] is False
        assert paper["automatic_retry"] is paper["automatic_implementation_queue"] is False
        assert paper["requires_gpu_validation"] is (paper["key"] in FIXED_GPU)
        assert catalogue[paper["key"]]["adapter"] is None
        assert catalogue[paper["key"]]["evaluation_tier"] == "l1_mechanism"
        assert catalogue[paper["key"]]["diagnostic_only"] is True


@pytest.mark.parametrize("fault", ["device", "seed", "check", "metric", "sources", "commit", "gate", "subset"])
def test_actual_cuda_contract_rejects_tampered_raw_evidence(fault):
    raw = deepcopy(raw_results())
    first = raw["cuda"]["components"]["merlin"]["per_seed"][0]
    if fault == "device":
        first["execution_device"] = "cpu"
    elif fault == "seed":
        first["seed"] = 0
    elif fault == "check":
        first["checks"].pop(next(iter(first["checks"])))
    elif fault == "metric":
        first["metrics"]["invented_metric"] = 1
    elif fault == "sources":
        raw["cuda"]["source_sha256"].pop(next(iter(raw["cuda"]["source_sha256"])))
    elif fault == "commit":
        raw["cuda"]["code_commit"] = "0" * 40
    elif fault == "gate":
        first["metrics"]["future_readout_leak_error"] = 1
    else:
        raw["cuda"]["components"].pop("fold-bias")
    with pytest.raises(ValueError):
        c.validate_raw(raw, execution_spec())


def test_learning_questions_cover_all_ten_and_bulletin_delta_is_not_invented():
    bank = {}
    for path in (ROOT / "docs/learning/questions").glob("oct30-*.json"):
        for identity, entry in json.loads(path.read_text())["papers"].items():
            assert identity not in bank
            bank[identity] = entry
    assert {identity.split(":", 1)[1] for identity in bank} == FIXED_ALL
    assert all({q["level"] for q in paper["questions"]} == {
        "basics", "mechanism", "comparison", "implementation"
    } for paper in bank.values())
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    previous = json.loads((ROOT / "docs/research-audits/oct29-components/source-coverage.json").read_text())
    assert coverage["actual_announced_on"] == "2026-10-28"
    assert coverage["review_watermark"] == WATERMARK
    assert len(coverage["bulletin_ids_by_category"]) == len(coverage["recent_ids_by_category_and_date"]) == 8
    current_ids = {identity.split("v", 1)[0] for rows in coverage["bulletin_ids_by_category"].values()
                   for identity in rows}
    previous_ids = {identity.split("v", 1)[0] for rows in previous["bulletin_ids_by_category"].values()
                    for identity in rows}
    assert current_ids == previous_ids  # Actual Oct28 bulletin, zero new identity delta.
    assert all("2026-10-27" in rows for rows in coverage["recent_ids_by_category_and_date"].values())
    assert coverage["full_bulletin_full_text_review_complete"] is False
    assert coverage["all_sources_exhaustive"] is False
    assert coverage["review_watermark_advanced"] is False


@pytest.mark.parametrize("fault", [
    "identity", "acceptance", "resolution", "counts", "evidence", "watermark", "full-cost",
    "capability", "evolve", "retry", "remove-paper", "invent-reference",
])
def test_joint_scope_ledger_tamper_cannot_forge_a_complete_delivery(fault):
    scope, batch = deepcopy(scope_and_batch())
    index = next(i for i, row in enumerate(scope["papers"]) if row["key"] == "merlin")
    for item in (scope["papers"][index], batch["candidates"][index]):
        if fault == "identity":
            item["id"] = "9999.99999"
        elif fault == "acceptance":
            item["component_accepted"] = False
        elif fault == "resolution":
            item["resolution"] = "full_pipeline"
        elif fault == "evidence":
            item["component_evidence"] = "docs/fake.json"
        elif fault == "full-cost":
            item["full_experiment_status"] = "reproduced"
        elif fault == "capability":
            item["promotion_eligible"] = True
        elif fault == "evolve":
            item["evolve_integrated"] = True
        elif fault == "retry":
            item["automatic_retry"] = True
    for item in (scope, batch):
        if fault == "counts":
            item["counts"]["gpu_validated_components"] = 10
        elif fault == "watermark":
            item["review_watermark"]["after"] = "2026-10-30"
        elif fault == "remove-paper":
            item["papers" if item is scope else "candidates"].pop(index)
        elif fault == "invent-reference":
            item["counts"]["reference_only_high_cost_done"] = 1
    with pytest.raises(ValueError):
        c.validate_scope(scope, batch, c.catalogue())


def test_source_claims_are_derived_from_committed_baseline_and_actual_retained_lists():
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    facts, counts = c.source_facts(c.catalogue(), coverage)
    scope, batch = scope_and_batch()
    assert counts == coverage["counts"] == scope["counts"] == batch["counts"]
    assert counts["latest_category_entries"] == 1478
    assert counts["latest_unique_identities"] == 1059
    assert counts["new_bulletin_identities_since_previous_capture"] == 0
    assert counts["selected_first_publications_after_previous_capture"] == 0
    assert counts["selected_historical_official_source_backfills"] == 1
    assert counts["selected_recent_overlap_backfills"] == 9
    assert {key for key, row in facts.items() if row["historical"]} == {"crop"}
    for row in scope["papers"]:
        assert all(row[field] == facts[row["key"]][field] for field in (
            "first_publication_after_previous_capture", "intake_class", "source_provenance"
        ))


def test_first_record_validation_uses_supplied_actual_sources_before_writing(monkeypatch, tmp_path):
    scope, batch = scope_and_batch()
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    primary = json.loads((AUDIT / "official-primary-receipts.json").read_text())
    monkeypatch.setattr(c, "AUDIT", tmp_path)
    c.validate_scope(scope, batch, c.catalogue(), coverage=coverage, primary_receipts=primary)
    primary["pages"] = []
    with pytest.raises(ValueError):
        c.validate_scope(scope, batch, c.catalogue(), coverage=coverage, primary_receipts=primary)
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize("fault", [
    "new-count", "first-publication-count", "backfill-counts", "first-publication-row", "intake",
    "source-url", "source-kind", "source-date", "baseline-hash", "category-swap", "recent-partition",
    "receipt-url", "receipt-status", "coverage-watermark", "full-review", "coverage-counts-only",
])
def test_joint_source_scope_ledger_forgery_is_rejected(fault):
    scope, batch = deepcopy(scope_and_batch())
    coverage = json.loads((AUDIT / "source-coverage.json").read_text())
    selected = [next(row for row in payload[key] if row["key"] == "merlin")
                for payload, key in ((scope, "papers"), (batch, "candidates"))]
    for payload in (scope, batch, coverage):
        if fault == "new-count":
            payload["counts"]["new_bulletin_identities_since_previous_capture"] = 999
        elif fault == "first-publication-count":
            payload["counts"]["selected_first_publications_after_previous_capture"] = 10
        elif fault == "backfill-counts":
            payload["counts"]["selected_historical_official_source_backfills"] = 0
            payload["counts"]["selected_recent_overlap_backfills"] = 10
    for row in selected:
        if fault == "first-publication-row":
            row["first_publication_after_previous_capture"] = True
        elif fault == "intake":
            row["intake_class"] = "new_first_publication"
        elif fault == "source-url":
            row["source_provenance"][1]["source_url"] = "https://invalid.example/list"
        elif fault == "source-kind":
            row["source_provenance"][1]["source_kind"] = "new_first_publication"
        elif fault == "source-date":
            row["source_provenance"][1]["announced_dates"] = ["2026-10-30"]
    if fault == "baseline-hash":
        coverage["baseline_sha256"] = "0" * 64
    elif fault == "category-swap":
        # Preserve the global union: only per-category baseline binding detects this.
        left, right = (coverage["bulletin_ids_by_category"][key] for key in ("cs.AI", "cs.CL"))
        i = next(i for i, value in enumerate(left) if value not in right)
        j = next(j for j, value in enumerate(right) if value not in left)
        left[i], right[j] = right[j], left[i]
    elif fault == "recent-partition":
        coverage["recent_ids_by_category_and_date"]["cs.AI"]["2026-10-22"].pop()
    elif fault == "receipt-url":
        coverage["retrieval_receipts"][0]["url"] = "https://invalid.example/list"
    elif fault == "receipt-status":
        coverage["retrieval_receipts"][0]["status"] = "failed"
    elif fault == "coverage-watermark":
        coverage["review_watermark"]["after"] = "2026-10-30"
    elif fault == "full-review":
        coverage["full_bulletin_full_text_review_complete"] = True
    elif fault == "coverage-counts-only":
        coverage["counts"]["latest_unique_identities"] += 1
    with pytest.raises(ValueError):
        c.validate_scope(scope, batch, c.catalogue(), coverage=coverage)
