#!/usr/bin/env python3
"""Validate real bitmask SpMV and decoded calibration on a public checkpoint."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time

import torch

from auto_research.foundation.sparse_decoding import DecodeCalibration, PackedDecodeLinear, pack_bitmask, wanda_nm
from auto_research.foundation.sparse_decoding_cuda import bitmask_spmv
from auto_research.post_training.oct10_checkpoint import _prompt, load_public_rows, verified_reward
from auto_research.public_holdout import validate_holdout


def kernel_checks(seed):
    torch.manual_seed(seed)
    rows = []
    for n, m in ((2, 4), (4, 8), (8, 16), (16, 32)):
        weight = torch.randn(257, 2048, device="cuda", dtype=torch.bfloat16)
        sparse, keep = wanda_nm(weight, torch.rand(2048, device="cuda"), n=n, m=m)
        values, words = pack_bitmask(sparse, keep)
        vector = torch.randn(2048, device="cuda", dtype=torch.bfloat16)
        actual = bitmask_spmv(values, words, vector)
        expected = (sparse.float() @ vector.float()).to(vector.dtype)
        relative = float((actual.float() - expected.float()).norm() / expected.float().norm())
        if relative > .005:
            raise ValueError(f"sparse CUDA mismatch: {relative}")
        for _ in range(5):
            bitmask_spmv(values, words, vector)
        torch.cuda.synchronize()
        start = time.perf_counter()
        for _ in range(30):
            bitmask_spmv(values, words, vector)
        torch.cuda.synchronize()
        sparse_ms = (time.perf_counter() - start) * 1000 / 30
        for _ in range(5):
            torch.nn.functional.linear(vector, sparse)
        torch.cuda.synchronize()
        start = time.perf_counter()
        for _ in range(30):
            torch.nn.functional.linear(vector, sparse)
        torch.cuda.synchronize()
        dense_ms = (time.perf_counter() - start) * 1000 / 30
        rows.append({"n": n, "m": m, "relative_error": relative, "sparse_ms": sparse_ms,
                     "dense_pruned_ms": dense_ms, "metadata_bits_per_nonzero": 2})
    print(json.dumps({"kernel_checks": rows}), flush=True)
    return rows


def generated(model, tokenizer, question, *, max_tokens, collector=None):
    ids = _prompt(tokenizer, question, "cuda")
    with torch.no_grad():
        result = model(ids, use_cache=True)
        tokens = []
        decode_calls = 0
        ended_with_eos = False
        torch.cuda.synchronize()
        start = time.perf_counter()
        for index in range(max_tokens):
            token = result.logits[:, -1].argmax(-1).reshape(1, 1)
            tokens.append(int(token))
            if int(token) == tokenizer.eos_token_id:
                ended_with_eos = True
                break
            # Do not execute a discarded forward pass after the final token.
            if index + 1 == max_tokens:
                break
            if collector is None:
                result = model(token, past_key_values=result.past_key_values, use_cache=True)
            else:
                with collector.decoding():
                    result = model(token, past_key_values=result.past_key_values, use_cache=True)
            decode_calls += 1
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
    return tokenizer.decode(tokens, skip_special_tokens=True), {
        "tokens": len(tokens), "decode_calls": decode_calls, "decode_seconds": elapsed,
        "ended_with_eos": ended_with_eos, "truncated": not ended_with_eos,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--kernel-only", action="store_true")
    p.add_argument("--output", type=Path, required=True)
    for name in ("checkpoint-path", "train-path", "validation-path", "split-manifest"):
        p.add_argument("--" + name, type=Path)
    for name in ("checkpoint-id", "checkpoint-revision", "dataset-revision"):
        p.add_argument("--" + name)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--n", type=int, default=2)
    p.add_argument("--m", type=int, default=4)
    p.add_argument("--calibration-examples", type=int, default=4)
    p.add_argument("--validation-examples", type=int, default=4)
    p.add_argument("--max-tokens", type=int, default=512)
    a = p.parse_args()
    if not torch.cuda.is_available():
        raise ValueError("real NVIDIA CUDA required")
    kernels = kernel_checks(a.seed)
    report = {"schema_version": 1, "adapter_key": "sparse-decoding", "seed": a.seed,
              "kernel_checks": kernels, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
              "claim_scope": "bounded Wanda backend and independent bitmask SpMV; not WritingBench/ClassEval or original kernel speedup",
              "max_tokens": a.max_tokens, "warmup": "two training-question tokens per recipe before timed validation"}
    if not a.kernel_only:
        required = (a.checkpoint_path, a.train_path, a.validation_path, a.split_manifest,
                    a.checkpoint_id, a.checkpoint_revision, a.dataset_revision)
        if not all(required) or min(a.calibration_examples, a.validation_examples, a.max_tokens) < 1:
            p.error("checkpoint identity, fixed public holdout and positive budgets required")
        split = validate_holdout(a.split_manifest, a.train_path, a.validation_path, dataset_revision=a.dataset_revision)
        from transformers import AutoModelForCausalLM, AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(a.checkpoint_path, local_files_only=True)
        model = AutoModelForCausalLM.from_pretrained(a.checkpoint_path, local_files_only=True, dtype=torch.bfloat16,
                                                    attn_implementation="eager").to("cuda").eval()
        train, valid = load_public_rows(a.train_path), load_public_rows(a.validation_path)
        layers = {name: layer for name, layer in model.named_modules()
                  if isinstance(layer, torch.nn.Linear) and name != "lm_head" and layer.in_features % 32 == 0}
        collector = DecodeCalibration(layers)
        calibration_generations = []
        try:
            for row in train[:a.calibration_examples]:
                _, stats = generated(model, tokenizer, row["question"], max_tokens=a.max_tokens, collector=collector)
                calibration_generations.append(stats)
        finally:
            collector.close()
        if not layers or not all(collector.counts.values()):
            raise ValueError("every prunable layer requires decoded activations")
        fixed = DecodeCalibration(layers)
        try:
            for row in train[:a.calibration_examples]:
                # Fixed-text baseline, including prefill, supplied exclusively
                # from training labels. It is explicitly NOT decode calibration.
                ids = _prompt(tokenizer, row["question"] + "\n" + row["answer"], "cuda")
                with torch.no_grad(), fixed.decoding():
                    model(ids, use_cache=False)
        finally:
            fixed.close()
        rows = []
        for recipe in ("dense", "fixed-text-wanda-bitmask", "decode-wanda-bitmask"):
            if recipe != "dense":
                for name, layer in layers.items():
                    energy = collector.energy if recipe == "decode-wanda-bitmask" else fixed.energy
                    sparse, keep = wanda_nm(layer.weight.detach(), energy[name], n=a.n, m=a.m)
                    packed = PackedDecodeLinear(sparse, keep, layer.bias)
                    parent, attr = name.rsplit(".", 1)
                    setattr(model.get_submodule(parent), attr, packed)
                torch.cuda.empty_cache()
            # Compile every checkpoint-specific shape on training input only.
            generated(model, tokenizer, train[0]["question"], max_tokens=2)
            for index, row in enumerate(valid[:a.validation_examples]):
                text, stats = generated(model, tokenizer, row["question"], max_tokens=a.max_tokens)
                item = {"recipe": recipe, "example": index, **stats,
                        "correct": verified_reward(text, row["answer"])}
                rows.append(item)
                print(json.dumps(item), flush=True)
        sparse_layers = [layer for layer in model.modules() if isinstance(layer, PackedDecodeLinear)]
        if not sparse_layers or not all(layer.sparse_calls for layer in sparse_layers):
            raise ValueError("all replaced layers must execute actual sparse CUDA calls")
        report.update(checkpoint={"id": a.checkpoint_id, "revision": a.checkpoint_revision},
                      dataset={"id": "openai/grade-school-math", "revision": a.dataset_revision,
                               "train_sha256": hashlib.sha256(a.train_path.read_bytes()).hexdigest(),
                               "validation_sha256": hashlib.sha256(a.validation_path.read_bytes()).hexdigest()},
                      split_provenance=split, n=a.n, m=a.m, rows=rows,
                      calibration={"phase": "decode_only", "prefill_excluded": True, "counts": collector.counts,
                                   "generations": calibration_generations},
                      fixed_text_calibration={"phase": "teacher_forced_train_only", "counts": fixed.counts},
                      sparse_calls=sum(layer.sparse_calls for layer in sparse_layers),
                      retained_dense_prefill_copy=True,
                      packed_bytes=sum(layer.values.numel() * layer.values.element_size() + layer.words.numel() * 4 for layer in sparse_layers),
                      test_read=split["test_read"])
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
