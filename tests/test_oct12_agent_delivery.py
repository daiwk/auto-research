"""Complete accepted six-paper scope, source metadata and runnable bindings."""
import json
from pathlib import Path
import pytest

from auto_research.paper_specs.runtime import adapter_from_spec
from auto_research.paper_specs.schema import load_spec, validate_spec

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {"evo2":"2610.13025","rsi-anything":"2610.13912","janus":"2610.13194",
          "t2mem":"2610.13348","rated":"2610.13889","jev-workflow":"2610.13092"}


@pytest.mark.parametrize("key,identifier",PAPERS.items())
def test_oct12_six_paper_bindings_metadata_and_documentation(key,identifier):
    directory = ROOT / "src/auto_research/reproductions" / key.replace("-","_")
    spec = load_spec(directory / "paper.yaml")
    assert not validate_spec(spec,root=ROOT)
    assert spec.key == key and spec.arxiv_id == identifier and spec.published == "2026-10-09"
    assert spec.execution["requires_gpu_validation"] is (key != "jev-workflow")
    assert not spec.evolve_operators
    adapter = adapter_from_spec(key)
    assert adapter.evaluation_tier.value == "l1_mechanism"
    assert adapter.paper.organization and adapter.paper.published
    text = (ROOT / spec.documentation).read_text()
    for heading in ("## 论文信息","## 原始论文总结","### 背景与主要改动","### 核心公式",
                    "### 论文离线与线上效果","## 本地复现","### 数据协议与代码映射",
                    "### 结果、验证与边界"):
        assert heading in text
    assert "2026-10-09（arXiv v1）" in text and spec.paper_url in text
    assert "原文开源代码" in text and "```mermaid" in text
    assert "未报告生产线上 A/B" in text and "不是本地结果" in text
    evidence = json.loads((ROOT / spec.documentation).parent.joinpath("assets/paper-results.json").read_text())
    assert evidence["local_run"] is False
    assert "diagnostic_only" not in evidence  # paper reports are not local diagnostics
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research" / (key+".json")).read_text())
    assert catalog["adapter"] == {"spec_key":key} and catalog["published"] == spec.published


def test_janus_is_not_mislabelled_as_author_released_implementation():
    spec = load_spec(ROOT / "src/auto_research/reproductions/janus/paper.yaml")
    assert spec.upstream_code.startswith("否") and "README/assets" in spec.upstream_code
    assert spec.execution["paper"]["code_url"] is None


def test_jev_is_evaluation_infrastructure_not_a_gpu_model_claim():
    adapter = adapter_from_spec("jev-workflow")
    assert adapter.requires_gpu_validation is False
    assert adapter.gpu_validation_artifact is None
    assert adapter.paper.code_url is None
    spec = load_spec(ROOT / "src/auto_research/reproductions/jev_workflow/paper.yaml")
    assert "匿名实验代码链接" in spec.upstream_code and "未核实可用源码" in spec.upstream_code


def test_six_catalog_records_resolve_to_packaged_specs_and_runnable_bindings():
    from auto_research.paper_specs.catalog import catalog_records
    records = {row["key"]:row for row in catalog_records() if row["key"] in PAPERS}
    assert set(records) == set(PAPERS)
    for key,row in records.items():
        assert row["adapter"]["adapter_key"] == key
        assert row["adapter"]["arxiv_id"] == PAPERS[key]
        assert row["adapter"]["local_code_dir"] == "src/auto_research/reproductions/" + key.replace("-","_")
        assert row["adapter"]["requires_gpu_validation"] is (key != "jev-workflow")


def test_documented_bash_commands_have_single_line_continuations():
    for key,identifier in PAPERS.items():
        text = (ROOT/"docs/reproductions"/(identifier+"-"+key)/"README.md").read_text()
        assert not any(line.endswith("\\\\") for line in text.splitlines())
