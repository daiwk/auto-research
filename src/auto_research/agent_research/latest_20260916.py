"""Observation-safe mechanisms from the Sep-16 Agent research batch."""

from __future__ import annotations

from collections import Counter
import math

import numpy as np

from .latest_20260907 import ObservationAgent, read_evidence
from .method_families.base import _tokens


class FuseEvaluatorAgent(ObservationAgent):
    """Verifiable simulation audit without access to hidden benchmark gold."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.simulated_dialogues = self.framing_checks = self.verifiable_motives = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        frames = [set(_tokens(fact)) for fact in observation.context]
        self.simulated_dialogues += 1
        self.framing_checks += sum(bool(left ^ right) for left, right in zip(frames, frames[1:]))
        self.verifiable_motives += int(bool(answer))
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "multi-agent-simulation/user-mediation/verifiable-hidden-motive"


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


class ScienceBuddyAgent(ObservationAgent):
    """Inner harness refinement followed by an outer policy-memory update."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.harness_memory: dict[str, tuple[str, ...]] = {}
        self.pending_key = ""
        self.inner_harness_updates = self.outer_policy_updates = self.cross_branch_lessons = 0

    def solve_observation(self, observation, step):
        answer, observed = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        prior = self.harness_memory.get(key, ())
        if observed and observed != prior:
            self.harness_memory[key] = observed
            self.inner_harness_updates += 1
        elif prior:
            self.cross_branch_lessons += 1
        self.pending_key = key
        plan = observed or prior
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "inner-harness-evolution/outer-policy-learning"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.outer_policy_updates += int(answer_ok and plan_ok and bool(self.pending_key))


LATEST_AGENTS = {
    "fuse-evaluator": FuseEvaluatorAgent,
    "harness-bandit": HarnessBanditAgent,
    "sciencebuddy": ScienceBuddyAgent,
}
