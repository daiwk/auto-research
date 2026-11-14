"""Keep partial discovery, CPU verification, and full reproduction distinct."""
from hashlib import sha256
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from english_learning_sources import question_units  # noqa: E402
from migrate_metric_schema_v2 import migrate_payload  # noqa: E402
from oct18_frozen_sources import verify_sources  # noqa: E402
from record_nov09_increment import LEDGER, V1  # noqa: E402
from run_nov09_components import (  # noqa: E402
    AUDIT, BATCH, COMPONENTS, SEEDS, artifact_path, load, spec_path, validate_metric,
)


def test_atom_admissions_do_not_advance_full_review():
    coverage = load(AUDIT / "source-coverage.json")
    scope = load(AUDIT / "task-scope.json")
    ledger = next(batch for batch in load(LEDGER)["batches"] if batch["batch"] == BATCH)
    assert not coverage["new_announcement_date_verified"]
    assert not coverage["all_sources_exhaustive"] and not coverage["review_watermark_advanced"]
    assert not coverage["full_bulletin_full_text_review_complete"]
    assert scope["review_watermark"]["before"] == scope["review_watermark"]["after"]
    assert ledger["candidates"] == scope["papers"]
    assert set(COMPONENTS) == {paper["key"] for paper in scope["papers"]}
    assert scope["counts"]["full_capability_reproductions"] == scope["counts"]["cuda_validated_components"] == 0
    for paper in scope["papers"]:
        assert paper["published_at"] == V1[paper["id"]] and "announced_on" not in paper
        assert paper["component_accepted"] and paper["review_done"] and paper["full_experiment_review_done"]
        assert paper["full_experiment_status"] == "not_reproduced_high_cost"
        assert not paper["automatic_retry"] and not paper["automatic_implementation_queue"]


@pytest.mark.parametrize("key", sorted(COMPONENTS))
def test_component_evidence_and_bilingual_learning(key):
    frozen = load(AUDIT / "frozen-sources.json")
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    assert frozen["execution"]["device"] == "cpu" and frozen["execution"]["seeds"] == SEEDS
    assert frozen["execution"]["elapsed_seconds"] <= 120 and not frozen["execution"]["full_experiments_executed"]
    spec = load(ROOT / spec_path(key))
    path = ROOT / artifact_path(spec)
    result = load(path)
    validate_metric(key, result, frozen)
    assert migrate_payload(path, result) == result
    detail = ROOT / "docs" / spec["detail_path"]
    fingerprint = sha256(detail.read_bytes()).hexdigest()
    assert f"<!-- source-sha256: {fingerprint} -->" in detail.with_name("README-en.md").read_text()
    figure = detail.parent / "assets/paper-figure-01.png"
    row = next(x for x in load(ROOT / "docs/paper-figures-manifest.json")
               if x["asset"] == figure.relative_to(ROOT).as_posix())
    assert row["visually_inspected"] and row["sha256"] == sha256(figure.read_bytes()).hexdigest()
    ref = f"{spec['domain']}:{key}"
    questions = load(ROOT / f"docs/learning/questions/nov09-{key}.json")["papers"][ref]["questions"]
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    overlay_path = ROOT / "docs/en/learning/translations"
    translations = load(overlay_path / f"qa-nov09-{key}.json")["units"]
    expected = question_units({ref: questions})
    assert set(translations) == set(expected)
    for unit, source in expected.items():
        assert translations[unit]["reviewed"] and translations[unit]["source_sha256"] == source.source_sha256
