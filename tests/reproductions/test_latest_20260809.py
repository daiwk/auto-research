from pathlib import Path

import pytest

from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


@pytest.mark.parametrize(
    ("key", "result_section", "mechanism_metric"),
    [
        ("hrpo", "variants", "hrpo residual-return policy"),
        ("kgd", "variants", "kgd bmtp + read-only transfer + acr"),
        ("llm-ts-prior", "variants", "llm semantic prior"),
        ("twitch-mor", "variants", "fresh-delayed lifecycle mmoe"),
        ("qevict", "metrics", "qevict_recall"),
        ("dblast", "metrics", "dependent_accepted_length"),
        ("hilp", "metrics", "hilp_mse"),
        ("macro", "metrics", "searched_routes"),
        ("bakron", "metrics", "bakron_weighted_error"),
    ],
)
def test_20260809_adapters_execute_and_publish_complete_artifacts(
    key: str, result_section: str, mechanism_metric: str
):
    adapter = get_adapter(key)
    result = adapter.run(DATA, 42)
    assert mechanism_metric in result[result_section]

    slug = f"{adapter.paper.arxiv_id}-{key}"
    page = ROOT / "docs" / "reproductions" / slug / "README.md"
    text = page.read_text(encoding="utf-8")
    for field in (
        "论文链接", "公司/机构", "首次公开日期", "原文开源代码",
        "Adapter", "本地复现代码", "本地对照口径",
    ):
        assert field in text
    assert "paper-figure:start" in text
    assert (page.parent / "metrics" / "public-seed42.json").exists()
    assert (page.parent / "assets" / "paper-figure-01.png").exists()


def test_new_industrial_adapters_keep_quantified_online_evidence():
    for key in ("hrpo", "kgd", "llm-ts-prior", "twitch-mor"):
        assert get_adapter(key).paper.has_online_ab
