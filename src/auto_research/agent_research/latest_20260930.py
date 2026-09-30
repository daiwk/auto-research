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


def time_evolving_memory(interactions, *, chunk_size: int, memory_budget: int, update):
    """ReMem Eq. (3): bounded, sequential memory updates over history chunks.

    ``update`` receives only the previous memory and current history chunk.  It
    cannot inspect the final recommendation label, preserving the inference
    boundary used by the paper.
    """
    if chunk_size < 1 or memory_budget < 1:
        raise ValueError("chunk_size and memory_budget must be positive")
    memory: tuple[str, ...] = ()
    trace = []
    for start in range(0, len(interactions), chunk_size):
        chunk = tuple(interactions[start:start + chunk_size])
        proposed = tuple(update(memory, chunk))
        memory = proposed[-memory_budget:]
        trace.append({"chunk_start": start, "chunk_size": len(chunk), "memory": memory})
    return memory, trace


def multi_memory_grpo_objective(
    final_ratio,
    memory_ratio,
    rewards,
    *,
    clip: float = 0.2,
    memory_weight: float = 1.0,
    epsilon: float = 1e-6,
):
    """ReMem Eqs. (11), (14)-(16): propagate final reward to every memory."""
    import torch

    if final_ratio.ndim != 2 or memory_ratio.ndim != 3:
        raise ValueError("final ratios are [group,tokens], memory ratios [group,memories,tokens]")
    if final_ratio.shape[0] != memory_ratio.shape[0] or rewards.shape != final_ratio.shape[:1]:
        raise ValueError("all tensors must share the rollout group dimension")
    advantage = (rewards - rewards.mean()) / rewards.std(unbiased=False).clamp_min(epsilon)

    def surrogate(ratio, expanded_advantage):
        unclipped = ratio * expanded_advantage
        clipped = ratio.clamp(1 - clip, 1 + clip) * expanded_advantage
        return torch.minimum(unclipped, clipped).mean()

    answer = surrogate(final_ratio, advantage[:, None])
    memory = surrogate(memory_ratio, advantage[:, None, None])
    return answer + memory_weight * memory, {
        "answer_objective": float(answer.detach()),
        "memory_objective": float(memory.detach()),
        "memory_count": memory_ratio.shape[1],
    }


def video_rsi_accept(
    incumbent_accuracy: float,
    incumbent_cost: float,
    candidate_accuracy: float,
    candidate_cost: float,
    *,
    maximum_cost_growth: float = 0.1,
    minimum_cost_reduction: float = 0.1,
    maximum_accuracy_loss: float = 0.01,
) -> tuple[bool, str]:
    """Video-RSI Eq. (3), the private-selection accuracy/cost admission gate."""
    delta = candidate_accuracy - incumbent_accuracy
    accuracy_gain = delta > 0 and candidate_cost <= (1 + maximum_cost_growth) * incumbent_cost
    cost_gain = (
        -maximum_accuracy_loss <= delta <= 0
        and incumbent_cost > 0
        and candidate_cost <= (1 - minimum_cost_reduction) * incumbent_cost
    )
    if accuracy_gain:
        return True, "accuracy_gain_with_bounded_cost"
    if cost_gain:
        return True, "cost_reduction_with_bounded_accuracy_loss"
    return False, "rejected_by_private_selection_gate"
