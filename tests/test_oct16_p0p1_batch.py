"""Accepted scope is 2 P0 + 12 P1 + one existing TransX upgrade, not 15 full runs."""
from __future__ import annotations

import hashlib
import importlib
import json
from pathlib import Path
import re

from auto_research.gpu_validation import load_gpu_receipt
from auto_research.paper_specs.catalog import catalog_records

ROOT = Path(__file__).resolve().parents[1]
KEYS = {
    "static-constraint-decoding", "cross-task-relationships", "transx",
    "novelty-patching", "rope-relay", "cots", "tf-opd", "waypoint-opd",
    "ggpo", "stopd", "cce-opd", "sif", "tool-bottleneck-bench", "librarian-agents", "scipivot",
}
CPU_ONLY = {"novelty-patching", "tool-bottleneck-bench", "librarian-agents", "scipivot"}


def selected():
    return {row["key"]: row for row in catalog_records() if row["key"] in KEYS}


def test_all_fifteen_have_real_operators_metadata_cost_boundaries_and_metrics():
    records = selected()
    assert set(records) == KEYS
    for key, row in records.items():
        assert row["full_experiment_status"] == "not_reproduced_high_cost", key
        assert row["evolve_integrated"] is False, key
        assert row["first_author_affiliation"]
        detail = ROOT / "docs" / row["detail_path"]
        text = detail.read_text()
        assert "不复现" in text and "DONE" in text
        assert "本地复现代码" in text
        assert "原作者代码" in text or "原文开源代码" in text
        assert "paper-figure:start" in text
        assert list((detail.parent / "metrics").glob("*.json")), key
        module, attribute = row["local_operator"].rsplit(".", 1)
        assert callable(getattr(importlib.import_module(module), attribute))
        if key != "transx":
            assert row["adapter"] is None
            assert row["published"] in text


def test_eleven_cuda_paths_bind_matching_sanitized_executed_source():
    records = selected()
    assert {key for key, row in records.items() if row.get("requires_gpu_validation")} == KEYS - CPU_ONLY
    for key in KEYS - CPU_ONLY:
        row = records[key]
        receipt = load_gpu_receipt(ROOT / row["gpu_validation_artifact"])
        assert receipt["adapter_key"] == row.get("component_key", key)
        assert receipt["seeds"] == [42, 43, 44]
        assert receipt["diagnostic_only"] is True
        assert receipt["promotion_eligible"] is False
        for path, digest in receipt["executed_source_sha256"].items():
            assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path


def test_browse_dimensions_include_each_new_component_once():
    for key, row in selected().items():
        if key == "transx":
            continue  # Existing adapter has the stronger original catalog test.
        expected = (ROOT / "docs" / row["detail_path"]).resolve()
        if row["domain"] == "recommendation":
            paths = [ROOT / "docs/reproductions/catalog" / f"by-{name}.md" for name in ("company", "topic", "month")]
        else:
            paths = [ROOT / "docs" / row["domain"] / "catalog" / f"by-{name}.md"
                     for name in ("organization", "topic", "year")]
        for path in paths:
            links = re.findall(r"\]\(([^)]+)\)", path.read_text())
            assert sum((path.parent / href).resolve() == expected for href in links) == 1, (key, path)


def test_transx_legacy_measurements_retained_but_not_formal_training_evidence():
    legacy = json.loads((ROOT / "docs/reproductions/2607.28940-transx/metrics/public-seeds42-44.json").read_text())
    assert legacy["method"]["ndcg_at_10"] == 0.04475488754459977
    assert legacy["diagnostic_only"] is True
    assert legacy["evaluation_protocol"]["formal_comparison"] is False
    row = selected()["transx"]
    assert row["adapter"]["fidelity"] == "concept_demo"
    assert len(row["supplemental_papers"]) == 1
