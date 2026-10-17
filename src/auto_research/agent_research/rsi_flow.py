"""Bounded, callback-driven RSIFlow skill-memory variant (no model backend).

The controller is fixed. Only a declared Task component and evidence-backed
experience records change. Reporting feedback is never passed to selection.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
import math
from typing import Callable, Mapping


COMPONENTS = ("model", "harness", "artifacts")


def _digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


@dataclass(frozen=True)
class Task:
    task_id: str
    payload: object


@dataclass(frozen=True)
class TaskState:
    model: object
    harness: object
    artifacts: object

    def fingerprint(self):
        return _digest([self.model, self.harness, self.artifacts])


@dataclass(frozen=True)
class Attempt:
    round_index: int
    attempt_index: int
    component: str
    parent_sha256: str
    candidate_sha256: str | None
    accepted: bool
    valid: bool
    paired_gain: float | None
    failure: str | None


@dataclass(frozen=True)
class EvolutionResult:
    state: TaskState
    attempts: tuple[Attempt, ...]
    skills: tuple[dict, ...]
    reporting_scores: Mapping[str, float]


def _tasks(tasks):
    values = tuple(tasks)
    if not values or len(values) > 1000 or any(not t.task_id for t in values):
        raise ValueError("one to 1000 identified public tasks required")
    if len({t.task_id for t in values}) != len(values):
        raise ValueError("duplicate task identifier")
    # Payloads must be serializable so identity checks do not depend on object addresses.
    for task in values:
        _digest(task.payload)
    return values


def _scores(evaluator, state, tasks, split):
    scores = dict(evaluator(deepcopy(state), deepcopy(tasks), split))
    if set(scores) != {t.task_id for t in tasks}:
        raise ValueError("evaluator must retain every task, including failures")
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v)
           for v in scores.values()):
        raise ValueError("finite numeric scores required")
    return {k: float(v) for k, v in scores.items()}


def evolve(
    initial: TaskState,
    training_batches,
    reporting_tasks,
    *,
    selector: Callable,
    proposers: Mapping[str, Callable],
    evaluator: Callable,
    attempts_per_round: int = 2,
    max_candidate_evaluations: int = 10,
    skill_distiller: Callable | None = None,
) -> EvolutionResult:
    """Execute M/H/A callbacks on immutable parents and paired training batches.

    Proposers receive only public tasks, scalar parent scores and past training
    evidence. Gold stays in the caller's evaluator. This is an API isolation
    contract, not an OS sandbox against malicious Python callbacks.
    """
    batches = tuple(_tasks(batch) for batch in training_batches)
    report = _tasks(reporting_tasks)
    if not batches or len(batches) > 20 or not 1 <= attempts_per_round <= 5:
        raise ValueError("bounded rounds and attempts required")
    if not 0 <= max_candidate_evaluations <= 100:
        raise ValueError("bounded candidate budget required")
    if set(proposers) != set(COMPONENTS):
        raise ValueError("explicit Model/Harness/Artifacts callbacks required")
    seen_ids, seen_payloads = set(), set()
    for batch in (*batches, report):
        ids = {t.task_id for t in batch}
        payloads = {_digest(t.payload) for t in batch}
        if seen_ids & ids or seen_payloads & payloads:
            raise ValueError("training rounds and reporting tasks must be disjoint")
        seen_ids |= ids
        seen_payloads |= payloads
    state, attempts, skills, consumed = deepcopy(initial), [], [], 0
    for round_index, batch in enumerate(batches):
        parent = deepcopy(state)
        parent_hash = parent.fingerprint()
        baseline = _scores(evaluator, parent, batch, "training")
        for attempt_index in range(attempts_per_round):
            if consumed >= max_candidate_evaluations:
                break
            context = {"round_index": round_index, "parent_sha256": parent_hash,
                       "task_ids": tuple(baseline), "parent_scores": dict(baseline)}
            component = selector(deepcopy(tuple(attempts)), deepcopy(tuple(skills)), context)
            if component not in COMPONENTS:
                raise ValueError("selector returned an undeclared component")
            candidate_hash, gain, failure, valid, accepted = None, None, None, False, False
            consumed += 1  # Implementation failures consume attempts too.
            stage = "proposal"
            try:
                candidate = proposers[component](
                    deepcopy(parent), deepcopy(batch), dict(baseline), deepcopy(tuple(skills)))
                if not isinstance(candidate, TaskState):
                    raise ValueError("proposer must return TaskState")
                candidate_hash = candidate.fingerprint()
                stage = "component_scope"
                if any(_digest(getattr(candidate, c)) != _digest(getattr(parent, c))
                       for c in COMPONENTS if c != component):
                    raise ValueError("candidate changed a component outside its declared scope")
                stage = "paired_evaluation"
                scores = _scores(evaluator, candidate, batch, "training")
                gain = sum(scores[k] - baseline[k] for k in baseline) / len(baseline)
                valid, accepted = True, gain > 0
                if accepted:
                    state = deepcopy(candidate)
            except Exception as exc:
                # Retain the failure denominator without passing arbitrary logs to the next model.
                failure = f"{stage}: {type(exc).__name__}"
            if parent.fingerprint() != parent_hash:
                raise RuntimeError("frozen parent changed")
            record = Attempt(round_index, attempt_index, component, parent_hash,
                             candidate_hash, accepted, valid, gain, failure)
            attempts.append(record)
            skills.append({"component": component, "accepted": accepted, "valid": valid,
                           "paired_gain": gain, "parent_sha256": parent_hash,
                           "lesson": "positive paired training evidence" if accepted else
                                     "counterexample: preserve parent and diagnose failure",
                           "evidence_round": round_index, "evidence_attempt": attempt_index})
            if skill_distiller is not None:
                distilled = tuple(skill_distiller(deepcopy(tuple(attempts)), deepcopy(tuple(skills))))
                _digest(distilled)  # Plain skill records, never executable program changes.
                if any(not isinstance(s, dict) for s in distilled) or len(distilled) > 1000:
                    raise ValueError("bounded serializable skill records required")
                skills = list(deepcopy(distilled))
            if accepted:
                break
        # A rejected candidate never becomes the next attempt's starting point.
    reporting = _scores(evaluator, state, report, "reporting")
    return EvolutionResult(deepcopy(state), tuple(attempts), tuple(deepcopy(skills)), reporting)
