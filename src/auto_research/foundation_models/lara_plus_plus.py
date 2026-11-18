"""Pinned author LARA++ deterministic mis-opt reference; paper/code differences documented."""

from __future__ import annotations

import math
import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/lara-plus-plus-a100-20261118-latest.json"
UPSTREAM_REVISION = "20a9f67a252059ce04383e1365700416de9d9447"


@torch.no_grad()
def cluster_means(q: Tensor, k: Tensor, clusters: int) -> tuple[Tensor, Tensor]:
    """Author variant: normalized joint Q+K, deterministic first center; CLS outside."""
    if q.ndim != 2 or k.shape != q.shape or not 1 <= clusters <= q.shape[0]:
        raise ValueError("matching [tokens,width] and bounded cluster count required")
    z = F.normalize(F.normalize(q, dim=-1) + F.normalize(k, dim=-1), dim=-1)
    index = z.norm(dim=-1).argmax()
    centers = [index]
    distance = 1 - z @ z[index]
    for _ in range(1, clusters):
        index = distance.argmax()
        centers.append(index)
        distance = torch.minimum(distance, 1 - z @ z[index])
    center_rows = z[torch.stack(centers)]
    assigned = (z @ center_rows.T).argmax(-1)
    membership = F.one_hot(assigned, clusters).to(q.dtype)
    count = membership.sum(0).clamp_min(1e-8)[:, None]
    return membership.T @ q / count, membership.T @ k / count


def attention(q: Tensor, k: Tensor, v: Tensor, landmarks: int) -> Tensor:
    """Noncausal self-attention kernel, matching pinned author's no-filter mis-opt path."""
    if (
        q.ndim != 2
        or k.shape != q.shape
        or v.shape[0] != q.shape[0]
        or not 1 <= landmarks <= q.shape[0]
        or not all(bool(torch.isfinite(t).all()) for t in (q, k, v))
    ):
        raise ValueError("finite self-attention Q/K/V and valid landmark budget required")
    if q.shape[0] <= landmarks:
        qbar, kbar = q, k
    else:
        qmean, kmean = cluster_means(q[1:], k[1:], landmarks)
        qbar, kbar = torch.cat([q[:1], qmean]), torch.cat([k[:1], kmean])
    mu = qbar + kbar  # Deterministic means, no Gaussian sampling.
    scale = 1 / math.sqrt(q.shape[-1])

    def feature(data: Tensor) -> Tensor:
        return scale * (mu @ data.T - 0.5 * data.square().sum(-1)[None])

    logq, logk, logmu = feature(q), feature(k), feature(mu)
    stats = logk.softmax(-1) @ v
    assignment = (scale * qbar @ q.T).softmax(-1)
    diagonal = logmu.diagonal()[:, None]
    balanced = (diagonal - logmu.logsumexp(-1, keepdim=True)).exp()
    alpha = (balanced + assignment - assignment.mean(0, keepdim=True)).clamp_min(1e-8)
    importance = (alpha.log() + logq + logk.logsumexp(-1, keepdim=True) - diagonal).softmax(0)
    return importance.T @ stats


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    q = torch.randn(17, 8, device=device, requires_grad=True)
    k, v = torch.randn_like(q), torch.randn(17, 5, device=device)
    result = attention(q, k, v, 4)
    repeated = attention(q, k, v, 4)
    constant = attention(q, k, torch.ones_like(v) * 2, 4)
    collapsed = attention(torch.ones_like(q), torch.ones_like(k), v, 4)
    result.square().mean().backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"output_norm": float(result.norm().detach())},
        "checks": {
            "deterministic_means": bool(torch.equal(result, repeated)),
            "constant_value_preserved": bool(
                torch.allclose(constant, torch.full_like(constant, 2), atol=1e-5)
            ),
            "empty_cluster_degeneracy_finite": bool(torch.isfinite(collapsed).all()),
            "query_receives_gradient": bool(q.grad is not None and q.grad.abs().sum() > 0),
        },
    }
