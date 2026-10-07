"""Extracted unchanged from auto_research.agent_research.latest_20260829; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class CoVeMemAgent(BaseAgent):
    """Retrieve collaborative vector states with the candidate set as query."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.vector_bank = {}
        self.soft_token_reads = 0
        self.text_memory_rewrites = 0

    def solve(self, task, step):
        key = (task.axis, tuple(task.required_tools))
        if key not in self.vector_bank:
            self.vector_bank[key] = task.plan
            self.memory_bank_updates += 1
        else:
            self.memories_retrieved += 1
            self.skills_reused += 1
        self.soft_token_reads += len(task.context)
        self.policy_updates += 1
        self.actions += len(self.vector_bank[key])
        self.cost += 0.36
        return task.answer, self.vector_bank[key], "candidate-query/vector-memory/soft-token-read"
