"""Provider-neutral contract for Choice, Score and Noul decisions.

The wire shape follows TypeSafe's public System One documentation, but the
types are intentionally provider neutral so local and future open backends can
be evaluated with the same questions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


Description = str | Mapping[str, Any] | list[Any] | None


@dataclass(frozen=True)
class ChoiceQuestion:
    instructions: Description
    criteria: Mapping[str, Description]
    type: str = field(default="choice", init=False)

    def __post_init__(self) -> None:
        if not 2 <= len(self.criteria) <= 255:
            raise ValueError("choice criteria must contain 2 to 255 options")
        if any(not str(key).strip() for key in self.criteria):
            raise ValueError("choice option names must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "instructions": self.instructions,
            "criteria": dict(self.criteria),
        }


@dataclass(frozen=True)
class ScoreQuestion:
    instructions: Description
    criteria: Mapping[str, Description]
    type: str = field(default="score", init=False)

    def __post_init__(self) -> None:
        if not 2 <= len(self.criteria) <= 10:
            raise ValueError("score criteria must contain 2 to 10 ordered levels")

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "instructions": self.instructions,
            "criteria": dict(self.criteria),
        }


@dataclass(frozen=True)
class NoulQuestion:
    instructions: Description
    type: str = field(default="noul", init=False)

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "instructions": self.instructions}


Question = ChoiceQuestion | ScoreQuestion | NoulQuestion


@dataclass(frozen=True)
class SystemOneRequest:
    state: str | Mapping[str, Any] | list[Any]
    questions: Mapping[str, Question]
    model: str = "jev-latest"

    def __post_init__(self) -> None:
        if not self.questions:
            raise ValueError("at least one question is required")
        if any(not str(key).strip() for key in self.questions):
            raise ValueError("question ids must be non-empty")

    def to_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "model": self.model,
            "questions": {key: question.to_dict() for key, question in self.questions.items()},
        }


@dataclass(frozen=True)
class DecisionAnswer:
    type: str
    value: str | float | bool
    probabilities: Mapping[str, float]
    confidence: float

    def __post_init__(self) -> None:
        if self.type not in {"choice", "score", "noul"}:
            raise ValueError(f"unsupported answer type: {self.type}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0, 1]")
        if self.probabilities:
            values = tuple(float(value) for value in self.probabilities.values())
            if any(value < 0.0 or value > 1.0 for value in values):
                raise ValueError("probabilities must be in [0, 1]")
            if abs(sum(values) - 1.0) > 1e-5:
                raise ValueError("choice/score probabilities must sum to one")


@dataclass(frozen=True)
class SystemOneResponse:
    model: str
    answers: Mapping[str, DecisionAnswer]
    usage: Mapping[str, int] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "SystemOneResponse":
        raw_answers = payload.get("answers")
        if not isinstance(raw_answers, Mapping):
            raise ValueError("response.answers must be an object")
        answers: dict[str, DecisionAnswer] = {}
        for key, raw in raw_answers.items():
            if not isinstance(raw, Mapping):
                raise ValueError(f"answer {key!r} must be an object")
            kind = str(raw.get("type", ""))
            if kind == "choice":
                value = str(raw["choice"])
                probabilities = _probabilities(raw.get("probabilities", {}))
                confidence = float(raw.get("confidence", max(probabilities.values())))
            elif kind == "score":
                value = float(raw["score"])
                probabilities = _probabilities(raw.get("probabilities", {}))
                confidence = float(raw.get("confidence", max(probabilities.values())))
            elif kind == "noul":
                yes = float(raw["noul"])
                if not 0.0 <= yes <= 1.0:
                    raise ValueError("noul probability must be in [0, 1]")
                value = yes >= 0.5
                probabilities = {"no": 1.0 - yes, "yes": yes}
                confidence = max(yes, 1.0 - yes)
            else:
                raise ValueError(f"unsupported answer type: {kind!r}")
            answers[str(key)] = DecisionAnswer(
                kind, value, probabilities, confidence
            )
        usage = payload.get("usage", {})
        if not isinstance(usage, Mapping):
            raise ValueError("response.usage must be an object")
        return cls(str(payload.get("model", "unknown")), answers, dict(usage))


def _probabilities(raw: Any) -> dict[str, float]:
    if not isinstance(raw, Mapping) or not raw:
        raise ValueError("choice/score answer requires a probability map")
    return {str(key): float(value) for key, value in raw.items()}
