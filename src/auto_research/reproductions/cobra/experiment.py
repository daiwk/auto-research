from __future__ import annotations

import os
from pathlib import Path

from ..industrial_batch import FAIR_DIN_STEPS, compact_movielens, evaluate_scores, run_din_baseline
from ..rec_utils import summarize_runs
from .model import scorer, semantic_codes, train


def reproduce_cobra(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, 180, 280)
    steps = int(os.environ.get("AUTO_RESEARCH_COBRA_STEPS", "100"))
    codes = semantic_codes(data, seed)
    results = {"sparse_only": [], "cobra_cascade": []}
    training = []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, bt = train(data, codes, run_seed, steps, False)
        method, mt = train(data, codes, run_seed, steps, True)
        results["sparse_only"].append(evaluate_scores(data, scorer(baseline)))
        results["cobra_cascade"].append(evaluate_scores(data, scorer(method)))
        training.append({"baseline": bt, "method": mt})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}
    base, method = aggregate["sparse_only"], aggregate["cobra_cascade"]
    seeds = (seed, seed + 1, seed + 2)
    aggregate["din"], din_training = run_din_baseline(data, seeds, FAIR_DIN_STEPS)
    return {"paper": {"arxiv_id": "2503.02453", "title": "Sparse Meets Dense: Unified Generative Recommendations with Cascaded Sparse-Dense Representations", "url": "https://arxiv.org/abs/2503.02453", "track": "recommendation"}, "dataset": "MovieLens-100K content and chronological feedback", "setup": {"users": len(data.train), "items": data.item_count, "steps": steps, "din_steps": FAIR_DIN_STEPS, "codebooks": 2, "codebook_size": 8, "seeds": list(seeds)}, "training": training, "din_training": din_training, "results": aggregate, "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1), "ndcg_vs_din_percent": 100 * (method["ndcg_at_10"] / max(aggregate["din"]["ndcg_at_10"], 1e-12) - 1), "paper_online_ab": {"conversion_percent": 3.60, "arpu_percent": 4.15}, "scope": "Jointly trains sparse semantic-ID generation and a dense item vector conditioned on generated sparse codes; inference fuses sparse beam scores with per-code dense scores. MovieLens replaces Baidu ad logs and the production ANN/BeamFusion service."}
