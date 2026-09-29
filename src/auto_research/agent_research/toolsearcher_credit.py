"""ToolSearcher event/selection credit for grouped tool-search rollouts.

This implements the paper's credit-assignment mechanism, not its Qwen policy
or StableToolBench/AppWorld training run. Retrieved tool documents must be
masked from the policy loss by callers.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class SearchTrace:
    """One rollout; each event contains tool IDs returned by that search."""

    events: tuple[frozenset[str], ...]
    selected: frozenset[str]


@dataclass(frozen=True)
class TraceCredit:
    search_advantages: tuple[float, ...]
    selection_advantage: float
    first_discoveries: tuple[frozenset[str], ...]


def _z_scores(values: tuple[float, ...]) -> tuple[float, ...]:
    mean = sum(values) / len(values)
    std = sqrt(sum((value - mean) ** 2 for value in values) / len(values))
    if std == 0:
        return (0.0,) * len(values)
    return tuple((value - mean) / std for value in values)


def trajectory_credit(
    traces: tuple[SearchTrace, ...], target_tools: frozenset[str],
) -> tuple[TraceCredit, ...]:
    """Compute Eq. 2, 5 and 7 without exposing target IDs to a policy.

    Target IDs are evaluator-private, entering only after rollout. A target
    found repeatedly within one trace receives credit only on its first
    discovery event. If a target is found by every trace, its search
    advantage is zero (mastered). Selection credit is zero unless the trace
    has searched *all* targets.
    """
    if len(traces) < 2 or not target_tools:
        raise ValueError("at least two traces and one target tool are required")
    if any(not trace.events for trace in traces):
        raise ValueError("every trace must contain at least one search event")
    discovered: list[tuple[frozenset[str], ...]] = []
    found: list[frozenset[str]] = []
    for trace in traces:
        seen: set[str] = set()
        first = []
        for event in trace.events:
            first.append(frozenset((event & target_tools) - seen))
            seen.update(event)
        discovered.append(tuple(first))
        found.append(frozenset(seen & target_tools))
    per_tool = {
        tool: _z_scores(tuple(float(tool in row) for row in found))
        for tool in target_tools
    }
    selection_rewards = tuple(
        float(trace.selected == target_tools) for trace in traces
    )
    selection_scores = _z_scores(selection_rewards)
    return tuple(
        TraceCredit(
            search_advantages=tuple(
                max((per_tool[tool][index] for tool in first), default=0.0)
                for first in discovered[index]
            ),
            selection_advantage=(
                selection_scores[index] if found[index] == target_tools else 0.0
            ),
            first_discoveries=discovered[index],
        )
        for index in range(len(traces))
    )
