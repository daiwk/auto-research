"""SCAR Eqs.4--6 exact bounded-coalition credit, not RM/LLM training.

The external frozen RM must score original-order, space-masked text coalitions.
No heuristic RM or syntax parser is substituted. Exact N<=10 enumeration is a
faithful small-game path, NOT the paper's hierarchical Owen/SHAP approximation.
"""
from __future__ import annotations
import math
import torch
from torch import Tensor


def exact_shapley(values: Tensor) -> Tensor:
    """Coalition values indexed by bit mask, v(empty)=0; signed credits retained."""
    if values.ndim != 1 or not values.is_floating_point() or not bool(torch.isfinite(values).all()):
        raise ValueError("finite floating coalition-value vector required")
    count = values.numel()
    if count < 2 or count & (count - 1) or count > 1024:
        raise ValueError("cost gate: complete 2**N table, 1<=N<=10 required")
    if float(values[0].detach()) != 0:
        raise ValueError("SCAR requires v(empty)=0")
    n = count.bit_length() - 1
    frozen = values.detach().to(torch.float64)
    result = frozen.new_zeros(n)
    for i in range(n):
        for coalition in range(count):
            if coalition & (1 << i):
                continue
            size = coalition.bit_count()
            weight = 1 / (n * math.comb(n - 1, size))
            result[i] += weight * (frozen[coalition | (1 << i)] - frozen[coalition])
    if not bool(torch.isfinite(result).all()):
        raise ValueError("Shapley values must be representable")
    return result


def scatter_dense_rewards(credits: Tensor, endpoints: Tensor, kl_rewards: Tensor,
                           *, terminal_reward: float, alpha: float = 1.,
                           discount: float = 1.) -> Tensor:
    """Eq.5--6: span credit only at span END, plus unchanged token KL penalties.

    Restrict gamma=1: equality of undiscounted sums does not imply equality of
    discounted returns at gamma<1. No 'optimality preservation' claim there.
    """
    if credits.ndim != 1 or not credits.numel() or not credits.is_floating_point() or not bool(torch.isfinite(credits).all()):
        raise ValueError("finite nonempty span credits required")
    if endpoints.shape != credits.shape or endpoints.dtype != torch.long or endpoints.device != credits.device:
        raise ValueError("aligned int64 span-end indices required")
    if kl_rewards.ndim != 1 or not kl_rewards.is_floating_point() or not bool(torch.isfinite(kl_rewards).all()) or kl_rewards.device != credits.device:
        raise ValueError("finite same-device token KL rewards required")
    if not kl_rewards.numel() or bool((endpoints < 0).any()) or bool((endpoints[1:] <= endpoints[:-1]).any()) or int(endpoints[-1]) != kl_rewards.numel() - 1:
        raise ValueError("strictly increasing span ends must finish at the final token")
    if not math.isfinite(alpha) or not 0 <= alpha <= 1 or not math.isfinite(terminal_reward) or discount != 1.:
        raise ValueError("finite alpha in [0,1], terminal reward and discount=1 required")
    if not torch.isclose(credits.sum(), credits.new_tensor(terminal_reward), rtol=1e-7, atol=1e-9):
        raise ValueError("Shapley efficiency must match the full-sequence terminal reward")
    result = kl_rewards.detach().to(credits.dtype).clone()
    result.scatter_add_(0, endpoints, alpha * credits.detach())
    result[-1] += (1 - alpha) * terminal_reward
    if not bool(torch.isfinite(result).all()):
        raise ValueError("shaped rewards must be representable")
    return result


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    generator = torch.Generator(device=device).manual_seed(seed)
    # Independent synthetic cooperative game with a negative player and a synergy.
    weights = torch.tensor([.8, -.2, .4, 0.], dtype=torch.float64, device=device)
    values = torch.stack([sum((weights[i] for i in range(4) if bits & (1 << i)), weights.new_zeros(()))
        + (.6 if bits & 3 == 3 else 0.) for bits in range(16)]).requires_grad_()
    credits = exact_shapley(values)
    reference = weights + weights.new_tensor([.3, .3, 0., 0.])
    kl = -torch.rand(9, dtype=torch.float64, device=device, generator=generator) * .03
    ends = torch.tensor([1, 3, 6, 8], device=device)
    dense = scatter_dense_rewards(credits, ends, kl, terminal_reward=float(values[-1].detach()), alpha=.7)
    sparse = scatter_dense_rewards(credits, ends, kl, terminal_reward=float(values[-1].detach()), alpha=0.)
    error = float((credits - reference).abs().max())
    total_error = float((dense.sum() - (kl.sum() + values[-1].detach())).abs())
    return {"seed": seed, "diagnostic_only": True, "metrics": {
        "formula_max_abs_error": error, "return_preservation_error": total_error,
        "coalitions": 16, "players": 4, "model_calls": 0}, "checks": {
        "exact_shapley_matches_independent_game": error < 1e-12,
        "dummy_player_zero": float(credits[3]) == 0.,
        "signed_contributions_not_clamped": float(exact_shapley(torch.tensor([0., -1.], device=device))[0]) < 0,
        "efficiency_preserves_undiscounted_return": total_error < 1e-12,
        "span_end_only_not_uniform_spread": bool(torch.equal(dense[[0,2,4,5,7]], kl[[0,2,4,5,7]])),
        "alpha_zero_is_sparse_reward": bool(torch.allclose(sparse[:-1], kl[:-1])) and abs(float(sparse[-1] - kl[-1]) - float(values[-1].detach())) < 1e-12,
        "frozen_reward_model_table": not credits.requires_grad and values.grad is None}}
