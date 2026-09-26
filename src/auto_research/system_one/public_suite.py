"""Strict loader and metrics for public Choice, Noul and Score decisions."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping

import numpy as np

from .contracts import ChoiceQuestion, NoulQuestion, ScoreQuestion, SystemOneRequest


@dataclass(frozen=True)
class PublicDecisionExample:
    id: str
    domain: str
    family: str
    request: SystemOneRequest
    question_id: str
    target: str | bool | int
    split: str = "legacy"
    source: str = "unknown"


@dataclass(frozen=True)
class PublicDecisionSplits:
    calibration: tuple[PublicDecisionExample, ...]
    test: tuple[PublicDecisionExample, ...]
    ood: tuple[PublicDecisionExample, ...] = ()


def load_public_decisions(path: Path) -> tuple[PublicDecisionExample, ...]:
    """Load the Nimble-compatible JSONL format without exposing references."""
    rows: list[PublicDecisionExample] = []
    ids: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        raw = json.loads(line)
        if not isinstance(raw, Mapping):
            raise ValueError(f"line {line_number}: record must be an object")
        inputs, reference = raw.get("input"), raw.get("reference")
        if not isinstance(inputs, Mapping) or not isinstance(reference, Mapping):
            raise ValueError(f"line {line_number}: input/reference must be objects")
        lowered = json.dumps(inputs, ensure_ascii=False).lower()
        if any(key in lowered for key in ('"target"', '"answer"', '"label"', '"gold"')):
            raise ValueError(f"line {line_number}: input may not contain gold fields")
        questions = inputs.get("questions")
        if not isinstance(questions, Mapping) or len(questions) != 1:
            raise ValueError(f"line {line_number}: exactly one question is required")
        question_id, spec = next(iter(questions.items()))
        if not isinstance(spec, Mapping):
            raise ValueError(f"line {line_number}: question must be an object")
        kind = str(spec.get("type", "")).lower()
        instructions = spec.get("instructions")
        criteria = spec.get("criteria")
        target = reference.get("target")
        if kind == "choice":
            if not isinstance(criteria, Mapping):
                raise ValueError(f"line {line_number}: choice criteria must be an object")
            question = ChoiceQuestion(instructions, criteria)
            target = str(target)
            if target not in criteria:
                raise ValueError(f"line {line_number}: choice target is not a criterion")
        elif kind in {"noul", "boolean"}:
            question = NoulQuestion(instructions)
            if not isinstance(target, bool):
                raise ValueError(f"line {line_number}: Noul target must be boolean")
        elif kind == "score":
            if isinstance(criteria, list):
                criteria = {str(index): value for index, value in enumerate(criteria)}
            if not isinstance(criteria, Mapping):
                raise ValueError(f"line {line_number}: score criteria must be ordered")
            question = ScoreQuestion(instructions, criteria)
            if isinstance(target, str) and target in criteria:
                target = list(criteria).index(target)
            if not isinstance(target, int) or not 0 <= target < len(criteria):
                raise ValueError(f"line {line_number}: score target is out of range")
        else:
            raise ValueError(f"line {line_number}: unsupported question type {kind!r}")
        row_id = str(raw.get("id", f"line-{line_number}"))
        if row_id in ids:
            raise ValueError(f"line {line_number}: duplicate public decision id {row_id!r}")
        ids.add(row_id)
        rows.append(PublicDecisionExample(
            id=row_id,
            domain=str(raw.get("domain", "unknown")),
            family=str(raw.get("family", raw.get("source_family", "unknown"))),
            request=SystemOneRequest(inputs.get("state", ""), {str(question_id): question}),
            question_id=str(question_id),
            target=target,
            split=str(raw.get("split", "legacy")),
            source=str(raw.get("source", raw.get("family", "unknown"))),
        ))
    if not rows:
        raise ValueError("public decision suite is empty")
    return tuple(rows)


def load_public_decision_splits(path: Path) -> PublicDecisionSplits:
    """Load explicit benchmark splits, with legacy family split compatibility."""
    manifest_path = path.with_suffix(".manifest.json")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != manifest.get("dataset_sha256"):
            raise ValueError("public decision suite SHA256 does not match manifest")
    rows = load_public_decisions(path)
    explicit = {row.split for row in rows if row.split != "legacy"}
    if not explicit:
        calibration, test = split_public_decisions(rows)
        return PublicDecisionSplits(calibration, test)
    unknown = {row.split for row in rows} - {"calibration", "test", "ood"}
    if unknown:
        raise ValueError(f"unsupported public decision splits: {sorted(unknown)}")
    calibration = tuple(row for row in rows if row.split == "calibration")
    test = tuple(row for row in rows if row.split == "test")
    ood = tuple(row for row in rows if row.split == "ood")
    if not calibration or not test:
        raise ValueError("formal public suite requires non-empty calibration and test splits")
    return PublicDecisionSplits(calibration, test, ood)


def split_public_decisions(
    rows: tuple[PublicDecisionExample, ...], validation_fraction: float = 0.5
) -> tuple[tuple[PublicDecisionExample, ...], tuple[PublicDecisionExample, ...]]:
    """Split by complete source family, deterministically, to prevent leakage."""
    if not 0 < validation_fraction < 1:
        raise ValueError("validation_fraction must be in (0, 1)")
    families = sorted({row.family for row in rows})
    if len(families) < 2:
        midpoint = max(1, len(rows) // 2)
        return rows[:midpoint], rows[midpoint:] or rows[:midpoint]
    count = min(len(families) - 1, max(1, round(len(families) * validation_fraction)))
    validation_families = set(families[:count])
    return (
        tuple(row for row in rows if row.family in validation_families),
        tuple(row for row in rows if row.family not in validation_families),
    )


def evaluate_public_decisions(
    provider: Any,
    examples: tuple[PublicDecisionExample, ...],
    confidence_threshold: float,
) -> dict[str, Any]:
    confidences: list[float] = []
    correct: list[float] = []
    nlls: list[float] = []
    briers: list[float] = []
    score_errors: list[float] = []
    by_type: dict[str, list[float]] = {}
    by_domain: dict[str, list[float]] = {}
    for row in examples:
        answer = provider.decide(row.request).answers[row.question_id]
        labels = list(answer.probabilities)
        if answer.type == "noul":
            expected = "yes" if row.target else "no"
            predicted = "yes" if bool(answer.value) else "no"
        elif answer.type == "score":
            target_index = int(row.target)
            expected = labels[target_index]
            predicted = max(answer.probabilities, key=answer.probabilities.get)
            score_errors.append(abs(float(answer.value) - float(target_index)))
        else:
            expected = str(row.target)
            predicted = str(answer.value)
        hit = float(predicted == expected)
        probability = max(float(answer.probabilities[expected]), 1e-12)
        confidences.append(float(answer.confidence))
        correct.append(hit)
        nlls.append(-math.log(probability))
        briers.append(sum(
            (float(value) - float(label == expected)) ** 2
            for label, value in answer.probabilities.items()
        ))
        by_type.setdefault(answer.type, []).append(hit)
        by_domain.setdefault(row.domain, []).append(hit)
    confidence = np.asarray(confidences)
    correctness = np.asarray(correct)
    accepted = confidence >= confidence_threshold
    return {
        "accuracy": float(correctness.mean()),
        "nll": float(np.mean(nlls)),
        "brier": float(np.mean(briers)),
        "ece": _expected_calibration_error(confidence, correctness),
        "coverage": float(accepted.mean()),
        "selective_accuracy": float(correctness[accepted].mean()) if accepted.any() else 0.0,
        "score_mae": float(np.mean(score_errors)) if score_errors else 0.0,
        "schema_validity": 1.0,
        "evaluated_examples": float(len(examples)),
        "by_type": {key: float(np.mean(values)) for key, values in sorted(by_type.items())},
        "by_domain": {key: float(np.mean(values)) for key, values in sorted(by_domain.items())},
        "worst_type_accuracy": min(float(np.mean(values)) for values in by_type.values()),
        "worst_domain_accuracy": min(float(np.mean(values)) for values in by_domain.values()),
    }


def _expected_calibration_error(
    confidence: np.ndarray, correctness: np.ndarray, bins: int = 10
) -> float:
    error = 0.0
    edges = np.linspace(0.0, 1.0, bins + 1)
    for index in range(bins):
        lower, upper = edges[index], edges[index + 1]
        mask = (confidence >= lower) & (
            confidence <= upper if index == bins - 1 else confidence < upper
        )
        if mask.any():
            error += float(mask.mean()) * abs(
                float(correctness[mask].mean()) - float(confidence[mask].mean())
            )
    return error
