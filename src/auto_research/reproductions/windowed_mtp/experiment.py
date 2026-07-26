from __future__ import annotations

from pathlib import Path

from auto_research.evolution.llm_data import load_llm_evolution_data
from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm

from ..llm_training import evaluate_language_model, require_torch, train_language_model
from .model import (
    benchmark_draft_attention,
    build_mtp_head,
    dense_greedy,
    speculative_greedy,
    train_mtp_head,
)


def reproduce_windowed_mtp(dataset_dir: Path, seed: int = 42) -> dict:
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
        layers=3,
        heads=4,
        sequence_length=128,
    )
    torch.manual_seed(seed)
    target = build_micro_lm("llama_modern", config)
    target_training = train_language_model(
        target,
        data.train,
        steps=240,
        batch_size=8,
        length=config.sequence_length,
        learning_rate=6e-4,
        seed=seed,
        torch=torch,
    )
    target_eval = evaluate_language_model(
        target, data.test, length=config.sequence_length, batches=24, torch=torch
    )
    draft = build_mtp_head(target).to(next(target.parameters()).device)
    draft_training = train_mtp_head(
        draft,
        data.train,
        steps=180,
        batch_size=16,
        context=96,
        learning_rate=8e-4,
        seed=seed,
        torch=torch,
    )
    prompt = torch.tensor(
        data.test[:96], dtype=torch.long, device=next(target.parameters()).device
    )[None]
    dense = dense_greedy(target, prompt, new_tokens=24, torch=torch)
    native = speculative_greedy(
        target,
        draft,
        prompt,
        new_tokens=24,
        gamma=4,
        window=None,
        sink=0,
        torch=torch,
    )
    windowed = speculative_greedy(
        target,
        draft,
        prompt,
        new_tokens=24,
        gamma=4,
        window=48,
        sink=8,
        torch=torch,
    )
    latency = benchmark_draft_attention(
        draft,
        contexts=(256, 1024, 4096, 16384),
        window=64,
        sink=8,
        repeats=10,
        seed=seed,
        torch=torch,
    )
    longest = {
        row["mode"]: row
        for row in latency
        if row["context"] == 16384
    }
    return {
        "paper": {
            "arxiv_id": "2607.21535",
            "title": "Windowed-MTP",
            "url": "https://arxiv.org/abs/2607.21535",
            "track": "llm",
        },
        "dataset": {
            "name": "WikiText-2",
            "train_tokens": len(data.train),
            "test_tokens": len(data.test),
        },
        "setup": {
            "seed": seed,
            "target_steps": 240,
            "draft_steps": 180,
            "speculative_gamma": 4,
            "speculative_window": 48,
            "attention_sink": 8,
        },
        "target": {**target_training, **target_eval},
        "draft": draft_training,
        "generation": {
            "dense_tokens": dense,
            "native": native,
            "windowed": windowed,
            "native_exact_match": native["tokens"] == dense,
            "windowed_exact_match": windowed["tokens"] == dense,
        },
        "latency": latency,
        "relative": {
            "context_16384_kv_read_reduction_percent": longest["windowed"][
                "kv_read_reduction_percent"
            ],
            "context_16384_latency_reduction_percent": 100
            * (
                longest["native"]["milliseconds"]
                - longest["windowed"]["milliseconds"]
            )
            / longest["native"]["milliseconds"],
        },
        "paper_results": {
            "qwen_35b_step_reduction_percent": 44.3,
            "qwen_122b_step_reduction_percent": 30.2,
            "nemotron_120b_step_reduction_percent": 28.3,
            "draft_kv_pool_fraction_percent": "7.7–11.1",
        },
        "scope": (
            "真实训练一个共享目标词嵌入的轻量 MTP draft head，并让 native draft 读取全历史、"
            "Windowed-MTP 只读取 sink+recent keys；两条 speculative greedy 路径均由完整 target "
            "逐 token 验证，输出与 dense greedy 完全一致。Mac 小模型 latency 只用于验证复杂度"
            "趋势，不替代论文 SGLang+B200 的百万 token kernel 结果。"
        ),
    }
