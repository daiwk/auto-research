"""RLBP's bounded PID actions, two-objective TD loss and policy kernels.

Only paper Eqs.3–11 are implemented. No campaign encoder, learned production
Q-network, auction simulator, live bidder or advertising-budget access.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def _finite(x, name):
    if not isinstance(x, Tensor) or x.dtype not in (torch.float32, torch.float64) or not x.numel() or not torch.isfinite(x).all():
        raise ValueError(f"{name} must be nonempty finite float32/float64")


def _aligned(*xs):
    if any(x.shape != xs[0].shape or x.device != xs[0].device or x.dtype != xs[0].dtype for x in xs[1:]):
        raise ValueError("aligned tensors required")


def action_multipliers(alpha=0.2, *, device="cpu", dtype=torch.float64):
    if isinstance(alpha, bool) or not isinstance(alpha, (int, float)) or not math.isfinite(alpha) or not 0 < alpha < 1:
        raise ValueError("0 < alpha < 1 required")
    if dtype not in (torch.float32, torch.float64):
        raise ValueError("float32/float64 required")
    values = (1 - alpha, 1., 1 + alpha)
    table = torch.tensor([(p, i, 1.) for p in values for i in values], dtype=dtype, device=device)
    if len(torch.unique(table, dim=0)) != 9:
        raise ValueError("alpha collapses distinct actions at this dtype")
    return table


def adjusted_gains(default: Tensor, multipliers: Tensor) -> Tensor:
    for x in (default, multipliers):
        _finite(x, "PID gains")
    if default.shape != (3,) or multipliers.ndim != 2 or multipliers.shape[1] != 3 or default.dtype != multipliers.dtype or default.device != multipliers.device or (default <= 0).any() or (multipliers <= 0).any() or not torch.all(multipliers[:, 2] == 1):
        raise ValueError("positive P/I/D with fixed derivative multiplier 1 required")
    result = default * multipliers
    if not torch.isfinite(result).all():
        raise ValueError("gain overflow")
    return result


def relative_lift(metric: Tensor, production: Tensor) -> Tensor:
    """Eq.9; no undocumented epsilon/floor for zero production denominators."""
    _finite(metric, "metric")
    _finite(production, "production")
    _aligned(metric, production)
    if (metric < 0).any() or (production <= 0).any():
        raise ValueError("nonnegative metrics and strictly positive baseline required")
    result = (metric - production) / production
    if not torch.isfinite(result).all():
        raise ValueError("relative reward overflow")
    return result


def two_head_td_loss(q_bu: Tensor, q_cpc: Tensor, actions: Tensor, r_bu: Tensor, r_cpc: Tensor,
                     *, gamma=0., next_bu: Tensor | None = None, next_cpc: Tensor | None = None):
    """Eqs.4–6: maximize BU, minimize CPC in separate detached backups.

    Default gamma=0 is the actual deployed contextual-bandit configuration.
    gamma>0 is a formula extension, not an optimal fused-return guarantee.
    """
    if isinstance(gamma, bool) or not isinstance(gamma, (int, float)) or not math.isfinite(gamma) or not 0 <= gamma < 1:
        raise ValueError("gamma in [0,1) required")
    for x in (q_bu, q_cpc, r_bu, r_cpc):
        _finite(x, "Q/reward")
    _aligned(q_bu, q_cpc)
    _aligned(r_bu, r_cpc)
    if q_bu.ndim != 2 or q_bu.shape[1] != 9 or r_bu.shape != (len(q_bu),) or r_bu.dtype != q_bu.dtype or r_bu.device != q_bu.device or not isinstance(actions, Tensor) or actions.dtype != torch.long or actions.shape != r_bu.shape or actions.device != q_bu.device or (actions < 0).any() or (actions >= 9).any():
        raise ValueError("batch-by-nine Qs, reward vectors and valid long action IDs required")
    bu_target, cpc_target = r_bu.detach(), r_cpc.detach()
    if gamma:
        for x in (next_bu, next_cpc):
            _finite(x, "next Q")
        _aligned(q_bu, next_bu, next_cpc)
        bu_target = bu_target + gamma * next_bu.detach().max(-1).values
        cpc_target = cpc_target + gamma * next_cpc.detach().min(-1).values
    elif next_bu is not None or next_cpc is not None:
        raise ValueError("gamma=0 must not consume future Qs")
    bu = (q_bu.gather(1, actions[:, None]).squeeze(1) - bu_target).square().mean()
    cpc = (q_cpc.gather(1, actions[:, None]).squeeze(1) - cpc_target).square().mean()
    if not torch.isfinite(bu + cpc):
        raise ValueError("TD loss overflow")
    return {"bu": bu, "cpc": cpc, "total": bu + cpc}


def fused_policy(q_bu: Tensor, q_cpc: Tensor, beta: Tensor, *, top_k=3, temperature=1., preprocess=None):
    """Eqs.7–8, stable tie-break and exactly zero mass outside top-K.

    The paper does not disclose numerical beta scale or score preprocessing.
    beta and the optional post-fusion preprocess callback are external. None
    is an identity numerical reference, not a claim about production settings.
    """
    for x in (q_bu, q_cpc, beta):
        _finite(x, "policy inputs")
    _aligned(q_bu, q_cpc)
    if q_bu.ndim != 2 or q_bu.shape[1] != 9 or beta.shape != (len(q_bu),) or beta.device != q_bu.device or beta.dtype != q_bu.dtype or (beta < 0).any():
        raise ValueError("batch-by-nine Qs and nonnegative per-state beta required")
    if isinstance(top_k, bool) or not isinstance(top_k, int) or not 1 <= top_k <= 9 or isinstance(temperature, bool) or not isinstance(temperature, (int, float)) or not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("valid top-K and positive finite temperature required")
    score = q_bu - beta[:, None] * q_cpc
    if not torch.isfinite(score).all():
        raise ValueError("fusion overflow")
    if preprocess is not None:
        if not callable(preprocess):
            raise ValueError("preprocess must be an explicit external callback")
        processed = preprocess(score.clone())
        _finite(processed, "preprocessed scores")
        _aligned(score, processed)
        score = processed
    indices = score.argsort(dim=-1, descending=True, stable=True)[:, :top_k]
    kept = score.gather(1, indices)
    temperature_tensor = torch.as_tensor(temperature, dtype=score.dtype, device=score.device)
    if not torch.isfinite(temperature_tensor) or temperature_tensor <= 0:
        raise ValueError("temperature must remain positive/finite at the input dtype")
    weights = ((kept - kept.max(-1, keepdim=True).values) / temperature_tensor).softmax(-1)
    if not torch.isfinite(weights).all():
        raise ValueError("policy normalization failed")
    return torch.zeros_like(score).scatter(1, indices, weights)


def ips_value(chosen_probability: Tensor, logging_probability: Tensor, rewards: Tensor) -> Tensor:
    for x in (chosen_probability, logging_probability, rewards):
        _finite(x, "IPS inputs")
    _aligned(chosen_probability, logging_probability, rewards)
    if chosen_probability.ndim != 1 or (chosen_probability < 0).any() or (chosen_probability > 1).any() or (logging_probability <= 0).any() or (logging_probability > 1).any():
        raise ValueError("valid support and propensity vectors required")
    result = (chosen_probability / logging_probability * rewards).mean()
    if not torch.isfinite(result):
        raise ValueError("IPS overflow")
    return result


def diagnostic(seed=42, device="cpu"):
    generator = torch.Generator(device=device).manual_seed(seed)
    dtype = torch.float64
    actions = torch.tensor([0, 2, 4, 8], device=device)
    q_bu = (torch.randn(4, 9, generator=generator, dtype=dtype, device=device) * 0.1).requires_grad_()
    q_cpc = (torch.randn(4, 9, generator=generator, dtype=dtype, device=device) * 0.1).requires_grad_()
    production = torch.tensor([1., 2., 4., 5.], dtype=dtype, device=device)
    rb = relative_lift(production * 1.1, production)
    rc = relative_lift(production * 0.9, production)
    optimizer = torch.optim.SGD([q_bu, q_cpc], lr=0.1)
    before = two_head_td_loss(q_bu, q_cpc, actions, rb, rc)["total"]
    optimizer.zero_grad()
    before.backward()
    grad = float(q_bu.grad.norm() + q_cpc.grad.norm())
    optimizer.step()
    after = two_head_td_loss(q_bu, q_cpc, actions, rb, rc)["total"]
    future = torch.arange(36, dtype=dtype, device=device).reshape(4, 9).requires_grad_()
    extended = two_head_td_loss(torch.zeros_like(q_bu), torch.zeros_like(q_cpc), actions,
                                torch.zeros_like(rb), torch.zeros_like(rc), gamma=0.5, next_bu=future, next_cpc=future)
    reference = (0.5 * future.detach().max(-1).values).square().mean() + (0.5 * future.detach().min(-1).values).square().mean()
    wrong = 2 * (0.5 * future.detach().max(-1).values).square().mean()
    qb = torch.arange(9, dtype=dtype, device=device)[None, :].repeat(2, 1)
    qc = qb * 2
    policy = fused_policy(qb, qc, torch.tensor([0., 1.], dtype=dtype, device=device), top_k=3, temperature=0.7)
    table = action_multipliers(device=device)
    gains = adjusted_gains(torch.tensor([2., 3., 4.], dtype=dtype, device=device), table)
    pi = torch.tensor([0.8, 0.2], dtype=dtype, device=device)
    prop = torch.tensor([0.5, 0.5], dtype=dtype, device=device)
    reward = torch.tensor([2., 1.], dtype=dtype, device=device)
    ips = ips_value(pi, prop, reward)
    metrics = {"td_loss_before": float(before.detach()), "td_loss_after": float(after.detach()),
               "actor_gradient_norm": grad, "max_min_backup_error": float((extended["total"] - reference).abs()),
               "wrong_cpc_max_backup_gap": float((wrong - reference).abs()), "policy_row_mass_error": float((policy.sum(-1) - 1).abs().max()),
               "derivative_gain_error": float((gains[:, 2] - 4).abs().max()), "ips_reference_error": abs(float(ips) - 1.8), "pretrained_model_calls": 0}
    checks = {"actual_reward_regression_update": metrics["td_loss_after"] < metrics["td_loss_before"] and grad > 0,
              "CPC_reduction_retains_negative_sign": bool((rc < 0).all()),
              "opposite_backup_directions": metrics["max_min_backup_error"] < 1e-10 and metrics["wrong_cpc_max_backup_gap"] > 1,
              "fusion_changes_preference": int(policy[0].argmax()) == 8 and int(policy[1].argmax()) == 0,
              "exact_top_k_support": bool(((policy > 0).sum(-1) == 3).all()),
              "nine_bounded_PID_actions": len(table) == 9 and metrics["derivative_gain_error"] == 0,
              "ordinary_IPS_not_self_normalized": metrics["ips_reference_error"] < 1e-10,
              "no_live_bidder_or_model_calls": True}
    return {"seed": seed, "metrics": metrics, "checks": checks}
