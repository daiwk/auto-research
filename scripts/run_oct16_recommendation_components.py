#!/usr/bin/env python3
"""Bounded STATIC, public cross-task training and TransX operator verification.

No downloads. Use an explicit official KuaiRand-Pure training-log prefix CSV.
The small chronological split is diagnostic, not YouTube/LinkedIn reproduction.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import time

import numpy as np
import torch
from torch.nn import functional as F

from auto_research.reproductions.cross_task_relationships.model import CrossTaskModel, auxiliary_loss, validate_pair
from auto_research.reproductions.static_constraint_decoding.algorithm import StaticTrie, beam_step
from auto_research.reproductions.transx.technical_report import RowWiseAdagrad, multi_cutoff_memory


def load_public(path: Path, limit: int):
    if not 100 <= limit <= 8192:
        raise ValueError("public diagnostic prefix budget is 100..8192 rows")
    with path.open() as stream:
        rows = list(itertools.islice(csv.DictReader(stream), limit))
    if len(rows) < 100:
        raise ValueError("insufficient public impressions")
    fields = ("user_id", "video_id", "time_ms", "duration_ms", "hourmin", "is_click", "long_view")
    revision = hashlib.sha256(json.dumps([[r[k] for k in fields] for r in rows], separators=(",", ":")).encode()).hexdigest()
    rows.sort(key=lambda r: int(r["time_ms"]))
    users, items = {}, {}
    u, v, features, labels = [], [], [], []
    for row in rows:
        u.append(users.setdefault(row["user_id"], len(users)))
        v.append(items.setdefault(row["video_id"], len(items)))
        hour = int(row["hourmin"]) // 100
        features.append([math.log1p(max(0, int(row["duration_ms"]))) / 12,
                         math.sin(hour * math.pi / 12), math.cos(hour * math.pi / 12)])
        labels.append([float(row["is_click"]), float(row["long_view"])])
    tensors = (torch.tensor(u), torch.tensor(v), torch.tensor(features), torch.tensor(labels))
    metadata = {"id": "KuaiRand-Pure/official-standard-log-fixed-prefix",
                "source_url": "https://zenodo.org/records/10439422", "revision": "sha256:" + revision,
                "selected_fields": list(fields), "rows": len(rows), "prefix_limit": limit,
                "split": "chronological 70/15/15 after fixed file-prefix selection",
                "features": "pre-impression user/video identifiers, duration and hour only",
                "selection_bias": "file-prefix diagnostic, not a representative production sample"}
    return tensors, metadata, sorted(int(item) for item in items)


def cross_task(data, metadata, *, seed: int, device: str, steps: int):
    torch.manual_seed(seed)
    users, items, features, labels = (x.to(device) for x in data)
    n = len(users)
    train, validation = int(.7 * n), int(.85 * n)
    counts = validate_pair(labels[:train])
    model = CrossTaskModel(int(users.max()) + 1, int(items.max()) + 1).to(device)
    initial = copy.deepcopy(model.state_dict())
    generator = torch.Generator().manual_seed(seed + 100)
    indices = [torch.randint(train, (64,), generator=generator).to(device) for _ in range(steps)]
    order = torch.randperm(train, generator=generator).to(device)
    shuffled = labels[:train].prod(-1)[order]
    output = {}
    for arm, weight in (("marginals", 0.), ("cross-label", .1), ("shuffled-cross-control", .1)):
        model.load_state_dict(initial)
        optimizer = torch.optim.AdamW(model.parameters(), lr=.003, weight_decay=0.)
        start = model.body[0].weight.detach().clone()
        for index in indices:
            logits, pair = model(users[index], items[index], features[index])
            loss, _ = auxiliary_loss(logits, pair, labels[index], weight=weight,
                                     auxiliary_labels=shuffled[index] if arm == "shuffled-cross-control" else None)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            metrics = {}
            for name, section in (("validation", slice(train, validation)), ("test", slice(validation, n))):
                logits, _ = model(users[section], items[section], features[section])
                metrics[name + "_bce"] = float(F.binary_cross_entropy_with_logits(logits, labels[section]))
                metrics[name + "_brier"] = float((logits.sigmoid() - labels[section]).square().mean())
        metrics.update(parameter_delta_l2=float((model.body[0].weight - start).norm().detach()), optimizer_steps=steps)
        output[arm] = metrics
    return {"method": "cross-task-relationships", "seed": seed, "dataset": metadata,
            "training_pair_counts": counts, "arms": output, "hyperparameter_selection": False,
            "test_used_only_after_fixed_training": True, "input_contains_feedback": False,
            "diagnostic_only": True, "promotion_eligible": False}


def static(items, metadata, *, seed: int, device: str):
    # Reversible base-16 item IDs, NOT learned semantic IDs or a retrieval model.
    width = max(2, math.ceil(max(items).bit_length() / 4))
    rows = [tuple((item >> (4 * i)) & 15 for i in range(width - 1, -1, -1)) for item in items]
    trie = StaticTrie.build(rows, 16, dense_depth=2).to(device)
    torch.manual_seed(seed)
    nodes, scores = torch.ones(8, 1, dtype=torch.long, device=device), torch.zeros(8, 1, device=device)
    prefixes = torch.empty(8, 1, 0, dtype=torch.long, device=device)
    for step in range(width):
        logits = torch.randn(8, nodes.shape[1], 16, device=device)
        result = beam_step(trie, logits, nodes, scores, prefixes, step=step, beam_width=8)
        nodes, scores, prefixes = result["nodes"], result["scores"], result["prefixes"]
    allowed = set(rows)
    decoded = prefixes[result["alive"]].tolist()
    valid = sum(tuple(row) in allowed for row in decoded)
    # Stable fixed-shape microbenchmark, including full-vocabulary normalization.
    probe_nodes = torch.ones(64, 8, dtype=torch.long, device=device)
    probe = torch.randn(64, 8, 16, device=device).log_softmax(-1)
    for _ in range(10):
        trie.candidates(probe, probe_nodes, 0)
    if device == "cuda":
        torch.cuda.synchronize()
    started = time.perf_counter()
    for _ in range(100):
        trie.candidates(probe, probe_nodes, 0)
    if device == "cuda":
        torch.cuda.synchronize()
    return {"method": "static-constraint-decoding", "seed": seed, "dataset": metadata,
            "constraint_items": len(rows), "identifier_tokens": width, "decoded": len(decoded),
            "valid_decoded": valid, "validity": valid / max(1, len(decoded)),
            "mean_extraction_ms": 1000 * (time.perf_counter() - started) / 100,
            "identifier_protocol": "reversible base16 public video IDs, not learned semantic IDs",
            "diagnostic_only": True, "promotion_eligible": False}


def transx(*, seed: int, device: str):
    torch.manual_seed(seed)
    x = torch.randn(64, 16, dtype=torch.float64, device=device, requires_grad=True)
    scoring = torch.randn(16, dtype=torch.float64, device=device, requires_grad=True)
    scores = x @ scoring
    cutoffs = [0, 7, 14, 28, 42, 56, 64]
    shared, counts = multi_cutoff_memory(x, scores, cutoffs)
    direct, _ = multi_cutoff_memory(x, scores, cutoffs, shared=False)
    weights = [torch.randn_like(row) for row in shared]
    lhs = sum((a * w).sum() for a, w in zip(shared, weights, strict=True))
    rhs = sum((a * w).sum() for a, w in zip(direct, weights, strict=True))
    grad = torch.autograd.grad(lhs, (x, scoring), retain_graph=True)
    oracle = torch.autograd.grad(rhs, (x, scoring))
    error = max(float((a - b).abs().max().detach()) for a, b in zip(grad, oracle, strict=True))
    forward = max(float((a - b).abs().max().detach()) for a, b in zip(shared, direct, strict=True) if a.numel())
    embedding = torch.nn.Embedding(32, 8, sparse=True, device=device)
    before = embedding.weight.detach().clone()
    optimizer = RowWiseAdagrad(embedding.parameters(), lr=.01)
    dense = torch.nn.Linear(8, 1, device=device)
    dense_optimizer = torch.optim.AdamW(dense.parameters(), lr=.001)
    # Two microbatches accumulate duplicate row gradients before one logical step.
    for ids in ([1, 1, 3], [1, 3, 5]):
        dense(embedding(torch.tensor(ids, device=device))).square().mean().div(2).backward()
    optimizer.step()
    dense_optimizer.step()
    untouched = [i for i in range(32) if i not in {1, 3, 5}]
    return {"method": "transx-report-components", "seed": seed,
            "dataset": {"id": "explicit-multi-cutoff-memory-and-sparse-gradient-fixture",
                        "revision": "transx-appendix-a-equivalence-v1", "capability_dataset": False},
            "maximum_forward_error": forward, "maximum_gradient_error": error,
            "counts": counts, "embedding_delta_l2": float((embedding.weight - before).norm().detach()),
            "untouched_row_error": float((embedding.weight[untouched] - before[untouched]).abs().max().detach()),
            "row_accumulator_elements": optimizer.state[embedding.weight]["sum"].numel(),
            "diagnostic_only": True, "promotion_eligible": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--rows", type=int, default=4096)
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or not 1 <= args.steps <= 64:
        raise ValueError("use a new output and at most 64 training steps")
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU fallback")
    seeds = [int(x) for x in args.seeds.split(",")]
    if len(seeds) != len(set(seeds)):
        raise ValueError("independent seed IDs must be unique")
    torch.set_num_threads(1)
    data, metadata, items = load_public(args.csv, args.rows)
    results = []
    for seed in seeds:
        results.append({"seed": seed, "static": static(items, metadata, seed=seed, device=args.device),
                        "cross_task": cross_task(data, metadata, seed=seed, device=args.device, steps=args.steps),
                        "transx": transx(seed=seed, device=args.device)})
    payload = {"schema_version": 2, "seeds": seeds, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
               "results": results, "diagnostic_only": True, "promotion_eligible": False,
               "full_experiment_status": "not_reproduced_high_cost"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"seeds": seeds, "device": args.device, "papers": 3, "output": str(args.output)}))


if __name__ == "__main__":
    main()
