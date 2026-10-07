"""Extracted unchanged from auto_research.agent_research.latest_20260826; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.method_families.base import BaseAgent

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
