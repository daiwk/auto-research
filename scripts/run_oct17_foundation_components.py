#!/usr/bin/env python3
"""Bounded five-paper formula/bit-format diagnostics; no models, downloads or training benchmark."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re
import statistics
import subprocess
import time

import torch

from auto_research.foundation_models.bit_sparse import pack_activation, sparse_activation_linear, unpack_activation
from auto_research.foundation_models.drop_kv import drop_kv_scores
from auto_research.foundation_models.lct import (
    build_codebook, compress_bf16, decompress_bf16, gaussian_exponent_model, lct_linear,
)
from auto_research.foundation_models.mirror_moe import MirrorMoELayer, cosine_mirror_ratio, mirror_routing
from auto_research.foundation_models.roleq import exact_ternary_fit, quantize_by_role

ROOT = Path(__file__).resolve().parents[1]
KEYS = ("drop-kv", "mirror-moe", "bit-sparse", "lct", "roleq")


def _random(shape, generator, device, *, dtype=torch.float64, grad=False):
    return torch.randn(shape, generator=generator, device=device, dtype=dtype, requires_grad=grad)


def drop_diagnostic(seed: int, device: str) -> dict:
    gen = torch.Generator(device=device).manual_seed(seed)
    q = _random((1, 4, 3, 8), gen, device, grad=True)
    k = _random((1, 2, 19, 8), gen, device, grad=True)
    v = _random((1, 2, 19, 8), gen, device, grad=True)
    result = drop_kv_scores(q, k, v, eviction_count=7)
    # Independent actual removal and re-normalization, not the singleton formula.
    reference = torch.zeros_like(result.scores)
    for head in range(4):
        for j in range(16):
            error = q.new_zeros(())
            for t in range(3):
                available = torch.arange(17 + t, device=device)
                logits = (k[0, head // 2, available] @ q[0, head, t]) / (8 ** .5)
                before = logits.softmax(0) @ v[0, head // 2, available]
                legal = available != j
                after = logits[legal].softmax(0) @ v[0, head // 2, available[legal]]
                error = error + (before - after).square().sum()
            reference[0, head // 2, j] += error / 2
    discrepancy = float((result.scores[..., :16] - reference[..., :16]).abs().max().detach())
    loss = result.outputs.square().mean() + result.scores[..., :16].mean()
    grads = torch.autograd.grad(loss, (q, k, v))
    attention_only = result.attention.sum(-2).reshape(1, 2, 2, 19).mean(-2)[..., :16]
    score = result.scores[..., :16]
    negative = float((score / score.sum(-1, keepdim=True) -
                      attention_only / attention_only.sum(-1, keepdim=True)).abs().max().detach())
    assert discrepancy < 1e-10 and bool((result.evicted_indices < 16).all()) and negative > 1e-5
    assert all(bool(torch.isfinite(g).all()) and float(g.norm()) > 0 for g in grads)
    return {"singleton_removal_reference_max_error": discrepancy, "recent_window_protected": True,
            "attention_only_negative_control_difference": negative,
            "query_gradient_norm": float(grads[0].norm()), "key_gradient_norm": float(grads[1].norm()),
            "value_gradient_norm": float(grads[2].norm()), "evicted_count_per_kv_head": 7}


def mirror_diagnostic(seed: int, device: str) -> dict:
    torch.manual_seed(seed)
    gen = torch.Generator(device=device).manual_seed(seed)
    layer = MirrorMoELayer(8, 12, 6, 2, 3).to(device=device, dtype=torch.float64)
    x = _random((9, 8), gen, device, grad=True)
    ratio = cosine_mirror_ratio(.2)
    output, routing = layer(x, ratio=ratio)
    logits = layer.router(x)
    xi = logits.exp() / logits.exp().sum(-1, keepdim=True)
    zeta = (-logits).exp() / (-logits).exp().sum(-1, keepdim=True)
    selected = ((1 - ratio) * xi + ratio * zeta).argsort(-1, descending=True)[:, :3]
    expected = torch.stack([expert(x) for expert in layer.shared]).sum(0)
    wrong = expected.clone()
    all_outputs = torch.stack([expert(x) for expert in layer.routed], 1)
    for token in range(x.shape[0]):
        for expert in selected[token]:
            expected[token] = expected[token] + xi[token, expert] * all_outputs[token, expert]
            wrong[token] = wrong[token] + routing.selection_probabilities[token, expert] * all_outputs[token, expert]
    error, negative = float((output - expected).abs().max().detach()), float((output - wrong).abs().max().detach())
    before = layer.router.weight.detach().clone()
    optimizer = torch.optim.SGD(layer.parameters(), lr=.02)
    optimizer.zero_grad()
    (output.square().mean() + .1 * routing.balancing_loss).backward()
    gradient = float(layer.router.weight.grad.norm())
    optimizer.step()
    delta = float((layer.router.weight - before).norm().detach())
    ordinary = mirror_routing(logits.detach(), top_k=3, ratio=0)
    assert error < 1e-12 and negative > 1e-7 and gradient > 0 and delta > 0
    assert torch.equal(ordinary.selected, logits.topk(3, -1).indices)
    return {"manual_aggregation_max_error": error, "mixed_weight_negative_control_error": negative,
            "router_gradient_norm": gradient, "router_update_norm": delta,
            "zero_ratio_recovers_topk": True, "final_schedule_ratio": cosine_mirror_ratio(1)}


def sparse_diagnostic(seed: int, device: str) -> dict:
    gen = torch.Generator(device=device).manual_seed(seed)
    raw = _random((33, 37), gen, device, dtype=torch.float32) - 1
    h = torch.where(raw > 0, raw, torch.zeros_like(raw)).to(torch.bfloat16)
    packed = pack_activation(h, tile_size=8)
    rebuilt = unpack_activation(packed)
    exact = bool(torch.equal(h.view(torch.int16), rebuilt.contiguous().view(torch.int16)))
    z = _random((9, 13), gen, device, grad=True)
    weight = _random((7, 13), gen, device, grad=True)
    reference_z, reference_w = z.detach().clone().requires_grad_(), weight.detach().clone().requires_grad_()
    actual = sparse_activation_linear(z, weight, power=2, tile_size=8)
    reference = reference_z.relu().square() @ reference_w.t()
    grad = _random(actual.shape, gen, device)
    actual_grads = torch.autograd.grad(actual, (z, weight), grad)
    reference_grads = torch.autograd.grad(reference, (reference_z, reference_w), grad)
    gradient_error = max(float((a - b).abs().max()) for a, b in zip(actual_grads, reference_grads, strict=True))
    error = float((actual - reference).abs().max().detach())
    assert exact and error == 0 and gradient_error < 1e-10
    return {"bf16_bitwise_roundtrip": exact, "forward_max_error": error,
            "backward_max_error": gradient_error, "dense_activation_bytes": h.numel() * h.element_size(),
            "compact_activation_bytes_including_mask_prefix": packed.storage_bytes,
            "storage_ratio_dense_over_compact": h.numel() * h.element_size() / packed.storage_bytes,
            "sparsity": float((h == 0).float().mean())}


def lct_diagnostic(seed: int, device: str, codebook) -> dict:
    gen = torch.Generator(device=device).manual_seed(seed)
    x = _random((16, 32), gen, device, dtype=torch.float32).to(torch.bfloat16)
    # All exponent byte values, varied signs/fractions: no numerical NaN operation.
    exponents = torch.arange(256, dtype=torch.int64, device=device)
    patterns = ((exponents << 7) | (exponents % 128) | ((exponents % 2) << 15)).to(torch.int16)
    bits = x.view(torch.int16).reshape(-1).clone()
    bits[:256] = patterns
    x = bits.view(torch.bfloat16).reshape(16, 32)
    packed = compress_bf16(x, codebook, streams=16, budget_bits=32, center=3)
    rebuilt = decompress_bf16(packed)
    exact = bool(torch.equal(x.view(torch.int16), rebuilt.view(torch.int16)))
    roomy = compress_bf16(x, codebook, streams=16, budget_bits=512, center=-4)
    roomy_exact = bool(torch.equal(x.view(torch.int16), decompress_bf16(roomy).view(torch.int16)))
    inputs = _random((8, 16), gen, device, dtype=torch.float32).to(torch.bfloat16).requires_grad_()
    weight = _random((5, 16), gen, device, dtype=torch.float32).to(torch.bfloat16).requires_grad_()
    other_x, other_w = inputs.detach().clone().requires_grad_(), weight.detach().clone().requires_grad_()
    actual, expected = lct_linear(inputs, weight, codebook), other_x @ other_w.t()
    gradient = torch.ones_like(actual)
    grad = torch.autograd.grad(actual, (inputs, weight), gradient)
    other_grad = torch.autograd.grad(expected, (other_x, other_w), gradient)
    gradient_equal = all(torch.equal(a, b) for a, b in zip(grad, other_grad, strict=True))
    assert exact and roomy_exact and packed.overflow_exponents.numel() > 0 and gradient_equal
    assert torch.equal(actual, expected)
    return {"all_bf16_exponents_bitwise_roundtrip": exact, "roomy_buffer_roundtrip": roomy_exact,
            "overflow_raw_tail_bytes": packed.overflow_exponents.numel(),
            "autograd_matches_dense": gradient_equal, "payload_and_stream_metadata_bytes": packed.payload_storage_bytes,
            "standalone_codebook_bytes": packed.standalone_codebook_bytes,
            "serialized_header_bytes": packed.serialized_header_bytes,
            "standalone_serialized_total_bytes": packed.payload_storage_bytes + packed.standalone_codebook_bytes + packed.serialized_header_bytes,
            "dense_bytes": x.numel() * x.element_size(), "prefix_cap_bits": codebook.prefix_cap,
            "model_expected_exponent_bits": codebook.expected_bits}


def roleq_diagnostic(seed: int, device: str) -> dict:
    gen = torch.Generator(device=device).manual_seed(seed)
    vector = _random((4,), gen, device)
    code, scale = exact_ternary_fit(vector)
    actual_loss = (vector - code * scale).square().sum()
    all_codes = torch.tensor(list(itertools.product((-1., 0., 1.), repeat=4)), device=device, dtype=vector.dtype)
    scales = ((all_codes @ vector) / all_codes.square().sum(-1).clamp_min(1)).clamp_min(0)
    brute_loss = (vector - all_codes * scales[:, None]).square().sum(-1).min()
    gap = float((actual_loss - brute_loss).abs())
    weight = _random((7, 11), gen, device)
    reader, writer = quantize_by_role(weight, "reader"), quantize_by_role(weight, "writer")
    transposed_reader = quantize_by_role(weight.t(), "reader")
    axis_error = float((writer.reconstruct() - transposed_reader.reconstruct().t()).abs().max())
    # Exact solver must not be replaced by a fixed threshold or mean scale.
    naive_codes = torch.where(vector.abs() > .7 * vector.abs().mean(), vector.sign(), 0)
    naive_scale = (vector.abs() * naive_codes.abs()).sum() / naive_codes.abs().sum().clamp_min(1)
    naive_loss = (vector - naive_codes * naive_scale).square().sum()
    assert gap < 1e-12 and axis_error == 0 and float(naive_loss - actual_loss) > -1e-12
    assert reader.scales.shape == (7,) and writer.scales.shape == (11,)
    bits = reader.bit_accounting()
    assert bits["payload_and_scale_storage_bits"] == reader.packed_trits.numel() * 8 + reader.scales.numel() * 64
    return {"bruteforce_global_optimum_loss_gap": gap, "writer_equals_transposed_reader_max_error": axis_error,
            "exact_loss": float(actual_loss), "threshold_control_loss": float(naive_loss),
            "reader_scale_count": reader.scales.numel(), "writer_scale_count": writer.scales.numel(),
            "actual_packed_code_bits": bits["packed_code_bits"], "actual_scale_bits": bits["scale_bits"],
            "serialized_payload_scale_bpw": bits["payload_and_scale_bpw"],
            "packing_padding_trits": bits["packing_padding_trits"]}


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
    parser.add_argument("--papers", default=",".join(KEYS))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    papers = args.papers.split(",")
    try:
        seeds = [int(s) for s in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not papers or set(papers) - set(KEYS) or len(papers) != len(set(papers)):
        parser.error("select unique supported papers")
    if not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 8:
        parser.error("1..8 unique seeds required")
    if args.code_commit and not re.fullmatch(r"[0-9a-fA-F]{40}", args.code_commit):
        parser.error("code commit must be 40 hexadecimal characters")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("explicit CUDA is unavailable; no CPU fallback")
    if args.output.exists():
        parser.error("output is immutable; choose a fresh path")
    torch.set_num_threads(1)
    started = time.monotonic()
    codebook = build_codebook(gaussian_exponent_model()) if "lct" in papers else None
    operations = {"drop-kv": drop_diagnostic, "mirror-moe": mirror_diagnostic,
                  "bit-sparse": sparse_diagnostic, "lct": lambda s, d: lct_diagnostic(s, d, codebook),
                  "roleq": roleq_diagnostic}
    components = {}
    for key in papers:
        rows = [{"seed": seed, "metrics": operations[key](seed, args.device)} for seed in seeds]
        components[key] = {"dataset": {"id": "synthetic-formula-and-bit-patterns",
                                       "revision": "oct17-foundation-components-v1", "checkpoint": None,
                                       "capability_benchmark": False},
                           "per_seed": rows, "metrics": summarize(rows), "diagnostic_only": True,
                           "promotion_eligible": False, "full_experiment_status": "not_reproduced_high_cost"}
    sources = [Path(__file__).resolve()] + [ROOT / "src/auto_research/foundation_models" / (k.replace("-", "_") + ".py") for k in KEYS]
    commit = args.code_commit.lower() if args.code_commit else subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    payload = {"schema_version": 1, "code_commit": commit, "device": args.device,
               "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
               "diagnostic_only": True, "promotion_eligible": False, "seeds": seeds,
               "components": components, "elapsed_seconds": time.monotonic() - started,
               "executed_source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    print(json.dumps({"output": str(args.output), "components": list(components), "elapsed_seconds": payload["elapsed_seconds"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
