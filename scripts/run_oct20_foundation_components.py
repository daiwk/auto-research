#!/usr/bin/env python3
"""Seconds-scale synthetic t-Muon/Time-JEPA/KronLSTM definition diagnostics."""
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

from auto_research.foundation_models.kronlstm import TinyKronLSTM
from auto_research.foundation_models.t_muon import TensorMuon, tensor_polar, transform_matrix
from auto_research.foundation_models.time_jepa import (
    StateNormalizer, TinyTimeJEPA, align_nearest, pool_tubelets,
)

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"t-muon": "t_muon", "time-jepa": "time_jepa", "kronlstm": "kronlstm"}
RECIPE = "oct20-foundation-definition-synthetic-v1"


def _norm(tensors) -> float:
    return math.sqrt(sum(float(value.detach().square().sum()) for value in tensors if value is not None))


def _eigen_polar(matrix: torch.Tensor) -> torch.Tensor:
    # Gram eigendecomposition, independent of the implementation's thin SVD.
    eigenvalues, vectors = torch.linalg.eigh(matrix.mH @ matrix)
    threshold = 1e-11 * max(1., float(eigenvalues.max()))
    inverse = torch.where(eigenvalues > threshold, eigenvalues.clamp_min(threshold).rsqrt(), 0.)
    return matrix @ ((vectors * inverse) @ vectors.mH)


def _transform_oracle(tensor: torch.Tensor, matrix: torch.Tensor) -> torch.Tensor:
    slices = [sum(matrix[k, j] * tensor[..., j].to(matrix.dtype) for j in range(tensor.shape[-1]))
              for k in range(tensor.shape[-1])]
    polarized = _eigen_polar(torch.block_diag(*slices))
    rows, cols = tensor.shape[:2]
    parts = [polarized[k * rows:(k + 1) * rows, k * cols:(k + 1) * cols] for k in range(len(slices))]
    result = torch.stack([sum(matrix[k, j].conj() * parts[k] for k in range(len(parts)))
                          for j in range(len(parts))], -1)
    return result.real.to(tensor.dtype)


def t_muon_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    parameters = [nn.Parameter(torch.randn(6, 4, device=device, dtype=torch.float64) * .3) for _ in range(3)]
    optimizer = TensorMuon(parameters, lr=.015, momentum=.9, weight_decay=.03,
                           mode="head-stack", heads=2, transform="dct")
    x = torch.randn(7, 4, device=device, dtype=torch.float64)
    targets = [torch.randn(7, 6, device=device, dtype=torch.float64) for _ in parameters]
    gradient_error, update_error, transform_error, momentum_error = 0., 0., 0., 0.
    gradient_norm, update_norm = 0., 0.
    previous = [torch.zeros_like(parameter) for parameter in parameters]
    audit = []
    for step in range(2):
        optimizer.zero_grad()
        losses = [(F.linear(x, parameter) - target).square().mean()
                  for parameter, target in zip(parameters, targets, strict=True)]
        loss = torch.stack(losses).mean()
        loss.backward()
        for parameter, target in zip(parameters, targets, strict=True):
            expected = 2 * (x @ parameter.detach().T - target).T @ x / (7 * 6 * 3)
            gradient_error = max(gradient_error, float((parameter.grad - expected).abs().max()))
        gradient_norm = max(gradient_norm, _norm(p.grad for p in parameters))
        buffers = [.9 * old + parameter.grad for old, parameter in zip(previous, parameters, strict=True)]
        directions = [parameter.grad + .9 * buffer for parameter, buffer in zip(parameters, buffers, strict=True)]
        # Explicit slicing is independent of the production pack/unpack helpers.
        tensor = torch.stack([matrix[start:start + 3] for matrix in directions for start in (0, 3)], -1)
        for kind in ("identity", "dct", "dst", "dft"):
            transform = transform_matrix(6, kind, device=device)
            error = (tensor_polar(tensor, transform) - _transform_oracle(tensor, transform)).abs().max()
            transform_error = max(transform_error, float(error))
        expected_tensor = _transform_oracle(tensor, transform_matrix(6, "dct", device=device))
        expected_updates = [torch.cat((expected_tensor[..., 2 * j], expected_tensor[..., 2 * j + 1]), 0) for j in range(3)]
        before = [parameter.detach().clone() for parameter in parameters]
        optimizer.step()
        for parameter, old, direction, buffer in zip(parameters, before, expected_updates, buffers, strict=True):
            expected = old * (1 - .015 * .03) - .015 * math.sqrt(6 / 4) * direction
            update_error = max(update_error, float((parameter.detach() - expected).abs().max()))
            momentum_error = max(momentum_error, float((optimizer.state[parameter]["momentum_buffer"] - buffer).abs().max()))
        update_norm += _norm(parameter.detach() - old for parameter, old in zip(parameters, before, strict=True))
        audit.append({"step": step, "loss": float(loss.detach()), "grouped_direction": tensor.detach().cpu().tolist()})
        previous = [buffer.detach().clone() for buffer in buffers]
    correct = tensor_polar(tensor, transform_matrix(6, "dct", device=device))
    unfolded = _eigen_polar(tensor.permute(2, 0, 1).reshape(18, 4)).reshape(6, 3, 4).permute(1, 2, 0)
    negative = float((correct - unfolded).norm())
    metrics = {"gradient_reference_max_error": gradient_error, "transform_polar_reference_max_error": transform_error,
               "optimizer_update_reference_max_error": update_error, "momentum_reference_max_error": momentum_error,
               "gradient_norm": gradient_norm, "parameter_update_norm": update_norm,
               "unfolded_muon_negative_difference_norm": negative,
               "zero_tensor_update_max": float(tensor_polar(torch.zeros_like(tensor), transform_matrix(6, "dct", device=device)).abs().max()),
               "optimizer_steps": 2, "tested_transforms": 4}
    if max(gradient_error, transform_error, update_error, momentum_error) > 1e-9 or min(gradient_norm, update_norm, negative) <= 1e-9:
        raise RuntimeError("t-Muon numerical, update or negative control failed")
    if metrics["zero_tensor_update_max"] != 0:
        raise RuntimeError("rank-zero polar must not produce an arbitrary isometry")
    return {"metrics": metrics, "audit": {"steps": audit, "tensorization": "head-stack", "heads": 2,
                                            "optimizer_transform": "dct", "polar": "exact_rank_reduced_svd",
                                            "reference": "explicit_M_sums_block_diagonal_Gram_eigen_polar"}}


def time_jepa_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    dtype = torch.float64
    model = TinyTimeJEPA().to(device=device, dtype=dtype)
    times = torch.arange(8, device=device, dtype=dtype) / 10
    sensor_times = times + times.new_tensor([-.01, .01, -.02, 0, .01, -.01, .02, 0])
    sensor = torch.randn(8, 8, 2, device=device, dtype=dtype)
    validity = torch.rand(8, 8, 2, device=device) > .2
    aligned, frame_valid = align_nearest(times, sensor_times, sensor, validity, max_gap=.04)
    pooled, tube_valid = pool_tubelets(aligned, frame_valid)
    normalizer = StateNormalizer.fit(pooled[:6], tube_valid[:6], split="train")
    frozen_mean, frozen_std = normalizer.mean.clone(), normalizer.std.clone()
    states, valid = normalizer.normalize(pooled[6:], tube_valid[6:])
    states.requires_grad_(True)  # must still not receive gradients through supervision
    video = torch.randn(2, 4, 3, 5, device=device, dtype=dtype)
    context = torch.tensor([0, 1, 3, 4, 6, 7, 9, 10], device=device)
    masked = torch.tensor([2, 5, 8, 11], device=device)
    result = model(video, context=context, masked=masked, states=states, valid=valid, time_weight=.7)
    prediction, latent_prediction = result["state_prediction"], result["latent_prediction"]
    difference = prediction.detach() - states.detach()
    absolute = difference.abs()
    scalar_time = sum((float(d) ** 2 if abs(float(d)) < .5 else abs(float(d)) - .25)
                      for d in difference[valid].cpu()) / int(valid.sum())
    scalar_latent = sum(abs(float(d)) for d in (latent_prediction.detach() - result["latent_target"]).flatten().cpu()) / latent_prediction.numel()
    actual_gradients = torch.autograd.grad(result["loss"], (prediction, latent_prediction), retain_graph=True)
    expected_time_grad = .7 * torch.where(valid, torch.where(absolute < .5, 2 * difference, difference.sign()), 0) / valid.sum()
    expected_latent_grad = (latent_prediction.detach() - result["latent_target"]).sign() / latent_prediction.numel()
    gradient_error = max(float((actual_gradients[0] - expected_time_grad).abs().max()),
                         float((actual_gradients[1] - expected_latent_grad).abs().max()))
    online = list(model.online.parameters())
    auxiliary_encoder_grad = _norm(torch.autograd.grad(result["time_loss"], online, retain_graph=True))
    latent_encoder_grad = _norm(torch.autograd.grad(result["latent_loss"], online, retain_graph=True))
    changed_video = video.clone().flatten(1, 2)
    changed_video[:, masked] += 7
    changed = model(changed_video.reshape_as(video), context=context, masked=masked, states=states, valid=valid, time_weight=.7)
    context_leak = float((result["latent_prediction"] - changed["latent_prediction"]).abs().max().detach())
    unmasked_sensitivity = float((prediction - changed["state_prediction"]).abs().max().detach())
    shuffled = model(video, context=context, masked=masked, states=states.flip(1), valid=valid.flip(1), time_weight=.7)
    shuffled_delta = abs(float(shuffled["time_loss"].detach() - result["time_loss"].detach()))
    before = [parameter.detach().clone() for parameter in model.parameters()]
    target_before = [parameter.detach().clone() for parameter in model.target.parameters()]
    result["loss"].backward()
    gradient_norm = _norm(p.grad for p in model.parameters())
    teacher_grad = _norm(p.grad for p in model.target.parameters())
    torch.optim.SGD((p for p in model.parameters() if p.requires_grad), lr=.01).step()
    target_optimizer_change = max(float((parameter.detach() - old).abs().max())
                                  for parameter, old in zip(model.target.parameters(), target_before, strict=True))
    update_norm = _norm(parameter.detach() - old for parameter, old in zip(model.parameters(), before, strict=True))
    model.update_target(.97)
    ema_error = max(float((target - (.97 * old + .03 * parameter.detach())).abs().max())
                    for target, old, parameter in zip(model.target.parameters(), target_before, model.online.parameters(), strict=True))
    rejected = False
    try:
        StateNormalizer.fit(pooled[6:], tube_valid[6:], split="validation")
    except ValueError:
        rejected = True
    metrics = {"loss": float(result["loss"].detach()), "time_loss": float(result["time_loss"].detach()),
               "latent_loss": float(result["latent_loss"].detach()),
               "joint_loss_reference_absolute_error": abs(float(result["loss"].detach()) - scalar_latent - .7 * scalar_time),
               "loss_gradient_reference_max_error": gradient_error, "gradient_norm": gradient_norm,
               "parameter_update_norm": update_norm, "auxiliary_online_gradient_norm": auxiliary_encoder_grad,
               "latent_online_gradient_norm": latent_encoder_grad, "teacher_gradient_norm": teacher_grad,
               "target_optimizer_update_max": target_optimizer_change, "ema_reference_max_error": ema_error,
               "state_target_gradient_norm": _norm([states.grad]), "masked_context_leak_max": context_leak,
               "unmasked_auxiliary_sensitivity": unmasked_sensitivity, "shuffled_state_loss_absolute_delta": shuffled_delta,
               "normalizer_mutation_max": max(float((normalizer.mean - frozen_mean).abs().max()), float((normalizer.std - frozen_std).abs().max())),
               "validation_fit_rejected": rejected, "valid_state_entries": int(valid.sum())}
    if max(metrics["joint_loss_reference_absolute_error"], gradient_error, ema_error) > 1e-10:
        raise RuntimeError("Time-JEPA independent loss/gradient/EMA oracle failed")
    if min(gradient_norm, update_norm, auxiliary_encoder_grad, latent_encoder_grad, shuffled_delta, unmasked_sensitivity) <= 1e-9:
        raise RuntimeError("Time-JEPA positive or negative controls degenerate")
    if any(metrics[name] != 0 for name in ("teacher_gradient_norm", "target_optimizer_update_max", "state_target_gradient_norm", "masked_context_leak_max", "normalizer_mutation_max")) or not rejected:
        raise RuntimeError("Time-JEPA target/context/calibration isolation failed")
    return {"metrics": metrics, "audit": {"sensor_timestamps": sensor_times.cpu().tolist(), "video_timestamps": times.cpu().tolist(),
                                            "alignment_policy": "nearest_earlier_tie_max_gap_0.04_seconds",
                                            "train_normalizer_examples": 6, "heldout_examples": 2,
                                            "train_mean": frozen_mean.cpu().tolist(), "train_std": frozen_std.cpu().tolist(),
                                            "context_indices": context.cpu().tolist(), "masked_indices": masked.cpu().tolist(),
                                            "physical_state_is_encoder_input": False,
                                            "latent_target": result["latent_target"].cpu().tolist(),
                                            "tiny_random_encoder_not_released_vjepa": True}}


def vector_memory_oracle(query, key, value, beta, write, forget):
    """Row-major vec(S): s'=(I-beta aa^T)diag(f.repeat(dv))s+c*a."""
    outputs, states = [], []
    for batch in range(key.shape[0]):
        head_outputs, head_states = [], []
        for head in range(key.shape[1]):
            dv, dk = value.shape[-1], key.shape[-1]
            state = key.new_zeros(dv * dk)
            sequence = []
            for index in range(key.shape[2]):
                # torch.kron on vectors is independent of the recurrence's contraction/outer update.
                a = torch.kron(value[batch, head, index].contiguous(), key[batch, head, index].contiguous())
                transition = (torch.eye(dv * dk, device=key.device, dtype=key.dtype)
                              - beta[batch, head, index] * torch.outer(a, a)) @ torch.diag(forget[batch, head, index].repeat(dv))
                state = transition @ state + write[batch, head, index] * a
                sequence.append(state.reshape(dv, dk) @ query[batch, head, index])
            head_outputs.append(torch.stack(sequence))
            head_states.append(state.reshape(dv, dk))
        outputs.append(torch.stack(head_outputs))
        states.append(torch.stack(head_states))
    return torch.stack(outputs), torch.stack(states)


def kronlstm_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    model = TinyKronLSTM().to(device=device, dtype=torch.float64)
    inputs = torch.randn(2, 7, 12, device=device, dtype=torch.float64)
    output, state, audit = model(inputs)
    arguments = tuple(audit[name] for name in ("query", "key", "value", "beta", "write", "forget"))
    reference_read, reference_state = vector_memory_oracle(*arguments)
    read_error = float((audit["read"] - reference_read).abs().max().detach())
    state_error = float((state - reference_state).abs().max().detach())
    read_target = torch.randn_like(reference_read)
    state_target = torch.randn_like(state)
    lhs = (audit["read"] - read_target).square().mean() + (state - state_target).square().mean()
    rhs = (reference_read - read_target).square().mean() + (reference_state - state_target).square().mean()
    native_gradients = torch.autograd.grad(lhs, arguments, retain_graph=True)
    reference_gradients = torch.autograd.grad(rhs, arguments, retain_graph=True)
    gradient_error = max(float((native - reference).abs().max()) for native, reference in zip(native_gradients, reference_gradients, strict=True))
    target = torch.randn_like(output)
    loss = (output - target).square().mean() + .1 * lhs
    before = [p.detach().clone() for p in model.parameters()]
    loss.backward()
    gradient_norm = _norm(p.grad for p in model.parameters())
    gate_gradient_norm = _norm([model.erase.weight.grad, model.write.weight.grad, model.forget.weight.grad, model.a_log.grad])
    torch.optim.SGD(model.parameters(), lr=.01).step()
    update_norm = _norm(p.detach() - old for p, old in zip(model.parameters(), before, strict=True))
    # Standard vector-residual DeltaNet is a *different* erasure rule.
    wrong_state = torch.zeros_like(state)
    wrong_reads = []
    q, k, v, b, c, f = [argument.detach() for argument in arguments]
    for index in range(k.shape[2]):
        decayed = wrong_state * f[:, :, index].unsqueeze(-2)
        vector_error = (decayed @ k[:, :, index].unsqueeze(-1)).squeeze(-1)
        wrong_state = decayed - b[:, :, index, None, None] * vector_error.unsqueeze(-1) * k[:, :, index].unsqueeze(-2)
        wrong_state = wrong_state + c[:, :, index, None, None] * v[:, :, index].unsqueeze(-1) * k[:, :, index].unsqueeze(-2)
        wrong_reads.append((wrong_state @ q[:, :, index].unsqueeze(-1)).squeeze(-1))
    negative = float((audit["read"].detach() - torch.stack(wrong_reads, 2)).norm())
    # Future tokens must not affect the prefix (includes the causal convolution).
    with torch.no_grad():
        changed = inputs.clone()
        changed[:, 4:] += 9
        after_a = model(inputs)[0]
        after_b = model(changed)[0]
        causal_error = float((after_a[:, :4] - after_b[:, :4]).abs().max())
    metrics = {"loss": float(loss.detach()), "recurrence_read_reference_max_error": read_error,
               "recurrence_state_reference_max_error": state_error, "gradient_reference_max_error": gradient_error,
               "gradient_norm": gradient_norm, "gate_gradient_norm": gate_gradient_norm,
               "parameter_update_norm": update_norm, "vector_deltanet_negative_difference_norm": negative,
               "causal_prefix_max_error": causal_error,
               "key_norm_max_error": float((k.norm(dim=-1) - 1).abs().max()),
               "value_norm_max_error": float((v.norm(dim=-1) - 1).abs().max())}
    if max(read_error, state_error, gradient_error, causal_error) > 1e-10 or min(gradient_norm, gate_gradient_norm, update_norm, negative) <= 1e-9:
        raise RuntimeError("KronLSTM reference, gradient, causality or negative control failed")
    return {"metrics": metrics, "audit": {"query": q.cpu().tolist(), "key": k.cpu().tolist(), "value": v.cpu().tolist(),
                                            "erase_gate": b.cpu().tolist(), "write_gate": c.cpu().tolist(),
                                            "key_axis_forget_gate": f.cpu().tolist(), "final_memory": state.detach().cpu().tolist(),
                                            "reference": "explicit_vectorized_rank_one_transition_matrix",
                                            "kernel": "pytorch_recurrence_not_fused_chunk_kernel"}}


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
        seeds = [int(item) for item in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(MODULES):
        parser.error("unique supported methods required")
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8 or any(not 0 <= seed < 2 ** 32 for seed in seeds):
        parser.error("1..8 unique seeds in [0,2**32) required")
    if args.code_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit):
        parser.error("full hexadecimal commit required")
    if args.output.exists():
        parser.error("output immutable; choose a fresh file")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA unavailable; no CPU fallback")
    torch.set_num_threads(1)
    sources = [Path(__file__).resolve()] + [ROOT / f"src/auto_research/foundation_models/{module}.py" for module in MODULES.values()]
    hashes = {str(source.relative_to(ROOT)): hashlib.sha256(source.read_bytes()).hexdigest() for source in sources}
    revision = "sha256:" + hashes[str(Path(__file__).resolve().relative_to(ROOT))]
    start = time.monotonic()
    operations = {"t-muon": t_muon_diagnostic, "time-jepa": time_jepa_diagnostic, "kronlstm": kronlstm_diagnostic}
    components = {}
    for key in methods:
        rows = [{"seed": seed, **operations[key](seed, args.device)} for seed in seeds]
        components[key] = {"dataset": {"id": f"synthetic:oct20-{key}-v1", "revision": revision,
                                       "checkpoint": None, "capability_benchmark": False, "recipe": RECIPE},
                           "per_seed": rows, "metrics": summarize(rows), "diagnostic_only": True,
                           "evaluation_tier": "l1_mechanism", "promotion_eligible": False, "evolve_integrated": False,
                           "full_experiment_status": "not_reproduced_high_cost", "review_done": True}
    commit = args.code_commit.lower() if args.code_commit else subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.device == "cuda":
        torch.cuda.synchronize()
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU", "seeds": seeds,
               "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
               "components": components, "elapsed_seconds": time.monotonic() - start, "executed_source_sha256": hashes}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
