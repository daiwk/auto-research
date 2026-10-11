#!/usr/bin/env python3
"""Real Qwen3 VFold calibration, exact-fold check and heldout cache decoding.

This bounded GSM8K runtime checks actual cache storage and logits; it does not
reproduce official RULER/LongBench scores or claim a fused decoding speedup.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import time

import torch

from auto_research.foundation.vfold import attach_finish_hooks, fit_alignment, fold_attention
from auto_research.foundation.vfold_cache import VFoldCache
from auto_research.post_training.oct10_checkpoint import _prompt, load_public_rows, verified_reward
from auto_research.public_holdout import validate_holdout


def collect_values(model, inputs):
    collected = [[] for _ in model.model.layers]
    handles = []
    heads, dim = model.config.num_key_value_heads, model.config.head_dim
    for index, layer in enumerate(model.model.layers):
        def capture(_, args, output, index=index):
            collected[index].append(output.detach().reshape(-1, heads, dim).float())
        handles.append(layer.self_attn.v_proj.register_forward_hook(capture))
    try:
        for ids in inputs:
            with torch.no_grad():
                model(ids, use_cache=False)
    finally:
        for handle in handles:
            handle.remove()
    return [torch.cat(rows) for rows in collected]


def decode(model, tokenizer, prompt, *, compressed, maximum_tokens):
    cache = VFoldCache(len(model.model.layers)) if compressed else None
    generated = []
    with torch.no_grad():
        output = model(prompt, past_key_values=cache, use_cache=True)
        cache = output.past_key_values
        for step in range(maximum_tokens):
            token = output.logits[:, -1].argmax(-1).reshape(1, 1)
            generated.append(int(token))
            if int(token) == tokenizer.eos_token_id or step == maximum_tokens - 1:
                break
            output = model(token, past_key_values=cache, use_cache=True)
    if compressed:
        persistent = cache.banks.persistent_bytes()
    else:
        persistent = sum(t.untyped_storage().nbytes() for layer in cache.layers
                         for t in (layer.keys, layer.values))
    return {"response": tokenizer.decode(generated, skip_special_tokens=True),
            "generated_tokens": len(generated), "cache_tokens": cache.get_seq_length(),
            "persistent_cache_bytes": persistent}


def main():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    p = argparse.ArgumentParser(description=__doc__)
    for name in ("checkpoint-path", "train-path", "validation-path", "split-manifest", "output"):
        p.add_argument("--" + name, required=True, type=Path)
    for name in ("checkpoint-id", "checkpoint-revision", "dataset-revision"):
        p.add_argument("--" + name, required=True)
    p.add_argument("--calibration-examples", type=int, default=4)
    p.add_argument("--validation-examples", type=int, default=4)
    p.add_argument("--max-tokens", type=int, default=256)
    p.add_argument("--calibration-max-tokens", type=int, default=512)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda")
    a = p.parse_args()
    if min(a.calibration_examples, a.validation_examples, a.max_tokens, a.calibration_max_tokens) < 1:
        raise ValueError("positive budgets required")
    split = validate_holdout(a.split_manifest, a.train_path, a.validation_path,
                             dataset_revision=a.dataset_revision)
    torch.manual_seed(a.seed)
    tokenizer = AutoTokenizer.from_pretrained(a.checkpoint_path, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(a.checkpoint_path, local_files_only=True,
             dtype=torch.bfloat16 if a.device.startswith("cuda") else torch.float32,
             attn_implementation="eager").to(a.device).eval()
    if model.config.model_type != "qwen3" or len(model.model.layers) % 2:
        raise ValueError("this adapter supports even-layer full-attention Qwen3 only")
    if any(layer.self_attn.sliding_window for layer in model.model.layers):
        raise ValueError("sliding-window caches need separate adapter")
    model.requires_grad_(False)
    original = deepcopy(model)
    train = load_public_rows(a.train_path)
    valid = load_public_rows(a.validation_path)
    inputs = [_prompt(tokenizer, r["question"], a.device)[:, :a.calibration_max_tokens]
              for r in train[:a.calibration_examples]]
    values = collect_values(model, inputs)
    start, pairs = time.perf_counter(), []
    for index in range(0, len(values), 2):
        alignment = fit_alignment(values[index], values[index + 1])
        fold_attention(model.model.layers[index + 1].self_attn, alignment,
                       head_dim=model.config.head_dim, query_heads=model.config.num_attention_heads,
                       kv_heads=model.config.num_key_value_heads)
        record = {"layers": [index, index + 1], "permutation": alignment.permutation,
                  "cost": alignment.cost, "map_max_condition": float(torch.linalg.cond(alignment.maps).max())}
        pairs.append(record)
        print(json.dumps(record), flush=True)
    calibration_seconds = time.perf_counter() - start
    del values
    with torch.no_grad():
        probe = _prompt(tokenizer, valid[0]["question"], a.device)
        base_logits, folded_logits = original(probe, use_cache=False).logits.float(), model(probe, use_cache=False).logits.float()
        relative = float(torch.linalg.vector_norm(base_logits - folded_logits) / torch.linalg.vector_norm(base_logits))
        if not torch.isfinite(folded_logits).all() or relative > .02:
            raise ValueError(f"BF16 fold function-preservation error too large: {relative}")
    del base_logits, folded_logits
    hooks = attach_finish_hooks(model)
    rows = []
    try:
        for index, example in enumerate(valid[:a.validation_examples]):
            ids = _prompt(tokenizer, example["question"], a.device)
            for name, network, compressed in (("full", original, False), ("vfold", model, True)):
                record = decode(network, tokenizer, ids, compressed=compressed, maximum_tokens=a.max_tokens)
                record.update(example=index, recipe=name, exact_match=verified_reward(record["response"], example["answer"]),
                              prompt_tokens=ids.shape[-1])
                # Keep answers out of the model input; only external scorer reads labels.
                rows.append(record)
                print(json.dumps({k: v for k, v in record.items() if k != "response"}), flush=True)
    finally:
        for hook in hooks:
            hook.remove()
    report = {"adapter_key": "vfold", "seed": a.seed, "diagnostic_only": True,
              "evaluation_tier": "l1_mechanism", "checkpoint": {"id": a.checkpoint_id, "revision": a.checkpoint_revision},
              "dataset": {"id": split["source_id"], "revision": a.dataset_revision},
              "split_provenance": split, "test_read": split["test_read"], "pairs": pairs, "rows": rows,
              "exact_fold_relative_logit_error": relative, "calibration_seconds": calibration_seconds,
              "limitations": ["small GSM8K training-only holdout; not official LongBench/RULER",
                              "eager materialization incurs transient full values; no kernel latency gain claimed",
                              "first 4 and last 128 values protected; keys never merged",
                              "batch-one Qwen3 full-attention backend; no beam or speculative rollback"]}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
