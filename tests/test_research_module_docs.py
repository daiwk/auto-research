from __future__ import annotations

import json
import re
import struct
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _manifest_count(module: str) -> int:
    payload = json.loads(
        (ROOT / "docs" / "research-manifest.json").read_text(encoding="utf-8")
    )
    return sum(paper["domain"] == module for paper in payload["papers"])

MODULES = {
    "post-training": {
        "dpo": "2305.18290-dpo",
        "kto": "2402.01306-kto",
        "orpo": "2403.07691-orpo",
        "grpo": "2402.03300-grpo",
        "tis": "web-2025-tis",
        "icepop": "2510.18855-icepop",
        "online-icepop": "web-2025-online-icepop",
        "ripo": "2607.10169-ripo",
        "kpop": "2606.15079-kpop",
        "gppo": "2508.07629-gppo",
        "dr-grpo": "2503.20783-dr-grpo",
        "armor": "2607.10481-armor",
        "reinforce-plus": "2501.03262-reinforce-plus",
        "taco": "2607.07976-taco",
        "chord": "2508.11408-chord",
        "vapo": "2504.05118-vapo",
        "reco-grpo": "2607.26862-reco",
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
        "slic-hf": "2305.10425-slic-hf",
        "steerlm": "2310.05344-steerlm",
        "spin": "2401.01335-spin",
        "relay-opd": "2607.26057-relay-opd",
        "cort": "2607.25659-cort",
        "gkd": "2306.13649-gkd",
        "minillm": "2306.08543-minillm",
        "opsd": "2601.18734-opsd",
        "opcd": "2602.12275-opcd",
        "beta-opsd": "2607.28582-beta-opsd",
        "vad": "2607.28590-vad",
        "flux-opd": "2607.28022-flux-opd",
        "dash": "2608.06243-dash",
        "distilled-rl": "2607.17247-distilled-rl",
        "u-opsd": "2608.06296-u-opsd",
        "rp-opsd": "2608.06347-rp-opsd",
        "pcsd": "2608.01837-pcsd",
        "adrs": "2608.03223-adrs",
        "mopd": "2606.30406-mopd",
        "opd-lm": "2606.06712-opd-lm",
        "rlaif": "2309.00267-rlaif",
        "process-supervision": "2305.20050-process-supervision",
        "math-shepherd": "2312.08935-math-shepherd",
        "self-rewarding": "2401.10020-self-rewarding",
        "luffy": "2504.14945-luffy",
        "ttrl": "2504.16084-ttrl",
        "absolute-zero": "2505.03335-absolute-zero",
        "intuitor": "2505.19590-intuitor",
        "cispo": "2506.13585-cispo",
        "spiral": "2506.24119-spiral",
        "conspo": "2605.12969-conspo",
        "minirl": "2512.01374-minirl",
        "missing-old-logits": "2605.12070-missing-old-logits",
        "stare": "2606.19236-stare",
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
        "gigpo": "2505.10978-gigpo",
        "steppo": "2604.18401-steppo",
        "swe-agent": "2405.15793-swe-agent",
        "openhands": "2407.16741-openhands",
        "mrkl": "2205.00445-mrkl",
        "hugginggpt": "2303.17580-hugginggpt",
        "generative-agents": "2304.03442-generative-agents",
        "memgpt": "2310.08560-memgpt",
        "webgpt": "2112.09332-webgpt",
        "saycan": "2204.01691-saycan",
        "pal": "2211.10435-pal",
        "art": "2303.09014-art",
        "seed": "2607.14777-seed",
        "cast": "2607.25308-cast",
        "turn-opd": "2607.05804-turn-opd",
        "hiskill": "2607.25853-hiskill",
        "unimem": "2607.26017-unimem",
        "search-r1": "2503.09516-search-r1",
        "ragen": "2504.20073-ragen",
        "loop": "2502.01600-loop",
        "webagent-r1": "2505.16421-webagent-r1",
        "mua-rl": "2508.18669-mua-rl",
        "cam-df": "2607.27083-cam-df",
        "skillrise": "2607.26784-skillrise",
        "tapo": "2607.27973-tapo",
        "grsd": "2607.28076-grsd",
        "os-shepherd": "2607.28609-osreward",
        "envace": "2608.06197-envace",
        "agent-opsd": "2608.05987-agent-opsd",
        "ocsd": "2608.04788-ocsd",
        "vermem": "2608.03137-vermem",
        "coevo-mem": "2608.01739-coevo-mem",
        "deepresearcher": "2504.03160-deepresearcher",
        "retool": "2504.11536-retool",
        "toolrl": "2504.13958-toolrl",
        "sage": "2512.17102-sage",
        "memskill": "2602.02474-memskill",
        "memento-skills": "2603.18743-memento-skills",
        "searl": "2604.07791-searl",
        "agent0": "2511.16043-agent0",
        "agent-r1": "2511.14460-agent-r1",
        "camel": "2303.17760-camel",
        "toolbench": "2305.16504-toolbench",
        "gaia": "2311.12983-gaia",
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


def test_site_uses_workflows_and_four_research_domains():
    homepage = (ROOT / "docs" / "index.md").read_text(encoding="utf-8")
    library = (ROOT / "docs" / "research-library.md").read_text(encoding="utf-8")
    evolution = (ROOT / "docs" / "evolution-domains.md").read_text(encoding="utf-8")
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert "## 两大核心工作流" in homepage
    assert "## 工作流 × 研究领域" in homepage
    assert "## 四大核心能力" not in homepage
    assert homepage.count('<div class="ar-capability-card ') == 2
    for domain in (
        "搜广推与 LLM 应用",
        "基础模型",
        "LLM 后训练",
        "Agent",
        "其他主题",
    ):
        assert domain in homepage

    for target in (
        "reproductions/industrial.md",
        "foundation-models/README.md",
        "post-training/README.md",
        "agent-research/README.md",
    ):
        assert f"({target})" in library

    assert "论文检索约束的组合式 genome" in evolution
    assert evolution.count("**可运行**") >= 4
    protocol = (ROOT / "docs" / "model-evolution.md").read_text(encoding="utf-8")
    overview = (ROOT / "docs" / "auto-research.md").read_text(encoding="utf-8")
    for required in (
        "## 候选到底从哪里来 {#candidate-sources}",
        "evidence-only",
        "不会把论文 PDF 翻译成 Python",
        "## 最短操作路径",
    ):
        assert required in protocol
    assert "## 先理解候选来源" in overview
    assert "新的工程假设" in overview
    assert "  - 自动研究与进化:" in navigation
    assert "  - 论文实现与评测:" in navigation
    assert "      - 基础模型:" in navigation
    assert "      - LLM 后训练:" in navigation
    assert "      - Agent:" in navigation


def test_foundation_models_have_a_separate_scalable_catalog():
    directory = ROOT / "docs" / "foundation-models"
    overview = (directory / "README.md").read_text(encoding="utf-8")
    for name in ("catalog.md", "lineage.md", "benchmark.md"):
        assert (directory / name).is_file()
        assert f"({name})" in overview
    for dimension in ("organization", "topic", "year"):
        relative = f"catalog/by-{dimension}.md"
        assert (directory / relative).is_file()
        assert f"({relative})" in overview

    topic = (directory / "catalog" / "by-topic.md").read_text(encoding="utf-8")
    for heading in (
        "## 网络架构",
        "## 注意力与长上下文",
        "## 预训练与数据",
        "## 多模态基础模型",
        "## 推理与系统效率",
    ):
        assert heading in topic


def test_recommendation_and_foundation_method_indexes_are_in_navigation():
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    expected = (
        ("recommendation", "reproductions", "reproductions/catalog.md"),
        ("foundation-models", "foundation-models", "foundation-models/catalog.md"),
    )
    manifest = json.loads(
        (ROOT / "docs" / "research-manifest.json").read_text(encoding="utf-8")
    )

    for domain, directory, nav_target in expected:
        assert f"- 方法索引: {nav_target}" in navigation
        index = (ROOT / "docs" / directory / "catalog.md").read_text(
            encoding="utf-8"
        )
        papers = [paper for paper in manifest["papers"] if paper["domain"] == domain]
        assert papers
        for paper in papers:
            assert f"`{paper['key']}`" in index
        assert "未标注机构" not in index
        assert "| 未标注" not in index


def test_sidebar_hides_global_and_per_paper_indexes_but_keeps_paper_pages():
    navigation = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    assert "全域论文谱系与缺口:" not in navigation
    assert "          - 论文实现:" not in navigation
    assert "post-training/2403.07691-orpo/README.md" not in navigation
    assert (ROOT / "docs" / "research-lineage.md").is_file()
    assert (
        ROOT / "docs" / "post-training" / "2403.07691-orpo" / "README.md"
    ).is_file()


def test_global_recommendation_lineage_has_no_dead_end_dcn_branch():
    lineage = (ROOT / "docs" / "research-lineage.md").read_text(encoding="utf-8")
    assert 'F["特征交互<br/>DeepFM / DCN-V2"]' in lineage
    assert 'F --> M["多任务与现代排序<br/>ESMM / MMoE / PLE"]' in lineage
    assert 'M --> H["长序列与大规模排序<br/>HSTU / RankMixer / HyFormer"]' in lineage
    assert 'W --> C["DCN-V2"]' not in lineage


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
            if slug.startswith("web-"):
                continue
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


def test_web_method_pages_have_complete_source_contract():
    methods = {
        "tis": (
            "web-2025-tis",
            "https://fengyao.notion.site/off-policy-rl",
            "2025-08-05",
        ),
        "online-icepop": (
            "web-2025-online-icepop",
            "https://zhuanlan.zhihu.com/p/1984379979035850499",
            "2025-12-16（作者公开说明页首发）",
        ),
    }
    required = (
        "## 资料信息",
        "| 资料链接 |",
        "| 公司 / 机构 |",
        "| 首次公开日期 |",
        "| 原作者代码 |",
        "| 本地 adapter /",
        "| 本地复现代码 |",
        "## 原始资料总结",
        "### 背景与主要改动",
        "### 核心公式",
        "### 资料离线与线上效果",
        "## 本地复现",
        "## 复现边界",
        "```mermaid",
    )
    for method, (slug, source_url, published) in methods.items():
        text = (
            ROOT / "docs" / "post-training" / slug / "README.md"
        ).read_text(encoding="utf-8")
        for entry in required:
            assert entry in text, f"post-training/{method} missing {entry}"
        assert f"`{method}`" in text
        assert source_url in text
        assert f"| 首次公开日期 | {published} |" in text
        assert "../../experiments/" in text


def test_icepop_paper_metadata_uses_the_ring_1t_report():
    text = (
        ROOT
        / "docs"
        / "post-training"
        / "2510.18855-icepop"
        / "README.md"
    ).read_text(encoding="utf-8")

    assert "https://arxiv.org/abs/2510.18855" in text
    assert "| 公司 / 机构 | Ant Group / Inclusion AI |" in text
    assert "| 首次公开日期 | 2025-10-21 |" in text
    assert "| 原作者代码 | 未发现/未发布 IcePop 独立算法源代码 |" in text


def test_post_training_and_agent_catalogs_cover_three_browse_dimensions():
    for module, methods in MODULES.items():
        overview = (ROOT / "docs" / module / "README.md").read_text(encoding="utf-8")
        for dimension in ("organization", "topic", "year"):
            relative = f"catalog/by-{dimension}.md"
            assert f"({relative})" in overview
            catalog = (ROOT / "docs" / module / relative).read_text(encoding="utf-8")
            for method, slug in methods.items():
                assert f"(../{slug}/README.md)" in catalog, (
                    f"{module}/{method} missing from by-{dimension}"
                )
            assert "详情页包含核心机制、公式、原文结果和本地复现边界" not in catalog
            entries = [
                line
                for line in catalog.splitlines()
                if line.startswith("- ") and "](../" in line
            ]
            assert len(entries) == _manifest_count(module)
            for entry in entries:
                summary = entry.split("）：", 1)[-1]
                assert len(summary) >= 35, (
                    f"{module}/{dimension} has a thin method summary: {entry}"
                )


def test_organization_catalogs_group_by_first_author_affiliation():
    for module, methods in MODULES.items():
        text = (
            ROOT / "docs" / module / "catalog" / "by-organization.md"
        ).read_text(encoding="utf-8")
        assert "按机构/公司/学校" in text
        assert "按论文一作的第一署名单位聚合" in text
        assert "## " in text
        entries = [
            line for line in text.splitlines()
            if line.startswith("- ") and "](../" in line
        ]
        assert len(entries) == _manifest_count(module)
        assert all(re.search(r"^- \d{4}-\d{2}-\d{2} · 一作：.+ · \[", line) for line in entries)
        assert "（按一作归档）" not in text


def test_topic_catalogs_use_a_compact_two_level_taxonomy():
    """Keep topic pages navigable as the number of papers keeps growing."""

    expected = {
        "post-training": {
            "## 偏好建模与监督",
            "## 在线强化学习与稳定性",
            "## 蒸馏与训练闭环",
            "### 成对、单样本与排序偏好",
            "### PPO、REINFORCE 与 group RL",
        },
        "agent-research": {
            "## Agentic RL 与后训练",
            "## 规划、搜索与反思",
            "## 记忆、技能与持续学习",
            "### 通用轨迹与 credit assignment",
            "### 主动 / 长期记忆",
        },
    }
    for module, headings in expected.items():
        text = (ROOT / "docs" / module / "catalog" / "by-topic.md").read_text(
            encoding="utf-8"
        )
        assert "研究方向 → 方法簇 → 论文" in text
        for heading in headings:
            assert heading in text


def test_every_paper_page_has_a_valid_original_paper_figure():
    """Keep figures mandatory for all current and future paper pages."""

    paper_pages = []
    for module in ("reproductions", "post-training", "agent-research"):
        for path in (ROOT / "docs" / module).glob("*/README.md"):
            text = path.read_text(encoding="utf-8")
            if "## 论文信息" in text:
                paper_pages.append((path, text))

    assert len(paper_pages) >= 187
    for path, text in paper_pages:
        for entry in (
            "<!-- paper-figure:start -->",
            "### 原论文关键图",
            "assets/paper-figure-01.png",
            "图片来自[原论文]",
            "版权归原作者所有",
            "<!-- paper-figure:end -->",
        ):
            assert entry in text, f"{path.relative_to(ROOT)} missing {entry}"

        asset = path.parent / "assets" / "paper-figure-01.png"
        assert asset.is_file(), f"{asset.relative_to(ROOT)} missing"
        data = asset.read_bytes()
        assert data[:8] == b"\x89PNG\r\n\x1a\n"
        assert len(data) >= 5_000, f"{asset.relative_to(ROOT)} is unexpectedly small"
        width, height = struct.unpack(">II", data[16:24])
        assert width >= 400 and height >= 140, (
            f"{asset.relative_to(ROOT)} is unreadable at {width}x{height}"
        )
