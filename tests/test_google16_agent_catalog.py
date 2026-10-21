import hashlib
import importlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
KEYS = ("dynamic-brt", "causal-armor", "polca", "hcrg")


@pytest.mark.parametrize("key", KEYS)
def test_google16_agent_components_have_complete_metadata_and_honest_boundaries(key):
    row = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research" /
                      f"{key}.json").read_text())
    assert row["adapter"] is None and row["implementation_status"] == "component_only"
    assert row["review_done"] is True and row["full_experiment_status"] == "not_reproduced_high_cost"
    assert row["diagnostic_only"] and not row["promotion_eligible"] and not row["evolve_integrated"]
    assert row["first_author"] and row["first_author_affiliation"] and row["code_status"]
    assert row["published_at"].startswith(row["published"])
    module, name = row["local_operator"].rsplit(".", 1)
    assert callable(getattr(importlib.import_module(module), name))
    detail = ROOT / "docs" / row["detail_path"]
    text = detail.read_text()
    for section in ("论文信息", "原始论文总结", "背景与主要改动", "核心公式",
                    "论文离线与线上效果", "本地复现", "成本过高，不复现（审查 DONE）"):
        assert section in text
    for metadata in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "本地 Adapter", "本地复现代码"):
        assert metadata in text
    metric = json.loads((detail.parent / "metrics/component-contract.json").read_text())
    assert metric["schema_version"] == 2 and metric["diagnostic_only"]
    assert not metric["formal_comparison"] and not metric["evolve_integrated"]
    assert metric["full_experiment_status"] == "not_reproduced_high_cost"
    provenance = json.loads((detail.parent / "assets/provenance.json").read_text())
    image = detail.parent / "assets" / provenance["asset"]
    assert image.is_file() and hashlib.sha256(image.read_bytes()).hexdigest() == provenance["asset_sha256"]
    assert provenance["source_pdf_url"].startswith("https://arxiv.org/pdf/")
    assert "assets/paper-figure-01.png" in text and "版权归作者" in text
    assert row["requires_gpu_validation"] == (key == "causal-armor")


def test_first_author_affiliation_not_google_coauthor_inheritance():
    catalog = ROOT / "src/auto_research/paper_specs/catalog/agent-research"
    polca = json.loads((catalog / "polca.json").read_text())
    armor = json.loads((catalog / "causal-armor.json").read_text())
    assert polca["first_author_affiliation"] == "University of Wisconsin-Madison"
    assert armor["first_author_affiliation"] == "Google Cloud AI Research"
    assert "Seoul National University" in armor["authorship_note"]
