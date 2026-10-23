"""GIFT logit-space gradient geometry, exact-quota selection and loss kernel.

Independent implementation from paper Equations 1/2/8/10/11/28/29. This bounded
component is not the distributed trainer and does not measure reasoning ability.
The teacher is training-only, its target and selection decisions are detached.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def coverage_ratio(step: int, *, hold_steps: int = 10, exit_step: int = 78) -> float:
    """Equation 30: full coverage through hold, exactly zero at teacher exit."""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (step, hold_steps, exit_step)):
        raise ValueError("integer schedule positions required")
    if step < 1 or not 0 <= hold_steps < exit_step:
        raise ValueError("step>=1 and 0<=hold<exit required")
    if step <= hold_steps:
        return 1.
    return max(0., (exit_step - step) / (exit_step - hold_steps))


def gradient_geometry(rl_gradient: Tensor, teacher_gradient: Tensor,
                      actor_mask: Tensor, *, norm_epsilon: float = 1e-8) -> dict:
    """Equations 2/8: score conflict by a, safe novelty by b, zero-RL by 0."""
    if rl_gradient.ndim != 3 or rl_gradient.shape != teacher_gradient.shape or min(rl_gradient.shape) < 1:
        raise ValueError("aligned nonempty [rollout,token,vocabulary] gradients required")
    if not rl_gradient.is_floating_point() or teacher_gradient.dtype != rl_gradient.dtype or teacher_gradient.device != rl_gradient.device:
        raise ValueError("floating gradients must match dtype/device")
    if actor_mask.shape != rl_gradient.shape[:2] or actor_mask.dtype != torch.bool or actor_mask.device != rl_gradient.device:
        raise ValueError("aligned Boolean actor mask required")
    if not math.isfinite(norm_epsilon) or norm_epsilon <= 0:
        raise ValueError("positive finite gradient tolerance required")
    if not bool(torch.isfinite(rl_gradient[actor_mask]).all()) or not bool(torch.isfinite(teacher_gradient[actor_mask]).all()):
        raise ValueError("finite active gradients required")
    dtype = torch.float32 if rl_gradient.dtype in (torch.float16, torch.bfloat16) else rl_gradient.dtype
    active = actor_mask[..., None]
    r = torch.where(active, rl_gradient.detach().to(dtype), 0.)
    d = torch.where(active, teacher_gradient.detach().to(dtype), 0.)
    r_norm, d_norm = r.norm(dim=-1), d.norm(dim=-1)
    if not bool(torch.isfinite(r_norm).all()) or not bool(torch.isfinite(d_norm).all()):
        raise ValueError("gradient norms must be representable")
    usable = actor_mask & (r_norm > norm_epsilon)
    direction = r / r_norm.clamp_min(norm_epsilon)[..., None]
    a = (d * direction).sum(-1)
    perpendicular = d - a[..., None] * direction
    b = perpendicular.norm(dim=-1)
    a, b = torch.where(usable, a, 0.), torch.where(usable, b, 0.)
    score = torch.where(usable, torch.where(a < 0, a, b), 0.)
    eligible = actor_mask & (d_norm > norm_epsilon)
    return {"parallel": a, "orthogonal": b, "score": score,
            "usable_rl": usable, "eligible": eligible, "rl_norm": r_norm,
            "teacher_norm": d_norm}


def exact_quota_mask(scores: Tensor, eligible: Tensor, actor_mask: Tensor,
                     retention: float) -> Tensor:
    """Equation 29 for ONE actor training sub-batch (all supplied tokens).

    Quota is floor(retention * ALL valid tokens), capped by eligible count.
    Conflicts can be selected when the quota exceeds non-conflicting capacity.
    Equal scores use flattened input order; no correctness/gold is consulted.
    """
    if scores.ndim != 2 or scores.shape != eligible.shape or scores.shape != actor_mask.shape:
        raise ValueError("aligned token-score and mask matrices required")
    if not scores.is_floating_point() or eligible.dtype != torch.bool or actor_mask.dtype != torch.bool:
        raise ValueError("floating scores and Boolean masks required")
    if scores.device != eligible.device or scores.device != actor_mask.device:
        raise ValueError("selection inputs must share a device")
    if bool((eligible & ~actor_mask).any()) or not bool(torch.isfinite(scores[eligible]).all()):
        raise ValueError("eligible scores must be finite valid response tokens")
    if not math.isfinite(retention) or not 0 <= retention <= 1:
        raise ValueError("retention must lie in [0,1]")
    quota = min(math.floor(retention * int(actor_mask.sum())), int(eligible.sum()))
    selected = torch.zeros_like(actor_mask)
    indices = torch.nonzero(eligible.flatten(), as_tuple=False).flatten()
    if quota:
        ranked = torch.argsort(scores.detach().flatten()[indices], descending=True, stable=True)
        selected.flatten()[indices[ranked[:quota]]] = True
    return selected


def gift_loss(student_logits: Tensor, teacher_logits: Tensor, old_action_log_probs: Tensor,
              actions: Tensor, advantages: Tensor, actor_mask: Tensor, *, step: int,
              hold_steps: int = 10, exit_step: int = 78, clip_epsilon: float = .2,
              teacher_top_k: int = 100, norm_epsilon: float = 1e-8) -> tuple[Tensor, dict]:
    """Unit-weight GRPO + GIFT for one sub-batch; no extra rollout IS weights.

    Teacher top-k tokens plus one tail bucket instantiate Equation 28 exactly.
    Geometry is computed in ORIGINAL vocabulary logit space, not bucket space.
    The retained teacher loss is unprojected, lambda=1, denominator=N_valid.
    ``teacher_top_k>=V`` is the exact full-vocabulary reference case.
    """
    if student_logits.ndim != 3 or min(student_logits.shape) < 1 or teacher_logits.shape != student_logits.shape:
        raise ValueError("aligned nonempty [rollout,token,vocabulary] logits required")
    if not student_logits.is_floating_point() or teacher_logits.dtype != student_logits.dtype or teacher_logits.device != student_logits.device:
        raise ValueError("floating student/teacher logits must match dtype/device")
    shape = student_logits.shape[:2]
    if actor_mask.shape != shape or actor_mask.dtype != torch.bool or not bool(actor_mask.any()):
        raise ValueError("nonempty Boolean actor mask required")
    if actions.shape != shape or actions.dtype != torch.long or old_action_log_probs.shape != shape or advantages.shape != shape:
        raise ValueError("aligned actions, old log probabilities and token advantages required")
    if any(value.device != student_logits.device for value in (actor_mask, actions, old_action_log_probs, advantages)):
        raise ValueError("all GIFT inputs must share a device")
    if not old_action_log_probs.is_floating_point() or not advantages.is_floating_point():
        raise ValueError("floating old log probabilities and advantages required")
    if any(not bool(torch.isfinite(value[actor_mask]).all()) for value in (student_logits, teacher_logits, old_action_log_probs, advantages)):
        raise ValueError("finite active logits, log probabilities and advantages required")
    if bool((old_action_log_probs[actor_mask] > 0).any()):
        raise ValueError("old action log probabilities must be nonpositive")
    if not bool(((actions[actor_mask] >= 0) & (actions[actor_mask] < student_logits.shape[-1])).all()):
        raise ValueError("active actions must be in vocabulary")
    if not math.isfinite(clip_epsilon) or not 0 < clip_epsilon < 1:
        raise ValueError("clipping epsilon must lie in (0,1)")
    if isinstance(teacher_top_k, bool) or not isinstance(teacher_top_k, int) or teacher_top_k < 1:
        raise ValueError("positive integer teacher top-k required")
    retention = coverage_ratio(step, hold_steps=hold_steps, exit_step=exit_step)
    dtype = torch.float32 if student_logits.dtype in (torch.float16, torch.bfloat16) else student_logits.dtype
    active = actor_mask[..., None]
    logp = torch.where(active, student_logits.to(dtype), 0.).log_softmax(-1)
    logq = torch.where(active, teacher_logits.detach().to(dtype), 0.).log_softmax(-1)
    if not bool(torch.isfinite(logp[actor_mask]).all()) or not bool(torch.isfinite(logq[actor_mask]).all()):
        raise ValueError("active log probabilities must be representable")
    p, q = logp.exp(), logq.exp()
    safe_actions = torch.where(actor_mask, actions, 0).unsqueeze(-1)
    log_action = logp.gather(-1, safe_actions).squeeze(-1)
    old = torch.where(actor_mask, old_action_log_probs.detach().to(dtype), 0.)
    advantage = torch.where(actor_mask, advantages.detach().to(dtype), 0.)
    ratio = (log_action - old).exp()
    if not bool(torch.isfinite(ratio[actor_mask]).all()):
        raise ValueError("active PPO ratios must be representable")
    token_rl = -torch.minimum(ratio * advantage,
                               ratio.clamp(1 - clip_epsilon, 1 + clip_epsilon) * advantage)
    active_branch = ((advantage >= 0) & (ratio <= 1 + clip_epsilon)) | ((advantage < 0) & (ratio >= 1 - clip_epsilon))
    one_hot = torch.nn.functional.one_hot(safe_actions.squeeze(-1), student_logits.shape[-1]).to(dtype)
    r = (advantage * ratio * active_branch)[..., None] * (p - one_hot)
    if teacher_top_k >= student_logits.shape[-1]:
        token_kl = (q * (logq - logp)).sum(-1)
        d = p - q
    else:
        indices = torch.topk(logq, teacher_top_k, dim=-1).indices
        support = torch.zeros_like(logq, dtype=torch.bool).scatter(-1, indices, True)
        logp_tail = logp.masked_fill(support, -torch.inf).logsumexp(-1)
        logq_tail = logq.masked_fill(support, -torch.inf).logsumexp(-1)
        # Sum tail probabilities directly in log space, avoiding 1-sum cancellation.
        token_kl = torch.where(support, q * (logq - logp), 0.).sum(-1)
        token_kl = token_kl + logq_tail.exp() * (logq_tail - logp_tail)
        effective_teacher = torch.where(support, q,
            (logp - logp_tail[..., None] + logq_tail[..., None]).exp())
        d = p - effective_teacher
    geometry = gradient_geometry(r, d, actor_mask, norm_epsilon=norm_epsilon)
    selected = exact_quota_mask(geometry["score"], geometry["eligible"], actor_mask, retention)
    valid_count = actor_mask.sum()
    rl_loss = torch.where(actor_mask, token_rl, 0.).sum() / valid_count
    teacher_loss = torch.where(selected, token_kl, 0.).sum() / valid_count
    loss = rl_loss + teacher_loss
    return loss, {**geometry, "selected": selected, "retention": retention,
                  "rl_gradient": r.detach(), "teacher_gradient": d.detach(),
                  "token_kl": token_kl.detach(), "rl_loss": rl_loss.detach(),
                  "teacher_loss": teacher_loss.detach(), "valid_count": int(valid_count)}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Bounded real backward/update, not a reasoning benchmark."""
    generator = torch.Generator(device=device).manual_seed(seed)
    logits = torch.randn(4, 3, 7, generator=generator, device=device, dtype=torch.float64).requires_grad_()
    teacher = torch.randn(4, 3, 7, generator=generator, device=device, dtype=torch.float64).requires_grad_()
    actions = torch.multinomial(logits.detach().softmax(-1).reshape(-1, 7), 1,
                                generator=generator).reshape(4, 3)
    old = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).requires_grad_()
    advantage = torch.tensor([1., -1., .5, -.5], device=device, dtype=torch.float64)[:, None].expand(4, 3).clone().requires_grad_()
    mask = torch.ones(4, 3, device=device, dtype=torch.bool)
    before = logits.detach().clone()
    loss, audit = gift_loss(logits, teacher, old, actions, advantage, mask,
                            step=44, teacher_top_k=3)
    logp, logq = logits.log_softmax(-1), teacher.detach().log_softmax(-1)
    p, q = logp.exp(), logq.exp()
    support = torch.zeros_like(p, dtype=torch.bool).scatter(-1, torch.topk(q, 3, -1).indices, True)
    p_tail, q_tail = torch.where(support, 0., p).sum(-1), torch.where(support, 0., q).sum(-1)
    reference_kl = torch.where(support, q * (logq - logp), 0.).sum(-1) + q_tail * (q_tail / p_tail).log()
    reference_d = torch.autograd.grad(reference_kl.sum(), logits, retain_graph=True)[0]
    sampled_log = logp.gather(-1, actions[..., None]).squeeze(-1)
    reference_rl = -(sampled_log - old.detach()).exp() * advantage.detach()
    reference_r = torch.autograd.grad(reference_rl.sum(), logits, retain_graph=True)[0]
    reference_error = float(torch.maximum((reference_d - audit["teacher_gradient"]).abs().max(),
                                          (reference_r - audit["rl_gradient"]).abs().max()).detach())
    loss.backward()
    gradient = logits.grad.detach().clone()
    with torch.no_grad():
        logits -= .001 * gradient
    delta = float((logits.detach() - before).norm())
    selected = int(audit["selected"].sum())
    quota = min(math.floor(audit["retention"] * audit["valid_count"]), int(audit["eligible"].sum()))
    return {"seed": seed, "diagnostic_only": True, "component": "gradient_geometry_exact_quota_loss_kernel",
            "metrics": {"loss": float(loss.detach()), "gradient_norm": float(gradient.norm()),
                "parameter_delta": delta, "selected_tokens": selected,
                "valid_tokens": audit["valid_count"], "retention": audit["retention"],
                "formula_reference_error": reference_error, "optimizer_updates": 1, "model_calls": 0},
            "checks": {"finite_gradient": bool(gradient.isfinite().all()), "teacher_detached": teacher.grad is None,
                "old_policy_detached": old.grad is None, "advantages_detached": advantage.grad is None,
                "real_parameter_update": delta > 0, "formula_reference_matches": reference_error < 1e-10,
                "exact_quota": selected == quota, "selection_detached": not audit["score"].requires_grad}}
