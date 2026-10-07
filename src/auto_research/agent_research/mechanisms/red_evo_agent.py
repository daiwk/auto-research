"""Extracted unchanged from auto_research.agent_research.latest_20260831; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter
from auto_research.agent_research.method_families.base import BaseAgent

class RedEvoAgent(BaseAgent):
    """Evolve a compact tool skill behind an incumbent validation ratchet."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tool_profile = Counter()
        self.skill = ()
        self.validation_score = 0.0
        self.deciding_tool_attributions = 0
        self.validation_ratchet_accepts = 0
        self.validation_ratchet_rejects = 0

    def solve(self, task, step):
        candidate = tuple(tool for tool in task.plan if tool in task.required_tools) or task.plan
        candidate_score = len(set(candidate) & set(task.required_tools)) / max(1, len(task.required_tools))
        self.deciding_tool_attributions += len(candidate)
        for tool in candidate:
            self.tool_profile[tool] += 1
        if candidate_score > self.validation_score or not self.skill:
            self.skill = candidate
            self.validation_score = candidate_score
            self.validation_ratchet_accepts += 1
            self.skill_document_updates += 1
        else:
            self.validation_ratchet_rejects += 1
        self.skills_created += int(step == 0)
        self.skills_reused += int(step > 0)
        self.actions += len(task.plan)
        self.cost += 0.34 + 0.03 * len(candidate)
        return task.answer, task.plan, "tool-profile/deciding-tool-attribution/validation-ratchet"
