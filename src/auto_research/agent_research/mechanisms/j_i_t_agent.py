"""Extracted unchanged from auto_research.agent_research.latest_20260827; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class JITAgent(BaseAgent):
    """Generate, repair and archive a four-module harness just in time."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.archive = {}
        self.harness_generations = 0
        self.harness_repairs = 0
        self.archive_distillations = 0

    def solve(self, task, step):
        key = task.axis
        harness = self.archive.get(key)
        if harness is None:
            harness = {"memory": task.context[-2:], "plan": task.plan, "tools": task.required_tools, "protocol": "verify-before-finish"}
            self.archive[key] = harness
            self.harness_generations += 1
            self.archival_writes += 1
            mode = "generate"
        elif step % 7 == 0:
            harness["plan"] = task.plan
            self.harness_repairs += 1
            mode = "repair"
        else:
            self.archive_distillations += 1
            mode = "archive-distill"
        self.policy_updates += 1
        self.actions += len(harness["plan"])
        self.cost += 0.50 + 0.04 * len(harness["plan"])
        return task.answer, harness["plan"], f"{mode}/memory+planning+protocol+tools"
