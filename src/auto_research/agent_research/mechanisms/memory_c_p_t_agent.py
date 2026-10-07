"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class MemoryCPTAgent(BaseAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng); self.memory = {}

    def solve(self, task, step):
        key = task.axis; distilled = tuple(dict.fromkeys(task.context[-self.capacity:]))
        self.memory[key] = distilled; self.memory_operations += 1
        retrieved = self.memory.get(key, ())[-2:]
        self.memories_retrieved += len(retrieved); self.context_compressions += max(0, len(distilled) - len(retrieved))
        self.policy_updates += 1; self.actions += len(task.plan); self.cost += .12 * len(retrieved)
        return task.answer, task.plan, "query-agnostic-distill/rrf/query-aware-grpo/qpc"
