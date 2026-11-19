"""ECA v1 training-only evidence returns and search-local policy objective.

This operator consumes externally scored training potentials, never answers.
It does not implement a retriever, scorer checkpoint, or evaluated agent.
"""

import torch

from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def evidence_returns(potentials, *, mode="horizon", clip_increment=2.0):
    tensor(potentials, "potentials", ndim=2)
    if potentials.shape != (8, 4) or mode not in {"horizon", "step"}:
        raise ValueError("v1 requires eight rollouts, three search slots, and a known mode")
    c = scalar(clip_increment, "clip_increment", lower=0, strict_lower=True)
    p = potentials.detach()
    if mode == "horizon":
        return (p[:, -1:] - p[:, :-1]) / (3 * c)
    delta = (p[:, 1:] - p[:, :-1]).clamp(-c, c)
    return delta.flip(-1).cumsum(-1).flip(-1) / (3 * c)


def cross_fold_advantages(returns, folds, novel_documents):
    tensor(returns, "returns", ndim=2)
    if returns.shape != (8, 3):
        raise ValueError("v1 requires eight rollouts and three search slots")
    if (not isinstance(folds, torch.Tensor) or folds.shape != (8,)
            or folds.dtype != torch.long or folds.device != returns.device
            or not bool(((folds == 0) | (folds == 1)).all())
            or int((folds == 0).sum()) != 4):
        raise ValueError("two disjoint four-rollout folds required")
    if (not isinstance(novel_documents, torch.Tensor) or novel_documents.dtype != torch.bool
            or novel_documents.shape != returns.shape or novel_documents.device != returns.device):
        raise ValueError("same-shape Boolean novelty gate required")
    u = returns.detach()
    z = torch.empty_like(u)
    for fold in (0, 1):
        ref = u[folds != fold]
        z[folds == fold] = ((u[folds == fold] - ref.mean(0))
                            / ref.std(0, correction=1).clamp_min(0.25)).clamp(-2, 2)
    return torch.where(novel_documents, z, z.clamp_max(0))


def token_advantages(rewards, search_credit, search_token_mask, policy_token_mask, *, weight=0.1):
    tensor(rewards, "rewards", ndim=1)
    tensor(search_credit, "search_credit", shape=(8, 3), device=rewards.device)
    if rewards.shape != (8,) or not bool(((rewards == 0) | (rewards == 1)).all()):
        raise ValueError("eight binary terminal rewards required")
    if (not isinstance(policy_token_mask, torch.Tensor) or policy_token_mask.dtype != torch.bool
            or policy_token_mask.ndim != 2 or policy_token_mask.shape[0] != 8
            or policy_token_mask.device != rewards.device or not bool(policy_token_mask.any(-1).all())):
        raise ValueError("nonempty policy-token mask per rollout required")
    expected = (8, 3, policy_token_mask.shape[1])
    if (not isinstance(search_token_mask, torch.Tensor) or search_token_mask.dtype != torch.bool
            or search_token_mask.shape != expected or search_token_mask.device != rewards.device
            or bool((search_token_mask.sum(1) > 1).any())
            or bool((search_token_mask.any(1) & ~policy_token_mask).any())):
        raise ValueError("disjoint search actions must contain only generated policy tokens")
    lam = scalar(weight, "weight", lower=0)
    r = rewards.detach()
    outcome = (r-r.mean()) / (r.std(correction=1)+1e-6)
    aux = (search_credit.detach().unsqueeze(-1) * search_token_mask).sum(1)
    return (outcome[:, None]+lam*aux).detach()


def policy_loss(current_logp, behavior_logp, advantages, policy_token_mask):
    tensor(current_logp, "current", ndim=2)
    tensor(behavior_logp, "behavior", shape=current_logp.shape, device=current_logp.device)
    tensor(advantages, "advantages", shape=current_logp.shape, device=current_logp.device)
    if (not isinstance(policy_token_mask, torch.Tensor) or policy_token_mask.dtype != torch.bool
            or policy_token_mask.shape != current_logp.shape
            or policy_token_mask.device != current_logp.device
            or not bool(policy_token_mask.any(-1).all())):
        raise ValueError("nonempty policy mask per trajectory required")
    log_ratio = torch.where(policy_token_mask, current_logp-behavior_logp.detach(), 0.)
    ratio = log_ratio.exp()
    # Eq.9: sum policy tokens, then mean trajectories; no ratio clipping or KL.
    terms = torch.where(policy_token_mask, ratio*advantages.detach(), 0.)
    return -terms.sum(-1).mean()


def diagnostic(seed, device="cpu"):
    generator = seeded(seed, device)
    p = torch.tensor([[-8., -4., -7., -7.]]*8, device=device, dtype=torch.float64)
    p[1:, 1:] += torch.randn(7, 3, generator=generator, dtype=torch.float64).to(device)*0.01
    h, s = evidence_returns(p), evidence_returns(p, mode="step")
    folds = torch.tensor([0]*4+[1]*4, dtype=torch.long, device=device)
    novelty = torch.ones(8, 3, dtype=torch.bool, device=device)
    novelty[0, 0] = False
    z = cross_fold_advantages(h, folds, novelty)
    policy = torch.tensor([[True, True, True, False]]*8, device=device)
    search = torch.zeros(8, 3, 4, dtype=torch.bool, device=device)
    search[:, 0, 0], search[:, 1, 1] = True, True
    adv = token_advantages(torch.zeros(8, device=device), z, search, policy)
    lp = torch.zeros(8, 4, device=device, dtype=torch.float64, requires_grad=True)
    old = torch.zeros_like(lp, requires_grad=True)
    out = policy_loss(lp, old, adv, policy)
    out.backward()
    return receipt(seed, "l1_mechanism", {
        "horizon_preserves_telescope": abs(h[0, 0].item()-1/6) < 1e-12,
        "step_clipping_erases_spike_gain": s[0, 0].item() == 0,
        "novelty_never_gives_positive_repeat_credit": z[0, 0].item() <= 0,
        "all_failure_search_gradient_survives": bool(lp.grad[:, :2].abs().sum() > 0),
        "final_answer_and_observations_have_no_auxiliary_gradient": bool((lp.grad[:, 2:] == 0).all()),
        "behavior_is_frozen": old.grad is None,
    }, {"loss": out.item(), "horizon_return": h[0, 0].item(),
        "step_return": s[0, 0].item(), "search_gradient_norm": lp.grad.norm().item()})
