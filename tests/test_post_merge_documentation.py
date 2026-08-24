from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_completed_roadmap_uses_stable_pull_request_links():
    roadmap = (ROOT / "docs" / "research-roadmap.md").read_text(encoding="utf-8")
    assert "DONE · 本 MR" not in roadmap
    for number in (113, 114, 115, 116, 117):
        assert f"https://github.com/daiwk/auto-research/pull/{number}" in roadmap


def test_lineage_pages_do_not_reopen_completed_static_work():
    foundation = (ROOT / "docs" / "foundation-models" / "lineage.md").read_text(
        encoding="utf-8"
    )
    post_training = (ROOT / "docs" / "post-training" / "lineage.md").read_text(
        encoding="utf-8"
    )
    agent = (ROOT / "docs" / "agent-research" / "lineage.md").read_text(
        encoding="utf-8"
    )
    assert "当前没有尚未实现的静态 P0/P1" in foundation
    assert "当前没有尚未实现的静态 P0/P1" in post_training
    assert "当前没有尚未实现的静态 P0/P1" in agent
    assert "连接可训练 LLM policy 与统一多轮 controller" not in agent
