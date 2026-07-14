from __future__ import annotations

import json
import re
from pathlib import Path

from auto_research.reproductions.base import ReproductionFidelity
from auto_research.reproductions.registry import list_adapters


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs" / "reproductions"


def _slug(adapter) -> str:
    return f"{adapter.paper.arxiv_id}-{adapter.key}"


def test_every_adapter_is_present_in_all_documentation_indexes():
    adapters = list_adapters()
    expected = {_slug(adapter) for adapter in adapters}
    actual = {
        path.parent.name
        for path in DOCS.glob("[0-9]*/README.md")
    }
    assert actual == expected

    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    main_index = (DOCS / "README.md").read_text(encoding="utf-8")
    company = (DOCS / "catalog" / "by-company.md").read_text(encoding="utf-8")
    month = (DOCS / "catalog" / "by-month.md").read_text(encoding="utf-8")
    topic = (DOCS / "catalog" / "by-topic.md").read_text(encoding="utf-8")
    for adapter in adapters:
        slug = _slug(adapter)
        assert f"`{adapter.key}`" in root_readme
        assert f"({slug}/README.md)" in main_index
        catalog_link = f"(../{slug}/README.md)"
        assert catalog_link in company
        assert catalog_link in month
        assert catalog_link in topic


def test_every_paper_readme_has_the_complete_reproduction_contract():
    required_headings = (
        "## 原始论文总结",
        "### 背景与主要改动",
        "### 核心公式",
        "### 论文离线与线上效果",
    )
    for adapter in list_adapters():
        directory = DOCS / _slug(adapter)
        text = (directory / "README.md").read_text(encoding="utf-8")
        for heading in required_headings:
            assert heading in text, f"{adapter.key} missing {heading}"
        assert "```mermaid" in text, f"{adapter.key} missing architecture diagram"
        assert re.search(r"^## 本地复现", text, re.MULTILINE)

        metric_files = sorted((directory / "metrics").glob("*.json"))
        assert metric_files, f"{adapter.key} missing stable metrics JSON"
        payloads = [json.loads(path.read_text(encoding="utf-8")) for path in metric_files]
        assert all(path.name in text for path in metric_files)
        if adapter.fidelity is ReproductionFidelity.CONCEPT_DEMO:
            assert any(payload.get("diagnostic_only") is True for payload in payloads)


def test_internal_markdown_links_resolve():
    link_pattern = re.compile(r"\[[^]]+\]\(([^)#]+)(?:#[^)]*)?\)")
    broken = []
    for path in (ROOT / "docs").rglob("*.md"):
        for target in link_pattern.findall(path.read_text(encoding="utf-8")):
            if "://" not in target and not (path.parent / target).resolve().exists():
                broken.append((str(path.relative_to(ROOT)), target))
    assert broken == []
