from pathlib import Path

from ..industrial_2026 import load_industrial_data
from .model import build_incrementality_problem, evaluate_policy


def reproduce_incrementality(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    problem = build_incrementality_problem(data, seed)
    baseline = evaluate_policy(problem, "predictive_score")
    method = evaluate_policy(problem, "incremental_score")
    gain = 100 * (method["policy_value"] - baseline["policy_value"]) / max(
        abs(baseline["policy_value"]), 1e-12
    )
    return {
        "paper": {
            "arxiv_id": "2608.10182",
            "title": "From Prediction to Incrementality: Causal Optimization for Large-Scale Targeting and Recommendation",
            "url": "https://arxiv.org/abs/2608.10182",
            "organization": "LinkedIn",
        },
        "dataset": {
            "name": "MovieLens 100K causal targeting simulation",
            "users": len(data.sequences.train),
            "items": data.item_count,
        },
        "setup": {"adapter": "incrementality", "same_budget_and_population": True},
        "baseline": {"name": "predictive targeting by estimated treated outcome", **baseline},
        "method": {"name": "uplift + uncertainty with global budget", **method},
        "relative": {"policy_value_percent": gain},
        "stages": {
            "examples": len(problem["true_uplift"]),
            "allocated_users": problem["budget"],
            "mean_propensity": float(problem["propensity"].mean()),
            "treatment_rate": float(problem["treatment"].mean()),
            "uplift_rmse": float(
                ((problem["estimated_uplift"] - problem["true_uplift"]) ** 2).mean() ** 0.5
            ),
        },
        "paper_results": {
            "linkedin_long_term_value_lift_percent": 7.20,
            "p_value": 0.041,
        },
        "scope": (
            "实际执行有混杂的 treatment 日志构造、双 outcome 回归、个体 uplift、"
            "不确定性探索分数和固定预算全局分配；未复刻 LinkedIn Transformer/DragonNet、"
            "在线神经 bandit 服务和大规模 LP 基础设施。"
        ),
    }
