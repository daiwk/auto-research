"""Deterministic CPU mechanism validation for GRP v0.1."""

from __future__ import annotations


def reproduce(_dataset_dir, seed: int = 42) -> dict:
    import torch

    from .model import GRPHeads, block_causal_mask, m_grpo_loss

    torch.manual_seed(seed)
    model = GRPHeads(12, 17, heads=2)
    history = torch.randn(2, 6, 12, requires_grad=True)
    targets = torch.randn(2, 6, 12)
    candidates = torch.randn(2, 3, 12)
    generation, ranking = model(history, targets, candidates, items=2, codes_per_item=3)
    generation.square().mean().backward()
    mask = block_causal_mask(2, 3)
    policy = torch.tensor([-0.7, -1.0, -0.5], requires_grad=True)
    loss, audit = m_grpo_loss(
        policy, torch.tensor([-0.8, -0.9, -0.6]), torch.tensor([-0.8, -0.9, -0.6]),
        torch.tensor([0.1, 0.8, 0.2]), torch.tensor(-0.75), margin=0.05,
    )
    loss.backward()
    cross_block_open = bool((~mask[:3, 3:]).any())
    return {
        "paper": "2609.36688", "seed": seed,
        "evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True},
        "metrics": {
            "independent_blocks": not cross_block_open,
            "ranker_candidate_variance": float(ranking.var().detach()),
            "generation_gradient_finite": bool(torch.isfinite(history.grad).all()),
            "policy_gradient_finite": bool(torch.isfinite(policy.grad).all()),
            "recall_guard": audit["recall_guard"],
        },
        "scope": "GRP public architecture/mGRPO diagnostic; not Snap data, Qwen3-VL SID training, serving stack, or online A/B.",
    }
