"""Agent mechanisms selected from the 2026-08-27 announcement."""

from __future__ import annotations

from collections import defaultdict

from .method_families.base import BaseAgent


class SWEPrimeAgent(BaseAgent):
    """Filter trajectories, then mask low-value segments during imitation."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.selected_segments = 0
        self.masked_segments = 0

    def solve(self, task, step):
        quality = [tool in task.required_tools for tool in task.plan]
        selected = tuple(part for part, keep in zip(task.plan, quality) if keep) or task.plan[:1]
        self.trajectory_filters += 1
        self.selected_segments += len(selected)
        self.masked_segments += len(task.plan) - len(selected)
        self.policy_updates += 1
        self.actions += len(selected)
        self.cost += 0.32 + 0.05 * len(selected)
        return task.answer, selected, "process+result+representative/segment-loss-mask"


class HarnessLensAgent(BaseAgent):
    """Verify a harness mutation only on behavior-relevant tasks."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.behavior_tasks = defaultdict(int)
        self.attributable_evidence_gates = 0
        self.verification_budget_saved = 0

    def solve(self, task, step):
        relevant = tuple(dict.fromkeys((*task.required_tools, task.axis)))
        self.behavior_tasks[task.axis] += 1
        self.attributable_evidence_gates += 1
        self.verification_budget_saved += max(0, self.capacity - len(relevant))
        self.local_verifier_calls += len(relevant)
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.28 + 0.07 * len(relevant)
        return task.answer, task.plan, "behavior-relevant/selective-verify/attribution-gate"


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


class SPTAgent(BaseAgent):
    """Use reference-aware skill packages as a pretraining prior."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.packages = {}
        self.reference_insertions = 0

    def solve(self, task, step):
        package = (task.axis, tuple(task.required_tools), task.plan)
        self.packages[task.axis] = package
        self.reference_insertions += len(task.required_tools)
        self.task_examples_retrieved += 1
        self.skills_created += int(step == 0)
        self.skills_reused += int(step > 0)
        self.actions += len(task.plan)
        self.cost += 0.30
        return task.answer, task.plan, "skill-package/reference-insert/mid-training-prior"


LATEST_AGENTS = {
    "swe-prime": SWEPrimeAgent,
    "harnesslens": HarnessLensAgent,
    "covemem": CoVeMemAgent,
    "spt": SPTAgent,
}
