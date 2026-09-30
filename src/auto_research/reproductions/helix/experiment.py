"""Deterministic HELIX architecture diagnostic with cache-reuse checks."""

from __future__ import annotations


def reproduce(_dataset_dir, seed: int = 42) -> dict:
    import torch

    from .model import HELIXCore

    torch.manual_seed(seed)
    model = HELIXCore(16, mix_tokens=4, heads=4)
    user = torch.randn(2, 9, 16, requires_grad=True)
    candidate_a = torch.randn(2, 5, 16)
    candidate_b = torch.randn(2, 5, 16)
    mix = torch.randn(2, 4, 16)
    cache = model.encode_user(user)
    cache_snapshot = cache.detach().clone()
    score_a, hidden_a = model(mix, candidate_a, user_cache=cache)
    score_b, hidden_b = model(mix, candidate_b, user_cache=cache)
    loss = score_a.square().mean() + score_b.square().mean()
    loss.backward()
    return {
        "paper": "2609.37183",
        "seed": seed,
        "evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True},
        "metrics": {
            "finite_loss": bool(torch.isfinite(loss)),
            "candidate_conditioned_delta": float((hidden_a - hidden_b).abs().mean().detach()),
            "user_cache_unchanged": bool(torch.equal(cache.detach(), cache_snapshot)),
            "user_gradient_finite": bool(torch.isfinite(user.grad).all()),
        },
        "scope": "HELIX one-way cache and MPTF diagnostic; not TikTok data, serving kernels or online A/B.",
    }
