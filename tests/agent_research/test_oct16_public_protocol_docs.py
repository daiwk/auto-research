import hashlib
import importlib
import json
from pathlib import Path
import re
import struct

import pytest

ROOT = Path(__file__).resolve().parents[2]
CASES = [
    ("2610.21098", "tool-bottleneck-bench", "tool_bottleneck_bench", "audit_discovery",
     "2026-10-15T01:59:58Z", "University of Osaka", "6f7fe7157c702c5c10937080f15bb3d48ce73d69"),
    ("2610.22273", "librarian-agents", "librarian_agents", "recompute_records",
     "2026-10-15T17:35:17Z", "Stanford University", "455ac88c81c639c10a8404464dabf71a7fbb563e"),
    ("2610.21082", "scipivot", "scipivot", "audit_release",
     "2026-10-15T01:34:44Z", "University of Maryland", "94a47d391893ea392fd9bb9883a65d2c8834e6f2"),
]


@pytest.mark.parametrize("arxiv,key,module,operator,timestamp,institution,revision", CASES)
def test_paper_metadata_source_hashes_and_noncapability_boundary(arxiv, key, module, operator,
                                                               timestamp, institution, revision):
    directory = ROOT / "docs/agent-research" / f"{arxiv}-{key}"
    text = (directory / "README.md").read_text()
    for label in ("论文信息", "论文链接", "公司/机构", "首次公开日期", "原文开源代码", "本地 Adapter",
                  "本地复现代码", "原始论文总结", "背景与主要改动", "核心公式", "论文离线与线上效果",
                  "本地复现", "成本过高，不复现（审查 DONE）", "未报告生产线上 A/B"):
        assert label in text
    assert institution in text and revision in text
    assert f"src/auto_research/agent_research/{module}.py" in text
    assert "<!-- paper-figure:start -->" in text and "版权归原作者所有" in text
    data = (directory / "assets/paper-figure-01.png").read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 5000
    width, height = struct.unpack(">II", data[16:24])
    assert width >= 400 and height >= 140
    for link in re.findall(r"\]\(([^)]+)\)", text):
        if not link.startswith("http"):
            assert (directory / link).exists(), link
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog/agent-research" / f"{key}.json").read_text())
    assert catalog["published_timestamp_utc"] == timestamp
    assert catalog["adapter"] is None
    assert catalog["implementation_status"] == "evaluation_protocol_interface"
    assert catalog["evolve_integrated"] is False and catalog["promotion_eligible"] is False
    assert catalog["diagnostic_only"] is True
    assert catalog["full_experiment_status"] == "not_reproduced_high_cost"
    assert callable(getattr(importlib.import_module("auto_research.agent_research." + module), operator))
    metrics = list((directory / "metrics").glob("*.json"))
    assert len(metrics) == 1
    result = json.loads(metrics[0].read_text())
    assert result["schema_version"] == 2 and result["upstream_revision"] == revision
    assert result["dataset"]["id"] and result["dataset"]["revision"] == revision
    assert not result["evaluation_protocol"]["formal_comparison"]
    assert result["diagnostic_only"] and not result["promotion_eligible"] and not result["evolve_integrated"]
    provenance = result["provenance"]
    assert hashlib.sha256((ROOT / "src/auto_research/agent_research" / f"{module}.py").read_bytes()).hexdigest() == provenance["implementation_sha256"]
    assert hashlib.sha256((ROOT / "scripts" / f"run_{module}.py").read_bytes()).hexdigest() == provenance["source_sha256"]
    if "inputs" in result:
        for row in result["inputs"]:
            path = directory / "validation/upstream" / row["file"]
            assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
            assert row["sha256"] in text
    else:
        path = directory / "validation/upstream/browsecomp_per_corpus.jsonl"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == result["input_sha256"]
        assert result["input_sha256"] in text
    assert (directory / "validation/upstream/LICENSE").is_file()


def test_full_scipivot_options_export_was_executed_without_a_model():
    receipt = json.loads((ROOT / "docs/agent-research/2610.21082-scipivot/validation/options-export-receipt.json").read_text())
    assert receipt["cases"] == 248 and receipt["planned_runs"] == 496
    assert not receipt["evaluator_executed"]
    assert receipt["public_sha256"] == "667869d4dec0f5c48eef9494caebfb7f4bd1537deca4429e03a6511cbff46b76"
    assert receipt["grader_sha256"] == "1d8315fb0cde7d001f2a13efc6576f1a24c49d2bc36738b23a3ba388df1298da"


def test_scipivot_audit_declares_actual_seedless_dataset_identity():
    path = ROOT / "docs/agent-research/2610.21082-scipivot/metrics/official-options-audit-cpu.json"
    result = json.loads(path.read_text())
    assert result["deterministic"] is True
    assert result["seeds"] == result["evaluation_protocol"]["seeds"] == []
    assert result["evaluation_protocol"]["formal_comparison"] is False
    assert result["evaluation_protocol"]["claim_policy"]
    assert result["dataset"] == {
        "id": "SciPIvot/released-options-only",
        "revision": "94a47d391893ea392fd9bb9883a65d2c8834e6f2",
        "split": "official 248-case options-only release; project histories not released",
        "source_sha256": "87a7b05115ce3438ba3b62b30a21dbe6f618c8657527442b094b79f5b664fd9f",
        "input_role": "official_questions",
        "aggregate_sha256": "e53e68a571ead46f9334bc899904b7a0e1f8c0dd3fb323e7d90f9c5ad05ec458"}
