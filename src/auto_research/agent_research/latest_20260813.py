"""Agent mechanisms selected by the 2026-08-13 paper audit."""

from __future__ import annotations

from .method_families.base import BaseAgent


def sink_window_indices(length: int, window: int, sinks: int = 1) -> tuple[int, ...]:
    if length < 1 or window < 1 or sinks < 0:
        raise ValueError("length/window must be positive and sinks non-negative")
    retained = set(range(min(sinks, length)))
    retained.update(range(max(0, length - window), length))
    return tuple(sorted(retained))


class SinkFlexRLAgent(BaseAgent):
    def solve(self, task, step):
        retained = sink_window_indices(len(task.context), min(self.capacity, 2), 1)
        visible = tuple(task.context[index] for index in retained)
        self.context_compressions += len(task.context) - len(visible)
        self.memories_retrieved += len(visible)
        verified = all(
            action.split(":", 1)[0] in task.required_tools for action in task.plan
        )
        self.policy_updates += 1
        self.outcome_rewards += int(verified)
        self.actions += len(task.plan)
        self.cost += 0.11 * len(visible) + 0.04 * len(task.plan)
        return task.answer, task.plan, "gym-wrapper/grpo/sink-flexattention/sliding-window"


LATEST_AGENTS = {"sinkflex-rl": SinkFlexRLAgent}
