"""Independent MOER Eq. 1, 3--6 and single-candidate rollback components.

Numerical mechanisms only: no generator, verifier, model, or capability claim.
The caller supplies verified TRAINING expert traces and observed rewards; these
must never be inserted into an evaluated agent's test-time prompt. Both prefix
and completion tokens of a guided row use the off-policy objective.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def prefix_ratio(step: int, *, anneal_steps: int = 500, warmup_steps: int = 50,
                 minimum: float = .1, maximum: float = 1.) -> float:
    """Eq. 3 during annealing; fixed author code holds the minimum afterwards.

    ``anneal_steps`` is the prefix schedule horizon, NOT a training stop step.
    """
    if any(type(value) is not int for value in (step, anneal_steps, warmup_steps)):
        raise ValueError("integer training steps required")
    if not 0 <= warmup_steps < anneal_steps or step < 0:
        raise ValueError("nonnegative step and a valid prefix annealing horizon required")
    if not all(math.isfinite(x) for x in (minimum, maximum)) or not 0 <= minimum <= maximum <= 1:
        raise ValueError("prefix ratios must satisfy 0 <= minimum <= maximum <= 1")
    if step < warmup_steps:
        return maximum
    if step >= anneal_steps:
        return minimum
    phase = (step - warmup_steps) / (anneal_steps - warmup_steps)
    return minimum + (maximum - minimum) * (.5 + .5 * math.cos(math.pi * phase))


def expert_cot_prefix(cot_tokens: tuple[int, ...], step: int, **schedule) -> tuple[int, ...]:
    """Floor-discretized CoT-only prefix; the caller must split final solution."""
    if not isinstance(cot_tokens, tuple) or any(type(token) is not int or token < 0 for token in cot_tokens):
        raise ValueError("an immutable tuple of nonnegative CoT token IDs required")
    return cot_tokens[:math.floor(len(cot_tokens) * prefix_ratio(step, **schedule))]


def selective_rollback(prefix: tuple[int, ...], completion: tuple[int, ...],
                       full_expert: tuple[int, ...], *, guided_correct: bool,
                       expert_verified: bool) -> tuple[tuple[int, ...], bool]:
    """Algorithm 1 for ONE guided candidate; verification is an external input.

    No generation or correctness inference happens here. A true verification
    flag is a caller precondition, not evidence that this function ran tests.
    There is no multi-candidate 'all fail, replace first only' extension.
    """
    for tokens in (prefix, completion, full_expert):
        if not isinstance(tokens, tuple) or any(type(t) is not int or t < 0 for t in tokens):
            raise ValueError("immutable nonnegative token-ID tuples required")
    if type(guided_correct) is not bool or type(expert_verified) is not bool:
        raise ValueError("explicit Boolean verifier outcomes required")
    if not expert_verified or not full_expert or not completion:
        raise ValueError("a verified full expert trace and nonempty completion required")
    if full_expert[:len(prefix)] != prefix:
        raise ValueError("guided prefix must belong to the full expert trace")
    return (prefix + completion, False) if guided_correct else (full_expert, True)


def mixed_group_advantages(rewards: Tensor, group_ids: Tensor, off_policy: Tensor) -> Tensor:
    """Eq. 1: center the UNION of on/off rewards, with NO std normalization.

    This component deliberately bounds itself to the author's main setting:
    one verified off-policy row and at least one unguided row per prompt.
    """
    if rewards.ndim != 1 or rewards.numel() == 0 or group_ids.shape != rewards.shape or off_policy.shape != rewards.shape:
        raise ValueError("aligned nonempty reward, prompt-group and policy vectors required")
    if not rewards.is_floating_point() or group_ids.dtype != torch.long or off_policy.dtype != torch.bool:
        raise ValueError("floating rewards, integer groups and Boolean policies required")
    if any(value.device != rewards.device for value in (group_ids, off_policy)):
        raise ValueError("group evidence must share a device")
    if not bool(torch.isfinite(rewards).all()) or not bool(((rewards >= 0) & (rewards <= 1)).all()):
        raise ValueError("finite terminal rewards in [0,1] required")
    observed = rewards.detach()
    if not bool((observed[off_policy] == 1).all()):
        raise ValueError("off-policy rows must be externally verified with reward 1")
    advantages = torch.empty_like(observed)
    for group in torch.unique(group_ids):
        members = group_ids == group
        if int(off_policy[members].sum()) != 1 or int((~off_policy[members]).sum()) < 1:
            raise ValueError("each prompt needs exactly one verified off-policy row and at least one on-policy row")
        values = observed[members]
        advantages[members] = values - values.mean()
    return advantages


def moer_loss(current_logits: Tensor, old_log_prob: Tensor, actions: Tensor,
              rewards: Tensor, group_ids: Tensor, off_policy: Tensor,
              actor_mask: Tensor, *, gamma: float = .1, alpha: float = .2,
              epsilon_low: float = .2, epsilon_high: float = .24) -> tuple[Tensor, dict]:
    """Minimize minus paper Eq. 6, normalized by ALL valid response tokens Z.

    ``old_log_prob`` is the frozen sampled-token probability of unguided rows;
    guided rows do not use it. Prompt/padding tokens must be masked out, but
    guided expert-prefix AND completion tokens must remain active. Eq. 4 uses
    the current probability in BOTH numerator and detached denominator. No
    entropy bonus, dual clipping, KL, or upstream experimental options are added.
    """
    if current_logits.ndim != 3 or min(current_logits.shape) < 1 or not current_logits.is_floating_point():
        raise ValueError("nonempty floating [rollout,token,vocabulary] logits required")
    shape = current_logits.shape[:2]
    if actor_mask.shape != shape or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()):
        raise ValueError("one nonempty Boolean actor mask per rollout required")
    if actions.shape != shape or actions.dtype != torch.long or old_log_prob.shape != shape or not old_log_prob.is_floating_point():
        raise ValueError("aligned sampled actions and floating old log probabilities required")
    if rewards.shape != (shape[0],) or off_policy.shape != rewards.shape:
        raise ValueError("one reward and policy flag per rollout required")
    if any(value.device != current_logits.device for value in (old_log_prob, actions, rewards, group_ids, off_policy, actor_mask)):
        raise ValueError("all loss inputs must share a device")
    if not math.isfinite(gamma) or not 0 < gamma <= 1 or not math.isfinite(alpha) or alpha < 0:
        raise ValueError("0 < gamma <= 1 and nonnegative finite alpha required")
    if not all(math.isfinite(x) for x in (epsilon_low, epsilon_high)) or not 0 <= epsilon_low < 1 or epsilon_high < 0:
        raise ValueError("valid nonnegative asymmetric clipping coefficients required")
    if not bool(torch.isfinite(current_logits[actor_mask]).all()):
        raise ValueError("finite active logits required")
    if not bool(((actions[actor_mask] >= 0) & (actions[actor_mask] < current_logits.shape[-1])).all()):
        raise ValueError("active actions must be within vocabulary")
    advantages = mixed_group_advantages(rewards, group_ids, off_policy)
    on_mask = actor_mask & ~off_policy[:, None]
    off_mask = actor_mask & off_policy[:, None]
    if not bool(torch.isfinite(old_log_prob[on_mask]).all()) or bool((old_log_prob[on_mask] > 0).any()):
        raise ValueError("finite nonpositive frozen on-policy log probabilities required")
    dtype = torch.float32 if current_logits.dtype in (torch.float16, torch.bfloat16) else current_logits.dtype
    clean_logits = torch.where(actor_mask[..., None], current_logits.to(dtype), 0.)
    log_probs = clean_logits.log_softmax(-1)
    safe_actions = torch.where(actor_mask, actions, 0)
    sampled_logp = log_probs.gather(-1, safe_actions[..., None]).squeeze(-1)
    if not bool(torch.isfinite(sampled_logp[actor_mask]).all()):
        raise ValueError("active log probabilities must be representable")
    frozen_old = torch.where(on_mask, old_log_prob.detach().to(dtype), 0.)
    ratio = torch.exp(torch.where(on_mask, sampled_logp - frozen_old, 0.))
    if not bool(torch.isfinite(ratio[on_mask]).all()):
        raise ValueError("on-policy importance ratios must be representable")
    advantage = advantages.to(dtype)[:, None]
    on_objective = torch.minimum(ratio * advantage,
        ratio.clamp(1 - epsilon_low, 1 + epsilon_high) * advantage)
    # Log-space evaluation prevents overflow before the trust-region cap.
    # sg is essential: even weight == 1 has NONZERO log-probability gradient.
    denominator_log = torch.maximum(sampled_logp.detach(), sampled_logp.new_tensor(math.log(gamma)))
    trust_weight = torch.exp(sampled_logp - denominator_log)
    off_objective = trust_weight * advantage
    terms = torch.where(on_mask, on_objective, 0.) + alpha * torch.where(off_mask, off_objective, 0.)
    token_count = actor_mask.sum()
    loss = -terms.sum() / token_count
    return loss, {"advantages": advantages, "on_mask": on_mask, "off_mask": off_mask,
        "on_ratio": ratio.detach(), "trust_weight": trust_weight.detach(),
        "token_objective": terms.detach(), "token_count": int(token_count)}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """True autograd/SGD on synthetic logits, NOT task or verifier evaluation."""
    generator = torch.Generator(device=device).manual_seed(seed)
    logits = torch.randn(6, 3, 5, dtype=torch.float64, device=device, generator=generator).requires_grad_()
    actions = torch.multinomial(logits.detach().softmax(-1).reshape(-1, 5), 1,
        generator=generator).reshape(6, 3)
    old = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).clone().requires_grad_()
    rewards = torch.tensor([0., 1., 1., 0., 0., 1.], device=device, dtype=torch.float64, requires_grad=True)
    groups = torch.tensor([0, 0, 0, 1, 1, 1], device=device)
    off = torch.tensor([False, False, True, False, False, True], device=device)
    mask = torch.ones(6, 3, dtype=torch.bool, device=device)
    mask[0, 2] = False
    before = logits.detach().clone()
    loss, audit = moer_loss(logits, old, actions, rewards, groups, off, mask)
    # Independent literal-probability reference to the printed equations.
    probabilities = logits.softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    expected_adv = torch.tensor([-2/3, 1/3, 1/3, -1/3, -1/3, 2/3], dtype=torch.float64, device=device)[:, None]
    on_ratio = probabilities / old.detach().exp()
    on = torch.minimum(on_ratio * expected_adv, on_ratio.clamp(.8, 1.24) * expected_adv)
    off_terms = probabilities / probabilities.detach().clamp_min(.1) * expected_adv
    reference = -(torch.where(audit["on_mask"], on, 0.) + .2 * torch.where(audit["off_mask"], off_terms, 0.)).sum() / 17
    reference_gradient = torch.autograd.grad(reference, logits, retain_graph=True)[0]
    error = float((loss.detach() - reference.detach()).abs())
    loss.backward()
    gradient = logits.grad.detach().clone()
    gradient_error = float((gradient - reference_gradient).abs().max())
    with torch.no_grad():
        logits -= .01 * gradient
    after, _ = moer_loss(logits, old, actions, rewards, groups, off, mask)
    delta = float((logits.detach() - before).norm())
    probe = torch.tensor([.04, .6], dtype=torch.float64, device=device, requires_grad=True)
    probe_gradient = torch.autograd.grad((probe / probe.detach().clamp_min(.1)).sum(), probe)[0]
    expected_probe = torch.tensor([10., 1/.6], dtype=torch.float64, device=device)
    retained, rolled = selective_rollback((1,), (2, 3), (1, 7, 8), guided_correct=True, expert_verified=True)
    replaced, failed = selective_rollback((1,), (9,), (1, 7, 8), guided_correct=False, expert_verified=True)
    return {"seed": seed, "diagnostic_only": True, "component": "paper_eq_1_3_6_single_candidate",
        "metrics": {"loss_before": float(loss.detach()), "loss_after": float(after.detach()),
            "gradient_norm": float(gradient.norm()), "parameter_delta": delta,
            "formula_reference_error": error, "gradient_reference_error": gradient_error,
            "valid_tokens": int(mask.sum()), "optimizer_updates": 1, "model_calls": 0},
        "checks": {"formula_reference_matches": error < 1e-12,
            "gradient_reference_matches": gradient_error < 1e-12,
            "old_policy_detached": old.grad is None, "rewards_detached": rewards.grad is None,
            "finite_gradient": bool(gradient.isfinite().all()), "real_parameter_update": delta > 0,
            "padding_zero_gradient": bool((gradient[~mask] == 0).all()),
            "union_group_mean_no_std": bool(torch.allclose(audit["advantages"], expected_adv[:, 0])),
            "global_token_normalization": audit["token_count"] == 17,
            "guided_completion_is_off_policy": bool(audit["off_mask"][off].all()),
            "trust_region_gradient_not_cancelled": bool(torch.allclose(probe_gradient, expected_probe)),
            "rollback_replaces_only_failed_candidate": retained == (1, 2, 3) and not rolled and replaced == (1, 7, 8) and failed,
            "cosine_schedule_endpoints": prefix_ratio(0) == 1. and prefix_ratio(50) == 1.
                and all(prefix_ratio(step) == .1 for step in (500, 501, 1000))}}
