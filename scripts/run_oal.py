"""Qwen2.5 Base QK grouping, attention-output calibration, OAL+LoRA conversion.

This small public-data experiment is diagnostic: dense exact-kernel training,
not author HD block-GEMM serving or the 512-step WikiText-103 benchmark.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

import torch
from torch.nn import functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer

from auto_research.foundation_models.oal import (
    GroupedQuadratic, QwenOALAttention, contribution, group_dimensions, install_lora, qwen_states,
)
from auto_research.foundation_models.oct13_runtime import check_checkpoint_identity

BASE_ID = "Qwen/Qwen2.5-0.5B"
BASE_REVISION = "060db6499f32faf8b98477b0a26969ef7d8b9987"


def blocks(tokenizer, path: Path, length: int, maximum: int) -> torch.Tensor:
    ids = tokenizer(path.read_text(), add_special_tokens=False)["input_ids"]
    usable = min(len(ids) // length, maximum)
    if usable < maximum:
        raise ValueError(f"insufficient independent text blocks in {path.name}")
    return torch.tensor(ids[:usable * length]).reshape(usable, length)


@torch.no_grad()
def capture(model, data: torch.Tensor, layer: int, device: str) -> list[tuple]:
    bank = []
    attention = model.model.layers[layer].self_attn

    def collect(module, args, kwargs):
        hidden = kwargs.get("hidden_states", args[0] if args else None)
        position = kwargs.get("position_embeddings")
        if hidden is None or position is None:
            raise ValueError("Qwen attention did not expose required post-RoPE inputs")
        bank.append(tuple(value.detach().float() for value in qwen_states(module, hidden, position)))

    hook = attention.register_forward_pre_hook(collect, with_kwargs=True)
    try:
        for row in data:
            model(input_ids=row[None].to(device), use_cache=False)
    finally:
        hook.remove()
    return bank


def fit(kernel: GroupedQuadratic, train: list[tuple], validation: list[tuple], steps: int) -> tuple[torch.Tensor, torch.Tensor]:
    optimizer = torch.optim.Adam(kernel.parameters(), lr=.02)
    best = torch.full((len(kernel.groups),), torch.inf, device=kernel.groups.device)
    factors = kernel.factors.detach().clone()
    for step in range(steps):
        q, k, v = train[step % len(train)]
        target = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        optimizer.zero_grad()
        loss = (kernel(q, k, v) - target).square().mean()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(kernel.parameters(), 10.)
        optimizer.step()
        with torch.no_grad():
            errors = torch.stack([(kernel(q, k, v) - F.scaled_dot_product_attention(q, k, v, is_causal=True)).square().mean((0, 2, 3))
                                  for q, k, v in validation]).mean(0)
            improved = errors < best
            factors[improved] = kernel.factors[improved]
            best = torch.minimum(best, errors)
    return factors, best


@torch.no_grad()
def nll(model, data: torch.Tensor, device: str) -> float:
    model.eval()
    return float(torch.stack([model(input_ids=row[None].to(device), labels=row[None].to(device), use_cache=False).loss
                              for row in data]).mean())


def adapt(model, train, validation, args) -> dict:
    parameters = [p for p in model.parameters() if p.requires_grad]
    before = torch.cat([p.detach().flatten() for p in parameters]).clone()
    optimizer = torch.optim.AdamW(parameters, lr=5e-4, weight_decay=.01)
    initial = nll(model, validation, args.device)
    best_nll, best_state, history = math.inf, None, []
    for step in range(args.steps):
        model.train()
        optimizer.zero_grad()
        row = train[step % len(train)][None].to(args.device)
        loss = model(input_ids=row, labels=row, use_cache=False).loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.)
        optimizer.step()
        current = nll(model, validation, args.device)
        history.append({"loss": float(loss.detach()), "validation_nll": current})
        if current < best_nll:
            best_nll = current
            best_state = [p.detach().clone() for p in parameters]
    with torch.no_grad():
        for parameter, value in zip(parameters, best_state, strict=True):
            parameter.copy_(value)
    return {"initial_validation_nll": initial, "selected_validation_nll": best_nll,
            "parameter_delta_l2": float((torch.cat([p.detach().flatten() for p in parameters]) - before).norm()),
            "history": history}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--checkpoint-id", default=BASE_ID)
    p.add_argument("--checkpoint-revision", default=BASE_REVISION)
    p.add_argument("--data", type=Path, required=True)
    p.add_argument("--dataset-id", required=True)
    p.add_argument("--dataset-revision", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", default="cuda")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=3)
    p.add_argument("--calibration-steps", type=int, default=10)
    p.add_argument("--sequence-length", type=int, default=32)
    p.add_argument("--layers", default="4")
    p.add_argument("--bootstrap", type=int, default=64)
    args = p.parse_args()
    if args.checkpoint_id != BASE_ID or args.checkpoint_revision != BASE_REVISION:
        p.error("this public protocol requires the fixed Qwen2.5-0.5B Base, not Instruct")
    if min(args.steps, args.calibration_steps, args.bootstrap) < 1 or args.sequence_length < 8:
        p.error("positive update budgets and sequence length >=8 required")
    check_checkpoint_identity(args.checkpoint, args.checkpoint_id, args.checkpoint_revision)
    torch.manual_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint, local_files_only=True)
    train = blocks(tokenizer, args.data / "train.txt", args.sequence_length, 16)
    validation = blocks(tokenizer, args.data / "validation.txt", args.sequence_length, 2)
    # Do not load/tokenize test until coefficient and model checkpoint selection finishes.
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint, local_files_only=True, dtype=torch.bfloat16 if args.device == "cuda" else torch.float32,
        attn_implementation="eager").to(args.device).eval()
    if model.config.model_type != "qwen2" or model.config.num_hidden_layers != 24:
        p.error("expected the Qwen2.5-0.5B Base configuration")
    layer_ids = [int(value) for value in args.layers.split(",")]
    if any(layer < 3 or layer > 20 for layer in layer_ids):
        p.error("conversion must retain first/final three native softmax layers")
    kernels, calibration = {}, {}
    for layer in layer_ids:
        grouping = capture(model, train[:4], layer, args.device)
        fitting = capture(model, train[4:8], layer, args.device)
        val = capture(model, validation, layer, args.device)
        scores = torch.cat([contribution(q, k) for q, k, _ in grouping], 0)
        groups = group_dimensions(scores, bootstrap=args.bootstrap, seed=args.seed)
        global_kernel = GroupedQuadratic(torch.zeros_like(groups))
        global_factors, global_error = fit(global_kernel, fitting, val, args.calibration_steps)
        kernel = GroupedQuadratic(groups)
        taylor = kernel.factors.detach().clone()
        learned = torch.zeros_like(taylor)
        learned[:, 0, 0] = global_factors[:, 0, 0]
        learned[:, 1:, 0] = global_factors[:, 1, 0, None]
        learned[:, 1:, 1] = global_factors[:, 1, 1, None]
        best_error = torch.full_like(global_error, torch.inf)
        selected = taylor.clone()
        for initial in (learned, taylor, learned + .01 * torch.randn_like(learned)):
            with torch.no_grad():
                kernel.factors.copy_(initial)
            factors, error = fit(kernel, fitting, val, args.calibration_steps)
            improved = error < best_error
            selected[improved] = factors[improved]
            best_error = torch.minimum(best_error, error)
        with torch.no_grad():
            kernel.factors.copy_(selected)
            q, k, v = val[0]
            dense = kernel(q[..., :8, :], k[..., :8, :], v[..., :8, :])
            recurrent = kernel.recurrent(q[..., :8, :], k[..., :8, :], v[..., :8, :])
            recurrence_error = float((dense - recurrent).abs().max())
            torch.testing.assert_close(dense, recurrent, atol=5e-4, rtol=5e-4)
        calibration[str(layer)] = {"groups_per_head": [int(row.max()) + 1 for row in groups],
                                   "validation_output_mse": float(best_error.mean()),
                                   "global_validation_output_mse": float(global_error.mean()),
                                   "recurrent_dense_max_error": recurrence_error}
        kernels[layer] = kernel
    baseline = copy.deepcopy(model)
    torch.manual_seed(args.seed)
    install_lora(baseline)
    torch.manual_seed(args.seed)
    install_lora(model)
    for layer, kernel in kernels.items():
        model.model.layers[layer].self_attn = QwenOALAttention(model.model.layers[layer].self_attn, kernel)
    # Both runs share the actual train order, budgets, data splits, and LoRA config.
    torch.manual_seed(args.seed)
    baseline_result = adapt(baseline, train[8:], validation, args)
    torch.manual_seed(args.seed)
    result = adapt(model, train[8:], validation, args)
    test = blocks(tokenizer, args.data / "test.txt", args.sequence_length, 2)
    for candidate, outcome in ((baseline, baseline_result), (model, result)):
        final = nll(candidate, test, args.device)
        outcome.update(test_nll=final, test_ppl=math.exp(min(final, 80)))
    report = {"paper": "2610.13674", "seed": args.seed, "diagnostic_only": True,
              "promotion_eligible": False, "fidelity": "core_mechanism", "evaluation_tier": "l1_mechanism",
              "checkpoint": {"id": args.checkpoint_id, "revision": args.checkpoint_revision},
              "dataset": {"id": args.dataset_id, "revision": args.dataset_revision,
                          "split_hashes": {name: hashlib.sha256((args.data / f"{name}.txt").read_bytes()).hexdigest()
                                           for name in ("train", "validation", "test")}},
              "calibration": calibration, "softmax_lora": baseline_result, "oal_lora": result,
              "converted_layers": layer_ids, "sequence_length": args.sequence_length,
              "steps": args.steps, "calibration_steps_per_initialization": args.calibration_steps,
              "bootstrap_replicates": args.bootstrap, "test_isolated_from_selection": True,
              "limitations": ["WikiText-2 small independent blocks, not the WikiText-103 author protocol",
                               "dense exact-kernel adaptation; HD recurrent equivalence separately measured",
                               "no native serving-cache backend, latency or bandwidth claim",
                               "one converted intermediate layer by default; not full 3..20 conversion"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
