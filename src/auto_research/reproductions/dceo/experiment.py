from pathlib import Path

from ..recent_20260728_common import full_catalog_metrics, load_recent_movielens, relative
from .model import causal_diagnostics, score_dceo, score_fixed


def reproduce_dceo(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_recent_movielens(dataset_dir, maximum_users=320, maximum_items=480)
    baseline = full_catalog_metrics(data, lambda history: score_fixed(data, history))
    # Evolve-style search is strictly validation-only.  The held-out test is
    # touched once after selecting the champion, avoiding the previous fixed
    # gain that improved Hit@10 while silently hurting NDCG@10.
    candidates = [
        (gain, temperature)
        for gain in (0.10, 0.20, 0.35, 0.50, 0.75)
        for temperature in (0.75, 1.0, 1.25, 1.5)
    ]
    validation_trials = []
    for gain, temperature in candidates:
        metrics = full_catalog_metrics(
            data,
            lambda history, gain=gain, temperature=temperature: score_dceo(
                data, history, causal_gain=gain, temperature=temperature,
            ),
            split="validation",
        )
        # NDCG is primary; Hit breaks ties; lower gain is the conservative
        # final tie-breaker and reduces head amplification.
        fitness = metrics["ndcg_at_10"] + 0.15 * metrics["hit_at_10"]
        validation_trials.append({
            "causal_gain": gain, "temperature": temperature,
            "fitness": fitness, **metrics,
        })
    selected = max(
        validation_trials,
        key=lambda row: (row["fitness"], row["hit_at_10"], -row["causal_gain"]),
    )
    method = full_catalog_metrics(
        data,
        lambda history: score_dceo(
            data, history, causal_gain=selected["causal_gain"],
            temperature=selected["temperature"],
        ),
    )
    return {
        "paper": {"arxiv_id": "2608.25635", "title": "DCEO"},
        "dataset": {"name": "MovieLens-1M", "users": len(data.train), "items": data.item_count},
        "setup": {
            "seed": seed, "full_catalog": True, "proxy_objectives": 4,
            "model_selection": "validation-only grid; held-out test evaluated once",
            "candidate_count": len(candidates),
        },
        "variants": {"fixed multi-objective fusion": baseline, "DCEO core": method},
        "relative": relative(method, baseline),
        "diagnostics": {
            **causal_diagnostics(data),
            "selected_causal_gain": selected["causal_gain"],
            "selected_temperature": selected["temperature"],
            "selected_validation_fitness": selected["fitness"],
            "validation_trials": validation_trials,
        },
        "paper_results": {"online_gmv_lift_percent": 0.36, "ab_test_days": 41},
        "scope": "在 MovieLens-1M 上执行上下文相关 simplex actor、用户级 proxy 聚合与相对干预诊断；线上只运行 actor。未复刻淘宝私有搜索日志、长期 GMV critic 或生产流量。",
    }
