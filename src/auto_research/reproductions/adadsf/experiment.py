from __future__ import annotations

from pathlib import Path

from auto_research.evolution.llm_data import load_llm_evolution_data
from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm

from ..llm_training import (
    evaluate_language_model,
    require_torch,
    sample_batch,
    train_language_model,
)
from .model import (
    allocate_retentions,
    calibration_similarities,
    routing_statistics,
    sparsify,
    train_alignment,
)


def reproduce_adadsf(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir,
        True,
        vocab_size=1024,
        maximum_train_tokens=260_000,
        maximum_eval_tokens=32_000,
    )
    config = MicroLMConfig(
        vocab_size=data.vocab_size,
        dimensions=96,
        layers=4,
        heads=4,
        sequence_length=96,
    )
    torch.manual_seed(seed)
    dense = build_micro_lm("llama_modern", config)
    pretrain = train_language_model(
        dense,
        data.train,
        steps=70,
        batch_size=8,
        length=config.sequence_length,
        learning_rate=6e-4,
        seed=seed,
        torch=torch,
    )
    calibration, _ = sample_batch(
        data.validation,
        batch_size=8,
        length=config.sequence_length,
        rng=__import__("numpy").random.default_rng(seed),
        device=next(dense.parameters()).device,
        torch=torch,
    )
    similarities = calibration_similarities(dense, calibration)
    adaptive_ratios = allocate_retentions(similarities, target=0.8)
    variants = {"Dense teacher": {**pretrain}}
    dense_eval = evaluate_language_model(
        dense, data.test, length=config.sequence_length, batches=32, torch=torch
    )
    variants["Dense teacher"].update(dense_eval)
    for name, ratios in (
        ("Uniform MoD 80%", [0.8] * config.layers),
        ("AdaDSF 80%", adaptive_ratios),
    ):
        student = sparsify(dense, ratios)
        alignment = train_alignment(
            student,
            dense,
            data.train,
            steps=35,
            batch_size=8,
            length=config.sequence_length,
            learning_rate=3e-4,
            seed=seed,
            torch=torch,
        )
        evaluation = evaluate_language_model(
            student,
            data.test,
            length=config.sequence_length,
            batches=32,
            torch=torch,
        )
        # Force one measured pass so statistics reflect integer Top-K execution.
        student(calibration)
        variants[name] = {
            **alignment,
            **evaluation,
            **routing_statistics(student),
            "parameters": sum(parameter.numel() for parameter in student.parameters()),
        }
    dense_ppl = variants["Dense teacher"]["perplexity"]
    uniform_ppl = variants["Uniform MoD 80%"]["perplexity"]
    adaptive_ppl = variants["AdaDSF 80%"]["perplexity"]
    return {
        "paper": {
            "arxiv_id": "2607.21291",
            "title": "Adaptive Depth Sparse Framework",
            "url": "https://arxiv.org/abs/2607.21291",
            "track": "llm",
        },
        "dataset": {
            "name": "WikiText-2",
            "train_tokens": len(data.train),
            "test_tokens": len(data.test),
        },
        "setup": {
            "seed": seed,
            "dense_steps": 70,
            "alignment_steps": 35,
            "target_retention": 0.8,
            "temperature": 0.05,
            "same_teacher_initialization_and_alignment_budget": True,
        },
        "calibration": {
            "layer_cosine_similarities": similarities,
            "adaptive_retentions": adaptive_ratios,
        },
        "variants": variants,
        "relative": {
            "adaptive_vs_uniform_ppl_reduction_percent": 100
            * (uniform_ppl - adaptive_ppl)
            / uniform_ppl,
            "adaptive_vs_dense_ppl_change_percent": 100
            * (adaptive_ppl - dense_ppl)
            / dense_ppl,
        },
        "paper_results": {
            "gpt_neox_dense_ppl": 17.9,
            "gpt_neox_mod_80_ppl": 21.6,
            "gpt_neox_adadsf_80_ppl": 18.9,
            "adadsf_normalized_flops": 0.787,
        },
        "scope": (
            "真实执行论文的 dense-layer cosine calibration、式(5–8)逐层预算分配、"
            "MLP Top-K token router 和中间层/输出分布对齐；每个 sparse block 只对被选中的 "
            "K 个 token 运行。模型与训练预算缩小到 Mac 可运行规模，不等同于论文的 "
            "GPT-NeoX/Qwen2.5 硬件 FLOP 结论。"
        ),
    }
