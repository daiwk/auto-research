from __future__ import annotations

from pathlib import Path

from .model import repair_retained_indices, streaming_retained_indices


def reproduce_twinkv(dataset_dir: Path, seed: int = 42):
    import torch

    generator = torch.Generator().manual_seed(seed)
    prototypes = torch.randn(48, 32, generator=generator)
    keys = prototypes.repeat(4, 1)
    keys = keys + 0.02 * torch.randn(keys.shape, generator=generator)
    retained = streaming_retained_indices(len(keys), 96, sink_tokens=4)
    repaired, diagnostics = repair_retained_indices(
        keys, retained, threshold=0.85, local_window=8, sink_tokens=4,
        recent_tokens=24,
    )
    return {
        "paper": {"arxiv_id": "2608.27128", "title": "TwinKV"},
        "dataset": {"name": "deterministic redundant-key mechanism mini-suite"},
        "setup": {"seed": seed, "sequence_length": len(keys), "retained_tokens": len(retained)},
        "baseline": {"name": "StreamingLLM", "retained_tokens": len(retained)},
        "method": {"name": "StreamingLLM + TwinKV", "retained_tokens": len(repaired), **diagnostics.__dict__},
        "relative": {"budget_change_percent": 100.0 * (len(repaired) - len(retained)) / len(retained)},
        "diagnostic_only": True,
        "scope": "固定预算 repair 公式验证；真实 Qwen3 KV 与 WikiText-2 结果见 GPU receipt。",
    }


def render(result):
    return f"# TwinKV\n\nFixed-budget swaps: {result['method']['swaps']}.\n"
