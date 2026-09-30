"""Reviewed P0/P1 metadata for the 2026-09-29 follow-up window."""

LATEST_METHOD_PAPERS = (
    {
        "domain": "foundation-models", "key": "lift-feedback", "title": "Pretraining Latent Information Feedback Transformers with Teacher Supervision",
        "paper_url": "https://arxiv.org/abs/2609.38149", "detail_path": "foundation-models/2609.38149-lift-feedback/README.md",
        "topic": ["网络架构", "潜状态反馈", "预训练"], "first_author": "Dor Tirosh",
        "first_author_affiliation": "Tel Aviv University", "published": "2026-09-29", "code": "https://github.com/dortirosh1/LIFT", "adapter": "lift-feedback", "priority": "P1",
    },
    {
        "domain": "foundation-models", "key": "triadic-linear-attention", "title": "Triadic Linear Attention: Three-Dimensional Recurrent States for Long-Context Sequence Modeling",
        "paper_url": "https://arxiv.org/abs/2609.36529", "detail_path": "foundation-models/2609.36529-triadic-linear-attention/README.md",
        "topic": ["网络架构", "线性注意力", "长上下文"], "first_author": "Oliver Sieberling",
        "first_author_affiliation": "MIT / MIT-IBM Watson AI Lab", "published": "2026-09-29", "code": "https://github.com/OliverSieberling/TriadicLinearAttention", "adapter": "triadic-linear-attention", "priority": "P1",
    },
    {
        "domain": "post-training", "key": "oasis-opsd", "title": "Overcoming Scaling Limits in On-Policy Self-Distillation for LLM Reasoning",
        "paper_url": "https://arxiv.org/abs/2609.37915", "detail_path": "post-training/2609.37915-oasis/README.md",
        "topic": ["On-policy self-distillation", "可验证推理"], "first_author": "Md. Ismail Hossain",
        "first_author_affiliation": "North South University", "published": "2026-09-29", "code": None, "adapter": "oasis-opsd", "priority": "P1",
    },
    {
        "domain": "post-training", "key": "graft", "title": "Learning Beyond What You Sample: Off-Policy-Aware Cross-Model Trajectory Exchange for RLVR",
        "paper_url": "https://arxiv.org/abs/2609.37868", "detail_path": "post-training/2609.37868-graft/README.md",
        "topic": ["RLVR", "跨模型轨迹交换", "离策略校正"], "first_author": "Doohyuk Jang",
        "first_author_affiliation": "KAIST", "published": "2026-09-29", "code": None, "adapter": "graft", "priority": "P1",
    },
    {
        "domain": "post-training", "key": "ride-opd", "title": "The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation",
        "paper_url": "https://arxiv.org/abs/2609.36484", "detail_path": "post-training/2609.36484-ride/README.md",
        "topic": ["On-policy distillation", "表征蒸馏"], "first_author": "Hao Li",
        "first_author_affiliation": "原文未列机构", "published": "2026-09-29", "code": "https://github.com/xixixixixxxx/RIDE", "adapter": "ride-opd", "priority": "P1",
    },
    {
        "domain": "post-training", "key": "pr-opd", "title": "PR-OPD: Privileged Representation On-policy Self-Distillation for Agentic Reinforcement Learning",
        "paper_url": "https://arxiv.org/abs/2609.36642", "detail_path": "post-training/2609.36642-pr-opd/README.md",
        "topic": ["Agentic RL", "On-policy distillation", "表征对齐"], "first_author": "Muyang Li",
        "first_author_affiliation": "University of Florida", "published": "2026-09-29", "code": "https://github.com/balibata/PR-OPD", "adapter": "pr-opd", "priority": "P1",
    },
    {
        "domain": "agent-research", "key": "user-proxy-bench", "title": "UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training",
        "paper_url": "https://arxiv.org/abs/2609.38043", "detail_path": "agent-research/2609.38043-userproxybench/README.md",
        "topic": ["Agent 评测", "用户模拟器", "信息泄漏审计"], "first_author": "Ashish Jain",
        "first_author_affiliation": "原文未列机构", "published": "2026-09-29", "code": None, "adapter": "user-proxy-bench", "priority": "P1",
    },
    {
        "domain": "agent-research", "key": "upliftmem", "title": "UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval",
        "paper_url": "https://arxiv.org/abs/2609.36805", "detail_path": "agent-research/2609.36805-upliftmem/README.md",
        "topic": ["Agent 记忆", "集合 uplift", "主动探测"], "first_author": "Mengkun Liang",
        "first_author_affiliation": "Beihang University", "published": "2026-09-29", "code": None, "adapter": "upliftmem", "priority": "P1",
    },
)
