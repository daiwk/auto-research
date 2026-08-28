#!/usr/bin/env python3
"""Synchronize the unified research manifest with registered paper adapters."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PATH = DOCS / "research-manifest.json"
sys.path.insert(0, str(ROOT / "src"))

from auto_research.reproductions.manifest import PaperManifest
from auto_research.reproductions.registry import list_adapters
from auto_research.historical_b07_b11 import PAPERS as HISTORICAL_B07_B11


POST_TRAINING_KEYS = {"dynamic-rubric", "off-context-grpo", "sis"}

FIRST_AUTHOR_OVERRIDES = {
    "tagr": "Wencai Ye",
    "wemm-embedding": "Junjie Zhou",
}

LATEST_METHOD_PAPERS = (
    {
        "domain": "post-training", "key": "v-rubrics",
        "title": "V-Rubrics: Visual Faithfulness via Rubric-Based Reinforcement Learning",
        "paper_url": "https://arxiv.org/abs/2608.25580",
        "detail_path": "post-training/2608.25580-v-rubrics/README.md",
        "topic": ["多模态 rubric RL"], "first_author": "Shulin Tian",
        "first_author_affiliation": "S-Lab, Nanyang Technological University",
        "published": "2026-08-26", "code": "https://shulin16.github.io/v-rubrics/",
        "adapter": "v-rubrics",
    },
    {
        "domain": "post-training", "key": "clue-opsd",
        "title": "Where to Look Matters: On-Policy Self-Distillation for Long-Video Understanding",
        "paper_url": "https://arxiv.org/abs/2608.25356",
        "detail_path": "post-training/2608.25356-clue-opsd/README.md",
        "topic": ["长视频特权视图 OPD"], "first_author": "Kaishen Wang",
        "first_author_affiliation": "University of Maryland, College Park",
        "published": "2026-08-26", "code": None, "adapter": "clue-opsd",
    },
    {
        "domain": "post-training", "key": "grin",
        "title": "From Memorization to Absorption: Mixed-Policy RL for Continual Knowledge Injection",
        "paper_url": "https://arxiv.org/abs/2608.25243",
        "detail_path": "post-training/2608.25243-grin/README.md",
        "topic": ["混合策略知识注入 RL"], "first_author": "Zhibo Hou",
        "first_author_affiliation": "University of California, Merced",
        "published": "2026-08-26", "code": None, "adapter": "grin",
    },
    {
        "domain": "post-training", "key": "grip",
        "title": "GRIP: Granular Reward-Guided Parameter Interpolation for Efficient Reasoning",
        "paper_url": "https://arxiv.org/abs/2608.25583",
        "detail_path": "post-training/2608.25583-grip/README.md",
        "topic": ["奖励引导参数插值"], "first_author": "Lam So",
        "first_author_affiliation": "Peking University",
        "published": "2026-08-26", "code": None, "adapter": "grip",
    },
    {
        "domain": "agent-research", "key": "jit-agent",
        "title": "JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution",
        "paper_url": "https://arxiv.org/abs/2608.25593",
        "detail_path": "agent-research/2608.25593-jit-agent/README.md",
        "topic": ["Harness 即时生成与进化"], "first_author": "Guibin Zhang",
        "first_author_affiliation": "LV-NUS Lab", "published": "2026-08-26",
        "code": "https://github.com/bingreeky/JIT", "adapter": "jit-agent",
    },
    {
        "domain": "agent-research", "key": "traceml",
        "title": "TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development",
        "paper_url": "https://arxiv.org/abs/2608.26086",
        "detail_path": "agent-research/2608.26086-traceml/README.md",
        "topic": ["ML 开发轨迹规划"], "first_author": "Jiarui Yan",
        "first_author_affiliation": "Carnegie Mellon University", "published": "2026-08-26",
        "code": "https://huggingface.co/datasets/jerryyan/TraceML", "adapter": "traceml",
    },
    {
        "domain": "agent-research", "key": "adavdr",
        "title": "AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research",
        "paper_url": "https://arxiv.org/abs/2608.25559",
        "detail_path": "agent-research/2608.25559-adavdr/README.md",
        "topic": ["视频研究自适应工具与反思"], "first_author": "Xintong Zhang",
        "first_author_affiliation": "Accio Team, Alibaba Group", "published": "2026-08-26",
        "code": "https://github.com/Accio-Lab/AdaVDR", "adapter": "adavdr",
    },
    {
        "domain": "agent-research", "key": "topas",
        "title": "TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving",
        "paper_url": "https://arxiv.org/abs/2608.25523",
        "detail_path": "agent-research/2608.25523-topas/README.md",
        "topic": ["工作流 Prefix-State 调度"], "first_author": "Hongqiu Ni",
        "first_author_affiliation": "University of Science and Technology of China",
        "published": "2026-08-26", "code": None, "adapter": "topas",
    },
    {
        "domain": "agent-research", "key": "caskg",
        "title": "CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval",
        "paper_url": "https://arxiv.org/abs/2608.25500",
        "detail_path": "agent-research/2608.25500-caskg/README.md",
        "topic": ["反事实因果技能图"], "first_author": "Zhiyuan Li",
        "first_author_affiliation": "Jilin University / Ant Group", "published": "2026-08-26",
        "code": "https://github.com/ZhiyuanLi218/Caskg", "adapter": "caskg",
    },
    {
        "domain": "agent-research", "key": "progrouter",
        "title": "ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs",
        "paper_url": "https://arxiv.org/abs/2608.25992",
        "detail_path": "agent-research/2608.25992-progrouter/README.md",
        "topic": ["在线进展成本路由"], "first_author": "Songyuan Li",
        "first_author_affiliation": "Aston University", "published": "2026-08-26",
        "code": None, "adapter": "progrouter",
    },
    {
        "domain": "post-training", "key": "opd-search-plus",
        "title": "OPDSearch+: Search-Enhanced On-Policy Distillation with Reinforcement Learning",
        "paper_url": "https://arxiv.org/abs/2608.24310",
        "detail_path": "post-training/2608.24310-opd-search-plus/README.md",
        "topic": ["搜索增强 OPD + RL"], "first_author": "Qinglin Ye",
        "first_author_affiliation": "University of Chinese Academy of Sciences",
        "published": "2026-08-25", "code": None,
        "adapter": "opd-search-plus",
    },
    {
        "domain": "post-training", "key": "opdvr",
        "title": "OPDVR: On-Policy Distillation with Verifiable Rewards",
        "paper_url": "https://arxiv.org/abs/2608.24696",
        "detail_path": "post-training/2608.24696-opdvr/README.md",
        "topic": ["可验证奖励 OPD"], "first_author": "Wenze Lin",
        "first_author_affiliation": "LeapLab, Tsinghua University",
        "published": "2026-08-25", "code": "https://github.com/LeapLabTHU/OPDVR",
        "adapter": "opdvr",
    },
    {
        "domain": "agent-research", "key": "spo-plus-plus",
        "title": "SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction",
        "paper_url": "https://arxiv.org/abs/2608.24870",
        "detail_path": "agent-research/2608.24870-spo-plus-plus/README.md",
        "topic": ["异步单流 Agent RL"], "first_author": "Kai Ruan",
        "first_author_affiliation": "Renmin University of China",
        "published": "2026-08-25", "code": None,
        "adapter": "spo-plus-plus",
    },
    {
        "domain": "agent-research", "key": "skillforge",
        "title": "SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents",
        "paper_url": "https://arxiv.org/abs/2608.24747",
        "detail_path": "agent-research/2608.24747-skillforge/README.md",
        "topic": ["可验证技能锻造"], "first_author": "Shidong Yang",
        "first_author_affiliation": "AMAP, Alibaba Group",
        "published": "2026-08-25", "code": None,
        "adapter": "skillforge",
    },
    {
        "domain": "agent-research", "key": "ahead",
        "title": "AHEAD: Agentic Hints for Effective Agent Development",
        "paper_url": "https://arxiv.org/abs/2608.24114",
        "detail_path": "agent-research/2608.24114-ahead/README.md",
        "topic": ["环境反馈提示训练"], "first_author": "Xiaolong Jin",
        "first_author_affiliation": "AWS AI Labs / Purdue University",
        "published": "2026-08-25", "code": None,
        "adapter": "ahead",
    },
    {
        "domain": "agent-research", "key": "smith",
        "title": "SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification",
        "paper_url": "https://arxiv.org/abs/2608.24571",
        "detail_path": "agent-research/2608.24571-smith/README.md",
        "topic": ["多维验证工具自进化"], "first_author": "Zhi Rui Tam",
        "first_author_affiliation": "Appier AI Research / National Taiwan University",
        "published": "2026-08-25", "code": "https://github.com/appier-research/smith",
        "adapter": "smith",
    },
    {
        "domain": "post-training", "key": "srpo",
        "title": "SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning",
        "paper_url": "https://arxiv.org/abs/2608.23493",
        "detail_path": "post-training/2608.23493-srpo/README.md",
        "topic": ["反思式 token 信用"], "first_author": "Jialong Liu",
        "first_author_affiliation": "Wuhan University",
        "published": "2026-08-24", "code": "https://github.com/Galleons2029/SRPO",
        "adapter": "srpo",
    },
    {
        "domain": "post-training", "key": "erpo",
        "title": "Beyond the Stability-Exploration Dilemma: Environmental Regularization for LLM Policy Optimization",
        "paper_url": "https://arxiv.org/abs/2608.23311",
        "detail_path": "post-training/2608.23311-erpo/README.md",
        "topic": ["输入侧 Query-KL"], "first_author": "Xianlei Zhou",
        "first_author_affiliation": "AMAP, Alibaba Group",
        "published": "2026-08-24", "code": "https://github.com/alibaba/ERPO",
        "adapter": "erpo",
    },
    {
        "domain": "agent-research", "key": "agent-g2",
        "title": "Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning",
        "paper_url": "https://arxiv.org/abs/2608.23318",
        "detail_path": "agent-research/2608.23318-agent-g2/README.md",
        "topic": ["高斯 guidance Agent RL"], "first_author": "Zixuan Wang",
        "first_author_affiliation": "Baidu",
        "published": "2026-08-24", "code": "https://github.com/ZJU-REAL/Agent-G2",
        "adapter": "agent-g2",
    },
    {
        "domain": "agent-research", "key": "autosaddler",
        "title": "AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces",
        "paper_url": "https://arxiv.org/abs/2608.23041",
        "detail_path": "agent-research/2608.23041-autosaddler/README.md",
        "topic": ["Harness 自动优化"], "first_author": "Sungho Park",
        "first_author_affiliation": "Microsoft / POSTECH",
        "published": "2026-08-24", "code": None,
        "adapter": "autosaddler",
    },
    {
        "domain": "post-training", "key": "gcpo",
        "title": "GCPO: Diagnosing and Constraining Subspace Geometry in Rollout RL for LLMs",
        "paper_url": "https://arxiv.org/abs/2608.11674",
        "detail_path": "post-training/2608.11674-gcpo/README.md",
        "topic": ["几何约束 RL"], "first_author": "Kai Yang",
        "first_author_affiliation": "Shanghai AI Laboratory",
        "published": "2026-08-12", "code": "https://github.com/Icarus1411/GCPO",
        "adapter": "gcpo",
    },
    {
        "domain": "agent-research", "key": "auso",
        "title": "AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization",
        "paper_url": "https://arxiv.org/abs/2608.21292",
        "detail_path": "agent-research/2608.21292-auso/README.md",
        "topic": ["动作级技能优化"], "first_author": "Huizu Lin",
        "first_author_affiliation": "University of Science and Technology of China",
        "published": "2026-08-21", "code": "https://github.com/JordanSancholhz/Action-Skill",
        "adapter": "auso",
    },
    {
        "domain": "agent-research", "key": "agentx",
        "title": "AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems",
        "paper_url": "https://arxiv.org/abs/2606.26859",
        "detail_path": "agent-research/2606.26859-agentx/README.md",
        "topic": ["研究自动化", "工业推荐 Agent"], "first_author": "AgentX Team",
        "first_author_affiliation": "Kuaishou",
        "published": "2026-06-26", "code": None,
        "adapter": "agentx",
    },
    {
        "domain": "post-training", "key": "ttpo",
        "title": "TTPO: Test-Time Policy Optimization",
        "paper_url": "https://arxiv.org/abs/2608.27448",
        "detail_path": "post-training/2608.27448-ttpo/README.md",
        "topic": ["测试时强化学习"], "first_author": "Aozhe Wang",
        "first_author_affiliation": "Zhejiang University",
        "published": "2026-08-27", "code": "https://github.com/ZJU-REAL/TTPO",
        "adapter": "ttpo",
    },
    {
        "domain": "post-training", "key": "weak-guide-rlvr",
        "title": "Boosting LLM Exploration via Weak-Model Guidance in RLVR",
        "paper_url": "https://arxiv.org/abs/2608.27420",
        "detail_path": "post-training/2608.27420-weak-guide-rlvr/README.md",
        "topic": ["弱模型前缀探索"], "first_author": "Xingyu Shen",
        "first_author_affiliation": "Peking University",
        "published": "2026-08-27", "code": None, "adapter": "weak-guide-rlvr",
    },
    {
        "domain": "post-training", "key": "uc-mopd",
        "title": "Preserving General Capabilities during Domain Specialization with Uncertainty-Calibrated MOPD",
        "paper_url": "https://arxiv.org/abs/2608.26735",
        "detail_path": "post-training/2608.26735-uc-mopd/README.md",
        "topic": ["多教师能力整合"], "first_author": "Ziyuan Liu",
        "first_author_affiliation": "Peking University",
        "published": "2026-08-27", "code": None, "adapter": "uc-mopd",
    },
    {
        "domain": "post-training", "key": "spear",
        "title": "SPEAR: Distilling Domain-Adaptive Reasoning Skeletons via Sequential Symbolic Alignment in Reinforcement Learning",
        "paper_url": "https://arxiv.org/abs/2608.26550",
        "detail_path": "post-training/2608.26550-spear/README.md",
        "topic": ["过程奖励"], "first_author": "Zhuochun Li",
        "first_author_affiliation": "University of Pittsburgh",
        "published": "2026-08-27", "code": "https://github.com/zhuochunli/SPEAR",
        "adapter": "spear",
    },
    {
        "domain": "agent-research", "key": "swe-prime",
        "title": "SWE-Prime: Fewer Trajectories, Better Performance",
        "paper_url": "https://arxiv.org/abs/2608.27449",
        "detail_path": "agent-research/2608.27449-swe-prime/README.md",
        "topic": ["软件轨迹筛选"], "first_author": "Dewu Zheng",
        "first_author_affiliation": "Sun Yat-sen University",
        "published": "2026-08-27", "code": None, "adapter": "swe-prime",
    },
    {
        "domain": "agent-research", "key": "harnesslens",
        "title": "Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification",
        "paper_url": "https://arxiv.org/abs/2608.27311",
        "detail_path": "agent-research/2608.27311-harnesslens/README.md",
        "topic": ["行为相关 Harness 验证"], "first_author": "Jinghan Xu",
        "first_author_affiliation": "Fudan University",
        "published": "2026-08-27", "code": "https://github.com/jhxu5214/HarnessLens",
        "adapter": "harnesslens",
    },
    {
        "domain": "agent-research", "key": "covemem",
        "title": "When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems",
        "paper_url": "https://arxiv.org/abs/2608.26895",
        "detail_path": "agent-research/2608.26895-covemem/README.md",
        "topic": ["可训练协同记忆"], "first_author": "Hanchong Chen",
        "first_author_affiliation": "Shenzhen Technology University",
        "published": "2026-08-27", "code": None, "adapter": "covemem",
    },
    {
        "domain": "agent-research", "key": "spt",
        "title": "SPT: Skills as Pre-Training Data for Agentic Language Models",
        "paper_url": "https://arxiv.org/abs/2608.26563",
        "detail_path": "agent-research/2608.26563-spt/README.md",
        "topic": ["Agent 技能预训练"], "first_author": "Yufei Sun",
        "first_author_affiliation": "Beijing University of Posts and Telecommunications",
        "published": "2026-08-27", "code": None, "adapter": "spt",
    },
) + tuple(
    {
        "domain": paper.domain,
        "key": paper.key,
        "title": paper.title,
        "paper_url": f"https://arxiv.org/abs/{paper.arxiv_id}",
        "detail_path": f"{paper.domain}/{paper.arxiv_id}-{paper.key}/README.md",
        "topic": list(paper.topic),
        "first_author": paper.first_author,
        "first_author_affiliation": paper.organization,
        "published": paper.published,
        "code": paper.code_url,
        "adapter": paper.key,
    }
    for paper in HISTORICAL_B07_B11
    if paper.domain in {"post-training", "agent-research"}
)


def _detail_path(adapter) -> str:
    matches = sorted((DOCS / "reproductions").glob(
        f"{adapter.paper.arxiv_id}-{adapter.key}/README.md"
    ))
    if len(matches) != 1:
        raise ValueError(
            f"expected one detail page for {adapter.key}, found {len(matches)}"
        )
    return str(matches[0].relative_to(DOCS))


def synchronize(payload: dict) -> dict:
    existing = {
        (paper["domain"], paper["key"]): paper
        for paper in payload.get("papers", [])
    }
    adapters = list_adapters()
    adapter_keys = {adapter.key for adapter in adapters}
    papers = [
        paper for paper in payload.get("papers", [])
        if not isinstance(paper.get("adapter"), dict)
        or paper["key"] in adapter_keys
    ]
    positions = {
        (paper["domain"], paper["key"]): index
        for index, paper in enumerate(papers)
    }
    for adapter in adapters:
        domain = (
            "post-training" if adapter.key in POST_TRAINING_KEYS
            else "recommendation" if adapter.paper.track == "recommendation"
            else "foundation-models"
        )
        identity = (domain, adapter.key)
        previous = existing.get(identity, {})
        record = {
            "domain": domain,
            "key": adapter.key,
            "title": adapter.paper.title,
            "paper_url": adapter.paper.url,
            "detail_path": _detail_path(adapter),
            "topic": list(adapter.paper.topics),
            "first_author": (
                previous.get("first_author")
                or FIRST_AUTHOR_OVERRIDES.get(adapter.key)
            ),
            "first_author_affiliation": (
                previous.get("first_author_affiliation")
                or adapter.paper.organization
            ),
            "published": adapter.paper.published,
            "code": adapter.paper.code_url,
            "adapter": PaperManifest.from_adapter(adapter).to_dict(),
        }
        if identity in positions:
            papers[positions[identity]] = record
        else:
            positions[identity] = len(papers)
            papers.append(record)
    for record in LATEST_METHOD_PAPERS:
        identity = (record["domain"], record["key"])
        if not (DOCS / record["detail_path"]).is_file():
            raise ValueError(f"missing detail page for {identity}: {record['detail_path']}")
        if identity in positions:
            papers[positions[identity]] = record
        else:
            positions[identity] = len(papers)
            papers.append(record)
    return {
        "schema_version": 1,
        "description": (
            "Canonical metadata for all research domains; generated pages must not "
            "maintain paper tables."
        ),
        "papers": sorted(papers, key=lambda paper: (paper["domain"], paper["key"])),
    }


def main() -> None:
    payload = json.loads(PATH.read_text(encoding="utf-8"))
    PATH.write_text(
        json.dumps(synchronize(payload), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
