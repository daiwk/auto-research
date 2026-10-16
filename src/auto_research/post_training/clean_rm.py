"""CleanRM (2610.21138), actual joint optimal transport and corrected loss.

The bounded exact solver handles uniform equal-size empirical batches, at most
12 points. It solves the *unregularized* assignment OT, not a nearest-neighbor
heuristic. Encoded features replace the paper's large backbone only in L1 demos.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class NoiseEstimator(nn.Module):
    """Two directional rates with mu + nu <= 1 - margin by construction."""
    def __init__(self, feature_dim: int, hidden_dim: int = 16, margin: float = .05):
        super().__init__()
        if feature_dim < 1 or hidden_dim < 1 or not 0 < margin < 1:
            raise ValueError("positive dimensions and margin in (0,1) required")
        self.network = nn.Sequential(nn.Linear(feature_dim, hidden_dim), nn.Tanh(), nn.Linear(hidden_dim, 3))
        self.margin = margin

    def forward(self, features: Tensor) -> tuple[Tensor, Tensor]:
        probabilities = self.network(features).softmax(-1) * (1 - self.margin)
        return probabilities[..., 0], probabilities[..., 1]


def _rates(mu: Tensor, nu: Tensor, labels: Tensor) -> None:
    if mu.shape != nu.shape or mu.shape != labels.shape:
        raise ValueError("one pair of directional noise rates per label required")
    if not all(torch.isfinite(x).all() for x in (mu, nu, labels)):
        raise ValueError("labels and noise estimates must be finite")
    if (mu < 0).any() or (nu < 0).any() or (mu + nu >= 1).any():
        raise ValueError("nonnegative nondegenerate directional rates required")
    if ((labels != 0) & (labels != 1)).any():
        raise ValueError("observed feedback must be binary")


def recover_preferences(labels: Tensor, mu: Tensor, nu: Tensor) -> Tensor:
    """Eq. 5; do not clip to [0,1], which would change the paper objective."""
    _rates(mu, nu, labels)
    return (labels.detach() - nu) / (1 - mu - nu)


def _minmax(values: Tensor) -> Tensor:
    low, high = values.min(), values.max()
    scale = high - low
    return (values - low) / scale.clamp_min(torch.finfo(values.dtype).eps)


def joint_cost(noisy_features: Tensor, recovered: Tensor,
               clean_features: Tensor, clean_labels: Tensor) -> Tensor:
    """Eq. 7: separately min-max-normalized semantic and preference costs."""
    if noisy_features.ndim != 2 or clean_features.ndim != 2 or noisy_features.shape[1] != clean_features.shape[1]:
        raise ValueError("two feature matrices with the same feature dimension required")
    if recovered.shape != noisy_features.shape[:1] or clean_labels.shape != clean_features.shape[:1]:
        raise ValueError("labels must align with their own feature rows")
    if not all(torch.isfinite(v).all() for v in (noisy_features, clean_features, recovered, clean_labels)):
        raise ValueError("joint transport inputs must be finite")
    semantic = torch.cdist(noisy_features.detach(), clean_features.detach()).square()
    preference = (recovered[:, None] - clean_labels.detach()[None, :]).square()
    return _minmax(semantic) + _minmax(preference)


def exact_uniform_transport(cost: Tensor) -> tuple[Tensor, Tensor]:
    """Exact equal-mass OT via subset-DP; gradient uses the optimal-plan envelope.

    A uniform square empirical transport polytope has a permutation optimum.
    The discrete argmin is detached, while <C,T*> keeps the real cost gradient.
    This CPU selection is deliberately small and is not a scalable OT engine.
    """
    if cost.ndim != 2 or cost.shape[0] != cost.shape[1] or not 1 <= cost.shape[0] <= 12:
        raise ValueError("bounded exact OT requires equal batches of 1--12 points")
    if not torch.isfinite(cost).all() or (cost < 0).any():
        raise ValueError("finite nonnegative transport costs required")
    values = cost.detach().double().cpu().tolist()
    size = len(values)
    best = {0: (0., ())}
    for mask in range(1 << size):
        if mask not in best:
            continue
        value, assignment = best[mask]
        row = len(assignment)
        if row == size:
            continue
        for column in range(size):
            if mask & (1 << column):
                continue
            new_mask, candidate = mask | (1 << column), value + values[row][column]
            if new_mask not in best or candidate < best[new_mask][0]:
                best[new_mask] = (candidate, assignment + (column,))
    assignment = best[(1 << size) - 1][1]
    plan = torch.zeros_like(cost)
    plan[torch.arange(size, device=cost.device), torch.tensor(assignment, device=cost.device)] = 1 / size
    return (cost * plan).sum(), plan.detach()


def noise_estimation_loss(estimator: NoiseEstimator, noisy_features: Tensor, noisy_labels: Tensor,
                          clean_features: Tensor, clean_labels: Tensor) -> tuple[Tensor, dict[str, Tensor]]:
    """Algorithm 1: learn noise rates from noisy data + a separate clean subset."""
    mu, nu = estimator(noisy_features.detach())
    recovered = recover_preferences(noisy_labels, mu, nu)
    cost = joint_cost(noisy_features, recovered, clean_features, clean_labels)
    loss, plan = exact_uniform_transport(cost)
    return loss, {"mu": mu.detach(), "nu": nu.detach(), "recovered": recovered.detach(), "plan": plan}


def corrected_reward_loss(prediction: Tensor, observed: Tensor, mu: Tensor, nu: Tensor,
                          *, family: str = "square", reduction: str = "mean") -> Tensor:
    """Eqs. 10--11 with detached estimated rates, not oracle corruption labels.

    The signed surrogate may be negative. `family=logistic` accepts logits;
    `square` accepts unconstrained scalar predictions, as in the RM regression.
    """
    mu, nu = mu.detach(), nu.detach()
    _rates(mu, nu, observed)
    if prediction.shape != observed.shape or not torch.isfinite(prediction).all():
        raise ValueError("one finite reward prediction per binary observation required")
    if family == "square":
        one, zero = (prediction - 1).square(), prediction.square()
    elif family == "logistic":
        one, zero = F.softplus(-prediction), F.softplus(prediction)
    else:
        raise ValueError("loss family must be square or logistic")
    denominator = 1 - mu - nu
    positive = ((1 - nu) * one - mu * zero) / denominator
    negative = ((1 - mu) * zero - nu * one) / denominator
    losses = torch.where(observed.bool(), positive, negative)
    if reduction == "none":
        return losses
    if reduction != "mean" or not losses.numel():
        raise ValueError("nonempty losses and reduction mean/none required")
    return losses.mean()
