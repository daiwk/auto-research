"""Reviewed 2026-09-29 announcement batch for the 2026-10-01 intake."""


def _paper(
    domain, key, title, arxiv_id, slug, topic, author, affiliation,
    *, code=None, priority="P1", published="2026-09-29",
):
    root = "reproductions" if domain == "recommendation" else domain
    return {
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


LATEST_METHOD_PAPERS = (
    _paper(
        "agent-research", "meta-reasoning",
        "Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning",
        "2609.38147", "meta-reasoning",
        ["Agent 推理", "元推理控制", "预算调度"],
        "Paras Dahal", "Meta Superintelligence Labs", priority="P0",
    ),
    _paper(
        "agent-research", "context-lm", "Context Language Models",
        "2609.37725", "context-lm", ["上下文管理", "Agent RL", "多 Agent"],
        "Rulin Shao", "University of Washington / Meta Superintelligence Labs",
        code="https://github.com/facebookresearch/context-language-models", priority="P0",
    ),
    _paper(
        "agent-research", "meta-skills",
        "Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI",
        "2609.38143", "meta-skills", ["Harness 设计", "Meta-skill", "RSI"],
        "Cheng Qian", "Apodex / University of Illinois Urbana-Champaign",
        code="https://github.com/qiancheng-apodex/MetaSkill-AI4AI", priority="P0",
    ),
    _paper(
        "agent-research", "branch-mixture",
        "Mixture of Self-Improving Branches for Agent Harness Optimization",
        "2609.37834", "branch-mixture", ["Harness 优化", "分支搜索", "RSI"],
        "Haoyu Dong", "原文首页未列机构", priority="P0",
    ),
    _paper(
        "post-training", "advisd",
        "AdviSD: Learning to Advise Frontier LLMs via Targeted Multi-Turn Self-Distillation",
        "2609.38142", "advisd", ["Advisor", "自蒸馏", "GRPO"],
        "Rishabh Agrawal", "University of Southern California", priority="P0",
    ),
    _paper(
        "post-training", "gats",
        "Guide, Then Let Go: Gap-Adaptive Teacher Scheduling for Sparse-Reward Agentic RL",
        "2609.37898", "gats", ["Agentic RL", "On-policy distillation", "课程调度"],
        "Youling Huang", "Dalian University of Technology / Kuaishou",
        code="https://github.com/Ricardo-H/guide-then-let-go", priority="P0",
    ),
    _paper(
        "recommendation", "cohortmix-ts",
        "Challenges and Solutions for Bandits in the Wild: Warm-Started Mixture Bandits for Cross-Cohort Slate Recommendation",
        "2609.37800", "cohortmix-ts", ["冷启动", "Slate bandit", "跨 cohort 迁移"],
        "Serafima Lebedeva", "DFKI / RPTU Kaiserslautern-Landau",
        code="https://github.com/etowho/university-games", priority="P0",
    ),
    _paper(
        "recommendation", "recap-ctr",
        "Beyond Interaction Capacity: Estimator Scaling with Recursive Models for CTR Prediction",
        "2609.37905", "recap-ctr", ["CTR", "Estimator scaling", "递归网络"],
        "Shivang Chopra", "Georgia Institute of Technology / Google Research",
    ),
    _paper(
        "post-training", "maestro-opd",
        "From Dissonance to Orchestration: Teacher Intervention in On-Policy Distillation",
        "2609.37510", "maestro", ["On-policy distillation", "教师介入", "策略分歧"],
        "Yuhao Wang", "Nanyang Technological University",
        code="https://github.com/yhao-wang/MAESTRO",
    ),
    _paper(
        "post-training", "ipd",
        "Interpolated Policy Distillation: A Controllable Continuum Between Off-Policy and On-Policy Distillation",
        "2609.37170", "ipd", ["策略蒸馏", "分布插值", "Speculative sampling"],
        "Youxu Shi", "WeChat Vision, Tencent",
    ),
    _paper(
        "post-training", "flowmap-opd",
        "FlowMap-OPD: Rollout-Kernel Separation for On-Policy Distillation of Few-Step Flow-Map Generators",
        "2609.37851", "flowmap-opd", ["On-policy distillation", "Flow map", "生成模型"],
        "Zhiqi Li", "Georgia Institute of Technology",
        code="https://github.com/ZhiqiLi-CG/Flowmap_OPD_source",
    ),
    _paper(
        "foundation-models", "vjepa-policy",
        "V-JEPA Policy: Building Effective World-Action Models on Predictive Visual Latents",
        "2609.37250", "vjepa-policy", ["世界动作模型", "预测视觉潜变量", "机器人"],
        "Yang Zhang", "Tsinghua University",
        code="https://github.com/breez3young/VJEPA-Policy",
    ),
    _paper(
        "foundation-models", "ce-guided-moe",
        "Cross-Entropy Guided Routing in Mixture-of-Experts Large Language Models",
        "2609.37751", "ce-guided-moe", ["MoE", "路由", "Token error"],
        "Yury Nahshan", "Bar-Ilan University",
    ),
    _paper(
        "foundation-models", "tadm",
        "Time-Anchored Diffusion Language Models: Latent-Space Caching for Fast Generation",
        "2609.37924", "tadm", ["扩散语言模型", "Latent cache", "推理效率"],
        "Joel Anto Paul", "The University of Texas at Austin",
    ),
    _paper(
        "foundation-models", "pumba",
        "On Trajectory-Aware Training for Masked Diffusion Language Models",
        "2609.37974", "pumba", ["扩散语言模型", "Trajectory-aware training", "BPTT"],
        "Manuel Madeira", "Apple",
    ),
    _paper(
        "foundation-models", "splash",
        "SPLASH: Switching Parallel Layouts of Attention with Seamless Handoff for LLM Serving",
        "2609.37626", "splash", ["推理系统", "并行布局", "KV cache"],
        "Chuan Liu", "Institute of Computing Technology, Chinese Academy of Sciences",
        code="https://github.com/ict-agent/SPLASH-sglang",
    ),
)
