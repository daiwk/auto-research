"""Keep the November 6 cohort tied to measured component evidence."""

import hashlib
import json
from pathlib import Path
import sys

import pytest

from auto_research.gpu_validation import load_gpu_receipt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from curate_nov06_components import (  # noqa: E402
    AUDIT, COMPONENTS, CUDA_KEYS, SEEDS, aggregate_metrics, load_specs, validate_raw,
)
from migrate_metric_schema_v2 import migrate_payload  # noqa: E402


def load(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_raw_runs_prove_exact_sources_and_three_diagnostic_seeds(device):
    raw, frozen = load(AUDIT / f"raw-{device}.json"), load(AUDIT / "frozen-sources.json")
    validate_raw(raw, device, frozen)
    assert len(raw["components"]) == (7 if device == "cpu" else 2)
    assert raw["seeds"] == [42, 43, 44]
    assert len(frozen["source_sha256"]) == 11


@pytest.mark.parametrize("field,value", [
    ("code_commit", "0" * 40), ("seeds", [42]), ("device", "cpu"), ("accelerator", "CPU"),
    ("formal_comparison", True), ("promotion_eligible", True),
])
def test_rejects_raw_claims_outside_scope(field, value):
    raw = load(AUDIT / "raw-cuda.json")
    raw[field] = value
    with pytest.raises(ValueError):
        validate_raw(raw, "cuda", load(AUDIT / "frozen-sources.json"))


def test_rejects_a_failed_device_check_even_with_all_seed_rows():
    raw = load(AUDIT / "raw-cuda.json")
    raw["components"]["ice"]["per_seed"][0]["checks"]["forced_failure"] = False
    with pytest.raises(ValueError):
        validate_raw(raw, "cuda", load(AUDIT / "frozen-sources.json"))


def test_metrics_and_gpu_receipts_match_measured_rows():
    specs = load_specs()
    assert set(specs) == set(COMPONENTS)
    for key, spec in specs.items():
        _, device = COMPONENTS[key]
        raw_path = AUDIT / f"raw-{device}.json"
        raw = load(raw_path)
        detail = ROOT / "docs" / spec["detail_path"]
        metric_path = detail.parent / f"metrics/component-{device}-seeds42-44.json"
        result = load(metric_path)
        assert result["per_seed"] == raw["components"][key]["per_seed"]
        assert result["metrics"] == aggregate_metrics(result["per_seed"])
        assert result["provenance"]["raw_runner_artifact_sha256"] == hashlib.sha256(raw_path.read_bytes()).hexdigest()
        assert result["provenance"]["executed_source_sha256"] == raw["source_sha256"]
        assert result["diagnostic_only"] and not result["promotion_eligible"]
        assert not result["formal_comparison"] and not result["evolve_integrated"]
        assert migrate_payload(metric_path, result) == result
        assert spec["requires_gpu_validation"] == spec["gpu_validation_passed"] == (key in CUDA_KEYS)
        if key in CUDA_KEYS:
            receipt = load_gpu_receipt(ROOT / spec["gpu_validation_artifact"])
            assert receipt["accelerator"]["model"] == raw["accelerator"]
            assert receipt["seeds"] == SEEDS
            assert receipt["metrics"] == result["metrics"]
            assert receipt["provenance"]["commit"] == raw["code_commit"]
            assert receipt["dataset"] == result["dataset"]


def test_full_experiment_deferrals_figures_and_reviewed_bilingual_learning():
    scope = load(AUDIT / "task-scope.json")["papers"]
    assert len(scope) == 8
    docs = ROOT / "docs"
    specs = load_specs() | {
        "xstack": load(ROOT / "src/auto_research/paper_specs/catalog/agent-research/xstack.json"),
    }
    ledger = load(docs / "paper-discovery-ledger.json")
    batch = next(row for row in ledger["batches"] if row["batch"] == "2026-11-06-priority-components")
    figures = {row["asset"]: row for row in load(docs / "paper-figures-manifest.json")}
    qa, translations = {}, {}
    for suffix in ("agent", "llm", "priority", "recommendation"):
        qa.update(load(docs / f"learning/questions/nov06-{suffix}.json")["papers"])
        translations.update(load(docs / f"en/learning/translations/qa-nov06-{suffix}.json")["units"])
    for row in scope:
        key = row["key"]
        spec = specs[key]
        assert row["review_done"] and spec["full_experiment_review_done"]
        assert spec["full_experiment_status"] == "not_reproduced_high_cost"
        assert not spec["automatic_retry"] and not spec["automatic_implementation_queue"]
        detail = docs / spec["detail_path"]
        english = detail.with_name("README-en.md")
        digest = hashlib.sha256(detail.read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in english.read_text()
        figure = load(detail.parent / "assets/provenance.json")
        asset = detail.parent / "assets/paper-figure-01.png"
        assert hashlib.sha256(asset.read_bytes()).hexdigest() == figure["sha256"]
        figure_entry = figures[asset.relative_to(ROOT).as_posix()]
        assert figure_entry["visually_inspected"]
        assert figure_entry["sha256"] == figure["sha256"]
        ref = f"{spec['domain']}:{key}"
        questions = qa[ref]["questions"]
        assert len(questions) == 4
        assert all(translations[f"qa/{ref}/{question['id']}"]["reviewed"] for question in questions)
        if key == "xstack":
            entry = next(candidate for candidate in batch["candidates"] if candidate["key"] == key)
            assert row["reason"] == entry["reason"] == spec["deferral_reason"]
            assert "不复现（审查 DONE）" in row["reason"]
            assert spec["local_operator"] is None and spec["adapter"] is None
            assert not (detail.parent / "metrics").exists()


def test_distinct_cord_papers_keep_distinct_catalog_and_source_paths():
    catalog = ROOT / "src/auto_research/paper_specs/catalog/post-training"
    original, new = load(catalog / "cord.json"), load(catalog / "cord-rollout.json")
    assert original["paper_url"] == "https://arxiv.org/abs/2610.29965v1"
    assert new["paper_url"] == "https://arxiv.org/abs/2611.07959"
    assert original["detail_path"] != new["detail_path"]
    assert "cord" not in COMPONENTS
    assert COMPONENTS["cord-rollout"] == ("post_training/cord_rollout.py", "cpu")


def test_source_counts_distinguish_bulletin_coverage_from_full_review():
    coverage = load(AUDIT / "source-coverage.json")
    receipts = coverage["retrieval_receipts"]
    assert len(receipts) == 16
    assert all(row["status"] == "retrieved" for row in receipts)
    new = [row for row in receipts if row["route"] == "new"]
    recent = [row for row in receipts if row["route"] == "recent"]
    assert len(new) == len(recent) == 8
    assert all(row["parse_complete"] for row in new)
    assert all(row["parsed_entries"] == row["expected_entries"] == len(row["identities"]) for row in new)
    assert sum(row["parsed_entries"] for row in new) == 1373
    for row in recent:
        assert {section["announced_on"] for section in row["sections"]} == {"2026-11-05", "2026-11-06"}
        assert all(section["parse_complete"] for section in row["sections"])
        assert sum(section["expected_entries"] for section in row["sections"]) == len(row["identities"])
    assert coverage["new_recent_nov06_nonreplacement_identities_equal"]
    assert coverage["counts"]["selected_first_publications_after_previous_capture"] == 5
    assert coverage["counts"]["selected_papers"] == 8
    assert not coverage["full_bulletin_full_text_review_complete"]
    assert not coverage["all_sources_exhaustive"]
    assert not coverage["review_watermark_advanced"]
