"""Extracted unchanged from auto_research.agent_research.latest_20260914; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter, defaultdict
import math
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class COBRASkillsAgent(ObservationAgent):
    """Contextual-UCB allocation over an evolving, evidence-grounded skill set."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skill_trials = Counter()
        self.skill_rewards = Counter()
        self.skill_plans: dict[str, tuple[str, ...]] = {}
        self.pending_skill = ""
        self.bandit_allocations = self.skill_evolutions = 0

    def _key(self, intent):
        tokens = sorted(_tokens(intent))
        return tokens[0] if tokens else "default"

    def solve_observation(self, observation, step):
        answer, observed = read_evidence(observation)
        context = _tokens(observation.intent)
        candidates = list(self.skill_plans)
        if candidates:
            total = 1 + sum(self.skill_trials.values())
            scored = []
            for key in candidates:
                overlap = int(key in context)
                mean = self.skill_rewards[key] / max(1, self.skill_trials[key])
                bonus = math.sqrt(math.log(total + 1) / (1 + self.skill_trials[key]))
                scored.append((overlap + mean + bonus, key))
            _, selected = max(scored)
            self.pending_skill = selected
            self.bandit_allocations += 1
            plan = observed or self.skill_plans[selected]
        else:
            self.pending_skill = self._key(observation.intent)
            plan = observed
        if observed and self.skill_plans.get(self.pending_skill) != observed:
            self.skill_plans[self.pending_skill] = observed
            self.skill_evolutions += 1
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "contextual-ucb/evidence-grounded-skill-evolution"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        if self.pending_skill:
            self.skill_trials[self.pending_skill] += 1
            self.skill_rewards[self.pending_skill] += int(answer_ok and plan_ok)
