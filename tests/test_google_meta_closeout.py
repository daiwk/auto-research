"""Bounded source review, implementation, cost and GPU evidence stay separate."""
import hashlib
import json
from pathlib import Path

from auto_research.discovery import repository_paper_records
from auto_research.gpu_validation import load_gpu_receipt
from scripts.sync_google_meta_closeout import BATCH, build_batch
from scripts.generate_research_catalogs import foundation_rows, render_foundation_catalog

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/google-meta-closeout-20261021"


def read(path):
    return json.loads(path.read_text())


def test_google39_exact_scope_and_retained_primary_evidence():
    data = read(AUDIT / "google39-reviews.json")
    prior = read(AUDIT.parent / "historical-backlog-reconciliation-20261021/reconciliation.json")
    rows = data["records"]
    assert [r["id"] for r in rows] == prior["current_2026_google_review_leads"]
    assert len(rows) == len({r["id"] for r in rows}) == 39
    for row in rows:
        receipt = AUDIT / row["source_retrieval_reference"]
        assert hashlib.sha256(receipt.read_bytes()).hexdigest() == row["source_sha256"]
        assert row["review_done"] is True
        assert row["implementation_status"] == "not_implemented"
        assert row["automatic_implementation_queue"] is False
        assert row["full_text_review"]["full_article_read"] is False
        assert row["full_text_review"]["read_sections"]
        assert row["cost_assessment"]["local_cost_measurement_performed"] is False


def test_append_only_closure_reproduces_and_does_not_miscount_catalog_delivery():
    ledger = read(ROOT / "docs/paper-discovery-ledger.json")
    assert [b for b in ledger["batches"] if b["batch"] == BATCH] == [build_batch(ledger)]
    rows = build_batch(ledger)["candidates"]
    assert len(rows) == len({row["id"] for row in rows}) == 62
    components = [row for row in rows if row["status"] == "implemented"]
    assert {r["key"] for r in components} == {"specguard", "video-encoder-selection"}
    assert sum(r.get("classification_repair_only", False) for r in rows) == 14
    assert all(row["automatic_implementation_queue"] is False for row in rows)
    states = repository_paper_records(ROOT / "docs/research-manifest.json", ROOT / "docs/paper-discovery-ledger.json")
    for row in components:
        assert states[row["id"]]["repository_status"] == "catalogued"
        assert states[row["id"]]["implementation_status"] == "component_only"
        assert states[row["id"]]["full_experiment_resolution"] == "not_reproduced_high_cost"
    summary = read(AUDIT / "current-state.json")
    assert summary["google39_repository_statuses"] == {"accepted-unimplemented": 16, "reviewed": 23}
    assert summary["review_watermark_advanced"] is summary["all_sources_exhaustive"] is False


def test_actual_gpu_evidence_retains_specguard_negative_results():
    spec = load_gpu_receipt(ROOT / "docs/gpu-validations/specguard-a100-20261021.json")
    assert spec["diagnostic_only"] is True
    assert spec["metrics"]["task_runs"] == spec["metrics"]["inconclusive"] == 3
    assert spec["metrics"]["certified_conflicts"] == spec["metrics"]["formal_agreements"] == 0
    assert spec["metrics"]["actual_model_calls"] == 6
    assert spec["metrics"]["actual_generated_tokens"] == 425
    assert spec["executed_model_roles"] == ["spec"]
    assert spec["end_to_end_certificate_observed"] is False
    video = load_gpu_receipt(ROOT / "docs/gpu-validations/video-encoder-selection-a100-20261021.json")
    assert video["diagnostic_only"] is True
    assert video["metrics"]["selected_tokens_mean"] == 32
    assert video["metrics"]["candidate_tokens_mean"] == 256
    assert video["metrics"]["source_position_max_error_max"] == 0
    assert video["protocol"]["full_SITE_selection_reproduced"] is False
    assert video["protocol"]["video_QA_capability_evaluated"] is False
    manifest = AUDIT / "evidence/video-source-manifest.json"
    assert hashlib.sha256(manifest.read_bytes()).hexdigest() == video["dataset"]["manifest_sha256"]
    assert set(read(manifest)) == {"dataset_id", "dataset_revision", "examples"}
    assert not {"answer", "gold"}.intersection(read(manifest)["examples"][0])


def test_all_foundation_catalog_entries_have_every_browse_dimension_once():
    expected = {paper["key"] for paper in read(ROOT / "docs/research-manifest.json")["papers"]
                if paper["domain"] == "foundation-models"}
    rows = foundation_rows()
    assert len(rows) == len(expected) == len({row["key"] for row in rows})
    assert {row["key"] for row in rows} == expected
    for dimension in ("organization", "topic", "year"):
        text = render_foundation_catalog(dimension)
        for key in expected:
            assert text.count(f"（`{key}`）") == 1, (dimension, key)
