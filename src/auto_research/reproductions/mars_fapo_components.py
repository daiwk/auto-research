"""MARS FAPO posterior weighting and ActionMask odds (Eqs11–13).

Masks are supplied by a trusted field-span/token alignment layer; no heuristic
substring matcher impersonates the absent tokenizer or policy. No GRPO, serving
or learned reward model is executed.
"""

from __future__ import annotations
import math
import torch
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def posterior_weight(chosen: float | None, rejected: float | None, scenario_mean: float) -> float:
    if (
        isinstance(scenario_mean, bool)
        or not math.isfinite(scenario_mean)
        or not 0 < scenario_mean <= 1
    ):
        raise ValueError("positive scenario mean required")
    for value in (chosen, rejected):
        if value is not None and (
            isinstance(value, bool) or not math.isfinite(value) or not 0 <= value <= 1
        ):
            raise ValueError("historical V2P must be a probability or missing")
    if chosen is None or rejected is None:
        return 1.0
    return min(3.0, max(0.2, 1 + 2 * (chosen - rejected) / scenario_mean))


def orient_weak_pair(
    *, weak: bool, chosen: float | None, rejected: float | None, scenario_mean: float, kappa: float
) -> bool:
    posterior_weight(chosen, rejected, scenario_mean)
    if type(weak) is not bool or isinstance(kappa, bool) or not math.isfinite(kappa) or kappa < 0:
        raise ValueError("explicit evidence flag and nonnegative relative gap required")
    return bool(
        weak
        and chosen is not None
        and rejected is not None
        and rejected > chosen
        and abs(chosen - rejected) >= kappa * scenario_mean
    )


def fapo_loss(
    chosen_logp,
    rejected_logp,
    chosen_actions,
    rejected_actions,
    *,
    generation_mask=None,
    beta: float = 0.5,
    weights=None,
):
    for x in (chosen_logp, rejected_logp):
        if (
            not isinstance(x, torch.Tensor)
            or x.ndim != 2
            or not x.is_floating_point()
            or x.numel() == 0
            or not torch.isfinite(x).all()
            or not (x < 0).all()
        ):
            raise ValueError("nonempty finite strictly negative token log probabilities required")
    if (
        chosen_logp.shape[0] != rejected_logp.shape[0]
        or isinstance(beta, bool)
        or not math.isfinite(beta)
        or beta < 0
    ):
        raise ValueError("matched batch and nonnegative beta required")
    masks = (chosen_actions, rejected_actions)
    for x, mask in zip((chosen_logp, rejected_logp), masks, strict=True):
        if (
            not isinstance(mask, torch.Tensor)
            or mask.dtype != torch.bool
            or mask.shape != x.shape
            or mask.device != x.device
            or not mask.any(dim=1).all()
        ):
            raise ValueError("at least one aligned action-value token per response required")
    if generation_mask is None:
        generation_mask = torch.ones_like(chosen_actions)
    if (
        not isinstance(generation_mask, torch.Tensor)
        or generation_mask.dtype != torch.bool
        or generation_mask.shape != chosen_logp.shape
        or generation_mask.device != chosen_logp.device
        or not generation_mask.any(1).all()
        or (chosen_actions & ~generation_mask).any()
    ):
        raise ValueError("valid full-response generation mask required")
    if weights is None:
        weights = chosen_logp.new_ones(chosen_logp.shape[0])
    if (
        not isinstance(weights, torch.Tensor)
        or not weights.is_floating_point()
        or weights.device != chosen_logp.device
        or weights.dtype != chosen_logp.dtype
        or weights.shape != (chosen_logp.shape[0],)
        or not torch.isfinite(weights).all()
        or not ((weights >= 0.2) & (weights <= 3)).all()
    ):
        raise ValueError("one clipped posterior weight per pair required")
    means = [
        (x * mask).sum(1) / mask.sum(1)
        for x, mask in zip((chosen_logp, rejected_logp), masks, strict=True)
    ]
    log_odds = [g - torch.log(-torch.expm1(g)) for g in means]
    generation = -(chosen_logp * generation_mask).sum(1) / generation_mask.sum(1)
    preference = -F.logsigmoid(log_odds[0] - log_odds[1])
    return (generation + beta * weights.detach() * preference).mean()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device not in {"cpu", "cuda"}:
        raise ValueError("valid seed/device required")
    torch.manual_seed(seed)
    c = (-torch.rand(2, 5, device=device) - 0.1).requires_grad_()
    r = (-torch.rand(2, 6, device=device) - 0.1).requires_grad_()
    cm, rm = torch.zeros_like(c, dtype=torch.bool), torch.zeros_like(r, dtype=torch.bool)
    cm[:, 1:3], rm[:, 2:4] = True, True
    loss = fapo_loss(c, r, cm, rm)
    loss.backward()
    plain = fapo_loss(c.detach(), r.detach(), cm, rm, beta=0)
    weighted_plain = fapo_loss(c.detach(), r.detach(), cm, rm, beta=0, weights=c.new_full((2,), 3))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "rejected_structure_zero_gradient": bool((r.grad[~rm] == 0).all()),
            "chosen_structure_anchor_gradient": bool((c.grad[~cm] != 0).all()),
            "weight_not_on_generation": bool(torch.equal(plain, weighted_plain)),
            "strong_pair_not_reversed": not orient_weak_pair(
                weak=False, chosen=0.1, rejected=0.2, scenario_mean=0.1, kappa=0.05
            ),
            "missing_estimate_neutral": posterior_weight(None, 0.2, 0.1) == 1.0,
        },
        "metrics": {
            "fixture_fapo_loss": float(loss.detach()),
            "rejected_action_gradient_norm": float(r.grad[rm].norm()),
        },
    }
