#!/usr/bin/env python3
"""Bounded FPoT/LAMP operator diagnostics, without checkpoint/data downloads."""
from __future__ import annotations

import argparse
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

from auto_research.foundation_models.fpot import (
    FPoTCodes, dequantize, integer_accumulate, quantize_weights, straight_through_weights,
)
from auto_research.foundation_models.lamp import (
    FeatureBatch, LampPredictor, Mixture, evaluate_test, select_mixture, vit_regions,
)

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"fpot": "fpot", "lamp": "lamp"}


def scalar_quantization_reference(weight: torch.Tensor, *, approximate: bool) -> torch.Tensor:
    """Independent Python scalar enumeration over all clipping/phase candidates."""
    rows = []
    for row in weight.detach().cpu().tolist():
        best_error, best_values = math.inf, None
        maximum = max(abs(x) for x in row)
        for ratio in (.7, .8, .9, 1.):
            for phase in range(16):
                scale = (ratio * maximum / 8 if maximum else 1.) * 2 ** (phase / 16)
                values = []
                for raw in row:
                    normalized = abs(raw) / scale
                    if normalized < 2 ** (-.25):
                        values.append(0.)
                        continue
                    if approximate:
                        grid = [2 ** (e // 2) * (1.5 if e % 2 else 1.) for e in range(7)]
                        exponent = min(range(7), key=lambda e: abs(normalized - grid[e]))
                        magnitude = grid[exponent]
                    else:
                        exponent = min(6, max(0, round(2 * math.log2(normalized))))
                        magnitude = 2 ** (exponent / 2)
                    values.append(math.copysign(scale * magnitude, raw))
                error = sum((x - y) ** 2 for x, y in zip(row, values, strict=True)) / len(row)
                if error < best_error:
                    best_error, best_values = error, values
        rows.append(best_values)
    return weight.new_tensor(rows)


def fpot_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    weight = nn.Parameter(torch.randn(6, 16, device=device, dtype=torch.float64))
    codes = quantize_weights(weight)
    reconstruction = dequantize(codes)
    oracle = scalar_quantization_reference(weight, approximate=True)
    error = float((reconstruction - oracle).abs().max())
    unaligned = dequantize(quantize_weights(weight, phase_steps=1))
    phase_gain = float(((unaligned - weight).square().mean() - (reconstruction - weight).square().mean()).detach())
    exact = quantize_weights(weight, approximate=False)
    # Negative: calibrate the exact sqrt(2) grid, then change its odd coefficient.
    posthoc = dequantize(FPoTCodes(exact.signs, exact.magnitudes, exact.scales, 4, 2, True))
    negative = float((posthoc - reconstruction).abs().max())
    mse_gain = float(((posthoc - weight).square().mean() - (reconstruction - weight).square().mean()).detach())
    activations = torch.randint(-7, 8, (8, 16), device=device, dtype=torch.int64)
    accumulated = integer_accumulate(activations, codes)
    signs, magnitudes = codes.signs.cpu().tolist(), codes.magnitudes.cpu().tolist()
    integer_reference, wrong_codes = [], []
    for row in activations.cpu().tolist():
        output, wrong = [], []
        for sign_row, magnitude_row in zip(signs, magnitudes, strict=True):
            total, wrong_total = 0, 0
            for x, sign, magnitude in zip(row, sign_row, magnitude_row, strict=True):
                if magnitude:
                    exponent = magnitude - 1
                    shifted = x * 2 ** (exponent // 2)
                    total += sign * (shifted if exponent % 2 == 0 else shifted + shifted // 2)
                    incorrect = x * 2 ** (magnitude // 2)
                    wrong_total += sign * (incorrect if magnitude % 2 == 0 else incorrect + incorrect // 2)
            output.append(total)
            wrong.append(wrong_total)
        integer_reference.append(output)
        wrong_codes.append(wrong)
    integer_error = int((accumulated - accumulated.new_tensor(integer_reference)).abs().max())
    code_negative = int((accumulated - accumulated.new_tensor(wrong_codes)).abs().max())
    inputs = torch.randn(5, 16, device=device, dtype=torch.float64)
    target = torch.randn(5, 6, device=device, dtype=torch.float64)
    prediction = F.linear(inputs, straight_through_weights(weight, codes))
    loss = (prediction - target).square().mean()
    before = weight.detach().clone()
    loss.backward()
    grad_reference = (2 / prediction.numel()) * (prediction.detach() - target).T @ inputs
    grad_error = float((weight.grad - grad_reference).abs().max())
    gradient = float(weight.grad.norm())
    torch.optim.SGD([weight], lr=.01).step()
    update = float((weight - before).norm().detach())
    assert error < 1e-10 and integer_error == 0 and grad_error < 1e-10
    assert negative > 1e-4 and code_negative > 0 and gradient > 0 and update > 0
    assert phase_gain >= -1e-12 and mse_gain >= -1e-12
    return {"approximate_grid_reference_max_error": error, "integer_shift_add_reference_max_error": integer_error,
            "magnitude_without_minus_one_negative_control_error": code_negative,
            "posthoc_grid_negative_control_difference": negative, "approx_grid_mse_gain_over_posthoc": mse_gain,
            "phase_search_mse_gain": phase_gain, "ste_gradient_reference_max_error": grad_error,
            "weight_gradient_norm": gradient, "weight_update_norm": update, "optimizer_steps": 1}


def _features(prefix: str, patches: torch.Tensor, layers: nn.ModuleList, projection: nn.Module) -> FeatureBatch:
    regions = []
    with torch.no_grad():
        value = patches
        for layer in layers:
            value = torch.tanh(layer(value))
            regions.append(vit_regions(value))
        global_features = F.normalize(projection(value.mean((1, 2))), dim=-1)
    return FeatureBatch(global_features, tuple(regions), tuple(f"{prefix}-{i}" for i in range(len(patches))))


def lamp_scalar_kernel_reference(model: LampPredictor, query: FeatureBatch) -> tuple[torch.Tensor, ...]:
    """Scalar regional all-pairs and support centering, independent of einsum."""
    result = []
    sg, qg = model.support.global_features, query.global_features
    result.append(torch.stack([torch.stack([torch.exp(-model.beta * (1 - torch.dot(q, s))) for s in sg]) for q in qg]))
    for index, (queries, supports) in enumerate(zip(query.regional_features, model.support.regional_features, strict=True)):
        def affinity(a, b):
            return sum(torch.exp(-model.regional_beta * (1 - torch.dot(x, y))) for x in a for y in b) / 16
        def kernel(a, b):
            return affinity(a, b) / torch.sqrt(affinity(a, a) * affinity(b, b))
        support_gram = torch.stack([torch.stack([kernel(a, b) for b in supports]) for a in supports])
        mean = support_gram.mean(1)
        grand = support_gram.mean()
        rows = []
        for q in queries:
            raw = torch.stack([kernel(q, s) for s in supports])
            mq = raw.mean()
            rows.append((raw - mq - mean + grand) / torch.sqrt((1 - 2 * mq + grand).clamp_min(1e-10)
                        * (1 - 2 * mean + grand).clamp_min(1e-10)))
        result.append(torch.stack(rows))
    return tuple(result)


def lamp_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    layers = nn.ModuleList([nn.Linear(8, 5), nn.Linear(5, 7), nn.Linear(7, 9)]).to(device=device, dtype=torch.float64)
    projection = nn.Linear(9, 6).to(device=device, dtype=torch.float64)
    for parameter in (*layers.parameters(), *projection.parameters()):
        parameter.requires_grad_(False)
    frozen_before = [p.detach().clone() for p in (*layers.parameters(), *projection.parameters())]
    support = _features("support", torch.randn(12, 4, 4, 8, device=device, dtype=torch.float64), layers, projection)
    validation = _features("validation", torch.randn(6, 4, 4, 8, device=device, dtype=torch.float64), layers, projection)
    test = _features("test", torch.randn(5, 4, 4, 8, device=device, dtype=torch.float64), layers, projection)
    labels = torch.arange(3, device=device).repeat_interleave(4)
    text = F.normalize(torch.randn(3, 6, device=device, dtype=torch.float64), dim=-1)
    model = LampPredictor(support, labels, text, regularization=.7, global_bandwidth=1.3,
                          support_image_ids=tuple(f"image-{i // 2}" for i in range(12)))
    candidates = (Mixture(0., (1 / 3,) * 3), Mixture(.5, (.2, .3, .5)), Mixture(1., (.5, .25, .25)))
    validation_labels = torch.tensor([0, 2, 1, 0, 1, 2], device=device)
    mixture, validation_score = select_mixture(model, validation, validation_labels, candidates)
    # Always exercise all regional branches, regardless of which validation candidate wins.
    exercised = candidates[1]
    actual = model.query_kernels(test)
    oracle = lamp_scalar_kernel_reference(model, test)
    kernel_error = max(float((a - b).abs().max()) for a, b in zip(actual, oracle, strict=True))
    weights = exercised.coefficients()
    residual = model.one_hot - support.global_features @ text.T
    # Independent inverse reference, distinct from the production linear solves.
    expected = test.global_features @ text.T + sum(w * h @ torch.linalg.inv(system) @ residual
                 for w, h, system in zip(weights, oracle, model.systems, strict=True))
    solve_error = float((model.predict(test, exercised) - expected).abs().max())
    cache = model.cache(test, exercised)
    prototypes = nn.Parameter(text.clone())
    initial_error = float((cache.predict(prototypes) - model.predict(test, exercised)).abs().max().detach())
    loss = model.prototype_loss(prototypes)
    loss.backward()
    gradient = float(prototypes.grad.norm())
    torch.optim.AdamW([prototypes], lr=.001, weight_decay=0).step()
    update = float((prototypes - text).norm().detach())
    fresh = model.predict(test, exercised, prototypes)
    cached = cache.predict(prototypes)
    cached_error = float((fresh - cached).abs().max().detach())
    gamma = F.normalize(prototypes, dim=-1) - text
    stale_residual = cache.base_scores + test.global_features @ gamma.T
    negative = float((cached - stale_residual).abs().max().detach())
    single = FeatureBatch(test.global_features[:1], tuple(t[:1] for t in test.regional_features), test.sample_ids[:1])
    batch_error = max(float((a[:1] - b).abs().max()) for a, b in zip(actual, model.query_kernels(single), strict=True))
    frozen_error = max(float((p - old).abs().max()) for p, old in zip((*layers.parameters(), *projection.parameters()), frozen_before, strict=True))
    # Final test labels are first read here, after mixture selection and training.
    test_labels = torch.tensor([0, 1, 2, 0, 1], device=device)
    final_report = evaluate_test(model, test, test_labels, mixture, validation_ids=validation.sample_ids)
    assert max(kernel_error, solve_error, initial_error, cached_error, batch_error, frozen_error) < 1e-10
    assert gradient > 0 and update > 0 and negative > 1e-7
    return {"regional_kernel_reference_max_error": kernel_error, "residual_solve_reference_max_error": solve_error,
            "initialization_reference_max_error": initial_error, "cached_response_reference_max_error": cached_error,
            "stale_support_residual_negative_control_difference": negative,
            "query_batch_invariance_max_error": batch_error, "frozen_encoder_change": frozen_error,
            "prototype_gradient_norm": gradient, "prototype_update_norm": update,
            "validation_selected_rho": mixture.rho, "synthetic_validation_accuracy": validation_score,
            "base_lamp_synthetic_test_accuracy": final_report["accuracy"], "test_examples": final_report["examples"], "optimizer_steps": 1}


def summarize(rows: list[dict]) -> dict:
    return {key: {"mean": statistics.mean(values := [row["metrics"][key] for row in rows]),
                  "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
            for key in rows[0]["metrics"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--papers", default=",".join(MODULES))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    papers = args.papers.split(",")
    try:
        seeds = [int(value) for value in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not papers or set(papers) - set(MODULES) or len(set(papers)) != len(papers):
        parser.error("select unique supported papers")
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8 or any(not 0 <= s < 2 ** 32 for s in seeds):
        parser.error("1..8 unique seeds in [0,2**32) required")
    if args.code_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit):
        parser.error("full hexadecimal commit required")
    if args.output.exists():
        parser.error("output is immutable; choose a fresh path")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no CPU fallback")
    torch.set_num_threads(1)
    start = time.monotonic()
    operations = {"fpot": fpot_diagnostic, "lamp": lamp_diagnostic}
    components = {}
    for paper in papers:
        rows = [{"seed": seed, "metrics": operations[paper](seed, args.device)} for seed in seeds]
        components[paper] = {"dataset": {"id": "synthetic-fpot-and-native-layer-kernel-features",
                                          "revision": "oct19-foundation-mechanisms-v1", "checkpoint": None,
                                          "capability_benchmark": False},
                             "per_seed": rows, "metrics": summarize(rows), "diagnostic_only": True,
                             "evaluation_tier": "l1_mechanism", "promotion_eligible": False, "evolve_integrated": False,
                             "full_experiment_status": "not_reproduced_high_cost", "review_done": True}
    sources = [Path(__file__).resolve()] + [ROOT / f"src/auto_research/foundation_models/{MODULES[key]}.py" for key in papers]
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
    print(json.dumps({"output": str(args.output), "components": list(components), "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
