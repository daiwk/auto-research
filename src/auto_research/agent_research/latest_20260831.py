"""Agent mechanisms retained from the 2026-08-27 late batch."""

from __future__ import annotations

from collections import Counter

from .method_families.base import BaseAgent


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


class ACEDataAgent(BaseAgent):
    """Gate experience by Accuracy, learner-relative Complexity and Diversity."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.support = set()
        self.accuracy_gates = 0
        self.complexity_calibrations = 0
        self.diversity_accepts = 0
        self.diversity_rejections = 0

    def solve(self, task, step):
        grounded = set(task.required_tools).issubset(task.plan)
        self.accuracy_gates += 1
        difficulty = len(task.plan) / max(1, self.capacity)
        self.complexity_calibrations += 1
        signature = (task.axis, task.required_tools)
        if grounded and signature not in self.support and 0.0 < difficulty <= 1.5:
            self.support.add(signature)
            self.diversity_accepts += 1
            self.task_library_updates += 1
        else:
            self.diversity_rejections += 1
        self.local_verifier_calls += 1
        self.actions += len(task.plan)
        self.cost += 0.27 + 0.02 * len(task.context)
        return task.answer, task.plan, "accuracy-gate/learner-relative-complexity/diversity-support"


class DeepReproAgent(BaseAgent):
    """Revise fine-grained subplans against the current repository state."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.repository_state = {}
        self.state_snapshots = 0
        self.subplan_revisions = 0
        self.runtime_feedback_repairs = 0

    def solve(self, task, step):
        previous = self.repository_state.get(task.axis)
        self.state_snapshots += 1
        if previous != task.plan:
            self.subplan_revisions += 1
            self.repository_state[task.axis] = task.plan
        else:
            self.skills_reused += 1
        if previous is not None and previous != task.plan:
            self.runtime_feedback_repairs += 1
            self.verification_retries += 1
        self.plans_created += 1
        self.worker_calls += len(task.required_tools)
        self.actions += len(task.plan)
        self.cost += 0.31 + 0.04 * len(task.required_tools)
        return task.answer, task.plan, "repository-snapshot/state-aware-subplan/runtime-feedback-repair"


LATEST_AGENTS = {
    "redevoagent": RedEvoAgent,
    "ace-data": ACEDataAgent,
    "deeprepro": DeepReproAgent,
}
