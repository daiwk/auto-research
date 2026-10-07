"""Extracted unchanged from auto_research.agent_research.latest_20260930; stable mechanism boundary."""
from __future__ import annotations

import numpy as np

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
