"""Reviewed P1 metadata for the 2026-09-28--30 closure batch."""


def _paper(
    domain, key, title, arxiv_id, slug, topic, author, affiliation,
    code=None, published="2026-09-28",
):
    root = "reproductions" if domain == "recommendation" else domain
    return {
        "domain": domain, "key": key, "title": title,
        "paper_url": f"https://arxiv.org/abs/{arxiv_id}",
        "detail_path": f"{root}/{arxiv_id}-{slug}/README.md",
        "topic": topic, "first_author": author,
        "first_author_affiliation": affiliation, "published": published,
        "code": code, "adapter": key, "priority": "P1",
    }


LATEST_METHOD_PAPERS = (
    _paper(
        "recommendation", "evoskillrec",
        "EvoSkillRec: Skill-Genome Evolution for Recommender Architecture Discovery",
        "2609.34552", "evoskillrec", ["推荐模型自动进化", "结构搜索"],
        "Xiaopeng Li", "City University of Hong Kong",
        "https://github.com/Xiaopengli1/EvoSkill-Rec",
    ),
    _paper(
        "recommendation", "promptshift",
        "Measuring and Mitigating Identity-Cue Preference Drift in LLM-based Recommender Systems",
        "2609.34229", "promptshift", ["LLM 推荐", "公平性与漂移"],
        "Zhuoxiong Gan", "University of Electronic Science and Technology of China",
    ),
    _paper(
        "foundation-models", "telescopic-lm", "Telescopic Language Models",
        "2609.35769", "telescopic-lm", ["网络架构", "弹性深度"],
        "Zhilin Guo", "University of Cambridge",
    ),
    _paper(
        "foundation-models", "frac-ssm",
        "Fractional State Space Transition for Long Sequence Modeling",
        "2609.36314", "frac-ssm", ["状态空间模型", "长上下文"],
        "Ivan Kobyzev", "Huawei Noah's Ark Lab, Montreal Research Center",
        "https://github.com/anasiri/frac-ssm",
    ),
    _paper(
        "post-training", "rfpo",
        "Unlocking the Critic: Reward-Free Policy Optimization for LLM Post-Training",
        "2609.37119", "rfpo", ["RL", "冻结 Critic", "无标签奖励"],
        "Hongyang Li", "University of Luxembourg", published="2026-09-29",
    ),
    _paper(
        "post-training", "olive", "Learning from Teacher Continuations at Student States",
        "2609.36246", "olive", ["在线蒸馏", "Teacher continuation"],
        "Haojin Wang", "University of Illinois Urbana-Champaign",
        "https://dylanzsz.github.io/olive/",
    ),
    _paper(
        "post-training", "ross",
        "ROSS: Relearning from Self-Generated Rollouts through Selective Supervision",
        "2609.35954", "ross", ["离线 SFT", "选择性监督"],
        "AllSpark Team", "AllSpark Team（原文以团队署名，未列机构）",
    ),
    _paper(
        "post-training", "r2-opd", "Reward-Aligned Reweighting for On-Policy Distillation",
        "2609.35517", "r2-opd", ["On-policy distillation", "奖励对齐重加权"],
        "Haofeng Xu", "The University of Hong Kong",
    ),
    _paper(
        "post-training", "mas-opd", "MAS-OPD: On-Policy Distillation for Multi-Agent Systems",
        "2609.34234", "mas-opd", ["多 Agent", "On-policy distillation"],
        "Qiyong Zhong", "University of Science and Technology of China",
    ),
    _paper(
        "agent-research", "dr-credit",
        "Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents",
        "2609.34296", "dr-credit", ["Agent RL", "过程信用分配"],
        "Yingjian Zhu", "University of Chinese Academy of Sciences",
    ),
    _paper(
        "agent-research", "ccm", "Continuous Context Management",
        "2609.35540", "ccm", ["上下文管理", "Agent RL"],
        "William Hoy", "University of Miami",
    ),
    _paper(
        "agent-research", "sage-planner",
        "SAGE: Symbolic Action-Gating and Editing for LLM Task Planners",
        "2609.34268", "sage", ["规划", "安全门", "局部恢复"],
        "Trung Minh Bui", "原文首页未列机构", "https://github.com/mtbui2010/sage",
    ),
    _paper(
        "agent-research", "certified-selective-eval",
        "Certified Selective Automation of LLM Agent Evaluation",
        "2609.34320", "certified-selective-eval",
        ["Agent 评测", "选择性自动化", "统计证书"],
        "Chengguang Gan", "Independent Researcher",
    ),
    _paper(
        "agent-research", "mnemon", "Mnemon: Raw Records, Fast Judgments, Slow Thoughts",
        "2609.36059", "mnemon", ["长期记忆", "Jev", "System 1/2"],
        "Guangren Wang", "原文未列机构",
    ),
)
