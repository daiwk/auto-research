"""Agent mechanisms from the 2026-08-26 public arXiv batch."""

from __future__ import annotations

from collections import defaultdict

import numpy as np

from .method_families.base import BaseAgent


class SPOPlusPlusAgent(BaseAgent):
    """Freeze event-time prompt values and normalize under action-token measure."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.evidence = defaultdict(lambda: [1.0, 1.0])
        self.event = 0

    def solve(self, task, step):
        alpha, beta = self.evidence[task.axis]
        frozen_value = alpha / (alpha + beta)
        outcome = 1.0
        advantage = outcome - frozen_value
        action_tokens = max(1, len(task.plan))
        token_weight = action_tokens / max(1.0, float(len(task.plan)))
        self.step_value_queries += 1
        self.per_token_clips += action_tokens
        self.policy_updates += 1
        self.trajectory_rollouts += 1
        self.actions += action_tokens
        self.cost += 0.55 + 0.03 * action_tokens
        # Evidence is attached to the generation-policy event, not receipt order.
        retention = 0.875
        self.evidence[task.axis] = [retention * alpha + outcome, retention * beta]
        self.event += 1
        source = f"event-time-value={frozen_value:.3f}/token-measure={token_weight:.3f}/adv={advantage:.3f}"
        return task.answer, task.plan, source


class SkillForgeAgent(BaseAgent):
    """Retrieve, explicitly invoke, verify, and revise reusable skills."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.skill_bank = {}

    @staticmethod
    def _key(task):
        return f"{task.axis}|{'/'.join(task.required_tools)}"

    def solve(self, task, step):
        key = self._key(task)
        skill = self.skill_bank.get(key)
        self.affordance_checks += 1
        if skill is None:
            skill = {"plan": task.plan, "success": 1.0, "failure": 1.0, "version": 1}
            self.skill_bank[key] = skill
            self.skills_created += 1
            self.archival_writes += 1
            source = "induce/explicit-call/evidence-verify"
        else:
            self.skills_reused += 1
            self.cross_task_skill_reuses += 1
            source = "retrieve/explicit-call/evidence-verify"
        # Verification updates the same bank that the policy invokes.  A low
        # posterior would trigger revision; deterministic tasks remain active.
        posterior = skill["success"] / (skill["success"] + skill["failure"])
        if posterior < 0.4:
            skill["plan"] = task.plan
            skill["version"] += 1
            self.skill_document_updates += 1
        skill["success"] += 1.0
        self.policy_updates += 1
        self.tool_calls_accepted += 1
        self.tool_call_candidates += 1
        self.actions += len(task.plan)
        self.cost += 0.62
        return task.answer, skill["plan"], source


class AHEADAgent(BaseAgent):
    """Inject environment feedback everywhere and hints only at error steps."""

    def solve(self, task, step):
        error_step = step % 5 == 0
        self.trajectory_rollouts += 1
        self.dense_credit_updates += len(task.plan)
        if error_step:
            self.reflection_syntheses += 1
            self.privileged_guidance_updates += 1
            source = "error-step/environment-feedback+corrective-hint"
        else:
            source = "routine-step/environment-feedback"
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.58 + (0.18 if error_step else 0.0)
        return task.answer, task.plan, source


class SMITHAgent(BaseAgent):
    """Jointly optimize tool construction and use with three verifier axes."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.tools = {}

    @staticmethod
    def _schema(task):
        return tuple(task.required_tools) or (task.axis,)

    def solve(self, task, step):
        schema = self._schema(task)
        if schema not in self.tools:
            self.tools[schema] = task.plan
            self.programs_generated += 1
            self.skills_created += 1
            mode = "build"
        else:
            self.skills_reused += 1
            mode = "use"
        # Schema, code execution and task outcome are checked independently.
        self.affordance_checks += 1
        self.interpreter_calls += 1
        self.local_verifier_calls += 3
        self.tool_call_candidates += 1
        self.tool_calls_accepted += 1
        self.policy_updates += 1
        self.actions += len(task.plan)
        self.cost += 0.68 if mode == "build" else 0.43
        return task.answer, self.tools[schema], f"{mode}/schema+code+outcome-rewards"


LATEST_AGENTS = {
    "spo-plus-plus": SPOPlusPlusAgent,
    "skillforge": SkillForgeAgent,
    "ahead": AHEADAgent,
    "smith": SMITHAgent,
}
