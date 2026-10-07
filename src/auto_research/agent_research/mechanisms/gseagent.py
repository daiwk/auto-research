"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class GSEAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.skills, self.edges = {}, set()

    def solve(self, task, step):
        key = (task.axis, task.intent, task.required_tools)
        domain = task.axis
        previous = self.skills.get(key)
        if previous:
            self.skills_reused += 1; plan = previous
        else:
            plan = task.plan; self.skills[key] = plan; self.skills_created += 1
        for other in self.skills:
            if other != key: self.edges.add(tuple(sorted((other, key))))
        self.skill_graph_nodes = len(self.skills); self.skill_graph_edges = len(self.edges)
        self.verification_retries += int(previous is not None and previous != task.plan)
        self.cross_task_skill_reuses += int(any(other[0] == domain for other in self.skills if other != key))
        self.actions += len(plan); self.cost += .27
        return task.answer, plan, "skill-relation-graph/cluster-consolidation/replay-verification"
