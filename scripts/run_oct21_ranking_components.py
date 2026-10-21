#!/usr/bin/env python3
"""Short, explicit mechanism diagnostics, never recommendation capability scores."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ["scripts/run_oct21_ranking_components.py",
           "src/auto_research/reproductions/baseline_incremental.py",
           "src/auto_research/reproductions/spar_prefix_balance.py",
           "src/auto_research/reproductions/echo_distillation.py"]


def baseline(seed):
    from auto_research.reproductions.baseline_incremental import incremental_term, value_model
    rng = np.random.default_rng(seed)
    p, b = rng.uniform(.001, .999, (2, 40))
    got = incremental_term(p, b)
    # k=1 logit gate has an independent rational-form reference.
    reference = p * p*(1-b)/(p*(1-b)+(1-p)*b)
    error = float(np.max(np.abs(got-reference)))
    hinge = incremental_term(p, b, scale="raw", magnitude="gap", sharpness=float("inf"))
    demotion = incremental_term([0, .9], [.5, .5], magnitude="constant", direction="demotion")
    raw = np.array([[.4, .9], [.6, .2]])
    increments = np.array([[0, .9], [.6, 0]])
    both = value_model(raw, increments, raw_weights=[1, .3], incremental_weights=[.8, .5])
    raw_only = value_model(raw, increments, raw_weights=[1, .3], incremental_weights=[0, 0])
    checks = {"independent_logit_reference": error < 1e-12,
              "hinge_is_positive_gap": bool(np.allclose(hinge, np.maximum(p-b, 0))),
              "demotion_does_not_vanish_at_floor": bool(demotion[0] < demotion[1] < 0),
              "raw_only_negative_control_changes_ranking": bool(np.argmax(both) != np.argmax(raw_only))}
    return {"seed": seed, "metrics": {"reference_max_error": error,
            "floor_demotion": float(demotion[0])}, "checks": checks}


def spar(seed):
    from auto_research.reproductions.spar_prefix_balance import rebalance_prefixes
    rng = np.random.default_rng(seed)
    residuals = rng.normal(size=(24, 3)) * .2
    centers = np.array([[0., 0., 0.], [6., 0., 0.], [0., 6., 0.], [0., 0., 6.]])
    original = centers.copy()
    weights = rng.integers(1, 8, 24).astype(float)
    z, reports = rebalance_prefixes(residuals, centers, np.zeros(24, dtype=int),
                                    weights, [(i//12,) for i in range(24)])
    moved = [m["item_index"] for r in reports for m in r["moves"]]
    checks = {"initial_assignments_are_nearest_centers": bool(
                  (((residuals[:, None]-centers[None])**2).sum(-1).argmin(-1) == 0).all()),
              "all_prefix_bounds_satisfied": all(max(r["loads_after"]) <= r["bound"]+1e-9 for r in reports),
              "frozen_codebook_unchanged": bool(np.array_equal(centers, original)),
              "at_most_one_move_per_item": len(set(moved)) == len(moved),
              "no_repair_negative_control_is_overloaded": all(max(r["loads_before"]) > r["bound"] for r in reports),
              "total_load_preserved": all(abs(sum(r["loads_before"])-sum(r["loads_after"])) < 1e-9 for r in reports),
              "parent_memberships_unchanged": len(z) == 24 and len(reports) == 2}
    return {"seed": seed, "metrics": {"repair_moves": len(moved),
            "max_bound_violation": max(max(r["loads_after"])-r["bound"] for r in reports)},
            "checks": checks, "prefix_reports": reports}


def echo(seed, device):
    import torch
    from auto_research.reproductions.echo_distillation import selector_losses
    torch.manual_seed(seed)
    # These are distinct user-target training samples, not test or production data.
    student = torch.nn.Parameter(torch.randn(3, 16, device=device, dtype=torch.float64))
    teacher = torch.randn_like(student, requires_grad=True)
    valid = torch.ones_like(student, dtype=torch.bool)
    valid[:, -2:] = False
    before = student.detach().clone()
    result = selector_losses(student, teacher, valid, keep=5, pairs=3,
                             temperature=2, mining_temperature=.5)
    reference = sum(-sum(float(torch.softmax(teacher[b, :14].detach()/2, 0)[j])
                    * torch.log_softmax(student[b, :14]/2, 0)[j]
                    for j in range(14)) * 4 for b in range(3)) / 3
    error = float((result["kd"]-reference).abs().detach())
    (result["kd"]+result["auxiliary"]).backward()
    gradient = student.grad.detach().clone()
    with torch.no_grad():
        student -= .05*student.grad
    identity = selector_losses(student, student.detach(), valid, keep=5, pairs=3,
                               temperature=2, mining_temperature=.5)
    half_checks = []
    for length, budget in ((2, 2), (70000, 5)):
        half_student = torch.ones(1, length, device=device, dtype=torch.float16, requires_grad=True)
        half_result = selector_losses(half_student, half_student.detach(),
                                      torch.ones_like(half_student, dtype=torch.bool), keep=budget, pairs=3)
        half_total = half_result["kd"]+half_result["auxiliary"]
        half_total.backward()
        half_checks.append(bool(torch.isfinite(half_total)) and half_result["auxiliary"].item() == 0
                           and bool(torch.isfinite(half_student.grad).all()))
    checks = {"independent_ce_reference": error < 1e-12,
              "detached_teacher_has_no_gradient": teacher.grad is None,
              "student_actually_updated": not torch.equal(before, student.detach()),
              "padding_has_zero_gradient": bool((gradient[:, -2:] == 0).all()),
              "selection_excludes_padding": bool((result["selected_indices"] < 14).all()),
              "identical_order_negative_control_has_no_boundary_pairs": identity["active_pairs"] == 0,
              "finite_losses_and_gradient": bool(torch.isfinite(gradient).all()),
              "fp16_long_history_and_empty_pairs_finite": all(half_checks)}
    return {"seed": seed, "metrics": {"kd_loss": float(result["kd"].detach()),
            "boundary_loss": float(result["auxiliary"].detach()), "active_pairs": result["active_pairs"],
            "ce_reference_max_error": error, "student_update_norm": float((student.detach()-before).norm())},
            "checks": checks}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--component", choices=("baseline-incremental", "spar-prefix-balance", "echo-selector-loss", "all"), default="all")
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output exists; keep immutable evidence")
    if args.device == "cuda":
        import torch
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA requested but unavailable; no fallback")
        accelerator = torch.cuda.get_device_name(0)
    else:
        accelerator = "CPU"
    seeds = [int(s) for s in args.seeds.split(",")]
    keys = ["baseline-incremental", "spar-prefix-balance", "echo-selector-loss"] if args.component == "all" else [args.component]
    functions = {"baseline-incremental": lambda s: baseline(s), "spar-prefix-balance": lambda s: spar(s),
                 "echo-selector-loss": lambda s: echo(s, args.device)}
    rows = {key: [functions[key](s) for s in seeds] for key in keys}
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        commit = __import__("os").environ["AUTO_RESEARCH_CODE_COMMIT"]
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": accelerator, "seeds": seeds, "diagnostic_only": True,
               "evaluation_tier": "l1_mechanism", "formal_comparison": False,
               "dataset": "synthetic-oct21-ranking-recipe-v1", "checkpoint": "none-formula-components",
               "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
               "components": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n")
    if not all(all(r["checks"].values()) for rows_ in rows.values() for r in rows_):
        raise RuntimeError("failed mechanism check; result preserved")
    print(json.dumps({"components": keys, "seeds": seeds, "checks_passed": True}))


if __name__ == "__main__":
    main()
