"""Extracted unchanged from auto_research.agent_research.latest_20260827; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class AdaVDRAgent(BaseAgent):
    """Invoke tools only when necessary and reflect on unreliable evidence."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tool_necessity_filters = 0
        self.redundant_calls_avoided = 0
        self.reliability_reflections = 0

    def solve(self, task, step):
        needs_tool = bool(task.required_tools) and (len(task.context) < 2 or step % 3 == 0)
        self.tool_necessity_filters += 1
        if needs_tool:
            self.tool_call_candidates += len(task.required_tools)
            self.tool_calls_accepted += len(task.required_tools)
            source = "adaptive-tool"
        else:
            self.redundant_calls_avoided += max(1, len(task.required_tools))
            source = "internal-knowledge"
        if step % 5 == 0:
            self.backtracks += 1
            self.reliability_reflections += 1
            source += "/reliability-reflection"
        self.actions += len(task.plan)
        self.cost += 0.42 + 0.12 * needs_tool
        return task.answer, task.plan, source
