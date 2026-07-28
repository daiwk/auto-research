from __future__ import annotations

import os
from pathlib import Path

from auto_research.evolution.llm import MicroLLMEvaluator
from auto_research.evolution.models import Genome


PAPERS = {
    "native-sparse-attention": {
        "arxiv_id": "2502.11089",
        "title": "Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention",
        "url": "https://arxiv.org/abs/2502.11089",
        "organization": "DeepSeek",
    },
    "gated-attention": {
        "arxiv_id": "2505.06708",
        "title": "Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free",
        "url": "https://arxiv.org/abs/2505.06708",
        "organization": "Qwen / Alibaba",
    },
    "muon": {
        "arxiv_id": "2502.16982",
        "title": "Muon is Scalable for LLM Training",
        "url": "https://arxiv.org/abs/2502.16982",
        "organization": "Moonshot AI / UCLA",
    },
    "engram": {
        "arxiv_id": "2601.07372",
        "title": "Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models",
        "url": "https://arxiv.org/abs/2601.07372",
        "organization": "DeepSeek",
    },
    "looped-latent-attention": {
        "arxiv_id": "2607.15456",
        "title": "Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers",
        "url": "https://arxiv.org/abs/2607.15456",
        "organization": "University of Maryland / Meta AI",
    },
    "gaugequant": {
        "arxiv_id": "2607.20757",
        "title": "GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries",
        "url": "https://arxiv.org/abs/2607.20757",
        "organization": "University of Cambridge",
    },
    "switch-transformer": {
        "arxiv_id": "2101.03961",
        "title": "Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity",
        "url": "https://arxiv.org/abs/2101.03961",
        "organization": "Google Brain",
    },
    "mamba": {
        "arxiv_id": "2312.00752",
        "title": "Mamba: Linear-Time Sequence Modeling with Selective State Spaces",
        "url": "https://arxiv.org/abs/2312.00752",
        "organization": "Carnegie Mellon University / Princeton University",
    },
    "switch-attention": {
        "arxiv_id": "2603.26380",
        "title": "Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers",
        "url": "https://arxiv.org/abs/2603.26380",
        "organization": "Peking University / Huawei Technologies",
    },
}


def run_llm_evolve_reproduction(
    dataset_dir: Path,
    seed: int,
    *,
    key: str,
    architecture: str,
    paper_results: dict,
    scope: str,
    optimizer: str = "adamw",
):
    steps = int(
        os.environ.get(
            "AUTO_RESEARCH_LLM_P0_STEPS",
            os.environ.get("AUTO_RESEARCH_LLM_P1_STEPS", "30"),
        )
    )
    evaluator = MicroLLMEvaluator(
        dataset_dir=dataset_dir,
        dataset="wikitext-2",
        steps=steps,
        seeds=(seed,),
        allow_network=True,
        maximum_train_tokens=120_000,
        maximum_eval_tokens=8_000,
        vocab_size=512,
        benchmark_suite="core",
    )
    base = Genome(
        architecture="llama_modern", dimensions=64, layers=2,
        heads=4, kv_heads=2, sequence_length=64, expansion=3,
        batch_size=4, learning_rate=6e-4,
    )
    method = Genome(**{**base.to_dict(), "architecture": architecture})
    method = Genome(
        **{
            **method.to_dict(),
            "optimizer": optimizer,
        }
    )
    baseline_trial = evaluator.evaluate(
        "baseline", 0, None, base, (), "same-budget LLaMA baseline"
    )
    method_trial = evaluator.evaluate(
        "method", 1, "baseline", method, (PAPERS[key]["arxiv_id"],),
        f"paper mechanism: {architecture}",
    )
    baseline = baseline_trial.validation
    proposed = method_trial.validation
    return {
        "paper": PAPERS[key],
        "dataset": {"name": "WikiText-2", **evaluator.summary()},
        "setup": {
            "seed": seed,
            "steps_per_variant": steps,
            "dimensions": 64,
            "layers": 2,
            "sequence_length": 64,
            "same_tokens_optimizer_and_budget": True,
            "evolve_architecture": architecture,
            "evolve_optimizer": optimizer,
        },
        "baseline": {
            "name": "llama_modern",
            **baseline,
            **baseline_trial.training,
        },
        "method": {
            "name": architecture,
            **proposed,
            **method_trial.training,
        },
        "relative": {
            "lm_loss_percent": 100.0 * (
                proposed["lm_loss"] - baseline["lm_loss"]
            ) / baseline["lm_loss"],
            "perplexity_percent": 100.0 * (
                proposed["perplexity"] - baseline["perplexity"]
            ) / baseline["perplexity"],
        },
        "paper_results": paper_results,
        "scope": scope,
    }


def render(result):
    base, method = result["baseline"], result["method"]
    return "\n".join([
        f"# {result['paper']['title']}",
        "",
        f"公开数据：WikiText-2；每组 {result['setup']['steps_per_variant']} steps。",
        "",
        "| Variant | LM loss | Perplexity | Parameters |",
        "|---|---:|---:|---:|",
        f"| {base['name']} | {base['lm_loss']:.4f} | {base['perplexity']:.2f} | {base['parameters']} |",
        f"| {method['name']} | {method['lm_loss']:.4f} | {method['perplexity']:.2f} | {method['parameters']} |",
        "",
        (
            "相对同预算 LLaMA baseline："
            f"LM loss {result['relative']['lm_loss_percent']:+.2f}%，"
            f"perplexity {result['relative']['perplexity_percent']:+.2f}%。"
        ),
        "",
        "## evolve 接入",
        "",
        (
            f"`--model micro-llm` 已可搜索结构 "
            f"`{result['setup']['evolve_architecture']}` 与优化器 "
            f"`{result['setup']['evolve_optimizer']}`。"
        ),
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ])
