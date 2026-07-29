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
        for path in DOCS.glob("*/README.md")
        if path.parent.name != "catalog"
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


def test_reproduction_hub_has_lineage_benchmark_and_expandable_paper_navigation():
    lineage = (DOCS / "lineage.md").read_text(encoding="utf-8")
    benchmark = (DOCS / "benchmark.md").read_text(encoding="utf-8")
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert "## 谱系覆盖" in lineage
    assert "## 当前缺口" in lineage
    assert "## 评测分层" in benchmark
    assert "## 本地基线规则" in benchmark
    assert "DIN 不是所有论文的强制基线" in benchmark
    assert "      - 搜广推与 LLM 应用:" in navigation
    assert "          - 论文谱系与缺口: reproductions/lineage.md" in navigation
    assert "          - 统一评测协议: reproductions/benchmark.md" in navigation
    assert "          - 论文实现:" in navigation


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


def test_catalogs_use_semantic_sections_instead_of_release_batch_names():
    catalog_dir = DOCS / "catalog"
    expected_sections = {
        "by-month.md": {
            "causal-retrieval": "2026-07",
            "pin-scale": "2026-07",
            "looped-latent-attention": "2026-07",
            "gaugequant": "2026-07",
            "pinclip": "2026-03",
            "dos": "2026-02",
            "mdl": "2026-02",
            "hisac": "2026-02",
            "podcast-mtl": "2026-01",
            "engram": "2026-01",
            "onemall": "2026-01",
        },
        "by-company.md": {
            "causal-retrieval": "Pinterest",
            "pin-scale": "Pinterest",
            "looped-latent-attention": "Meta",
            "gaugequant": "学术与经典基线",
            "pinclip": "Pinterest",
            "dos": "Meituan",
            "mdl": "ByteDance / Douyin / TikTok",
            "hisac": "Alibaba",
            "podcast-mtl": "Spotify",
            "engram": "DeepSeek-AI",
            "onemall": "Kuaishou",
        },
        "by-topic.md": {
            "causal-retrieval": "因果推断与长期价值",
            "pin-scale": "冷启动与语义-行为对齐",
            "looped-latent-attention": "纯 LLM：架构、预训练与条件记忆",
            "gaugequant": "纯 LLM：架构、预训练与条件记忆",
            "pinclip": "冷启动与语义-行为对齐",
            "dos": "生成式召回与端到端推荐",
            "mdl": "排序网络与长序列",
            "hisac": "排序网络与长序列",
            "podcast-mtl": "冷启动与语义-行为对齐",
            "engram": "纯 LLM：架构、预训练与条件记忆",
            "onemall": "生成式召回与端到端推荐",
        },
    }
    for name, assignments in expected_sections.items():
        text = (catalog_dir / name).read_text(encoding="utf-8")
        assert "2026 P1 与 LLM evolve" not in text
        current_section = None
        located = {}
        for line in text.splitlines():
            if line.startswith("## "):
                current_section = line.removeprefix("## ")
            for adapter_key in assignments:
                if f"-{adapter_key}/README.md)" in line:
                    located[adapter_key] = current_section
        assert located == assignments


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
        paper_label = adapter.paper.publication_label or f"arXiv {adapter.paper.arxiv_id}"
        required_metadata = (
            "## 论文信息",
            f"| 论文链接 | [{paper_label}]({adapter.paper.url}) |",
            "| 公司/机构 |",
            "| 首次公开日期 |",
            "| 原文开源代码 |",
            f"| Adapter | `{adapter.key}` |",
            f"| 本地复现代码 | [`{source_directory}`](https://github.com/daiwk/auto-research/tree/main/{source_directory}) |",
        )
        for entry in required_metadata:
            assert entry in text, f"{adapter.key} missing metadata: {entry}"
        date_source = adapter.paper.publication_source or "arXiv v1"
        assert re.search(
            rf"^\| 首次公开日期 \| \d{{4}}-\d{{2}}-\d{{2}}（{date_source}） \|$",
            text, re.MULTILINE,
        ), f"{adapter.key} missing exact first-publication date"
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
