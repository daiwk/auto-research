#!/usr/bin/env python3
"""Paired public WikiText training; validation selects recipe, test stays sealed.

Byte-level tokenizer is identical for every recipe. This is small from-scratch
LM training, not the original FineWeb-scale or pretrained-SFT experiment.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path

import numpy as np
import torch

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.foundation.adamw4bit import AdamW4Bit


def tensor_data(path, maximum, device):
    data = path.read_bytes()[:maximum]
    if len(data) < 1024:
        raise ValueError("real public text with at least 1024 bytes required")
    return torch.tensor(list(data), dtype=torch.long, device=device)


def loss_on(model, data, length, batches=16):
    losses = []
    model.eval()
    with torch.no_grad():
        for start in range(0, min(len(data) - length, batches * length), length):
            logits = model(data[start:start + length][None])
            losses.append(float(torch.nn.functional.cross_entropy(
                logits.flatten(0, 1), data[start + 1:start + length + 1])))
    model.train()
    return float(np.mean(losses))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--steps", type=int, default=200)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--maximum-train-bytes", type=int, default=1000000)
    args = parser.parse_args()
    seeds = tuple(int(x) for x in args.seeds.split(","))
    if args.steps < 10 or len(set(seeds)) != len(seeds):
        raise ValueError("at least ten updates and distinct seeds required")
    if args.device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA is unavailable")
    torch.set_num_threads(2)
    train = tensor_data(args.data / "train.txt", args.maximum_train_bytes, args.device)
    validation = tensor_data(args.data / "valid.txt", 100000, args.device)
    config = MicroLMConfig(vocab_size=256, dimensions=64, layers=2, heads=4,
                          sequence_length=64)
    rows, trained = [], []
    for seed in seeds:
        torch.manual_seed(seed)
        initial = build_micro_lm("gpt_baseline", config).to(args.device)
        # All recipes share the same *untied* head architecture and initialization.
        # This enables the paper's head-only final-10% NF4-SR schedule.
        initial.output.weight = torch.nn.Parameter(initial.output.weight.detach().clone())
        for recipe in ("adamw", "zip-sr", "ze-eden"):
            torch.manual_seed(seed)
            rng = torch.Generator(device=args.device).manual_seed(seed + 10000)
            model = deepcopy(initial)
            optimizer = (torch.optim.AdamW(model.parameters(), lr=3e-4, betas=(.9, .95),
                                          eps=1e-8, weight_decay=.1) if recipe == "adamw" else
                         AdamW4Bit(model.parameters(), recipe=recipe, lr=3e-4))
            if args.device == "cuda":
                torch.cuda.reset_peak_memory_stats()
            initial_loss = loss_on(model, validation, config.sequence_length)
            for step in range(args.steps):
                starts = torch.randint(len(train) - 65, (4,), generator=rng, device=args.device)
                offsets = torch.arange(64, device=args.device)
                tokens = train[starts[:, None] + offsets]
                labels = train[starts[:, None] + offsets + 1]
                optimizer.zero_grad(set_to_none=True)
                loss = torch.nn.functional.cross_entropy(model(tokens).flatten(0, 1), labels.flatten())
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
                if isinstance(optimizer, AdamW4Bit):
                    optimizer.schedule_lm_head(model.output.parameters(), completed_steps=step,
                                               total_steps=args.steps)
                optimizer.step()
            moment_bytes = sum(v.numel() * v.element_size() for state in optimizer.state.values()
                               for k, v in state.items() if isinstance(v, torch.Tensor)
                               and k != "step")
            packed_values = sum(state.get("m_codes", torch.empty(0)).numel() * 2
                                for state in optimizer.state.values())
            row = {"seed": seed, "recipe": recipe, "steps": args.steps,
                   "initial_validation_loss": initial_loss,
                   "validation_loss": loss_on(model, validation, 64),
                   "persistent_moment_bytes": moment_bytes,
                   "packed_parameter_values": packed_values,
                   "head_first_moment_sr_steps": args.steps - round(.9 * args.steps)
                       if recipe != "adamw" else 0,
                   "untied_head": True,
                   "cuda_peak_allocated_bytes": torch.cuda.max_memory_allocated()
                       if args.device == "cuda" else None}
            rows.append(row)
            trained.append((row, model.cpu()))
            print(json.dumps(row), flush=True)
    means = {recipe: float(np.mean([r["validation_loss"] for r in rows if r["recipe"] == recipe]))
             for recipe in ("adamw", "zip-sr", "ze-eden")}
    selected = min(means, key=means.get)
    # The test text is not even opened until validation selection has finished.
    test = tensor_data(args.data / "test.txt", 100000, args.device)
    for row, model in trained:
        if row["recipe"] == selected:
            row["selected_test_loss"] = loss_on(model.to(args.device), test, 64)
    payload = {"schema_version": 1, "diagnostic_only": False,
               "evaluation_tier": "l2_public_dataset", "rows": rows,
               "selected_recipe": selected, "validation_means": means,
               "claim_scope": "bounded byte-level WikiText training; not original paper benchmark",
               "training_budget": {"steps": args.steps, "batch_size": 4, "sequence_length": 64},
               "dataset": {"id": "WikiText-2", "revision": {
                   split: hashlib.sha256((args.data / filename).read_bytes()).hexdigest()
                   for split, filename in (("train", "train.txt"), ("validation", "valid.txt"), ("test", "test.txt"))}},
               "checkpoint": {"id": "auto-research/micro-lm-gpt-baseline",
                              "initialization": "from-scratch", "config": config.__dict__},
               "test_read_after_selection": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
