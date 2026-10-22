"""CORD's mini-batch gradient combination, arXiv:2610.29965v1 Eq. 6/Alg. 1.

Loss gradients are descent gradients. The local first-order statement is about
the combined vector, BEFORE AdamW, momentum, weight decay or finite-step effects.
No agent rollout, GRPO host, teacher or skill bank is supplied by this component.
"""
from __future__ import annotations

from collections.abc import Sequence
import math

import torch
from torch import Tensor


def _validate_pair(first: Tensor, second: Tensor) -> None:
    if first.ndim != 1 or not first.numel() or not first.is_floating_point():
        raise ValueError("nonempty floating flat objective gradients required")
    if second.shape != first.shape or second.dtype != first.dtype or second.device != first.device:
        raise ValueError("gradient shape, dtype and device must match")
    if not bool(torch.isfinite(first).all()) or not bool(torch.isfinite(second).all()):
        raise ValueError("finite objective gradients required")


def combine_gradients(first: Tensor, second: Tensor, *, weight: float = 1.,
                      protect: str = "first", gate: str = "conflict-only") -> tuple[Tensor, dict]:
    """Closest feasible replacement of only the unprotected weighted gradient.

    first = G1 and second = G2, not lambda*G2. Roles are selected AFTER applying
    lambda. At lambda=0 the paper explicitly returns G1, independently of roles.
    The caller must accumulate the full optimizer mini-batch before this call.
    Half-precision vectors are promoted to float32 for the entire combination.
    """
    _validate_pair(first, second)
    if isinstance(weight, bool) or not math.isfinite(weight) or weight < 0:
        raise ValueError("finite nonnegative second-objective weight required")
    if protect not in {"first", "second"} or gate not in {"conflict-only", "always", "none"}:
        raise ValueError("explicit first/second protection and conflict-only/always/none gate required")
    first, second = first.detach(), second.detach()
    if first.dtype in (torch.float16, torch.bfloat16):
        first, second = first.float(), second.float()
    u, v = first, weight * second
    a, b = (u, v) if protect == "first" else (v, u)
    dot, norm = torch.dot(a, b), torch.dot(a, a)
    if not bool(torch.isfinite(dot)) or not bool(torch.isfinite(norm)):
        raise ValueError("weighted gradient statistics overflowed")
    active = weight > 0 and bool(norm > 0) and (gate == "always" or (gate == "conflict-only" and bool(dot < 0)))
    candidate = b - (dot / norm) * a if active else b
    combined = u if weight == 0 else a + candidate
    return combined, {"protected": a, "candidate_before": b, "candidate_after": candidate,
                      "cross_dot": dot, "protected_norm_squared": norm,
                      "projected": active, "protect": protect, "gate": gate,
                      "guarantee_before_optimizer_only": True}


def accumulate_gradients(first_micro: Sequence[Tensor], second_micro: Sequence[Tensor],
                         micro_weights: Sequence[float], **options) -> tuple[Tensor, dict]:
    """Fixed loss weights first, ONE nonlinear projection per optimizer batch.

    No automatic normalization is applied to the specified aggregation weights.
    Repartitioning is invariant only when the underlying weighted losses agree.
    This is a single-device flat-vector API, not distributed shard reduction.
    """
    if not first_micro or len(first_micro) != len(second_micro) or len(first_micro) != len(micro_weights):
        raise ValueError("equal nonempty micro-batch gradient and weight lists required")
    if any(isinstance(w, bool) or not math.isfinite(w) or w < 0 for w in micro_weights) or not sum(micro_weights) > 0:
        raise ValueError("nonnegative fixed micro weights with a positive sum required")
    for first, second in zip(first_micro, second_micro):
        _validate_pair(first_micro[0], first)
        _validate_pair(first, second)
    # Promote BEFORE multiplying aggregation weights or adding micro-batches.
    # Promoting only in combine_gradients cannot undo fp16 overflow or bf16
    # increments already rounded away during accumulation.
    first_work = [g.float() for g in first_micro] if first_micro[0].dtype in (torch.float16, torch.bfloat16) else first_micro
    second_work = [g.float() for g in second_micro] if second_micro[0].dtype in (torch.float16, torch.bfloat16) else second_micro
    a = sum((w * g for w, g in zip(micro_weights, first_work)), torch.zeros_like(first_work[0]))
    b = sum((w * g for w, g in zip(micro_weights, second_work)), torch.zeros_like(second_work[0]))
    result, audit = combine_gradients(a, b, **options)
    return result, {**audit, "micro_batches": len(first_micro), "first_accumulated": a,
                    "second_accumulated": b, "projection_after_accumulation": True}


def objective_gradients(loss: Tensor, parameters: Sequence[Tensor], *, retain_graph: bool = True) -> Tensor:
    """Extract one loss's flat gradients, retaining unused parameters as zeros."""
    params = tuple(parameters)
    if loss.ndim != 0 or not loss.requires_grad or not bool(torch.isfinite(loss)):
        raise ValueError("finite differentiable scalar loss required")
    if not params or any(not p.requires_grad or not p.is_floating_point() for p in params):
        raise ValueError("trainable floating parameters required")
    if any(p.device != params[0].device or p.dtype != params[0].dtype for p in params):
        raise ValueError("parameters must share dtype and device")
    values = torch.autograd.grad(loss, params, retain_graph=retain_graph, allow_unused=True)
    return torch.cat([(torch.zeros_like(p) if g is None else g).detach().reshape(-1) for p, g in zip(params, values)])


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Three real tiny-neural SGD updates; no agent/benchmark capability claim."""
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("integer seed required")
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU fallback")
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        model = torch.nn.Sequential(torch.nn.Linear(3, 5), torch.nn.Tanh(), torch.nn.Linear(5, 3)).to(device=dev, dtype=torch.float64)
        inputs = torch.randn((4, 3), dtype=torch.float64).to(dev)
    params = tuple(model.parameters())
    before = torch.cat([p.detach().flatten().clone() for p in params])
    optimizer = torch.optim.SGD(params, lr=.02)
    reference_error = protected_error = 0.
    projection_count = 0
    weights = (.25, .75)
    for _ in range(3):
        optimizer.zero_grad(set_to_none=True)
        outputs = model(inputs)
        # Different supervised targets instantiate the paper's generic pair of
        # differentiable objectives; these are NOT simulated agent rewards.
        first_losses = [torch.nn.functional.cross_entropy(row, torch.zeros(len(row), dtype=torch.long, device=dev)) for row in outputs.split(2)]
        second_losses = [torch.nn.functional.cross_entropy(row, torch.ones(len(row), dtype=torch.long, device=dev)) for row in outputs.split(2)]
        g1 = [objective_gradients(loss, params) for loss in first_losses]
        g2 = [objective_gradients(loss, params) for loss in second_losses]
        combined, audit = accumulate_gradients(g1, g2, weights, weight=.7)
        # Independent total-loss gradients, scalar CPU dot products, then the
        # closed form; no call to combine_gradients in the reference branch.
        total1 = sum(w * loss for w, loss in zip(weights, first_losses))
        total2 = sum(w * loss for w, loss in zip(weights, second_losses))
        ra = objective_gradients(total1, params)
        rb = .7 * objective_gradients(total2, params)
        av, bv = ra.tolist(), rb.tolist()
        dot = sum(x * y for x, y in zip(av, bv))
        norm = sum(x * x for x in av)
        coefficient = dot / norm if norm > 0 and dot < 0 else 0.
        reference = torch.tensor([x + y - coefficient * x for x, y in zip(av, bv)], dtype=torch.float64, device=dev)
        reference_error = max(reference_error, float((combined - reference).abs().max()))
        expected_progress = norm + max(dot, 0.)
        protected_error = max(protected_error, abs(float(torch.dot(ra, combined)) - expected_progress))
        projection_count += int(audit["projected"])
        offset = 0
        for p in params:
            p.grad = combined[offset:offset + p.numel()].reshape_as(p).clone()
            offset += p.numel()
        optimizer.step()
    # A negative control that changes ONLY projection placement, not the total
    # objective or its fixed micro-batch weights.
    a = [torch.tensor(v, dtype=torch.float64, device=dev) for v in ([1., 0.], [0., 1.])]
    b = [torch.tensor(v, dtype=torch.float64, device=dev) for v in ([-2., 1.], [1., -2.])]
    correct, _ = accumulate_gradients(a, b, (.5, .5))
    wrong = sum((.5 * combine_gradients(x, y)[0] for x, y in zip(a, b)), torch.zeros_like(a[0]))
    placement_gap = float((correct - wrong).abs().max())
    aligned = torch.tensor([1., 2.], dtype=torch.float64, device=dev)
    conflict, _ = combine_gradients(aligned, aligned, gate="conflict-only")
    always, _ = combine_gradients(aligned, aligned, gate="always")
    after = torch.cat([p.detach().flatten() for p in params])
    return {"seed": seed, "metrics": {"optimizer_updates": 3, "micro_batches_per_update": 2,
            "projection_count": projection_count, "gradient_reference_error": reference_error,
            "protected_first_order_error": protected_error,
            "per_micro_projection_negative_gap": placement_gap,
            "always_vs_conflict_gate_gap": float((always - conflict).norm()),
            "student_parameter_delta": float((after - before).norm()), "final_first_loss": float(total1.detach()),
            "final_second_loss": float(total2.detach())},
            "checks": {"three_real_updates": bool((after - before).norm() > 0),
                       "independent_gradient_reference": reference_error < 1e-10,
                       "protected_first_order_identity": protected_error < 1e-10,
                       "accumulate_before_project_negative_control": placement_gap > .1,
                       "always_differs_on_aligned_gradients": bool((always - conflict).norm() > .1),
                       "no_optimizer_direction_guarantee_claim": True}}
