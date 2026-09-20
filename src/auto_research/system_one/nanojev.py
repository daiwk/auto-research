"""Pinned NanoJev checkpoint provider for the shared System One contract.

NanoJev is an independent community model, not an implementation of
TypeSafe's unpublished Jev architecture or RLCD training algorithm.  The
provider loads the public checkpoint's bundled inference source at an exact
Hugging Face commit and converts only the public typed-decision wire format.
"""

from __future__ import annotations

import importlib.util
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


NANOJEV_REPO_ID = "C-Tianyu/NanoJev"
NANOJEV_REVISION = "047b927b30882a1138fc504821b82ac145a4b81a"
NANOJEV_BASE_MODEL = "Qwen/Qwen3-0.6B"
NANOJEV_BASE_REVISION = "c1899de289a04d12100db370d81485cdf75e47ca"
NANOJEV_WEIGHT_SHA256 = (
    "f68c47d66998231b86b7e91b4ed5e82ae23acf104c8b7cd6d165c3ac7b7ffe1b"
)


class NanoJevPredictor(Protocol):
    def predict(
        self,
        payload: Mapping[str, Any],
        *,
        batch_questions: int = 0,
        temperature: float = 1.0,
    ) -> Mapping[str, Any]: ...


class NanoJevProvider:
    """Adapt a persistent NanoJev ``DecisionPredictor`` to SystemOneProvider."""

    def __init__(
        self,
        predictor: NanoJevPredictor,
        *,
        temperature: float = 1.0,
        batch_questions: int = 0,
        checkpoint_revision: str = NANOJEV_REVISION,
    ) -> None:
        if not math.isfinite(temperature) or temperature <= 0.0:
            raise ValueError("NanoJev temperature must be a finite positive number")
        if batch_questions < 0:
            raise ValueError("NanoJev batch_questions must be non-negative")
        self.predictor = predictor
        self.temperature = float(temperature)
        self.batch_questions = int(batch_questions)
        self.checkpoint_revision = checkpoint_revision
        self.last_execution: dict[str, Any] = {}

    @classmethod
    def from_checkpoint(
        cls,
        checkpoint_dir: Path | None = None,
        *,
        allow_download: bool = True,
        revision: str = NANOJEV_REVISION,
        device: str = "cuda:0",
        precision: str = "bf16",
        temperature: float = 1.0,
        batch_questions: int = 0,
        disable_native_triton: bool = False,
    ) -> "NanoJevProvider":
        if revision != NANOJEV_REVISION:
            raise ValueError(
                "NanoJev revision must remain pinned to the audited immutable commit"
            )
        root = checkpoint_dir
        if root is None:
            if not allow_download:
                raise FileNotFoundError(
                    "NanoJev checkpoint is not local and downloads are disabled"
                )
            try:
                from huggingface_hub import snapshot_download
            except ImportError as exc:  # pragma: no cover - optional GPU dependency
                raise RuntimeError(
                    "Install auto-research[system-one-gpu] to download NanoJev"
                ) from exc
            root = Path(snapshot_download(
                repo_id=NANOJEV_REPO_ID,
                revision=revision,
                token=False,
                allow_patterns=[
                    "best.safetensors",
                    "config.json",
                    "backbone_config/*",
                    "tokenizer/*",
                    "source/LICENSE",
                    "source/scripts/predict_toy_decisions.py",
                    "source/scripts/train_toy_decisions.py",
                ],
            ))
        root = Path(root).expanduser().resolve()
        script = root / "source" / "scripts" / "predict_toy_decisions.py"
        if not script.is_file():
            raise FileNotFoundError(
                f"NanoJev checkpoint is missing bundled inference source: {script}"
            )
        module = _load_module(script)
        predictor = module.DecisionPredictor(
            root,
            device_name=device,
            precision=precision,
            disable_native_triton=disable_native_triton,
        )
        return cls(
            predictor,
            temperature=temperature,
            batch_questions=batch_questions,
            checkpoint_revision=revision,
        )

    def decide(self, decision: SystemOneRequest) -> SystemOneResponse:
        payload = {
            "states": [{
                "id": "request",
                "state": decision.state,
                "questions": {
                    key: _question_payload(question)
                    for key, question in decision.questions.items()
                },
            }]
        }
        raw = self.predictor.predict(
            payload,
            batch_questions=self.batch_questions,
            temperature=self.temperature,
        )
        answers, execution = _parse_response(raw, decision)
        self.last_execution = execution
        usage = {
            key: int(execution[key])
            for key in ("candidate_paths", "forward_passes", "autoregressive_decode_steps")
            if isinstance(execution.get(key), int)
        }
        return SystemOneResponse(
            model=f"nanojev:{NANOJEV_REPO_ID}@{self.checkpoint_revision}",
            answers=answers,
            usage=usage,
        )


def _load_module(path: Path):
    spec = importlib.util.spec_from_file_location("auto_research_nanojev_inference", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load NanoJev inference source: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, "DecisionPredictor"):
        raise RuntimeError("NanoJev inference source has no DecisionPredictor")
    return module


def _description_text(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value
    if value is not None:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
        if text.strip():
            return text
    return fallback


def _question_payload(question) -> dict[str, Any]:
    instructions = _description_text(
        question.instructions, "Evaluate this structured decision."
    )
    if isinstance(question, NoulQuestion):
        return {"type": "boolean", "instructions": instructions}
    if isinstance(question, ChoiceQuestion):
        return {
            "type": "choice",
            "instructions": instructions,
            "criteria": {
                str(key): _description_text(value, str(key))
                for key, value in question.criteria.items()
            },
        }
    if isinstance(question, ScoreQuestion):
        return {
            "type": "score",
            "instructions": instructions,
            "criteria": [
                _description_text(value, str(key))
                for key, value in question.criteria.items()
            ],
        }
    raise TypeError(f"unsupported NanoJev question: {type(question)!r}")


def _parse_response(
    raw: Mapping[str, Any], decision: SystemOneRequest
) -> tuple[dict[str, DecisionAnswer], dict[str, Any]]:
    states = raw.get("states")
    if not isinstance(states, list) or len(states) != 1:
        raise ValueError("NanoJev response must contain exactly one state")
    state = states[0]
    if not isinstance(state, Mapping) or state.get("id") != "request":
        raise ValueError("NanoJev response state id does not match request")
    raw_answers = state.get("answers")
    if not isinstance(raw_answers, Mapping) or set(raw_answers) != set(decision.questions):
        raise ValueError("NanoJev response question ids do not match request")
    answers: dict[str, DecisionAnswer] = {}
    for key, question in decision.questions.items():
        item = raw_answers[key]
        if not isinstance(item, Mapping):
            raise ValueError(f"NanoJev answer {key!r} must be an object")
        raw_probabilities = item.get("probabilities")
        if not isinstance(raw_probabilities, Mapping):
            raise ValueError(f"NanoJev answer {key!r} has no probability map")
        if isinstance(question, NoulQuestion):
            probabilities = _validated_probabilities(
                raw_probabilities, ("false", "true"), key
            )
            yes = probabilities["true"]
            answer = DecisionAnswer(
                "noul", yes >= 0.5,
                {"no": probabilities["false"], "yes": yes},
                max(probabilities.values()),
            )
        elif isinstance(question, ChoiceQuestion):
            labels = tuple(question.criteria)
            probabilities = _validated_probabilities(raw_probabilities, labels, key)
            winner = max(probabilities, key=probabilities.get)
            answer = DecisionAnswer(
                "choice", winner, probabilities, max(probabilities.values())
            )
        elif isinstance(question, ScoreQuestion):
            labels = tuple(question.criteria)
            indexed = _validated_probabilities(
                raw_probabilities, tuple(str(index) for index in range(len(labels))), key
            )
            probabilities = {
                label: indexed[str(index)] for index, label in enumerate(labels)
            }
            levels = [_numeric_level(label, index) for index, label in enumerate(labels)]
            score = sum(
                probabilities[label] * level
                for label, level in zip(labels, levels, strict=True)
            )
            answer = DecisionAnswer(
                "score", float(score), probabilities, max(probabilities.values())
            )
        else:  # pragma: no cover - closed union
            raise TypeError(f"unsupported NanoJev question: {type(question)!r}")
        answers[key] = answer
    execution = raw.get("execution", {})
    if not isinstance(execution, Mapping):
        raise ValueError("NanoJev execution metadata must be an object")
    return answers, dict(execution)


def _validated_probabilities(
    raw: Mapping[str, Any], expected: tuple[str, ...], question_id: str
) -> dict[str, float]:
    if set(raw) != set(expected):
        raise ValueError(
            f"NanoJev answer {question_id!r} probability labels do not match request"
        )
    result = {key: float(raw[key]) for key in expected}
    if any(not math.isfinite(value) or not 0.0 <= value <= 1.0 for value in result.values()):
        raise ValueError(f"NanoJev answer {question_id!r} contains invalid probabilities")
    if not math.isclose(sum(result.values()), 1.0, abs_tol=1e-5):
        raise ValueError(f"NanoJev answer {question_id!r} probabilities do not sum to one")
    return result


def _numeric_level(key: str, fallback: int) -> float:
    try:
        return float(key)
    except ValueError:
        return float(fallback)
