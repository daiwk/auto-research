"""RLiD decision-plane policy/PPO and same-policy credit audit (2611.02455).

This module consumes aligned numerical label logits, not privileged simulator
states or gold plans. It is not an LDM backbone, task compiler or ALFWorld agent.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/rlid-a100-20261104.json"


def menu_log_probabilities(label_logits: Tensor, menu_mask: Tensor, *, calibration: Tensor | None = None) -> Tensor:
    """Equation 1: softmax over executable single-token menu labels only.

    Content-independent calibration is an external frozen snapshot. Its update
    schedule cannot be inferred or fabricated by this numerical readout.
    """
    if label_logits.ndim != 2 or min(label_logits.shape) < 1 or not label_logits.is_floating_point():
        raise ValueError("nonempty floating [decision,label] logits required")
    if menu_mask.shape != label_logits.shape or menu_mask.dtype != torch.bool or menu_mask.device != label_logits.device or not bool(menu_mask.any(-1).all()):
        raise ValueError("a nonempty Boolean executable menu per decision required")
    if not bool(torch.isfinite(label_logits[menu_mask]).all()):
        raise ValueError("finite active label logits required")
    dtype = torch.float32 if label_logits.dtype in (torch.float16, torch.bfloat16) else label_logits.dtype
    values = label_logits.to(dtype)
    if calibration is not None:
        if calibration.shape != values.shape or calibration.device != values.device or not calibration.is_floating_point() or not bool(torch.isfinite(calibration[menu_mask]).all()):
            raise ValueError("aligned finite active frozen calibration required")
        # Sanitize padding before arithmetic: inactive NaNs cannot enter grads.
        values = torch.where(menu_mask, values, 0.) - torch.where(menu_mask, calibration.detach().to(dtype), 0.)
    values = torch.where(menu_mask, values, -torch.inf)
    return values.log_softmax(-1)


def decision_ppo_loss(label_logits: Tensor, menu_mask: Tensor, actions: Tensor,
                      old_log_probabilities: Tensor, advantages: Tensor, *,
                      calibration: Tensor | None = None, clip_epsilon: float = .2,
                      weights: Tensor | None = None) -> Tensor:
    """Equation 2, mean over supplied decisions; no fabricated advantage source.

    Optional frozen weights implement externally supplied episode balancing.
    With weights=T_mean/T_episode the decision mean gives equal episode weight.
    It is NOT normalized again by sum(weights), silently changing the objective.
    """
    logp = menu_log_probabilities(label_logits, menu_mask, calibration=calibration)
    batch = label_logits.shape[0]
    if actions.shape != (batch,) or actions.dtype != torch.long or actions.device != label_logits.device:
        raise ValueError("one int64 sampled action per decision required")
    if bool(((actions < 0) | (actions >= label_logits.shape[1])).any()) or not bool(menu_mask.gather(1, actions[:, None]).all()):
        raise ValueError("sampled actions must belong to their executable menus")
    if not math.isfinite(clip_epsilon) or not 0 < clip_epsilon < 1:
        raise ValueError("clip_epsilon must be finite in (0,1)")
    for values in (old_log_probabilities, advantages):
        if values.shape != (batch,) or values.device != label_logits.device or not values.is_floating_point() or not bool(torch.isfinite(values).all()):
            raise ValueError("aligned finite frozen old logp and advantages required")
    if bool((old_log_probabilities > 0).any()):
        raise ValueError("old log probabilities cannot be positive")
    chosen = logp.gather(1, actions[:, None]).squeeze(1)
    ratios = (chosen - old_log_probabilities.detach().to(chosen.dtype)).exp()
    if not bool(torch.isfinite(ratios).all()):
        raise ValueError("PPO ratio is not representable; do not silently cap it")
    frozen_advantages = advantages.detach().to(chosen.dtype)
    losses = -torch.minimum(ratios * frozen_advantages,
                            ratios.clamp(1 - clip_epsilon, 1 + clip_epsilon) * frozen_advantages)
    if weights is not None:
        if weights.shape != (batch,) or weights.device != label_logits.device or not weights.is_floating_point() or not bool(torch.isfinite(weights).all()) or bool((weights < 0).any()) or not bool((weights > 0).any()):
            raise ValueError("aligned finite nonnegative decision weights required")
        losses = losses * weights.detach().to(chosen.dtype)
    if not bool(torch.isfinite(losses).all()):
        raise ValueError("surrogate loss is not representable")
    return losses.mean()


def marginal_label_penalty(label_logits: Tensor, menu_mask: Tensor) -> Tensor:
    """Sec.2's KL(uniform || mean policy), grouped by identical menu support.

    Caller must supply consistently aligned label columns and separately decide
    the coefficient. This is not entropy per decision or KL(mean || uniform).
    """
    log_probabilities = menu_log_probabilities(label_logits, menu_mask)
    penalties = []
    for support in torch.unique(menu_mask, dim=0):
        rows = (menu_mask == support).all(-1)
        log_marginal = torch.logsumexp(log_probabilities[rows][:, support], dim=0) - math.log(int(rows.sum()))
        count = int(support.sum())
        penalties.append((-math.log(count) - log_marginal).mean())
    # Local explicit reduction: each support group contributes equally.
    return torch.stack(penalties).mean()


def credit_variance_audit(text_logits: Tensor, action_of_text: Tensor, action_advantages: Tensor) -> dict[str, Tensor]:
    """Enumerate Proposition 1 exactly within ONE categorical text policy.

    Scores use the full-text softmax logits as coordinates. Advantages depend
    only on actions. This identity does not compare differently trained LDMs
    and generative models, and says nothing about temporal credit estimation.
    """
    if text_logits.ndim != 1 or text_logits.numel() < 2 or not text_logits.is_floating_point() or not bool(torch.isfinite(text_logits).all()):
        raise ValueError("finite text-logit vector required")
    if action_of_text.shape != text_logits.shape or action_of_text.dtype != torch.long or action_of_text.device != text_logits.device:
        raise ValueError("aligned int64 action mapping required")
    if action_advantages.ndim != 1 or action_advantages.numel() < 1 or action_advantages.device != text_logits.device or not action_advantages.is_floating_point() or not bool(torch.isfinite(action_advantages).all()):
        raise ValueError("finite action-conditioned advantages required")
    if bool(((action_of_text < 0) | (action_of_text >= action_advantages.numel())).any()) or torch.unique(action_of_text).numel() != action_advantages.numel():
        raise ValueError("mapping must cover every action exactly as a partition")
    values = text_logits.detach().double()
    p = values.softmax(-1)
    conditional = torch.zeros((action_advantages.numel(), p.numel()), dtype=values.dtype, device=p.device)
    for action in range(action_advantages.numel()):
        members = action_of_text == action
        conditional[action, members] = p[members] / p[members].sum()
    text_scores = torch.eye(p.numel(), dtype=p.dtype, device=p.device) - p
    decision_scores = conditional[action_of_text] - p
    advantage = action_advantages.detach().double()[action_of_text, None]
    text_gradients = text_scores * advantage
    decision_gradients = decision_scores * advantage
    mean_text = (p[:, None] * text_gradients).sum(0)
    mean_decision = (p[:, None] * decision_gradients).sum(0)
    text_variance = (p[:, None] * (text_gradients - mean_text).square()).sum()
    decision_variance = (p[:, None] * (decision_gradients - mean_decision).square()).sum()
    realization = (p[:, None] * (text_gradients - decision_gradients).square()).sum()
    return {"mean_update_max_error": (mean_text - mean_decision).abs().max(),
            "text_variance_trace": text_variance, "decision_variance_trace": decision_variance,
            "realization_second_moment": realization,
            "variance_identity_error": (text_variance - decision_variance - realization).abs()}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Synthetic logits with real autograd; no environment/gold/model calls."""
    generator = torch.Generator(device="cpu").manual_seed(seed)
    logits = torch.randn(4, 4, generator=generator, dtype=torch.float64).to(device).requires_grad_()
    menu = torch.tensor([[1, 1, 0, 0], [1, 1, 1, 0], [1, 1, 0, 0], [1, 1, 1, 0]], dtype=torch.bool, device=device)
    calibration = torch.zeros_like(logits, requires_grad=True)
    actions = torch.tensor([0, 1, 1, 2], device=device)
    old = menu_log_probabilities(logits.detach(), menu).gather(1, actions[:, None]).squeeze(1).requires_grad_()
    advantages = torch.tensor([1., -.6, -.3, .8], dtype=torch.float64, device=device, requires_grad=True)
    loss = decision_ppo_loss(logits, menu, actions, old, advantages, calibration=calibration)
    loss.backward()
    gradient = logits.grad.detach().clone()
    after = decision_ppo_loss(logits.detach() - .01 * gradient, menu, actions, old, advantages, calibration=calibration)
    probability = menu_log_probabilities(logits.detach(), menu).exp()
    text = torch.randn(6, generator=generator, dtype=torch.float64).to(device)
    audit = credit_variance_audit(text, torch.tensor([0, 0, 1, 1, 2, 2], device=device), torch.tensor([1., -.5, .2], device=device))
    constant = torch.ones_like(logits)
    uniform_penalty = marginal_label_penalty(constant, menu)
    checks = {"only_menu_actions_have_mass": bool((probability[~menu] == 0).all()),
              "menu_mass_one": bool(torch.allclose(probability.sum(-1), torch.ones(4, dtype=torch.float64, device=device))),
              "gradient_finite_nonzero": bool(torch.isfinite(gradient).all()) and float(gradient.norm()) > 0,
              "padding_gradient_zero": bool((gradient[~menu] == 0).all()),
              "old_advantage_calibration_frozen": old.grad is None and advantages.grad is None and calibration.grad is None,
              "small_update_decreases_surrogate": float(after.detach()) < float(loss.detach()),
              "same_policy_expected_update_preserved": float(audit["mean_update_max_error"]) < 1e-10,
              "realization_variance_identity": float(audit["variance_identity_error"]) < 1e-10,
              "realization_variance_positive": float(audit["realization_second_moment"]) > 0,
              "uniform_label_penalty_zero": abs(float(uniform_penalty)) < 1e-10}
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"loss": float(loss.detach()), "loss_after": float(after.detach()), "gradient_norm": float(gradient.norm()), **{key: float(value) for key, value in audit.items()}, "model_calls": 0}, "checks": checks}
