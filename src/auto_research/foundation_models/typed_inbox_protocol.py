"""Frozen-view, thread isolation and validation-cost interfaces for Typed Inbox.

This is a CPU protocol diagnostic, not an inbox classifier, a secret detector,
or the paper's stratified cross-validation implementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import math
import random
import re
from collections.abc import Sequence

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class FrozenEmail:
    email_id: str
    sender: str
    subject: str
    body: str
    received_at: str
    channel: str
    thread_key: str
    view_sha256: str


def _text(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("email view fields must be strings")
    return value


def freeze_email(*, email_id: str, sender: str, subject: str, body: str,
                 received_at: str, channel: str, secrets: Sequence[str] = ()) -> FrozenEmail:
    """Redact explicit secrets before storing the exact, bounded model view.

    Explicit replacement is deliberately not advertised as complete PII/secret
    discovery. Labels and model predictions are not accepted as view fields.
    """
    values = [_text(x) for x in (email_id, sender, subject, body, received_at, channel)]
    if not email_id or not sender or not channel:
        raise ValueError("email_id, sender and channel are required")
    if isinstance(secrets, (str, bytes)):
        raise TypeError("secrets must be a sequence of strings")
    for secret in sorted(set(secrets), key=len, reverse=True):
        if not isinstance(secret, str) or not secret:
            raise ValueError("explicit secrets must be nonempty strings")
        values = [x.replace(secret, "[REDACTED]") for x in values]
    identity, sender, subject, body, received_at, channel = values
    body = body[:1500]
    normalized_subject = re.sub(r"^(?:(?:re|fw|fwd)\s*:\s*)+", "", subject.strip(), flags=re.I)
    normalized_subject = " ".join(normalized_subject.casefold().split())
    thread = sha256(json.dumps([sender.strip().casefold(), normalized_subject],
                              ensure_ascii=False).encode()).hexdigest()
    payload = [identity, sender, subject, body, received_at, channel]
    digest = sha256(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    return FrozenEmail(*payload, thread, digest)


def grouped_folds(emails: Sequence[FrozenEmail], *, folds: int = 5, seed: int = 42) -> dict[str, int]:
    """Deterministically allocate whole threads, without reading gold labels.

    This local isolation interface does NOT reproduce class-stratified grouped
    CV. A full benchmark must add independent labels and its frozen sampling.
    """
    if isinstance(folds, bool) or not isinstance(folds, int) or folds < 2:
        raise ValueError("folds must be an integer >= 2")
    if len({e.email_id for e in emails}) != len(emails):
        raise ValueError("duplicate email ids")
    groups = sorted({e.thread_key for e in emails},
                    key=lambda key: sha256(f"{seed}:{key}".encode()).hexdigest())
    assignments = {key: i % folds for i, key in enumerate(groups)}
    return {e.email_id: assignments[e.thread_key] for e in emails}


@dataclass(frozen=True)
class ValidationAction:
    score: float
    needs_action: bool


def _score(value: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("score must be finite numeric")
    if not 0 <= value <= 1:
        raise ValueError("score outside [0, 1]")
    return float(value)


@dataclass(frozen=True)
class ActionThreshold:
    threshold: float
    missed_action_cost: float
    false_action_cost: float
    validation_cost: float

    def predict(self, score: float) -> bool:
        return _score(score) >= self.threshold


def fit_action_threshold(validation: Sequence[ValidationAction], *, split: str,
                         missed_action_cost: float = 10.0,
                         false_action_cost: float = 1.0) -> ActionThreshold:
    """Choose a cutoff from validation only; test labels have no argument path."""
    if split != "validation" or not validation:
        raise ValueError("nonempty validation split required; never fit on test")
    costs = (missed_action_cost, false_action_cost)
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0
           for x in costs) or not any(costs):
        raise ValueError("costs must be finite, nonnegative and not both zero")
    for row in validation:
        _score(row.score)
        if type(row.needs_action) is not bool:
            raise TypeError("needs_action must be an independent bool label")
    cutoffs = sorted({0.0, math.nextafter(1.0, math.inf), *(float(r.score) for r in validation)})

    def cost(threshold: float) -> float:
        return sum(missed_action_cost if r.needs_action and r.score < threshold else
                   false_action_cost if not r.needs_action and r.score >= threshold else 0.0
                   for r in validation) / len(validation)

    best = min(cutoffs, key=lambda t: (cost(t), -t))
    return ActionThreshold(best, float(missed_action_cost), float(false_action_cost), cost(best))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU protocol only; no CUDA/model implementation")
    rng = random.Random(seed)
    messages = [freeze_email(email_id=str(i), sender="A@example.org", subject=s,
                            body="private-token " + "x" * 1600, received_at="2026-11-18",
                            channel="email", secrets=("private-token",))
                for i, s in enumerate(("Project", "Re: Project", "Fwd: Project", "Other"))]
    folds = grouped_folds(messages, seed=seed)
    validation = [ValidationAction(0.15 + rng.random() * 0.05, False),
                  ValidationAction(0.7 + rng.random() * 0.05, True)]
    threshold = fit_action_threshold(validation, split="validation")
    rejected_test = False
    try:
        fit_action_threshold(validation, split="test")
    except ValueError:
        rejected_test = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "checks": {"thread_isolation": len({folds[str(i)] for i in range(3)}) == 1,
                       "redacted_before_storage": all("private-token" not in e.body for e in messages),
                       "bounded_exact_view": all(len(e.body) == 1500 for e in messages),
                       "test_fit_rejected": rejected_test,
                       "validation_actions_separated": not threshold.predict(validation[0].score)
                       and threshold.predict(validation[1].score)},
            "metrics": {"messages": len(messages), "threads": len({e.thread_key for e in messages}),
                        "body_limit": 1500, "validation_cost": threshold.validation_cost}}
