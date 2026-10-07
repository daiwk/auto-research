"""Extracted unchanged from auto_research.agent_research.latest_20260916; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter
import math
import numpy as np
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class HarnessBanditAgent(ObservationAgent):
    """Online harness scheduler combining learnability and transferability."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.harness_trials = Counter()
        self.harness_rewards = Counter()
        self.harness_vectors: dict[str, np.ndarray] = {}
        self.pending = ""
        self.harness_allocations = self.gradient_sketch_updates = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        harnesses = ("direct", "planner", "tool", "reflect")
        tokens = sorted(_tokens(observation.intent))
        sketch = np.asarray([len(tokens), len(observation.context), len(plan), 1.0])
        scores = []
        for harness in harnesses:
            trials = self.harness_trials[harness]
            learnability = abs(self.harness_rewards[harness] / max(1, trials) - 0.5)
            prior = self.harness_vectors.get(harness)
            transfer = 0.0 if prior is None else float(np.dot(sketch, prior) / ((np.linalg.norm(sketch) * np.linalg.norm(prior)) + 1e-12))
            visit_bonus = math.sqrt(math.log(step + 2) / (trials + 1))
            scores.append((learnability + max(0.0, transfer) + 0.2 * visit_bonus, harness))
        self.pending = max(scores)[1]
        self.harness_vectors[self.pending] = sketch
        self.harness_allocations += 1
        self.gradient_sketch_updates += 1
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, f"harness-bandit/{self.pending}"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.harness_trials[self.pending] += 1
        self.harness_rewards[self.pending] += int(answer_ok and plan_ok)
