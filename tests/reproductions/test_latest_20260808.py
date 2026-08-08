from pathlib import Path

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.reproductions.registry import get_adapter


def test_latest_industrial_papers_have_online_evidence_and_metadata():
    gryphon = get_adapter("gryphon-v2")
    degr = get_adapter("degr")
    assert gryphon.paper.published == "2026-08-06"
    assert degr.paper.published == "2026-08-05"
    assert gryphon.paper.has_online_ab and degr.paper.has_online_ab
    assert gryphon.paper.code_url is None and degr.paper.code_url is None


def test_rd_attnres_executes_separate_qk_and_v_routes():
    import torch

    config = MicroLMConfig(vocab_size=64, dimensions=32, layers=2, heads=4, sequence_length=16)
    shared = build_micro_lm("block_attnres", config)
    decoupled = build_micro_lm("rd_attnres", config)
    tokens = torch.randint(0, 64, (2, 16))
    shared(tokens)
    decoupled(tokens)
    assert shared.architecture_stats()["qk_v_role_decoupled"] is False
    assert decoupled.architecture_stats()["qk_v_role_decoupled"] is True
    assert decoupled.architecture_stats()["qk_v_route_js_divergence"] > 0


def test_latest_docs_include_required_metadata_and_metrics():
    root = Path(__file__).resolve().parents[2]
    for page in (
        root / "docs/reproductions/2608.06213-gryphon-v2/README.md",
        root / "docs/reproductions/2608.04809-degr/README.md",
        root / "docs/reproductions/2608.01075-rd-attnres/README.md",
        root / "docs/post-training/2608.06243-dash/README.md",
        root / "docs/agent-research/2608.06197-envace/README.md",
    ):
        text = page.read_text(encoding="utf-8")
        for field in ("论文链接", "首次公开日期", "本地复现代码"):
            assert field in text
        assert "公司/机构" in text or "公司 / 机构" in text
        assert "原文开源代码" in text or "原作者代码" in text
        assert "本地复现" in text and "复现边界" in text
