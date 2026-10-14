"""Affordable/deferred papers retain correct source-owned browse routing."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def generator():
    spec = importlib.util.spec_from_file_location(
        "oct14_catalog_visibility", ROOT / "scripts/generate_research_catalogs.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("dimension", ("organization", "topic", "year"))
def test_ev_jepa_is_visible_without_becoming_an_executable_model(dimension):
    module = generator()
    text = module.render_foundation_catalog(dimension)
    link = "../../reproductions/2610.14324-ev-jepa/README.md"
    line = next(line for line in text.splitlines() if f"]({link})" in line)
    assert "成本过高，暂不复现" in line
    assert "待验收" in line and "未注册可执行入口" in line
    assert text.count(f"]({link})") == 1
    if dimension == "topic":
        assert "### 视频表征与弹性跨设备推理" in text


@pytest.mark.parametrize("domain, topic, expected", (
    ("post-training", "on-policy-self-distillation",
     ("蒸馏与训练闭环", "on-policy / context 蒸馏")),
    ("agent-research", "agentic-rl",
     ("Agentic RL 与后训练", "技能、turn 与 rollout credit")),
))
def test_deferred_methods_are_classified_by_real_algorithm_family(domain, topic, expected):
    assert generator().TOPIC_HIERARCHY[domain][topic] == expected


@pytest.mark.parametrize("filename", ("by-company.md", "by-topic.md", "by-month.md"))
def test_new_industrial_entries_are_independent_and_deferred_status_is_explicit(filename):
    text = (ROOT / "docs/reproductions/catalog" / filename).read_text(encoding="utf-8")
    for slug, deferred in (
        ("2610.16132-unisgr-v2", True),
        ("2610.14550-snap-dpa-relevance", True),
        ("2610.16979-wegr", False),
    ):
        target = f"](../{slug}/README.md)"
        lines = [line for line in text.splitlines() if target in line]
        assert len(lines) == 1
        line = lines[0]
        assert line.startswith("- ") and "：" in line
        assert len(re.findall(r"[\u3400-\u9fff]", line.split("：", 1)[1])) >= 35
        assert line.count("](../") == 1
        if deferred:
            assert "成本过高，暂不复现" in line
            assert "待验收" in line and "未注册可执行入口" in line


def test_new_october_entries_remain_date_descending_after_normal_sort(tmp_path):
    module = generator()
    source = ROOT / "docs/reproductions/catalog/by-month.md"
    target = tmp_path / "by-month.md"
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    module.sort_reproduction_catalog(target)
    october = target.read_text(encoding="utf-8").split("## 2026-10", 1)[1].split("## ", 1)[0]
    links = re.findall(r"\]\((\.\./[^)]+)\)", october)
    dates = [module._paper_date(link) for link in links]
    assert dates == sorted(dates, reverse=True)
    assert dates[:3] == ["2026-10-12", "2026-10-12", "2026-10-10"]

