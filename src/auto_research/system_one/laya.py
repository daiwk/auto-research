"""Pinned Laya typed-decisions checkpoint provider."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Protocol

from .contracts import (
    ChoiceQuestion,
    DecisionAnswer,
    NoulQuestion,
    ScoreQuestion,
    SystemOneRequest,
    SystemOneResponse,
)


LAYA_REPO_ID = "convaiinnovations/laya-typed-decisions"
LAYA_REVISION = "f9ab0b228f0fc0f14d873dbc99038f135c2da1b2"
LAYA_WEIGHT_SHA256 = (
    "4fa56de72383a9d3efa9cfa78955733c81b9fc8067a587ca4beb82c78107a24e"
)


class LayaAgent(Protocol):
    def system_one(
        self, state: str | Mapping[str, Any] | list[Any], questions: Mapping[str, Any]
    ) -> Mapping[str, Any]: ...


class LayaProvider:
    """Strict adapter around Laya's public ``Agent.system_one`` API."""

    def __init__(
        self,
        agent: LayaAgent,
        *,
        checkpoint_revision: str = LAYA_REVISION,
        temperature_scale: float = 1.0,
    ) -> None:
        if not math.isfinite(temperature_scale) or temperature_scale <= 0:
            raise ValueError("Laya temperature scale must be finite and positive")
        self.agent = agent
        self.checkpoint_revision = checkpoint_revision
        self.temperature_scale = float(temperature_scale)

    @classmethod
    def from_checkpoint(
        cls,
        checkpoint_dir: Path | None = None,
        *,
        allow_download: bool = True,
        revision: str = LAYA_REVISION,
        device: str = "cuda:0",
        temperature_scale: float = 1.0,
    ) -> "LayaProvider":
        if revision != LAYA_REVISION:
            raise ValueError("Laya revision must remain pinned to the audited commit")
        root = checkpoint_dir
        if root is None:
            if not allow_download:
                raise FileNotFoundError("offline Laya requires a local checkpoint")
            try:
                from huggingface_hub import snapshot_download
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError("Install auto-research[system-one-gpu]") from exc
            root = Path(snapshot_download(
                repo_id=LAYA_REPO_ID,
                revision=revision,
                token=False,
                allow_patterns=[
                    "encoder/config.json",
                    "model.safetensors",
                    "rl_agent_config.json",
                    "tokenizer/*",
                ],
            ))
        root = Path(root).expanduser().resolve()
        required = (
            root / "model.safetensors",
            root / "rl_agent_config.json",
            root / "encoder" / "config.json",
            root / "tokenizer" / "tokenizer.json",
        )
        if not all(path.is_file() for path in required):
            raise FileNotFoundError("Laya checkpoint snapshot is incomplete")
        with (root / "model.safetensors").open("rb") as handle:
            digest = hashlib.file_digest(handle, "sha256").hexdigest()
        if digest != LAYA_WEIGHT_SHA256:
            raise ValueError("Laya weight SHA256 does not match the audited checkpoint")
        try:
            from laya import Agent
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install auto-research[system-one-gpu] for Laya") from exc
        return cls(
            Agent(str(root), device=device),
            checkpoint_revision=revision,
            temperature_scale=temperature_scale,
        )

    def decide(self, decision: SystemOneRequest) -> SystemOneResponse:
        questions = {
            key: _question_payload(question)
            for key, question in decision.questions.items()
        }
        raw = self.agent.system_one(decision.state, questions)
        raw_answers = raw.get("answers")
        if not isinstance(raw_answers, Mapping) or set(raw_answers) != set(questions):
            raise ValueError("Laya response question ids do not match request")
        answers: dict[str, DecisionAnswer] = {}
        for key, question in decision.questions.items():
            item = raw_answers[key]
            if not isinstance(item, Mapping):
                raise ValueError(f"Laya answer {key!r} must be an object")
            if isinstance(question, NoulQuestion):
                yes = float(item.get("noul", float("nan")))
                raw_probs = {"false": 1.0 - yes, "true": yes}
                probs = _rescale(raw_probs, self.temperature_scale, key)
                answers[key] = DecisionAnswer(
                    "noul", probs["true"] >= 0.5,
                    {"no": probs["false"], "yes": probs["true"]},
                    max(probs.values()),
                )
            elif isinstance(question, ChoiceQuestion):
                labels = tuple(question.criteria)
                probs = _rescale(item.get("probabilities"), self.temperature_scale, key)
                checked = _probabilities(probs, labels, key)
                winner = max(checked, key=checked.get)
                answers[key] = DecisionAnswer(
                    "choice", winner, checked, max(checked.values())
                )
            elif isinstance(question, ScoreQuestion):
                labels = tuple(question.criteria)
                probs = _rescale(item.get("probabilities"), self.temperature_scale, key)
                indexed = _probabilities(
                    probs, tuple(str(i) for i in range(len(labels))), key
                )
                checked = {
                    label: indexed[str(index)] for index, label in enumerate(labels)
                }
                levels = [_numeric_level(label, i) for i, label in enumerate(labels)]
                expected = sum(
                    checked[label] * level
                    for label, level in zip(labels, levels, strict=True)
                )
                answers[key] = DecisionAnswer(
                    "score", float(expected), checked, max(checked.values())
                )
            else:  # pragma: no cover
                raise TypeError(f"unsupported Laya question: {type(question)!r}")
        usage = raw.get("usage", {})
        if not isinstance(usage, Mapping):
            raise ValueError("Laya usage must be an object")
        return SystemOneResponse(
            model=f"laya:{LAYA_REPO_ID}@{self.checkpoint_revision}",
            answers=answers,
            usage={key: int(value) for key, value in usage.items()},
        )


def _question_payload(question):
    instructions = _text(question.instructions, "Evaluate this structured decision.")
    if isinstance(question, NoulQuestion):
        return {"type": "noul", "instructions": instructions}
    if isinstance(question, ChoiceQuestion):
        return {
            "type": "choice",
            "instructions": instructions,
            "criteria": {
                str(key): _text(value, str(key))
                for key, value in question.criteria.items()
            },
        }
    if isinstance(question, ScoreQuestion):
        return {
            "type": "score",
            "instructions": instructions,
            "criteria": [
                _text(value, str(key)) for key, value in question.criteria.items()
            ],
        }
    raise TypeError(f"unsupported Laya question: {type(question)!r}")


def _text(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value
    if value is not None:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return fallback


def _rescale(raw, scale, question_id):
    if not isinstance(raw, Mapping) or not raw:
        raise ValueError(f"Laya answer {question_id!r} has no probability map")
    values = {str(key): float(value) for key, value in raw.items()}
    if any(not math.isfinite(value) or not 0 <= value <= 1 for value in values.values()):
        raise ValueError(f"Laya answer {question_id!r} has invalid probabilities")
    total = sum(values.values())
    if not math.isclose(total, 1.0, abs_tol=2e-3):
        raise ValueError(f"Laya answer {question_id!r} probabilities do not sum to one")
    if scale == 1.0:
        return {key: value / total for key, value in values.items()}
    logits = {key: math.log(max(value, 1e-12)) / scale for key, value in values.items()}
    pivot = max(logits.values())
    exp = {key: math.exp(value - pivot) for key, value in logits.items()}
    normalizer = sum(exp.values())
    return {key: value / normalizer for key, value in exp.items()}


def _probabilities(raw, expected, question_id):
    if set(raw) != set(expected):
        raise ValueError(
            f"Laya answer {question_id!r} probability labels do not match request"
        )
    result = {key: float(raw[key]) for key in expected}
    if not math.isclose(sum(result.values()), 1.0, abs_tol=1e-5):
        raise ValueError(f"Laya answer {question_id!r} probabilities do not sum to one")
    return result


def _numeric_level(label: str, fallback: int) -> float:
    try:
        return float(label)
    except ValueError:
        return float(fallback)
