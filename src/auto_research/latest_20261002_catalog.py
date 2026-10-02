"""Reviewed P0/P1 papers for the 2026-10-02 intake."""

from __future__ import annotations


def _paper(
    domain,
    key,
    title,
    arxiv_id,
    slug,
    topic,
    author,
    affiliation,
    *,
    code=None,
    upstream_note=None,
    priority="P1",
    published="2026-10-01",
    selection_exception=None,
    requires_gpu_validation=False,
    gpu_validation_artifact=None,
):
    root = "reproductions" if domain == "recommendation" else domain
    record = {
        "domain": domain,
        "key": key,
        "title": title,
        "paper_url": f"https://arxiv.org/abs/{arxiv_id}",
        "detail_path": f"{root}/{arxiv_id}-{slug}/README.md",
        "topic": topic,
        "first_author": author,
        "first_author_affiliation": affiliation,
        "published": published,
        "code": code,
        "adapter": key,
        "priority": priority,
    }
    if selection_exception:
        record["selection_exception"] = selection_exception
    if upstream_note:
        record["upstream_note"] = upstream_note
    if requires_gpu_validation:
        record["requires_gpu_validation"] = True
        record["gpu_validation_artifact"] = gpu_validation_artifact
    return record


LATEST_METHOD_PAPERS = (
    _paper(
        "foundation-models", "gemini-for-google",
        "Customizing an LLM for Enterprise Software Engineering",
        "2605.16517", "gemini-for-google",
        ["企业 LLM", "数据治理", "中训练与后训练"],
        "Aditya Kini", "Google", priority="P0", published="2026-05-15",
    ),
    _paper(
        "recommendation", "gear",
        "Generative End-to-end Ad Retrieval at Douyin",
        "2609.39327", "gear", ["广告召回", "生成式检索", "语义 ID"],
        "Shaowen Zeng", "ByteDance", priority="P0", published="2026-09-30",
    ),
    _paper(
        "post-training", "dars",
        "Dependency-Aware Reward Shaping for Agentic Reinforcement Learning",
        "2610.01207", "dars", ["Agentic RL", "依赖图", "步级奖励"],
        "Ziyi Chen", "University of Illinois Urbana-Champaign",
        priority="P0",
        upstream_note=(
            "否：官方仓库 https://github.com/JianhuiWei7/DARS 已建立，"
            "但截至 2026-10-02 明确标注实现仍在准备中"
        ),
    ),
    _paper(
        "agent-research", "active-saddler",
        "ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization",
        "2610.00906", "active-saddler", ["Harness 优化", "主动课程", "RSI"],
        "Sungho Park", "POSTECH",
        code="https://github.com/microsoft/AutoSaddler/tree/feat/activesaddler",
        priority="P0",
    ),
    _paper(
        "agent-research", "safe-self-improvement",
        "Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover",
        "2610.01073", "safe-self-improvement", ["RSI 安全", "验证", "回滚"],
        "Yunbei Zhang", "原文首页未列第一作者机构", priority="P0",
    ),
    _paper(
        "post-training", "range-grpo",
        "Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals",
        "2610.01548", "range-grpo", ["GRPO", "奖励区间", "半监督后训练"],
        "Ryunyi Lee", "Yonsei University", priority="P0",
    ),
    _paper(
        "agent-research", "veriharness",
        "VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks",
        "2610.00972", "veriharness", ["Agent 验证", "证据工具", "长程任务"],
        "Caiqi Zhang", "Google Cloud AI Research", priority="P0",
    ),
    _paper(
        "recommendation", "effective-training-time",
        "Optimizing Effective Training Time for Large-Scale Recommendation Systems",
        "2610.02057", "effective-training-time",
        ["推荐训练系统", "训练有效时间", "GPU 集群"],
        "Mingming Ding", "Meta Platforms, Inc.",
        selection_exception=(
            "用户于 2026-10-02 明确批准的生产训练基础设施例外；"
            "部署指标是 ETT，不作为推荐模型效果或线上 A/B 收益。"
        ),
    ),
    _paper(
        "foundation-models", "taco-optimizer",
        "TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning",
        "2610.02199", "taco-optimizer", ["优化器", "显存效率", "全参微调"],
        "Jichao Jiang", "University of Central Florida",
        code="https://github.com/Jichao2357/TACO_optimizer",
        requires_gpu_validation=True,
        gpu_validation_artifact="docs/gpu-validations/taco-optimizer-a100-20261002.json",
    ),
    _paper(
        "foundation-models", "veto",
        "VETO: Video Efficient Token Optimization for Vision Language Models",
        "2610.01785", "veto", ["视频 VLM", "Token 压缩", "推理效率"],
        "Gueter Josmy Faure", "National Taiwan University",
        requires_gpu_validation=True,
        gpu_validation_artifact="docs/gpu-validations/veto-a100-20261002.json",
    ),
    _paper(
        "agent-research", "mem-plus-plus",
        "Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents",
        "2610.02002", "mem-plus-plus", ["Agent 记忆", "时间检索", "组织知识"],
        "Ahmad Yehia", "The University of Texas at Austin",
        code="https://github.com/AIDAChip-Inc/mem-plus-plus",
    ),
    _paper(
        "agent-research", "defa",
        "DeFA: Dependency-Guided Failure Attribution for LLM Agents",
        "2610.01256", "defa", ["失败归因", "依赖图", "技能进化"],
        "Bo Deng", "Qwen DianJin Team, Alibaba Cloud Computing",
    ),
    _paper(
        "post-training", "my-fault",
        "My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning",
        "2610.01161", "my-fault", ["Agentic RL", "信用分配", "自诊断"],
        "Yihua Zhu", "Alibaba Group",
    ),
    _paper(
        "agent-research", "flowright",
        "It Takes Workflows to Evolve Better Workflows",
        "2610.01026", "flowright", ["工作流进化", "多 Agent", "层级奖励"],
        "Xuehang Guo", "William & Mary",
    ),
    _paper(
        "post-training", "where-opd",
        "Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes",
        "2610.02117", "where-opd", ["多模态后训练", "OPD", "空间引导"],
        "Sophia Sirko-Galouchenko", "Valeo.ai",
        code="https://github.com/sirkosophia/Where-OPD",
    ),
    _paper(
        "recommendation", "gris",
        "Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)",
        "2610.01533", "gris", ["生成式推荐", "语义 ID", "图聚类"],
        "Aleksei Medvedev", "Huawei Ireland Research Centre",
        code="https://github.com/hirc-airecs/graph-informed-sids",
        selection_exception=(
            "用户于 2026-10-02 明确批准的学术/Evolve 机制例外；"
            "论文没有量化线上 A/B，不进入工业证据结论。"
        ),
    ),
    _paper(
        "recommendation", "repair-state",
        "Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders",
        "2610.01270", "repair-state", ["个性化", "用户状态修复", "序列推荐"],
        "Parthiv Chatterjee", "原文首页未列第一作者机构",
        selection_exception=(
            "用户于 2026-10-02 明确批准的学术/Evolve 机制例外；"
            "论文没有量化线上 A/B，不进入工业证据结论。"
        ),
    ),
)
