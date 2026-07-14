from __future__ import annotations
import os
from pathlib import Path
from ..industrial_batch import compact_movielens, evaluate_scores
from ..rec_utils import summarize_runs
from .model import align_ipo, scorer, serendipity_at_10, train_sft


def reproduce_seral(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, 180, 280); steps = int(os.environ.get("AUTO_RESEARCH_SERAL_STEPS", "100"))
    results = {"sft": [], "seral_ipo": []}; novelty = {"sft": [], "seral_ipo": []}; training = []
    for run_seed in (seed, seed + 1, seed + 2):
        sft, st = train_sft(data, run_seed, steps); aligned, it = align_ipo(copy_model(sft), data, run_seed, steps // 2)
        for name, model in (("sft", sft), ("seral_ipo", aligned)):
            fn = scorer(model); results[name].append(evaluate_scores(data, fn)); novelty[name].append(serendipity_at_10(data, fn))
        training.append({"sft": st, "ipo": it})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}; novelty_mean = {name: float(sum(values) / len(values)) for name, values in novelty.items()}
    base, method = aggregate["sft"], aggregate["seral_ipo"]
    return {"paper": {"arxiv_id": "2502.13539", "title": "Bursting Filter Bubble: Enhancing Serendipity Recommendations with Aligned Large Language Models", "url": "https://arxiv.org/abs/2502.13539", "track": "recommendation"}, "dataset": "MovieLens-100K content and chronological feedback", "setup": {"users": len(data.train), "items": data.item_count, "steps": steps, "seeds": [seed, seed + 1, seed + 2]}, "training": training, "results": aggregate, "serendipity_at_10": novelty_mean, "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1), "paper_online_ab": {"serendipity_pvr_percent": 5.7, "serendipity_clicks_percent": 29.56, "transactions_percent": 27.6}, "scope": "Builds static/short/long cognition profiles, SFTs a generative catalog scorer, constructs CDI preference pairs from collaborative relevance and category novelty, applies the paper's IPO+SFT objective, and caches full-catalog nearline scores. MovieLens replaces Taobao and GPT-4 annotations."}


def copy_model(model):
    import copy
    return copy.deepcopy(model)

