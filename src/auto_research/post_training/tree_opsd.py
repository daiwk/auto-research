"""TreeOPSD's exact tree backup and finite Bernoulli-target objective.

This is a defining L1 component, not a search environment or an LLM verifier.
Only actor-token log probabilities enter the objective; observations are context.
"""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
import math

import torch
from torch import Tensor
from torch.nn import functional as F


@dataclass(frozen=True)
class Turn:
    actor: tuple[int, ...]
    observation: tuple[int, ...] = ()


def merge_rollout_prefixes(prompt: tuple[int, ...], rollouts: Sequence[Sequence[Turn]]) -> dict:
    """Merge complete history prefixes, not just equal final actor strings.

    A terminal/nonterminal flag is part of the identity: an otherwise identical
    stopped response and a continuing response are different sampled events.
    Duplicate complete trajectories retain duplicate leaf indices for K/std.
    """
    if not prompt or not rollouts:
        raise ValueError("a public prompt and nonempty rollouts are required")
    nodes, leaves, seen = [], [], {}
    for rollout in rollouts:
        if not rollout:
            raise ValueError("empty rollout")
        history, parent = prompt, -1
        for position, turn in enumerate(rollout):
            if not isinstance(turn, Turn) or not turn.actor:
                raise ValueError("every turn requires actor tokens")
            terminal = position == len(rollout) - 1
            if terminal and turn.observation:
                raise ValueError("terminal answer cannot contain an observation")
            # Parent and full history prevent accidental merging across branches.
            key = (parent, history, turn.actor, turn.observation, terminal)
            if key not in seen:
                seen[key] = len(nodes)
                nodes.append({"parent": parent, "history": history, "actor": turn.actor,
                              "observation": turn.observation, "terminal": terminal})
            parent = seen[key]
            history += turn.actor + turn.observation
        leaves.append(parent)
    return {"nodes": nodes, "leaf_indices": leaves}


def tree_credit(parents: Sequence[int], behavior_span_logp: Tensor,
                leaf_indices: Sequence[int], rewards: Tensor) -> Tensor:
    """Equations 4--5: sample-std leaf credit and likelihood-weighted backup."""
    n = len(parents)
    if n == 0 or behavior_span_logp.shape != (n,) or not behavior_span_logp.is_floating_point():
        raise ValueError("one floating behavior span log probability per node required")
    if rewards.shape != (len(leaf_indices),) or len(leaf_indices) < 2 or not rewards.is_floating_point():
        raise ValueError("at least two floating terminal rewards required")
    if rewards.device != behavior_span_logp.device:
        raise ValueError("credit tensors must share a device")
    if not torch.isfinite(behavior_span_logp).all() or not torch.isfinite(rewards).all():
        raise ValueError("finite behavior probabilities and rewards required")
    children = [[] for _ in parents]
    for node, parent in enumerate(parents):
        if type(parent) is not int or parent < -1 or parent >= node:
            raise ValueError("parents must form an acyclic topologically ordered tree/forest")
        if parent >= 0:
            children[parent].append(node)
    if any(type(i) is not int or not 0 <= i < n for i in leaf_indices):
        raise ValueError("invalid terminal node")
    if set(leaf_indices) != {i for i, values in enumerate(children) if not values}:
        raise ValueError("terminal rewards must cover exactly all tree leaves")
    reward = rewards.detach()
    deviation = reward.std(correction=1)
    advantages = torch.zeros_like(reward) if deviation == 0 else (reward - reward.mean()) / deviation
    result = torch.empty(n, dtype=reward.dtype, device=reward.device)
    assigned = {}
    for leaf, value in zip(leaf_indices, advantages, strict=True):
        if leaf in assigned and not torch.equal(assigned[leaf], value):
            raise ValueError("one merged terminal trajectory cannot have conflicting rewards")
        result[leaf] = value
        assigned[leaf] = value
    old = behavior_span_logp.detach().to(reward.dtype)
    for node in reversed(range(n)):
        if children[node]:
            indices = children[node]
            result[node] = (old[indices].softmax(0) * result[indices]).sum()
    return result.detach()


def posterior_loss(current_logp: Tensor, behavior_logp: Tensor, actor_mask: Tensor,
                   credit: Tensor, *, terminal_count: int, rho: float = .25) -> tuple[Tensor, dict]:
    """Equations 8--15, with no target clipping and detached tree teachers."""
    if current_logp.ndim != 2 or current_logp.shape != behavior_logp.shape:
        raise ValueError("aligned [unique turn, token] log probabilities required")
    if actor_mask.shape != current_logp.shape or actor_mask.dtype != torch.bool:
        raise ValueError("aligned Boolean actor mask required")
    if credit.shape != (current_logp.shape[0],) or not bool(actor_mask.any(1).all()):
        raise ValueError("each unique turn needs credit and at least one actor token")
    if any(value.device != current_logp.device for value in (behavior_logp, actor_mask, credit)):
        raise ValueError("objective tensors must share a device")
    if not current_logp.is_floating_point() or not behavior_logp.is_floating_point() or not credit.is_floating_point():
        raise ValueError("floating log probabilities and credit required")
    if not torch.isfinite(current_logp[actor_mask]).all() or not torch.isfinite(behavior_logp[actor_mask]).all() or not torch.isfinite(credit).all():
        raise ValueError("finite active actor probabilities and credits required")
    if type(terminal_count) is not int or terminal_count < 2 or not 0 < rho < .5 or not math.isfinite(rho):
        raise ValueError("K>=2 and finite 0<rho<1/2 required")
    lengths = actor_mask.sum(1).to(current_logp.dtype)
    difference = torch.where(actor_mask, current_logp, 0.) - torch.where(actor_mask, behavior_logp.detach(), 0.)
    score = difference.sum(1) / lengths
    tau = (terminal_count - 1) / (rho * math.sqrt(terminal_count))
    target = .5 + credit.detach().to(current_logp.dtype) / tau
    tolerance = 16 * torch.finfo(target.dtype).eps
    if bool(((target < .5 - rho - tolerance) | (target > .5 + rho + tolerance)).any()):
        raise ValueError("credit violates the standardized-leaf TreeOPSD bound; do not clip targets")
    entropy = -(target * target.log() + (1 - target) * (1 - target).log())
    divergence = F.binary_cross_entropy_with_logits(score, target, reduction="none") - entropy
    loss = tau * (lengths * divergence).sum() / lengths.sum()
    return loss, {"target": target.detach(), "posterior": score.detach().sigmoid(),
                  "tau": tau, "unique_actor_tokens": int(lengths.sum())}
