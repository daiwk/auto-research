from __future__ import annotations

from pathlib import Path

from auto_research.evolution.llm_data import load_llm_evolution_data

from ..llm_training import evaluate_language_model, require_torch
from .model import build_variant, evaluate_retrieval, train_mixed


def reproduce_mobius_rope(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir, True, vocab_size=1024,
        maximum_train_tokens=260_000, maximum_eval_tokens=32_000,
    )
    variants = {}
    for name in ("Standard RoPE", "Hybrid Möbius RoPE"):
        torch.manual_seed(seed)
        model, config = build_variant(name, data.vocab_size)
        training = train_mixed(model, data.train, config, seed, torch)
        language = evaluate_language_model(
            model, data.test, length=config.sequence_length, batches=32, torch=torch
        )
        retrieval = evaluate_retrieval(model, config, seed, torch)
        variants[name] = {**training, **language, **retrieval}
    baseline, method = variants["Standard RoPE"], variants["Hybrid Möbius RoPE"]
    return {
        "paper": {
            "arxiv_id": "2607.21405",
            "title": "Anti-Periodic Positional Encoding",
            "url": "https://arxiv.org/abs/2607.21405",
            "track": "llm",
        },
        "dataset": {
            "name": "WikiText-2 + synthetic single-needle retrieval",
            "train_tokens": len(data.train),
            "test_tokens": len(data.test),
        },
        "setup": {
            "seed": seed,
            "steps": 90,
            "context_length": config.sequence_length,
            "mobius_head_fraction": 0.25,
            "same_initialization_tokens_optimizer_and_steps": True,
        },
        "variants": variants,
        "relative": {
            "perplexity_reduction_percent": 100 * (
                baseline["perplexity"] - method["perplexity"]
            ) / baseline["perplexity"],
            "needle_accuracy_points": 100 * (
                method["needle_accuracy"] - baseline["needle_accuracy"]
            ),
            "far_needle_accuracy_points": 100 * (
                method["far_needle_accuracy"] - baseline["far_needle_accuracy"]
            ),
        },
        "paper_results": {
            "standard_perplexity": 29.72,
            "hybrid_perplexity": 29.66,
            "standard_needle_accuracy_percent": 63.3,
            "hybrid_needle_accuracy_percent": 90.3,
        },
        "scope": (
            "实际把 25% attention heads 的 RoPE 频率替换为固定训练上下文 N 下的 "
            "theta_i=pi(2i+1)/N，并以相同初始化、语料混合和训练预算对照 standard RoPE。"
            "本地 retrieval 是可审计的单针 key/value 任务；它用于验证几何机制，不等同于论文 "
            "160M/410M、2B-token、六随机种子统计结论。"
        ),
    }
