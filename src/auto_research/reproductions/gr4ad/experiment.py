from __future__ import annotations

import os
from pathlib import Path

from ..industrial_batch import FAIR_DIN_STEPS, compact_movielens, evaluate_scores, run_din_baseline
from ..rec_utils import summarize_runs
from .model import scorer, train_dlrm, train_gr4ad, ua_sid


def reproduce_gr4ad(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, 180, 280)
    steps = int(os.environ.get("AUTO_RESEARCH_GR4AD_STEPS", "110"))
    codes = ua_sid(data, seed)
    results = {"dlrm": [], "gr4ad": []}
    training = []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, bt = train_dlrm(data, run_seed, steps)
        method, mt = train_gr4ad(data, codes, run_seed, steps)
        results["dlrm"].append(evaluate_scores(data, scorer(baseline)))
        results["gr4ad"].append(evaluate_scores(data, scorer(method)))
        training.append({"dlrm": bt, "gr4ad": mt})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}
    base, method = aggregate["dlrm"], aggregate["gr4ad"]
    seeds = (seed, seed + 1, seed + 2)
    aggregate["din"], din_training = run_din_baseline(data, seeds, FAIR_DIN_STEPS)
    return {"paper": {"arxiv_id": "2602.22732", "title": "Generative Recommendation for Large-Scale Advertising", "url": "https://arxiv.org/abs/2602.22732", "track": "recommendation"}, "dataset": "MovieLens-100K content, value proxy, and feedback", "setup": {"users": len(data.train), "items": data.item_count, "steps": steps, "din_steps": FAIR_DIN_STEPS, "seeds": list(seeds), "ua_sid_levels": [8, 8, 8, 16]}, "training": training, "din_training": din_training, "results": aggregate, "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1), "ndcg_vs_din_percent": 100 * (method["ndcg_at_10"] / max(aggregate["din"]["ndcg_at_10"], 1e-12) - 1), "paper_online_ab": {"ad_revenue_percent": 4.2, "users_million": 400}, "scope": "Builds content+value UA-SIDs with a collision hash, trains parallel LazyAR level heads with value-weighted supervised learning, then applies list-wise RSPO over sampled slates. MovieLens popularity replaces eCPM, and dynamic beam serving is represented only by the parallel fixed-budget decoder."}
