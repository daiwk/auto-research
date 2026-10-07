"""Extracted unchanged from auto_research.agent_research.latest_20260916_followup; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class InteractiveMemoryAgent(ObservationAgent):
    """Planner/Trigger co-evolution using delayed observed success only."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.memory: dict[str, tuple[str, ...]] = {}
        self.value = Counter()
        self.pending_key = ""
        self.pending_plan: tuple[str, ...] = ()
        self.planner_updates = self.trigger_updates = self.delayed_rewards = 0

    def solve_observation(self, observation, step):
        answer, observed_plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        stored = self.memory.get(key, ())
        trigger = bool(stored) and self.value[key] >= 0
        plan = stored if trigger else observed_plan
        self.pending_key, self.pending_plan = key, tuple(observed_plan)
        self.trigger_updates += int(trigger)
        self.actions += len(plan)
        self.cost += len(observation.context) + int(trigger)
        return answer, plan, f"planner-trigger/{'retrieve' if trigger else 'observe'}"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        reward = 1 if answer_ok and plan_ok else -1
        self.value[self.pending_key] += reward
        self.delayed_rewards += 1
        if reward > 0 and self.pending_plan:
            if len(self.memory) >= self.capacity and self.pending_key not in self.memory:
                victim = min(self.memory, key=lambda key: self.value[key])
                self.memory.pop(victim)
            self.memory[self.pending_key] = self.pending_plan
            self.planner_updates += 1
