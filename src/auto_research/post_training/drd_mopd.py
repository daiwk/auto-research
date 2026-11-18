"""DRD-MOPD (2611.13249), Sections 3.1--3.4: routed delta AdamW.

All deltas participate in every forward pass. Only UPDATE routing is changed.
This is not inference-time MoE routing, an LM, a teacher or an OPD rollout loop.
"""
from __future__ import annotations

import math
from collections.abc import Callable, Sequence
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/drd-mopd-a100-20261111.json"


def route_matrix(domains: int, mode: str, rollout_step: int, *, device: str | torch.device = "cpu", dtype: torch.dtype = torch.float64) -> Tensor:
    """Rows are input domains, columns are updated parameter components.

    Rollout steps are one-based. Other copies each gradient without division;
    SingleComponent downweights each other domain by 1/(K-1).
    """
    if type(domains) is not int or domains < 2 or type(rollout_step) is not int or rollout_step < 1:
        raise ValueError("K >= 2 and one-based rollout_step required")
    if mode == "alternate":
        mode = "other" if rollout_step % 2 else "own"
    eye = torch.eye(domains, dtype=dtype, device=device)
    if mode == "own":
        return eye
    if mode == "other":
        return 1 - eye
    if mode == "single_component":
        active = (rollout_step - 1) % domains
        result = torch.zeros_like(eye)
        result[:, active] = 1 / (domains - 1)
        result[active, active] = 1.
        return result
    raise ValueError("mode must be own, other, alternate or single_component")


class DeltaAdamW:
    """Independent full-parameter deltas, moments and selected-only Adam steps."""

    def __init__(self, base: Tensor, domains: int, *, learning_rate: float = .001,
                 betas: tuple[float, float] = (.9, .999), epsilon: float = 1e-8,
                 weight_decay: float = .01, max_grad_norm: float | None = 1.):
        if base.device.type not in {"cpu", "cuda"} or not base.is_floating_point() or not bool(torch.isfinite(base).all()) or base.numel() < 1:
            raise ValueError("finite nonempty floating CPU/CUDA base required")
        if type(domains) is not int or domains < 2 or not all(math.isfinite(v) for v in (learning_rate, *betas, epsilon, weight_decay)):
            raise ValueError("finite hyperparameters and K >= 2 required")
        if learning_rate <= 0 or epsilon <= 0 or weight_decay < 0 or any(not 0 <= b < 1 for b in betas):
            raise ValueError("invalid AdamW hyperparameters")
        if max_grad_norm is not None and (not math.isfinite(max_grad_norm) or max_grad_norm <= 0):
            raise ValueError("positive clipping threshold required")
        self.base = base.detach().clone()
        self.deltas = torch.zeros((domains, *base.shape), device=base.device, dtype=base.dtype)
        self.first = torch.zeros_like(self.deltas)
        self.second = torch.zeros_like(self.deltas)
        self.steps = torch.zeros(domains, device=base.device, dtype=torch.long)
        self.lr, self.betas, self.eps, self.decay, self.clip = learning_rate, betas, epsilon, weight_decay, max_grad_norm

    def composed(self) -> Tensor:
        return self.base + self.deltas.sum(0)

    @torch.no_grad()
    def step(self, domain_gradients: Tensor, *, mode: str, rollout_step: int, domain_weights: Tensor | None = None) -> Tensor:
        """Accumulate all domains' SAME-composite gradients before any update."""
        if domain_gradients.shape != self.deltas.shape or domain_gradients.device != self.base.device or domain_gradients.dtype != self.base.dtype or not bool(torch.isfinite(domain_gradients).all()):
            raise ValueError("finite, aligned common-snapshot domain gradients required")
        k = self.deltas.shape[0]
        route = route_matrix(k, mode, rollout_step, device=self.base.device, dtype=self.base.dtype)
        if domain_weights is not None:
            if domain_weights.shape != (k,) or domain_weights.device != self.base.device or not bool(torch.isfinite(domain_weights).all()) or bool((domain_weights < 0).any()):
                raise ValueError("finite nonnegative weights on the same device required")
            route = route * domain_weights[:, None]
        selected = route.abs().sum(0) > 0
        gradients = (route.T @ domain_gradients.reshape(k, -1)).reshape_as(self.deltas)
        b1, b2 = self.betas
        for j in range(k):
            if not bool(selected[j]):
                continue  # No counter, momentum, parameter OR weight-decay update.
            grad = gradients[j]
            if self.clip is not None:
                grad = grad * (self.clip / (grad.norm() + 1e-12)).clamp(max=1.)
            self.steps[j] += 1
            self.first[j].mul_(b1).add_(grad, alpha=1 - b1)
            self.second[j].mul_(b2).addcmul_(grad, grad, value=1 - b2)
            n = int(self.steps[j])
            moment = self.first[j] / (1 - b1 ** n)
            variance = self.second[j] / (1 - b2 ** n)
            self.deltas[j].mul_(1 - self.lr * self.decay)
            self.deltas[j].addcdiv_(moment, variance.sqrt() + self.eps, value=-self.lr)
        return selected

    def step_losses(self, loss_functions: Sequence[Callable[[Tensor], Tensor]], *, mode: str, rollout_step: int, domain_weights: Tensor | None = None) -> Tensor:
        """Convenience path enforcing a shared composed-weight gradient snapshot."""
        if len(loss_functions) != self.deltas.shape[0]:
            raise ValueError("one scalar differentiable loss function per domain required")
        weight = self.composed().detach().requires_grad_()
        gradients = []
        for loss_fn in loss_functions:
            loss = loss_fn(weight)
            if loss.ndim != 0 or not bool(torch.isfinite(loss)):
                raise ValueError("finite scalar loss required")
            gradients.append(torch.autograd.grad(loss, weight)[0].detach())
        return self.step(torch.stack(gradients), mode=mode, rollout_step=rollout_step, domain_weights=domain_weights)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if torch.device(device).type not in {"cpu", "cuda"}:
        raise ValueError("CPU or CUDA required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    base = torch.randn(5, generator=generator, dtype=torch.float64).to(device)
    router = DeltaAdamW(base, 3, learning_rate=.01, weight_decay=.1)
    targets = torch.stack((base + .5, base + 1., base + 1.5))
    losses = [lambda w, t=t: (w - t).square().mean() for t in targets]
    before_loss = float(torch.stack([fn(router.composed()) for fn in losses]).mean())
    router.step_losses(losses, mode="own", rollout_step=1)
    before = tuple(x.clone() for x in (router.deltas, router.first, router.second, router.steps))
    router.step_losses(losses, mode="single_component", rollout_step=2)
    untouched = all(torch.equal(old[[0, 2]], new[[0, 2]]) for old, new in zip(before, (router.deltas, router.first, router.second, router.steps)))
    after_loss = float(torch.stack([fn(router.composed()) for fn in losses]).mean())
    gradients = torch.randn(3, 5, generator=generator, dtype=torch.float64).to(device)
    own = route_matrix(3, "own", 1, device=device)
    other = route_matrix(3, "other", 1, device=device)
    difference = float(((other.T @ gradients).sum(0) - 2 * (own.T @ gradients).sum(0)).abs().max())
    checks = {
        "all_components_in_forward": bool(torch.equal(router.composed(), base + router.deltas.sum(0))),
        "inactive_parameters_moments_counters_unchanged": untouched,
        "selected_only_update_counts": router.steps.tolist() == [1, 2, 1],
        "other_copies_without_dividing": difference < 1e-12,
        "alternate_odd_is_other": bool(torch.equal(route_matrix(3, "alternate", 1, device=device), other)),
        "alternate_even_is_own": bool(torch.equal(route_matrix(3, "alternate", 2, device=device), own)),
        "small_component_update_reduces_probe_loss": after_loss < before_loss,
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"probe_loss_before": before_loss, "probe_loss_after": after_loss, "delta_norm": float(router.deltas.norm()), "sgd_composite_identity_error": difference, "model_calls": 0}, "checks": checks}
