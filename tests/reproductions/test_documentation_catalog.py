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


def test_catalog_entries_are_one_paper_per_line_with_chinese_summaries():
    catalog_dir = DOCS / "catalog"
    for name in ("by-company.md", "by-topic.md", "by-month.md"):
        path = catalog_dir / name
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if "(../" not in line:
                continue
            assert line.startswith("- "), f"{name}:{line_number} is not a paper bullet"
            assert line.count("(../") == 1, (
                f"{name}:{line_number} combines multiple papers on one line"
            )
            _, separator, summary = line.partition("：")
            assert separator and re.search(r"[\u4e00-\u9fff]", summary), (
                f"{name}:{line_number} is missing a Chinese method summary"
            )


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
        source_directory = f"src/auto_research/reproductions/{adapter.key.replace('-', '_')}/"
        required_metadata = (
            "## 论文信息",
            f"| 论文链接 | [arXiv {adapter.paper.arxiv_id}]({adapter.paper.url}) |",
            "| 公司/机构 |",
            "| 首次公开日期 |",
            "| 原文开源代码 |",
            f"| Adapter | `{adapter.key}` |",
            f"| 本地复现代码 | [`{source_directory}`](https://github.com/daiwk/auto-research/tree/main/{source_directory}) |",
        )
        for entry in required_metadata:
            assert entry in text, f"{adapter.key} missing metadata: {entry}"
        assert re.search(
            r"^\| 首次公开日期 \| \d{4}-\d{2}-\d{2}（arXiv v1） \|$",
            text,
            re.MULTILINE,
        ), f"{adapter.key} missing exact arXiv v1 date"
        assert re.search(
            r"^\| 原文开源代码 \| (?:是：\[[^]]+\]\(https?://[^)]+\)|否：[^|]+) \|$",
            text,
            re.MULTILINE,
        ), f"{adapter.key} has ambiguous upstream code availability"
        for heading in required_headings:
            assert heading in text, f"{adapter.key} missing {heading}"
        assert "```mermaid" in text, f"{adapter.key} missing architecture diagram"
        assert re.search(r"^## 本地复现", text, re.MULTILINE)
        assert re.search(
            r"^> \*\*本地对照口径\*\*：.*基线.*(?:实验组|相对).*(?:%|不适用)",
            text,
            re.MULTILINE,
        ), f"{adapter.key} missing an explicit local baseline comparison"

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
