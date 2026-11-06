"""Guard the distinction between priority backfills and new announcements."""
import hashlib
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from migrate_metric_schema_v2 import migrate_payload  # noqa: E402
from oct18_frozen_sources import verify_sources  # noqa: E402
from record_nov07_backfill import ANNOUNCED, BASELINE, BATCH, LEDGER, validate_bulletin  # noqa: E402
from run_nov07_components import AUDIT, COMPONENTS, SEEDS, load, metric_path, spec_for, validate_metric  # noqa: E402


def test_same_complete_bulletin_not_new_papers_or_full_review():
    coverage = load(AUDIT / "source-coverage.json")
    receipts = coverage["retrieval_receipts"]
    cutoff = validate_bulletin(receipts, load(BASELINE))
    assert coverage["baseline_last_checked_at"] == cutoff.isoformat()
    assert coverage["observed_new_announcement_days"] == []
    assert not coverage["all_sources_exhaustive"]
    assert not coverage["review_watermark_advanced"]
    assert not coverage["full_bulletin_full_text_review_complete"]
    receipts[0]["parse_complete"] = False
    with pytest.raises(ValueError, match="completely retrieved"):
        validate_bulletin(receipts, load(BASELINE))


def test_closed_scope_is_only_three_original_paper_identities():
    scope = load(AUDIT / "task-scope.json")
    rows = {paper["key"]: paper for paper in scope["papers"]}
    ledger = load(LEDGER)
    batch = next(item for item in ledger["batches"] if item["batch"] == BATCH)
    assert set(rows) == set(COMPONENTS)
    assert batch["candidates"] == scope["papers"]
    assert scope["counts"]["first_publications_after_previous_capture"] == 0
    assert scope["counts"]["full_capability_reproductions"] == 0
    for key, (_, identity, _) in COMPONENTS.items():
        row = rows[key]
        assert row["id"] == identity and row["announced_on"] == ANNOUNCED[key]
        assert not row["first_publication_after_previous_capture"]
        assert row["review_done"] and row["full_experiment_review_done"]
        assert row["full_experiment_status"] == "not_reproduced_high_cost"
        assert row["requires_gpu_validation"] is row["gpu_validation_passed"] is False
        assert not row["automatic_retry"] and not row["automatic_implementation_queue"]


@pytest.mark.parametrize("key", sorted(COMPONENTS))
def test_measured_metrics_are_frozen_cpu_l1_and_migration_fixed_point(key):
    frozen = load(AUDIT / "frozen-sources.json")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    run = frozen["execution"]
    assert run["device"] == "cpu" and run["seeds"] == SEEDS
    assert 0 <= run["elapsed_seconds"] <= 120
    assert run["pretrained_model_or_api_calls"] == 0 and not run["full_experiments_executed"]
    path = ROOT / metric_path(spec_for(key))
    result = load(path)
    validate_metric(key, result, frozen)
    assert migrate_payload(path, result) == result
    result["per_seed"][0]["execution_device"] = "cuda"
    with pytest.raises(ValueError, match="device or tier"):
        validate_metric(key, result, frozen)


@pytest.mark.parametrize(("key", "learning_file"), [
    ("ginger", "ginger"), ("gslm2", "multimodal"), ("emoreward", "emoreward"),
])
def test_every_backfill_has_reviewed_bilingual_learning_and_original_figure(key, learning_file):
    docs = ROOT / "docs"
    spec = spec_for(key)
    detail = docs / spec["detail_path"]
    english = detail.with_name("README-en.md")
    digest = hashlib.sha256(detail.read_bytes()).hexdigest()
    assert f"<!-- source-sha256: {digest} -->" in english.read_text()
    figure = detail.parent / "assets/paper-figure-01.png"
    figure_entry = next(
        row for row in load(docs / "paper-figures-manifest.json")
        if row["asset"] == figure.relative_to(ROOT).as_posix()
    )
    assert figure_entry["visually_inspected"]
    assert hashlib.sha256(figure.read_bytes()).hexdigest() == figure_entry["sha256"]
    ref = spec["domain"] + ":" + key
    questions = load(docs / f"learning/questions/nov07-{learning_file}.json")["papers"][ref]["questions"]
    translated = load(docs / f"en/learning/translations/qa-nov07-{learning_file}.json")["units"]
    assert {row["level"] for row in questions} == {"basics", "mechanism", "comparison", "implementation"}
    assert all(translated[f"qa/{ref}/{row['id']}"]["reviewed"] for row in questions)
