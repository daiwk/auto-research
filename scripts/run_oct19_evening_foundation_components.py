#!/usr/bin/env python3
"""Seconds-scale EgoP2C/BMuon/Sink-Sparse definition diagnostics; no downloads."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import time

import torch
from torch import nn
from torch.nn import functional as F

from auto_research.foundation_models.bmuon import BudgetMuon, polar
from auto_research.foundation_models.ego_p2c import (
    ROLES, RoleDecoder, SegmentScores, role_context, sample_segment, score_segment, segment_mopd_loss,
)
from auto_research.foundation_models.sink_sparse import calibrate_sink_mask, hybrid_attention

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"ego-p2c": "ego_p2c", "bmuon": "bmuon", "sink-sparse": "sink_sparse"}
RECIPE = "oct19-evening-foundation-mechanisms-v1"


def _norm(parameters) -> float:
    return math.sqrt(sum(float(p.grad.detach().square().sum()) for p in parameters if p.grad is not None))


def ego_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    student = RoleDecoder().to(device=device, dtype=torch.float64)
    student.enable_general_residual()
    teachers = {r: copy.deepcopy(student).requires_grad_(False).eval() for r in ROLES}
    with torch.no_grad():
        # Random frozen specialist distributions, NOT trained teacher ability.
        for index, teacher in enumerate(teachers.values()):
            teacher.head.weight.add_(torch.randn_like(teacher.head.weight) * (.07 + .03 * index))
    generator = torch.Generator(device=device).manual_seed(seed + 100)
    video, question, options = (3, 4, 5), (8, 9), (10, 11)
    planner = role_context("PC", video=video, question=question, options=options)
    mode = sample_segment(student, planner, steps=2, generator=generator)
    perception_context = role_context("V", video=video, subquestion=mode.tokens)
    observation = sample_segment(student, perception_context, steps=3, generator=generator)
    composition = sample_segment(student, role_context("PC", video=video, question=question, options=options,
                                                       history=mode.tokens + observation.tokens), steps=3, generator=generator)
    direct_mode = sample_segment(student, planner, steps=1, generator=generator)
    direct = sample_segment(student, role_context("G", video=video, question=question, options=options), steps=3, generator=generator)
    # Fixed PLAN/DIRECT skeletons: segment tokens are live on-policy samples.
    # This does not implement learned tool-call parsing or free-form interaction.
    trajectories = [(mode, observation, composition), (direct_mode, direct)]
    records, losses, reference_losses, negative_losses, expected_gradients = [], [], [], [], []
    old_current_error = 0.
    for trajectory in trajectories:
        counts = {r: sum(len(s.tokens) for s in trajectory if s.context.role == r) for r in ROLES}
        scores, wrong_scores, row = [], [], []
        reference = 0.
        for segment in trajectory:
            r = segment.context.role
            ids = torch.tensor(segment.tokens, device=device)
            logits = score_segment(student, segment)
            logits.retain_grad()
            current = logits.log_softmax(-1).gather(-1, ids[:, None]).squeeze(-1)
            old_current_error = max(old_current_error, float((current.detach() - segment.rollout_log_probs).abs().max()))
            with torch.no_grad():
                teacher_logits = score_segment(teachers[r], segment)
                teacher_logp = teacher_logits.log_softmax(-1).gather(-1, ids[:, None]).squeeze(-1)
                wrong_role = "PC" if r != "PC" else "V"
                # Same permitted context; negative changes teacher identity only.
                wrong_logp = score_segment(teachers[wrong_role], segment).log_softmax(-1).gather(-1, ids[:, None]).squeeze(-1)
            scores.append(SegmentScores(r, current, teacher_logp, segment.rollout_log_probs))
            wrong_scores.append(SegmentScores(r, current, wrong_logp, segment.rollout_log_probs))
            advantage = (teacher_logp - segment.rollout_log_probs).clamp(-5, 5)
            expected = -.5 * (advantage / counts[r])[:, None] * (F.one_hot(ids, 32) - logits.detach().softmax(-1))
            expected_gradients.append((logits, expected))
            # Independent scalar full-vocabulary normalization and role counts.
            scalar_current = []
            for values, token in zip(logits.detach().cpu().tolist(), segment.tokens, strict=True):
                maximum = max(values)
                scalar_current.append(values[token] - maximum - math.log(sum(math.exp(v - maximum) for v in values)))
            reference -= sum(float(a) * lp for a, lp in zip(advantage.cpu().tolist(), scalar_current, strict=True)) / counts[r]
            row.append({"role": r, "visible_fields": list(segment.context.visible_fields),
                        "video_tokens": list(segment.context.video), "text_context": list(segment.context.text),
                        "sampled_tokens": list(segment.tokens), "old_log_probs": segment.rollout_log_probs.cpu().tolist(),
                        "current_log_probs": current.detach().cpu().tolist(), "teacher_log_probs": teacher_logp.cpu().tolist(),
                        "clipped_advantage": advantage.cpu().tolist(), "teacher_role": r, "role_token_count": counts[r]})
        losses.append(segment_mopd_loss(scores))
        negative_losses.append(segment_mopd_loss(wrong_scores))
        reference_losses.append(reference)
        records.append(row)
    loss = torch.stack(losses).mean()
    before = {name: p.detach().clone() for name, p in student.named_parameters()}
    loss.backward()
    gradient_error = max(float((logits.grad - expected).abs().max()) for logits, expected in expected_gradients)
    trainable = [p for p in student.parameters() if p.requires_grad]
    gradient_norm = _norm(trainable)
    teacher_gradient = sum(_norm(teacher.parameters()) for teacher in teachers.values())
    frozen_gradient = _norm(p for p in student.parameters() if not p.requires_grad)
    torch.optim.SGD(trainable, lr=.02).step()
    update = math.sqrt(sum(float((p.detach() - before[name]).square().sum()) for name, p in student.named_parameters()))
    frozen_update = max(float((p.detach() - before[name]).abs().max()) for name, p in student.named_parameters() if not p.requires_grad)
    forbidden_rejected = 0
    try:
        role_context("V", video=video, subquestion=mode.tokens, options=options)
    except ValueError:
        forbidden_rejected = 1
    metrics = {"loss": float(loss.detach()), "loss_reference_max_error": abs(float(loss.detach()) - statistics.mean(reference_losses)),
               "logit_gradient_reference_max_error": gradient_error, "rollout_rescore_max_error": old_current_error,
               "trainable_gradient_norm": gradient_norm, "parameter_update_norm": update,
               "teacher_gradient_norm": teacher_gradient, "frozen_gradient_norm": frozen_gradient,
               "frozen_parameter_update_max": frozen_update, "perception_private_context_rejected": forbidden_rejected,
               "wrong_teacher_loss_absolute_delta": abs(float(torch.stack(negative_losses).mean().detach() - loss.detach()))}
    if max(metrics["loss_reference_max_error"], gradient_error, old_current_error) > 1e-10 or min(gradient_norm, update) <= 0:
        raise RuntimeError("EgoP2C reference/gradient diagnostic failed")
    if teacher_gradient != 0 or frozen_gradient != 0 or frozen_update != 0 or forbidden_rejected != 1:
        raise RuntimeError("EgoP2C isolation/freeze contract failed")
    return {"metrics": metrics, "audit": {"trajectories": records, "protocol_skeleton_is_fixed": True,
                                            "teacher_is_random_frozen_not_trained": True,
                                            "full_loss_reference": reference_losses}}


def _eigen_polar(matrix: torch.Tensor) -> torch.Tensor:
    values, vectors = torch.linalg.eigh(matrix.T @ matrix)
    threshold = 1e-11 * max(1., float(values.max()))
    inverse = torch.where(values > threshold, values.clamp_min(threshold).rsqrt(), 0.)
    return matrix @ ((vectors * inverse) @ vectors.T)


def _scalar_allocation(scores: list[float], budget: float, floor: float) -> list[float]:
    # alpha=1/2 only in this independent recipe: mu=clip(c*a^2).
    lo, hi = 0., 1.
    while sum(min(1., max(floor, hi * a * a)) for a in scores) < budget:
        hi *= 2
    for _ in range(100):
        midpoint = (lo + hi) / 2
        result = [min(1., max(floor, midpoint * a * a)) for a in scores]
        if sum(result) > budget:
            hi = midpoint
        else:
            lo = midpoint
    return result


def bmuon_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    blocks = [(nn.Parameter(torch.randn(4, 3, device=device, dtype=torch.float64)),
               nn.Parameter(torch.randn(2, 4, device=device, dtype=torch.float64))),
              (nn.Parameter(torch.randn(3, 2, device=device, dtype=torch.float64)),
               nn.Parameter(torch.randn(2, 3, device=device, dtype=torch.float64)))]
    optimizer = BudgetMuon(blocks, budget=2.8, lr=.01, momentum=.9, allocation_period=5)
    inputs = [torch.randn(5, left.shape[1], device=device, dtype=torch.float64) for left, _ in blocks]
    targets = [torch.randn(5, right.shape[0], device=device, dtype=torch.float64) for _, right in blocks]
    loss = sum((F.linear(F.gelu(F.linear(x, left)), right) - y).square().mean()
               for (left, right), x, y in zip(blocks, inputs, targets, strict=True))
    loss.backward()
    gradient_norm = _norm(p for pair in blocks for p in pair)
    before = [p.detach().clone() for pair in blocks for p in pair]
    # First Nesterov step: B=G, M=G+beta*B.
    momenta = [(left.grad.detach() * 1.9, right.grad.detach() * 1.9) for left, right in blocks]
    old_mu = optimizer.allocations
    scores, objective_before = [], 0.
    for (m1, m2), mu in zip(momenta, old_mu, strict=True):
        d = torch.diag(mu.sqrt())
        p1, p2 = _eigen_polar(d @ m1), _eigen_polar(m2 @ d)
        scores.extend(((m1 * p1).sum(1) + (m2 * p2).sum(0)).cpu().tolist())
        objective_before += float(torch.linalg.svdvals(d @ m1).sum() + torch.linalg.svdvals(m2 @ d).sum())
    allocation_reference = _scalar_allocation(scores, 2.8, 1e-6)
    optimizer.step()
    allocation = torch.cat(optimizer.allocations)
    allocation_error = float((allocation - allocation.new_tensor(allocation_reference)).abs().max())
    update_reference, objective_after, unweighted_difference = [], 0., 0.
    for (m1, m2), mu in zip(momenta, optimizer.allocations, strict=True):
        d = torch.diag(mu.sqrt())
        updates = d @ _eigen_polar(d @ m1), _eigen_polar(m2 @ d) @ d
        update_reference.extend(updates)
        objective_after += float(torch.linalg.svdvals(d @ m1).sum() + torch.linalg.svdvals(m2 @ d).sum())
        unweighted_difference += float((updates[0] - polar(m1)).square().sum() + (updates[1] - polar(m2)).square().sum())
    params = [p for pair in blocks for p in pair]
    update_error = max(float((p.detach() - (old - .01 * expected)).abs().max())
                       for p, old, expected in zip(params, before, update_reference, strict=True))
    update_norm = math.sqrt(sum(float((p.detach() - old).square().sum()) for p, old in zip(params, before, strict=True)))
    metrics = {"loss": float(loss.detach()), "gradient_norm": gradient_norm, "parameter_update_norm": update_norm,
               "allocation_reference_max_error": allocation_error, "parameter_update_reference_max_error": update_error,
               "global_budget_absolute_error": abs(float(allocation.sum()) - 2.8),
               "mm_objective_gain": objective_after - objective_before,
               "ordinary_muon_direction_difference_norm": math.sqrt(unweighted_difference),
               "allocation_min": float(allocation.min()), "allocation_max": float(allocation.max())}
    if max(allocation_error, update_error, metrics["global_budget_absolute_error"]) > 1e-9 or objective_after < objective_before - 1e-9:
        raise RuntimeError("BMuon independent oracle or MM monotonicity failed")
    if min(gradient_norm, update_norm, unweighted_difference) <= 0:
        raise RuntimeError("BMuon update/negative control degenerate")
    return {"metrics": metrics, "audit": {"global_budget": 2.8, "alpha": .5, "floor": 1e-6,
                                            "scores": scores, "old_allocation": torch.cat(old_mu).cpu().tolist(),
                                            "allocation": allocation.cpu().tolist(), "scalar_reference": allocation_reference,
                                            "mm_objective_before": objective_before, "mm_objective_after": objective_after,
                                            "polar_implementation": "exact_svd_not_five_step_kernel"}}


def sink_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    def queries(count):
        q, k = [torch.randn(count, 2, 12, 4, device=device, dtype=torch.float64) * .4 for _ in range(2)]
        q[..., 0] += 3.
        k[:, :, :3, 0] += 2.
        return q, k
    calibration_q, calibration_k = queries(6)
    mask = calibrate_sink_mask(calibration_q, calibration_k, block_size=3, coverage=.8)
    frozen_mask = mask.blocks.clone()
    q, k = queries(2)  # fresh observations, excluded from offline mask calibration
    q, k = nn.Parameter(q), nn.Parameter(k)
    v = nn.Parameter(torch.randn(2, 2, 12, 5, device=device, dtype=torch.float64))
    actual, details = hybrid_attention(q, k, v, mask, pool_gap=3)
    dense_logits = q @ k.transpose(-1, -2) / 2
    expanded = mask.blocks.repeat_interleave(3, -2).repeat_interleave(3, -1)
    exact = dense_logits.masked_fill(~expanded[None], -torch.inf)
    pooled_k = k.reshape(2, 2, 4, 3, 4).mean(3)
    pooled_v = v.reshape(2, 2, 4, 3, 5).mean(3)
    # Single softmax on a virtual union, independent of separate branch fusion.
    union = torch.cat((exact, q @ pooled_k.transpose(-1, -2) / 2 + math.log(3)), -1)
    oracle = union.softmax(-1) @ torch.cat((v, pooled_v), -2)
    error = float((actual - oracle).abs().max().detach())
    target = torch.randn_like(actual)
    loss = (actual - target).square().mean()
    reference_loss = (oracle - target).square().mean()
    gradients = torch.autograd.grad(loss, (q, k, v), retain_graph=True)
    reference_gradients = torch.autograd.grad(reference_loss, (q, k, v))
    gradient_error = max(float((a - b).abs().max()) for a, b in zip(gradients, reference_gradients, strict=True))
    gradient_norm = math.sqrt(sum(float(g.square().sum()) for g in gradients))
    old = [p.detach().clone() for p in (q, k, v)]
    with torch.no_grad():
        for parameter, gradient in zip((q, k, v), gradients, strict=True):
            parameter.add_(gradient, alpha=-.01)
    update = math.sqrt(sum(float((p.detach() - before).square().sum()) for p, before in zip((q, k, v), old, strict=True)))
    naive = .5 * (details["sink"] + details["compensation"])
    wrong_alpha = (details["sink_lse"] - details["compensation_lse"]).sigmoid()
    wrong = wrong_alpha[..., None] * details["sink"] + (1 - wrong_alpha[..., None]) * details["compensation"]
    dense = dense_logits.detach().softmax(-1) @ old[2]
    metrics = {"loss": float(loss.detach()), "virtual_union_reference_max_error": error,
               "gradient_reference_max_error": gradient_error, "gradient_norm": gradient_norm,
               "parameter_update_norm": update, "sink_block_density": float(mask.blocks.double().mean()),
               "heldout_dense_output_rmse": float((actual.detach() - dense.detach()).square().mean().sqrt()),
               "fixed_average_negative_max_difference": float((actual - naive).abs().max().detach()),
               "missing_pool_correction_negative_max_difference": float((actual - wrong).abs().max().detach()),
               "calibration_mask_mutation_count": int((mask.blocks != frozen_mask).sum())}
    if max(error, gradient_error) > 1e-10 or min(gradient_norm, update) <= 0 or metrics["calibration_mask_mutation_count"] != 0:
        raise RuntimeError("Sink-Sparse reference, gradient or calibration isolation failed")
    return {"metrics": metrics, "audit": {"calibration_observations": 6, "heldout_observations": 2,
                                            "coverage": .8, "block_size": 3, "pool_gap": 3,
                                            "static_mask": mask.blocks.cpu().tolist(),
                                            "calibration_mean_block_mass": mask.mean_block_mass.cpu().tolist(),
                                            "heldout_alpha": details["alpha"].detach().cpu().tolist(),
                                            "pooled_support_includes_sink_blocks": True}}


def summarize(rows: list[dict]) -> dict:
    return {key: {"mean": statistics.mean(values := [row["metrics"][key] for row in rows]),
                  "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
            for key in rows[0]["metrics"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(MODULES))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    methods = args.methods.split(",")
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(MODULES):
        parser.error("select unique supported methods")
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8 or any(not 0 <= s < 2 ** 32 for s in seeds):
        parser.error("1..8 unique seeds in [0,2**32) required")
    if args.code_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit):
        parser.error("full hexadecimal commit required")
    if args.output.exists():
        parser.error("output immutable; choose a fresh path")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no CPU fallback")
    torch.set_num_threads(1)
    start = time.monotonic()
    operations = {"ego-p2c": ego_diagnostic, "bmuon": bmuon_diagnostic, "sink-sparse": sink_diagnostic}
    components = {}
    for method in methods:
        rows = [{"seed": seed, **operations[method](seed, args.device)} for seed in seeds]
        components[method] = {"dataset": {"id": "synthetic-role-decoder-mlp-attention", "revision": RECIPE,
                                           "checkpoint": None, "capability_benchmark": False},
                              "per_seed": rows, "metrics": summarize(rows), "diagnostic_only": True,
                              "evaluation_tier": "l1_mechanism", "promotion_eligible": False, "evolve_integrated": False,
                              "full_experiment_status": "not_reproduced_high_cost", "review_done": True}
    sources = [Path(__file__).resolve()] + [ROOT / f"src/auto_research/foundation_models/{MODULES[key]}.py" for key in methods]
    commit = args.code_commit.lower() if args.code_commit else subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.device == "cuda":
        torch.cuda.synchronize()
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU", "seeds": seeds,
               "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
               "components": components, "elapsed_seconds": time.monotonic() - start,
               "executed_source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
