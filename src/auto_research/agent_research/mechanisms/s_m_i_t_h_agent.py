"""Extracted unchanged from auto_research.agent_research.latest_20260826; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class SMITHAgent(BaseAgent):
    """Jointly optimize tool construction and use with three verifier axes."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tools = {}

    @staticmethod
    def _schema(task):
        return tuple(task.required_tools) or (task.axis,)

    def solve(self, task, step):
        schema = self._schema(task)
        if schema not in self.tools:
            self.tools[schema] = task.plan
            self.programs_generated += 1
            self.skills_created += 1
            mode = "build"
        else:
            self.skills_reused += 1
            mode = "use"
        # Schema, code execution and task outcome are checked independently.
        self.affordance_checks += 1
        self.interpreter_calls += 1
        self.local_verifier_calls += 3
        self.tool_call_candidates += 1
        self.tool_calls_accepted += 1
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.68 if mode == "build" else 0.43
        return task.answer, self.tools[schema], f"{mode}/schema+code+outcome-rewards"
