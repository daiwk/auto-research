import os
from pathlib import Path

from .data import load_alpaca_preferences
from .model import evaluate_policy, train_dynamic_rubric, train_static_policy


def reproduce_dynamic_rubric(dataset_dir: Path, seed: int = 42) -> dict:
    train, test = load_alpaca_preferences(dataset_dir, seed=seed)
    steps = int(os.environ.get("AUTO_RESEARCH_DYNAMIC_RUBRIC_STEPS", "1600"))
    baseline_policy, baseline_training = train_static_policy(train, steps=steps, seed=seed)
    policy, generator, method_training = train_dynamic_rubric(train, steps=steps, seed=seed)
    baseline = evaluate_policy(baseline_policy, test)
    method = evaluate_policy(policy, test)
    return {
        "paper": {
            "arxiv_id": "2607.20083",
            "title": "Co-Evolving LLM Evaluators and Policies via DynamicRubric",
            "url": "https://arxiv.org/abs/2607.20083",
            "organization": "WeChat / Tencent and Tsinghua University",
        },
        "dataset": {"name": "Stanford Alpaca", "train_preferences": len(train), "test_preferences": len(test)},
        "setup": {
            "seed": seed,
            "steps_per_variant": steps,
            "candidates_per_prompt": 3,
            "rubric_items": 4,
            "policy_induced_hard_negatives": True,
        },
        "baseline": {"name": "static prompt-only rubric policy", **baseline},
        "method": {"name": "DynamicRubric evaluator-policy co-evolution", **method},
        "relative": {
            "preference_accuracy_percent": 100 * (method["alpaca_preference_accuracy"] - baseline["alpaca_preference_accuracy"]) / max(baseline["alpaca_preference_accuracy"], 1e-12),
            "margin_delta": method["mean_good_vs_hard_negative_margin"] - baseline["mean_good_vs_hard_negative_margin"],
        },
        "training": {"static_rubric": baseline_training, "dynamic_rubric": method_training},
        "stages": {
            "response_set_conditioned_rubric_generator": True,
            "weighted_binary_rubrics": True,
            "discriminability_objective": True,
            "anchor_objective": True,
            "policy_evaluator_co_evolution": True,
            "generator_weight_norm": float((generator ** 2).sum() ** 0.5),
        },
        "paper_results": {
            "online_lifts_disclosed": False,
            "online_ab_significant_metrics": ["total search volume", "user duration", "absolute positive behaviors"],
            "fully_deployed": True,
            "traffic": "all WeChat Search AI-answering traffic; tens of millions of requests/day",
        },
        "scope": "实际执行 response-set-conditioned rubric 权重生成、binary rubric verifier、discriminability/anchor 双目标和多轮 evaluator-policy 共进化；公开 Alpaca instruction-response 与确定性受损候选构成可审计偏好集。紧凑文本策略替代 Qwen3-8B/生产回答模型，未复刻 70B/235B judges。",
    }
