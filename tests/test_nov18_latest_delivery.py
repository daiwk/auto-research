"""Finite intake completeness and immutable evidence, not capability certification."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from run_nov18_latest_components import AUDIT, config, load, source_hashes, validate_raw
from curate_nov18_latest_evidence import main as curate
from close_nov18_latest_intake import learning_counts
from oct18_frozen_sources import verify_sources


def test_complete_exact_intake_and_learning():
    scope = load(AUDIT / "task-scope.json")
    counts = scope["counts"]
    assert scope["selected_scope_complete"] is True
    assert len(scope["accepted_papers"]) == len(set(scope["accepted_papers"])) == 47
    assert counts == {
        "accepted_papers": 47,
        "new_papers": 46,
        "historical_new_code": 1,
        "low_cost_components": 35,
        "cuda_components": 22,
        "high_cost_review_only": 12,
        "authored_bilingual_questions": 189,
        "same_topic_deep_dive_updates": 47,
        "full_capability_reproductions": 0,
    }
    assert learning_counts() == {
        "authored_bilingual_questions": 189,
        "same_topic_deep_dive_updates": 47,
    }
    assert not scope["all_sources_exhaustive"] and not scope["watermark_advanced"]
    for p in scope["papers"]:
        assert (
            p["review_done"]
            and not p["automatic_implementation_queue"]
            and not p["automatic_retry"]
        )
        assert not p["promotion_eligible"] and not p["evolve_integrated"]
        assert p["full_experiment_status"] == "not_reproduced_high_cost"


def test_actual_frozen_cpu_and_a100_runs():
    frozen = load(AUDIT / "frozen-sources.json")
    assert frozen["source_sha256"] == source_hashes()
    verify_sources(ROOT, frozen["commit"], frozen["source_sha256"], frozen["proof"])
    cfg = config()
    assert len(cfg["components"]) == 35 and sum(r["cuda"] for r in cfg["components"].values()) == 22
    for device in ("cpu", "cuda"):
        raw = load(AUDIT / f"raw-{device}.json")
        validate_raw(raw, frozen)
        assert raw["elapsed_seconds"] <= 180
        assert len(raw["components"]) == (35 if device == "cpu" else 22)
    assert load(AUDIT / "raw-cuda.json")["accelerator"].startswith(("NVIDIA A100", "NVIDIA A30"))


@pytest.mark.parametrize(
    "mutation",
    ["promotion", "missing_component", "wrong_seed", "false_check", "nan", "fake_device", "tier"],
)
def test_admission_rejects_tampered_actual_run(mutation):
    frozen = load(AUDIT / "frozen-sources.json")
    raw = deepcopy(load(AUDIT / "raw-cuda.json"))
    key = next(iter(raw["components"]))
    row = raw["components"][key]["per_seed"][0]
    if mutation == "promotion":
        raw["promotion_eligible"] = True
    elif mutation == "missing_component":
        del raw["components"][key]
    elif mutation == "wrong_seed":
        row["seed"] = 99
    elif mutation == "false_check":
        row["checks"][next(iter(row["checks"]))] = False
    elif mutation == "nan":
        row["metrics"][next(iter(row["metrics"]))] = float("nan")
    elif mutation == "fake_device":
        raw["accelerator"] = "CPU"
    else:
        row["evaluation_tier"] = "l2_capability"
    with pytest.raises(ValueError):
        validate_raw(raw, frozen)


def test_superseded_incorrect_quantizer_is_not_admitted():
    old = load(AUDIT / "superseded-run.json")
    new = load(AUDIT / "frozen-sources.json")
    assert (
        old["status"] == "superseded_not_admitted"
        and old["cuda_run_executed_for_superseded_source"] is False
    )
    assert old["source_commit"] != new["commit"]
    oldproof = load(AUDIT / "superseded/frozen-sources-66cda008.json")
    path = "src/auto_research/foundation_models/wm_quant.py"
    assert oldproof["source_sha256"][path] != new["source_sha256"][path]
    assert new["source_sha256"][path] == hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def test_metadata_is_not_backlog_or_exhaustion_claim():
    metadata = load(AUDIT / "metadata-index.json")
    coverage = load(AUDIT / "source-coverage.json")
    assert (
        metadata["metadata_only"] and not metadata["metadata_inventory_is_implementation_backlog"]
    )
    assert not coverage["all_sources_exhaustive"] and not coverage["watermark_advanced"]
    priority = load(AUDIT / "priority-primary-selection.json")
    assert priority["meta_new_paper"]["id"] == "2611.21839"
    assert priority["google_new_repository"]["paper"] == "2603.02029"
    assert priority["google_new_repository"]["published_at"] == "2026-03-02T16:12:46Z"
    assert priority["google_new_repository"]["resolution"] == "historical_new_code_accepted"
