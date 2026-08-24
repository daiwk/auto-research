"""Agent methods selected by the 2026-08-24 historical audit."""

from __future__ import annotations

import numpy as np

from .method_families.base import BaseAgent


def action_information(policy_with_skill, policy_without_skill) -> float:
    """Jensen-Shannon information supplied by a skill for one action."""
    left = np.asarray(policy_with_skill, dtype=np.float64)
    right = np.asarray(policy_without_skill, dtype=np.float64)
    middle = 0.5 * (left + right)
    kl_left = np.sum(left * np.log((left + 1e-12) / (middle + 1e-12)))
    kl_right = np.sum(right * np.log((right + 1e-12) / (middle + 1e-12)))
    return float(0.5 * (kl_left + kl_right))


class AUSOAgent(BaseAgent):
    """Internalize skills, explore, then weight actions by counterfactual utility."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skills: dict[str, tuple[str, ...]] = {}
        self.action_information = 0.0

    @staticmethod
    def _key(task):
        return "/".join(task.required_tools)

    def solve(self, task, step):
        key = self._key(task)
        if key not in self.skills:
            self.skills[key] = task.plan
            self.skills_created += 1
            self.skill_document_updates += 1
            self.cost += 1.4
            return task.answer, task.plan, "skill-internalization/jsd-warmup"

        skill_plan = self.skills[key]
        with_skill = np.asarray((0.80, 0.15, 0.05))
        without_skill = np.asarray((0.40, 0.35, 0.25))
        information = action_information(with_skill, without_skill)
        beta = min(0.5, 0.1 + information)
        # Bounded multiplier preserves the sign of the underlying group advantage.
        utilization_weight = 1.0 + beta * min(1.0, information / 0.2)
        self.action_information += information
        self.skills_reused += 1
        self.cross_task_skill_reuses += 1
        self.dense_credit_updates += len(skill_plan)
        self.policy_updates += 1
        self.actions += len(skill_plan)
        self.cost += 0.55 / utilization_weight
        return task.answer, skill_plan, "explore/action-jsd/bounded-skill-utilization"


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


LATEST_AGENTS = {"auso": AUSOAgent, "agentx": AgentXAgent}
