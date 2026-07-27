from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np

from auto_research.runtime import device_for

from ..llm_training import require_torch, seed_everything
from .data import load_data
from .model import build_model, fit_calibration, train_model


def reproduce_pinequalizer(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_data(dataset_dir)
    steps = int(os.environ.get("AUTO_RESEARCH_PINEQUALIZER_STEPS", "100"))
    seeds = (seed, seed + 1, seed + 2)
    runs = {"baseline": [], "pinequalizer": []}
    training = {"baseline": [], "pinequalizer": []}
    selections = []
    for run_seed in seeds:
        seed_everything(run_seed, torch)
        baseline = build_model(data, debiased=False).to(device_for(torch))
        training["baseline"].append(
            train_model(baseline, data, steps=steps, seed=run_seed, torch=torch)
        )
        baseline_calibration = fit_calibration(
            baseline, data, grouped=False, seed=run_seed, torch=torch
        )
        runs["baseline"].append(
            evaluate(baseline, data, "test", baseline_calibration, 0.0, torch)
        )

        seed_everything(run_seed, torch)
        proposed = build_model(data, debiased=True).to(device_for(torch))
        training["pinequalizer"].append(
            train_model(proposed, data, steps=steps, seed=run_seed, torch=torch)
        )
        proposed_calibration = fit_calibration(
            proposed, data, grouped=True, seed=run_seed, torch=torch
        )
        candidates = (0.0, 0.02, 0.05, 0.1, 0.2)
        validation = {
            alpha: evaluate(
                proposed, data, "validation", proposed_calibration, alpha, torch
            )
            for alpha in candidates
        }
        alpha = max(
            candidates,
            key=lambda value: (
                validation[value]["ndcg_at_10"]
                + 0.5 * validation[value]["fresh_ndcg_at_10"],
                -value,
            ),
        )
        selections.append({"seed": run_seed, "ucb_alpha": alpha, "validation": validation[alpha]})
        runs["pinequalizer"].append(
            evaluate(proposed, data, "test", proposed_calibration, alpha, torch)
        )
    aggregate = {
        name: {
            metric: float(np.mean([run[metric] for run in values]))
            for metric in values[0]
        }
        for name, values in runs.items()
    }
    baseline, proposed = aggregate["baseline"], aggregate["pinequalizer"]
    return {
        "paper": {
            "arxiv_id": "2607.22518",
            "title": "PinEqualizer",
            "url": "https://arxiv.org/abs/2607.22518",
            "organization": "Pinterest",
        },
        "dataset": {
            "name": "MovieLens-1M",
            "users": data.users,
            "items": data.items,
            "fresh_items": int(data.fresh.sum()),
            "underexplored_items": int(data.underexplored.sum()),
            "exploration_corpus_items": int(data.exploration_corpus.sum()),
        },
        "setup": {
            "seeds": list(seeds),
            "steps_per_model": steps,
            "fresh_definition": "top 20% item first-observation timestamps",
            "underexplored_definition": "fresh and below fresh-item median popularity",
            "selection": "validation NDCG@10 + 0.5 × fresh NDCG@10",
        },
        "training": training,
        "selection": selections,
        "runs": runs,
        "results": aggregate,
        "relative": {
            "ndcg_at_10_percent": _relative(proposed["ndcg_at_10"], baseline["ndcg_at_10"]),
            "fresh_ndcg_at_10_percent": _relative(
                proposed["fresh_ndcg_at_10"], baseline["fresh_ndcg_at_10"]
            ),
            "underexplored_exposure_percent": _relative(
                proposed["underexplored_exposure_at_10"],
                baseline["underexplored_exposure_at_10"],
            ),
        },
        "paper_results": {
            "fresh_impressions_increase_percent": 350,
            "related_ranking_all_fresh_engagement_percent": 8.63,
            "related_ranking_underexplored_engagement_percent": 6.57,
            "homefeed_underexplored_holdout_percent": 37,
            "search_underexplored_holdout_percent": 13,
            "related_underexplored_holdout_percent": 27,
        },
        "scope": (
            "在 MovieLens-1M 上用首见时间构造 fresh/old cohort，训练同预算 baseline 与"
            "带 individual engagement dropout、content×age/engagement crossing、fresh-aware "
            "score regularization 和分 cohort calibration 的模型；探索层真实构建 posterior "
            "exploration corpus，并用 relevance-scaled UCB 排序。电影首见时间只是 Pinterest "
            "内容冷启动的公开代理，不替代线上 holdout。"
        ),
    }


def evaluate(model, data, split, calibration, alpha, torch):
    targets = data.validation if split == "validation" else data.test
    device = next(model.parameters()).device
    hit = ndcg = fresh_hit = fresh_ndcg = 0.0
    fresh_count = 0
    recommendations = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, data.users, 128):
            stop = min(data.users, start + 128)
            users = torch.arange(start, stop, dtype=torch.long, device=device)
            scores = model.catalog_scores(users).cpu().numpy()
            if "all" in calibration:
                scores = (
                    calibration["all"]["scale"] * scores
                    + calibration["all"]["bias"]
                )
            else:
                for cohort, selected in (
                    ("fresh", data.fresh),
                    ("established", ~data.fresh),
                ):
                    scores[:, selected] = (
                        calibration[cohort]["scale"] * scores[:, selected]
                        + calibration[cohort]["bias"]
                    )
            if alpha:
                relevance = data.user_profiles[start:stop] @ data.genres.T
                uncertainty = np.sqrt(
                    np.log1p(data.popularity.sum()) / (data.popularity + 1)
                )
                bonus = (
                    np.clip(relevance, 0, 1) ** 0.5
                    * uncertainty[None]
                    * data.exploration_corpus[None]
                )
                scores += alpha * bonus
            for offset, user in enumerate(range(start, stop)):
                context = data.train[user] + (
                    (data.validation[user],) if split == "test" else ()
                )
                scores[offset, list(set(context))] = -np.inf
                top = np.argpartition(scores[offset], -10)[-10:]
                top = top[np.argsort(scores[offset, top])[::-1]]
                recommendations.extend(top.tolist())
                positions = np.flatnonzero(top == targets[user])
                target_fresh = bool(data.fresh[targets[user]])
                fresh_count += target_fresh
                if positions.size:
                    gain = 1 / math.log2(int(positions[0]) + 2)
                    hit += 1
                    ndcg += gain
                    if target_fresh:
                        fresh_hit += 1
                        fresh_ndcg += gain
    recommendations = np.asarray(recommendations)
    return {
        "hit_at_10": hit / data.users,
        "ndcg_at_10": ndcg / data.users,
        "fresh_hit_at_10": fresh_hit / max(fresh_count, 1),
        "fresh_ndcg_at_10": fresh_ndcg / max(fresh_count, 1),
        "fresh_exposure_at_10": float(data.fresh[recommendations].mean()),
        "underexplored_exposure_at_10": float(
            data.underexplored[recommendations].mean()
        ),
    }


def _relative(proposed, baseline):
    return 100 * (proposed - baseline) / max(abs(baseline), 1e-12)
