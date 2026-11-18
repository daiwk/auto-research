"""SpeCal v1 Eq.3–12; external hidden representations, not model rollout."""

import torch
from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def calibrate(
    representations, advantages, *, target_rank, rank_tolerance, lower=0.5, upper=1.5, epsilon=1e-12
):
    tensor(representations, "representations", ndim=3)
    batch, group, dim = representations.shape
    if min(batch, dim) < 1 or group < 3:
        raise ValueError("at least three rollouts per group required")
    tensor(advantages, "advantages", shape=representations.shape[:2], device=representations.device)
    mu = scalar(target_rank, "target_rank", lower=0, upper=1)
    tau = scalar(rank_tolerance, "rank_tolerance", lower=0, strict_lower=True)
    lo = scalar(lower, "lower", lower=0)
    hi = scalar(upper, "upper", lower=lo)
    eps = scalar(epsilon, "epsilon", lower=0, strict_lower=True)
    with torch.no_grad():
        if bool((representations.norm(dim=-1) <= eps).any()):
            raise ValueError(
                "zero response representations are unavailable, not meaningful spectra"
            )
        z = representations.detach() / representations.detach().norm(dim=-1, keepdim=True)
        zc = z - z.mean(1, keepdim=True)
        eig = torch.linalg.eigvalsh(zc @ zc.transpose(-1, -2)).clamp_min(0)
        rank = min(group - 1, dim)
        eig = eig[:, -rank:]
        mass = eig.sum(-1) / group
        p = eig / eig.sum(-1, keepdim=True).clamp_min(eps)
        er = torch.exp(-(p * p.clamp_min(eps).log()).sum(-1))
        er = torch.where(mass > eps, er, torch.zeros_like(er))
        wg = mass * torch.exp(-0.5 * ((er / rank - mu) / tau).square())
        support = torch.zeros(batch, group, dtype=z.dtype, device=z.device)
        for b in range(batch):
            for j in range(group):
                other = torch.cat([z[b, :j], z[b, j + 1 :]])
                mean = other.mean(0)
                _, singular, vh = torch.linalg.svd(other - mean, full_matrices=False)
                available = int((singular > eps).sum())
                count = min(int(torch.ceil(er[b]).item()), available)
                x = z[b, j] - mean
                if count and bool(x.square().sum() > eps):
                    support[b, j] = (vh[:count] @ x).square().sum() / x.square().sum()
        wr = (support / support.mean(-1, keepdim=True).clamp_min(eps)).clamp(lo, hi)
        # A collapsed group has no supervised contrast, not a perfect weight.
        wr = torch.where(support.mean(-1, keepdim=True) > eps, wr, torch.zeros_like(wr))
        group_scale = wg / wg.square().mean().sqrt().clamp_min(eps)
        inside = wr * advantages.detach()
        normalized = inside / inside.square().mean(-1, keepdim=True).sqrt().clamp_min(eps)
        result = group_scale[:, None] * normalized
    return {
        "advantages": result,
        "group_weight": wg,
        "rollout_weight": wr,
        "support": support,
        "effective_rank": er,
    }


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    z = torch.randn(2, 4, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    a = torch.tensor(
        [[1.0, -1.0, 2.0, -2.0], [1.0, 2.0, -1.0, -2.0]], device=device, dtype=torch.float64
    ).requires_grad_()
    out = calibrate(z, a, target_rank=0.5, rank_tolerance=0.2)
    collapsed = calibrate(torch.ones_like(z), a, target_rank=0.5, rank_tolerance=0.2)
    altered = z.detach().clone()
    altered[:, 0] *= 7
    scale = calibrate(altered, a, target_rank=0.5, rank_tolerance=0.2)
    return receipt(
        seed,
        "l1_mechanism",
        {
            "all_calibration_stop_gradient": not out["advantages"].requires_grad,
            "conditional_support_in_unit_interval": bool(
                ((out["support"] >= -1e-10) & (out["support"] <= 1 + 1e-10)).all()
            ),
            "collapsed_group_yields_no_advantage": bool((collapsed["advantages"] == 0).all()),
            "response_l2_scale_invariant": bool(
                torch.allclose(out["advantages"], scale["advantages"], atol=1e-9)
            ),
            "rollout_weights_clipped": bool(
                ((out["rollout_weight"] >= 0.5) & (out["rollout_weight"] <= 1.5)).all()
            ),
        },
        {
            "mean_group_weight": out["group_weight"].mean().item(),
            "mean_support": out["support"].mean().item(),
            "advantage_rms": out["advantages"].square().mean().sqrt().item(),
        },
    )
