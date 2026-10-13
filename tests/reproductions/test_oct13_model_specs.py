import json
from pathlib import Path

import pytest

from auto_research.foundation_models.oct13_runtime import check_checkpoint_identity, execute
from auto_research.paper_specs.schema import load_spec, validate_spec

ROOT = Path(__file__).resolve().parents[2]
PAPERS = (("cv-opd", "cv_opd", "2610.13264"), ("oal", "oal", "2610.13674"),
          ("replayssm", "replayssm", "2610.13778"),
          ("doublecat-semicat", "doublecat_semicat", "2610.13834"))


@pytest.mark.parametrize("key,folder,identifier", PAPERS)
def test_complete_individual_spec_metadata_and_diagnostic_evidence(key, folder, identifier):
    spec = load_spec(ROOT / "src/auto_research/reproductions" / folder / "paper.yaml")
    assert not validate_spec(spec, root=ROOT)
    assert spec.key == key and spec.arxiv_id == identifier
    assert spec.published == "2026-10-09"
    assert spec.execution["requires_gpu_validation"]
    assert spec.execution["gpu_validation_artifact"]
    assert spec.evolve_operators == ()
    readme = (ROOT / spec.documentation).read_text()
    for heading in ("## 论文信息", "## 原始论文总结", "### 背景与主要改动", "### 核心公式",
                    "### 论文离线与线上效果", "## 本地复现", "### 代码映射"):
        assert heading in readme
    for field in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "Adapter", "本地复现代码"):
        assert f"| {field} |" in readme
    metrics = list((ROOT / spec.documentation).parent.glob("metrics/*.json"))
    assert metrics
    assert all(json.loads(path.read_text())["diagnostic_only"] for path in metrics)
    assert all(path.name in readme for path in metrics)


def test_checkpoint_identity_rejects_relabelled_instruct(tmp_path):
    (tmp_path / "provenance.json").write_text(json.dumps({
        "public_id": "Qwen/Qwen2.5-0.5B-Instruct", "revision": "wrong"}))
    with pytest.raises(ValueError, match="provenance differs"):
        check_checkpoint_identity(tmp_path, "Qwen/Qwen2.5-0.5B", "060db6499f32faf8b98477b0a26969ef7d8b9987")


def test_missing_runtime_config_never_silently_downgrades_to_fixture(tmp_path):
    with pytest.raises(FileNotFoundError, match="explicit local config"):
        execute("oal", "run_oal.py", tmp_path, 42)
