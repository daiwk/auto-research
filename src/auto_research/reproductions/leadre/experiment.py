from __future__ import annotations
import copy
import os
from pathlib import Path
from ..industrial_batch import compact_movielens, evaluate_scores
from ..rec_utils import summarize_runs
from .model import ad_semantic_ids, align_dpo, scorer, train_sft


def reproduce_leadre(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, 180, 280); steps = int(os.environ.get("AUTO_RESEARCH_LEADRE_STEPS", "100")); dpo_steps = int(os.environ.get("AUTO_RESEARCH_LEADRE_DPO_STEPS", str(steps // 2))); beta = float(os.environ.get("AUTO_RESEARCH_LEADRE_BETA", "0.2")); codes = ad_semantic_ids(data, seed)
    results = {"sft": [], "leadre_dpo": []}; training = []
    for run_seed in (seed, seed + 1, seed + 2):
        sft, st = train_sft(data, codes, run_seed, steps); method, dt = align_dpo(copy.deepcopy(sft), data, run_seed, dpo_steps, beta)
        results["sft"].append(evaluate_scores(data, scorer(sft))); results["leadre_dpo"].append(evaluate_scores(data, scorer(method))); training.append({"sft": st, "dpo": dt})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}; base, method = aggregate["sft"], aggregate["leadre_dpo"]
    return {"paper": {"arxiv_id": "2411.13789", "title": "LEADRE: Multi-Faceted Knowledge Enhanced LLM Empowered Display Advertisement Recommender System", "url": "https://arxiv.org/abs/2411.13789", "track": "recommendation"}, "dataset": "MovieLens-100K content, business-value proxy, and feedback", "setup": {"users": len(data.train), "items": data.item_count, "steps": steps, "dpo_steps": dpo_steps, "beta": beta, "seeds": [seed, seed + 1, seed + 2], "sid_levels": [8, 8, 16]}, "training": training, "results": aggregate, "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1), "paper_online_ab": {"channels_gmv_percent": 1.57, "moments_gmv_percent": 1.17}, "scope": "Generates ad Semantic IDs, builds long/short/business intent profiles, jointly trains SID generation with semantic and business auxiliary tasks, then applies DPO against the frozen SFT policy. Long profiles are cacheable while recent intent remains request-time; MovieLens replaces WeChat ads."}
