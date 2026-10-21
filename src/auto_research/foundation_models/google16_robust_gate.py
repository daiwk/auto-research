"""Finite-support robust generative gate: paper §5.2, §6 and §7.3.

Exact finite sums expose the global partition constraint instead of pretending
that an input-wise softmax over experts normalizes the resulting sequence law.
No language-model robustness/capability claim follows from these diagnostics.
"""
from __future__ import annotations

import torch
from torch import Tensor


def _distributions(value: Tensor, name: str) -> None:
    if value.ndim != 2 or not value.numel() or not torch.isfinite(value).all() or (value <= 0).any():
        raise ValueError(f"{name} must be positive finite [domain, support]")
    if not torch.allclose(value.sum(-1), torch.ones_like(value.sum(-1)), atol=1e-6):
        raise ValueError(f"{name} rows must sum to one")


def gated_mass(experts: Tensor, gate_logits: Tensor) -> Tensor:
    """π_g(x)=Σ_k g(x,k)π_k(x); this is NOT automatically a probability law."""
    _distributions(experts, "experts")
    if gate_logits.shape != experts.T.shape or not torch.isfinite(gate_logits).all():
        raise ValueError("gate logits must be finite [support, expert]")
    return (gate_logits.softmax(-1) * experts.T.detach()).sum(-1)


def primal_dual_step(gate_logits: Tensor, experts: Tensor, domains: Tensor,
                     adversary: Tensor, dual: Tensor, optimizer: torch.optim.Optimizer,
                     *, adversary_lr: float = .05, dual_lr: float = .1) -> dict[str, Tensor]:
    """Algorithm 2 with exact support, EG adversary and scalar dual ascent.

    Domain KL (rather than entropy-shifted NLL) drives the adversary, as in
    Algorithm 1/Appendix D. Parameters update against the new adversary/dual.
    """
    _distributions(domains, "domains")
    if domains.shape != experts.shape or adversary.shape != (len(domains),) or dual.numel() != 1:
        raise ValueError("domain, adversary and dual dimensions must align")
    if (adversary <= 0).any() or not torch.isfinite(adversary).all() or not torch.isfinite(dual).all():
        raise ValueError("adversary must be positive and dual finite")
    if not torch.allclose(adversary.sum(), adversary.new_tensor(1.)) or min(adversary_lr, dual_lr) <= 0:
        raise ValueError("normalized adversary and positive learning rates required")
    mass = gated_mass(experts, gate_logits)
    domain_kl = (domains * (domains.log() - mass.log()[None])).sum(-1)
    updated = (adversary.log() + adversary_lr * domain_kl.detach()).softmax(-1)
    new_dual = dual.detach() + dual_lr * (mass.sum().detach() - 1)
    objective = (updated * domain_kl).sum() + new_dual * (mass.sum() - 1)
    optimizer.zero_grad()
    objective.backward()
    optimizer.step()
    return {"adversary": updated.detach(), "dual": new_dual.detach(),
            "domain_kl": domain_kl.detach(), "partition": mass.sum().detach(),
            "objective": objective.detach()}


def sir_resample(experts: Tensor, gate_logits: Tensor, candidates: int, samples: int,
                 generator: torch.Generator) -> Tensor:
    """Algorithm 3 finite-support SIR; invalid/zero mass is an error, not success."""
    if min(candidates, samples) <= 0:
        raise ValueError("positive sampling budgets required")
    mass = gated_mass(experts, gate_logits).detach()
    proposal = experts.mean(0)
    output = []
    for _ in range(samples):
        proposed = torch.multinomial(proposal, candidates, replacement=True, generator=generator)
        weights = mass[proposed] / proposal[proposed]
        choice = torch.multinomial(weights, 1, generator=generator)
        output.append(proposed[choice].reshape(()))
    return torch.stack(output)


def cached_router_nll(router_logits: Tensor, cached_target_log_probs: Tensor, mask: Tensor | None = None) -> Tensor:
    """Algorithm 5: NLL of observed teacher tokens under a causal expert router.

    Cached tensor stores log π_k(y_t|prefix), not full teacher distributions;
    detached expert probabilities cannot receive training gradients. Causality
    is the caller's contract: logits must be computed from prefixes only.
    """
    if router_logits.shape != cached_target_log_probs.shape or router_logits.ndim != 3:
        raise ValueError("router and cached target log probabilities must be [batch,time,expert]")
    if not torch.isfinite(router_logits).all() or not torch.isfinite(cached_target_log_probs).all():
        raise ValueError("finite log probabilities required")
    if (cached_target_log_probs > 1e-6).any():
        raise ValueError("cached target log probabilities cannot be positive")
    nll = -torch.logsumexp(router_logits.log_softmax(-1) + cached_target_log_probs.detach(), -1)
    if mask is None:
        return nll.mean()
    if mask.shape != nll.shape or mask.dtype != torch.bool or not mask.any():
        raise ValueError("mask must be nonempty boolean [batch,time]")
    return nll[mask].mean()
