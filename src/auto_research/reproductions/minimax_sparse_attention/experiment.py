from __future__ import annotations

import math
import os
import random
import time
from pathlib import Path

import numpy as np

from ...datasets import wikitext_2
from ...runtime import device_for
from ..industrial_ranking import require_backend, summarize_training
from .model import build_tiny_lm


def _tokens(text, limit):
    return np.frombuffer(text.encode("utf-8", errors="ignore"), dtype=np.uint8).astype(np.int64)[:limit] % 128


def _train(model, train, validation, seed, steps, length=96):
    torch, _ = require_backend()
    random.seed(seed); np.random.seed(seed); torch.manual_seed(seed)
    device = device_for(torch)
    model = model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4)
    rng, losses = random.Random(seed), []
    started = time.perf_counter()
    model.train()
    for _ in range(steps):
        starts = [rng.randrange(0, len(train) - length - 1) for _ in range(4)]
        batch = torch.tensor(np.stack([train[s:s + length + 1] for s in starts]), dtype=torch.long, device=device)
        logits = model(batch[:, :-1])
        loss = torch.nn.functional.cross_entropy(logits.reshape(-1, 128), batch[:, 1:].reshape(-1))
        if model.attention.index_loss is not None:
            loss = loss + 0.05 * model.attention.index_loss
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    duration = time.perf_counter() - started
    model.eval()
    values = []
    with torch.inference_mode():
        for start in range(0, min(len(validation) - length - 1, 4096), length):
            batch = torch.tensor(validation[start:start + length + 1][None], dtype=torch.long, device=device)
            logits = model(batch[:, :-1])
            values.append(float(torch.nn.functional.cross_entropy(logits.reshape(-1, 128), batch[:, 1:].reshape(-1)).cpu()))
    return model, {
        **summarize_training(model, losses, device.type),
        "validation_loss": float(np.mean(values)),
        "perplexity": math.exp(min(float(np.mean(values)), 20)),
        "seconds": duration,
        "attention_pair_ratio": model.attention.last_pair_ratio,
    }


def reproduce_minimax_sparse_attention(dataset_dir: Path, seed: int = 42):
    wiki = wikitext_2(dataset_dir, allow_network=True)
    train = _tokens(wiki["train"], 120_000)
    validation = _tokens(wiki["validation"], 12_000)
    steps = int(os.environ.get("AUTO_RESEARCH_MSA_STEPS", "36"))
    results = {}
    for name, sparse in (("dense_gqa", False), ("minimax_sparse_attention", True)):
        torch, _ = require_backend()
        torch.manual_seed(seed)
        model = build_tiny_lm(sparse=sparse)
        _, results[name] = _train(model, train, validation, seed, steps)
    return {
        "paper": {"arxiv_id": "2606.13392", "title": "MiniMax Sparse Attention", "url": "https://arxiv.org/abs/2606.13392", "organization": "MiniMax"},
        "dataset": {"name": "WikiText-2", "train_tokens": len(train), "validation_tokens": len(validation)},
        "setup": {"seed": seed, "steps": steps, "sequence_length": 96, "same_initialization_and_budget": True},
        "baseline": {"name": "dense GQA", **results["dense_gqa"]},
        "method": {"name": "blockwise MSA", **results["minimax_sparse_attention"]},
        "paper_results": {"attention_compute_reduction_at_1m_x": 28.4, "h800_prefill_speedup_x": 14.2, "h800_decode_speedup_x": 7.6},
        "scope": "真实训练共享 KV 的 GQA 与轻量 index branch；index 每个 GQA 组选择 top-k 历史块，主分支只在命中块上执行精确 causal attention。WikiText-2 上的小模型用于机制与公平消融，不等同于论文 109B 模型或官方 fused CUDA kernel。",
    }
