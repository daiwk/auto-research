"""RSC v1 Eq.7 gradient estimator, independent same-history auxiliary actions.

The returned surrogate has the prescribed gradient, not the population W value.
Behavior, ratios, response advantages and auxiliary sampling weights are frozen.
"""

import torch
from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def loss(
    logp,
    behavior_logp,
    advantages,
    aux_logp,
    aux_behavior_logp,
    *,
    beta=0.1,
    low=0.5,
    high=2.0,
    kl_cap=None,
    aux_weights=None,
):
    tensor(logp, "logp", ndim=1)
    for value, name in [(behavior_logp, "behavior"), (advantages, "advantages")]:
        tensor(value, name, shape=logp.shape, device=logp.device)
    tensor(aux_logp, "auxiliary", ndim=2, device=logp.device)
    tensor(aux_behavior_logp, "auxiliary behavior", shape=aux_logp.shape, device=logp.device)
    if aux_logp.shape[0] != logp.shape[0] or any(
        bool((x > 0).any()) for x in [logp, aux_logp, behavior_logp, aux_behavior_logp]
    ):
        raise ValueError("same-history nonpositive log-probabilities required")
    b = scalar(beta, "beta", lower=0)
    lo = scalar(low, "low", lower=0, upper=1)
    hi = scalar(high, "high", lower=1)
    if aux_weights is None:
        w = torch.full_like(aux_logp, 1 / aux_logp.shape[-1])
    else:
        tensor(aux_weights, "weights", shape=aux_logp.shape, device=logp.device)
        if bool((aux_weights < 0).any()) or not torch.allclose(
            aux_weights.sum(-1), torch.ones_like(logp)
        ):
            raise ValueError("nonnegative normalized auxiliary weights required")
        w = aux_weights.detach()
    rho = (logp.detach() - behavior_logp.detach()).exp()
    arho = (aux_logp.detach() - aux_behavior_logp.detach()).exp()
    if not bool(torch.isfinite(rho).all() and torch.isfinite(arho).all()):
        raise ValueError("importance ratio overflow")
    rkl = arho if kl_cap is None else arho.clamp_max(scalar(kl_cap, "kl_cap", lower=1))
    a = advantages.detach()
    reward = a * (rho.clamp(lo, hi) * logp - (w * arho.clamp(lo, hi) * aux_logp).sum(-1))
    penalty = b * (w * torch.special.xlogy(rkl, rkl).detach() * aux_logp).sum(-1)
    return (-reward + penalty).mean()


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    logits = torch.randn(1, 4, generator=g, dtype=torch.float64).to(device).requires_grad_()
    behavior = torch.randn(1, 4, generator=g, dtype=torch.float64).to(device).log_softmax(-1)
    lp = logits.log_softmax(-1)
    a = torch.tensor([2.0], device=device, dtype=torch.float64, requires_grad=True)
    # Exact enumeration is an independent full-action expectation negative control.
    out = loss(
        lp[:, 0],
        behavior[:, 0],
        a,
        lp,
        behavior,
        beta=0.2,
        low=1,
        high=1,
        aux_weights=behavior.exp(),
    )
    grad = torch.autograd.grad(out, logits, retain_graph=True)[0]
    expected = -a.detach() * (lp[:, 0] - (behavior.exp() * lp).sum(-1)) + 0.2 * (
        lp.exp() * (lp - behavior)
    ).sum(-1)
    exact = torch.autograd.grad(expected.mean(), logits, retain_graph=True)[0]
    no_center = -a.detach() * lp[:, 0]
    wrong = torch.autograd.grad(no_center.mean(), logits, retain_graph=True)[0]
    out.backward()
    return receipt(
        seed,
        "l1_mechanism",
        {
            "exact_action_enumeration_gradient": bool(torch.allclose(grad, exact, atol=1e-10)),
            "center_is_not_reward_mean": not bool(torch.allclose(grad, wrong)),
            "external_advantage_frozen": a.grad is None,
            "finite_gradient": bool(torch.isfinite(grad).all()),
        },
        {
            "surrogate": out.item(),
            "gradient_oracle_error": float((grad - exact).abs().max()),
            "uncentered_gradient_difference": float((grad - wrong).norm()),
        },
    )
