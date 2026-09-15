from __future__ import annotations

import copy
from pathlib import Path

import numpy as np

from auto_research.evolution.llm_data import load_llm_evolution_data

from ..llm_training import evaluate_language_model, require_torch, sample_batch, train_language_model
from .model import build_tiny_sas_lm, clone_as_sparse


def _train_selector(model, tokens, *, seed: int, steps: int, length: int, torch) -> dict:
    device = next(model.parameters()).device
    optimizer = torch.optim.AdamW(
        (parameter for parameter in model.parameters() if parameter.requires_grad), lr=2e-3
    )
    rng = np.random.default_rng(seed + 17)
    losses = []
    gradient_norms = []
    model.train()
    for _ in range(steps):
        inputs, labels = sample_batch(tokens, 8, length, rng, device, torch)
        logits = model(inputs)
        loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, logits.shape[-1]), labels.reshape(-1)
        )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        gradient_norms.append(float(torch.nn.utils.clip_grad_norm_(
            [*model.attention.selector_q.parameters(), *model.attention.selector_k.parameters()], 1.0
        ).detach().cpu()))
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:5])),
        "final_loss": float(np.mean(losses[-5:])),
        "selector_gradient_norm_mean": float(np.mean(gradient_norms)),
    }


def reproduce_sas_attention(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    data = load_llm_evolution_data(
        dataset_dir,
        False,
        vocab_size=256,
        maximum_train_tokens=12_000,
        maximum_eval_tokens=4_096,
    )
    length = 64
    torch.manual_seed(seed)
    dense = build_tiny_sas_lm(vocab_size=data.vocab_size, sequence_length=length)
    dense.attention.sparse = False
    pretraining = train_language_model(
        dense,
        data.train,
        steps=30,
        batch_size=8,
        length=length,
        learning_rate=8e-4,
        seed=seed,
        torch=torch,
    )
    dense_reference = copy.deepcopy(dense)
    sparse = clone_as_sparse(dense)
    selector_training = _train_selector(
        sparse, data.train, seed=seed, steps=24, length=length, torch=torch
    )
    dense_validation = evaluate_language_model(
        dense_reference, data.validation, length=length, batches=12, torch=torch
    )
    sparse_validation = evaluate_language_model(
        sparse, data.validation, length=length, batches=12, torch=torch
    )
    dense_test = evaluate_language_model(
        dense_reference, data.test, length=length, batches=12, torch=torch
    )
    sparse_test = evaluate_language_model(
        sparse, data.test, length=length, batches=12, torch=torch
    )
    diagnostics = dict(sparse.attention.last_diagnostics)
    return {
        "paper": {
            "arxiv_id": "2609.13141",
            "title": "SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking",
            "url": "https://arxiv.org/abs/2609.13141",
            "track": "llm",
        },
        "dataset": {
            "name": "WikiText-2",
            "train_tokens": len(data.train),
            "validation_tokens": len(data.validation),
            "test_tokens": len(data.test),
        },
        "setup": {
            "seed": seed,
            "backbone_pretraining_steps": 30,
            "selector_training_steps": 24,
            "sequence_length": length,
            "block_size": sparse.attention.block_size,
            "top_k_historical_blocks": sparse.attention.top_k_blocks,
            "frozen_backbone_during_selector_training": True,
            "test_isolation": "hyperparameters fixed before test evaluation",
        },
        "pretraining": pretraining,
        "selector_training": selector_training,
        "validation": {"dense": dense_validation, "sas": sparse_validation},
        "test": {"dense": dense_test, "sas": sparse_test},
        "routing": diagnostics,
        "relative": {
            "test_ppl_change_vs_dense_percent": 100.0
            * (sparse_test["perplexity"] - dense_test["perplexity"])
            / dense_test["perplexity"],
            "attention_positions_reduced_percent": 100.0
            * (1.0 - diagnostics["retained_attention_fraction"]),
        },
        "paper_results": {
            "math500_qwen3_4b_budget1024_sas": 90.65,
            "math500_qwen3_4b_budget1024_seer_attention_r": 84.67,
            "bfcl_qwen3_4b_budget2048_sas": 32.50,
            "bfcl_qwen3_4b_budget2048_seer_attention_r": 29.00,
            "decode_speedup_batch1_context512k": 5.6,
        },
        "manifest_ref": "reproduction:sas-attention",
        "scope": (
            "在 WikiText-2 上真实训练 tiny decoder，并冻结 dense backbone、只用语言模型损失训练 "
            "SAS selector；执行历史块 softmax 归一化、硬 Top-K、连续 gate 及 softmax 内 log-gate。"
            "PyTorch 参考实现仍物化稠密注意力矩阵，不复刻论文 Triton/FlashAttention kernel、"
            "Qwen3/OLMo3 规模训练或论文 benchmark，因此不能据此声称吞吐加速或论文精度复现。"
        ),
    }
