"""TFRBench's CPU scoring and bounded five-role reference-construction protocol.

Reference construction consults outcomes and must never be presented as held-out
forecast evaluation. The prediction view itself contains no future target.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from typing import Callable, Sequence

Matrix = tuple[tuple[float, ...], ...]


def matrix(values: Sequence[Sequence[float]]) -> Matrix:
    result = tuple(tuple(float(value) for value in row) for row in values)
    if not result or not result[0] or any(len(row) != len(result[0]) for row in result):
        raise ValueError("nonempty rectangular time-by-channel matrix required")
    if any(not math.isfinite(value) for row in result for value in row):
        raise ValueError("time-series values must be finite")
    return result


def mase(history: Matrix, target: Matrix, forecast: Matrix, seasonality: int = 1) -> float:
    """Eq. (1), separately normalized per channel then averaged across channels.

    Zero-scale channels are undefined, never smoothed to create an easy success.
    Multichannel macro aggregation is a local declared policy; Eq. (1) is scalar.
    """
    history, target, forecast = matrix(history), matrix(target), matrix(forecast)
    channels = len(history[0])
    if len(target) != len(forecast) or len(target[0]) != channels or len(forecast[0]) != channels:
        raise ValueError("forecast/target shape mismatch")
    if not 1 <= seasonality < len(history):
        raise ValueError("seasonality must be shorter than history")
    scores = []
    for channel in range(channels):
        scale = mean(abs(history[i][channel] - history[i - seasonality][channel]) for i in range(seasonality, len(history)))
        if scale == 0:
            raise ValueError("MASE undefined for a zero-scale history channel")
        scores.append(mean(abs(y[channel] - p[channel]) for y, p in zip(target, forecast, strict=True)) / scale)
    return mean(scores)


@dataclass(frozen=True)
class Event:
    text: str
    source_url: str
    published_at: str
    event_time: str

    def __post_init__(self) -> None:
        if not self.text.strip() or not self.source_url.startswith("https://"):
            raise ValueError("grounded event text and HTTPS source required")
        for timestamp in (self.published_at, self.event_time):
            if datetime.fromisoformat(timestamp.replace("Z", "+00:00")).tzinfo is None:
                raise ValueError("event timestamps require a timezone")


@dataclass(frozen=True)
class ForecastView:
    history: Matrix
    reasoning: str
    horizon: int
    description: str


@dataclass(frozen=True)
class ReasonView:
    history: Matrix
    events: tuple[Event, ...]
    description: str
    feedback: str = ""
    assumption_verification: str = ""


@dataclass(frozen=True)
class Candidate:
    reasoning: str
    forecast: Matrix
    consistency: int
    mase: float
    iteration: int


@dataclass(frozen=True)
class ReferenceModels:
    search: Callable[[ReasonView], Sequence[Event]]
    hypotheses: Callable[[ReasonView], str]
    verify_assumptions: Callable[[str, tuple[Event, ...]], str]
    reason: Callable[[ReasonView], Sequence[str]]
    forecast: Callable[[ForecastView], Sequence[Sequence[float]]]
    consistency: Callable[[str, Matrix], int]
    diagnose: Callable[[Candidate], str]
    summarize: Callable[[str], str]
    # The paper describes a composite rank but gives no unique numeric weight.
    # Its exact selection policy is therefore supplied, not silently invented.
    select: Callable[[tuple[Candidate, ...]], int]


class OutcomeEvaluator:
    """Gold-owned evaluator: no serializable model view contains its target."""

    def __init__(self, history: Matrix, target: Matrix, seasonality: int = 1):
        self._history, self.__target = matrix(history), matrix(target)
        self.seasonality = seasonality
        # Validate once before any model callback.
        mase(self._history, self.__target, self.__target, seasonality)

    @property
    def horizon(self) -> int:
        return len(self.__target)

    def score(self, forecast: Matrix) -> float:
        return mase(self._history, self.__target, forecast, self.seasonality)


def evaluate_forecaster(
    *, history: Matrix, target: Matrix, reasoning: str, forecast,
    description: str = "", seasonality: int = 1,
    events: Sequence[Event] = (), cutoff: str,
) -> dict:
    """One-shot heldout forecast evaluation; no outcome feedback or reselection.

    Externally supplied reasoning is NOT certified leakage-free. Callers must
    prove it was produced without outcome-conditioned references or later news.
    """
    cutoff_time = datetime.fromisoformat(cutoff.replace("Z", "+00:00"))
    if cutoff_time.tzinfo is None:
        raise ValueError("cutoff requires a timezone")
    if any(datetime.fromisoformat(e.published_at.replace("Z", "+00:00")) > cutoff_time for e in events):
        raise ValueError("post-cutoff source leaks future information")
    evaluator = OutcomeEvaluator(history, target, seasonality)
    prediction = matrix(forecast(ForecastView(matrix(history), reasoning, evaluator.horizon, description)))
    return {
        "mase": evaluator.score(prediction),
        "forecast": prediction,
        "protocol": "one_shot_heldout_prediction",
        "outcome_feedback": False,
        "reasoning_provenance_verified": False,
    }


def build_reference(
    *, history: Matrix, target: Matrix, models: ReferenceModels,
    description: str = "", seasonality: int = 1,
    max_loops: int = 3, max_candidates_per_loop: int = 3,
) -> dict:
    """Algorithm 1 / §3.2: bounded outcome-conditioned benchmark construction.

    Model callbacks are separate invocations. Python callbacks are trusted code,
    not a security sandbox; the isolation contract is the view passed to them.
    """
    if not 1 <= max_loops <= 3 or not 1 <= max_candidates_per_loop <= 8:
        raise ValueError("bounded loops 1..3 and candidates 1..8 required")
    history = matrix(history)
    evaluator = OutcomeEvaluator(history, target, seasonality)
    feedback, archive = "", []
    selected = None
    for iteration in range(1, max_loops + 1):
        view = ReasonView(history, (), description, feedback)
        events = tuple(models.search(view))
        if any(not isinstance(event, Event) for event in events):
            raise ValueError("search must return grounded Event records")
        hypothesis = models.hypotheses(ReasonView(history, events, description, feedback))
        verification = models.verify_assumptions(hypothesis, events)
        traces = tuple(models.reason(ReasonView(history, events, description, feedback, verification)))
        if not 1 <= len(traces) <= max_candidates_per_loop or any(not trace.strip() for trace in traces):
            raise ValueError("reasoning must respect the nonempty candidate budget")
        candidates = []
        for trace in traces:
            prediction = matrix(models.forecast(ForecastView(history, trace, evaluator.horizon, description)))
            consistency = models.consistency(trace, prediction)
            if type(consistency) is not int or not 1 <= consistency <= 5:
                raise ValueError("verifier score must be an integer 1..5")
            candidates.append(Candidate(trace, prediction, consistency, evaluator.score(prediction), iteration))
        selection = models.select(tuple(candidates))
        if type(selection) is not int or not 0 <= selection < len(candidates):
            raise ValueError("selector must return a candidate index")
        selected = candidates[selection]
        archive.extend(candidates)
        if selected.mase < 1 and selected.consistency >= 4:
            break
        feedback = models.diagnose(selected)
    assert selected is not None
    summary = models.summarize(selected.reasoning)
    if not isinstance(summary, str) or not summary.strip():
        raise ValueError("nonempty summary required")
    summary_forecast = matrix(models.forecast(ForecastView(history, summary, evaluator.horizon, description)))
    summary_consistency = models.consistency(summary, summary_forecast)
    if type(summary_consistency) is not int or not 1 <= summary_consistency <= 5:
        raise ValueError("summary verifier score must be an integer 1..5")
    summary_mase = evaluator.score(summary_forecast)
    accepted = selected.mase < 1 and selected.consistency >= 4
    summary_accepted = accepted and summary_mase < 1 and summary_consistency >= 4
    return {
        "protocol": "outcome_conditioned_benchmark_construction_not_heldout_evaluation",
        "diagnostic_only": True,
        "promotion_eligible": False,
        "future_events_allowed_in_construction": True,
        "candidates": [candidate.__dict__ for candidate in archive],
        "selected": selected.__dict__,
        "reference_accepted": accepted,
        "summary": summary if summary_accepted else None,
        "summary_accepted": summary_accepted,
        "summary_mase": summary_mase,
        "selection_policy": "explicit_callback_paper_does_not_fix_composite_weights",
    }
