"""Extracted unchanged from auto_research.agent_research.latest_20260912; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence

class FeedbackScaffoldAgent(ObservationAgent):
    """Early public action guidance followed by late observation enrichment."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.early_action_guidance = 0
        self.feedback_observations = 0
        self.late_stage_enrichments = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        # FEE switches scaffold type over the trajectory.  At the first turn a
        # workflow explicitly present in the public observation can guide the
        # action sequence; this is evidence supplied to the agent, never the
        # benchmark's hidden gold plan.
        if step == 0 and plan:
            self.early_action_guidance += 1
        # Enrichment exposes state summaries only after initial exploration;
        # it never inserts a next-action label.
        if step > 0:
            summaries = tuple(
                fact for fact in observation.context if "resolves to" in fact
            )
            self.feedback_observations += len(summaries)
            self.late_stage_enrichments += int(bool(summaries))
            if not answer:
                answer, _ = read_evidence(PublicObservation(
                    observation.task_id, observation.intent, summaries
                ))
        self.actions += len(plan)
        self.cost += len(observation.context)
        phase = "early-public-action-guidance" if step == 0 else "late-observation-enrichment"
        return answer, plan, f"{phase}/feedback-scaffold"
