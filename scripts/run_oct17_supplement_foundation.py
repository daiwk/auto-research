#!/usr/bin/env python3
"""Bounded Prism-1/LangDiT mechanism diagnostics; no downloads or capability claims."""
from __future__ import annotations

import argparse
from dataclasses import replace
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import time

import torch

from auto_research.foundation_models.langdit import (
    LangDiTDenoiser, corrupt_tokens, likelihood_shortcut, noise_coefficients,
    posterior_mean, training_self_condition,
)
from auto_research.foundation_models.prism_one import PrismOneScorer, choice_diagnostics, pack_options

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"prism-1": "prism_one", "langdit": "langdit"}


def prism_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    model = PrismOneScorer().to(device=device, dtype=torch.float64)
    prefix = torch.tensor([4, 5, 6], device=device)
    options = [torch.tensor(ids, device=device) for ids in ([7, 8], [9], [10, 11, 12])]
    packed = pack_options(prefix, options)
    scores = model(packed)
    independent = []
    for option in options:
        tokens = torch.cat((prefix, option))
        h = model.token_embedding(tokens) + model.position_embedding(torch.arange(tokens.numel(), device=device))
        causal = torch.ones((tokens.numel(), tokens.numel()), dtype=torch.bool, device=device).tril()
        for block in model.blocks:
            h = block(h, causal)
        logits = model.vocabulary_head(model.final_norm(h[-1]))
        independent.append(logits[model.yes_token] - logits[model.no_token])
    error = float((scores - torch.stack(independent)).abs().max().detach())
    permutation = [2, 0, 1]
    permuted = model(pack_options(prefix, [options[i] for i in permutation]))
    permutation_error = float((permuted - scores[permutation]).abs().max().detach())
    extended = model(pack_options(prefix, options + [torch.tensor([20, 21, 22, 23], device=device)]))
    diagnostics = choice_diagnostics(scores, extended)
    wrong = replace(packed, allowed_attention=torch.ones_like(packed.allowed_attention).tril())
    contamination = float((model(wrong) - scores).abs().max().detach())
    before = model.vocabulary_head.weight.detach().clone()
    optimizer = torch.optim.SGD(model.parameters(), lr=.01)
    optimizer.zero_grad()
    # Arbitrary label trains the mechanism; never a benchmark/test answer.
    loss = -scores.log_softmax(0)[0]
    loss.backward()
    gradient = float(model.vocabulary_head.weight.grad.norm())
    assert all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in model.parameters())
    optimizer.step()
    update = float((model.vocabulary_head.weight - before).norm().detach())
    assert max(error, permutation_error, *diagnostics.values()) < 1e-10
    assert contamination > 1e-6 and gradient > 0 and update > 0
    return {"independent_causal_forward_max_error": error, "permutation_score_max_error": permutation_error,
            **diagnostics, "cross_option_attention_negative_control_error": contamination,
            "vocabulary_head_gradient_norm": gradient, "vocabulary_head_update_norm": update,
            "parameters": sum(p.numel() for p in model.parameters()), "optimizer_steps": 1}


def langdit_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    gen = torch.Generator(device=device).manual_seed(seed)
    dtype = torch.float64
    c = torch.randn(7, 4, generator=gen, device=device, dtype=dtype, requires_grad=True)
    z = torch.randn(2, 3, 4, generator=gen, device=device, dtype=dtype, requires_grad=True)
    gamma = torch.tensor([-.5, .7], device=device, dtype=dtype)
    gate = torch.tensor([.5, 2.], device=device, dtype=dtype)
    actual = likelihood_shortcut(z, gamma, c, gate)
    a, s = noise_coefficients(gamma)
    reference = torch.stack([gate[b] * a[b] / s[b].square() * z[b] @ c.detach().t() for b in range(2)])
    shortcut_error = float((actual - reference).abs().max().detach())
    gz, gc = torch.autograd.grad(actual.square().mean(), (z, c), allow_unused=True)
    direct_gradient_absent = gc is None
    tokens = torch.tensor([[0, 1, 2], [3, 4, 5]], device=device)
    noisy = corrupt_tokens(c, tokens, gamma, torch.zeros_like(z))
    input_path = likelihood_shortcut(noisy, gamma, c, gate)
    input_gradient = float(torch.autograd.grad(input_path.square().mean(), c)[0].norm())
    logits = torch.randn(2, 3, 7, generator=gen, device=device, dtype=dtype)
    probability = logits.softmax(-1).requires_grad_()
    weighted, confidence = training_self_condition(probability, c)
    oracle_entropy = torch.stack([torch.stack([
        -sum(probability[b, t, v] * probability[b, t, v].log() for v in range(7)) for t in range(3)])
        for b in range(2)])
    oracle_weight = (1 - oracle_entropy / math.log(7)).clamp(0, 1)
    condition_error = float((weighted - (oracle_weight[..., None] * (probability @ c)).detach()).abs().max())
    sampling_difference = float((posterior_mean(probability, c).detach() - weighted).abs().max())
    model = LangDiTDenoiser().to(device=device, dtype=dtype)
    train_tokens = torch.randint(19, (4, 6), generator=gen, device=device)
    train_gamma = torch.tensor([-1., -.3, .4, 1.], device=device, dtype=dtype)
    noise = torch.randn(4, 6, 16, generator=gen, device=device, dtype=dtype)
    mask = torch.tensor([True, False, False, False], device=device)
    optimizer = torch.optim.SGD(model.parameters(), lr=.02)
    before = model.raw_codebook.detach().clone()
    losses = []
    for _ in range(3):
        optimizer.zero_grad()
        prediction, auxiliary = model.training_logits(train_tokens, train_gamma, noise, mask)
        assert not auxiliary.requires_grad and int(torch.count_nonzero(auxiliary[1:])) == 0
        loss = model.token_loss(prediction, train_tokens)
        loss.backward()
        assert all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in model.parameters())
        optimizer.step()
        losses.append(float(loss.detach()))
    update = float((model.raw_codebook - before).norm().detach())
    attention_gradient = float(model.blocks[0].qkv.weight.grad.norm())
    state = corrupt_tokens(model.codebook(), train_tokens, train_gamma, noise)
    expected_mean = model(state, train_gamma).softmax(-1) @ model.codebook()
    sampler_error = float((model.inference_mean(state, train_gamma) - expected_mean).abs().max().detach())
    calibration = model.calibration_mlp(model.noise_embedding(train_gamma)).clamp(-math.log(2), math.log(2)).exp()
    calibration_min, calibration_max = float(calibration.min().detach()), float(calibration.max().detach())
    assert max(shortcut_error, condition_error, sampler_error) < 1e-10
    assert direct_gradient_absent and input_gradient > 0 and float(gz.norm()) > 0
    assert not weighted.requires_grad and not confidence.requires_grad
    assert sampling_difference > 1e-4 and update > 0 and attention_gradient > 0
    assert .5 <= calibration_min <= calibration_max <= 2
    return {"shortcut_independent_reference_max_error": shortcut_error,
            "explicit_shortcut_codebook_gradient_absent": direct_gradient_absent,
            "shortcut_input_gradient_norm": float(gz.norm()), "retained_codebook_input_gradient_norm": input_gradient,
            "entropy_gated_bootstrap_max_error": condition_error,
            "unweighted_sampling_negative_control_difference": sampling_difference,
            "inference_posterior_mean_max_error": sampler_error, "codebook_update_norm": update,
            "learned_calibration_min": calibration_min, "learned_calibration_max": calibration_max,
            "bidirectional_attention_gradient_norm": attention_gradient,
            "first_fixture_training_loss": losses[0], "last_fixture_training_loss": losses[-1],
            "parameters": sum(p.numel() for p in model.parameters()), "optimizer_steps": 3}


def summarize(rows: list[dict]) -> dict:
    result = {}
    for key in rows[0]["metrics"]:
        values = [row["metrics"][key] for row in rows]
        result[key] = (all(values) if isinstance(values[0], bool) else
                       {"mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0.,
                        "n": len(values)})
    return result


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
    if not papers or set(papers) - set(MODULES) or len(papers) != len(set(papers)):
        parser.error("select unique supported papers")
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8:
        parser.error("1..8 unique seeds required")
    if args.code_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit):
        parser.error("code commit must be a full hexadecimal commit id")
    if args.output.exists():
        parser.error("output is immutable; choose a fresh path")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no CPU fallback")
    torch.set_num_threads(1)
    start = time.monotonic()
    operations = {"prism-1": prism_diagnostic, "langdit": langdit_diagnostic}
    components = {}
    for paper in papers:
        rows = [{"seed": seed, "metrics": operations[paper](seed, args.device)} for seed in seeds]
        components[paper] = {
            "dataset": {"id": "synthetic-packed-options-and-noisy-tokens", "revision": "oct17-supplement-foundation-v1",
                        "checkpoint": None, "capability_benchmark": False},
            "per_seed": rows, "metrics": summarize(rows), "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost",
        }
    sources = [Path(__file__).resolve()] + [ROOT / "src/auto_research/foundation_models" / f"{name}.py"
                                          for name in MODULES.values()]
    commit = args.code_commit.lower() if args.code_commit else subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.device == "cuda":
        torch.cuda.synchronize()
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
               "seeds": seeds, "diagnostic_only": True, "promotion_eligible": False,
               "components": components, "elapsed_seconds": time.monotonic() - start,
               "executed_source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                          for p in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "components": list(components),
                      "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
