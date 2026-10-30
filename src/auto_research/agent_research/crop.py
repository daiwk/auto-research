"""CROP Algorithm 1: externally evaluated textual prompt optimization.

Only the control mechanism is implemented. Every generation, critique, prompt
rewrite and validation measurement is supplied by the caller. No LLM, dataset,
gold-answer oracle, weight training or Evolve integration is provided here.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import math
import random

REQUIRES_GPU_VALIDATION = False


def _text(value: str, name: str, *, empty: bool = False) -> None:
    if not isinstance(value, str) or (not empty and not value.strip()):
        raise ValueError(f"{name} must be {'a string' if empty else 'nonempty text'}")


def _count(value: int, name: str, *, minimum: int = 0) -> None:
    if type(value) is not int or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}")


@dataclass(frozen=True)
class TrainingExample:
    example_id: str
    query: str
    reference: str

    def __post_init__(self) -> None:
        for name in ("example_id", "query", "reference"):
            _text(getattr(self, name), name)


@dataclass(frozen=True)
class Response:
    """Text and actual tokenizer/provider output-token count, not characters."""

    text: str
    tokens: int

    def __post_init__(self) -> None:
        _text(self.text, "response", empty=True)
        _count(self.tokens, "output tokens")


@dataclass(frozen=True)
class TaskFeedback:
    critique: str
    correct: bool

    def __post_init__(self) -> None:
        _text(self.critique, "task critique", empty=True)
        if type(self.correct) is not bool:
            raise ValueError("correct must be an externally evaluated Boolean")


@dataclass(frozen=True)
class OptimizerContext:
    """Appendix A.6 conversation and gradients; no reference-answer field.

    Caller-owned critics must avoid copying answers into textual feedback.
    Python callback isolation is an API boundary, not a security sandbox.
    """

    query: str
    response: Response
    task_gradient: str
    regularization_gradient: str

    @property
    def total_gradient(self) -> str:
        """Eq.3 literal newline concatenation; do not average textual gradients."""
        return self.task_gradient + "\n" + self.regularization_gradient


@dataclass(frozen=True)
class ValidationMeasurement:
    """Frozen external validation cohort, also used for the measured CoT baseline."""

    dataset_revision: str
    example_ids: tuple[str, ...]
    correct: int
    token_counts: tuple[int, ...]
    split: str = "validation"

    def __post_init__(self) -> None:
        _text(self.dataset_revision, "dataset revision")
        if self.split != "validation":
            raise ValueError("prompt selection accepts validation only, never train/test")
        if not isinstance(self.example_ids, tuple) or not self.example_ids:
            raise ValueError("nonempty immutable validation example IDs required")
        for identity in self.example_ids:
            _text(identity, "validation example ID")
        if len(set(self.example_ids)) != len(self.example_ids):
            raise ValueError("validation example IDs must be unique")
        if not isinstance(self.token_counts, tuple) or len(self.token_counts) != len(self.example_ids):
            raise ValueError("one immutable token count per validation example required")
        for count in self.token_counts:
            _count(count, "validation output tokens")
        _count(self.correct, "validation correct count")
        if self.correct > len(self.example_ids):
            raise ValueError("correct count exceeds validation cohort size")

    @property
    def accuracy(self) -> float:
        return self.correct / len(self.example_ids)

    @property
    def average_tokens(self) -> float:
        return sum(self.token_counts) / len(self.token_counts)


def tradeoff_score(measured: ValidationMeasurement, baseline: ValidationMeasurement,
                   penalty: float = .2) -> float:
    """Eq.4: accuracy - lambda * mean output tokens / mean CoT output tokens.

    The same fixed validation cohort and tokenizer/model configuration are
    required. Revision/IDs are checked; external tokenizer honesty is not.
    """
    if not isinstance(measured, ValidationMeasurement) or not isinstance(baseline, ValidationMeasurement):
        raise ValueError("external ValidationMeasurement objects required")
    if (measured.dataset_revision, measured.example_ids) != (baseline.dataset_revision, baseline.example_ids):
        raise ValueError("validation cohort/revision must match the frozen CoT baseline")
    if isinstance(penalty, bool) or not isinstance(penalty, (int, float)) or not math.isfinite(penalty) or penalty < 0:
        raise ValueError("penalty must be finite and nonnegative")
    if baseline.average_tokens <= 0:
        raise ValueError("measured CoT baseline average output tokens must be positive")
    return measured.accuracy - penalty * measured.average_tokens / baseline.average_tokens


@dataclass(frozen=True)
class Step:
    prompt: str
    contexts: tuple[OptimizerContext, ...]
    training_accuracy: float
    training_average_tokens: float
    validation: ValidationMeasurement
    score: float


@dataclass(frozen=True)
class OptimizationResult:
    best_prompt: str
    best_score: float
    steps: tuple[Step, ...]
    final_unvalidated_proposal: str


def optimize_prompt(
    initial_prompt: str,
    training_batches: Sequence[Sequence[TrainingExample]],
    *,
    generate: Callable[[str, str], Response],
    task_evaluator: Callable[[str, TrainingExample, Response], TaskFeedback],
    brevity_evaluator: Callable[[str, str, Response], str],
    optimizer: Callable[[str, tuple[OptimizerContext, ...]], str],
    validate: Callable[[str], ValidationMeasurement],
    cot_baseline: ValidationMeasurement,
    length_threshold: int,
    penalty: float = .2,
) -> OptimizationResult:
    """Execute finite pre-batched Algorithm 1 with independent validation selection.

    Caller fixes batches/budget; no unbounded retry, sampling, API or model
    defaults. Section 3.3 supplies the strict length gate omitted in pseudocode.
    Unlike Algorithm 1's on-batch monitor, candidate selection uses separate
    validation measurements (an explicit local anti-leakage strengthening).
    As in Algorithm 1, the final rewrite has not been evaluated and cannot win.
    """
    _text(initial_prompt, "initial prompt")
    _count(length_threshold, "length threshold")
    tradeoff_score(cot_baseline, cot_baseline, penalty)
    if not isinstance(training_batches, Sequence) or not training_batches:
        raise ValueError("finite nonempty pre-batched training data required")
    batches = tuple(tuple(batch) for batch in training_batches)
    validation_ids = set(cot_baseline.example_ids)
    for batch in batches:
        if not batch or any(not isinstance(row, TrainingExample) for row in batch):
            raise ValueError("each training batch must contain TrainingExample objects")
        if len({row.example_id for row in batch}) != len(batch):
            raise ValueError("duplicate training IDs within a batch")
        if any(row.example_id in validation_ids for row in batch):
            raise ValueError("training and validation example IDs must be disjoint")
    callbacks = (generate, task_evaluator, brevity_evaluator, optimizer, validate)
    if any(not callable(callback) for callback in callbacks):
        raise ValueError("all model/evaluator/optimizer operations require external callbacks")
    prompt, best_prompt, best_score = initial_prompt, initial_prompt, -math.inf
    steps = []
    for batch in batches:
        contexts, correct, total_tokens = [], 0, 0
        for example in batch:
            response = generate(prompt, example.query)  # Never pass reference to the target.
            if not isinstance(response, Response):
                raise ValueError("generate must return Response with measured token count")
            feedback = task_evaluator(prompt, example, response)
            if not isinstance(feedback, TaskFeedback):
                raise ValueError("task evaluator must return TaskFeedback")
            regularization = ""
            if response.tokens > length_threshold:
                regularization = brevity_evaluator(prompt, example.query, response)
                _text(regularization, "brevity critique", empty=True)
            contexts.append(OptimizerContext(example.query, response, feedback.critique, regularization))
            correct += feedback.correct
            total_tokens += response.tokens
        measured = validate(prompt)  # Never expose validation examples/answers to optimizer.
        score = tradeoff_score(measured, cot_baseline, penalty)
        steps.append(Step(prompt, tuple(contexts), correct / len(batch), total_tokens / len(batch), measured, score))
        if score > best_score:  # Strict tie: retain earlier validated prompt.
            best_prompt, best_score = prompt, score
        prompt = optimizer(prompt, tuple(contexts))
        _text(prompt, "optimizer proposal")
    return OptimizationResult(best_prompt, best_score, tuple(steps), prompt)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Deterministic callback doubles test control flow, not LLM capability."""
    _count(seed, "seed")
    if device != "cpu":
        raise ValueError("pure CPU control diagnostic; no GPU/model execution")
    queries = [TrainingExample("train-long", "long-input", "HIDDEN-REFERENCE-A"),
               TrainingExample("train-short", "short-input", "HIDDEN-REFERENCE-B")]
    random.Random(seed).shuffle(queries)
    baseline = ValidationMeasurement("generated-contract-v1", ("val-1", "val-2"), 2, (20, 20))
    brevity_calls, optimizer_views = [], []

    def generate(prompt, query):
        return Response("generated diagnostic response", 12 if query == "long-input" else 4)

    def task_evaluator(prompt, example, response):
        return TaskFeedback("preserve essential calculation", True)

    def brevity_evaluator(prompt, query, response):
        brevity_calls.append(query)
        return "remove peripheral narrative gradually"

    def optimizer(prompt, contexts):
        optimizer_views.append(repr(contexts))
        return "concise" if prompt == "initial" else "unmeasured-final"

    def validate(prompt):
        counts = (20, 20) if prompt == "initial" else (8, 8)
        return ValidationMeasurement(baseline.dataset_revision, baseline.example_ids, 2, counts)

    result = optimize_prompt("initial", (queries, queries), generate=generate,
                             task_evaluator=task_evaluator, brevity_evaluator=brevity_evaluator,
                             optimizer=optimizer, validate=validate, cot_baseline=baseline,
                             length_threshold=4)
    first = result.steps[0]
    return {"seed": seed, "diagnostic_only": True, "component": "crop_textual_prompt_control",
            "metrics": {"evaluated_prompt_count": len(result.steps),
                        "brevity_callback_count": len(brevity_calls),
                        "reference_normalized_score": result.best_score,
                        "reference_normalized_length": result.steps[1].validation.average_tokens / baseline.average_tokens},
            "checks": {"strict_length_gate": brevity_calls == ["long-input", "long-input"],
                       "literal_gradient_concatenation": all(c.total_gradient == c.task_gradient + "\n" + c.regularization_gradient for c in first.contexts),
                       "validated_prompt_selected": result.best_prompt == "concise",
                       "unvalidated_final_not_selected": result.final_unvalidated_proposal == "unmeasured-final" and result.best_prompt != result.final_unvalidated_proposal,
                       "score_matches_equation4": math.isclose(result.best_score, .92),
                       "optimizer_reference_field_absent": all("HIDDEN-REFERENCE" not in view for view in optimizer_views),
                       "callback_doubles_not_capability": True}}
