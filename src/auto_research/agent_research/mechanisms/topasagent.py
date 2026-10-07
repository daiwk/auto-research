"""Extracted unchanged from auto_research.agent_research.latest_20260827; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class TOPASAgent(BaseAgent):
    """Jointly score workflow critical path and prefix reuse under a budget."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.prefix_cache = set()
        self.prefix_hits = 0
        self.critical_path_updates = 0
        self.aging_promotions = 0

    def solve(self, task, step):
        prefix = (task.axis, tuple(task.required_tools))
        hit = prefix in self.prefix_cache
        self.prefix_hits += int(hit)
        self.critical_path_updates += 1
        if len(self.prefix_cache) >= self.capacity:
            self.prefix_cache.pop()
            self.tool_evictions += 1
        self.prefix_cache.add(prefix)
        if step and step % 9 == 0:
            self.aging_promotions += 1
        self.actions += len(task.plan)
        self.cost += 0.34 if hit else 0.61
        return task.answer, task.plan, f"critical-path/prefix-{'hit' if hit else 'load'}/aging"
