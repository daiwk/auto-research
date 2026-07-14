from __future__ import annotations

import os
from pathlib import Path

from ..industrial_batch import FAIR_DIN_STEPS, compact_movielens, evaluate_scores, run_din_baseline
from ..rec_utils import summarize_runs
from .model import scorer, subset, train_student, train_teacher


def reproduce_cross_domain_kd(dataset_dir: Path, seed: int = 42):
    data = compact_movielens(dataset_dir, maximum_users=240, maximum_items=260)
    split = int(0.75 * len(data.train))
    source = subset(data, range(split))
    target = subset(data, range(split, len(data.train)))
    steps = int(os.environ.get("AUTO_RESEARCH_KD_STEPS", "90"))
    kd_weight = float(os.environ.get("AUTO_RESEARCH_KD_WEIGHT", "0.35"))
    results = {"target_only": [], "zero_shot_kd": []}
    training = []
    for run_seed in (seed, seed + 1, seed + 2):
        teacher, teacher_metrics = train_teacher(source, run_seed, steps)
        baseline, baseline_metrics = train_student(target, run_seed, steps)
        distilled, distilled_metrics = train_student(target, run_seed, steps, teacher, kd_weight)
        results["target_only"].append(evaluate_scores(target, scorer(baseline, target)))
        results["zero_shot_kd"].append(evaluate_scores(target, scorer(distilled, target)))
        training.append({"teacher": teacher_metrics, "baseline": baseline_metrics, "distilled": distilled_metrics})
    aggregate = {name: summarize_runs(values) for name, values in results.items()}
    base, method = aggregate["target_only"], aggregate["zero_shot_kd"]
    seeds = (seed, seed + 1, seed + 2)
    aggregate["din"], din_training = run_din_baseline(target, seeds, FAIR_DIN_STEPS)
    return {
        "paper": {"arxiv_id": "2603.28994", "title": "Zero-shot Cross-domain Knowledge Distillation: A Case study on YouTube Music", "url": "https://arxiv.org/abs/2603.28994", "track": "recommendation"},
        "dataset": "MovieLens-100K source/low-traffic user domains",
        "setup": {"source_users": len(source.train), "target_users": len(target.train), "items": data.item_count, "steps": steps, "din_steps": FAIR_DIN_STEPS, "kd_weight": kd_weight, "seeds": list(seeds)},
        "training": training, "din_training": din_training,
        "results": aggregate,
        "ndcg_gain_percent": 100 * (method["ndcg_at_10"] / max(base["ndcg_at_10"], 1e-12) - 1),
        "ndcg_vs_din_percent": 100 * (method["ndcg_at_10"] / max(aggregate["din"]["ndcg_at_10"], 1e-12) - 1),
        "paper_online_ab": {"discovery_percent": 1.12, "new_releases_engagement_percent": 11.39},
        "scope": "Trains a larger multi-task source-domain teacher, applies it zero-shot to disjoint low-traffic target users, and distills full-catalog logits plus a non-serving content task into a small target ranker. Public MovieLens user domains replace YouTube/YouTube Music surfaces.",
    }
