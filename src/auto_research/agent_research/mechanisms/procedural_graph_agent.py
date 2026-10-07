"""Extracted unchanged from auto_research.agent_research.latest_20260912; stable mechanism boundary."""
from __future__ import annotations

from collections import Counter, defaultdict
from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence
from auto_research.agent_research.method_families.base import _tokens

class ProceduralGraphAgent(ObservationAgent):
    """Procedure-relation-procedure graph with a conservative edit gate."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.edges = Counter()
        self.accepted_plans: dict[str, tuple[str, ...]] = {}
        self.procedural_graph_edges = 0
        self.heldout_edit_accepts = 0
        self.heldout_edit_rejects = 0

    def solve_observation(self, observation, step):
        answer, observed_plan = read_evidence(observation)
        key = " ".join(sorted(_tokens(observation.intent)))
        prior = self.accepted_plans.get(key, ())
        # A public workflow is a candidate edit.  Replacing an established
        # route is allowed only when it preserves its endpoints, a deterministic
        # local analogue of the paper's held-out validation gate.
        if observed_plan:
            admissible = not prior or (
                observed_plan[0] == prior[0] and observed_plan[-1] == prior[-1]
            )
            if admissible:
                self.accepted_plans[key] = observed_plan
                self.heldout_edit_accepts += 1
                for left, right in zip(observed_plan, observed_plan[1:]):
                    self.edges[(left, "next", right)] += 1
            else:
                self.heldout_edit_rejects += 1
        plan = observed_plan or prior
        self.procedural_graph_edges = len(self.edges)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "procedure-relation-procedure/localize/heldout-edit-gate"
