"""Public WikiText-2 KITE/SST versus dense control at matched matmul FLOPs.

This is a small CPU mechanism diagnostic, not the paper's MoE scaling result.
The profiler counts supported forward/backward operator FLOPs; it does not
count optimizer, layer normalization or memory movement. Interpret the
reported compute match as an approximation, and inspect both FLOPs and time.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import statistics
import time

import torch
from torch.nn import functional as F
from torch.profiler import ProfilerActivity, profile

from auto_research.datasets import wikitext_2
from auto_research.foundation_models.kite_sst import SmallSST, train_two_stages


def _batch(text: str, *, seed: int, batch_size: int = 8, sequence: int = 32) -> torch.Tensor:
    values = torch.tensor(list(text.encode("utf-8")), dtype=torch.long)
    if len(values) <= sequence + 1:
        raise ValueError("public split is shorter than the context")
    generator = torch.Generator().manual_seed(seed)
    starts = torch.randint(0, len(values) - sequence - 1, (batch_size,), generator=generator)
    return torch.stack([values[index:index + sequence + 1] for index in starts])


def _nll(model: SmallSST, batch: torch.Tensor) -> float:
    model.eval()
    with torch.inference_mode():
        logits, _ = model(batch[:, :-1])
        return float(F.cross_entropy(logits.reshape(-1, 256), batch[:, 1:].reshape(-1)))


def _profile_update_flops(model: SmallSST, batch: torch.Tensor) -> int:
    model.train()
    model.zero_grad(set_to_none=True)
    with profile(activities=[ProfilerActivity.CPU], with_flops=True) as run:
        logits, _ = model(batch[:, :-1])
        loss = F.cross_entropy(logits.reshape(-1, 256), batch[:, 1:].reshape(-1))
        loss.backward()
    model.zero_grad(set_to_none=True)
    flops = sum(event.flops for event in run.key_averages())
    if flops <= 0:
        raise RuntimeError("this PyTorch profiler did not report model FLOPs")
    return flops


def _train_dense(model: SmallSST, batch: torch.Tensor, stages: tuple[int, int]) -> None:
    model.train()
    inputs, labels = batch[:, :-1], batch[:, 1:]
    for steps in stages:
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
        for _ in range(steps):
            logits, _ = model(inputs)
            loss = F.cross_entropy(logits.reshape(-1, 256), labels.reshape(-1))
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()


def _last_token_latency_ms(model: SmallSST, prompt: torch.Tensor, repeats: int = 20) -> float:
    model.eval()
    with torch.inference_mode():
        for _ in range(3):
            model(prompt, last_only=True)
        samples = []
        for _ in range(repeats):
            started = time.perf_counter_ns()
            model(prompt, last_only=True)
            samples.append((time.perf_counter_ns() - started) / 1e6)
    return statistics.median(samples)


def run(
    *, data_root: Path, seeds: tuple[int, ...] = (42, 43, 44),
    source_steps: int = 30, continuation_steps: int = 30,
) -> dict:
    if len(seeds) < 1 or len(set(seeds)) != len(seeds):
        raise ValueError("nonempty unique seeds required")
    if min(source_steps, continuation_steps) < 1:
        raise ValueError("training budgets must be positive")
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    corpus = wikitext_2(data_root, allow_network=False)
    split_sha256 = {
        name: hashlib.sha256(content.encode()).hexdigest()
        for name, content in corpus.items()
    }
    rows = []
    for seed in seeds:
        torch.manual_seed(seed)
        source = SmallSST(256, width=32, layers=2, max_positions=64).cpu()
        dense = SmallSST(256, width=32, layers=4, max_positions=64).cpu()
        # Match embeddings/head and the first two blocks at initialization.
        dense_state = dense.state_dict()
        dense_state.update(source.state_dict())
        dense.load_state_dict(dense_state)
        train = _batch(corpus["train"], seed=seed)
        validation = _batch(corpus["validation"], seed=seed + 1000, batch_size=64)
        test = _batch(corpus["test"], seed=seed + 2000, batch_size=64)
        source_flops = _profile_update_flops(source, train)
        expanded_profiler_model = deepcopy(source)
        expanded_profiler_model.expand()
        expanded_flops = _profile_update_flops(expanded_profiler_model, train)
        dense_flops = _profile_update_flops(dense, train)
        # Both models restart AdamW at the stage boundary. Rounding is explicit.
        dense_stages = (
            max(1, round(source_steps * source_flops / dense_flops)),
            max(1, round(continuation_steps * expanded_flops / dense_flops)),
        )
        started = time.perf_counter()
        train_two_stages(
            source, train, source_steps=source_steps,
            continuation_steps=continuation_steps,
        )
        expanded_train_seconds = time.perf_counter() - started
        started = time.perf_counter()
        _train_dense(dense, train, dense_stages)
        dense_train_seconds = time.perf_counter() - started
        expanded_total_flops = source_steps * source_flops + continuation_steps * expanded_flops
        dense_total_flops = sum(dense_stages) * dense_flops
        prompt = validation[:1, :32]
        rows.append({
            "seed": seed,
            "expanded_validation_nll": _nll(source, validation),
            "dense_validation_nll": _nll(dense, validation),
            "expanded_test_nll": _nll(source, test),
            "dense_test_nll": _nll(dense, test),
            "expanded_parameters": sum(p.numel() for p in source.parameters()),
            "dense_parameters": sum(p.numel() for p in dense.parameters()),
            "expanded_profiled_flops": expanded_total_flops,
            "dense_profiled_flops": dense_total_flops,
            "compute_ratio_dense_over_expanded": dense_total_flops / expanded_total_flops,
            "dense_stage_steps": dense_stages,
            "expanded_train_seconds": expanded_train_seconds,
            "dense_train_seconds": dense_train_seconds,
            "expanded_last_token_latency_ms": _last_token_latency_ms(source, prompt),
            "dense_last_token_latency_ms": _last_token_latency_ms(dense, prompt),
        })
    return {
        "paper": "KITE arXiv:2609.27294",
        "status": "diagnostic_only",
        "dataset": "WikiText-2 raw byte-level next-token task",
        "dataset_sha256": split_sha256,
        "selection_split": "validation_only",
        "test_used_for_selection": False,
        "compute_accounting": "PyTorch profiler-supported forward/backward FLOPs only",
        "model": "two-stage 2+2 dense SST versus four-layer dense transformer; width 32",
        "source_steps": source_steps,
        "continuation_steps": continuation_steps,
        "runs": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-steps", type=int, default=30)
    parser.add_argument("--continuation-steps", type=int, default=30)
    args = parser.parse_args()
    print(json.dumps(run(
        data_root=args.data_root,
        seeds=tuple(int(seed) for seed in args.seeds.split(",")),
        source_steps=args.source_steps,
        continuation_steps=args.continuation_steps,
    ), indent=2))
