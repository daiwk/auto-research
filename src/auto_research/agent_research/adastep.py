"""AdaStep's group-statistic step-credit operator (arXiv:2610.03223).

Uses observed actions and discounted returns only. Gold plans/answers and
future test labels must never be passed into this training-time operator.
"""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class StepObservation:
    task_id: str
    anchor_state: str
    action: str
    discounted_return: float
    episode_advantage: float


@dataclass(frozen=True)
class StepCredit:
    coefficient: float
    local_advantage: float
    combined_advantage: float
    estimable: bool


def assign_step_credit(
    observations: list[StepObservation], *, normalize_local: bool = False
) -> list[StepCredit]:
    """Apply paper Eq. 17-18 per anchor-state group.

    Population variances use N and n_a, *not* sample (N-1) denominators.
    The paper's sparse/non-estimable fallback is w=1. Identical returns yield
    zero local advantage, so their coefficient is immaterial.
    """
    if not observations:
        raise ValueError("at least one observed step is required")
    groups: dict[tuple[str, str], list[int]] = defaultdict(list)
    for index, row in enumerate(observations):
        if not row.task_id or not row.anchor_state or not row.action or not all(map(math.isfinite, (
            row.discounted_return, row.episode_advantage,
        ))):
            raise ValueError("steps require nonempty task/state/action and finite values")
        groups[(row.task_id, row.anchor_state)].append(index)
    credits: list[StepCredit | None] = [None] * len(observations)
    for indices in groups.values():
        returns = np.asarray([observations[i].discounted_return for i in indices], dtype=np.float64)
        action_groups: dict[str, list[float]] = defaultdict(list)
        for index in indices:
            item = observations[index]
            action_groups[item.action].append(item.discounted_return)
        total_variance = float(np.var(returns))
        estimable = (
            len(action_groups) >= 2
            and all(len(values) >= 2 for values in action_groups.values())
            and total_variance > 0
        )
        if estimable:
            within = sum(
                len(values) / len(indices) * float(np.var(values))
                for values in action_groups.values()
            )
            coefficient = min(1.0, max(0.0, 1 - within / total_variance))
        else:
            coefficient = 1.0
        scale = math.sqrt(total_variance) if normalize_local and total_variance > 0 else 1.0
        mean_return = float(np.mean(returns))
        for index in indices:
            row = observations[index]
            local = (row.discounted_return - mean_return) / scale
            credits[index] = StepCredit(
                coefficient=coefficient,
                local_advantage=local,
                combined_advantage=row.episode_advantage + coefficient * local,
                estimable=estimable,
            )
    return [credit for credit in credits if credit is not None]
