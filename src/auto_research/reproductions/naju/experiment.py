from __future__ import annotations

from pathlib import Path

from auto_research.evolution.llm_data import load_llm_evolution_data

from ..llm_training import evaluate_language_model, require_torch, train_language_model
from .model import build_variant


def reproduce_naju(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir, True, vocab_size=1024,
        maximum_train_tokens=260_000, maximum_eval_tokens=32_000,
    )
    variants = {}
    for name in ("Transformer", "Naju"):
        torch.manual_seed(seed)
        model, config = build_variant(name, data.vocab_size)
        training = train_language_model(
            model, data.train, steps=70, batch_size=6,
            length=config.sequence_length, learning_rate=7e-4,
            seed=seed, torch=torch,
        )
        metrics = evaluate_language_model(
            model, data.test, length=config.sequence_length,
            batches=32, torch=torch,
        )
        with torch.inference_mode():
            sample = torch.tensor(
                data.validation[: 2 * config.sequence_length].reshape(2, config.sequence_length),
                dtype=torch.long,
                device=next(model.parameters()).device,
            )
            model(sample)
        variants[name] = {
            **training,
            **metrics,
            "mixer": model.sequence_mixer_stats(),
        }
    baseline, method = variants["Transformer"], variants["Naju"]
    return {
        "paper": {
            "arxiv_id": "2607.21000",
            "title": "Naju",
            "url": "https://arxiv.org/abs/2607.21000",
            "track": "llm",
        },
        "dataset": {
            "name": "WikiText-2",
            "train_tokens": len(data.train),
            "test_tokens": len(data.test),
        },
        "setup": {
            "seed": seed,
            "steps": 70,
            "sequence_length": config.sequence_length,
            "same_tokens_optimizer_and_steps": True,
            "naju_state_size": max(8, config.dimensions // config.heads),
            "forget_bias": 5.0,
            "write_bias": -2.0,
        },
        "variants": variants,
        "relative": {
            "perplexity_reduction_percent": 100 * (
                baseline["perplexity"] - method["perplexity"]
            ) / baseline["perplexity"],
        },
        "paper_results": {
            "wikitext103_naju_perplexity": 26.20,
            "wikitext103_mamba2_perplexity": 28.31,
            "diagnostic_retention_accuracy": 0.99,
            "diagnostic_overwrite_accuracy": 0.89,
        },
        "scope": (
            "实际执行论文 native-discrete recurrence：独立 sigmoid retain/write gates、"
            "token-dependent B/C、短程 causal depthwise convolutions、状态 readout、feedthrough、"
            "SiLU output modulation 和 residual。当前 Python sequential scan 与论文递推等价，"
            "但未使用作者 fused associative scan，也未复跑 1.2B-token WikiText-103 和完整 Mamba 对照。"
        ),
    }
