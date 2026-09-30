"""Gold-isolated kernels for Harness Learning and GraphHCA."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import math

import numpy as np


@dataclass(frozen=True)
class Transition:
    state: str
    action: str
    next_state: str


def graphhca_credit(
    rollouts: list[tuple[list[Transition], bool]],
    *,
    discount: float = 0.95,
    floor: float = 1e-2,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
):
    """GraphHCA discounted fixed point and same-state advantages.

    The estimator receives only sampled states, actions and terminal outcomes;
    it has no interface for gold answers or plans.
    """
    if not 0 < discount < 1 or not 0 < floor < 1:
        raise ValueError("discount and floor must lie in (0, 1)")
    edge_counts: Counter[tuple[str, str, str]] = Counter()
    state_counts: Counter[str] = Counter()
    goal_states: set[str] = set()
    failure_states: set[str] = set()
    ordered_edges: list[Transition] = []
    for transitions, success in rollouts:
        if not transitions:
            continue
        for transition in transitions:
            edge_counts[(transition.state, transition.action, transition.next_state)] += 1
            state_counts[transition.state] += 1
            ordered_edges.append(transition)
        (goal_states if success else failure_states).add(transitions[-1].next_state)
    states = set(state_counts) | {edge[2] for edge in edge_counts}
    values = {state: float(state in goal_states) for state in states}
    non_terminal = states - goal_states - failure_states
    for iteration in range(1, max_iterations + 1):
        updated = dict(values)
        for state in non_terminal:
            expectation = sum(
                count / max(1, state_counts[state]) * values[target]
                for (source, _action, target), count in edge_counts.items()
                if source == state
            )
            updated[state] = discount * expectation
        delta = max((abs(updated[state] - values[state]) for state in states), default=0.0)
        values = updated
        if delta <= tolerance:
            break
    else:  # pragma: no cover
        raise RuntimeError("GraphHCA fixed point did not converge")
    potentials = {state: math.log(max(value, floor)) for state, value in values.items()}
    credits = np.asarray(
        [potentials[edge.next_state] - potentials[edge.state] for edge in ordered_edges],
        dtype=np.float64,
    )
    grouped: dict[str, list[int]] = defaultdict(list)
    for index, edge in enumerate(ordered_edges):
        grouped[edge.state].append(index)
    advantages = np.zeros_like(credits)
    for indices in grouped.values():
        if len(indices) < 2:
            continue
        state_credit = credits[indices]
        if state_credit.std() > 0:
            advantages[indices] = (state_credit - state_credit.mean()) / state_credit.std()
    return {
        "values": values,
        "potentials": potentials,
        "credits": credits,
        "step_advantages": advantages,
        "iterations": iteration,
        "edge_count": len(edge_counts),
    }


class HarnessProposer:
    """Categorical revision policy trained only from execution outcomes."""

    def __init__(self, revisions=("retry", "validate", "interpreter", "retrieve")):
        self.revisions = tuple(revisions)
        self.logits = np.zeros(len(self.revisions), dtype=np.float64)

    def probabilities(self):
        shifted = self.logits - self.logits.max()
        weights = np.exp(shifted)
        return weights / weights.sum()

    def train_step(self, rewards, learning_rate: float = 0.1):
        """Group-relative REINFORCE update over executed harness revisions."""
        rewards = np.asarray(rewards, dtype=np.float64)
        if rewards.shape != self.logits.shape:
            raise ValueError("one execution reward is required for each revision")
        advantages = rewards - rewards.mean()
        probabilities = self.probabilities()
        gradient = advantages - probabilities * advantages.sum()
        self.logits += learning_rate * gradient
        return {
            "mean_reward": float(rewards.mean()),
            "best_revision": self.revisions[int(rewards.argmax())],
        }

    def propose(self, execution_report: dict[str, float | str]) -> str:
        """Choose an edit from public execution status, never hidden labels."""
        scores = self.logits.copy()
        failure = str(execution_report.get("failure", ""))
        boosts = {"invalid": "validate", "timeout": "interpreter", "missing_evidence": "retrieve"}
        if failure in boosts and boosts[failure] in self.revisions:
            scores[self.revisions.index(boosts[failure])] += 1.0
        return self.revisions[int(scores.argmax())]


def adapt_harness(
    proposer: HarnessProposer,
    seed_harness: tuple[str, ...],
    execute,
    rounds: int = 4,
):
    """Repeated frozen-policy test-time adaptation from execution reports."""
    harness = list(seed_harness)
    trace = []
    for round_index in range(rounds):
        report = dict(execute(tuple(harness)))
        revision = proposer.propose(report)
        if revision not in harness:
            harness.append(revision)
        trace.append({"round": round_index, "revision": revision, "report": report})
    return tuple(harness), trace
