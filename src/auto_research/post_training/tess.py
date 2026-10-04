"""TESS sequential model fitting and Pointwise Value Matching (Algorithm 1)."""

from __future__ import annotations

import copy
import torch
from torch import nn, Tensor


def pointwise_value_matching(
    predictions: Tensor, train_only_losses: Tensor, validation_guided_losses: Tensor
) -> Tensor:
    """Eq. 7; pseudo-targets never backpropagate into either source model."""
    if (
        predictions.shape != train_only_losses.shape
        or predictions.shape != validation_guided_losses.shape
    ):
        raise ValueError("sample predictions and losses must have identical shape")
    if not predictions.numel() or not all(
        torch.isfinite(x).all() for x in (predictions, train_only_losses, validation_guided_losses)
    ):
        raise ValueError("PVM inputs must be nonempty and finite")
    target = (train_only_losses - validation_guided_losses).detach()
    return (predictions - target).square().mean()


def fit_tess(
    initial_model: nn.Module,
    selector: nn.Module,
    *,
    train_batch,
    validation_batch,
    pool_features: Tensor,
    train_features: Tensor,
    per_example_loss,
    steps: int = 100,
    selector_steps: int = 100,
    learning_rate: float = 0.01,
    alpha: float = 1.0,
):
    """Sequential U -> W -> selector training with supplied differentiable loss.

    ``per_example_loss(model, batch)`` returns one loss per example. This accepts
    token-averaged LM losses or a diagnostic classifier loss without silently
    replacing one with the other. The function has no test-data argument.
    U and W start from the same initial weights and are optimized independently.
    """
    if min(steps, selector_steps) < 1 or learning_rate <= 0 or alpha <= 0:
        raise ValueError("invalid training budget")
    if (
        train_features.ndim != 2
        or pool_features.ndim != 2
        or train_features.shape[1] != pool_features.shape[1]
    ):
        raise ValueError("feature matrices must have the same dimension")
    targets = []
    for validation_guided in (False, True):
        model = copy.deepcopy(initial_model)
        model.train()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        for _ in range(steps):
            optimizer.zero_grad()
            train_loss = per_example_loss(model, train_batch)
            if train_loss.shape != (len(train_features),) or not torch.isfinite(train_loss).all():
                raise ValueError("loss callback must return one finite training loss per example")
            loss = train_loss.mean()
            if validation_guided:
                validation_loss = per_example_loss(model, validation_batch)
                if not validation_loss.numel() or not torch.isfinite(validation_loss).all():
                    raise ValueError("invalid validation losses")
                loss = alpha * loss + validation_loss.mean()
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.no_grad():
            targets.append(per_example_loss(model, train_batch).detach().clone())
        # Retain only sample losses: the two trained models need not coexist.
        del optimizer, model
    selector.train()
    optimizer = torch.optim.Adam(selector.parameters(), lr=learning_rate)
    losses = []
    for _ in range(selector_steps):
        optimizer.zero_grad()
        predictions = selector(train_features).reshape(-1)
        loss = pointwise_value_matching(predictions, targets[0], targets[1])
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    selector.eval()
    with torch.no_grad():
        pool_scores = selector(pool_features).reshape(-1).detach()
    return {
        "scores": pool_scores,
        "pseudo_labels": targets[0] - targets[1],
        "pvm_losses": losses,
        "selector": selector,
    }
