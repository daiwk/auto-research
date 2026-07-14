from __future__ import annotations

import os
from pathlib import Path

from .model import SessionRecConfig, load_kuairand_sessions, train_and_evaluate


def reproduce_sessionrec(dataset_dir: Path, seed: int = 42):
    config = SessionRecConfig(
        rows=int(os.environ.get("AUTO_RESEARCH_SESSIONREC_ROWS", "350000")),
        users=int(os.environ.get("AUTO_RESEARCH_SESSIONREC_USERS", "2000")),
        steps=int(os.environ.get("AUTO_RESEARCH_SESSIONREC_STEPS", "180")),
        rank_weight=float(os.environ.get("AUTO_RESEARCH_SESSIONREC_RANK_WEIGHT", "0.01")),
    )
    data = load_kuairand_sessions(dataset_dir, config)
    if not data.train or not data.test:
        raise RuntimeError("SessionRec needs at least three positive KuaiRand sessions per retained user")
    baseline = train_and_evaluate(data, config, seed, False)
    method = train_and_evaluate(data, config, seed, True)
    return {
        "paper": {"arxiv_id": "2502.10157", "title": "SessionRec: Next Session Prediction Paradigm For Generative Sequential Recommendation", "url": "https://arxiv.org/abs/2502.10157", "track": "recommendation"},
        "dataset": "KuaiRand-Pure standard exposure log; 30-minute sessions; click or long-view positives",
        "setup": {"seed": seed, "source_rows": config.rows, "users": data.users, "items": data.item_count, "train": len(data.train), "validation": len(data.validation), "test": len(data.test), "steps": config.steps, "rank_weight": config.rank_weight},
        "results": {"item_transformer": baseline, "sessionrec_transformer": method},
        "paper_online_ab": {"pay_pv_percent": 0.603, "pvctcvr_percent": 0.564, "traffic": "Meituan homepage, 7 days"},
        "scope": "Executes item-within-session mean encoding, session-sequence Transformer, multi-positive next-session retrieval and within-session exposed hard-negative ranking. KuaiRand-Pure replaces Meituan/KuaiSAR/RecFlow; ANN serving is evaluated by exact full-catalog ranking.",
    }
