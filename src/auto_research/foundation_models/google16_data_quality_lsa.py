"""Exact linear-self-attention core from arXiv:2603.01293 Eq.3.1–4.1.

OS here is outcome-supervised regression, NOT a policy-gradient RL algorithm.
Ground-truth intermediate states occur only in the explicit SFT training loss;
autonomous rollout accepts context labels but never the target weight vector.
"""
from __future__ import annotations

import torch
from torch import Tensor


def lsa_forward(z: Tensor, value: Tensor, query_key: Tensor, scale: float) -> Tensor:
    if z.ndim != 3 or value.shape != (z.shape[1], z.shape[1]) or query_key.shape != value.shape:
        raise ValueError("LSA requires z [batch,feature,token] and square V/W")
    if scale <= 0 or not all(torch.isfinite(t).all() for t in (z, value, query_key)):
        raise ValueError("positive scale and finite LSA tensors required")
    return z + (value @ z) @ (z.transpose(-2, -1) @ query_key @ z) / scale


def context_embedding(x: Tensor, y: Tensor) -> Tensor:
    if x.ndim != 3 or y.shape != x.shape[:2] or not x.shape[1]:
        raise ValueError("x [batch,n,d], y [batch,n] required")
    if not torch.isfinite(x).all() or not torch.isfinite(y).all():
        raise ValueError("finite context required")
    batch, n, dim = x.shape
    z = x.new_zeros(batch, 2 * dim + 2, n + 1)
    z[:, :dim, :n] = x.transpose(-2, -1)
    z[:, dim, :n] = y
    z[:, -1, -1] = 1
    return z


def population_initialization(covariance: Tensor, n: int) -> tuple[Tensor, Tensor]:
    if covariance.ndim != 2 or covariance.shape[0] != covariance.shape[1] or n <= 0:
        raise ValueError("square covariance and positive prompt length required")
    if not torch.isfinite(covariance).all() or not torch.allclose(covariance, covariance.T):
        raise ValueError("covariance must be finite symmetric positive definite")
    torch.linalg.cholesky(covariance)
    dim = len(covariance)
    identity = torch.eye(dim, device=covariance.device, dtype=covariance.dtype)
    gamma = (1 + 1 / n) * covariance + covariance.trace() / n * identity
    value = covariance.new_zeros(2 * dim + 2, 2 * dim + 2)
    query_key = torch.zeros_like(value)
    value[dim + 1:2 * dim + 1, :dim] = -torch.linalg.inv(gamma)
    query_key[:dim, dim + 1:2 * dim + 1] = identity
    query_key[dim, -1] = -1
    return value, query_key


def rollout(x: Tensor, y: Tensor, value: Tensor, query_key: Tensor, steps: int) -> Tensor:
    if steps <= 0:
        raise ValueError("positive rollout steps required")
    z = context_embedding(x, y)
    predictions = []
    dim, n = x.shape[-1], x.shape[1]
    for _ in range(steps):
        token = lsa_forward(z, value, query_key, n)[:, :, -1:]
        predictions.append(token[:, dim + 1:2 * dim + 1, 0])
        z = torch.cat((z, token), dim=-1)
    return torch.stack(predictions, dim=1)


def outcome_supervision_loss(x: Tensor, y: Tensor, training_weights: Tensor,
                             value: Tensor, query_key: Tensor, steps: int) -> Tensor:
    prediction = rollout(x, y, value, query_key, steps)[:, -1]
    if prediction.shape != training_weights.shape:
        raise ValueError("training weight targets must have shape [batch,d]")
    return (prediction - training_weights).square().sum() / (2 * len(x))


def sft_loss(x: Tensor, y: Tensor, training_weights: Tensor, value: Tensor,
             query_key: Tensor, k: int, rate: float) -> Tensor:
    """Eq.3.5: teacher forced i=0..k, including every token-coordinate loss."""
    if k < 0 or not 0 < rate <= 1 or training_weights.shape != (len(x), x.shape[-1]):
        raise ValueError("valid SFT k/rate and [batch,d] training targets required")
    z = context_embedding(x, y)
    dim, n = x.shape[-1], x.shape[1]
    loss = x.new_zeros(())
    for index in range(k + 1):
        prediction = lsa_forward(z, value, query_key, n)[:, :, -1:]
        target = x.new_zeros(len(x), 2 * dim + 2, 1)
        target[:, dim + 1:2 * dim + 1, 0] = (1 - (1 - rate) ** (index + 1)) * training_weights
        target[:, -1] = 1
        loss = loss + (prediction - target).square().sum() / (2 * len(x))
        z = torch.cat((z, target), dim=-1)
    return loss


def closest_sft_value(x: Tensor, training_weights: Tensor, covariance: Tensor, rate: float) -> Tensor:
    """Eq.4.1: nonzero V31 block of closest SFT solution (W13 fixed identity)."""
    if x.ndim != 3 or training_weights.shape != (len(x), x.shape[-1]) or not 0 < rate <= 1:
        raise ValueError("valid SFT context/target/rate required")
    _, n, dim = x.shape
    value, _ = population_initialization(covariance, n)
    empirical = x.transpose(-2, -1) @ x / n
    phi = (empirical @ training_weights[..., None]).squeeze(-1).T
    omega = training_weights.T
    inverse = torch.linalg.pinv(phi)
    projector = phi @ inverse
    initial = value[dim + 1:2 * dim + 1, :dim]
    return -rate * omega @ inverse + initial @ (torch.eye(dim, device=x.device, dtype=x.dtype) - projector)
