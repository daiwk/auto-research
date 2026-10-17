"""Live-clock accounting and validation-gated TORSI guidance updates.

This is a protocol component. No game engine, teacher or student is supplied.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import math
from typing import Mapping


@dataclass(frozen=True)
class ActionTiming:
    observation_at: float
    response_at: float
    applied_at: float

    def measurements(self) -> dict[str, float]:
        times = (self.observation_at, self.response_at, self.applied_at)
        if not all(math.isfinite(x) for x in times) or not times[0] <= times[1] <= times[2]:
            raise ValueError("ordered finite observation/response/application times required")
        return {"response_latency": times[1] - times[0], "action_age": times[2] - times[0]}


@dataclass(frozen=True)
class FeedbackTrace:
    task_id: str
    observations: tuple[object, ...]
    actions: tuple[str, ...]
    timings: tuple[ActionTiming, ...]


@dataclass(frozen=True)
class GuidanceDecision:
    guidance: object
    accepted: bool
    paired_validation_gain: float
    validation_tasks: int


def select_guidance(current, candidate, current_scores: Mapping[str, float],
                    candidate_scores: Mapping[str, float], *, split="validation",
                    feedback_task_ids=(), test_task_ids=()) -> GuidanceDecision:
    """Frozen candidate wins strictly on the same validation task identities."""
    ids = set(current_scores)
    if split != "validation" or not ids or not all(ids) or ids != set(candidate_scores):
        raise ValueError("complete paired validation scores required")
    if ids & (set(feedback_task_ids) | set(test_task_ids)):
        raise ValueError("feedback, validation and test task IDs must be disjoint")
    values = [*current_scores.values(), *candidate_scores.values()]
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in values):
        raise ValueError("finite validation scores required, including failures")
    gain = sum(candidate_scores[i] - current_scores[i] for i in sorted(ids)) / len(ids)
    accepted = gain > 0
    return GuidanceDecision(deepcopy(candidate if accepted else current), accepted, gain, len(ids))


def propose_guidance(current, feedback_traces, teacher):
    """A trusted teacher callback sees feedback only, never validation/test cases."""
    traces = tuple(feedback_traces)
    if not traces or len({x.task_id for x in traces}) != len(traces):
        raise ValueError("distinct feedback traces required")
    for trace in traces:
        if len(trace.actions) != len(trace.timings):
            raise ValueError("action timing coverage differs")
        for timing in trace.timings:
            timing.measurements()
    return teacher(deepcopy(current), deepcopy(traces))


def normalized_progress(progress: float, reference: float) -> float:
    if not math.isfinite(progress) or not math.isfinite(reference) or progress < 0 or reference <= 0:
        raise ValueError("nonnegative progress and positive reference required")
    return 100 * min(progress / reference, 1.)
