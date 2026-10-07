"""Extracted unchanged from auto_research.agent_research.latest_20260912; stable mechanism boundary."""
from __future__ import annotations

from auto_research.agent_research.mechanisms.public_observation import ObservationAgent, PublicObservation, read_evidence

class MAPLEAgent(ObservationAgent):
    """Persistent accepted plan/candidate state across natural-language updates."""

    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.programs: dict[str, tuple[str, ...]] = {}
        self.accepted_solution_updates = 0
        self.reused_executable_states = 0

    def solve_observation(self, observation, step):
        answer, proposed = read_evidence(observation)
        key = observation.intent.split()[0].lower() if observation.intent else "default"
        previous = self.programs.get(key, ())
        if proposed:
            # Executability contract of this mini-suite: a plan is a nonempty
            # sequence of named operations.  Hidden benchmark fields are not
            # used to accept it.
            if all(isinstance(action, str) and action.strip() for action in proposed):
                self.programs[key] = proposed
                self.accepted_solution_updates += 1
        elif previous:
            proposed = previous
            self.reused_executable_states += 1
        self.actions += len(proposed)
        self.cost += len(observation.context)
        return answer, proposed, "persistent-program/accepted-plan/evolutionary-candidate-state"
