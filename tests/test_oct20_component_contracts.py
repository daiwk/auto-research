"""Bounded scope, portable executed-source proofs and tamper rejection."""
from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.gpu_validation import load_gpu_receipt

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct20_evidence", ROOT / "scripts/curate_oct20_component_evidence.py")
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)
COMPONENTS = {key for _, _, items in admission.GROUPS.values() for key in items}


def metric_for(key):
    path = ROOT / admission.metric_path(key)
    assert path.is_file(), f"real measured evidence required: {path}"
    return json.loads(path.read_text())


def test_fixed_scope_and_original_figures_and_no_fake_references():
    assert len(COMPONENTS) == 10 and len(admission.REFERENCES) == 3
    assert COMPONENTS | admission.REFERENCES == set(admission.COSTS)
    for key in admission.COSTS:
        row = admission.catalog_for(key)
        assert row["full_experiment_status"] == "not_reproduced_high_cost" and row["review_done"] is True
        assert row["diagnostic_only"] is True and row["promotion_eligible"] is False and row["evolve_integrated"] is False
        assert row["published_at"] and row["first_author_affiliation"]
        text = (ROOT / "docs" / row["detail_path"]).read_text()
        for token in ("## 论文信息", "### 背景与主要改动", "### 核心公式", "不复现", "DONE", "assets/paper-figure-01.png"):
            assert token in text, (key, token)
        if key in admission.REFERENCES:
            assert row["implementation_status"] == "deferred_high_cost" and row["adapter"] is None
            assert not row.get("local_operator") and not row.get("requires_gpu_validation") and not row.get("gpu_validation_artifact")
        else:
            module, member = row["local_operator"].rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), member))
            if key != "sid-topology":
                assert row["adapter"] is None


@pytest.mark.parametrize("key", sorted(COMPONENTS))
def test_actual_curated_evidence_portable_to_shallow_squash_clone(key):
    admission.validate_curated(metric_for(key), key)


@pytest.mark.parametrize("key", ["t-muon", "time-jepa", "kronlstm", "muse-glimmer-30b"])
def test_foundation_browse_dimensions_include_new_papers(key):
    stem = Path(admission.catalog_for(key)["detail_path"]).parent.name
    for dimension in ("organization", "topic", "year"):
        assert stem in (ROOT / f"docs/foundation-models/catalog/by-{dimension}.md").read_text()


@pytest.mark.parametrize("key", ["sid-topology", "maps-creative"])
def test_recommendation_components_and_reference_are_visible_in_all_browse_dimensions(key):
    stem = Path(admission.catalog_for(key)["detail_path"]).parent.name
    for dimension in ("company", "topic", "month"):
        text = (ROOT / f"docs/reproductions/catalog/by-{dimension}.md").read_text()
        assert stem in text
        if key == "maps-creative":
            line = next(line for line in text.splitlines() if stem in line)
            assert "不复现（审查 DONE）" in line and "无可执行入口" in line

@pytest.mark.parametrize("mutation", ["promotion", "seed", "metric", "source", "dataset", "rehashed-dataset", "raw-trajectory", "tier", "formal-comparison"])
def test_mutated_curated_evidence_rejected(mutation):
    metric = deepcopy(metric_for("sid-topology"))
    if mutation == "promotion":
        metric["promotion_eligible"] = True
    elif mutation == "seed":
        metric["per_seed"][1]["seed"] = 42
    elif mutation == "metric":
        metric["metrics"]["full_remap_old_address_losses"]["mean"] += 1
    elif mutation == "source":
        name = next(iter(metric["provenance"]["executed_source_sha256"]))
        metric["provenance"]["executed_source_sha256"][name] = "0" * 64
    elif mutation == "dataset":
        metric["dataset"]["revision"] += "changed"
    elif mutation == "rehashed-dataset":
        metric["dataset"]["id"] = "synthetic-wrong-recipe"
        metric["dataset"]["revision"] = "unrelated-v900"
        metric["provenance"]["dataset_fingerprint"] = admission.generated_input_fingerprint(
            metric["dataset"], metric["provenance"]["executed_source_sha256"])
    elif mutation == "tier":
        metric["evaluation_tier"] = metric["evaluation_protocol"]["tier"] = "l2_public_benchmark"
    elif mutation == "formal-comparison":
        metric["evaluation_protocol"]["formal_comparison"] = True
    else:
        metric["per_seed"][0]["raw_rollout"] = ["unexpected large trace"]
    with pytest.raises(ValueError):
        admission.validate_curated(metric, "sid-topology")


@pytest.mark.parametrize("mutation", ["metric", "accelerator", "command", "dataset", "checkpoint", "full-experiment", "raw-hash", "recipe-hash"])
def test_mutated_gpu_receipt_rejected(mutation):
    key = "spod"
    metric = metric_for(key)
    receipt = deepcopy(load_gpu_receipt(ROOT / admission.catalog_for(key)["gpu_validation_artifact"]))
    if mutation == "metric":
        receipt["metrics"]["parameter_delta_l2"]["mean"] += 1
    elif mutation == "accelerator":
        receipt["accelerator"]["model"] = "CPU"
    elif mutation == "command":
        receipt["command"][1] = "different.py"
    elif mutation == "dataset":
        receipt["dataset"]["revision"] = "changed"
    elif mutation == "full-experiment":
        receipt["full_experiment_status"] = "fully_reproduced"
    elif mutation in ("raw-hash", "recipe-hash"):
        receipt["provenance"]["raw_runner_artifact_sha256" if mutation == "raw-hash" else "dataset_fingerprint"] = "0" * 64
    else:
        receipt["checkpoint"]["pretrained"] = True
    with pytest.raises(ValueError):
        admission.validate_receipt_binding(receipt, metric, key)


def test_metric_raw_hash_must_match_separate_gpu_receipt():
    metric = deepcopy(metric_for("spod"))
    metric["provenance"]["raw_runner_artifact_sha256"] = "0" * 64
    with pytest.raises(ValueError):
        admission.validate_curated(metric, "spod")


def test_defining_checks_do_not_accept_faked_success_or_nan():
    good = metric_for("spod")["per_seed"][0]["metrics"]
    for name, value in (("teacher_parameter_delta_l2", 1.), ("parameter_delta_l2", 0.),
                        ("optimizer_updates", 0), ("loss_reference_max_abs_error", float("nan"))):
        with pytest.raises(ValueError):
            admission.validate_outcomes("spod", {**good, name: value})


def test_batch_does_not_advance_watermark_or_requeue_high_cost_full_experiments():
    ledger = json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())
    batch = next(b for b in ledger["batches"] if b["batch"] == admission.BATCH)
    assert len(batch["candidates"]) == 13 and not batch["coverage_complete"] and not batch["review_watermark_advanced"]
    assert set(batch["required_tracks"]) <= {row["track"] for row in batch["candidates"]}
    assert batch["component_validation_counts"] == {"gpu_validated_components": 6, "cpu_validated_components_or_interfaces": 4, "review_only": 3}
    for row in batch["candidates"]:
        assert row["review_done"] and row["terminal"] and row["status"] == "deferred"
        assert not row["automatic_retry"] and not row["automatic_implementation_queue"]

def test_latest_source_receipts_and_directory_changes_do_not_inflate_new_papers():
    audit = json.loads((admission.AUDIT / "source-coverage.json").read_text())
    assert audit["latest_observed_arxiv_announcement"] == "2026-10-20"
    assert not audit["all_sources_exhaustive"] and not audit["review_watermark"]["advanced"]
    assert len(audit["arxiv_sources"]) == 8
    assert all(r["parse_complete"] and r["expected_entries"] == r["parsed_entries"]
               for r in audit["arxiv_sources"])
    assert audit["counts"]["selected_papers"] == 13
    assert audit["counts"]["category_entries_including_crosslists_and_replacements"] == 2920
    meta = next(row for row in audit["official_directory_deltas"] if row["organization"] == "Meta")
    assert meta["attempted_pages"] == 6 and not meta["all_sources_exhaustive"]
