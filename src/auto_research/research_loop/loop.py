from __future__ import annotations

import time
from collections.abc import Callable, Iterable
from typing import Any, Protocol

from ..models import Trial
from .cache import TrialCache

Evaluate = Callable[[dict[str, Any]], float]
OnTrial = Callable[[Trial, Trial | None], None]


class ProposalStrategy(Protocol):
    """Adaptive idea source; implementations may inspect all prior trials."""

    def propose(self, history: tuple[Trial, ...]) -> dict[str, Any] | None: ...


class SequenceProposer:
    """Adapter from a deterministic search space to the adaptive proposal API."""

    def __init__(self, proposals: Iterable[dict[str, Any]]):
        self._iterator = iter(proposals)

    def propose(self, _history: tuple[Trial, ...]) -> dict[str, Any] | None:
        return next(self._iterator, None)


class IterativeResearchLoop:
    """Run proposed settings while keeping orchestration independent of ML code.

    A future agent can replace the proposal iterable without changing evaluation,
    caching, checkpointing, or report generation.
    """

    def __init__(
        self,
        evaluate: Evaluate,
        direction: str,
        cache: TrialCache | None = None,
        cache_context: dict[str, Any] | None = None,
        force_rerun: bool = False,
    ):
        if direction not in {"minimize", "maximize"}:
            raise ValueError("direction must be minimize or maximize")
        self.evaluate = evaluate
        self.direction = direction
        self.cache = cache
        self.cache_context = cache_context or {}
        self.force_rerun = force_rerun

    def run(
        self,
        proposals: Iterable[dict[str, Any]] | ProposalStrategy,
        on_trial: OnTrial | None = None,
    ) -> tuple[list[Trial], Trial | None]:
        proposer = (
            proposals
            if hasattr(proposals, "propose")
            else SequenceProposer(proposals)
        )
        trials: list[Trial] = []
        best: Trial | None = None
        while (params := proposer.propose(tuple(trials))) is not None:
            number = len(trials) + 1
            trial = None
            if self.cache and not self.force_rerun:
                trial = self.cache.load(self.cache_context, params, number)
            if trial is None:
                trial = self._evaluate(number, params)
                if self.cache and trial.metric is not None:
                    self.cache.save(self.cache_context, trial)
            trials.append(trial)
            best = choose_best(trials, self.direction)
            if on_trial:
                on_trial(trial, best)
        return trials, best

    def _evaluate(self, number: int, params: dict[str, Any]) -> Trial:
        started = time.monotonic()
        try:
            metric = float(self.evaluate(params))
            return Trial(number, params, metric, "completed", time.monotonic() - started)
        except Exception as exc:
            return Trial(
                number,
                params,
                None,
                "failed",
                time.monotonic() - started,
                f"{type(exc).__name__}: {exc}",
            )


def choose_best(trials: list[Trial], direction: str) -> Trial | None:
    completed = [trial for trial in trials if trial.metric is not None]
    if not completed:
        return None
    return (min if direction == "minimize" else max)(
        completed, key=lambda trial: trial.metric
    )
