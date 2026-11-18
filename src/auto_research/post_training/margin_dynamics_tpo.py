"""Margin Dynamics fixed-v1 TPO-S Eq.3 and normalized TPO-H Eq.25."""

import torch
from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def tpo_s(chosen_scores, rejected_scores, *, beta=0.1, margin=0.5, smoothing=0.05):
    tensor(chosen_scores, "chosen")
    tensor(rejected_scores, "rejected", shape=chosen_scores.shape, device=chosen_scores.device)
    b = scalar(beta, "beta", lower=0, strict_lower=True)
    mu = scalar(margin, "margin")
    e = scalar(smoothing, "smoothing", lower=0, upper=0.5)
    delta = b * (chosen_scores - rejected_scores - mu)
    return (
        (1 - e) * torch.nn.functional.softplus(-delta) + e * torch.nn.functional.softplus(delta)
    ).mean()


def tpo_h(margins, *, target, transition):
    tensor(margins, "margins")
    target = scalar(target, "target")
    d = scalar(transition, "transition", lower=0, strict_lower=True)
    error = (target - margins).abs()
    return torch.where(error <= d, error.square() / (2 * d), error - d / 2).mean()


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    b = 0.1
    mu = 0.5
    e = 0.05
    attractor = mu + torch.log(torch.tensor((1 - e) / e, dtype=torch.float64)).item() / b
    chosen = torch.tensor(
        [attractor - 2, attractor, attractor + 2],
        dtype=torch.float64,
        device=device,
        requires_grad=True,
    )
    out = tpo_s(chosen, torch.zeros_like(chosen))
    out.backward()
    h = torch.tensor([-100.0, 0.0, 100.0], device=device, dtype=torch.float64, requires_grad=True)
    huber = tpo_h(h, target=0, transition=2)
    huber.backward()
    jitter = float(torch.rand((), generator=g))
    return receipt(
        seed,
        "l1_mechanism",
        {
            "below_attractor_pushed_up": bool(chosen.grad[0] < 0),
            "attractor_zero_gradient": bool(chosen.grad[1].abs() < 1e-12),
            "overshoot_restoring_force": bool(chosen.grad[2] > 0),
            "huber_gradient_bounded": bool((h.grad.abs() <= 1 / 3 + 1e-12).all()),
            "huber_target_is_stationary": bool(h.grad[1] == 0),
        },
        {
            "tpo_s_loss": out.item(),
            "tpo_h_loss": huber.item(),
            "score_gap_attractor": attractor,
            "seeded_probe": jitter,
        },
    )
