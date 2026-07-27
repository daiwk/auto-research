from pathlib import Path

from ..p0_2026_common import run_scoring_reproduction
from .model import train_pagewise_policy


def reproduce_genrec(dataset_dir: Path, seed: int = 42):
    return run_scoring_reproduction(
        key="genrec", paper={"arxiv_id": "2604.14878", "title": "GenRec: A Preference-Oriented Generative Framework for Large-Scale Recommendation", "url": "https://arxiv.org/abs/2604.14878", "organization": "JD.com"},
        dataset_dir=dataset_dir, build_method=train_pagewise_policy,
        baseline_name="point-wise transition/content ranker", method_name="page-wise NTP + Token Merger + GRPO-SR",
        paper_results={"online_clicks_percent": 9.5, "online_transactions_percent": 8.7},
        scope="真实把下一页三项作为联合训练单元，执行非对称上下文合并、组内序位 reward advantage 和带 NLL 先验的策略更新。公开电影页替代京东曝光页、LLM backbone 与在线策略系统。",
    )
