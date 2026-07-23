import os
from pathlib import Path

from .data import load_gsm8k
from .model import run_comparison


def reproduce_off_context_grpo(dataset_dir: Path, seed: int = 42) -> dict:
    train, test = load_gsm8k(dataset_dir, seed=seed)
    steps = int(os.environ.get("AUTO_RESEARCH_OC_GRPO_STEPS", "2400"))
    baseline, method, baseline_training, method_training = run_comparison(train, test, steps, seed)
    return {
        "paper": {
            "arxiv_id": "2607.19313",
            "title": "Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information",
            "url": "https://arxiv.org/abs/2607.19313",
            "organization": "Meta AI / Columbia University",
        },
        "dataset": {"name": "GSM8K official", "train_examples": len(train), "test_examples": len(test)},
        "setup": {"seed": seed, "steps_per_variant": steps, "candidate_rollouts": 8, "verifiable_exact_answer_reward": True},
        "baseline": {"name": "vanilla GRPO", **baseline},
        "method": {"name": "Off-Context GRPO with importance correction", **method},
        "relative": {
            "pass_at_1_percent": 100 * (method["pass_at_1"] - baseline["pass_at_1"]) / max(baseline["pass_at_1"], 1e-12),
            "gold_margin_delta": method["gold_margin"] - baseline["gold_margin"],
        },
        "training": {"grpo": baseline_training, "off_context_grpo": method_training},
        "stages": {
            "privileged_solution_prefix_rollouts": True,
            "original_unguided_target_objective": True,
            "importance_ratio_correction": True,
            "group_relative_advantage": True,
            "verifiable_reward": True,
        },
        "paper_results": {
            "qwen_2_5_7b_absolute_gain_points": 3.9,
            "qwen_2_5_7b_relative_gain_percent": 13.8,
            "qwen_2_5_3b_relative_gain_percent": 7.2,
            "qwen_2_5_1_5b_relative_gain_percent": 10.2,
        },
        "scope": "实际在官方 GSM8K 上执行 group-relative verifiable reward：vanilla GRPO 从原 prompt rollout；OC-GRPO 从含解题过程的 privileged prompt 采样，再以原 prompt policy/behavior policy importance ratio 修正到无提示目标。紧凑可解释的数学候选策略替代 Qwen2.5 1.5B–7B token rollout，以便 Mac CPU 可完成；GPU 完整模型入口在复现说明中给出。",
    }
