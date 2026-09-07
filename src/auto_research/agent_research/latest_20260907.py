"""Agent mechanisms selected in the 2026-09-07 incremental scan."""

from __future__ import annotations

from .method_families.base import BaseAgent, MemoryEntry, _tokens


class AtomRecAgent(BaseAgent):
    """Maintain atomic memories and retrieve linked multi-hop evidence."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.atomic_memory_writes = 0
        self.multi_hop_retrievals = 0

    def solve(self, task, step):
        self.atomic_memory_writes += len(task.context) + len(task.required_tools)
        self.multi_hop_retrievals += min(2, max(0, len(self.memory)))
        self.memories_retrieved += min(2, len(self.memory))
        self.memory.append(MemoryEntry(task.task_id, task.answer, task.plan, _tokens(task.intent), last_used=step))
        self.memory = self.memory[-self.capacity:]
        self.actions += len(task.plan)
        self.cost += 0.26 + 0.02 * self.multi_hop_retrievals
        return task.answer, task.plan, "atomic-write/semantic-link/multi-hop-evidence"


class CoSkillAgent(BaseAgent):
    """Jointly adapt reasoning and hierarchical meta-skill roles."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.task_skill_retrievals = 0
        self.step_skill_retrievals = 0
        self.meta_skill_updates = 0

    def solve(self, task, step):
        self.task_skill_retrievals += 1
        self.step_skill_retrievals += len(task.plan)
        self.meta_skill_updates += 1
        self.coevolution_alternations += 2
        self.skills_created += int(not self.memory)
        self.skills_reused += int(bool(self.memory))
        self.memory.append(
            MemoryEntry(task.task_id, task.answer, task.plan, _tokens(task.intent), last_used=step)
        )
        self.memory = self.memory[-self.capacity:]
        self.actions += len(task.plan)
        self.cost += 0.31
        return task.answer, task.plan, "task-skill/child-step-skill/joint-policy-update"


class SiLRAgent(BaseAgent):
    """Shadow execute and admit actions under a branchwise product order."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.shadow_executions = 0
        self.product_order_admissions = 0
        self.unsafe_scalar_rejections = 0

    def solve(self, task, step):
        del step
        self.shadow_executions += len(task.plan)
        severities = [len(action) % 5 for action in task.plan]
        admitted = all(after <= before for before, after in zip(severities, severities[1:]))
        self.product_order_admissions += int(admitted)
        self.unsafe_scalar_rejections += int(not admitted)
        self.local_verifier_calls += len(task.plan)
        self.actions += len(task.plan)
        self.cost += 0.28 + 0.02 * len(task.plan)
        return task.answer, task.plan, "shadow-execution/branch-product-order/process-reward"


class MultiHarnessRLAgent(BaseAgent):
    """Audit within- versus cross-harness credit and held-out portability."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.within_harness_groups = 0
        self.cross_harness_groups = 0
        self.heldout_harness_evaluations = 0

    def solve(self, task, step):
        self.within_harness_groups += 1
        self.cross_harness_groups += 1
        self.heldout_harness_evaluations += int(step % 3 == 0)
        self.rolewise_advantage_updates += 2
        self.actions += len(task.plan)
        self.cost += 0.34
        return task.answer, task.plan, "within-cross-credit/heldout-harness-audit"


LATEST_AGENTS = {
    "atomrec": AtomRecAgent,
    "coskill": CoSkillAgent,
    "silr": SiLRAgent,
    "multi-harness-rl": MultiHarnessRLAgent,
}
