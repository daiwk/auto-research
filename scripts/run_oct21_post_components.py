#!/usr/bin/env python3
"""Bounded AP-OPD/OPTD defining-component diagnostics, not LLM benchmarks."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import statistics
import subprocess
import time

import torch
from torch import nn

from auto_research.post_training.oct21_distillation import adaptive_pullback_loss, transition_distillation_loss

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("scripts/run_oct21_post_components.py", "src/auto_research/post_training/oct21_distillation.py")
METHODS = ("ap-opd", "optd")


def softmax(values):
    maximum = max(values)
    exponents = [math.exp(v - maximum) for v in values]
    total = sum(exponents)
    return [v / total for v in exponents]


def log_softmax(values):
    maximum = max(values)
    normalizer = maximum + math.log(sum(math.exp(v - maximum) for v in values))
    return [v - normalizer for v in values]


def ap_reference(student, teacher, block_size=2, z=2.):
    weights, gradients, value, jumps = [], [], 0., 0
    n = sum(map(len, student))
    for s, t in zip(student, teacher, strict=True):
        ratio = [a - b for a, b in zip(s, t, strict=True)]
        blocks = [[max(r, 0.) for r in ratio[i:i + block_size]] for i in range(0, len(ratio), block_size)]
        means = [statistics.mean(block) for block in blocks]
        w = [1.] * len(s)
        for i in range(len(blocks) - 1):
            left, right = blocks[i:i + 2]
            if len(left) < 2 or len(right) < 2:
                continue
            se = math.sqrt(statistics.variance(left) / len(left) + statistics.variance(right) / len(right))
            if means[i + 1] - means[i] > z * se:
                jumps += 1
                for j in range((i + 1) * block_size, min((i + 2) * block_size, len(s))):
                    w[j] = means[i] / means[i + 1]
        g = [a * b / n for a, b in zip(w, ratio, strict=True)]
        value += sum(a * b for a, b in zip(g, s, strict=True))
        weights.append(w)
        gradients.append(g)
    return value, gradients, weights, jumps


def optd_reference(student, teacher, top_k=5, *, use_increment_weights=False):
    """Independent scalar loop plus analytic softmax-Jacobian logit gradient."""
    batch, depth, tokens, vocab = len(student), len(student[0]), len(student[0][0]), len(student[0][0][0])
    gradient = [[[[0.] * vocab for _ in range(tokens)] for _ in range(depth)] for _ in range(batch)]
    value, denominator = 0., batch * tokens
    for b in range(batch):
        for t in range(tokens):
            ls = [log_softmax(student[b][d][t]) for d in range(depth)]
            lt = [log_softmax(teacher[b][d][t]) for d in range(depth)]
            ids = sorted(range(vocab), key=lambda v: ls[-1][v], reverse=True)[:top_k]
            grads = [[0.] * vocab for _ in range(depth)]
            weights = softmax([ls[-1][v] for v in ids])
            for v, w in zip(ids, weights, strict=True):
                coefficient = w * (ls[-1][v] - lt[-1][v]) / denominator
                value += coefficient * ls[-1][v]
                grads[-1][v] += coefficient
            for d in range(1, depth):
                ds = [ls[d][v] - ls[d - 1][v] for v in ids]
                dt = [lt[d][v] - lt[d - 1][v] for v in ids]
                weights = softmax(ds if use_increment_weights else [ls[d][v] for v in ids])
                for v, w, a, q in zip(ids, weights, ds, dt, strict=True):
                    coefficient = w * (a - q) / denominator
                    value += coefficient * a
                    grads[d][v] += coefficient
                    grads[d - 1][v] -= coefficient
            for d in range(depth):
                probs, total = softmax(student[b][d][t]), sum(grads[d])
                gradient[b][d][t] = [g - p * total for g, p in zip(grads[d], probs, strict=True)]
    return value, gradient


class TinyDepthCausalPolicy(nn.Module):
    """Random 12-token GRU + residual-depth readouts; no pretrained language."""
    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(12, 8)
        self.recurrent = nn.GRU(8, 8, batch_first=True)
        self.blocks = nn.ModuleList(nn.Linear(8, 8) for _ in range(3))
        self.norm = nn.LayerNorm(8)
        self.head = nn.Linear(8, 12)

    def forward(self, tokens):
        h, _ = self.recurrent(self.embedding(tokens))
        readouts = [self.head(self.norm(h))]
        for block in self.blocks:
            h = h + torch.tanh(block(h))
            readouts.append(self.head(self.norm(h)))
        return torch.stack(readouts, 1)


@torch.no_grad()
def sample(model, prefix, device, length=10):
    response = []
    for _ in range(length):
        x = torch.tensor([prefix + response], device=device)
        logits = model(x)[0, -1, -1]
        response.append(int(torch.multinomial(logits.softmax(-1), 1)))
    return response


def run_method(key, device, steps):
    model = TinyDepthCausalPolicy().to(device=device, dtype=torch.float64)
    teacher = TinyDepthCausalPolicy().to(device=device, dtype=torch.float64).eval().requires_grad_(False)
    initial = [p.detach().clone() for p in model.parameters()]
    teacher_initial = [p.detach().clone() for p in teacher.parameters()]
    optimizer = torch.optim.SGD(model.parameters(), lr=.02)
    errors, grad_errors, norms, controls, jumps, records = [], [], [], [], [], []
    for iteration in range(steps):
        histories = [[1, 2 + i] for i in range(4)]
        responses = [sample(model, h, device) for h in histories]
        ids = torch.tensor([h + r[:-1] for h, r in zip(histories, responses, strict=True)], device=device)
        student = model(ids)[:, :, -10:]
        with torch.no_grad():
            target = teacher(ids)[:, :, -10:]
        mask = torch.ones((4, 10), device=device, dtype=torch.bool)
        if key == "ap-opd":
            labels = torch.tensor(responses, device=device)[..., None]
            lp = student[:, -1].log_softmax(-1).gather(-1, labels).squeeze(-1)
            lq = target[:, -1].log_softmax(-1).gather(-1, labels).squeeze(-1)
            loss, audit = adaptive_pullback_loss(lp, lq, mask, block_size=2)
            expected, gradient, expected_weights, count = ap_reference(lp.detach().tolist(), lq.tolist())
            actual_grad = torch.autograd.grad(loss, lp, retain_graph=True)[0]
            grad_errors.append(float((actual_grad - torch.tensor(gradient, device=device, dtype=torch.float64)).abs().max()))
            errors.append(abs(float(loss.detach()) - expected))
            if not torch.allclose(audit["weights"], torch.tensor(expected_weights, device=device, dtype=torch.float64), atol=1e-12, rtol=0):
                raise RuntimeError("AP-OPD weights differ from independent scalar reference")
            jumps.append(count)
            controls.append(abs(float(loss.detach()) - float(((lp.detach() - lq) * lp.detach()).mean())))
            records.append({"update": iteration, "public_histories": histories, "student_sampled_responses": responses,
                            "selected_boundaries": audit["selected_boundaries"], "weights": audit["weights"].tolist()})
        else:
            loss, audit = transition_distillation_loss(student, target, mask, top_k=5)
            raw_s, raw_t = student.detach().tolist(), target.tolist()
            expected, gradient = optd_reference(raw_s, raw_t)
            actual_grad = torch.autograd.grad(loss, student, retain_graph=True)[0]
            grad_errors.append(float((actual_grad - torch.tensor(gradient, device=device, dtype=torch.float64)).abs().max()))
            errors.append(abs(float(loss.detach()) - expected))
            _, wrong = optd_reference(raw_s, raw_t, use_increment_weights=True)
            controls.append(float((actual_grad - torch.tensor(wrong, device=device, dtype=torch.float64)).norm()))
            records.append({"update": iteration, "public_histories": histories, "student_sampled_responses": responses,
                            "fixed_final_topk_candidate_ids": audit["candidate_ids"].tolist(),
                            "transition_scale": audit["transition_scale"]})
        if max(errors) > 1e-10 or max(grad_errors) > 1e-7:
            raise RuntimeError("independent loss/gradient audit failed")
        optimizer.zero_grad()
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 10., error_if_nonfinite=True)
        if not torch.isfinite(loss) or not math.isfinite(float(norm)) or float(norm) <= 0:
            raise RuntimeError("finite nonzero policy gradient required")
        norms.append(float(norm))
        optimizer.step()
    parameter_delta = math.sqrt(sum(float((p.detach() - q).square().sum()) for p, q in zip(model.parameters(), initial, strict=True)))
    frozen_delta = max(float((p.detach() - q).abs().max()) for p, q in zip(teacher.parameters(), teacher_initial, strict=True))
    metrics = {"optimizer_updates": steps, "parameter_delta_l2": parameter_delta,
               "gradient_norm_min": min(norms), "loss_reference_max_abs_error": max(errors),
               "logit_gradient_reference_max_abs_error": max(grad_errors),
               "negative_control_difference_max": max(controls), "teacher_parameter_delta_max": frozen_delta,
               "teacher_gradient_count": sum(p.grad is not None for p in teacher.parameters()),
               "pretrained_or_public_benchmark_evaluated": False}
    if key == "ap-opd":
        metrics["actual_sampled_selected_boundaries_total"] = sum(jumps)
        # Guaranteed edge-case diagnostic is separate from actual model rollouts.
        r = torch.tensor([[1., 1., 3., 3., 5., 5.]], device=device, dtype=torch.float64)
        fixture, _ = adaptive_pullback_loss(r, torch.zeros_like(r), torch.ones_like(r, dtype=torch.bool), block_size=2)
        expected, _, weights, count = ap_reference(r.tolist(), torch.zeros_like(r).tolist())
        if abs(float(fixture) - expected) > 1e-12 or weights != [[1., 1., 1 / 3, 1 / 3, 3 / 5, 3 / 5]] or count != 2:
            raise RuntimeError("original-profile staircase invariant failed")
        metrics["staircase_original_profile_reference_error"] = abs(float(fixture) - expected)
        metrics["staircase_recursive_profile_negative_control_difference"] = abs(3 / 5 - 1 / 5)
    return {"metrics": metrics, "rollout_audit": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--methods", default=",".join(METHODS))
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--steps", type=int, default=3)
    parser.add_argument("--code-commit")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        methods, seeds = args.methods.split(","), [int(v) for v in args.seeds.split(",")]
    except ValueError:
        parser.error("integer seeds required")
    if not methods or len(set(methods)) != len(methods) or set(methods) - set(METHODS):
        parser.error("distinct known methods required")
    if not seeds or len(set(seeds)) != len(seeds) or any(s < 0 or s >= 2 ** 32 for s in seeds) or not 1 <= args.steps <= 6:
        parser.error("distinct bounded seeds and 1--6 updates required")
    if args.output.exists():
        parser.error("immutable output exists")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("requested CUDA unavailable; no CPU fallback")
    commit = args.code_commit or subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        parser.error("full lowercase code commit required")
    torch.set_num_threads(1)
    started = time.monotonic()
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in SOURCES}
    common = {"diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
              "formal_comparison_eligible": False, "full_experiment_status": "not_reproduced_high_cost"}
    result = {"schema_version": 2, "code_commit": commit, "executed_source_sha256": hashes,
              "device": args.device, "accelerator": torch.cuda.get_device_name(0) if args.device == "cuda" else "CPU",
              "seeds": seeds, "limits": {"steps": args.steps, "no_downloads": True, "pretrained_checkpoint": None,
                  "synthetic_protocol_revision": "oct21-ap-opd-optd-defining-components-v1"}, "components": {}, **common}
    for method in methods:
        rows = []
        for seed in seeds:
            torch.manual_seed(seed)
            rows.append({"seed": seed, "status": "completed", **run_method(method, args.device, args.steps)})
        aggregate = {}
        for name in rows[0]["metrics"]:
            values = [r["metrics"][name] for r in rows]
            if not all(math.isfinite(float(v)) for v in values):
                raise RuntimeError("nonfinite metric")
            aggregate[name] = all(values) if all(isinstance(v, bool) for v in values) else {
                "mean": statistics.mean(values), "std": statistics.stdev(values) if len(values) > 1 else 0., "n": len(values)}
        result["components"][method] = {"per_seed": rows, "metrics": aggregate, "dataset": {
            "id": f"synthetic:oct21-{method}-v1", "revision": "sha256:" + hashes[SOURCES[0]],
            "capability_benchmark": False}, **common}
    if args.device == "cuda":
        torch.cuda.synchronize()
    result["elapsed_seconds"] = time.monotonic() - started
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2, allow_nan=False)
        stream.write("\n")
    print(json.dumps({"output": str(args.output), "methods": methods, "seeds": seeds, "device": args.device}))


if __name__ == "__main__":
    main()
