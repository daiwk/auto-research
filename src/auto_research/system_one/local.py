"""Small auditable Jev-shaped decision model for local experiments.

This is an independent implementation of the public input/output shape.  It is
not a reconstruction of TypeSafe's unpublished architecture or training data.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
import re
from typing import Iterable, Mapping

import numpy as np

from .contracts import (
    ChoiceQuestion,
    DecisionAnswer,
    NoulQuestion,
    ScoreQuestion,
    SystemOneRequest,
    SystemOneResponse,
)


TOKEN = re.compile(r"[\w]+", re.UNICODE)


@dataclass(frozen=True)
class DecisionTrainingExample:
    state: str
    instructions: str
    criteria: Mapping[str, str]
    target: str


class LocalDecisionModel:
    """Candidate-conditioned bilinear scorer with optional rival centering."""

    def __init__(
        self,
        dimensions: int = 256,
        *,
        architecture: str = "bilinear",
        objective: str = "cross_entropy",
        seed: int = 42,
    ) -> None:
        if dimensions < 8:
            raise ValueError("dimensions must be at least 8")
        if architecture not in {"bilinear", "rival_attention"}:
            raise ValueError("architecture must be bilinear or rival_attention")
        if objective not in {"cross_entropy", "brier", "hybrid"}:
            raise ValueError("objective must be cross_entropy, brier or hybrid")
        self.dimensions = dimensions
        self.architecture = architecture
        self.objective = objective
        rng = np.random.default_rng(seed)
        self.weight = np.eye(dimensions, dtype=np.float64) * 0.25
        self.weight += rng.normal(0.0, 0.01, size=(dimensions, dimensions))
        self.temperature = 1.0
        self._criteria_cache: dict[tuple[tuple[str, str], ...], np.ndarray] = {}

    def fit(
        self,
        examples: Iterable[DecisionTrainingExample],
        *,
        steps: int = 80,
        learning_rate: float = 0.15,
        seed: int = 42,
    ) -> dict[str, float]:
        rows = tuple(examples)
        if not rows:
            raise ValueError("training examples cannot be empty")
        if steps < 1 or learning_rate <= 0:
            raise ValueError("steps and learning_rate must be positive")
        rng = np.random.default_rng(seed)
        losses: list[float] = []
        candidate_cache: dict[tuple[tuple[str, str], ...], np.ndarray] = {}
        for index in rng.integers(0, len(rows), size=steps):
            row = rows[int(index)]
            labels = tuple(row.criteria)
            if row.target not in row.criteria:
                raise ValueError(f"unknown target {row.target!r}")
            state = _encode(f"{row.instructions} {row.state}", self.dimensions)
            cache_key = tuple((str(key), str(value)) for key, value in row.criteria.items())
            candidates = candidate_cache.setdefault(
                cache_key, self._candidate_vectors(row.criteria)
            )
            probabilities = _softmax(self._logits(state, candidates))
            target = np.zeros(len(labels), dtype=np.float64)
            target[labels.index(row.target)] = 1.0
            delta, loss = _objective_gradient(probabilities, target, self.objective)
            # sum_i delta_i outer(state, candidate_i)
            gradient = np.outer(state, delta @ candidates)
            self.weight -= learning_rate * np.clip(gradient, -2.0, 2.0)
            losses.append(loss)
        return {
            "initial_loss": float(losses[0]),
            "final_loss": float(losses[-1]),
            "steps": float(steps),
        }

    def predict(
        self,
        state: str,
        instructions: str,
        criteria: Mapping[str, str],
    ) -> dict[str, float]:
        if not 2 <= len(criteria) <= 255:
            raise ValueError("criteria must contain 2 to 255 options")
        state_vector = _encode(f"{instructions} {state}", self.dimensions)
        cache_key = tuple((str(key), str(value)) for key, value in criteria.items())
        candidates = self._criteria_cache.setdefault(
            cache_key, self._candidate_vectors(criteria)
        )
        probabilities = _softmax(self._logits(state_vector, candidates))
        return {
            key: float(value)
            for key, value in zip(criteria, probabilities, strict=True)
        }

    def calibrate_temperature(
        self,
        examples: Iterable[DecisionTrainingExample],
    ) -> float:
        rows = tuple(examples)
        if not rows:
            raise ValueError("calibration examples cannot be empty")
        candidates = np.geomspace(0.4, 3.0, 48)
        best = min(candidates, key=lambda value: self._calibration_nll(rows, float(value)))
        self.temperature = float(best)
        return self.temperature

    def _calibration_nll(
        self, rows: tuple[DecisionTrainingExample, ...], temperature: float
    ) -> float:
        previous = self.temperature
        self.temperature = temperature
        losses = []
        for row in rows:
            probabilities = self.predict(
                row.state, row.instructions, row.criteria
            )
            losses.append(-math.log(max(probabilities[row.target], 1e-12)))
        self.temperature = previous
        return float(np.mean(losses))

    def _candidate_vectors(self, criteria: Mapping[str, str]) -> np.ndarray:
        candidates = np.stack(
            [_encode(f"{key} {description}", self.dimensions) for key, description in criteria.items()]
        )
        if self.architecture == "rival_attention":
            centered = candidates - candidates.mean(axis=0, keepdims=True)
            norms = np.linalg.norm(centered, axis=1, keepdims=True)
            candidates = centered / np.maximum(norms, 1e-12)
        return candidates

    def _logits(self, state: np.ndarray, candidates: np.ndarray) -> np.ndarray:
        return (state @ self.weight @ candidates.T) / max(self.temperature, 1e-6)


class LocalSystemOneProvider:
    def __init__(self, model: LocalDecisionModel) -> None:
        self.model = model

    def decide(self, decision: SystemOneRequest) -> SystemOneResponse:
        state = (
            decision.state
            if isinstance(decision.state, str)
            else json.dumps(decision.state, ensure_ascii=False, sort_keys=True)
        )
        answers: dict[str, DecisionAnswer] = {}
        for key, question in decision.questions.items():
            instructions = _description_text(question.instructions)
            if isinstance(question, NoulQuestion):
                criteria = {
                    "no": "the proposition is false or unsupported",
                    "yes": "the proposition is true and supported",
                }
                probabilities = self.model.predict(state, instructions, criteria)
                yes = probabilities["yes"]
                answers[key] = DecisionAnswer(
                    "noul", yes >= 0.5, probabilities, max(probabilities.values())
                )
                continue
            criteria = {
                option: _description_text(description)
                for option, description in question.criteria.items()
            }
            probabilities = self.model.predict(state, instructions, criteria)
            winner = max(probabilities, key=probabilities.get)
            if isinstance(question, ChoiceQuestion):
                value: str | float = winner
                kind = "choice"
            elif isinstance(question, ScoreQuestion):
                numeric = [_numeric_level(option, index) for index, option in enumerate(criteria)]
                value = float(sum(probabilities[key] * level for key, level in zip(criteria, numeric, strict=True)))
                kind = "score"
            else:  # pragma: no cover - closed union, retained for defensive callers
                raise TypeError(f"unsupported question: {type(question)!r}")
            answers[key] = DecisionAnswer(
                kind, value, probabilities, max(probabilities.values())
            )
        return SystemOneResponse("local-system-one", answers, {})


def _description_text(value: object) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _numeric_level(key: str, fallback: int) -> float:
    try:
        return float(key)
    except ValueError:
        return float(fallback)


def _encode(text: str, dimensions: int) -> np.ndarray:
    vector = np.zeros(dimensions, dtype=np.float64)
    for token in TOKEN.findall(text.lower()):
        digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        number = int.from_bytes(digest, "little")
        vector[number % dimensions] += 1.0 if (number >> 8) & 1 else -1.0
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - float(np.max(logits))
    values = np.exp(np.clip(shifted, -60.0, 60.0))
    return values / values.sum()


def _objective_gradient(
    probabilities: np.ndarray,
    target: np.ndarray,
    objective: str,
) -> tuple[np.ndarray, float]:
    ce_gradient = probabilities - target
    ce_loss = -float(np.sum(target * np.log(np.maximum(probabilities, 1e-12))))
    residual = probabilities - target
    expected = float(np.sum(probabilities * residual))
    brier_gradient = 2.0 * probabilities * (residual - expected)
    brier_loss = float(np.sum(residual**2))
    if objective == "cross_entropy":
        return ce_gradient, ce_loss
    if objective == "brier":
        return brier_gradient, brier_loss
    return 0.5 * (ce_gradient + brier_gradient), 0.5 * (ce_loss + brier_loss)
