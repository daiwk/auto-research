"""Metadata, measured CPU evidence and original-figure contracts for this batch."""
import hashlib
import json
from pathlib import Path
import struct

import pytest


ROOT = Path(__file__).resolve().parents[2]
PAPERS = {
    "tf-opd": ("2610.22236", "2026-10-15T17:15:01Z"),
    "waypoint-opd": ("2610.21601", "2026-10-15T09:47:19Z"),
    "ggpo": ("2610.20814", "2026-10-14T18:59:29Z"),
    "stopd": ("2610.21337", "2026-10-15T06:22:08Z"),
    "cce-opd": ("2610.21195", "2026-10-15T03:55:34Z"),
    "sif": ("2610.21392", "2026-10-15T07:08:46Z"),
}


@pytest.mark.parametrize("key", PAPERS)
def test_metadata_cost_terminal_metrics_and_original_small_figure_are_complete(key):
    identifier, published = PAPERS[key]
    page = ROOT / "docs/post-training" / f"{identifier}-{key}"
    text = (page / "README.md").read_text()
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog/post-training" / f"{key}.json").read_text())
    evidence = json.loads((page / "metrics/component-cpu-seeds42-44.json").read_text())
    for phrase in ("## 论文信息", "| 论文链接 |", "| 公司 / 机构 |", "| 首次公开日期 |",
                   "| 原作者代码 |", "| 本地 adapter / 方法键 |", "| 本地复现代码目录 |",
                   published, f"`{key}`", "## 原始论文总结", "### 背景与主要改动", "### 核心公式",
                   "### 论文离线与线上效果", "## 本地复现", "```mermaid", "线上 A/B：未报告",
                   "成本过高，不复现（审查 DONE）", "metrics/component-cpu-seeds42-44.json",
                   "<!-- paper-figure:start -->", "### 原论文关键图", "assets/paper-figure-01.png",
                   "图片来自[原论文]", "版权归原作者所有", "<!-- paper-figure:end -->"):
        assert phrase in text, (key, phrase)
    assert catalog["published_at"] == published and catalog["published"] == published[:10]
    assert catalog["adapter"] is None and catalog["implementation_status"] == "component_only"
    assert catalog["evolve_integrated"] is False and catalog["promotion_eligible"] is False
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    assert catalog["first_author_affiliation"] and catalog["code_status"]
    first_institutions = {
        "tf-opd": "University of Illinois Urbana-Champaign",
        "waypoint-opd": "Alibaba Cloud Computing",
        "ggpo": "University of Illinois Urbana-Champaign",
        "stopd": "Cornell University",
        "cce-opd": "The Chinese University of Hong Kong, Shenzhen",
        "sif": "Institute of Automation, Chinese Academy of Sciences",
    }
    assert catalog["first_author_affiliation"] == first_institutions[key]
    assert evidence["schema_version"] == 2 and evidence["measured_locally"]
    assert evidence["diagnostic_only"] and not evidence["promotion_eligible"]
    assert evidence["adapter"] is None and evidence["evaluation_protocol"]["formal_comparison"] is False
    assert evidence["full_experiment"]["review_done"] and not evidence["full_experiment"]["automatic_retry"]
    assert evidence["metrics"]["parameter_delta_l2"]["mean"] > 0
    assert evidence["metrics"]["frozen_teacher_parameter_delta_l2"]["mean"] == 0
    assert evidence["manifest_ref"] == f"post-training:{key}" and evidence["seeds"] == [42, 43, 44]
    module = ROOT / "src/auto_research/post_training" / f"{key.replace('-', '_')}.py"
    assert evidence["provenance"]["implementation_sha256"] == hashlib.sha256(module.read_bytes()).hexdigest()
    for filename, digest in evidence["provenance"]["executed_source_sha256"].items():
        assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == digest
    source = evidence["dataset"]
    assert source["revision"] == "sha256:" + source["source_sha256"]
    assert source["byte_ranges"]["train"][1] == source["byte_ranges"]["validation"][0]
    assert source["byte_ranges"]["validation"][1] == source["byte_ranges"]["test"][0]
    image = (page / "assets/paper-figure-01.png").read_bytes()
    assert image[:8] == b"\x89PNG\r\n\x1a\n" and len(image) >= 5000
    width, height = struct.unpack(">II", image[16:24])
    assert width >= 400 and height >= 140
    if key == "sif":
        assert "550" in text and "缩窗" in text
        assert not evidence["execution_checks"]["original_sif_550_online_path_validated"]
        assert all(step["paper_default_eligible_responses"] == 0
                   for row in evidence["per_seed"] for step in row["history"])
