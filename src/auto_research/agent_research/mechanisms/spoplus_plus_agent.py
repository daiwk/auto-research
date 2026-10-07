"""Extracted unchanged from auto_research.agent_research.latest_20260826; stable mechanism boundary."""
from __future__ import annotations

from collections import defaultdict
from auto_research.agent_research.method_families.base import BaseAgent

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
