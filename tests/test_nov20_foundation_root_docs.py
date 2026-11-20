"""Bilingual facts, source provenance and explicit non-capability boundaries."""

from hashlib import sha256
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov20-latest"
PAPERS = [
    ("foundation-models", "hisa"),
    ("foundation-models", "canon-layers-scale"),
    ("recommendation", "antom-3-in-1"),
    ("recommendation", "fleet-feature-optimization"),
    ("recommendation", "dna"),
    ("recommendation", "lser-serving"),
]


def spec(domain, key):
    return json.loads((ROOT / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json").read_text())


@pytest.mark.parametrize("domain,key", PAPERS)
def test_reviewed_bilingual_writeup_and_original_figure(domain, key):
    record = spec(domain, key)
    source = ROOT / "docs" / record["detail_path"]
    cn = source.read_bytes()
    en = (source.parent / "README-en.md").read_text()
    assert "<!-- source-sha256: " + sha256(cn).hexdigest() + " -->" in en
    assert "[简体中文](README.md)" in en
    for heading in ["论文信息", "背景与主要改动", "核心公式", "论文离线与线上效果",
                    "数据协议与代码映射", "同主题比较与边界", "高成本完整实验"]:
        assert heading in cn.decode()
    assert "成本过高，不复现（审查 DONE）" in cn.decode()
    assert "~~~mermaid" in cn.decode()
    provenance = json.loads((source.parent / "assets/provenance.json").read_text())
    assert provenance["source_url"] == record["reviewed_version_url"]
    assert provenance["source_pdf_sha256"] == record["method_source_sha256"]
    assert provenance["asset_sha256"] == sha256((source.parent / "assets/paper-figure-01.png").read_bytes()).hexdigest()
    assert provenance["page"] >= 1 and len(provenance["crop_box_pdf_points"]) == 4
    assert record["diagnostic_only"] is True and record["promotion_eligible"] is False
    assert record["evolve_integrated"] is False
    assert record["full_experiment_status"] == "not_reproduced_high_cost"
    assert record["automatic_retry"] is False
    if record["evaluation_tier"] == "review_only":
        assert record["local_operator"] is None
        assert record["requires_gpu_validation"] is False
        assert not (source.parent / "metrics").exists()


@pytest.mark.parametrize("name", ["foundation", "root"])
def test_authored_questions_have_four_levels_actual_sections_and_reviewed_english(name):
    bundle = json.loads((AUDIT / f"{name}-authored-bundle.json").read_text())
    assert len(bundle["papers"]) == 3
    overlays = bundle["english_question_units"]
    assert len(overlays) == 12
    for identity, paper in bundle["papers"].items():
        domain, key = identity.split(":")
        source = (ROOT / "docs" / spec(domain, key)["detail_path"]).read_text()
        assert {q["level"] for q in paper["questions"]} == {
            "basics", "mechanism", "comparison", "implementation"
        }
        for q in paper["questions"]:
            assert q["added"] == "2026-11-20"
            assert all(q[k] for k in ["question", "answer", "example"])
            assert all(section in source for section in q["source_sections"])
            unit = overlays[f"qa/{identity}/{q['id']}"]
            expected = sha256(json.dumps(q, ensure_ascii=False, sort_keys=True,
                                         separators=(",", ":")).encode()).hexdigest()
            assert unit["source_sha256"] == expected and unit["reviewed"] is True
            assert set(unit["fields"]) == {"question", "answer", "example"}


def test_primary_affiliation_and_original_dates_are_not_directory_dates():
    canon = spec("foundation-models", "canon-layers-scale")
    assert canon["published_at"] == "2026-11-12T18:51:19Z"
    assert canon["announced_on"] == "2026-11-20"
    assert canon["first_author_affiliation"] == "Allen-Zhu Research"
    assert canon["research_execution_organizations"] == ["FAIR at Meta"]
    assert canon["verified_priority_organizations"] == []
    fleet = spec("recommendation", "fleet-feature-optimization")
    assert fleet["first_author_affiliation"] == "Meta, Inc."
    assert fleet["verified_priority_organizations"] == ["Meta"]
    assert spec("foundation-models", "hisa")["code_license"] == "Apache-2.0"


def test_lser_online_experiment_is_not_llm_incrementality():
    record = spec("recommendation", "lser-serving")
    evidence = record["online_ab_review"]
    assert evidence["llm_features_enabled"] is False
    assert evidence["validates_llm_incrementality"] is False
    assert evidence["offline_llm_hr10_absolute_pp"] == 9.6
    assert evidence["traffic_split"] == [0.5, 0.5]
    source = (ROOT / "docs" / record["detail_path"]).read_text()
    assert "未启用LLM" in source
    assert "没有user_id权限隔离" in source
    assert "兼容baseline fusion" in source


def test_industrial_metrics_and_missing_confidence_are_preserved():
    antom = spec("recommendation", "antom-3-in-1")["online_ab_review"]
    assert antom["portfolio_loss_rate_relative_change"] == -0.3788
    assert antom["stage_ii_date_weighted_cb_relative_change"] == -0.2609
    assert antom["reported_confidence_interval"] is None
    dna = spec("recommendation", "dna")["online_ab_review"]
    assert dna["control"] == "CrossAttn-2"
    assert dna["ctr_relative_lift"] == .008 and dna["gmv_relative_lift"] == .005
    assert dna["duration"] is None and dna["confidence_interval"] is None
    fleet = spec("recommendation", "fleet-feature-optimization")["online_ab_review"]
    assert fleet["metric_name"] == "not disclosed"
    assert fleet["duration"] is None and fleet["confidence_interval"] is None
