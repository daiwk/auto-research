"""Evidence stays bounded, portable, and resistant to seed/device/source drift."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import record_nov12_components as recorder  # noqa: E402
from curate_nov12_components import validate_raw  # noqa: E402
from run_nov12_components import AUDIT, COMPONENTS, CUDA_KEYS  # noqa: E402


def read(name):
    return json.loads((AUDIT / name).read_text())


@pytest.fixture
def frozen():
    return read("frozen-sources.json")


@pytest.mark.parametrize("device", ["cpu", "cuda"])
def test_accepted_raw_scope_and_actual_seeds(device, frozen):
    raw = read(f"raw-{device}.json")
    validate_raw(raw, device, frozen)
    assert set(raw["components"]) == (set(COMPONENTS) if device == "cpu" else CUDA_KEYS)
    assert raw["full_experiments_executed"] is False


@pytest.mark.parametrize("field,value", [
    ("promotion_eligible", True), ("formal_comparison", True), ("evolve_integrated", True),
    ("pretrained_model_calls", 1), ("full_experiments_executed", True), ("automatic_retry", True),
    ("elapsed_seconds", 181), ("elapsed_seconds", float("nan")), ("accelerator", "CPU"),
    ("device", "cpu"), ("code_commit", "0" * 40), ("seeds", [42, 43]),
])
def test_promoted_or_relabelled_raw_is_rejected(field, value, frozen):
    raw = read("raw-cuda.json")
    raw[field] = value
    with pytest.raises(ValueError):
        validate_raw(raw, "cuda", frozen)


def test_source_hash_drift_in_both_raw_and_proof_is_rejected(frozen):
    raw = read("raw-cuda.json")
    changed = deepcopy(frozen)
    path = "src/auto_research/post_training/bopd.py"
    changed["source_sha256"][path] = raw["source_sha256"][path] = "0" * 64
    with pytest.raises(ValueError):
        validate_raw(raw, "cuda", changed)


@pytest.mark.parametrize("change", ["missing", "seed", "device", "accelerator", "failed-check"])
def test_per_seed_tampering_is_rejected(change, frozen):
    raw = read("raw-cuda.json")
    rows = raw["components"]["bopd"]["per_seed"]
    if change == "missing":
        rows.pop()
    elif change == "seed":
        rows[0]["seed"] = 99
    elif change == "device":
        rows[0]["execution_device"] = "cpu"
    elif change == "accelerator":
        rows[0]["execution_accelerator"] = "CPU"
    else:
        rows[0]["checks"][next(iter(rows[0]["checks"]))] = False
    with pytest.raises(ValueError):
        validate_raw(raw, "cuda", frozen)


def test_pure_theory_is_not_relabelled_high_cost():
    specs = recorder.specifications()
    assert specs[recorder.THEORY]["full_experiment_status"] == "not_applicable_theory_only"
    assert sum(s["full_experiment_status"] == "not_reproduced_high_cost" for s in specs.values()) == 7
    broken = deepcopy(specs)
    broken[recorder.THEORY]["full_experiment_status"] = "not_reproduced_high_cost"
    with pytest.raises(ValueError, match="cost/eligibility"):
        recorder.validate_execution(broken)


@pytest.mark.parametrize("key", sorted(COMPONENTS))
def test_all_selected_papers_have_paired_original_figure_blocks(key):
    spec = recorder.specifications()[key]
    for name in ("README.md", "README-en.md"):
        text = (ROOT / "docs" / Path(spec["detail_path"]).parent / name).read_text()
        assert text.count("<!-- paper-figure:start -->") == 1
        assert text.count("<!-- paper-figure:end -->") == 1
        assert text.index("<!-- paper-figure:start -->") < text.index("<!-- paper-figure:end -->")
        assert "assets/paper-figure-01.png" in text


def test_portable_record_check_does_not_reread_captures(monkeypatch):
    def forbidden(_receipts):
        raise AssertionError("portable --check must not reread .cache bytes")
    monkeypatch.setattr(recorder, "verify_captures", forbidden)
    recorder.record(check_only=True)


def test_source_recheck_is_explicit_and_required_for_initial_admission(monkeypatch):
    calls = []
    monkeypatch.setattr(recorder, "verify_captures", lambda rows: calls.append(rows))
    specs = recorder.specifications()
    recorder.validate_sources(specs, reread_captures=False)
    assert calls == []
    recorder.validate_sources(specs, reread_captures=True)
    assert len(calls) == 1 and len(calls[0]) >= 8
    recorder.record(check_only=True, recheck_source_captures=True)
    assert len(calls) == 2
    with pytest.raises(ValueError, match="immutable"):
        recorder.record()
    assert len(calls) == 3


def test_capture_byte_recheck_rejects_changed_and_missing_files(monkeypatch, tmp_path):
    path = tmp_path / ".cache/nov12-components/public.html"
    path.parent.mkdir(parents=True)
    path.write_bytes(b"fixed public source")
    row = {"capture": path.relative_to(tmp_path).as_posix(),
           "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    monkeypatch.setattr(recorder, "ROOT", tmp_path)
    recorder.verify_captures([row])
    path.write_bytes(b"changed")
    with pytest.raises(ValueError, match="missing/changed"):
        recorder.verify_captures([row])
    path.unlink()
    with pytest.raises(ValueError, match="fresh clone"):
        recorder.verify_captures([row])


@pytest.mark.parametrize("field,value", [
    ("accepted", True), ("implemented", True), ("blocks_watermark", True),
    ("resolution", "quantified_production_evidence_accepted"),
])
def test_unconfirmed_industrial_conflict_cannot_be_promoted(monkeypatch, field, value):
    original = recorder.load
    def load_changed(path):
        payload = original(path)
        if path.name == "industrial-source-exception.json":
            payload = deepcopy(payload)
            payload[field] = value
        return payload
    monkeypatch.setattr(recorder, "load", load_changed)
    with pytest.raises(ValueError, match="timeline cannot be promoted"):
        recorder.record(check_only=True)


def test_fixed_scope_and_archived_exception_are_separate():
    scope = read("task-scope.json")
    assert scope["counts"]["selected_papers"] == 8
    assert scope["counts"]["same_announcement_carryovers"] == 6
    assert scope["counts"]["official_source_historical_backfills"] == 2
    assert scope["counts"]["new_first_publications_since_prior_delivery"] == 0
    assert scope["review_watermark"] == {"before": "2026-11-09", "after": "2026-11-09"}
    assert {row["key"] for row in scope["papers"]} == set(COMPONENTS)
    assert "2609.04961" not in {row["id"] for row in scope["papers"]}
    assert scope["exceptions"][0]["id"] == "2609.04961"
    assert scope["exceptions"][0]["priority"] == "P2"
    assert scope["exceptions"][0]["accepted"] is False
    assert all(row["full_capability_reproduced"] is False for row in scope["papers"])


def test_announcement_pool_is_not_an_implementation_queue():
    source, index = read("source-coverage.json"), read("announcement-index.json")
    assert source["full_window_review_complete"] is False
    assert source["review_watermark_advanced"] is False
    assert index["all_candidates_method_reviewed"] is False
    assert index["automatic_implementation_queue"] is False
    assert index["is_new_announcement_relative_to_prior_batch"] is False
