"""Read-only research registration must not grant execution or acceptance."""
from __future__ import annotations

import json
import hashlib
import struct
from pathlib import Path

import pytest

from auto_research.paper_specs.catalog import catalog_records
from auto_research.paper_specs.runtime import spec_index
from auto_research.reproductions.registry import list_adapters

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "unisgr-v2": ("recommendation", "2610.16132", "2026-10-12"),
    "snap-dpa-relevance": ("recommendation", "2610.14550", "2026-10-10"),
    "ev-jepa": ("foundation-models", "2610.14324", "2026-10-09"),
    "loopsd": ("post-training", "2610.18162", "2026-10-13"),
    "rsipo": ("agent-research", "2610.15772", "2026-10-11"),
}


@pytest.mark.parametrize("key", PAPERS)
def test_deferred_research_is_visible_but_not_executable(key):
    domain, arxiv_id, published = PAPERS[key]
    row = next(row for row in catalog_records() if row["key"] == key)
    assert row["domain"] == domain
    assert row["published"] == published
    assert row["paper_url"] == f"https://arxiv.org/abs/{arxiv_id}"
    assert row["implementation_status"] == "deferred_high_cost"
    assert "成本过高，暂不复现" in row["deferral_reason"]
    assert row.get("adapter") is None
    assert row["gpu_validation_passed"] is False
    assert key not in spec_index()
    assert key not in {adapter.key for adapter in list_adapters()}

    archive = ROOT / row["deferred_execution_spec"]
    plan = json.loads(archive.read_text(encoding="utf-8"))
    assert plan["kind"] == "deferred_reproduction_plan"
    assert plan["fidelity_is_planned_only"] is True
    assert plan["execution"]["enabled"] is False
    assert plan["execution"]["requires_gpu_validation"] is True
    assert plan["execution"]["gpu_validation_artifact"] is None
    assert plan["cost_assessment"]["measured_locally"] is False
    assert plan["cost_assessment"]["downloads_started"] is False
    assert plan["cost_assessment"]["experiments_started"] is False
    assert plan["evolve_operators"] == []
    assert not archive.with_name("paper.yaml").exists()
    assert not archive.with_name("adapter.py").exists()

    text = (ROOT / "docs" / row["detail_path"]).read_text(encoding="utf-8")
    for heading in (
        "## 论文信息", "## 原始论文总结", "### 背景与主要改动",
        "### 核心公式", "### 论文离线与线上效果", "## 本地复现",
    ):
        assert heading in text
    for field in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码",
                  "Adapter", "本地复现代码"):
        assert f"| {field} |" in text
    assert "待验收" in text and "尚无算法实现" in text
    assert "没有本地指标" in text
    assert text.count(chr(96) * 3 + "mermaid") == 1
    assert text.count(chr(96) * 3) == 2
    assert ("\\" + chr(96)) * 3 not in text
    assert r"\[" not in text and r"\]" not in text
    assert r"\(" not in text and r"\)" not in text
    figure = json.loads((ROOT / "docs" / row["detail_path"]).with_name("figure-source.json")
                        .read_text(encoding="utf-8"))
    asset = (ROOT / "docs" / row["detail_path"]).parent / figure["local_asset"]
    body = asset.read_bytes()
    assert hashlib.sha256(body).hexdigest() == figure["local_asset_sha256"]
    assert body[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(body) >= 5_000
    width, height = struct.unpack(">II", body[16:24])
    assert (width, height) == (figure["width"], figure["height"])
    assert width >= 400 and height >= 140
    assert figure["visual_verified"] is True
    assert figure["version"] == "v1" and figure["paper_id"] == arxiv_id
    assert figure["source_resource"].startswith(f"https://arxiv.org/html/{arxiv_id}v1/")
    assert len(figure["source_resource_sha256"]) == 64


def test_rsipo_uses_first_author_affiliation_and_declares_official_code():
    row = next(row for row in catalog_records() if row["key"] == "rsipo")
    assert row["first_author"] == "Fan Zhang"
    assert row["first_author_affiliation"] == "Chinese University of Hong Kong"
    assert row["code"] == "https://github.com/zfkarl/RSIPO"
    text = (ROOT / "docs" / row["detail_path"]).read_text(encoding="utf-8")
    assert r"\mathbf1\{R(\tau)=1\}\cdot" in text


def test_loopsd_preserves_pdf_affiliation_not_an_email_domain_guess():
    row = next(row for row in catalog_records() if row["key"] == "loopsd")
    assert row["first_author"] == "Wei Fan"
    assert row["first_author_affiliation"] == "Anhui Province Key Laboratory of Digital Security"


def test_netflix_does_not_bypass_industrial_production_gate():
    excluded = json.loads(
        (ROOT / "docs/research-audits/oct14-screening/netflix-sid-excluded.json")
        .read_text(encoding="utf-8")
    )
    assert excluded["status"] == "excluded_missing_online_ab"
    assert excluded["evidence"]["quantified_production_control_found"] is False
    assert excluded["adapter_registered"] is False
    assert excluded["evolve_integrated"] is False
    assert not any(row["paper_url"].endswith("/2610.15864")
                   for row in catalog_records())

