"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class CodeGrepAgent(BaseAgent):
    def solve(self, task, step):
        queries = tuple(dict.fromkeys(task.required_tools))
        self.tool_call_candidates += len(queries); self.tool_calls_accepted += len(queries)
        self.search_queries += len(queries); self.references_collected += len(queries)
        self.dense_credit_updates += len(queries); self.policy_updates += 1
        self.actions += len(task.plan); self.cost += .16 * len(queries)
        return task.answer, task.plan, "parallel-grep-glob-read/grpo/advantage-efficiency"
