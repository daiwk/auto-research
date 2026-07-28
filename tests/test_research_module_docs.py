from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MODULES = {
    "post-training": {
        "dpo": "2305.18290-dpo",
        "kto": "2402.01306-kto",
        "orpo": "2403.07691-orpo",
        "grpo": "2402.03300-grpo",
        "ppo-rlhf": "2203.02155-ppo-rlhf",
        "rloo": "2402.14740-rloo",
        "remax": "2310.10505-remax",
        "dapo": "2503.14476-dapo",
        "gspo": "2507.18071-gspo",
        "lightning-opd": "2604.13010-lightning-opd",
        "gprl": "2605.18721-gprl",
        "tcr": "2607.19824-tcr",
        "ipo": "2310.12036-ipo",
        "simpo": "2405.14734-simpo",
        "luspo": "2602.05261-luspo",
        "coba-rl": "2606.22317-coba-rl",
        "constitutional-ai": "2212.08073-constitutional-ai",
        "rrhf": "2304.05302-rrhf",
        "raft": "2304.06767-raft",
    },
    "agent-research": {
        "toolformer": "2302.04761-toolformer",
        "self-refine": "2303.17651-self-refine",
        "rewoo": "2305.18323-rewoo",
        "autogen": "2308.08155-autogen",
        "pearl": "2601.20439-pearl",
        "tree-of-thoughts": "2305.10601-tree-of-thoughts",
        "lats": "2310.04406-lats",
        "react": "2210.03629-react",
        "reflexion": "2303.11366-reflexion",
        "voyager": "2305.16291-voyager",
        "u-mem": "2602.22406-u-mem",
        "legomem": "2510.04851-legomem",
        "memtool": "2507.21428-memtool",
        "metagpt": "2308.00352-metagpt",
        "critic": "2305.11738-critic",
        "agent-lightning": "2508.03680-agent-lightning",
        "swe-agent": "2405.15793-swe-agent",
        "openhands": "2407.16741-openhands",
        "mrkl": "2205.00445-mrkl",
        "hugginggpt": "2303.17580-hugginggpt",
        "generative-agents": "2304.03442-generative-agents",
        "memgpt": "2310.08560-memgpt",
    },
}


def test_research_modules_have_scalable_hub_structure():
    for module, methods in MODULES.items():
        directory = ROOT / "docs" / module
        for name in ("README.md", "catalog.md", "lineage.md", "benchmark.md"):
            assert (directory / name).is_file(), f"{module} missing {name}"

        overview = (directory / "README.md").read_text(encoding="utf-8")
        catalog = (directory / "catalog.md").read_text(encoding="utf-8")
        assert "## 快速入口" in overview
        assert "## 研究闭环" in overview
        assert "## 后续扩展约定" in overview
        assert "(catalog.md)" in overview
        assert "(benchmark.md)" in overview
        assert "(lineage.md)" in overview
        for method, slug in methods.items():
            assert f"({slug}/README.md)" in overview
            assert f"({slug}/README.md)" in catalog
            assert f"`{method}`" in catalog


def test_site_uses_workflows_by_domains_instead_of_four_peer_products():
    homepage = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
    library = (ROOT / "docs" / "research-library.md").read_text(encoding="utf-8")
    evolution = (ROOT / "docs" / "evolution-domains.md").read_text(encoding="utf-8")
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert "## 两大核心工作流" in homepage
    assert "## 工作流 × 研究领域" in homepage
    assert "## 四大核心能力" not in homepage
    assert homepage.count('<div class="ar-capability-card ') == 2
    for domain in ("搜广推与 LLM 应用", "纯 LLM", "Agent", "其他主题"):
        assert domain in homepage

    for target in (
        "reproductions/README.md",
        "post-training/README.md",
        "agent-research/README.md",
    ):
        assert f"({target})" in library

    assert "论文检索约束的组合式 genome" in evolution
    assert evolution.count("**可运行**") >= 4
    assert "  - 自动研究与进化:" in navigation
    assert "  - 论文实现与评测:" in navigation
    assert "      - 纯 LLM 后训练:" in navigation
    assert "      - Agent:" in navigation


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
