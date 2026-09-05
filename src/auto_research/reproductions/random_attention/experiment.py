from __future__ import annotations

from pathlib import Path
import time

import torch

from .model import random_retained_indices, recent_retained_indices


def _reconstruct(keys, values, retained):
    outputs = []
    for head in range(keys.shape[0]):
        index = retained[head]
        query = keys[head, -1]
        weight = torch.softmax(keys[head, index] @ query / keys.shape[-1] ** 0.5, dim=0)
        outputs.append(weight @ values[head, index])
    return torch.stack(outputs)


def reproduce_random_attention(dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    torch.manual_seed(seed)
    heads, length, dim, prompt, budget = 8, 512, 32, 64, 192
    keys, values = torch.randn(heads, length, dim), torch.randn(heads, length, dim)
    full = torch.arange(length).expand(heads, -1)
    target = _reconstruct(keys, values, full)
    started = time.perf_counter()
    baseline_idx = recent_retained_indices(length, budget, prompt_tokens=prompt, heads=heads)
    baseline_time = time.perf_counter() - started
    started = time.perf_counter()
    random_idx = random_retained_indices(
        length, budget, prompt_tokens=prompt, heads=heads, seed=seed
    )
    selection_time = time.perf_counter() - started
    cosine = torch.nn.functional.cosine_similarity
    return {
        "paper": {"arxiv_id": "2609.03430", "title": "Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning", "url": "https://arxiv.org/abs/2609.03430", "organization": "Salesforce AI Research / UIUC"},
        "dataset": {"name": "deterministic KV mechanism fixture", "tokens": length, "heads": heads},
        "setup": {"adapter": "random-attention", "seed": seed, "prompt_tokens": prompt, "retained_tokens": budget},
        "baseline": {"name": "prompt + recent", "attention_cosine": float(cosine(target.flatten(), _reconstruct(keys, values, baseline_idx).flatten(), dim=0)), "selection_seconds": baseline_time},
        "method": {"name": "prompt-protected per-head random eviction", "attention_cosine": float(cosine(target.flatten(), _reconstruct(keys, values, random_idx).flatten(), dim=0)), "selection_seconds": selection_time},
        "stages": {"prompt_protected": True, "independent_head_patterns": int(torch.unique(random_idx, dim=0).shape[0]), "scoring_passes": 0},
        "paper_results": {"vllm_throughput_gain_min_percent": 32.0, "vllm_throughput_gain_max_percent": 43.0},
        "scope": "CPU fixture tests the exact eviction rule; the committed A100 receipt uses real checkpoint KV tensors. Full six-task/vLLM paper matrix is not claimed.",
        "manifest_ref": "reproduction:random-attention",
    }


def render(result: dict) -> str:
    return f"# Random Attention\n\nMethod cosine: {result['method']['attention_cosine']:.4f}\n"
