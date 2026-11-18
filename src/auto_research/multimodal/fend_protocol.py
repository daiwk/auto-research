"""Deadline/priority and human-FPR evaluation interfaces for FEND.

No audio encoder, beep detector, ASR, dialogue LLM or learned AI-cadence model
is implemented here. Detector events are externally supplied observations.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import math

REQUIRES_GPU_VALIDATION = False
LABELS = ("human", "ai", "ivr", "voicemail")
PRIORITY = {label: rank for rank, label in enumerate(LABELS)}


@dataclass(frozen=True)
class DetectorEvent:
    observed_at: float
    label: str
    detector: str

    def __post_init__(self) -> None:
        if (isinstance(self.observed_at, bool) or not isinstance(self.observed_at, (int, float))
                or not math.isfinite(self.observed_at) or self.observed_at < 0):
            raise ValueError("event time must be finite and nonnegative")
        if self.label not in PRIORITY or self.label == "human" or not self.detector:
            raise ValueError("events must identify one automated class and detector")


def arbitrate(events: Sequence[DetectorEvent], *, deadline: float = 20.0) -> dict:
    """Accumulate through the deadline; class priority is not first-arrival."""
    if (isinstance(deadline, bool) or not isinstance(deadline, (int, float))
            or not math.isfinite(deadline) or deadline <= 0):
        raise ValueError("deadline must be positive and finite")
    admitted = sorted((e for e in events if e.observed_at <= deadline),
                      key=lambda e: (e.observed_at, -PRIORITY[e.label], e.detector))
    label = max((e.label for e in admitted), key=PRIORITY.get, default="human")
    return {"label": label, "deadline": float(deadline),
            "admitted": tuple(admitted), "ignored_late": len(events) - len(admitted)}


def evaluate(gold: Mapping[str, str], predictions: Mapping[str, str]) -> dict:
    """Gold is confined to this outer scorer, never supplied to arbitration."""
    if not gold or set(gold) != set(predictions):
        raise ValueError("nonempty, exactly matching call ids required")
    if any(x not in LABELS for x in (*gold.values(), *predictions.values())):
        raise ValueError("unknown class")
    humans = [k for k, label in gold.items() if label == "human"]
    if not humans:
        raise ValueError("human FPR undefined without true-human calls")
    false_human = sum(predictions[k] != "human" for k in humans)
    return {"calls": len(gold), "true_human_calls": len(humans),
            "human_false_positives": false_human, "human_fpr": false_human / len(humans),
            "accuracy": sum(predictions[k] == v for k, v in gold.items()) / len(gold)}


def _quantile(values: Sequence[float], q: float) -> float:
    ordered = sorted(values)
    position = (len(ordered) - 1) * q
    low, high = math.floor(position), math.ceil(position)
    return ordered[low] * (high - position) + ordered[high] * (position - low) if low != high else ordered[low]


def acoustic_null_gate(reference_humans: Sequence[float], shifted_humans: Sequence[float]) -> dict:
    """Paper's median shift/IQR check on external human-only detector scores.

    Linear sample quantiles are a documented local convention. Passing this
    calibration screen says nothing about positive-class discrimination.
    """
    for values in (reference_humans, shifted_humans):
        if len(values) < 4 or any(isinstance(x, bool) or not isinstance(x, (int, float))
                                  or not math.isfinite(x) for x in values):
            raise ValueError("at least four finite human-only scores per corpus required")
    iqr = _quantile(reference_humans, 0.75) - _quantile(reference_humans, 0.25)
    if iqr <= 0:
        raise ValueError("zero reference IQR: calibration gate is undefined")
    g = (_quantile(shifted_humans, 0.5) - _quantile(reference_humans, 0.5)) / iqr
    return {"normalized_median_shift": g, "admitted": abs(g) <= 1.0}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU protocol only")
    events = [DetectorEvent(1, "ai", "external-cadence"), DetectorEvent(19, "ivr", "external-tool"),
              DetectorEvent(20, "voicemail", "external-beep"),
              DetectorEvent(21, "voicemail", "late-tool")]
    decision = arbitrate(events)
    predictions = {"h": arbitrate([])["label"], "v": decision["label"]}
    score = evaluate({"h": "human", "v": "voicemail"}, predictions)
    shifted = acoustic_null_gate([0, 1, 2, 3], [9, 10, 11, 12])
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "checks": {"priority_over_first_arrival": decision["label"] == "voicemail",
                       "deadline_inclusive_late_ignored": len(decision["admitted"]) == 3
                       and decision["ignored_late"] == 1,
                       "human_default": predictions["h"] == "human",
                       "permutation_invariant": arbitrate(list(reversed(events)))["label"] == decision["label"],
                       "shifted_human_null_rejected": not shifted["admitted"],
                       "gold_only_outer_scorer": score["human_false_positives"] == 0},
            "metrics": {"admitted_events": len(decision["admitted"]),
                        "late_events": decision["ignored_late"], "synthetic_calls": score["calls"],
                        "null_median_shift": shifted["normalized_median_shift"]}}
