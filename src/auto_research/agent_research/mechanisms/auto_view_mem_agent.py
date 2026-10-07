"""Extracted unchanged from auto_research.agent_research.latest_20260921; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class AutoViewMemAgent(ObservationAgent):
    """Discover low-overlap write-time views before ordinary top-k retrieval."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.views: dict[str, list[str]] = {}
        self.view_discoveries = self.orthogonal_writes = self.view_consolidations = 0

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        for fact in observation.context:
            tokens = _tokens(fact)
            view = min(tokens, key=len) if tokens else "misc"
            bucket = self.views.setdefault(view, [])
            self.view_discoveries += int(not bucket)
            if fact not in bucket:
                bucket.append(fact); self.orthogonal_writes += 1
            if len(bucket) > self.capacity:
                del bucket[:-self.capacity]; self.view_consolidations += 1
        focused = [fact for key, facts in self.views.items() if key in _tokens(observation.intent) for fact in facts]
        if focused and (not answer or not plan):
            recovered = read_evidence(PublicObservation(observation.task_id, observation.intent, tuple(focused)))
            answer, plan = answer or recovered[0], plan or recovered[1]
        self.cost += len(observation.context); self.actions += len(plan)
        return answer, plan, "write-time-orthogonal-views/top-k"
