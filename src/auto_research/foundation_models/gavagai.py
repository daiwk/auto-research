"""GAVAGAI's capped word-region transport, arXiv:2611.00319 Eqs. 1–3.

This component accepts caller-provided embeddings/capacities and optional cost
priors. It does not implement SAYCam preprocessing, its learned word filter,
cross-scene tally estimation, or the paper's four-A100 training experiment.
"""
from __future__ import annotations

import math

import torch
from torch import nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def _finite_matrix(value: torch.Tensor, name: str) -> None:
    if value.ndim != 2 or min(value.shape) < 1 or value.dtype not in (torch.float32, torch.float64):
        raise ValueError(f"{name} must be a nonempty FP32/FP64 matrix")
    if not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} must be finite")


@torch.no_grad()
def capped_transport(cost: torch.Tensor, capacities: torch.Tensor, *, epsilon: float = .05,
                     iterations: int = 8) -> torch.Tensor:
    """Log-domain Eq.2. Column 0 is uncapped Nothing, not a visual region.

    Finite iterations need not satisfy row equalities exactly after the final
    column scaling. Do not renormalize rows afterward: that can violate caps.
    Callers must inspect residuals before treating the plan as converged.
    """
    _finite_matrix(cost, "cost")
    if cost.shape[1] < 2 or capacities.shape != (cost.shape[1] - 1,):
        raise ValueError("cost needs Nothing plus >=1 region, with one capacity per region")
    if (capacities.dtype != cost.dtype or capacities.device != cost.device
            or not bool(torch.isfinite(capacities).all()) or bool((capacities < 0).any())):
        raise ValueError("capacities must be finite, nonnegative and match cost dtype/device")
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("finite positive epsilon required")
    if isinstance(iterations, bool) or not isinstance(iterations, int) or iterations < 1:
        raise ValueError("iterations must be a positive integer")
    log_k = -cost / epsilon
    if not bool(torch.isfinite(log_k).all()):
        raise ValueError("cost/epsilon overflow; use a representable scale")
    log_v = torch.zeros(cost.shape[1], dtype=cost.dtype, device=cost.device)
    log_b = capacities.log()  # zero capacity deliberately gives -inf.
    for _ in range(iterations):
        log_u = -torch.logsumexp(log_k + log_v[None], dim=1)
        denominator = torch.logsumexp(log_k + log_u[:, None], dim=0)
        log_v = torch.cat((cost.new_zeros(1), torch.minimum(cost.new_zeros(capacities.shape), log_b - denominator[1:])))
    return (log_u[:, None] + log_k + log_v[None]).exp()


def alignment_objective(cost: torch.Tensor, plan: torch.Tensor, caption_ce: torch.Tensor, *,
                        coefficient: float = .1, nothing_target: float = .6,
                        nothing_penalty: float = .01) -> dict[str, torch.Tensor]:
    """Eq.3 with fixed P*, plus the disclosed mean-Nothing hinge penalty.

    The paper's transport term is a SUM, not a token-normalized mean. The
    Nothing penalty also uses detached assignments here, and thus is a value
    diagnostic, not an invented extra gradient through the solver. The v1 text
    does not specify an alternative differentiable path for that penalty.
    """
    _finite_matrix(cost, "cost")
    if (plan.shape != cost.shape or plan.dtype != cost.dtype or plan.device != cost.device
            or not bool(torch.isfinite(plan).all()) or bool((plan < 0).any())):
        raise ValueError("nonnegative finite same-shape/device/dtype plan required")
    if (caption_ce.numel() != 1 or caption_ce.device != cost.device or caption_ce.dtype != cost.dtype
            or not bool(torch.isfinite(caption_ce).all())):
        raise ValueError("finite scalar caption cross-entropy with matching dtype/device required")
    if (not all(math.isfinite(v) for v in (coefficient, nothing_target, nothing_penalty))
            or coefficient < 0 or not 0 <= nothing_target <= 1 or nothing_penalty < 0):
        raise ValueError("nonnegative finite coefficients and 0 <= Nothing target <= 1 required")
    fixed = plan.detach()
    alignment = (fixed * cost).sum()
    penalty = (fixed[:, 0].mean() - nothing_target).clamp_min(0) * nothing_penalty
    return {"total": caption_ce + coefficient * alignment + penalty,
            "alignment": alignment, "nothing_penalty": penalty}


class ReferentialAlignment(nn.Module):
    """Learned two-layer Nothing head and normalized word-region costs.

    Region proposals, content-word filtering and any cross-scene prior are
    caller inputs. Word and region representations must share a dimension.
    """

    def __init__(self, dimension: int, *, temperature: float = .07):
        super().__init__()
        if isinstance(dimension, bool) or not isinstance(dimension, int) or dimension < 1:
            raise ValueError("positive integer embedding dimension required")
        if not math.isfinite(temperature) or temperature <= 0:
            raise ValueError("finite positive temperature required")
        self.temperature = temperature
        self.nothing_head = nn.Sequential(nn.Linear(dimension, dimension), nn.GELU(), nn.Linear(dimension, 1))

    def forward(self, words: torch.Tensor, regions: torch.Tensor, capacities: torch.Tensor,
                caption_ce: torch.Tensor, *, prior: torch.Tensor | None = None,
                epsilon: float = .05, iterations: int = 8) -> dict[str, torch.Tensor]:
        _finite_matrix(words, "words")
        _finite_matrix(regions, "regions")
        if (words.shape[1] != regions.shape[1] or words.device != regions.device or words.dtype != regions.dtype
                or words.shape[1] != self.nothing_head[0].in_features):
            raise ValueError("compatible same-device word/region embeddings required")
        if bool((words.norm(dim=-1) == 0).any()) or bool((regions.norm(dim=-1) == 0).any()):
            raise ValueError("zero-norm word/region embeddings have undefined unit normalization")
        visual = -(F.normalize(words, dim=-1) @ F.normalize(regions, dim=-1).T) / self.temperature
        cost = torch.cat((self.nothing_head(words), visual), dim=1)
        if prior is not None:
            if (prior.shape != cost.shape or prior.dtype != cost.dtype or prior.device != cost.device
                    or not bool(torch.isfinite(prior).all()) or prior.requires_grad):
                raise ValueError("prior must be fixed finite same-shape/device/dtype external cost prior")
            cost = cost + prior
        plan = capped_transport(cost, capacities, epsilon=epsilon, iterations=iterations)
        return {"cost": cost, "plan": plan, **alignment_objective(cost, plan, caption_ce)}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Synthetic operator diagnostic, not vocabulary grounding accuracy."""
    generator = torch.Generator(device=device).manual_seed(seed)
    cost = torch.randn((4, 2), generator=generator, dtype=torch.float64, device=device) * .03
    capacity = cost.new_tensor([1.2])
    plan8 = capped_transport(cost, capacity)
    plan = capped_transport(cost, capacity, iterations=512)
    # Independent scalar dual bisection for one capped visual column.
    lo, hi = -100., 0.
    delta = (cost[:, 0] - cost[:, 1]) / .05
    for _ in range(100):
        middle = (lo + hi) / 2
        if float(torch.sigmoid(delta + middle).sum()) > float(capacity[0]):
            hi = middle
        else:
            lo = middle
    probability = torch.sigmoid(delta + (lo + hi) / 2)
    reference = torch.stack((1 - probability, probability), dim=1)
    error = float((plan - reference).abs().max())
    inactive = capped_transport(cost, cost.new_tensor([4.]))
    inactive_error = float((inactive - torch.softmax(-cost / .05, dim=1)).abs().max())
    zero = capped_transport(cost, cost.new_zeros(1))
    leaf = cost.detach().clone().requires_grad_()
    external = plan.detach().clone().requires_grad_()
    ce = cost.new_tensor(.7, requires_grad=True)
    loss = alignment_objective(leaf, external, ce)["total"]
    loss.backward()
    gradient_error = float((leaf.grad - .1 * plan).abs().max())
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"scalar_dual_max_error": error, "inactive_cap_softmax_error": inactive_error,
                        "envelope_gradient_error": gradient_error,
                        "eight_iteration_row_residual": float((plan8.sum(1) - 1).abs().max()),
                        "eight_iteration_capacity_excess": float((plan8[:, 1:].sum(0) - capacity).clamp_min(0).max()),
                        "converged_row_residual": float((plan.sum(1) - 1).abs().max()),
                        "nothing_mass": float(plan[:, 0].mean())},
            "checks": {"scalar_dual_reference": error < 1e-9, "inactive_cap_is_row_softmax": inactive_error < 1e-10,
                       "zero_capacity_goes_to_nothing": bool((zero[:, 1] == 0).all()) and bool(torch.allclose(zero[:, 0], torch.ones_like(zero[:, 0]))),
                       "no_gradient_through_plan": external.grad is None, "envelope_gradient": gradient_error < 1e-12,
                       "caption_gradient_retained": ce.grad.item() == 1., "finite_eight_step_plan": bool(torch.isfinite(plan8).all()),
                       "capacity_bound": bool((plan8[:, 1:].sum(0) <= capacity + 1e-12).all())}}
