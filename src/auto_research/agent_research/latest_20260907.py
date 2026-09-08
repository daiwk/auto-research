"""Observation-only legacy diagnostics, not tool-use or LLM RL benchmarks."""
from __future__ import annotations

from dataclasses import dataclass
import re

from .method_families.base import BaseAgent, _tokens
from .sep7_mechanisms import AtomicMemory, HierarchicalSkills


@dataclass(frozen=True)
class PublicObservation:
    task_id: str
    intent: str
    context: tuple[str, ...]


def read_evidence(observation):
    """Decode public fixture grammar; abstain without unambiguous evidence."""
    answers, plans = [], []
    for fact in observation.context:
        match = re.fullmatch(r"(.+?) case \d+ resolves to (\S+)", fact)
        if match and match[1] in _tokens(observation.intent):
            answers.append(match[2])
        if fact.startswith("workflow "):
            plans.append(tuple(fact.removeprefix("workflow ").split(" -> ")))
    return (answers[0] if len(set(answers)) == 1 else "",
            plans[0] if len(set(plans)) == 1 else ())


class ObservationAgent(BaseAgent):
    def solve(self, task, step):
        observation = PublicObservation(task.task_id, task.intent, tuple(task.context))
        return self.solve_observation(observation, step)

    def solve_observation(self, observation, step):
        del step
        answer, plan = read_evidence(observation)
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "public-fixture-parser; no-tool-execution-or-training"


class AtomRecAgent(ObservationAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.atomic = AtomicMemory(capacity)
        self.atomic_memory_writes = self.multi_hop_retrievals = 0

    def solve_observation(self, observation, step):
        for index, fact in enumerate(observation.context):
            self.atomic.write(f"{observation.task_id}:{index}", fact, step)
            self.atomic_memory_writes += 1
        notes, paths = self.atomic.retrieve(observation.intent, hops=2)
        self.memories_retrieved += len(notes)
        self.multi_hop_retrievals += sum(len(path) > 1 for path in paths)
        answer, plan = read_evidence(observation)
        if not answer or not plan:
            recovered = read_evidence(PublicObservation(
                observation.task_id, observation.intent, tuple(note.content for note in notes)))
            answer, plan = answer or recovered[0], plan or recovered[1]
        self.actions += len(plan)
        self.cost += len(observation.context) + len(notes)
        return answer, plan, "atomic-graph/revision/multi-hop-evidence; public-fixture-parser"


class CoSkillAgent(ObservationAgent):
    def __init__(self, capacity, rng):
        super().__init__(capacity, rng)
        self.library = HierarchicalSkills(capacity)
        self.task_skill_retrievals = self.step_skill_retrievals = self.meta_skill_updates = 0

    def solve_observation(self, observation, step):
        answer, plan = read_evidence(observation)
        parent = self.library.retrieve(observation.intent)
        if parent is not None:
            self.task_skill_retrievals += 1
            children = self.library.bundles[parent]
            self.step_skill_retrievals += len(children)
            self.skills_reused += 1
            if not plan:
                plan = tuple(children)
        # Staging an observed procedure is not an RL update.
        if plan:
            self.library.stage(observation.intent, list(plan))
        self.actions += len(plan)
        self.cost += len(observation.context)
        return answer, plan, "hierarchical-skill/staged-edit; diagnostic-no-policy-training"


class SiLRAgent(ObservationAgent):
    """No safety verdict in this fixture; use ShadowGate with a simulator."""


class MultiHarnessRLAgent(ObservationAgent):
    """No fake RL updates; use relative_credit on harness-labelled rollouts."""


LATEST_AGENTS = {"atomrec": AtomRecAgent, "coskill": CoSkillAgent,
                 "silr": SiLRAgent, "multi-harness-rl": MultiHarnessRLAgent}
