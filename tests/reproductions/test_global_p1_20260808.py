from pathlib import Path

import pytest

from auto_research.reproductions.registry import get_adapter

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"

P1_KEYS = (
    "twin-v2", "sim", "crsd", "clip", "llava",
    "speculative-decoding", "awq", "medusa",
)


@pytest.mark.parametrize("key", P1_KEYS)
def test_p1_adapter_runs_and_has_complete_documentation(key: str):
    adapter = get_adapter(key)
    result = adapter.run(DATA, 42)
    page = ROOT / "docs" / "reproductions" / (
        f"{adapter.paper.arxiv_id}-{key}"
    ) / "README.md"
    text = page.read_text(encoding="utf-8")
    for field in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "Adapter", "本地复现代码"):
        assert field in text
    assert result["scope"]


def test_industrial_p1_keeps_online_evidence_and_candidate_mechanisms():
    twin = get_adapter("twin-v2").run(DATA, 42)
    sim = get_adapter("sim").run(DATA, 42)
    crsd = get_adapter("crsd").run(DATA, 42)
    assert twin["stages"]["candidate_aware_gsu"]
    assert sim["stages"]["exact_search_attention"]
    assert crsd["stages"]["shared_student_two_views"]
    for key in ("twin-v2", "sim", "crsd"):
        assert get_adapter(key).paper.has_online_ab


def test_inference_p1_preserves_outputs_or_reduces_quantization_error():
    speculative = get_adapter("speculative-decoding").run(DATA, 42)
    medusa = get_adapter("medusa").run(DATA, 42)
    awq = get_adapter("awq").run(DATA, 42)
    assert speculative["stages"]["exact_output_match"]
    assert speculative["method"]["target_calls"] < speculative["baseline"]["target_calls"]
    assert medusa["stages"]["exact_output_match"]
    assert medusa["method"]["backbone_calls"] < medusa["baseline"]["backbone_calls"]
    assert awq["method"]["output_mse"] < awq["baseline"]["output_mse"]
