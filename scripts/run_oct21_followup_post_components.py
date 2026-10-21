#!/usr/bin/env python3
"""Small formula/gradient diagnostics; not a learned synthesizer or projector."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import time

import torch

from auto_research.post_training.oct21_followup_distillation import (
    a2d_candidate_opd_loss, a2d_question_reward, a2d_token_signal,
    calibrate_a2d_scale, projected_distillation_loss, verified_edit_masks,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("scripts/run_oct21_followup_post_components.py", "src/auto_research/post_training/oct21_followup_distillation.py")
METHODS = ("ask-to-distill", "projected-distillation")


def _probabilities(values):
    maximum = max(values)
    exponents = [math.exp(v - maximum) for v in values]
    total = sum(exponents)
    return [v / total for v in exponents]


def scalar_a2d_reference(student, teacher, top_k):
    """Independent Python full-vocabulary calculation for Eq. 2--5."""
    discrepancies, compatible = [], []
    for a, b in zip(student, teacher, strict=True):
        p, q = _probabilities(a), _probabilities(b)
        left = sorted(range(len(p)), key=lambda i: p[i], reverse=True)[:top_k]
        right = sorted(range(len(q)), key=lambda i: q[i], reverse=True)[:top_k]
        union = sorted(set(left + right))
        ps, qs = sum(p[i] for i in union), sum(q[i] for i in union)
        discrepancies.append(sum(q[i] / qs * math.log((q[i] / qs) / (p[i] / ps)) for i in union))
        compatible.append(sum(q[i] for i in left))
    return discrepancies, compatible


def run_a2d(device):
    logits = torch.randn(3, 6, 9, dtype=torch.float64, device=device, requires_grad=True)
    teacher = torch.randn_like(logits, requires_grad=True)
    old = logits.detach().clone().requires_grad_(True)
    mask = torch.tensor([[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0], [1, 1, 1, 0, 0, 0]], dtype=torch.bool, device=device)
    signal = a2d_token_signal(old, teacher, mask, top_k=3)
    ref = float(calibrate_a2d_scale(signal["discrepancy"], mask))
    reward, audit = a2d_question_reward(old, teacher, mask, torch.tensor([1 / 3, 2 / 3, 2 / 3], device=device),
                                        top_k=3, delta_ref=ref, response_budget=6)
    discrepancy_error, mass_error = 0., 0.
    for b in range(3):
        ds, cs = scalar_a2d_reference(old[b, mask[b]].tolist(), teacher[b, mask[b]].tolist(), 3)
        discrepancy_error = max(discrepancy_error, max(abs(float(v) - x) for v, x in zip(signal["discrepancy"][b, mask[b]], ds, strict=True)))
        mass_error = max(mass_error, max(abs(float(v) - x) for v, x in zip(signal["compatibility"][b, mask[b]], cs, strict=True)))
    loss, update = a2d_candidate_opd_loss(logits, old, teacher, mask, top_k=3)
    gradient = torch.autograd.grad(loss, logits, retain_graph=True)[0]
    ids, advantage = update["candidate_ids"], update["fixed_advantage"]
    direct = torch.zeros_like(logits).scatter_add_(-1, ids, -advantage / mask.sum())
    direct = direct - logits.detach().softmax(-1) * direct.sum(-1, keepdim=True)
    direct = torch.where(mask[..., None], direct, 0.)
    gradient_error = float((gradient - direct).abs().max())
    wrong_mass = torch.ones_like(signal["compatibility"])  # Incorrect support-renormalized teacher mass.
    negative_control = float((audit["token_score"][mask] -
                              (signal["discrepancy"][mask] / (ref + 1e-8)).clamp_max(1) * wrong_mass[mask]).abs().mean())
    initial = logits.detach().clone()
    loss.backward()
    with torch.no_grad():
        logits -= .01 * logits.grad
    if max(discrepancy_error, mass_error, gradient_error) > 1e-10 or negative_control <= 0:
        raise RuntimeError("A2D independent formula/gradient or negative control failed")
    return {"metrics": {"discrepancy_reference_max_abs_error": discrepancy_error,
                         "compatibility_reference_max_abs_error": mass_error,
                         "gradient_reference_max_abs_error": gradient_error,
                         "renormalized_teacher_mass_negative_control_difference": negative_control,
                         "reward_mean": float(reward.mean()), "delta_ref": ref,
                         "gradient_norm": float(gradient.norm()), "parameter_delta_l2": float((logits.detach() - initial).norm()),
                         "teacher_gradient_count": int(teacher.grad is not None), "old_policy_gradient_count": int(old.grad is not None)},
            "checks": {"reward_detached": not reward.requires_grad, "fixed_advantage_detached": not advantage.requires_grad,
                       "padding_zero_gradient": bool(gradient[~mask].eq(0).all())}}


def run_projected(device):
    negative_tokens, positive_tokens = [1, 2, 3, 4, 5], [1, 7, 3, 8, 5]
    neg_mask, pos_mask = verified_edit_masks(negative_tokens, positive_tokens, lambda tokens: tokens == positive_tokens)
    pos, neg = torch.randn(1, 5, 10, dtype=torch.float64, device=device, requires_grad=True), torch.randn(1, 5, 10, dtype=torch.float64, device=device, requires_grad=True)
    lp = pos.log_softmax(-1).gather(-1, torch.tensor([positive_tokens], device=device)[..., None]).squeeze(-1)
    ln = neg.log_softmax(-1).gather(-1, torch.tensor([negative_tokens], device=device)[..., None]).squeeze(-1)
    rp, rn = (lp.detach() - .2).requires_grad_(True), (ln.detach() + .1).requires_grad_(True)
    pm, nm = torch.tensor([pos_mask], device=device), torch.tensor([neg_mask], device=device)
    own = torch.tensor([[-1., -2., -3.]], dtype=torch.float64, device=device, requires_grad=True)
    loss, audit = projected_distillation_loss(lp, ln, rp, rn, pm, nm, beta=.3,
        self_correct_log_probs=own, self_correct_mask=torch.ones_like(own, dtype=torch.bool))
    gp, gn = torch.autograd.grad(loss, (lp, ln), retain_graph=True)
    margin = sum(float(lp[0, i].detach() - rp[0, i].detach()) for i in range(5) if pos_mask[i]) - sum(float(ln[0, i].detach() - rn[0, i].detach()) for i in range(5) if neg_mask[i])
    expected_loss = math.log1p(math.exp(-.3 * margin)) + 6
    coefficient = -.3 / (1 + math.exp(.3 * margin))
    gradient_error = max(float((gp - pm.to(gp.dtype) * coefficient).abs().max()),
                         float((gn + nm.to(gn.dtype) * coefficient).abs().max()))
    # Incorrect full-sequence contrast must differ even when most text is retained.
    wrong_margin = float(((lp - rp).sum() - (ln - rn).sum()).detach())
    negative_control = abs(margin - wrong_margin)
    loss.backward()
    if gradient_error > 1e-12 or abs(float(loss.detach()) - expected_loss) > 1e-12 or negative_control <= 0:
        raise RuntimeError("Projected Distillation scalar/gradient audit failed")
    return {"metrics": {"loss_reference_abs_error": abs(float(loss.detach()) - expected_loss),
                         "gradient_reference_max_abs_error": gradient_error,
                         "full_sequence_negative_control_margin_difference": negative_control,
                         "positive_logit_gradient_norm": float(pos.grad.norm()), "negative_logit_gradient_norm": float(neg.grad.norm()),
                         "reference_gradient_count": int(rp.grad is not None) + int(rn.grad is not None),
                         "self_correct_gradient_abs_error": float((own.grad + 1).abs().max()),
                         "changed_positive_tokens": sum(pos_mask), "changed_negative_tokens": sum(neg_mask),
                         "self_correct_sft_loss": float(audit["self_correct_sft_loss"])},
            "checks": {"unchanged_gathered_token_gradient_zero": bool(gp[~pm].eq(0).all() and gn[~nm].eq(0).all()),
                       "projector_not_executed": True, "supplied_fixture_not_language_capability": True}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-commit", help="frozen source commit when remote checkout has no .git")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        seeds = [int(v) for v in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not seeds or len(seeds) > 3 or len(set(seeds)) != len(seeds) or any(s < 0 or s >= 2 ** 32 for s in seeds):
        parser.error("one to three distinct seeds in [0,2**32) required")
    if args.output.exists():
        parser.error("immutable output exists")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("requested CUDA unavailable; no CPU fallback")
    commit = args.source_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        parser.error("full lowercase 40-hex source commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    result = {"schema_version": 2, "device": args.device, "seeds": seeds,
              "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
              "code_commit": commit,
              "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES},
              "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
              "no_pretrained_model_calls": True, "pretrained_checkpoint": None,
              "dataset": "synthetic-logit-and-edit-fixtures", "dataset_revision": "oct21-followup-post-v1",
              "full_experiment_status": "not_reproduced_high_cost", "components": {}}
    for key, run in ((METHODS[0], run_a2d), (METHODS[1], run_projected)):
        rows = []
        for seed in seeds:
            torch.manual_seed(seed)
            row = {"seed": seed, **run(args.device)}
            if not all(math.isfinite(v) for v in row["metrics"].values()) or not all(row["checks"].values()):
                raise RuntimeError("nonfinite metric or failed diagnostic check")
            rows.append(row)
        result["components"][key] = {"per_seed": rows}
    if args.device == "cuda":
        torch.cuda.synchronize()
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "device": args.device, "seeds": seeds}))


if __name__ == "__main__":
    main()
