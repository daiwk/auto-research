"""Observation-safe reference agents for the 2026-09-19 paper batch."""

from __future__ import annotations

from collections import Counter

from .latest_20260907 import ObservationAgent, read_evidence
from .method_families.base import _tokens


class EvoSkillGUIAgent(ObservationAgent):
    """Reflect-revise-reuse a bounded skill package from observed outcomes."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skills = {}
        self.pending = None
        self.skill_revisions = self.skill_reuses = self.critic_reviews = 0

    def solve_observation(self, observation, step):
        del step
        answer, observed_plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent))[:2]) or "default"
        plan = self.skills.get(key, tuple(observed_plan))
        self.skill_reuses += int(key in self.skills)
        self.pending = (key, tuple(observed_plan))
        self.actions += len(plan); self.cost += len(observation.context)
        return answer, plan, "reflect/revise/reuse"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.critic_reviews += 1
        if answer_ok and plan_ok and self.pending:
            key, plan = self.pending
            if len(self.skills) >= self.capacity and key not in self.skills:
                self.skills.pop(next(iter(self.skills)))
            self.skills[key] = plan; self.skill_revisions += 1


class DependencyRefinementAgent(ObservationAgent):
    """Prune and merge observable plan rounds with a dependency DAG."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.dependency_edges = self.leaf_prunes = self.strict_merges = self.relaxed_merges = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        refined = []
        seen = set()
        for action in plan:
            tokens = _tokens(action)
            self.dependency_edges += int(bool(refined))
            if not tokens:
                self.leaf_prunes += 1; continue
            if tokens <= seen:
                self.strict_merges += 1; continue
            if refined and len(tokens & seen) >= max(1, len(tokens) // 2):
                refined[-1] = f"{refined[-1]}；{action}"; self.relaxed_merges += 1
            else:
                refined.append(action)
            seen |= tokens
        self.actions += len(refined); self.cost += len(observation.context)
        return answer, tuple(refined) or tuple(plan), "dependency-dag-refinement"


class HarnessDesignStudyAgent(ObservationAgent):
    """Ablate planning, action granularity and context compression explicitly."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.rule_elisions = self.context_summaries = self.action_granularity_choices = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        context = tuple(dict.fromkeys(observation.context))[-self.capacity:]
        self.rule_elisions += max(0, len(observation.context) - len(context))
        self.context_summaries += int(len(observation.context) > self.capacity)
        self.action_granularity_choices += 1
        chosen = tuple(plan[: max(1, min(len(plan), 1 + step % 3))])
        self.actions += len(chosen); self.cost += len(context)
        return answer, chosen, "fixed-loop/harness-ablation"


class CERAMoAAgent(ObservationAgent):
    """Route by observable familiarity and update only the selected specialist."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.specialists = Counter(); self.pending = "default"
        self.familiarity_routes = self.targeted_allocations = self.router_updates = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        axes = sorted(_tokens(observation.intent))[:3] or ["default"]
        self.pending = max(axes, key=lambda key: self.specialists[key])
        self.familiarity_routes += 1
        self.actions += len(plan); self.cost += len(observation.context)
        return answer, plan, f"familiarity-route/{self.pending}"

    def observe(self, task, answer_ok, plan_ok, step):
        del task, step
        self.specialists[self.pending] += 1 if answer_ok and plan_ok else -1
        self.targeted_allocations += 1; self.router_updates += 1


LATEST_AGENTS = {
    "evoskill-gui": EvoSkillGUIAgent,
    "dependency-refinement": DependencyRefinementAgent,
    "harness-design-study": HarnessDesignStudyAgent,
    "cera-moa": CERAMoAAgent,
}
