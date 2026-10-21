#!/usr/bin/env python3
"""Bounded SSA and RACE formula diagnostics; no checkpoints or benchmark claims."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import time

import torch

from auto_research.foundation_models.oct21_followup_attention import (
    apply_rope, calibrate_race, fold_race_weights, native_race_attention,
    stratified_sparse_attention,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("src/auto_research/foundation_models/oct21_followup_attention.py", "scripts/run_oct21_followup_attention.py")


def run_ssa(device: str, seed: int) -> dict:
    torch.manual_seed(seed)
    q = torch.randn(8, device=device, requires_grad=True)
    k = torch.randn(64, 8, device=device, requires_grad=True)
    v = torch.randn(64, 6, device=device, requires_grad=True)
    # Synthetic noisy scores are explicit INPUTS to Alg. 1, not a claimed PQCache.
    proxy = (k.detach() @ q.detach() / math.sqrt(8)) + torch.randn(64, device=device) * 0.3
    generator = torch.Generator(device=device).manual_seed(seed)
    sparse = stratified_sparse_attention(q, k, v, proxy, 16, generator=generator)
    dense = (k @ q / math.sqrt(8)).softmax(0) @ v
    sparse.output.square().mean().backward()
    full = stratified_sparse_attention(q.detach(), k.detach(), v.detach(), proxy, 64)
    proposal = proxy.double().softmax(0)
    residual_mask = torch.ones(64, device=device, dtype=torch.bool)
    residual_mask[sparse.heavy_indices] = False
    wrong_inclusion = torch.ones_like(proposal)
    wrong_inclusion[residual_mask] = proposal[residual_mask] / proposal[residual_mask].sum()
    exact = k.detach()[sparse.selected_indices] @ q.detach() / math.sqrt(8)
    wrong_output = (exact.double() - wrong_inclusion[sparse.selected_indices].log()).softmax(0).float() @ v.detach()[sparse.selected_indices]
    metric = {"sparse_dense_l2_error": float((sparse.output.detach() - dense.detach()).norm()),
              "dense_budget_max_abs_error": float((full.output - dense.detach()).abs().max()),
              "selected_keys": sparse.selected_indices.numel(), "heavy_keys": sparse.heavy_indices.numel(),
              "residual_draws": sparse.residual_draws.numel(),
              "query_gradient_norm": float(q.grad.norm()), "value_gradient_norm": float(v.grad.norm()),
              "minimum_inclusion_probability": float(sparse.inclusion_probabilities.min()),
              "wrong_draw_probability_output_l2_gap": float((wrong_output - sparse.output.detach()).norm())}
    checks = {"finite_metrics": all(math.isfinite(value) for value in metric.values()),
              "dense_budget_parity": metric["dense_budget_max_abs_error"] < 2e-6,
              "positive_query_gradient": metric["query_gradient_norm"] > 0,
              "positive_value_gradient": metric["value_gradient_norm"] > 0,
              "budget_respected": metric["selected_keys"] <= 16,
              "wrong_probability_negative_control": metric["wrong_draw_probability_output_l2_gap"] > 1e-9}
    if not all(checks.values()):
        raise RuntimeError("SSA finite/parity checks failed")
    return {"seed": seed, "metrics": metric, "checks": checks, "selected_indices": sparse.selected_indices.tolist(),
            "dataset_sha256": hashlib.sha256(torch.cat((k.detach().flatten(), v.detach().flatten())).cpu().numpy().tobytes()).hexdigest()}


def run_race(device: str, seed: int) -> dict:
    torch.manual_seed(seed)
    x = torch.randn(24, 8, device=device, requires_grad=True)
    weights = tuple(torch.randn(8, 8, device=device) / 4 for _ in range(4))
    q, k, v = x @ weights[0], x @ weights[1], x @ weights[2]
    projection = calibrate_race(q, k, v, 4, 4, layout="split_half")
    positions = torch.arange(24, device=device)
    frequencies = torch.tensor([1.0, 0.1, 0.01, 0.001], device=device)
    folded = fold_race_weights(*weights, projection)
    result = native_race_attention(x, positions, frequencies, folded, projection)
    rq = apply_rope(q, positions, frequencies, layout="split_half")[:, projection.coordinate_ids]
    rk = apply_rope(k, positions, frequencies, layout="split_half")[:, projection.coordinate_ids]
    scores = rq @ rk.T / math.sqrt(8)
    scores = scores.masked_fill(torch.ones_like(scores, dtype=torch.bool).triu(1), -torch.inf)
    explicit = scores.softmax(-1) @ v @ projection.value_basis @ projection.value_basis.T @ weights[3]
    wrong_scaled = (scores * math.sqrt(2)).softmax(-1) @ v @ projection.value_basis @ projection.value_basis.T @ weights[3]
    commuted = apply_rope(q[:, projection.coordinate_ids], positions, frequencies[projection.pair_ids], layout="split_half")
    result.square().mean().backward()
    metric = {"folded_explicit_max_abs_error": float((result.detach() - explicit.detach()).abs().max()),
              "rope_commutation_max_abs_error": float((rq.detach() - commuted.detach()).abs().max()),
              "input_gradient_norm": float(x.grad.norm()),
              "value_basis_orthogonality_max_error": float((projection.value_basis.T @ projection.value_basis - torch.eye(4, device=device)).abs().max()),
              "retained_qk_dimension": 4, "original_qk_dimension": 8, "retained_value_dimension": 4,
              "wrong_reduced_dim_scale_output_l2_gap": float((wrong_scaled.detach() - result.detach()).norm())}
    checks = {"finite_metrics": all(math.isfinite(value) for value in metric.values()),
              "folded_explicit_parity": metric["folded_explicit_max_abs_error"] < 2e-5,
              "rope_commutation": metric["rope_commutation_max_abs_error"] < 2e-5,
              "value_basis_orthogonal": metric["value_basis_orthogonality_max_error"] < 2e-5,
              "positive_input_gradient": metric["input_gradient_norm"] > 0,
              "wrong_scale_negative_control": metric["wrong_reduced_dim_scale_output_l2_gap"] > 1e-9}
    if not all(checks.values()):
        raise RuntimeError("RACE finite/parity checks failed")
    return {"seed": seed, "metrics": metric, "checks": checks, "retained_pair_ids": projection.pair_ids.tolist(),
            "dataset_sha256": hashlib.sha256(x.detach().cpu().numpy().tobytes()).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(value) for value in args.seeds.split(",")]
    if not 1 <= len(seeds) <= 3 or len(seeds) != len(set(seeds)):
        raise SystemExit("cost gate: 1-3 distinct seeds")
    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("CUDA unavailable; CPU fallback forbidden")
    if args.output.exists():
        raise SystemExit("immutable output already exists")
    commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise SystemExit("full source commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    results = {"stratified-sparse-attention": [run_ssa(args.device, seed) for seed in seeds],
               "race-rope-compression": [run_race(args.device, seed) for seed in seeds]}
    output = {"schema_version": 2, "protocol": "oct21-followup-attention-formulas-l1-v1",
              "code_commit": commit, "device": args.device,
              "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
              "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in SOURCES},
              "evaluation_tier": "l1_mechanism", "diagnostic_only": True, "fixture_only": True,
              "promotion_eligible": False, "evolve_integrated": False, "formal_comparison": False,
              "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
              "dataset": "generated_single_head_attention_vectors_v1", "checkpoint": None,
              "pretrained_model_calls": 0, "seeds": seeds,
              "components": {key: {"per_seed": rows} for key, rows in results.items()},
              "elapsed_seconds": time.monotonic() - started}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "seconds": output["elapsed_seconds"], "seeds": seeds}))


if __name__ == "__main__":
    main()
