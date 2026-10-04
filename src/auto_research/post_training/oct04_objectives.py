"""Paper equations for T2SPO, Weakest-Link CRL and RLCPR.

These differentiable CPU-compatible objectives operate on actual rollout
statistics. They do not fabricate teacher probabilities or step predictions.
"""

from __future__ import annotations

import torch
from torch import Tensor


def _finite(x: Tensor, name: str) -> None:
    if not x.numel() or not torch.isfinite(x).all():
        raise ValueError(f"{name} must be nonempty and finite")


def t2spo_credit(
    distances: Tensor,
    successor_distances: Tensor,
    *,
    mask: Tensor,
    success_terminal: Tensor,
    failure_terminal: Tensor,
    truncated: Tensor,
    gamma: float = 1.0,
    weight: float = 1.0,
    cap: float = 3.0,
    optimizer: str = "grpo",
    gate: Tensor | None = None,
) -> Tensor:
    """Equations 6–8; normalize only supported, changed, valid turns.

    Caller combines prediction validity, historical support and observation
    change in mask. GRPO zeros truncations; PPO bootstraps their real successor.
    """
    _finite(distances, "distances")
    _finite(successor_distances, "successor_distances")
    arrays = (successor_distances, mask, success_terminal, failure_terminal, truncated)
    if any(x.shape != distances.shape for x in arrays):
        raise ValueError("turn tensors must have equal shapes")
    if any(x.dtype != torch.bool for x in (mask, success_terminal, failure_terminal, truncated)):
        raise ValueError("masks must be boolean")
    if not 0 < gamma <= 1 or weight < 0 or cap <= 0 or optimizer not in {"grpo", "ppo"}:
        raise ValueError("invalid credit configuration")
    if ((success_terminal.int() + failure_terminal.int() + truncated.int()) > 1).any():
        raise ValueError("terminal states are mutually exclusive")
    if (distances < 0).any() or (successor_distances < 0).any():
        raise ValueError("distances cannot be negative")
    gates = torch.ones_like(distances) if gate is None else gate
    _finite(gates, "gate")
    if gates.shape != distances.shape or ((gates < 0) | (gates > 1)).any():
        raise ValueError("gate must have turn shape and lie in [0, 1]")
    with torch.no_grad():
        successor = torch.where(success_terminal, 0.0, successor_distances)
        difference = distances - gamma * successor
        zero = failure_terminal | (truncated if optimizer == "grpo" else torch.zeros_like(mask))
        difference = torch.where(zero, 0.0, difference)
        z = difference.asinh()
        if not mask.any():
            return torch.zeros_like(z)
        rms = z[mask].square().mean().sqrt()
        credit = weight * gates * (z / (rms + 1e-8)).clamp(-cap, cap)
        return torch.where(mask, credit, 0.0)


def clipped_policy_loss(
    log_probs: Tensor, old_log_probs: Tensor, advantages: Tensor, mask: Tensor, *, clip: float = 0.2
) -> Tensor:
    """Token surrogate; observation/padding tokens have mask=False."""
    _finite(log_probs, "log_probs")
    if not 0 < clip < 1 or any(
        x.shape != log_probs.shape for x in (old_log_probs, advantages, mask)
    ):
        raise ValueError("invalid policy tensors or clip")
    if mask.dtype != torch.bool or not mask.any():
        raise ValueError("at least one generated token is required")
    _finite(old_log_probs, "old_log_probs")
    _finite(advantages, "advantages")
    ratios = (log_probs - old_log_probs.detach()).exp()
    adv = advantages.detach()
    objective = torch.minimum(ratios * adv, ratios.clamp(1 - clip, 1 + clip) * adv)
    return -objective[mask].mean()


def weakest_link_rewards(
    teacher_log_probs: Tensor, task_rewards: Tensor, *, budget: float, penalty: float
) -> tuple[Tensor, Tensor]:
    """Eq. 4–5: prefix average cost and absorbing infeasibility.

    Inputs are one unpadded trajectory. Violation at the current action affects
    its reward immediately and cannot be repaired by later cheap tokens.
    """
    _finite(teacher_log_probs, "teacher_log_probs")
    _finite(task_rewards, "task_rewards")
    if teacher_log_probs.ndim != 1 or task_rewards.shape != teacher_log_probs.shape:
        raise ValueError("expected equally sized one-dimensional trajectories")
    if (teacher_log_probs > 0).any() or budget < 0 or penalty <= 0:
        raise ValueError("invalid teacher probabilities, budget or penalty")
    costs = -teacher_log_probs.detach()
    prefix = costs.cumsum(0) / torch.arange(1, len(costs) + 1, device=costs.device)
    violated = (prefix > budget).int().cummax(0).values.bool()
    return torch.where(violated, -penalty, task_rewards.detach()), violated


def weakest_link_loss(
    logits: Tensor,
    actions: Tensor,
    teacher_log_probs: Tensor,
    task_rewards_by_action: Tensor,
    *,
    budget: float,
    penalty: float,
    gamma: float = 1.0,
) -> Tensor:
    """Section 3.3 exact vocabulary immediate term + future Monte Carlo term.

    One on-policy unpadded trajectory. Teacher scores cover every action at
    each visited prefix; no teacher data is needed at student inference time.
    """
    _finite(logits, "logits")
    _finite(teacher_log_probs, "teacher_log_probs")
    _finite(task_rewards_by_action, "task_rewards_by_action")
    if (
        logits.ndim != 2
        or teacher_log_probs.shape != logits.shape
        or task_rewards_by_action.shape != logits.shape
    ):
        raise ValueError("vocabulary tensors must have shape [turn, vocabulary]")
    if actions.shape != (len(logits),) or actions.dtype != torch.long:
        raise ValueError("actions must be a long tensor with one action per turn")
    if (actions < 0).any() or (actions >= logits.shape[1]).any():
        raise ValueError("action outside vocabulary")
    if not 0 < gamma <= 1 or budget < 0 or penalty <= 0 or (teacher_log_probs > 0).any():
        raise ValueError("invalid constraint configuration")
    with torch.no_grad():
        costs = -teacher_log_probs
        chosen_costs = costs.gather(1, actions[:, None]).squeeze(1)
        prior_sum = chosen_costs.cumsum(0) - chosen_costs
        count = torch.arange(1, len(logits) + 1, device=logits.device)
        previously_broken = torch.cat(
            (
                torch.zeros(1, device=logits.device, dtype=torch.bool),
                (chosen_costs.cumsum(0) / count > budget).int().cummax(0).values[:-1].bool(),
            )
        )
        broken = previously_broken[:, None] | (
            (prior_sum[:, None] + costs) / count[:, None] > budget
        )
        rewards = torch.where(broken, -penalty, task_rewards_by_action)
        sampled = rewards.gather(1, actions[:, None]).squeeze(1)
        future = torch.zeros_like(sampled)
        accumulated = torch.zeros((), device=logits.device, dtype=logits.dtype)
        for t in range(len(logits) - 1, -1, -1):
            future[t] = accumulated
            accumulated = sampled[t] + gamma * accumulated
        discount = gamma ** torch.arange(len(logits), device=logits.device)
    logp = logits.log_softmax(-1)
    immediate = (logp.exp() * rewards).sum(-1)
    long_term = gamma * future * logp.gather(1, actions[:, None]).squeeze(1)
    return -(discount * (immediate + long_term)).sum()


def rlcpr_sampling_probabilities(
    entropies: Tensor, *, quantiles=(0.33, 0.67), filter_rates=(0.0, 0.3, 0.7)
) -> Tensor:
    """Eq. 15 expected retained distribution; ties use strict empirical CDF."""
    _finite(entropies, "entropies")
    if entropies.ndim != 1 or (entropies < 0).any():
        raise ValueError("entropies must be a nonnegative vector")
    lo, hi = quantiles
    if (
        not 0 <= lo <= hi <= 1
        or len(filter_rates) != 3
        or any(not 0 <= r <= 1 for r in filter_rates)
    ):
        raise ValueError("invalid bins or filtering rates")
    with torch.no_grad():
        cdf = (entropies[:, None] > entropies[None, :]).to(entropies.dtype).mean(1)
        bins = (cdf >= lo).long() + (cdf >= hi).long()
        weights = 1 - entropies.new_tensor(filter_rates)[bins]
        if weights.sum() <= 0:
            raise ValueError("filtering removed every example")
        return weights / weights.sum()


def rlcpr_rewards(
    posteriors: Tensor,
    lengths: Tensor,
    *,
    length_quantile: float = 0.5,
    gap_quantile: float = 0.5,
    strength: float = 1.0,
) -> tuple[Tensor, Tensor]:
    """Eq. 16–19 for a rectangular batch of rollout groups."""
    _finite(posteriors, "posteriors")
    _finite(lengths, "lengths")
    if posteriors.ndim != 2 or lengths.shape != posteriors.shape:
        raise ValueError("expected [group, rollout] matrices")
    if ((posteriors < 0) | (posteriors > 1)).any() or (lengths < 0).any():
        raise ValueError("invalid probabilities or lengths")
    if not 0 <= length_quantile <= 1 or not 0 <= gap_quantile <= 1 or strength < 0:
        raise ValueError("invalid regularization settings")
    with torch.no_grad():
        gaps = posteriors.max(1).values - posteriors.min(1).values
        lens = lengths.to(posteriors.dtype)
        minimum, maximum = lens.min(1).values, lens.max(1).values
        delta = torch.quantile(lens.flatten(), length_quantile)
        alpha = torch.quantile(gaps, gap_quantile)
        active = (minimum > delta) & (gaps < alpha)
        penalty = (
            -active[:, None].to(lens.dtype)
            * (lens - minimum[:, None])
            / (maximum - minimum).clamp_min(1)[:, None]
        )
        return posteriors.detach() + strength * penalty, active
