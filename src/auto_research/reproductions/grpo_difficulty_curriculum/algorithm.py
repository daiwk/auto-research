"""Paper Eqs1/2/6 and validation-only plateau scheduling."""
from __future__ import annotations

from dataclasses import dataclass

BANDS = ((.625, .875), (.5, .75), (.375, .625), (.25, .5), (.125, .375))


def success_rate(rewards):
    if len(rewards) < 2 or any(r not in (0, 1) for r in rewards):
        raise ValueError("at least two actual binary correctness outcomes required")
    return sum(rewards)/len(rewards)


def band_gate(rewards, band):
    low, high = band
    if not 0 <= low <= high <= 1:
        raise ValueError("success-rate band outside [0,1]")
    return low <= success_rate(rewards) <= high


@dataclass
class PlateauSchedule:
    stage: int = 0
    best: float = -1.
    stale_evaluations: int = 0
    tolerance: float = .0107
    patience: int = 2

    def observe(self, diagnostic_accuracy):
        if not 0 <= diagnostic_accuracy <= 1:
            raise ValueError("diagnostic accuracy outside [0,1]")
        if diagnostic_accuracy > self.best + self.tolerance:
            self.best, self.stale_evaluations = diagnostic_accuracy, 0
            return "new-best"
        self.stale_evaluations += 1
        if self.stale_evaluations >= self.patience and self.stage < len(BANDS)-1:
            self.stage += 1
            self.best, self.stale_evaluations = -1., 0
            return "advance"
        return "keep"


def difficulty_dynamics(history):
    if not history or any(len(row) != len(history[0]) for row in history):
        raise ValueError("aligned problem difficulty history required")
    spans, variation = [], []
    for values in zip(*history):
        spans.append(max(values)-min(values))
        variation.append(sum(abs(b-a) for a,b in zip(values, values[1:])))
    return {"span": spans, "total_variation": variation,
            "extra_round_trip_variation": [v-s for v,s in zip(variation, spans)]}
