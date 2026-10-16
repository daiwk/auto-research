#!/usr/bin/env python3
"""Bounded formula diagnostics only; no checkpoint, network access, or benchmark claims."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import statistics
import subprocess
import sys
import time

import numpy as np
import torch

from auto_research.foundation_models.cots import CotsState, competitive_token_selection
from auto_research.foundation_models.novelty_patching import (
    calibrate_threshold, document_fingerprint, fit_novelty_table,
)
from auto_research.foundation_models.rope_relay import apply_rotary, relay_cache, rotary_factors

ROOT = Path(__file__).resolve().parents[1]
KEYS = ("novelty-patching", "rope-relay", "cots")


def corpus_documents(args: argparse.Namespace) -> tuple[list[bytes], dict]:
    required = (args.corpus_path, args.corpus_sha256, args.corpus_id, args.corpus_revision)
    if not all(required):
        raise ValueError("novelty requires --corpus-path/--corpus-sha256/--corpus-id/--corpus-revision")
    if args.corpus_path.stat().st_size > 16_000_000:
        raise ValueError("source corpus exceeds the 16 MB local read bound")
    raw = args.corpus_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != args.corpus_sha256:
        raise ValueError("public training corpus SHA-256 mismatch")
    if args.corpus_format == "raw":
        documents = [raw[:args.corpus_max_bytes]]
    else:
        documents, consumed = [], 0
        for line in raw.splitlines():
            item = json.loads(line)
            if not isinstance(item.get("question"), str) or not isinstance(item.get("answer"), str):
                raise ValueError("GSM8K training JSONL must contain question and answer strings")
            data = (item["question"] + "\n" + item["answer"] + "\n").encode("utf-8")
            take = data[:args.corpus_max_bytes - consumed]
            if take:
                documents.append(take)
                consumed += len(take)
            if consumed >= args.corpus_max_bytes:
                break
    if not documents or not sum(map(len, documents)):
        raise ValueError("training corpus is empty")
    return documents, {
        "id": args.corpus_id, "revision": args.corpus_revision,
        "source_sha256": digest, "split": "public_train_only_caller_declared",
        "format": args.corpus_format, "training_bytes": sum(map(len, documents)),
        "documents": len(documents), "training_fingerprint": document_fingerprint(documents),
        "validation_used_for_threshold": False, "test_read": False,
        "checkpoint": None,
    }


def novelty_diagnostic(args: argparse.Namespace) -> dict:
    documents, dataset = corpus_documents(args)
    started = time.monotonic()
    table = fit_novelty_table(documents)
    calibration = calibrate_threshold(table, documents, .1)
    scores = np.concatenate([table.scores(doc) for doc in documents])
    prefix = documents[0][:min(100, len(documents[0]))]
    left, right = prefix + b"future A", prefix + b"future B"
    causal = bool(np.array_equal(table.scores(left)[:len(prefix)+1], table.scores(right)[:len(prefix)+1]))
    observed = float((scores > calibration.threshold).mean())
    assert causal and abs(observed - calibration.achieved_rate) < 1e-12
    return {
        "dataset": dataset, "seeds": [], "deterministic": True,
        "configuration": {"window": 128, "match_cap": 16, "minimum_context_count": 20,
                          "target_patch_rate": .1, "threshold_calibrated_on": "same public training bytes",
                          "document_boundaries_reset_history": True, "future_labels_online": False},
        "metrics": {"training_patch_rate": observed, "target_rate_absolute_error": abs(observed-.1),
                    "threshold": calibration.threshold, "global_mean_novelty": table.global_mean,
                    "frequent_two_byte_contexts": int((table.two_byte_counts >= 20).sum()),
                    "frequent_one_byte_contexts": int((table.one_byte_counts >= 20).sum()),
                    "prefix_causal": causal, "calibration_rate_matches_execution": True},
        "elapsed_seconds": time.monotonic() - started,
    }


def rope_diagnostic(seed: int, device: str) -> dict:
    generator = torch.Generator(device=device).manual_seed(seed)
    raw = torch.randn(2, 2, 8, 12, generator=generator, device=device, requires_grad=True)
    values = torch.randn(2, 2, 8, 5, generator=generator, device=device, requires_grad=True)
    query = torch.randn(2, 2, 3, 12, generator=generator, device=device, requires_grad=True)
    source = torch.tensor([[[100, 2, 8191, 20, 90, 7, 300, 45], [7, 41, 200, 3, 999, 20, -1, -1]],
                           [[45, 2, 998, 9, -1, -1, -1, -1], [78, 5, -1, -1, -1, -1, -1, -1]]], device=device)
    frequency = torch.tensor([1., .1, .01, .001], device=device)
    def factors(p):
        return rotary_factors(p, frequency, 1.3)
    cached = apply_rotary(raw, *factors(source.clamp_min(0)))
    result = relay_cache(cached, values, source, factors, source.ge(0))
    ordered_raw = raw.gather(-2, result.permutation[..., None].expand_as(raw))
    # Independent complex reference, not inverse/re-rotation via the component.
    phase = result.compact_positions.clamp_min(0).float()[..., None] * frequency
    unrotated_complex = torch.complex(ordered_raw[..., :4], ordered_raw[..., 4:8])
    complex_reference = unrotated_complex * torch.polar(torch.full_like(phase, 1.3), phase)
    reference = torch.cat((complex_reference.real, complex_reference.imag, ordered_raw[..., 8:]), -1)
    error = (result.keys[result.valid_mask] - reference[result.valid_mask]).abs().max()
    positions = result.question_positions(3)
    synchronized = apply_rotary(query, *factors(positions))
    logits = synchronized @ result.keys.transpose(-1, -2)
    logits = logits.masked_fill(~result.valid_mask.unsqueeze(-2), -torch.inf)
    output = logits.softmax(-1) @ result.values
    gradients = torch.autograd.grad(output.square().mean(), (raw, values, query))
    wrong_query = apply_rotary(query, *factors(torch.arange(8192, 8195, device=device)))
    wrong_logits = wrong_query @ result.keys.transpose(-1, -2)
    negative_control = (logits - wrong_logits)[result.valid_mask.unsqueeze(-2).expand_as(logits)].abs().mean()
    sorted_values = values.gather(-2, result.permutation[..., None].expand_as(values))
    values_unchanged = bool(torch.equal(result.values, sorted_values))
    tail_unchanged = bool(torch.equal(result.keys[..., 8:], ordered_raw[..., 8:]))
    gradients_valid = all(bool(torch.isfinite(g).all()) and float(g.norm()) > 0 for g in gradients)
    endpoint = bool((result.compact_positions.max(-1).values == result.anchor-1).all())
    assert float(error.detach()) < 3e-5 and values_unchanged and tail_unchanged and gradients_valid and endpoint
    assert result.question_positions(3).tolist() == [8, 9, 10]
    assert result.answer_input_positions(3, 2).tolist() == [11, 12]
    assert float(negative_control.detach()) > 1e-4
    return {"seed": seed, "metrics": {"max_reference_absolute_error": float(error.detach()),
             "values_unchanged": values_unchanged, "nonrotary_tail_unchanged": tail_unchanged,
             "heterogeneous_endpoints_aligned": endpoint, "query_and_answer_positions_synchronized": True,
             "gradient_norm_keys": float(gradients[0].norm()), "gradient_norm_values": float(gradients[1].norm()),
             "gradient_norm_queries": float(gradients[2].norm()),
             "unsynchronized_query_mean_logit_error": float(negative_control.detach())}}


def cots_diagnostic(seed: int, device: str) -> dict:
    generator = torch.Generator(device=device).manual_seed(seed)
    logits = torch.randn(8, 31, generator=generator, device=device, requires_grad=True)
    embeddings = torch.randn(31, 12, generator=generator, device=device, requires_grad=True)
    probabilities = logits.softmax(-1)
    sampled = torch.multinomial(probabilities, 1, generator=generator).squeeze(-1)
    result = competitive_token_selection(probabilities, embeddings, sampled,
                                         CotsState.initial((8,), device=device), top_k=9)
    gradients = torch.autograd.grad(result.next_embedding.square().mean(), (logits, embeddings))
    drift = (result.next_embedding-result.discrete_embedding).norm(dim=-1)
    soft_drift = (result.soft_embedding-result.discrete_embedding).norm(dim=-1)
    bound_excess = (drift-.5*soft_drift).max()
    controls = torch.tensor([1, 2, 3, 0, 0, 0, 0, 0], device=device)
    lock = competitive_token_selection(probabilities, embeddings, controls,
             CotsState.initial((8,), device=device), top_k=9,
             end_think_token_ids=(1,), protected_token_ids=(2,), eos_token_ids=(3,))
    after = competitive_token_selection(probabilities, embeddings, torch.zeros_like(controls),
                                        lock.state, top_k=9)
    phase_correct = bool((lock.effective_alpha[:3] == 0).all() and after.effective_alpha[0] == 0
                         and after.effective_alpha[1] > 0 and after.effective_alpha[2] == 0
                         and after.state.finished[2])
    assert float(result.sampled_coefficient.min().detach()) >= .5 and float(bound_excess.detach()) <= 1e-6 and phase_correct
    assert all(bool(torch.isfinite(g).all()) and float(g.norm()) > 0 for g in gradients)
    return {"seed": seed, "metrics": {"minimum_discrete_anchor_weight": float(result.sampled_coefficient.min().detach()),
             "alpha_minimum": float(result.alpha.min().detach()), "alpha_maximum": float(result.alpha.max().detach()),
             "maximum_half_drift_bound_excess": float(bound_excess.detach()), "phase_lock_and_protection_correct": phase_correct,
             "gradient_norm_logits": float(gradients[0].norm()), "gradient_norm_embeddings": float(gradients[1].norm())}}


def summarize(rows: list[dict]) -> dict:
    out = {}
    for name in rows[0]["metrics"]:
        values = [row["metrics"][name] for row in rows]
        out[name] = (all(values) if isinstance(values[0], bool) else
                     {"mean": statistics.mean(values), "std": statistics.stdev(values) if len(values)>1 else 0.,
                      "n": len(values)})
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--papers", default=",".join(KEYS))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--code-commit", help="40-hex identity for a controlled hash-bound source export; defaults to Git HEAD")
    parser.add_argument("--corpus-path", type=Path)
    parser.add_argument("--corpus-sha256")
    parser.add_argument("--corpus-id")
    parser.add_argument("--corpus-revision")
    parser.add_argument("--corpus-format", choices=("raw", "gsm8k-jsonl"), default="raw")
    parser.add_argument("--corpus-max-bytes", type=int, default=262144)
    args = parser.parse_args()
    if args.code_commit is not None and re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit) is None:
        parser.error("--code-commit must be exactly 40 hexadecimal characters")
    papers = args.papers.split(",")
    try:
        seeds = [int(s) for s in args.seeds.split(",")]
    except ValueError:
        parser.error("--seeds must contain comma-separated integers")
    if not papers or set(papers)-set(KEYS) or len(set(papers)) != len(papers):
        parser.error("select unique supported paper keys")
    if not seeds or len(set(seeds)) != len(seeds) or not 1 <= args.corpus_max_bytes <= 4_000_000:
        parser.error("unique seeds and 1..4,000,000 corpus bytes required")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA explicitly requested but unavailable; no silent CPU fallback")
    if args.output.exists():
        parser.error("choose a new immutable output path")
    if args.device == "cuda" and "novelty-patching" in papers:
        parser.error("Novelty table fitting is CPU-only; run CUDA tensor components separately")
    torch.set_num_threads(1)
    started = time.monotonic()
    commit = (args.code_commit.lower() if args.code_commit is not None else
              subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip())
    components = {}
    for key in papers:
        module = ROOT / "src/auto_research/foundation_models" / (key.replace("-", "_") + ".py")
        payload = novelty_diagnostic(args) if key == "novelty-patching" else None
        if payload is None:
            operation = rope_diagnostic if key == "rope-relay" else cots_diagnostic
            rows = [operation(seed, args.device) for seed in seeds]
            payload = {"seeds": seeds, "per_seed": rows, "metrics": summarize(rows),
                       "dataset": {"id": "synthetic-formula-tensors", "revision": "oct16-component-v1",
                                   "checkpoint": None, "capability_benchmark": False}}
        components[key] = {
            "schema_version": 2, "method": key, "adapter": None, "manifest_ref": "foundation-models:"+key,
            "implementation_status": "component_only", "evaluation_tier": "l1_mechanism",
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "measured_locally": True, "device": args.device,
            "accelerator": torch.cuda.get_device_name() if args.device == "cuda" else "CPU",
            "evaluation_protocol": {"tier": "l1_mechanism", "formal_comparison": False,
                                    "claim_policy": "formula/gradient/causality diagnostics; no model capability claim"},
            "full_experiment": {"status": "not_reproduced_high_cost", "review_done": True},
            "provenance": {"code_commit": commit,
                           "implementation_sha256": hashlib.sha256(module.read_bytes()).hexdigest(),
                           "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           "command": " ".join(["PYTHONPATH=src", "python", "scripts/"+Path(__file__).name, *sys.argv[1:]])},
            **payload,
        }
    if args.device == "cuda":
        torch.cuda.synchronize()
    result = next(iter(components.values())) if len(components) == 1 else {
        "schema_version": 2, "diagnostic_only": True, "promotion_eligible": False,
        "components": components, "elapsed_seconds": time.monotonic()-started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"papers": papers, "device": args.device, "output": str(args.output),
                      "elapsed_seconds": time.monotonic()-started}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
