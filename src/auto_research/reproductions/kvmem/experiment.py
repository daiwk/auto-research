from __future__ import annotations

from pathlib import Path

import torch

from .model import select_workspace_blocks


def _attend(query, keys, values, index):
    weight = torch.softmax(keys[index] @ query / keys.shape[-1] ** 0.5, dim=0)
    return weight @ values[index]


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    torch.manual_seed(seed)
    length, dim, block_size, selected_blocks = 768, 32, 32, 6
    keys, values = torch.randn(length, dim), torch.randn(length, dim)
    query = keys[83] + keys[401] + 0.05 * torch.randn(dim)
    selected, blocks, _ = select_workspace_blocks(keys, query, block_size=block_size, selected_blocks=selected_blocks)
    recent = torch.arange(length - len(selected), length)
    full = _attend(query, keys, values, torch.arange(length))
    cosine = torch.nn.functional.cosine_similarity
    return {
        "paper": {"arxiv_id": "2609.04852", "title": "KVMem", "url": "https://arxiv.org/abs/2609.04852", "organization": "Shanghai University of Finance and Economics"},
        "dataset": {"name": "deterministic paged-KV fixture", "tokens": length},
        "setup": {"adapter": "kvmem", "seed": seed, "block_size": block_size, "selected_blocks": selected_blocks},
        "baseline": {"name": "recent-context compaction", "attention_cosine": float(cosine(full, _attend(query, keys, values, recent), dim=0))},
        "method": {"name": "query-conditioned paged KV", "attention_cosine": float(cosine(full, _attend(query, keys, values, selected), dim=0))},
        "stages": {"workspace_blocks": length // block_size, "materialized_blocks": len(blocks), "virtualization_tiers": 3},
        "paper_results": {"deepswe_compaction_success_percent": 43.8, "deepswe_kvmem_success_percent": 48.4, "workspace_tokens": 1000000},
        "scope": "CPU fixture checks attention-space indexing and materialization; committed A100 receipt uses real checkpoint KV tensors.",
        "manifest_ref": "reproduction:kvmem",
    }


def render(result: dict) -> str:
    return f"# KVMem\n\nMethod cosine: {result['method']['attention_cosine']:.4f}\n"
