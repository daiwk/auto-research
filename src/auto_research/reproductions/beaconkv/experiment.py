from __future__ import annotations

from pathlib import Path

import torch

from .model import beacon_retained_indices


def _attend(query, keys, values, index):
    weight = torch.softmax(keys[index] @ query / keys.shape[-1] ** 0.5, dim=0)
    return weight @ values[index]


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    torch.manual_seed(seed)
    length, dim, budget = 512, 32, 160
    keys, values, queries = torch.randn(length, dim), torch.randn(length, dim), torch.randn(96, dim)
    query = queries[-1]
    selected = beacon_retained_indices(keys, queries, budget, beacon_count=8, recent_tokens=64)
    recent = torch.arange(length - budget, length)
    full = _attend(query, keys, values, torch.arange(length))
    cosine = torch.nn.functional.cosine_similarity
    return {
        "paper": {"arxiv_id": "2609.04971", "title": "BeaconKV", "url": "https://arxiv.org/abs/2609.04971", "organization": "Hanyang University"},
        "dataset": {"name": "deterministic KV mechanism fixture", "tokens": length},
        "setup": {"adapter": "beaconkv", "seed": seed, "retained_tokens": budget, "beacons": 8},
        "baseline": {"name": "recent-token KV", "attention_cosine": float(cosine(full, _attend(query, keys, values, recent), dim=0))},
        "method": {"name": "beacon-query KV", "attention_cosine": float(cosine(full, _attend(query, keys, values, selected), dim=0))},
        "stages": {"beacon_queries": 8, "recent_tokens_protected": 64, "selected_tokens": len(selected)},
        "paper_results": {"memory_reduction_x": 5.8, "throughput_improvement_x": 4.3},
        "scope": "CPU fixture checks beacon clustering and scoring; committed A100 receipt uses real checkpoint KV tensors.",
        "manifest_ref": "reproduction:beaconkv",
    }


def render(result: dict) -> str:
    return f"# BeaconKV\n\nMethod cosine: {result['method']['attention_cosine']:.4f}\n"
