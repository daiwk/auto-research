"""GRAFT trajectory-graph credit assignment (arXiv:2609.28963, Eqs. 5-10).

This is an exact-state, outcome-only reference implementation. It does not
train a language-model policy or claim the paper's benchmark scores.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Step:
    state: str
    action: str
    next_state: str


@dataclass(frozen=True)
class Trajectory:
    steps: tuple[Step, ...]
    outcome: float


@dataclass(frozen=True)
class Credit:
    values: dict[str, float]
    td: tuple[tuple[float, ...], ...]
    graph_gae: tuple[tuple[float, ...], ...]


def trajectory_credit(
    trajectories: tuple[Trajectory, ...], *, gamma: float = 0.99,
    gae_lambda: float = 0.95, tolerance: float = 1e-10,
    max_sweeps: int = 10000,
) -> Credit:
    """Merge exact states, Bellman-backup values, then score raw edges.

    Graph GAE averages *raw edge instances* at every downstream hop, not
    unique successor nodes. A terminal state cannot also be nonterminal:
    merging those would make its boundary value ambiguous.
    """
    if not trajectories or not 0 < gamma < 1 or not 0 <= gae_lambda <= 1:
        raise ValueError("nonempty trajectories, gamma in (0,1), lambda in [0,1] required")
    if tolerance <= 0 or max_sweeps < 1:
        raise ValueError("invalid convergence settings")
    edges: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)
    raw_out: dict[str, list[Step]] = defaultdict(list)
    sink_rewards: dict[str, float] = {}
    nodes: set[str] = set()
    for path in trajectories:
        if not path.steps or not math.isfinite(path.outcome):
            raise ValueError("each trajectory needs steps and a finite outcome")
        for previous, current in zip(path.steps, path.steps[1:]):
            if previous.next_state != current.state:
                raise ValueError("disconnected trajectory")
        for step in path.steps:
            nodes.update((step.state, step.next_state))
            edges[step.state][(step.action, step.next_state)] += 1
            raw_out[step.state].append(step)
        terminal = path.steps[-1].next_state
        if terminal in sink_rewards and sink_rewards[terminal] != path.outcome:
            raise ValueError("a merged terminal state has conflicting outcomes")
        sink_rewards[terminal] = path.outcome
    if set(sink_rewards) & set(edges):
        raise ValueError("terminal state also has outgoing actions")

    # Reverse BFS provides the paper's near-sink-first Gauss-Seidel order.
    reverse: dict[str, set[str]] = defaultdict(set)
    for source, grouped in edges.items():
        for _, target in grouped:
            reverse[target].add(source)
    distance = {node: 0 for node in sink_rewards}
    queue = deque(sink_rewards)
    while queue:
        target = queue.popleft()
        for source in reverse[target]:
            if source not in distance:
                distance[source] = distance[target] + 1
                queue.append(source)
    values = {node: sink_rewards.get(node, 0.0) for node in nodes}
    order = sorted(edges, key=lambda node: (distance.get(node, math.inf), node))
    for _ in range(max_sweeps):
        delta = 0.0
        for source in order:
            grouped = edges[source]
            total = sum(grouped.values())
            updated = gamma * sum(count * values[target] for (_, target), count in grouped.items()) / total
            delta = max(delta, abs(updated - values[source]))
            values[source] = updated
        if delta < tolerance:
            break
    else:
        raise RuntimeError("Bellman iteration did not converge")

    td = tuple(tuple(gamma * values[step.next_state] - values[step.state]
                     for step in path.steps) for path in trajectories)
    graph_gae: list[tuple[float, ...]] = []
    for path, path_td in zip(trajectories, td):
        estimates = []
        for offset, step in enumerate(path.steps):
            score = path_td[offset]
            frontier = {step.next_state}
            # Count each reachable raw edge instance once per hop, including
            # repeated sampled edges, but do not multiply it by path count.
            for hop in range(1, len(path.steps) - offset):
                descendants = [edge for state in frontier for edge in raw_out.get(state, ())]
                if not descendants:
                    break
                mean_td = sum(gamma * values[edge.next_state] - values[edge.state]
                              for edge in descendants) / len(descendants)
                score += (gamma * gae_lambda) ** hop * mean_td
                frontier = {edge.next_state for edge in descendants}
            estimates.append(score)
        graph_gae.append(tuple(estimates))
    return Credit(values, td, tuple(graph_gae))
