from __future__ import annotations

import json
from pathlib import Path

import pytest

from auto_research.paper_specs.schema import load_spec,validate_spec

ROOT=Path(__file__).resolve().parents[2]
PAPERS={
    "state-opd":"2610.13238", "magicbeanstalk":"2610.12659",
    "gppo-framework":"2610.13015", "tapo-trajectory":"2610.13020",
    "synthself":"2610.13113", "upturn":"2610.13672", "soar":"2610.13157",
    "grpo-difficulty-curriculum":"2610.13669", "progressive-contraction":"2610.12933",
}


@pytest.mark.parametrize("key,identifier",PAPERS.items())
def test_oct13_paper_metadata_complete_and_diagnostic_boundaries_explicit(key,identifier):
    spec=load_spec(ROOT/"src/auto_research/reproductions"/key.replace("-","_")/"paper.yaml")
    assert not validate_spec(spec,root=ROOT)
    assert spec.key==key and spec.arxiv_id==identifier
    assert spec.published==("2026-10-08" if key=="magicbeanstalk" else "2026-10-09")
    assert spec.fidelity=="core_mechanism" and spec.evaluation_tier=="l1_mechanism"
    assert spec.execution["requires_gpu_validation"] is True
    receipt_date={k:"20261014" for k in ("state-opd","grpo-difficulty-curriculum","synthself","upturn","progressive-contraction")}.get(key,"20261013")
    suffix="-seeds42-44" if key in {"synthself","progressive-contraction"} else ""
    assert spec.execution["gpu_validation_artifact"]==f"docs/gpu-validations/{key}-a100-{receipt_date}{suffix}.json"
    assert spec.evolve_operators==()
    doc=ROOT/spec.documentation
    assert doc.parent.name==f"{identifier}-{key}" and doc.parent.parent==ROOT/"docs/reproductions"
    text=doc.read_text()
    required=("## 论文信息",f"| 论文链接 | [arXiv {identifier}](https://arxiv.org/abs/{identifier}) |",
              "| 公司/机构 |",f"| 首次公开日期 | {spec.published}（arXiv v1） |","| 原文开源代码 |",
              f"| Adapter | `{key}` |","| 本地复现代码 |","## 原始论文总结","### 背景与主要改动",
              "### 核心公式","### 论文离线与线上效果","```mermaid","## 本地复现",
              "> **本地对照口径**：","未报告生产线上A/B","mechanism-contracts.json","formal_comparison: false")
    assert all(entry in text for entry in required)
    row=json.loads((ROOT/"src/auto_research/paper_specs/catalog/post-training"/(key+".json")).read_text())
    assert row["adapter"]=={"spec_key":key}
    assert row["detail_path"]==spec.documentation.removeprefix("docs/")
    metrics=json.loads((doc.parent/"metrics/mechanism-contracts.json").read_text())
    assert metrics["diagnostic_only"] is True
    assert metrics["evaluation_protocol"]["tier"]=="l0_contract"
    assert metrics["evaluation_protocol"]["formal_comparison"] is False
    paper_results=json.loads((doc.parent/"paper-results.json").read_text())
    assert paper_results["measured_locally"] is False
    figure=json.loads((doc.parent/"figure-source.json").read_text())
    assert figure["version"]=="v1" and identifier+"v1" in figure["source_resource"]


def test_state_current_receipt_requires_all_new_arms_not_the_old_default_only_run():
    spec=load_spec(ROOT/"src/auto_research/reproductions/state_opd/paper.yaml")
    receipt=json.loads((ROOT/spec.execution["gpu_validation_artifact"]).read_text())
    result=json.loads((ROOT/receipt["provenance"]["metrics_artifact"]).read_text())
    assert receipt["provenance"]["commit"]=="6aabe57a97ec3a586aac7aeea66128750f9441da"
    assert receipt["variants"]==["state","full-history-opd","state-no-expansion"]
    assert receipt["seeds"]==[42,43,44]
    assert result["actual_cuda_run_count"]==9
    assert len(result["provenance"]["raw_results_sha256"])==9
    assert result["evaluation_protocol"]["formal_comparison"] is False
    assert result["execution_checks"]["full-history-opd"]["teacher_prior_reasoning_removed_responses_per_seed"]==[0,0,0]


def test_abbreviation_collisions_do_not_replace_historical_catalog_entries():
    catalog=ROOT/"src/auto_research/paper_specs/catalog/post-training"
    assert json.loads((catalog/"gppo.json").read_text())["paper_url"].endswith("2508.07629")
    assert json.loads((ROOT/"src/auto_research/paper_specs/catalog/agent-research/tapo.json").read_text())["paper_url"].endswith("2607.27973")


def test_curriculum_actual_three_variants_are_one_seed_and_do_not_complete_all_controls():
    spec=load_spec(ROOT/"src/auto_research/reproductions/grpo_difficulty_curriculum/paper.yaml")
    receipt=json.loads((ROOT/spec.execution["gpu_validation_artifact"]).read_text())
    result=json.loads((ROOT/receipt["provenance"]["metrics_artifact"]).read_text())
    assert receipt["provenance"]["commit"]=="6aabe57a97ec3a586aac7aeea66128750f9441da"
    assert receipt["variants"]==["fixed-medium","staged","too-hard"] and receipt["seeds"]==[42]
    assert len(result["seed_results"])==1 and result["actual_cuda_run_count"]==3
    assert result["evaluation_protocol"]["formal_comparison"] is False
    assert result["evaluation_protocol"]["promotion_eligible"] is False
    assert all(v["n"]==1 for v in result["aggregate_metrics"].values())
    assert [result["execution_checks"][v]["actual_optimizer_updates"] for v in receipt["variants"]]==[8,9,11]
    text=(ROOT/spec.documentation).read_text()
    assert "数值修复后的五臂42/43/44计划未完成" in text and "旧A100三臂未执行static和unfiltered" in text
    assert "三个variants不算三个seeds" in text and "单seed机制GPU门禁通过不代表本批整体完成" in text


def test_cuda_missing_configuration_does_not_run_a_fixture(tmp_path):
    from auto_research.post_training.oct13_common import adapter_run
    with pytest.raises(FileNotFoundError,match="oct13_execution.json"):
        adapter_run("synthself",tmp_path,42)
