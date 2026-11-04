"""ProLand (arXiv:2611.00236), exact thin-factor Algorithm 2.

Only the optimizer component is implemented. No pretrained model, GLUE run,
mixed-precision production kernel, or paper-scale training claim is included.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch

REQUIRES_GPU_VALIDATION = True


def _matrix(value: torch.Tensor, name: str) -> None:
    if value.ndim != 2 or min(value.shape) < 1 or value.dtype not in (torch.float32, torch.float64):
        raise ValueError(f"{name} must be a nonempty FP32/FP64 matrix")
    if not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")


def _pair(b: torch.Tensor, a: torch.Tensor) -> None:
    _matrix(b, "B")
    _matrix(a, "A")
    if b.shape[1] != a.shape[0] or b.device != a.device or b.dtype != a.dtype:
        raise ValueError("compatible B[m,r], A[r,n] with the same dtype/device required")


def product_projection(b: torch.Tensor, a: torch.Tensor, value: torch.Tensor) -> torch.Tensor:
    """Pi(Z)=P_B Z+(I-P_B) Z P_A, valid also for rank-deficient factors."""
    _pair(b, a)
    _matrix(value, "product matrix")
    if value.shape != (b.shape[0], a.shape[1]) or value.dtype != b.dtype or value.device != b.device:
        raise ValueError("product matrix shape, dtype and device must match B @ A")
    pb = b @ torch.linalg.pinv(b)
    pa = torch.linalg.pinv(a) @ a
    return pb @ value + (value - pb @ value) @ pa


@dataclass(frozen=True)
class ThinMomentum:
    """The retained product-space EMA is left @ right.T, width <= 2r."""
    left: torch.Tensor
    right: torch.Tensor


def _polar_factors(left: torch.Tensor, right: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    ql, lc = torch.linalg.qr(left, mode="reduced")
    qr, rc = torch.linalg.qr(right, mode="reduced")
    u, s, vh = torch.linalg.svd(lc @ rc.T, full_matrices=False)
    # The paper uses the compact polar factor, including zero and arbitrary
    # rank. Do not turn numerical null singular directions into an isometry.
    threshold = torch.finfo(s.dtype).eps * max(left.shape[0], right.shape[0]) * s.max()
    keep = s > threshold
    return ql @ u[:, keep], qr @ vh[keep].T


@torch.no_grad()
def step(b: torch.Tensor, a: torch.Tensor, grad_b: torch.Tensor, grad_a: torch.Tensor,
         momentum: ThinMomentum | None = None, *, gamma: float = .01,
         beta: float = .9, rho: float = .05) -> tuple[torch.Tensor, torch.Tensor, ThinMomentum]:
    """One simultaneous Algorithm-2 update using gradients of the SAME loss.

    gamma scales the objective direction; rho independently scales Landing.
    Returned factors and state are detached. The caller owns parameter copying.
    No weight decay or epsilon-regularized pseudoinverse is silently added.
    """
    _pair(b, a)
    for gradient, parameter, name in ((grad_b, b, "grad_B"), (grad_a, a, "grad_A")):
        _matrix(gradient, name)
        if gradient.shape != parameter.shape or gradient.dtype != b.dtype or gradient.device != b.device:
            raise ValueError("gradients must match their factor shape, dtype and device")
    if not all(math.isfinite(x) for x in (gamma, beta, rho)) or gamma <= 0 or not 0 <= beta < 1 or rho < 0:
        raise ValueError("finite gamma > 0, 0 <= beta < 1, rho >= 0 required")
    rank = b.shape[1]
    if momentum is None:
        old_ma, old_mb = torch.zeros_like(a), torch.zeros_like(b)
    else:
        left, right = momentum.left, momentum.right
        _matrix(left, "momentum.left")
        _matrix(right, "momentum.right")
        if (left.shape[0] != b.shape[0] or right.shape[0] != a.shape[1]
                or left.shape[1] != right.shape[1] or left.shape[1] > 2 * rank
                or left.device != b.device or right.device != b.device
                or left.dtype != b.dtype or right.dtype != b.dtype):
            raise ValueError("compatible same-device thin momentum of width <= 2r required")
        old_ma = (b.T @ left) @ right.T
        old_mb = left @ (right.T @ a.T)
    ma = beta * old_ma + (1 - beta) * grad_a
    mb = beta * old_mb + (1 - beta) * grad_b
    hat_a = beta * ma + (1 - beta) * grad_a
    hat_b = beta * mb + (1 - beta) * grad_b
    bp, ap = torch.linalg.pinv(b), torch.linalg.pinv(a)

    def reconstruct(ga, gb):
        return torch.cat((bp.T, gb - b @ (bp @ gb)), dim=1), torch.cat((ga.T, ap), dim=1)

    lh, rh = reconstruct(ma, mb)
    lj, rj = reconstruct(hat_a, hat_b)
    uy, vy = _polar_factors(lj, rj)
    da = (bp @ uy) @ vy.T
    db = (uy - b @ (bp @ uy)) @ (vy.T @ ap)
    gram_error = b.T @ b - torch.eye(rank, dtype=b.dtype, device=b.device)
    # Both right-hand sides use the OLD factors, not the just-updated A/B.
    return b - gamma * db - rho * b @ gram_error, a - gamma * da, ThinMomentum(lh, rh)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Small real-gradient operator checks, not a language-model benchmark."""
    generator = torch.Generator(device=device).manual_seed(seed)
    def rand(*shape):
        return torch.randn(shape, generator=generator, dtype=torch.float64, device=device)
    b = torch.linalg.qr(rand(8, 2)).Q @ torch.diag(torch.tensor([1.04, .97], dtype=torch.float64, device=device))
    a, target = rand(2, 7), rand(8, 7)
    initial_violation = float(torch.linalg.norm(b.T @ b - torch.eye(2, dtype=b.dtype, device=device)))
    state = None
    dense_h = torch.zeros_like(target)
    max_error, horizontal_error, core_width = 0., 0., 0
    initial_loss = float((b @ a - target).square().mean())
    for _ in range(4):
        g = 2 * (b @ a - target) / target.numel()
        projected = product_projection(b, a, g)
        dense_h = .9 * product_projection(b, a, dense_h) + .1 * projected
        j = .9 * dense_h + .1 * projected
        # Independent eigendecomposition, not the implementation's QR/core SVD.
        eig, vec = torch.linalg.eigh(j.T @ j)
        cutoff = (torch.finfo(j.dtype).eps * max(j.shape) * torch.linalg.norm(j, ord=2)).square()
        keep = eig > torch.maximum(cutoff, eig.max() * 1e-12)
        y = (j @ vec[:, keep] / eig[keep].sqrt()) @ vec[:, keep].T
        bp, ap = torch.linalg.pinv(b), torch.linalg.pinv(a)
        da = bp @ y
        db = (y - b @ (bp @ y)) @ ap
        expected_b = b - .005 * db - .05 * b @ (b.T @ b - torch.eye(2, dtype=b.dtype, device=device))
        expected_a = a - .005 * da
        nb, na, state = step(b, a, g @ a.T, b.T @ g, state, gamma=.005)
        max_error = max(max_error, float((nb - expected_b).abs().max()), float((na - expected_a).abs().max()),
                        float((state.left @ state.right.T - dense_h).abs().max()))
        horizontal_error = max(horizontal_error, float((b.T @ db).abs().max()))
        core_width = max(core_width, state.left.shape[1])
        b, a = nb, na
    final_violation = float(torch.linalg.norm(b.T @ b - torch.eye(2, dtype=b.dtype, device=device)))
    final_loss = float((b @ a - target).square().mean())
    z = torch.zeros_like(target)
    zero_b, zero_a, _ = step(b, a, z @ a.T, b.T @ z, gamma=.005, rho=0)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"dense_reference_max_error": max_error, "horizontal_error": horizontal_error,
                        "initial_gram_violation": initial_violation, "final_gram_violation": final_violation,
                        "initial_loss": initial_loss, "final_loss": final_loss, "momentum_width": core_width},
            "checks": {"dense_reference_agrees": max_error < 1e-8, "horizontal_direction": horizontal_error < 1e-9,
                       "landing_recovers_feasibility": final_violation < initial_violation,
                       "actual_objective_descends": final_loss < initial_loss, "thin_state": core_width <= 4,
                       "zero_gradient_no_landing_identity": torch.equal(zero_b, b) and torch.equal(zero_a, a)}}
