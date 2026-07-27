from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MODULES = {
    "post-training": {
        "lightning-opd": "2604.13010-lightning-opd",
        "gprl": "2605.18721-gprl",
        "tcr": "2607.19824-tcr",
    },
    "agent-research": {
        "u-mem": "2602.22406-u-mem",
        "legomem": "2510.04851-legomem",
        "memtool": "2507.21428-memtool",
    },
}


def test_research_modules_have_scalable_hub_structure():
    for module, methods in MODULES.items():
        directory = ROOT / "docs" / module
        for name in ("README.md", "catalog.md", "benchmark.md"):
            assert (directory / name).is_file(), f"{module} missing {name}"

        overview = (directory / "README.md").read_text(encoding="utf-8")
        catalog = (directory / "catalog.md").read_text(encoding="utf-8")
        assert "## 快速入口" in overview
        assert "## 研究闭环" in overview
        assert "## 后续扩展约定" in overview
        assert "(catalog.md)" in overview
        assert "(benchmark.md)" in overview
        for method, slug in methods.items():
            assert f"({slug}/README.md)" in overview
            assert f"({slug}/README.md)" in catalog
            assert f"`{method}`" in catalog


def test_each_research_paper_page_has_complete_contract():
    required = (
        "## 论文信息",
        "| 论文链接 |",
        "| 公司 / 机构 |",
        "| 首次公开日期 |",
        "| 原作者代码 |",
        "| 本地 adapter /",
        "| 本地复现代码 |",
        "## 原始论文总结",
        "### 背景与主要改动",
        "### 核心公式",
        "### 论文离线与线上效果",
        "## 本地复现",
        "## 复现边界",
        "```mermaid",
    )
    for module, methods in MODULES.items():
        for method, slug in methods.items():
            path = ROOT / "docs" / module / slug / "README.md"
            text = path.read_text(encoding="utf-8")
            for entry in required:
                assert entry in text, f"{module}/{method} missing {entry}"
            assert f"`{method}`" in text
            upstream_line = next(
                line for line in text.splitlines() if line.startswith("| 原作者代码 |")
            )
            assert "http" in upstream_line or "未" in upstream_line
            assert "../../experiments/" in text
