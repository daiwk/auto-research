"""RACE's LoGiC progressive cover and cover-aware actor objective.

Training trajectories may contain successful reference actions. This module is
not an inference policy and never returns a reference action to an agent.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
import math
from typing import Callable


@dataclass(frozen=True)
class Turn:
    reasoning: str
    action: str
    observation: str
    token_ids: tuple[int, ...] = ()
    sampled_mask: tuple[bool, ...] = ()
    action_choices: tuple[str, ...] = ()
    raw_target: str = ""


@dataclass(frozen=True)
class TrainingTrajectory:
    question: str
    turns: tuple[Turn, ...]
    successful: bool
    split: str = "train"

    def __post_init__(self):
        if self.split != "train" or not self.turns or not self.question:
            raise ValueError("LoGiC accepts only nonempty training trajectories")
        if any(not turn.action for turn in self.turns):
            raise ValueError("reference actions must be nonempty")


def logic_cover(trajectory: TrainingTrajectory,
                action_likelihoods: Callable[[TrainingTrajectory], tuple[float, ...]],
                epsilon=0.001):
    """Algorithm 1; verify all later actions and carry accepted removals forward."""
    if epsilon < 0 or not trajectory.successful:
        raise ValueError("cover construction requires successful training rollouts")
    current = trajectory
    reference = tuple(action_likelihoods(current))
    if len(reference) != len(current.turns) or not all(math.isfinite(v) for v in reference):
        raise ValueError("one finite mean token log-likelihood per action required")
    skipped, audit = [], []
    for index in range(1, len(current.turns)):
        turns = list(current.turns)
        turns[index] = replace(turns[index], reasoning="")
        candidate = replace(current, turns=tuple(turns))
        scores = tuple(action_likelihoods(candidate))
        if len(scores) != len(reference) or not all(math.isfinite(v) for v in scores):
            raise ValueError("invalid candidate action likelihood vector")
        decreases = [reference[j] - scores[j] for j in range(index, len(scores))]
        accept = all(value <= epsilon for value in decreases)
        audit.append({"turn": index, "accepted": accept, "later_action_decreases": decreases})
        if accept:
            current, reference = candidate, scores
            skipped.append(index)
    return current, tuple(skipped), audit


def cover_aware_loss(current_logp, old_logp, advantage, policy_mask, skipped_reasoning_mask,
                     closure_logp, total_turns, *, clip=.2, closure_weight=.02):
    """Eq.13–15: retain original token/turn denominators after masking.

    skipped_reasoning_mask and closure_logp must come only from LoGiC-verified
    successful rollouts; failed rollouts retain ordinary GRPO policy masks.
    """
    import torch

    if current_logp.shape != old_logp.shape or current_logp.shape != policy_mask.shape:
        raise ValueError("unaligned token arrays")
    if skipped_reasoning_mask.shape != policy_mask.shape or not bool(policy_mask.any()):
        raise ValueError("nonempty policy tokens required")
    if total_turns <= 0 or closure_weight < 0 or not 0 < clip < 1:
        raise ValueError("invalid turns or loss hyperparameters")
    ratio = (current_logp - old_logp.detach()).exp()
    labels = advantage.detach()
    if labels.ndim == 1:
        labels = labels[:, None]
    retained = policy_mask.bool() & ~skipped_reasoning_mask.bool()
    surrogate = torch.minimum(ratio * labels, ratio.clamp(1 - clip, 1 + clip) * labels)
    actor = -(surrogate * retained).sum() / policy_mask.sum()
    closure = -closure_logp.sum() / total_turns
    return actor + closure_weight * closure
