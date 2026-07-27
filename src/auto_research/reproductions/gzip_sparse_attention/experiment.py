from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np

from auto_research.datasets import wikitext_2
from auto_research.runtime import device_for

from ..llm_training import require_torch, sample_batch, seed_everything
from .model import GzipLMConfig, build_attention_mask, build_model, compression_ratios


def reproduce_gzip_sparse_attention(dataset_dir: Path, seed: int = 42) -> dict:
    torch = require_torch()
    wiki = wikitext_2(dataset_dir)
    train = np.frombuffer(wiki["train"].encode("utf-8"), dtype=np.uint8).astype(np.int64)
    test = np.frombuffer(wiki["test"].encode("utf-8"), dtype=np.uint8).astype(np.int64)
    config = GzipLMConfig()
    steps = int(os.environ.get("AUTO_RESEARCH_GZIP_STEPS", "120"))
    results = {}
    for mode in ("dense", "bigbird", "gzip"):
        results[mode] = _train_and_evaluate(
            mode, train, test, config, steps, seed, torch
        )
    sample = torch.tensor(
        train[: config.sequence_length], dtype=torch.long
    )[None]
    gzip_mask = build_attention_mask(
        sample,
        mode="gzip",
        heads=config.heads,
        block_size=config.block_size,
    )
    dense_edges = config.heads * config.sequence_length * (
        config.sequence_length + 1
    ) / 2
    gzip_edges = int(gzip_mask.sum())
    baseline = results["bigbird"]["bits_per_byte"]
    proposed = results["gzip"]["bits_per_byte"]
    return {
        "paper": {
            "arxiv_id": "2607.21752",
            "title": "Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection",
            "url": "https://arxiv.org/abs/2607.21752",
            "track": "llm",
        },
        "dataset": {
            "name": "WikiText-2 raw UTF-8 bytes",
            "train_bytes": len(train),
            "test_bytes": len(test),
        },
        "setup": {
            "seed": seed,
            "steps_per_model": steps,
            "sequence_length": config.sequence_length,
            "block_size": config.block_size,
            "dimensions": config.dimensions,
            "layers": config.layers,
            "heads": config.heads,
        },
        "results": results,
        "mask": {
            "sample_block_compression_ratios": compression_ratios(
                sample, config.block_size
            )[0],
            "sample_gzip_allowed_edges": gzip_edges,
            "sample_dense_causal_edges": int(dense_edges),
            "sample_edge_reduction_percent": 100 * (dense_edges - gzip_edges) / dense_edges,
        },
        "relative": {
            "gzip_vs_bigbird_bpb_reduction_percent": 100
            * (baseline - proposed)
            / baseline,
            "gzip_vs_dense_bpb_reduction_percent": 100
            * (results["dense"]["bits_per_byte"] - proposed)
            / results["dense"]["bits_per_byte"],
        },
        "paper_results": {
            "pg19_gzip_bpb": 1.71,
            "pg19_dense_bpb": 2.89,
            "pg19_bigbird_bpb": 2.34,
            "convergence_speedup": 3.3,
        },
        "scope": (
            "对原始 UTF-8 bytes 逐块执行 gzip level-1，按样本均值选 literal blocks，"
            "真实构造 50% local、25% literal-long-range、25% hybrid head masks，并与"
            "相同参数和训练预算的 dense/BigBird 对照。当前 PyTorch 实现用 dense masked "
            "matmul，不宣称 wall-clock 稀疏加速。"
        ),
    }


def _train_and_evaluate(mode, train, test, config, steps, seed, torch):
    seed_everything(seed, torch)
    device = device_for(torch)
    model = build_model(config, mode).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=6e-4, weight_decay=0.1)
    rng = np.random.default_rng(seed)
    losses = []
    model.train()
    for _ in range(steps):
        inputs, labels = sample_batch(
            train, 2, config.sequence_length, rng, device, torch
        )
        logits = model(inputs)
        loss = torch.nn.functional.cross_entropy(
            logits.reshape(-1, 256), labels.reshape(-1)
        )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    eval_losses = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, 12 * config.sequence_length, config.sequence_length):
            values = torch.tensor(
                test[start : start + config.sequence_length + 1],
                dtype=torch.long,
                device=device,
            )
            logits = model(values[:-1][None])
            eval_losses.append(float(
                torch.nn.functional.cross_entropy(logits[0], values[1:]).cpu()
            ))
    loss = float(np.mean(eval_losses))
    return {
        "initial_loss": float(np.mean(losses[:5])),
        "final_loss": float(np.mean(losses[-5:])),
        "validation_loss": loss,
        "bits_per_byte": loss / math.log(2),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }
