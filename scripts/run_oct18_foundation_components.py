#!/usr/bin/env python3
"""Five bounded trainable mechanism diagnostics; no models/data downloaded."""
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
from torch import nn

from auto_research.foundation_models.adaloop_vision import (
    QuestionConditionedVisionLoop, depth_supervised_loss, stability_stop, visual_prefix,
)
from auto_research.foundation_models.memory_mosaics_plus import MemoryMosaicsPlus, masked_average
from auto_research.foundation_models.mjev_spatial import (
    NativeSpatialReadout, crop_original, decode_count, encode_count, length_codebook,
    refine_region, stage_normalized_loss,
)
from auto_research.foundation_models.rr_vlm import RetrofittedRecurrentVLM, recovery_loss
from auto_research.foundation_models.softcache import SoftCacheSampler, residual_extrapolation

ROOT = Path(__file__).resolve().parents[1]
MODULES = {"memory-mosaics-plus": "memory_mosaics_plus", "mjev-spatial": "mjev_spatial",
           "adaloop-vision": "adaloop_vision", "softcache": "softcache", "rr-vlm": "rr_vlm"}


def update_once(model: nn.Module, loss: torch.Tensor, parameter: torch.Tensor, lr: float = .01) -> tuple[float, float]:
    before = parameter.detach().clone()
    optimizer = torch.optim.SGD([p for p in model.parameters() if p.requires_grad], lr=lr)
    optimizer.zero_grad()
    loss.backward()
    assert all(p.grad is None or bool(torch.isfinite(p.grad).all()) for p in model.parameters())
    gradient = float(parameter.grad.norm())
    optimizer.step()
    update = float((parameter - before).norm().detach())
    assert gradient > 0 and update > 0
    return gradient, update


def mosaics_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    model = MemoryMosaicsPlus().to(device=device, dtype=torch.float64)
    x = torch.randn(2, 8, 16, device=device, dtype=torch.float64)
    starts = torch.tensor([[0, 0, 0, 3, 3, 3, 6, 6]] * 2, device=device)
    pieces = model.components(x, starts)
    expected = torch.zeros_like(pieces["target"])
    # Independent scalar-loop oracle: two separately normalized task estimates.
    for b in range(2):
        for head in range(4):
            for t in range(8):
                for indices in (range(int(starts[b, t]), t), range(min(int(starts[b, t]), t))):
                    indices = list(indices)
                    if indices:
                        scores = torch.stack([pieces["logits"][b, head, t, i] for i in indices])
                        expected[b, head, t] += sum(weight * pieces["values"][b, head, i]
                                                  for weight, i in zip(scores.softmax(0), indices, strict=True))
    error = float((expected - pieces["target"] - pieces["related"]).abs().max().detach())
    pooled = masked_average(pieces["logits"], pieces["values"], pieces["target_mask"] | pieces["related_mask"])
    negative = float((pooled - pieces["target"] - pieces["related"]).abs().max().detach())
    changed = x.clone()
    changed[:, 5:] += 50
    causal_error = float((model(changed, starts)[:, :5] - model(x, starts)[:, :5]).abs().max().detach())
    target = torch.randn_like(x)
    loss = (model(x, starts) - target).square().mean()
    grad, update = update_once(model, loss, model.key.weight)
    assert error < 1e-10 and causal_error < 1e-10 and negative > 1e-4
    return {"separate_normalizer_reference_max_error": error, "pooled_memory_negative_control_error": negative,
            "future_perturbation_max_error": causal_error, "key_gradient_norm": grad, "key_update_norm": update,
            "training_loss": float(loss.detach()), "optimizer_steps": 1}


def spatial_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    backbone = nn.TransformerEncoderLayer(16, 4, 32, dropout=0., batch_first=True).to(device=device, dtype=torch.float64)
    final_layer = nn.ModuleDict({"norm": nn.RMSNorm(16, eps=1e-6), "query": nn.Linear(16, 16, bias=False),
                                 "key": nn.Linear(16, 8, bias=False), "query_norm": nn.RMSNorm(4, eps=1e-6),
                                 "key_norm": nn.RMSNorm(4, eps=1e-6)}).to(device=device, dtype=torch.float64)
    readout = NativeSpatialReadout(input_norm=final_layer["norm"], query_projection=final_layer["query"],
                                   key_projection=final_layer["key"], query_head_norm=final_layer["query_norm"],
                                   key_head_norm=final_layer["key_norm"])
    assert readout.query is final_layer["query"] and readout.key is final_layer["key"]
    model = nn.ModuleList([backbone, final_layer, readout])
    x = torch.randn(2, 12, 16, device=device, dtype=torch.float64)
    hidden = backbone(x, src_mask=torch.ones(12, 12, device=device, dtype=torch.bool).triu(1))
    decisions = torch.tensor([11, 11], device=device)
    ends = torch.tensor([[3, 6, 9]] * 2, device=device)
    scores = readout(hidden, decisions, ends)
    q, k = readout.projected(hidden, decisions, ends)
    oracle = torch.stack([torch.stack([sum(torch.dot(q[b, 0, head], k[b, c, head // 2])
                                                for head in range(4)) / (4 * 2) for c in range(3)]) for b in range(2)])
    wrong_group = (q * k.repeat(1, 1, 2, 1)).sum(-1).mean(-1) / 2
    error = float((scores - oracle).abs().max().detach())
    negative = float((scores - wrong_group).abs().max().detach())
    stage_scores = [scores[0], scores[0] + torch.tensor([.2, -.4, .1], device=device), scores[1]]
    loss = stage_normalized_loss(stage_scores, [0, 1, 2], [0, 0, 1])
    reference_loss = ((-stage_scores[0].log_softmax(0)[0] - stage_scores[1].log_softmax(0)[1]) / 2
                      - stage_scores[2].log_softmax(0)[2]) / 2
    stage_error = float((loss - reference_loss).abs().detach())
    grad, update = update_once(model, loss, readout.query.weight)
    count_errors = sum(decode_count(*encode_count(value)) != value for value in range(1024))
    edges, cells = length_codebook()
    assert cells == (4,) * 6 + (8,) * 24 and abs(edges[-1] - 16384) < 1e-8
    bounds = (0., 0., 1., 1.)
    original = torch.arange(3 * 81 * 81, device=device, dtype=torch.float64).reshape(3, 81, 81)
    crop_sum = 0.
    for choice in (4, 2, 7):
        bounds = refine_region(bounds, choice)
        crop_sum += float(crop_original(original, bounds).mean())
    assert error < 1e-10 and stage_error < 1e-10 and negative > 1e-4 and count_errors == 0
    return {"native_gqa_reference_max_error": error, "wrong_gqa_group_negative_control_error": negative,
            "question_normalized_loss_max_error": stage_error, "count_roundtrip_errors": count_errors,
            "original_crop_checksum": crop_sum, "query_gradient_norm": grad, "query_update_norm": update,
            "training_loss": float(loss.detach()), "optimizer_steps": 1}


def adaloop_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    model = QuestionConditionedVisionLoop().to(device=device, dtype=torch.float64)
    classifier = nn.Linear(16, 5).to(device=device, dtype=torch.float64)
    all_modules = nn.ModuleList([model, classifier])
    image = torch.randn(3, 6, 16, device=device, dtype=torch.float64)
    question = torch.randn(3, 4, 16, device=device, dtype=torch.float64)
    labels = torch.tensor([1, 2, 3], device=device)
    states = model(image, question)
    condition = model.condition(question)
    block = model.blocks[0]
    # Independent frozen attention/MLP formula at zero AdaLN initialization.
    normal = block.norm_attention(image)
    q, k, v = nn.functional.linear(normal, block.attention.in_proj_weight, block.attention.in_proj_bias).chunk(3, -1)
    split = lambda tensor: tensor.reshape(3, 6, 4, 4).transpose(1, 2)
    attend = ((split(q) @ split(k).transpose(-2, -1)) / 2).softmax(-1) @ split(v)
    attend = attend.transpose(1, 2).reshape(3, 6, 16)
    residual = image + nn.functional.linear(attend, block.attention.out_proj.weight, block.attention.out_proj.bias)
    reference = residual + block.mlp(block.norm_mlp(residual))
    error = float((reference - block(image, condition)).abs().max().detach())
    logits = tuple(classifier(state.mean(1)) for state in states)
    weights = image.new_tensor([.2, .3, .5])
    loss = depth_supervised_loss(logits, labels, weights)
    direct = sum(weights[i] * nn.functional.cross_entropy(logits[i], labels) for i in range(3))
    loss_error = float((loss - direct).abs().detach())
    frozen = {name: p.detach().clone() for name, p in model.named_parameters() if not p.requires_grad}
    grad, update = update_once(all_modules, loss, block.modulation.weight)
    frozen_error = max(float((dict(model.named_parameters())[name] - before).abs().max()) for name, before in frozen.items())
    q_effect = float((model(image, question)[-1] - model(image, question + 2)[-1]).abs().max().detach())
    assert visual_prefix(states, question, "A").shape[1] == 10
    assert visual_prefix(states, question, "B").shape[1] == 22
    assert stability_stop(["left", "right", "right"], 3) == 3
    assert max(error, loss_error, frozen_error) < 1e-10 and q_effect > 1e-8
    return {"frozen_visual_block_reference_max_error": error, "depth_objective_reference_max_error": loss_error,
            "frozen_backbone_change": frozen_error, "question_condition_negative_control_difference": q_effect,
            "modulator_gradient_norm": grad, "modulator_update_norm": update,
            "training_loss": float(loss.detach()), "optimizer_steps": 1}


def rr_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    model = RetrofittedRecurrentVLM().to(device=device, dtype=torch.float64)
    tokens = torch.randint(23, (2, 4), device=device)
    visual = torch.randn(2, 2, 16, device=device, dtype=torch.float64)
    initial = torch.randn(2, 6, 16, device=device, dtype=torch.float64) * .02
    labels = torch.randint(23, (2, 6), device=device)
    x = torch.cat((model.projector(visual), model.embedding(tokens)), 1)
    mask = torch.ones(6, 6, device=device, dtype=torch.bool).triu(1)
    context = x
    for layer in model.prelude:
        context = layer(context, src_mask=mask)
    state = initial
    for _ in range(3):
        state = nn.functional.linear(torch.cat((state, context), -1), model.adapter.weight)
        for layer in model.core:
            state = layer(state, src_mask=mask)
    for layer in model.coda:
        state = layer(state, src_mask=mask)
    reference = nn.functional.linear(state, model.output.weight)
    logits = model(tokens, visual, initial_state=initial)
    error = float((reference - logits).abs().max().detach())
    depth_difference = float((model(tokens, visual, iterations=1, initial_state=initial) - logits).abs().max().detach())
    teacher_before = model.teacher_logits(tokens, visual).clone()
    metrics = {"unrolled_recurrence_max_error": error, "single_pass_negative_control_difference": depth_difference}
    for stage in (0, 1, 2):
        model.configure_stage(stage)
        # Stage 0 is strictly text-only; stages 1/2 expose visual projection.
        stage_visual = visual[:, :0] if stage == 0 else visual
        stage_initial = initial[:, 2:] if stage == 0 else initial
        stage_labels = labels[:, 2:] if stage == 0 else labels
        logits = model(tokens, stage_visual, initial_state=stage_initial)
        teacher = model.teacher_logits(tokens, stage_visual)
        loss = recovery_loss(logits, teacher, stage_labels, weight=0. if stage == 1 else .5)
        parameter = model.projector.weight if stage == 1 else model.adapter.weight
        grad, update = update_once(model, loss, parameter)
        metrics[f"stage{stage}_gradient_norm"] = grad
        metrics[f"stage{stage}_update_norm"] = update
    teacher_error = float((teacher_before - model.teacher_logits(tokens, visual)).abs().max())
    assert error < 1e-10 and teacher_error == 0 and depth_difference > 1e-4
    return {**metrics, "frozen_teacher_change": teacher_error, "optimizer_steps": 3}


def softcache_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    network = nn.Sequential(nn.Linear(9, 12), nn.Tanh(), nn.Linear(12, 8)).to(device=device, dtype=torch.float64)
    training_x = torch.randn(4, 8, device=device, dtype=torch.float64)
    training_t = torch.rand(4, 1, device=device, dtype=torch.float64)
    prediction = network(torch.cat((training_x, training_t), -1))
    loss = (prediction - (.1 * training_x + training_t)).square().mean()
    grad, update = update_once(network, loss, network[0].weight)
    initial = torch.randn(1, 8, device=device, dtype=torch.float64)
    residual = lambda x, t: network(torch.cat((x, x.new_full((x.shape[0], 1), t)), -1))
    readout = lambda x, r, t: r
    probe = lambda x, t: torch.ones_like(x) * (1 + .05 * t)
    nodes = [index / 20 for index in range(21)]
    with torch.no_grad():
        output, trace = SoftCacheSampler(threshold=.015).sample(initial, nodes, residual, readout, probe)
        full, full_trace = SoftCacheSampler(threshold=1e-15).sample(initial, nodes, residual, readout, probe)
        hard, _ = SoftCacheSampler(threshold=.015, max_jump=1).sample(initial, nodes, residual, readout, probe)
        oracle = initial.clone()
        for left, right in zip(nodes[:-1], nodes[1:], strict=True):
            oracle = oracle + (right - left) * residual(oracle, left)
        error = float((full - oracle).abs().max())
        anchor = torch.randn_like(initial)
        previous = torch.randn_like(initial)
        extrapolated = residual_extrapolation(anchor, previous, .6, .4, .2, .5)
        extrapolation_error = float((extrapolated - (1.5 * anchor - .5 * previous)).abs().max())
    fresh = sum(row.fresh for row in trace)
    jumps = sum(not row.fresh and row.step > row.scheduled_step * (1 + 1e-9) for row in trace)
    assert jumps <= sum(not row.fresh for row in trace)
    negative = float((output - hard).abs().max())
    assert error < 1e-10 and extrapolation_error < 1e-10
    assert 1 < fresh < len(trace) < len(full_trace) and jumps > 0 and negative > 1e-6
    assert abs(sum(row.step for row in trace) - 1) < 1e-10
    return {"cache_disabled_euler_reference_max_error": error, "residual_extrapolation_reference_max_error": extrapolation_error,
            "hard_cache_negative_control_difference": negative, "fresh_evaluations": fresh, "visited_nodes": len(trace),
            "headroom_jumps": jumps, "full_euler_model_evaluations": len(full_trace),
            "endpoint_error_to_full_euler": float((output - oracle).norm()),
            "residual_network_gradient_norm": grad, "residual_network_update_norm": update, "optimizer_steps": 1}


def summarize(rows: list[dict]) -> dict:
    result = {}
    for key in rows[0]["metrics"]:
        values = [row["metrics"][key] for row in rows]
        result[key] = {"mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
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
    operations = {"memory-mosaics-plus": mosaics_diagnostic, "mjev-spatial": spatial_diagnostic,
                  "adaloop-vision": adaloop_diagnostic, "softcache": softcache_diagnostic, "rr-vlm": rr_diagnostic}
    components = {}
    for paper in papers:
        rows = [{"seed": seed, "metrics": operations[paper](seed, args.device)} for seed in seeds]
        components[paper] = {"dataset": {"id": "synthetic-memory-spatial-vision-recurrence-and-ode",
                                          "revision": "oct18-foundation-mechanisms-v1", "checkpoint": None,
                                          "capability_benchmark": False},
                             "per_seed": rows, "metrics": summarize(rows), "diagnostic_only": True,
                             "promotion_eligible": False, "evolve_integrated": False,
                             "full_experiment_status": "not_reproduced_high_cost"}
    sources = [Path(__file__).resolve()] + [ROOT / "src/auto_research/foundation_models" / f"{MODULES[key]}.py" for key in papers]
    commit = args.code_commit.lower() if args.code_commit else subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if args.device == "cuda":
        torch.cuda.synchronize()
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
               "seeds": seeds, "diagnostic_only": True, "promotion_eligible": False,
               "components": components, "elapsed_seconds": time.monotonic() - start,
               "executed_source_sha256": {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "components": list(components), "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
