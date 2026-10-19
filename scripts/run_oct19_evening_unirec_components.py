#!/usr/bin/env python3
"""Bounded UniRec-v3 objective diagnostics; no production/RecFlow experiment."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import statistics
import subprocess
import time

import torch
from torch.nn import functional as F

from auto_research.reproductions.unirec.v3_objectives import (
    agrr_loss, confidence_pairs, cppa_loss, cross_stage_alignment, evidence_rewards,
    preference_evidence, quantile_groups,
)

ROOT = Path(__file__).resolve().parents[1]


def diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    predictions = torch.randn(8, 3, device=device, dtype=torch.float64)
    predictions[1, 0] = predictions[0, 0]  # exact ties exclude this objective only
    weights = predictions.new_tensor([.7, 1.2, .4])
    scores = torch.nn.Parameter(torch.randn(8, device=device, dtype=torch.float64))
    positive, negative = preference_evidence(predictions, weights)
    actual = cppa_loss(scores, positive, negative)
    reference = scores.sum() * 0
    for i in range(8):
        for j in range(8):
            for m in range(3):
                direction = float(torch.sign(predictions[i, m] - predictions[j, m]))
                if direction:
                    reference = reference + weights[m] * F.softplus(-direction * (scores[i] - scores[j]))
    gradient = torch.autograd.grad(actual, scores, retain_graph=True)[0]
    expected_gradient = torch.autograd.grad(reference, scores, retain_graph=True)[0]
    value_error = abs(float((actual - reference).detach()))
    gradient_error = float((gradient - expected_gradient).abs().max())
    no_pruning = cppa_loss(scores, positive, negative, pair_mask=confidence_pairs(positive, negative, 7))
    no_pruning_error = abs(float((actual - no_pruning).detach()))
    mask = confidence_pairs(positive, negative, 2)
    selected = {(i, j) for i in range(8) for j in sorted((j for j in range(8) if i != j),
                     key=lambda j: (-float(abs(positive[i, j] - negative[i, j])), j))[:2]}
    pair_error = sum(bool(mask[i, j]) != ((i, j) in selected) for i in range(8) for j in range(8))
    wrong = (positive - negative).abs() * F.softplus(-torch.sign(positive - negative)
                                                    * (scores[:, None] - scores[None, :]))
    majority_negative = abs(float((actual - wrong.sum()).detach()))
    rewards = evidence_rewards(positive, negative, epsilon=.01)
    oracle_rewards = scores.new_tensor([sum(float(positive[i, j] - negative[i, j]) for j in range(8))
                     / sum(float(positive[i, j] + negative[i, j]) + .01 for j in range(8)) for i in range(8)])
    reward_error = float((rewards - oracle_rewards).abs().max())
    groups = quantile_groups(scores.new_tensor([0., 0., 1., 1., 2., 2., 3., 3.]), 2)
    regularizer = agrr_loss(scores, rewards, groups, temperature=.8)
    kl_reference = scores.sum() * 0
    for group in torch.unique(groups):
        ids = torch.where(groups == group)[0]
        local = [float(rewards[i]) for i in ids]
        mean = statistics.mean(local)
        std = statistics.pstdev(local)
        advantage = scores.new_tensor([max(-5., min(5., (x - mean) / max(std, .001))) / .8 for x in local])
        q = torch.softmax(advantage, 0)
        kl_reference = kl_reference + (q * (q.log() - F.log_softmax(scores[ids], 0))).sum()
    kl_reference = kl_reference / len(torch.unique(groups))
    kl_error = abs(float((regularizer - kl_reference).detach()))
    shift_error = abs(float((regularizer - agrr_loss(scores + 100 * groups, rewards, groups, temperature=.8)).detach()))
    rank = torch.nn.Parameter(torch.randn(4, device=device, dtype=torch.float64))
    aligned = cross_stage_alignment(scores[:4], rank)
    rank_gradient = torch.autograd.grad(aligned, rank, allow_unused=True, retain_graph=True)[0]
    loss = cppa_loss(scores, positive, negative, pair_mask=mask) + regularizer + .1 * aligned
    before = scores.detach().clone()
    loss.backward()
    torch.optim.SGD([scores], lr=.01).step()
    update = float((scores - before).norm().detach())
    max_error = max(value_error, gradient_error, no_pruning_error, reward_error, kl_error, shift_error)
    assert max_error < 1e-10 and pair_error == 0 and majority_negative > 1e-3 and update > 0 and rank_gradient is None
    return {"cppa_value_reference_max_error": value_error, "cppa_gradient_reference_max_error": gradient_error,
            "no_pruning_equivalence_max_error": no_pruning_error, "capp_pair_reference_errors": pair_error,
            "directed_pairs": int(mask.sum()), "majority_collapse_negative_control_difference": majority_negative,
            "reward_reference_max_error": reward_error, "agrr_kl_reference_max_error": kl_error,
            "group_shift_invariance_max_error": shift_error, "ranking_target_gradient_blocked": rank_gradient is None,
            "score_gradient_norm": float(scores.grad.norm()), "score_update_norm": update, "optimizer_steps": 1}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    seeds = [int(value) for value in args.seeds.split(",")]
    if not seeds or len(set(seeds)) != len(seeds) or any(not 0 <= s < 2**32 for s in seeds) or len(seeds) > 8:
        parser.error("1..8 unique uint32 seeds required")
    if args.code_commit and not re.fullmatch(r"[0-9a-f]{40}", args.code_commit):
        parser.error("full lowercase commit required")
    if args.output.exists():
        parser.error("output immutable; select fresh path")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no fallback")
    torch.set_num_threads(1)
    start = time.monotonic()
    rows = [{"seed": seed, "metrics": diagnostic(seed, args.device)} for seed in seeds]
    metrics = {key: statistics.mean(float(r["metrics"][key]) for r in rows) for key in rows[0]["metrics"]
               if type(rows[0]["metrics"][key]) in (int, float)}
    sources = [Path(__file__).resolve(), ROOT / "src/auto_research/reproductions/unirec/v3_objectives.py"]
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.device == "cuda":
        torch.cuda.synchronize()
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU", "seeds": seeds,
               "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
               "components": {"unirec-v3-components": {"dataset": {"id": "synthetic-unirec-v3-objective-fixture",
                   "revision": "oct19-evening-unirec-v3-v1", "capability_benchmark": False}, "per_seed": rows,
                   "metrics": metrics, "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
                   "full_experiment_status": "not_reproduced_high_cost"}},
               "elapsed_seconds": time.monotonic() - start,
               "executed_source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "components": list(payload["components"]), "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
