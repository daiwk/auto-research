"""Accepted 9 operators, 2 interfaces, 3 references: no silent omissions/promotions."""
from __future__ import annotations

import hashlib
from copy import deepcopy
import importlib
import importlib.util
import json
from pathlib import Path
import re
import statistics

import pytest

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.paper_specs.catalog import catalog_records

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = {"prism-1", "langdit", "oprd-reminder", "opcredit", "structural-signal-retriever",
              "rsiflow", "leash", "probe", "terminal-rsi"}
INTERFACES = {"gacc-bench", "muon-paired-budget"}
REFERENCES = {"gemini-minecraft", "hy-memory", "athanor"}
GPU = {"prism-1", "langdit", "oprd-reminder", "opcredit"}
ALL = COMPONENTS | INTERFACES | REFERENCES


def records():
    return {row["key"]: row for row in catalog_records() if row["key"] in ALL}


def metric_for(row):
    device = "cuda" if row["key"] in GPU else "cpu"
    return json.loads((ROOT / "docs" / row["detail_path"]).with_name("metrics").joinpath(
        f"component-{device}-seeds42-44.json").read_text())


def test_exact_accepted_scope_and_honest_executable_status():
    rows = records()
    assert set(rows) == ALL
    for key, row in rows.items():
        assert row["adapter"] is None, key
        assert row["full_experiment_status"] == "not_reproduced_high_cost", key
        assert row["diagnostic_only"] is True and row["promotion_eligible"] is False, key
        assert row["evolve_integrated"] is False, key
        assert row["published"] == "2026-10-15" and row["first_author_affiliation"], key
        if not row.get("code"):
            assert "未" in row.get("code_status", ""), key
        text = (ROOT / "docs" / row["detail_path"]).read_text()
        for token in ("## 论文信息", "## 原始论文总结", "### 核心公式", "## 本地复现", "不复现", "DONE",
                      "assets/paper-figure-01.png"):
            assert token in text, (key, token)
        if key in REFERENCES:
            assert row["implementation_status"] == "deferred_high_cost" and row["review_done"] is True
            assert not row.get("local_operator") and not row.get("local_command")
            assert not row.get("gpu_validation_artifact") and row["gpu_validation_passed"] is False
        else:
            expected = "evaluation_protocol_interface" if key in INTERFACES else "component_only"
            assert row["implementation_status"] == expected
            module, name = row["local_operator"].rsplit(".", 1)
            assert callable(getattr(importlib.import_module(module), name)), key
            assert row["local_command"], key


def test_existing_reverse_distillation_oprd_is_not_overwritten_by_reminder_paper():
    rows = {row["key"]: row for row in catalog_records()}
    assert "2609.08798" in rows["oprd"]["paper_url"]
    assert rows["oprd"]["adapter"] == "oprd"
    assert "2610.21496" in rows["oprd-reminder"]["paper_url"]


@pytest.mark.parametrize("key", sorted(COMPONENTS | INTERFACES))
def test_actual_per_paper_measurements_bind_current_source_and_recompute_statistics(key):
    row = records()[key]
    metric = metric_for(row)
    assert metric["method"] == key and metric["seeds"] == [42, 43, 44]
    assert metric["diagnostic_only"] is True and metric["promotion_eligible"] is False
    assert metric["evaluation_protocol"]["seeds"] == [42, 43, 44]
    assert metric["evaluation_protocol"]["formal_comparison"] is False
    assert [trial["seed"] for trial in metric["per_seed"]] == [42, 43, 44]
    hashes = metric["provenance"]["executed_source_sha256"]
    assert any(name.startswith("src/") for name in hashes) and any(name.startswith("scripts/") for name in hashes)
    for name, digest in hashes.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, (key, name)
    for field, aggregate in metric["metrics"].items():
        values = [trial["metrics"][field] for trial in metric["per_seed"]]
        if all(isinstance(value, bool) for value in values):
            assert aggregate is all(values)
        elif all(type(value) in (int, float) for value in values):
            assert aggregate["n"] == 3
            assert aggregate["mean"] == pytest.approx(statistics.mean(values), abs=1e-14)
            assert aggregate["std"] == pytest.approx(statistics.stdev(values), abs=1e-14)
    if key in GPU:
        assert row["requires_gpu_validation"] is True
        receipt = load_gpu_receipt(ROOT / row["gpu_validation_artifact"])
        assert receipt["adapter_key"] == key and receipt["metrics"] == metric["metrics"]
        assert receipt["executed_source_sha256"] == hashes
        assert any(gpu in receipt["accelerator"]["model"].upper() for gpu in ("A100", "A30"))
    else:
        assert row["requires_gpu_validation"] is False and not row.get("gpu_validation_artifact")


def test_all_fourteen_have_one_link_in_each_browse_dimension():
    for key, row in records().items():
        expected = (ROOT / "docs" / row["detail_path"]).resolve()
        for dimension in ("organization", "topic", "year"):
            page = ROOT / "docs" / row["domain"] / "catalog" / f"by-{dimension}.md"
            links = re.findall(r"\]\(([^)]+)\)", page.read_text())
            assert sum((page.parent / link).resolve() == expected for link in links) == 1, (key, dimension)


def admission_module():
    spec = importlib.util.spec_from_file_location("oct17_supplement_admission", ROOT / "scripts/curate_oct17_supplement_evidence.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("status", ["failed", "partial", "timeout", "skipped", "error"])
def test_curator_cannot_turn_execution_failure_into_pass(status):
    with pytest.raises(ValueError, match="failure"):
        admission_module().reject_failure({"status": status})


@pytest.mark.parametrize("key", sorted(GPU))
def test_curator_rechecks_actual_diagnostic_outcomes(key):
    module = admission_module()
    metrics = metric_for(records()[key])["per_seed"][0]["metrics"].copy()
    raw_key = "oprd" if key == "oprd-reminder" else key
    module.validate_measurement(raw_key, metrics)
    field = {"prism-1": "cross_option_attention_negative_control_error", "langdit": "codebook_update_norm",
             "oprd-reminder": "parameter_delta_l2", "opcredit": "parameter_delta_l2"}[key]
    metrics[field] = 0
    with pytest.raises(ValueError, match="positive"):
        module.validate_measurement(raw_key, metrics)


@pytest.mark.parametrize("mutation,reason", [
    ("failed_seed", "failure"), ("missing_seed", "per-seed"),
    ("edited_summary", "aggregate"), ("wrong_commit", "frozen source"),
])
def test_finalizer_rejects_corrupted_curated_artifacts(mutation, reason):
    module = admission_module()
    metric = deepcopy(metric_for(records()["structural-signal-retriever"]))
    if mutation == "failed_seed":
        metric["per_seed"][0]["status"] = "failed"
    elif mutation == "missing_seed":
        metric["per_seed"].pop()
    elif mutation == "edited_summary":
        metric["metrics"]["registry_cards"]["mean"] += 1
    else:
        metric["provenance"]["commit"] = "0" * 40
    with pytest.raises(ValueError, match=reason):
        module.validate_curated(metric, "structural-signal-retriever")
