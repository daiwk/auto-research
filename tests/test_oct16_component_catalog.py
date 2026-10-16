"""Keep the eight accepted P1 items and their evidence boundaries together."""
from __future__ import annotations

import json
from pathlib import Path
import re

from auto_research.paper_specs.catalog import catalog_records
from auto_research.reproductions.registry import get_adapter

ROOT = Path(__file__).resolve().parents[1]
KEYS = {
    "oob-regularization", "transparent-compact", "formcraft",
    "divergence-routed-opd", "rap-walk", "ctxgap",
    "selective-reasoning", "clasharness",
}


def test_all_eight_p1_items_have_complete_catalog_and_cost_boundaries():
    records = {row["key"]: row for row in catalog_records() if row["key"] in KEYS}
    assert set(records) == KEYS
    for key, row in records.items():
        assert row["full_experiment_status"] == "not_reproduced_high_cost", key
        assert row.get("evolve_integrated") is False, key
        detail = ROOT / "docs" / row["detail_path"]
        text = detail.read_text(encoding="utf-8")
        assert "不复现" in text and "DONE" in text, key
        assert "paper-figure:start" in text, key
        assert row["first_author_affiliation"], key
        assert row["published"][:10] in text, key
        assert "原作者代码" in text or "原文开源代码" in text, key
        assert "本地复现代码" in text, key
        if key != "oob-regularization":
            assert row["adapter"] is None, key


def test_cuda_components_bind_real_receipts_and_routed_opd_has_distinct_identity():
    records = {row["key"]: row for row in catalog_records() if row["key"] in KEYS}
    expected = {"oob-regularization", "divergence-routed-opd", "rap-walk"}
    assert {key for key, row in records.items() if row.get("requires_gpu_validation")} == expected
    for key in expected:
        row = records[key]
        receipt = json.loads((ROOT / row["gpu_validation_artifact"]).read_text())
        assert receipt["adapter_key"] == key
        assert receipt["accelerator"]["vendor"] == "NVIDIA"
        assert receipt["result"] == "passed"
        assert receipt["executed_source_sha256"]
        assert receipt["provenance"]["commit"]
    assert "2610.19572" in records["divergence-routed-opd"]["paper_url"]
    old = next(row for row in catalog_records() if row["key"] == "dr-opd")
    assert "2609.38025" in old["paper_url"]
    adapter = get_adapter("oob-regularization")
    assert adapter.requires_gpu_validation is True


def test_replays_do_not_advertise_new_model_capability_or_evolve_integration():
    records = {row["key"]: row for row in catalog_records() if row["key"] in KEYS}
    for key in ("ctxgap", "clasharness", "selective-reasoning"):
        row = records[key]
        assert row["implementation_status"] == "evaluation_protocol_interface"
        assert row["adapter"] is None
        assert row["evolve_integrated"] is False


def test_all_eight_are_visible_in_each_domain_browse_dimension():
    for row in catalog_records():
        if row["key"] not in KEYS:
            continue
        expected = (ROOT / "docs" / row["detail_path"]).resolve()
        for dimension in ("organization", "topic", "year"):
            path = ROOT / "docs" / row["domain"] / "catalog" / f"by-{dimension}.md"
            links = re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8"))
            found = [link for link in links if (path.parent / link).resolve() == expected]
            assert len(found) == 1, (row["key"], dimension)


def test_raw_validation_or_official_reference_imports_are_not_public_experiment_cards():
    payload = json.loads((ROOT / "docs/assets/data/experiment-dashboard.json").read_text())
    assert all("validation" not in Path(row["path"]).parts for row in payload["experiments"])
    for row in payload["experiments"]:
        if row["method"] in KEYS:
            assert row["evidence"]["diagnostic_only"] is True
            assert row["evidence"]["formal_comparison"] is False
