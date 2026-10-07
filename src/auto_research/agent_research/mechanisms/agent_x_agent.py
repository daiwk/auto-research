"""Extracted unchanged from auto_research.agent_research.latest_20260824; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

class AgentXAgent(BaseAgent):
    """Close the idea, implementation, evaluation and harness-evolution loop.

    The deterministic suite represents production artifacts as keyed plans.  A
    first encounter pays for bounded proposal exploration, repository-grounded
    implementation and two verifier stages; later encounters reuse both
    positive and negative experiment assets and therefore cost less.
    """

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.experiment_kb: dict[str, tuple[str, ...]] = {}

    @staticmethod
    def _key(task):
        return f"{task.axis}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        self.actions += len(task.plan)
        if key not in self.experiment_kb:
            # Brainstorm -> develop -> local verification -> guarded global
            # evaluation -> assetization -> semantic-gradient harness update.
            self.plan_explorations += 3
            self.references_collected += 4
            self.worker_calls += 1
            self.local_verifier_calls += 2
            self.global_verifier_calls += 1
            self.archival_writes += 1
            self.memory_bank_updates += 1
            self.skill_document_updates += 1
            self.policy_updates += 1
            self.experiment_kb[key] = task.plan
            self.skills_created += 1
            self.cost += 1.55
            return task.answer, task.plan, "brainstorm/develop/guardrail-ab/assetize/sgpo"

        plan = self.experiment_kb[key]
        self.memories_retrieved += 1
        self.skills_reused += 1
        self.cross_task_skill_reuses += 1
        self.local_verifier_calls += 1
        self.global_verifier_calls += 1
        self.policy_updates += 1
        self.cost += 0.48
        return task.answer, plan, "experiment-kb/replay/guardrail-ab"
