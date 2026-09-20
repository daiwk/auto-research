"""System One / Jev adjacent papers with explicit evidence boundaries."""

LATEST_METHOD_PAPERS = (
    {
        "domain": "foundation-models", "key": "gliclass",
        "title": "GLiClass: Generalist Lightweight Model for Sequence Classification Tasks",
        "paper_url": "https://arxiv.org/abs/2508.07662",
        "detail_path": "foundation-models/2508.07662-gliclass/README.md",
        "topic": ["动态候选分类", "System One 相邻方法"],
        "first_author": "Ihor Stepanov", "first_author_affiliation": "Knowledgator",
        "published": "2025-08-11", "code": "https://github.com/Knowledgator/GLiClass",
        "adapter": "system-one:bilinear-ce", "priority": "P1",
    },
    {
        "domain": "post-training", "key": "rlcr",
        "title": "Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty",
        "paper_url": "https://arxiv.org/abs/2507.16806",
        "detail_path": "post-training/2507.16806-rlcr/README.md",
        "topic": ["校准奖励", "Proper scoring rule"],
        "first_author": "Mehul Damani",
        "first_author_affiliation": "Massachusetts Institute of Technology",
        "published": "2025-07-22", "code": "https://github.com/damanimehul/RLCR",
        "adapter": "system-one:rival-brier", "priority": "P1",
    },
    {
        "domain": "post-training", "key": "calibration-aware-rl",
        "title": "Balancing Classification and Calibration Performance in Decision-Making LLMs via Calibration Aware Reinforcement Learning",
        "paper_url": "https://arxiv.org/abs/2601.13284",
        "detail_path": "post-training/2601.13284-calibration-aware-rl/README.md",
        "topic": ["校准强化学习", "决策 token"],
        "first_author": "Duygu Nur Yaldiz",
        "first_author_affiliation": "University of Southern California",
        "published": "2026-01-19", "code": None,
        "adapter": "system-one:rival-hybrid", "priority": "P1",
    },
)
