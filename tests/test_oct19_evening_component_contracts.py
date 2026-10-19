"""Bounded scope, portable executed-source proofs and tamper rejection."""
from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path

import pytest

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.reproductions.registry import get_adapter

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("oct19_evening_evidence", ROOT / "scripts/curate_oct19_evening_component_evidence.py")
admission = importlib.util.module_from_spec(spec)
spec.loader.exec_module(admission)
COMPONENTS = {key for _, _, items in admission.GROUPS.values() for key in items}


def metric_for(key):
    path = ROOT / admission.metric_path(key)
    assert path.is_file(), f"real measured evidence required: {path}"
    return json.loads(path.read_text())


def test_fixed_scope_and_original_figures_and_no_fake_references():
    assert len(COMPONENTS) == 11 and len(admission.REFERENCES) == 3
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
            if key != "unirec-v3-components":
                assert row["adapter"] is None


@pytest.mark.parametrize("key", sorted(COMPONENTS))
def test_actual_curated_evidence_portable_to_shallow_squash_clone(key):
    admission.validate_curated(metric_for(key), key)


@pytest.mark.parametrize("key", ["ego-p2c", "bmuon", "sink-sparse", "ppmem", "jev-portuguese-ir"])
def test_foundation_browse_dimensions_include_new_papers(key):
    stem = Path(admission.catalog_for(key)["detail_path"]).parent.name
    for dimension in ("organization", "topic", "year"):
        assert stem in (ROOT / f"docs/foundation-models/catalog/by-{dimension}.md").read_text()


def test_jev_protocol_reachable_from_its_topic_and_all_browse_dimensions():
    stem = "2610.23346-jev-portuguese-ir"
    for path in ("README.md", "catalog.md", "catalog/by-organization.md", "catalog/by-topic.md", "catalog/by-year.md"):
        assert stem in (ROOT / "docs/system-one" / path).read_text()


@pytest.mark.parametrize("mutation", ["promotion", "seed", "metric", "source", "dataset", "raw-trajectory", "tier", "formal-comparison"])
def test_mutated_curated_evidence_rejected(mutation):
    metric = deepcopy(metric_for("unirec-v3-components"))
    if mutation == "promotion":
        metric["promotion_eligible"] = True
    elif mutation == "seed":
        metric["per_seed"][1]["seed"] = 42
    elif mutation == "metric":
        metric["metrics"]["score_update_norm"]["mean"] += 1
    elif mutation == "source":
        name = next(iter(metric["provenance"]["executed_source_sha256"]))
        metric["provenance"]["executed_source_sha256"][name] = "0" * 64
    elif mutation == "dataset":
        metric["dataset"]["revision"] += "changed"
    elif mutation == "tier":
        metric["evaluation_tier"] = metric["evaluation_protocol"]["tier"] = "l2_public_benchmark"
    elif mutation == "formal-comparison":
        metric["evaluation_protocol"]["formal_comparison"] = True
    else:
        metric["per_seed"][0]["raw_rollout"] = ["unexpected large trace"]
    with pytest.raises(ValueError):
        admission.validate_curated(metric, "unirec-v3-components")


@pytest.mark.parametrize("mutation", ["metric", "accelerator", "command", "dataset", "checkpoint", "full-experiment"])
def test_mutated_gpu_receipt_rejected(mutation):
    key = "unirec-v3-components"
    metric = metric_for(key)
    receipt = deepcopy(load_gpu_receipt(ROOT / admission.catalog_for(key)["gpu_validation_artifact"]))
    if mutation == "metric":
        receipt["metrics"]["score_update_norm"]["mean"] += 1
    elif mutation == "accelerator":
        receipt["accelerator"]["model"] = "CPU"
    elif mutation == "command":
        receipt["command"][1] = "different.py"
    elif mutation == "dataset":
        receipt["dataset"]["revision"] = "changed"
    elif mutation == "full-experiment":
        receipt["full_experiment_status"] = "fully_reproduced"
    else:
        receipt["checkpoint"]["pretrained"] = True
    with pytest.raises(ValueError):
        admission.validate_receipt_binding(receipt, metric, key)


def test_defining_checks_do_not_accept_faked_success_or_nan():
    good = metric_for("simopd")["per_seed"][0]["metrics"]
    for name, value in (("teacher_parameter_delta_l2", 1.), ("parameter_delta_l2", 0.),
                        ("optimizer_updates", 0), ("loss_reference_max_abs_error", float("nan"))):
        with pytest.raises(ValueError):
            admission.validate_outcomes("simopd", {**good, name: value})


def test_unirec_legacy_fixed_scorer_remains_diagnostic_negative_result():
    adapter = get_adapter("unirec")
    assert adapter.fidelity.value == "concept_demo"
    result = json.loads((ROOT / "docs/reproductions/2609.11052-unirec/metrics/movielens-100k-seeds42-44.json").read_text())
    assert result["diagnostic_only"] and not result["evaluation_protocol"]["formal_comparison"]
    assert all(row["relative"]["ndcg_at_10_percent"] < 0 for row in result["runs"])


def test_jev_published_table_arithmetic_is_not_inference():
    audit = json.loads((admission.AUDIT / "jev-published-table-arithmetic.json").read_text())
    assert not audit["new_model_inference"] and sum(row["judgments"] for row in audit["tables"].values()) == 13200
    for row in metric_for("jev-portuguese-ir")["per_seed"]:
        assert row["metrics"]["language_model_evaluated"] is False and row["metrics"]["real_backend_used"] is False


def test_batch_does_not_advance_watermark_or_requeue_high_cost_full_experiments():
    ledger = json.loads((ROOT / "docs/paper-discovery-ledger.json").read_text())
    batch = next(b for b in ledger["batches"] if b["batch"] == admission.BATCH)
    assert len(batch["candidates"]) == 14 and not batch["coverage_complete"] and not batch["review_watermark_advanced"]
    assert batch["component_validation_counts"] == {"gpu_validated_components": 7, "cpu_validated_components_or_interfaces": 4, "review_only": 3}
    for row in batch["candidates"]:
        assert row["review_done"] and row["terminal"] and row["status"] == "deferred"
        assert not row["automatic_retry"] and not row["automatic_implementation_queue"]
