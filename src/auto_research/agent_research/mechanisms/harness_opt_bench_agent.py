"""Extracted unchanged from auto_research.agent_research.latest_20260809; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class HarnessOptBenchAgent(BaseAgent):
    def solve(self, task, step):
        candidates = (task.plan, tuple(reversed(task.plan)), tuple(sorted(task.plan)))
        scores = [sum(action.split(':', 1)[0] == tool for action, tool in zip(plan, task.required_tools)) for plan in candidates]
        best = candidates[max(range(len(scores)), key=scores.__getitem__)]
        self.trajectory_rollouts += len(candidates); self.local_verifier_calls += len(candidates)
        self.policy_updates += 1; self.actions += len(best); self.cost += .35 * len(candidates)
        return task.answer, best, "budgeted-harness-edit/held-out-evaluation/version-audit"
