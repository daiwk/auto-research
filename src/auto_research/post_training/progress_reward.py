"""PRM4RL (NeurIPS 2025; arXiv 2610.22056), reviewed plan interfaces.

No generated Python is executed. Callers supply reviewed state predicates,
potential and sentence embeddings; this component is not an LLM planner.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import torch
from torch import Tensor


@dataclass(frozen=True)
class ProgressPlan:
    subtasks: tuple[str, ...]
    completed: tuple[Callable[[Tensor], Tensor], ...]
    potential: Callable[[Tensor], Tensor]

    def stage(self, states: Tensor) -> Tensor:
        """First incomplete ordered subtask, recomputed from the current state.

        Unlike a history-only monotone counter this permits a grasp to be lost.
        The terminal state retains the final subtask embedding.
        """
        if states.ndim != 2 or not self.subtasks or len(self.completed) != len(self.subtasks):
            raise ValueError("nonempty reviewed plan and batched states required")
        checks = [predicate(states) for predicate in self.completed]
        if any(c.shape != states.shape[:1] or c.dtype != torch.bool for c in checks):
            raise ValueError("completion predicates must return one boolean per state")
        prefix_completed = torch.stack(checks, -1).long().cumprod(-1).sum(-1)
        return prefix_completed.clamp_max(len(self.subtasks) - 1)

    def progress(self, states: Tensor) -> Tensor:
        result = self.potential(states)
        if result.shape != states.shape[:1] or not torch.isfinite(result).all():
            raise ValueError("potential must return one finite scalar per state")
        return result


def augment_state(states: Tensor, plan: ProgressPlan, sentence_embeddings: Tensor) -> Tensor:
    """[state, E(plan_list[Psi(state)])]; E is supplied, never inferred from gold."""
    if sentence_embeddings.ndim != 2 or sentence_embeddings.shape[0] != len(plan.subtasks):
        raise ValueError("one fixed-size embedding per reviewed subtask required")
    if states.device != sentence_embeddings.device or not torch.isfinite(sentence_embeddings).all():
        raise ValueError("finite embeddings on the state device required")
    return torch.cat((states, sentence_embeddings[plan.stage(states)]), -1)


def progress_reward(current: Tensor, following: Tensor, success: Tensor, *,
                    gamma: float = .99, bonus: float = 1., terminated: Tensor | None = None) -> Tensor:
    """Eq. 3, with explicit episodic absorbing-state handling.

    True terminal potential is zero when `terminated` is supplied; time-limit
    truncations must *not* be marked terminal. Without this argument Eq. 3 is
    applied literally, suitable for a continuing/absorbing trajectory.
    """
    if current.shape != following.shape or success.shape != current.shape or current.ndim != 1:
        raise ValueError("one current/next potential and success indicator per transition required")
    if not 0 <= gamma <= 1 or not torch.isfinite(current).all() or not torch.isfinite(following).all():
        raise ValueError("finite potentials and gamma in [0,1] required")
    if success.dtype != torch.bool or not torch.isfinite(torch.tensor(bonus)):
        raise ValueError("boolean success and finite success bonus required")
    if terminated is not None:
        if terminated.shape != current.shape or terminated.dtype != torch.bool:
            raise ValueError("boolean true-terminal mask must match transitions")
        following = following.masked_fill(terminated, 0)
    return gamma * following - current + success.to(current.dtype) * bonus
