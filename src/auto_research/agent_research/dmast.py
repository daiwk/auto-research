"""DMAST v2 Stage-3 pooled-role GRPO component, not a browser agent."""
from __future__ import annotations

import math

import torch
from torch import Tensor


def pooled_advantages(rewards: Tensor, task: Tensor, attacked: Tensor, seed: Tensor,
                      role: Tensor, length_penalty: Tensor, *, std_correction: int,
                      epsilon: float, penalty_coefficient: float = .1) -> tuple[Tensor, Tensor]:
    """Eq.2/Appendix B.2: raw statistics pool BOTH roles only when attacked.

    Groups are (task, attack-mode, environment-seed), never role. Clean groups
    contain only role=0 (agent). The paper does not specify std correction or
    the exact cosine implementation; callers supply both correction and L_t.
    Zero-RAW-variance groups are excluded BEFORE length shaping.
    """
    if rewards.ndim != 1 or not len(rewards) or not rewards.is_floating_point():
        raise ValueError("nonempty floating terminal reward vector required")
    for values in (task, seed, role):
        if values.shape != rewards.shape or values.dtype != torch.long or values.device != rewards.device:
            raise ValueError("aligned int64 group/role vectors required")
    if attacked.shape != rewards.shape or attacked.dtype != torch.bool or attacked.device != rewards.device:
        raise ValueError("aligned Boolean attack-mode vector required")
    if (length_penalty.ndim != 2 or length_penalty.shape[0] != len(rewards)
            or not length_penalty.is_floating_point() or length_penalty.device != rewards.device
            or length_penalty.shape[1] < 1):
        raise ValueError("aligned [trajectory,step] length penalties required")
    if not bool(((role == 0) | (role == 1)).all()) or bool(((role == 1) & ~attacked).any()):
        raise ValueError("roles are agent=0/attacker=1; clean trajectories must be agents")
    if (not bool(torch.isfinite(rewards).all()) or not bool(torch.isfinite(length_penalty).all())
            or bool(((length_penalty < 0) | (length_penalty > 1)).any())
            or type(std_correction) is not int or std_correction not in (0, 1)
            or not math.isfinite(epsilon) or epsilon <= 0
            or not math.isfinite(penalty_coefficient) or penalty_coefficient < 0):
        raise ValueError("finite rewards, L in [0,1], explicit std correction and positive epsilon required")
    work = rewards.detach().double() if rewards.dtype == torch.float64 else rewards.detach().float()
    penalty = length_penalty.detach().to(work.dtype)
    advantages = torch.zeros_like(penalty)
    eligible = torch.zeros_like(attacked)
    keys = torch.stack((task, attacked.long(), seed), 1)
    for group in torch.unique(keys, dim=0):
        members = (keys == group).all(1)
        values = work[members]
        if len(values) <= std_correction:
            continue
        deviation = values.std(correction=std_correction)
        if bool(deviation == 0):
            continue
        shaped = values[:, None] - penalty_coefficient * (values > 0)[:, None] * penalty[members]
        advantages[members] = (shaped - values.mean()) / (deviation + epsilon)
        eligible[members] = True
    if not bool(torch.isfinite(advantages).all()):
        raise ValueError("advantages are not representable")
    return advantages.detach(), eligible.detach()


def grpo_loss(logits: Tensor, actions: Tensor, old_logp: Tensor, sampled_logp: Tensor,
              reference_logp: Tensor, advantages: Tensor, eligible: Tensor,
              token_mask: Tensor, *, clip_low: float = .1, clip_high: float = .3,
              beta: float = .05) -> tuple[Tensor, dict]:
    """Appendix B.2 clipped PG + kappa KL, global valid-token denominator.

    logits=[trajectory,step,token,vocab]. IS correction is min(exp(old-sampled),1)
    and zero below .1; only PG is weighted. Old, reference, sampling logprobs,
    advantage, eligibility and masks are frozen. No attacker HTML is generated.
    """
    if logits.ndim != 4 or min(logits.shape) < 1 or not logits.is_floating_point():
        raise ValueError("floating [trajectory,step,token,vocabulary] logits required")
    shape = logits.shape[:-1]
    if (actions.shape != shape or actions.dtype != torch.long or token_mask.shape != shape
            or token_mask.dtype != torch.bool or advantages.shape != shape[:2]
            or not advantages.is_floating_point() or eligible.shape != shape[:1]
            or eligible.dtype != torch.bool):
        raise ValueError("aligned actions, masks, step advantages and trajectory eligibility required")
    if any(t.device != logits.device for t in (actions, old_logp, sampled_logp, reference_logp,
                                               advantages, eligible, token_mask)):
        raise ValueError("all tensors must share a device")
    if any(t.shape != shape or not t.is_floating_point() for t in (old_logp, sampled_logp, reference_logp)):
        raise ValueError("aligned floating log-probability arrays required")
    if not (math.isfinite(clip_low) and 0 < clip_low < 1 and math.isfinite(clip_high) and clip_high > 0
            and math.isfinite(beta) and beta >= 0):
        raise ValueError("valid clipping and nonnegative finite beta required")
    mask = token_mask.detach() & eligible.detach()[:, None, None]
    if (not bool(torch.isfinite(logits[mask]).all()) or
            not bool(((actions[mask] >= 0) & (actions[mask] < logits.shape[-1])).all())
            or not bool(torch.isfinite(advantages[eligible]).all())):
        raise ValueError("finite active logits/advantages and in-range active actions required")
    dtype = torch.float32 if logits.dtype in (torch.float16, torch.bfloat16) else logits.dtype
    clean = torch.where(mask[..., None], logits.to(dtype), 0.)
    current = clean.log_softmax(-1).gather(-1, torch.where(mask, actions, 0)[..., None]).squeeze(-1)
    frozen = []
    for value in (old_logp, sampled_logp, reference_logp):
        if not bool(torch.isfinite(value[mask]).all()) or bool((value[mask] > 0).any()):
            raise ValueError("finite nonpositive active frozen log probabilities required")
        frozen.append(torch.where(mask, value.detach().to(dtype), 0.))
    old, sampled, reference = frozen
    adv = torch.where(eligible[:, None], advantages.detach().to(dtype), 0.)[..., None]
    ratio_log = torch.where(mask, current - old, 0.)
    clipped_log = torch.where(adv >= 0, ratio_log.clamp_max(math.log1p(clip_high)),
                             ratio_log.clamp_min(math.log1p(-clip_low)))
    correction_log = old - sampled
    correction = torch.where(correction_log >= math.log(.1), correction_log.clamp_max(0).exp(), 0.)
    # A truncated IS weight (or zero advantage) defines an exactly zero PG
    # term. Mask BEFORE exponentiation: 0*exp(large) otherwise becomes NaN,
    # including in backward. Do not clamp a genuinely active unbounded branch.
    pg_active = mask & (correction > 0) & (adv != 0)
    pg_log = torch.where(pg_active, clipped_log, 0.)
    pg = torch.where(pg_active, correction * pg_log.exp() * adv, 0.)
    if beta > 0:
        delta = torch.where(mask, reference - current, 0.)
        kl = torch.expm1(delta) - delta
    else:
        # beta=0 removes KL mathematically; don't evaluate an overflowing
        # unused exp and then multiply its infinity by zero.
        kl = torch.zeros_like(current)
    count = int(mask.sum())
    loss = torch.where(mask, -pg + beta * kl, 0.).sum() / max(count, 1)
    if not bool(torch.isfinite(loss)):
        raise ValueError("objective is not representable")
    return loss, {"valid_tokens": count, "is_zeroed_tokens": int((mask & (correction == 0)).sum()),
                  "pg": torch.where(mask, pg, 0.).sum().detach() / max(count, 1),
                  "kl": torch.where(mask, kl, 0.).sum().detach() / max(count, 1)}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    generator = torch.Generator(device=dev).manual_seed(seed)
    features = torch.randn(8, 2, 3, 4, generator=generator, device=dev, dtype=torch.float64)
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        policy = torch.nn.Linear(4, 5).to(device=dev, dtype=torch.float64)
    logits = policy(features)
    actions = torch.multinomial(logits.detach().softmax(-1).reshape(-1, 5), 1, generator=generator).reshape(8, 2, 3)
    old = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).requires_grad_()
    reference = (old.detach() - .1).requires_grad_()
    sampled = (old.detach() + .3).clamp_max(-.001).requires_grad_()
    raw = torch.tensor([1., 0., 0., 1., 1., 0., 1., 1.], dtype=torch.float64, device=dev, requires_grad=True)
    task = torch.tensor([0, 0, 0, 0, 0, 0, 1, 1], device=dev)
    attacked = torch.tensor([True]*4 + [False]*4, device=dev)
    role = torch.tensor([0, 1, 0, 1, 0, 0, 0, 0], device=dev)
    env_seed = torch.zeros(8, dtype=torch.long, device=dev)
    penalty = torch.linspace(0., 1., 16, device=dev, dtype=torch.float64).reshape(8, 2)
    adv, eligible = pooled_advantages(raw, task, attacked, env_seed, role, penalty,
                                     std_correction=0, epsilon=1e-6)
    mask = torch.ones(8, 2, 3, dtype=torch.bool, device=dev)
    mask[1, 1, 2] = False
    loss, audit = grpo_loss(logits, actions, old, sampled, reference, adv, eligible, mask)
    lp = logits.log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    valid = mask & eligible[:, None, None]
    ratio = (lp - old.detach()).exp()
    correction = (old.detach() - sampled.detach()).exp().clamp_max(1.)
    correction = torch.where(correction >= .1, correction, 0.)
    pg = torch.minimum(ratio * adv[..., None], ratio.clamp(.9, 1.3) * adv[..., None])
    oracle = (-correction * pg + .05 * ((reference.detach() - lp).exp() - (reference.detach() - lp) - 1))[valid].mean()
    oracle_grad = torch.autograd.grad(oracle, logits, retain_graph=True)[0]
    actual_grad = torch.autograd.grad(loss, logits, retain_graph=True)[0]
    error = float((actual_grad - oracle_grad).abs().max())
    before = torch.cat([p.detach().clone().flatten() for p in policy.parameters()])
    loss.backward()
    optimizer = torch.optim.SGD(policy.parameters(), lr=.01)
    optimizer.step()
    delta = float((torch.cat([p.detach().flatten() for p in policy.parameters()]) - before).norm())
    # Execute the two formerly-overflowing but mathematically removed branches
    # on the requested device too: huge negative-advantage ratio at token0,
    # huge disabled-KL exponent at token1. IS is truncated to zero for both.
    extreme = torch.tensor([[[[0., 0.], [-1000., 0.]]]], device=dev,
                           dtype=torch.float64, requires_grad=True)
    extreme_old = torch.full((1, 1, 2), -1000., device=dev, dtype=torch.float64)
    extreme_loss, _ = grpo_loss(extreme, torch.zeros(1, 1, 2, device=dev, dtype=torch.long),
        extreme_old, torch.full_like(extreme_old, -1.), torch.full_like(extreme_old, -.7),
        torch.tensor([[-1.]], device=dev, dtype=torch.float64), torch.tensor([True], device=dev),
        torch.ones(1, 1, 2, device=dev, dtype=torch.bool), beta=0.)
    extreme_loss.backward()
    extreme_ok = extreme_loss.item() == 0 and bool(extreme.grad.isfinite().all()) and not bool(extreme.grad.any())
    return {"seed": seed, "metrics": {"loss": float(loss.detach()), "gradient_reference_error": error,
        "formula_reference_error": float((loss - oracle).detach().abs()), "parameter_delta": delta,
        "valid_tokens": audit["valid_tokens"], "eligible_trajectories": int(eligible.sum()), "optimizer_steps": 1},
        "checks": {"raw_pooled_role_statistics": bool(torch.allclose(adv[:4], (raw[:4, None].detach() - .1 * (raw[:4, None].detach() > 0) * penalty[:4] - .5) / (.5 + 1e-6))),
            "zero_raw_variance_excluded": not bool(eligible[6:].any()),
            "clean_attack_modes_separated": bool(eligible[:6].all()),
            "gradient_matches_reference": error < 1e-10,
            "padding_and_excluded_zero_gradient": bool((actual_grad[~valid] == 0).all()),
            "frozen_rollout_reference_rewards": old.grad is None and sampled.grad is None and reference.grad is None and raw.grad is None,
            "real_shared_policy_update": delta > 0,
            "zero_importance_branch_finite_zero_gradient": extreme_ok}}
