import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "convapparel": "2602.16938",
    "simula": "2603.29791",
    "tfrbench": "2604.05364",
    "scientist-one": "2605.26340",
}


@pytest.mark.parametrize("key,paper_id", PAPERS.items())
def test_protocol_metadata_and_checked_in_demo_are_not_capability_claims(key, paper_id):
    spec = json.loads((ROOT / f"src/auto_research/paper_specs/catalog/agent-research/{key}.json").read_text())
    directory = ROOT / f"docs/agent-research/{paper_id}-{key}"
    text = (directory / "README.md").read_text()
    metric = json.loads((directory / "metrics/protocol-cpu-seed42.json").read_text())
    assert spec["implementation_status"] == "evaluation_protocol_interface"
    assert spec["evaluation_tier"] == "l0_interface"
    assert spec["adapter"] is None
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert not spec["requires_gpu_validation"]
    assert metric["fixture_demo"] and metric["diagnostic_only"]
    assert metric["model_calls"] == 0 and not metric["promotion_eligible"]
    for field in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "本地 Adapter", "本地复现代码", "成本过高", "不复现", "审查 DONE"):
        assert field in text
    assert (directory / "assets/paper-figure-01.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


def test_runner_requires_explicit_fixture_or_input_and_outputs_are_immutable(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("google16_evaluation_runner", ROOT / "scripts/run_google16_evaluation.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for component in PAPERS:
        result = module.COMPONENTS[component](42)
        assert result["model_calls"] == 0
    assert module.scientist_demo(42)["report"]["i2"]["status"] == "unverified"
    assert module.scientist_demo(42)["report"]["i3"]["status"] == "unverified"
    assert module.scientist_demo(42)["report"]["i4"]["status"] == "unverified"
    output = tmp_path / "result.json"
    monkeypatch.setattr(sys, "argv", ["runner", "--component", "simula", "--output", str(output)])
    with pytest.raises(SystemExit):
        module.main()
    monkeypatch.setattr(sys, "argv", ["runner", "--component", "simula", "--fixture-demo", "--output", str(output)])
    assert module.main() == 0
    before = output.read_bytes()
    with pytest.raises(SystemExit):
        module.main()
    assert output.read_bytes() == before
