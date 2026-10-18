"""Selected scope, measured evidence and non-promotion contracts for Oct18."""
from __future__ import annotations

from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.paper_specs.catalog import catalog_records

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct18_evidence", ROOT / "scripts/curate_oct18_component_evidence.py")
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)


def records():
    return {r["key"]: r for r in catalog_records() if r["key"] in admission.COSTS}


def metric_for(key):
    device, _, (domain, identity, _) = admission.item_for(key)
    return json.loads((ROOT / f"docs/{domain}/{identity}-{key}/metrics/component-{device}-seeds42-44.json").read_text())


def test_complete_nineteen_paper_scope_has_no_unearned_capability_claims():
    rows = records()
    assert set(rows) == set(admission.COSTS) and len(rows) == 19
    for key, row in rows.items():
        admission.validate_catalog_identity(row)
        assert row["adapter"] is None
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
        assert row["diagnostic_only"] is True and row["promotion_eligible"] is False
        assert row["evolve_integrated"] is False
        assert row["first_author_affiliation"] and row["published"] in {"2026-10-14", "2026-10-15"}
        text = (ROOT / "docs" / row["detail_path"]).read_text()
        for token in ("## 论文信息", "## 原始论文总结", "### 核心公式", "## 本地复现", "不复现", "DONE",
                      "assets/paper-figure-01.png"):
            assert token in text, (key, token)
        if key in admission.REFERENCES:
            assert row["implementation_status"] == "deferred_high_cost" and row["review_done"] is True
            assert not row.get("local_operator") and not row.get("local_command")
            assert not row.get("gpu_validation_artifact")
        else:
            assert row["implementation_status"] in {"component_only", "evaluation_protocol_interface"}
            module, member = row["local_operator"].rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), member))


def test_new_papers_are_reachable_in_all_three_domain_browse_catalogs():
    for row in records().values():
        for dimension in ("organization", "topic", "year"):
            page = ROOT / "docs" / row["domain"] / "catalog" / f"by-{dimension}.md"
            assert Path(row["detail_path"]).parent.name in page.read_text(), (row["key"], dimension)


@pytest.mark.parametrize("key", sorted(set(admission.COSTS) - admission.REFERENCES))
def test_measured_seeds_and_receipts_revalidated_against_current_and_frozen_sources(key):
    metric = metric_for(key)
    device = admission.validate_curated(metric, key)
    assert key in admission.OUTCOME_CHECKS and admission.OUTCOME_CHECKS[key]
    row = records()[key]
    if device == "cuda":
        assert row["requires_gpu_validation"] is True
        receipt = load_gpu_receipt(ROOT / row["gpu_validation_artifact"])
        admission.validate_receipt_binding(receipt, metric, key)
        assert receipt["adapter_key"] == key and receipt["metrics"] == metric["metrics"]
        assert receipt["provenance"]["commit"] == metric["provenance"]["commit"]
        assert receipt["executed_source_sha256"] == metric["provenance"]["executed_source_sha256"]
        assert any(name in receipt["accelerator"]["model"] for name in ("A100", "A30"))
    else:
        assert not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact")


@pytest.mark.parametrize("status", ["failed", "partial", "error", "timeout", "skipped"])
def test_explicit_failures_cannot_be_relabelled_passed(status):
    with pytest.raises(ValueError, match="failure"):
        admission.reject_failure({"status": status})


@pytest.mark.parametrize("mutation", ["failed_seed", "missing_seed", "edited_aggregate", "wrong_commit",
                                      "missing_dataset", "wrong_input_fingerprint", "full_claim", "review_unfinished", "tier_upgrade"])
def test_curated_artifact_is_not_a_trusted_pass_certificate(mutation):
    metric = deepcopy(metric_for("memory-mosaics-plus"))
    if mutation == "failed_seed":
        metric["per_seed"][0]["status"] = "failed"
    elif mutation == "missing_seed":
        metric["per_seed"].pop()
    elif mutation == "edited_aggregate":
        metric["metrics"][next(iter(metric["metrics"]))] = {"mean": 9999, "std": 0, "n": 3}
    elif mutation == "wrong_commit":
        metric["provenance"]["commit"] = "0" * 40
    elif mutation == "missing_dataset":
        metric["dataset"] = {}
    elif mutation == "wrong_input_fingerprint":
        metric["provenance"]["dataset_fingerprint"] = "sha256:" + "0" * 64
    elif mutation == "full_claim":
        metric["full_experiment_status"] = "reproduced_full_pipeline"
    elif mutation == "review_unfinished":
        metric["full_experiment_review_done"] = False
    else:
        metric["evaluation_protocol"]["tier"] = "l3_formal"
    with pytest.raises(ValueError):
        admission.validate_curated(metric, "memory-mosaics-plus")


def test_committed_evidence_verification_needs_no_git_history_or_network(monkeypatch):
    def no_subprocess(*args, **kwargs):
        pytest.fail("persistent evidence verification must be self-contained")
    monkeypatch.setattr(admission.subprocess, "check_output", no_subprocess)
    for key in sorted(set(admission.COSTS) - admission.REFERENCES):
        admission.validate_curated(metric_for(key), key)


def test_nested_failure_and_nonterminal_results_are_rejected():
    for result in ({"result": {"status": "failed"}}, {"result": False}, {"status": "running"}):
        with pytest.raises(ValueError):
            admission.reject_failure(result)


@pytest.mark.parametrize("field,value", [("paper_url", "https://arxiv.org/abs/9999.99999"),
                                         ("domain", "agent-research"), ("detail_path", "wrong.md")])
def test_catalog_cannot_attach_measurements_to_wrong_paper(field, value):
    row = deepcopy(records()["memory-mosaics-plus"])
    row[field] = value
    with pytest.raises(ValueError, match="identity"):
        admission.validate_catalog_identity(row)


@pytest.mark.parametrize("field", ["dataset", "commit"])
def test_receipt_binding_rejects_changed_dataset_or_commit(field):
    metric = metric_for("memory-mosaics-plus")
    row = records()["memory-mosaics-plus"]
    receipt = load_gpu_receipt(ROOT / row["gpu_validation_artifact"])
    if field == "dataset":
        receipt["dataset"] = {"id": "different", "revision": "changed"}
    else:
        receipt["provenance"]["commit"] = "0" * 40
    with pytest.raises(ValueError, match=field):
        admission.validate_receipt_binding(receipt, metric, "memory-mosaics-plus")


def test_selected_batch_does_not_claim_coverage_or_advance_watermark():
    ledger = json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())
    batch = next(b for b in ledger["batches"] if b["batch"] == admission.BATCH)
    assert batch["review_watermark_advanced"] is False and batch["coverage_complete"] is False
    assert {c["key"] for c in batch["candidates"]} == set(admission.COSTS)
    assert batch["component_validation_counts"] == {
        "gpu_validated_components": 10, "cpu_validated_components_or_interfaces": 6, "review_only": 3}
    for item in batch["candidates"]:
        assert item["review_done"] is True and item["terminal"] is True
        assert item["automatic_retry"] is False and item["automatic_implementation_queue"] is False
        assert item["status_scope"] == "full_paper_reproduction"


def test_latest_announcement_date_is_not_misreported_as_v1_or_today():
    report = json.loads((ROOT / "docs/research-audits/oct18-components/source-coverage.json").read_text())
    assert len(report["official_announcements"]) == 6
    assert all(r["parse_complete"] and r["announced_on"] == "2026-10-16"
               and r["expected_entries"] == r["parsed_entries"] for r in report["official_announcements"])
    assert report["coverage_complete"] is False and report["review_watermark_advanced"] is False
