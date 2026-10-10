"""MASS workflow search and trajectory selection (2610.12176).

Callbacks execute the actual model/scaffold. Tests with scripted callbacks are
controller diagnostics only; they do not establish recursive capability gains.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
from typing import Protocol

import numpy as np


@dataclass(frozen=True)
class Task:
    identifier: str
    prompt: str
    initial_workflow: str
    split: str = "train"


@dataclass(frozen=True)
class Conversation:
    role: str
    messages: tuple[dict, ...]


@dataclass(frozen=True)
class Execution:
    identifier: str
    workspace: str
    conversations: tuple[Conversation, ...]


class SharedModel(Protocol):
    revision: str

    def execute(self, task: Task, workflow: str) -> Execution: ...
    def propose(self, task: Task, previous: str, incumbent: str, history: list) -> str: ...
    def compare(self, task: Task, candidate: Execution, incumbent: Execution) -> tuple[float, str]: ...
    def fine_tune(self, training: tuple[Conversation, ...],
                  validation: tuple[Conversation, ...]) -> "SharedModel": ...


def bradley_terry_ranking(n, comparisons, iterations=500):
    """Fit pairwise fractional wins with a small finite-score ridge penalty."""
    if n < 2 or not comparisons:
        raise ValueError("pairwise ranking requires at least two candidates")
    scores = np.zeros(n, dtype=float)
    for _ in range(iterations):
        gradient = -.001 * scores
        for a, b, win in comparisons:
            if not 0 <= win <= 1 or not (0 <= a < n and 0 <= b < n) or a == b:
                raise ValueError("invalid pairwise comparison")
            probability = 1 / (1 + np.exp(-np.clip(scores[a] - scores[b], -30, 30)))
            residual = win - probability
            gradient[a] += residual
            gradient[b] -= residual
        scores += .1 * gradient / len(comparisons)
        scores -= scores.mean()
    return tuple(np.argsort(-scores, kind="stable").tolist()), tuple(scores.tolist())


def _bare_orchestrator(task, execution):
    rendered = []
    for conversation in execution.conversations:
        messages = [dict(message) for message in conversation.messages]
        if conversation.role == "orchestrator":
            index = next((i for i, m in enumerate(messages) if m["role"] == "user"), None)
            if index is None:
                raise ValueError("orchestrator trajectory has no task prompt")
            messages[index]["content"] = task.prompt
        # Worker assignments, tool observations and system prompts are retained;
        # tokenization downstream must mask all non-assistant messages.
        rendered.append(Conversation(conversation.role, tuple(messages)))
    return tuple(rendered)


def run_mass(model: SharedModel, tasks: tuple[Task, ...], *, cycles=2, search_iterations=2,
             candidates=4, selected=3, guardrail=lambda workflow: bool(workflow.strip())):
    """Algorithms 1–3; self-evaluation only, disjoint SFT episode validation.

    No held-out external judge is accepted here: external evaluation belongs to
    the caller after all cycles and cannot steer workflow or checkpoint choices.
    """
    if not tasks or any(t.split != "train" for t in tasks):
        raise ValueError("MASS optimization only accepts training tasks")
    if not (cycles > 0 and search_iterations >= 0 and 2 <= selected <= candidates):
        raise ValueError("invalid MASS search/collection budget")
    if len({t.identifier for t in tasks}) != len(tasks):
        raise ValueError("duplicate training task identifiers")
    audits = []
    for cycle in range(cycles):
        revision = model.revision
        training, validation = [], []
        for task in tasks:
            previous = incumbent = task.initial_workflow
            best = model.execute(task, incumbent)
            feedback = []
            for iteration in range(search_iterations):
                proposal = model.propose(task, previous, incumbent, feedback)
                if not guardrail(proposal):
                    raise ValueError("workflow violates scaffold structural guardrails")
                execution = model.execute(task, proposal)
                win, rationale = model.compare(task, execution, best)
                if win not in {0., .5, 1.}:
                    raise ValueError("self-comparison verdict must be loss/tie/win")
                feedback.append({"iteration": iteration, "workflow": proposal,
                                 "win": win, "rationale": rationale})
                if win > .5:
                    incumbent, best = proposal, execution
                previous = proposal
            pool = [model.execute(task, incumbent) for _ in range(candidates)]
            if len({e.identifier for e in pool}) != candidates:
                raise ValueError("collection requires independent trajectory identifiers")
            comparisons = [(a, b, model.compare(task, pool[a], pool[b])[0])
                           for a, b in itertools.combinations(range(candidates), 2)]
            ranking, scores = bradley_terry_ranking(candidates, comparisons)
            for index in ranking[:selected - 1]:
                training.extend(_bare_orchestrator(task, pool[index]))
            validation.extend(_bare_orchestrator(task, pool[ranking[selected - 1]]))
            audits.append({"cycle": cycle, "task": task.identifier, "revision": revision,
                           "workflow": incumbent, "search": feedback,
                           "training_episodes": [pool[i].identifier for i in ranking[:selected - 1]],
                           "validation_episode": pool[ranking[selected - 1]].identifier,
                           "bradley_terry_scores": scores})
            if model.revision != revision:
                raise ValueError("executor/evaluator/optimizer weights changed within a generation")
        updated = model.fine_tune(tuple(training), tuple(validation))
        if updated.revision == revision:
            raise ValueError("MASS cycle must return an actually updated model revision")
        model = updated
    return model, audits
