"""AOPD paper Equations 3.6/3.8, independently implemented loss component.

This is not an LLM trainer or capability evaluation. The caller must collect
unprivileged, on-policy student rollouts and keep reward/teacher access outside
the student. Frozen rollout probabilities, teacher targets and rewards never
receive gradients. Upstream-only residual and all-wrong KL terms are not added.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def leave_one_out_advantages(rewards: Tensor, group_ids: Tensor) -> Tensor:
    """Algorithm 1 baseline; each prompt group must contain at least two draws."""
    if rewards.ndim != 1 or group_ids.shape != rewards.shape or rewards.numel() == 0:
        raise ValueError("aligned nonempty reward and prompt-group vectors required")
    if not rewards.is_floating_point() or group_ids.dtype != torch.long:
        raise ValueError("floating rewards and integer prompt-group IDs required")
    if rewards.device != group_ids.device:
        raise ValueError("rewards and groups must share a device")
    if not bool(torch.isfinite(rewards).all()) or not bool(((rewards >= 0) & (rewards <= 1)).all()):
        raise ValueError("finite terminal rewards in [0,1] required")
    observed = rewards.detach()
    result = torch.empty_like(observed)
    for group in torch.unique(group_ids):
        members = group_ids == group
        count = int(members.sum())
        if count < 2:
            raise ValueError("leave-one-out needs at least two independent rollouts per prompt")
        values = observed[members]
        result[members] = values - (values.sum() - values) / (count - 1)
    return result


def aopd_loss(student_logits: Tensor, rollout_logits: Tensor, teacher_logits: Tensor,
              actions: Tensor, rewards: Tensor, group_ids: Tensor, actor_mask: Tensor,
              *, clip: float | None = 4.) -> tuple[Tensor, dict]:
    """Negative clipped AOPD objective, mean over per-rollout token means.

    ``rollout_logits`` are S, not the changing S_theta. The same detached
    truncated teacher measure enters both terms, without re-normalization.
    ``clip=None`` evaluates the untruncated unbiased estimator (Equation 3.6).
    There is no PPO ratio between S_theta and S in this paper objective.
    """
    if student_logits.ndim != 3 or min(student_logits.shape) < 1:
        raise ValueError("nonempty [rollout,token,vocabulary] logits required")
    for value in (rollout_logits, teacher_logits):
        if value.shape != student_logits.shape or value.dtype != student_logits.dtype or value.device != student_logits.device:
            raise ValueError("aligned floating logits with matching dtype/device required")
    if not student_logits.is_floating_point():
        raise ValueError("floating logits required")
    if actor_mask.shape != student_logits.shape[:2] or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()):
        raise ValueError("one nonempty Boolean actor mask per rollout required")
    if actions.shape != actor_mask.shape or actions.dtype != torch.long:
        raise ValueError("integer sampled actions aligned with actor mask required")
    if any(value.device != student_logits.device for value in (actions, actor_mask, rewards, group_ids)):
        raise ValueError("all AOPD inputs must share a device")
    if rewards.shape != (student_logits.shape[0],):
        raise ValueError("one terminal reward per rollout required")
    if not bool(((actions[actor_mask] >= 0) & (actions[actor_mask] < student_logits.shape[-1])).all()):
        raise ValueError("active sampled actions must be in vocabulary")
    if clip is not None and (not math.isfinite(clip) or clip <= 0):
        raise ValueError("positive finite importance cap required")
    if any(not bool(torch.isfinite(value[actor_mask]).all()) for value in (student_logits, rollout_logits, teacher_logits)):
        raise ValueError("finite active logits required")
    advantages = leave_one_out_advantages(rewards, group_ids)
    dtype = torch.float32 if student_logits.dtype in (torch.float16, torch.bfloat16) else student_logits.dtype
    active = actor_mask[..., None]
    current = torch.where(active, student_logits.to(dtype), 0.).log_softmax(-1)
    old = torch.where(active, rollout_logits.detach().to(dtype), 0.).log_softmax(-1)
    teacher = torch.where(active, teacher_logits.detach().to(dtype), 0.).log_softmax(-1)
    if not all(bool(torch.isfinite(value[actor_mask]).all()) for value in (current, old, teacher)):
        raise ValueError("active log probabilities must be representable")
    # Work in log space so capped importance ratios do not first overflow.
    target_log = teacher if clip is None else torch.minimum(teacher, old + math.log(clip))
    target = target_log.exp().detach()
    safe_actions = torch.where(actor_mask, actions, 0).unsqueeze(-1)
    sampled_log_ratio = (target_log - old).gather(-1, safe_actions).squeeze(-1)
    sampled_weight = sampled_log_ratio.exp().detach()
    if not bool(torch.isfinite(sampled_weight[actor_mask]).all()):
        raise ValueError("uncapped importance ratios are not representable; use a finite cap")
    sampled_current = current.gather(-1, safe_actions).squeeze(-1)
    teacher_expectation = (target * current).sum(-1)
    token_objective = sampled_weight * sampled_current - teacher_expectation
    sequence_objective = torch.where(actor_mask, token_objective, 0.).sum(1) / actor_mask.sum(1)
    loss = -(advantages.to(dtype) * sequence_objective).mean()
    return loss, {"advantages": advantages.detach(), "sampled_weights": sampled_weight,
                  "truncated_teacher_mass": target.sum(-1), "teacher_target": target,
                  "token_objective": token_objective.detach()}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """One genuine logit optimization step; no model/task capability claim."""
    generator = torch.Generator(device=device).manual_seed(seed)
    logits = torch.randn(4, 3, 5, generator=generator, device=device, dtype=torch.float64).requires_grad_()
    old = logits.detach().clone().requires_grad_()
    teacher = torch.randn(4, 3, 5, generator=generator, device=device, dtype=torch.float64).requires_grad_()
    actions = torch.multinomial(old.detach().softmax(-1).reshape(-1, 5), 1,
                                generator=generator).reshape(4, 3)
    rewards = torch.tensor([1., 0., 0., 1.], device=device, dtype=torch.float64)
    groups = torch.tensor([0, 0, 1, 1], device=device)
    mask = torch.ones(4, 3, device=device, dtype=torch.bool)
    before = logits.detach().clone()
    loss, audit = aopd_loss(logits, old, teacher, actions, rewards, groups, mask)
    current_log = logits.log_softmax(-1)
    reference_target = torch.minimum(teacher.detach().softmax(-1), 4 * old.detach().softmax(-1))
    sampled_target = reference_target.gather(-1, actions[..., None]).squeeze(-1)
    sampled_old = old.detach().softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    reference_terms = sampled_target / sampled_old * current_log.gather(-1, actions[..., None]).squeeze(-1)
    reference_terms -= (reference_target * current_log).sum(-1)
    reference_loss = -(torch.tensor([1., -1., -1., 1.], device=device) * reference_terms.mean(1)).mean()
    reference_error = float((loss - reference_loss).abs().detach())
    loss.backward()
    gradient = logits.grad.detach().clone()
    with torch.no_grad():
        logits -= .01 * gradient
    after, _ = aopd_loss(logits, old, teacher, actions, rewards, groups, mask)
    delta = float((logits.detach() - before).norm())
    return {"seed": seed, "diagnostic_only": True, "component": "paper_eq_3_8_loss_kernel",
            "metrics": {"loss_before": float(loss.detach()), "loss_after": float(after.detach()),
                "gradient_norm": float(gradient.norm()), "parameter_delta": delta,
                "max_sampled_weight": float(audit["sampled_weights"].max()),
                "formula_reference_error": reference_error, "optimizer_updates": 1, "model_calls": 0},
            "checks": {"teacher_detached": teacher.grad is None, "rollout_policy_detached": old.grad is None,
                "finite_gradient": bool(gradient.isfinite().all()), "real_parameter_update": delta > 0,
                "formula_reference_matches": reference_error < 1e-10,
                "bounded_step_decreases_fixed_objective": bool(after.detach() < loss.detach()),
                "clipped_measure_not_renormalized": bool((audit["truncated_teacher_mass"] <= 1 + 1e-12).all())}}
