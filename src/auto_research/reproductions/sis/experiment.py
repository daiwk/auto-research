from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from ...datasets import tiny_shakespeare
from .algorithm import sis_topk_weight, weight_stats


def reproduce_sis(
    dataset_dir: Path,
    seed: int = 42,
    samples: int = 50_000,
    top_k: int = 10,
) -> dict[str, Any]:
    text = tiny_shakespeare(dataset_dir)
    vocab = sorted(set(text))
    token_id = {token: index for index, token in enumerate(vocab)}
    encoded = np.fromiter((token_id[token] for token in text), dtype=np.int64)
    split = int(len(encoded) * 0.45)
    later = int(len(encoded) * 0.8)
    behavior = _bigram_probabilities(encoded[:split], len(vocab), alpha=0.2)
    target = _bigram_probabilities(encoded[split:later], len(vocab), alpha=0.2)
    contexts = encoded[1:split]
    rng = np.random.default_rng(seed)
    raw_weights: list[float] = []
    sis_weights: list[float] = []
    accepted = 0
    for _ in range(samples):
        context = int(contexts[rng.integers(0, len(contexts))])
        token = int(rng.choice(len(vocab), p=behavior[context]))
        raw_weights.append(float(target[context, token] / behavior[context, token]))
        modified, was_accepted = sis_topk_weight(
            target[context], behavior[context], token, top_k, rng
        )
        sis_weights.append(modified)
        accepted += was_accepted
    baseline = weight_stats("token_is", raw_weights, 0.0, samples, top_k)
    method = weight_stats("sis", sis_weights, accepted / samples, samples, top_k)
    return {
        "paper": {
            "arxiv_id": "2607.04728",
            "title": "Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment",
            "url": "https://arxiv.org/abs/2607.04728",
            "track": "llm",
        },
        "dataset": "Tiny Shakespeare",
        "setup": {
            "behavior_policy": "character bigram fitted on first 45%",
            "target_policy": "character bigram fitted on subsequent 35%",
            "samples": samples,
            "seed": seed,
            "top_k": top_k,
        },
        "baseline": asdict(baseline),
        "method": asdict(method),
        "variance_reduction_percent": 100
        * (baseline.weight_variance - method.weight_variance)
        / baseline.weight_variance,
    }


def _bigram_probabilities(
    encoded: np.ndarray, vocab_size: int, alpha: float
) -> np.ndarray:
    counts = np.full((vocab_size, vocab_size), alpha, dtype=np.float64)
    np.add.at(counts, (encoded[:-1], encoded[1:]), 1.0)
    return counts / counts.sum(axis=1, keepdims=True)
