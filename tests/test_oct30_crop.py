from dataclasses import FrozenInstanceError, fields
import hashlib
import json
import math
from pathlib import Path
import re

import pytest

from auto_research.agent_research.crop import (
    OptimizerContext, Response, TaskFeedback, TrainingExample,
    ValidationMeasurement, diagnostic, optimize_prompt, tradeoff_score,
)


def measurement(correct=2, tokens=(20, 20), **kwargs):
    return ValidationMeasurement("fixed-v1", ("val-a", "val-b"), correct, tokens, **kwargs)


def run(**overrides):
    calls = {"generate": [], "brevity": [], "optimizer": []}
    def generate(prompt, query):
        calls["generate"].append((prompt, query))
        return Response("model output", 5 if query == "long" else 4)
    def brevity(prompt, query, response):
        calls["brevity"].append(query)
        return "trim filler, retain calculation"
    def optimizer(prompt, contexts):
        calls["optimizer"].append(contexts)
        return "candidate" if prompt == "initial" else "unvalidated"
    arguments = dict(generate=generate,
                     task_evaluator=lambda p, row, out: TaskFeedback("task feedback", True),
                     brevity_evaluator=brevity, optimizer=optimizer,
                     validate=lambda p: measurement(tokens=(20, 20) if p == "initial" else (8, 8)),
                     cot_baseline=measurement(), length_threshold=4)
    arguments.update(overrides)
    batches = ((TrainingExample("train-a", "long", "PRIVATE GOLD A"),
                TrainingExample("train-b", "short", "PRIVATE GOLD B")),) * 2
    return optimize_prompt("initial", batches, **arguments), calls


def test_gate_concatenation_and_gold_free_target_optimizer_views():
    result, calls = run()
    assert calls["brevity"] == ["long", "long"]
    assert all(len(args) == 2 for args in calls["generate"])
    assert "PRIVATE GOLD" not in repr(calls)
    context_fields = {field.name for field in fields(OptimizerContext)}
    assert "reference" not in context_fields
    long, short = result.steps[0].contexts
    assert long.total_gradient == "task feedback\ntrim filler, retain calculation"
    assert short.total_gradient == "task feedback\n"
    assert result.best_prompt == "candidate"
    assert result.best_score == pytest.approx(.92)
    assert result.final_unvalidated_proposal == "unvalidated"
    assert result.steps[0].training_average_tokens == 4.5
    assert result.steps[0].training_accuracy == 1
    with pytest.raises(FrozenInstanceError):
        long.query = "mutated"


def test_selection_is_validation_not_training_accuracy_or_final_iteration():
    result, _ = run(validate=lambda p: measurement(correct=2 if p == "initial" else 1, tokens=(20, 20)))
    assert result.best_prompt == "initial"
    assert result.steps[0].training_accuracy == result.steps[1].training_accuracy == 1
    assert result.final_unvalidated_proposal not in {step.prompt for step in result.steps}


def test_equal_validation_score_keeps_earlier_prompt():
    result, _ = run(validate=lambda p: measurement())
    assert result.best_prompt == "initial"


def test_exact_normalization_uses_mean_not_total_or_character_count():
    assert tradeoff_score(measurement(1, (5, 15)), measurement()) == pytest.approx(.4)
    assert tradeoff_score(measurement(1, (0, 0)), measurement(), 0) == .5


@pytest.mark.parametrize("split", ["train", "test", "held-out", "Validation"])
def test_rejects_non_validation_selection(split):
    with pytest.raises(ValueError, match="validation only"):
        measurement(split=split)


@pytest.mark.parametrize("measured", [
    ValidationMeasurement("changed", ("val-a", "val-b"), 2, (20, 20)),
    ValidationMeasurement("fixed-v1", ("val-b", "val-a"), 2, (20, 20)),
    ValidationMeasurement("fixed-v1", ("other",), 1, (20,)),
])
def test_rejects_cohort_or_revision_changes(measured):
    with pytest.raises(ValueError, match="cohort/revision"):
        tradeoff_score(measured, measurement())


@pytest.mark.parametrize("penalty", [-1, math.inf, math.nan, True, "0.2"])
def test_rejects_bad_penalty(penalty):
    with pytest.raises(ValueError, match="penalty"):
        tradeoff_score(measurement(), measurement(), penalty)


@pytest.mark.parametrize("tokens", [(-1, 2), (True, 2), (1.5, 2), (1,), [1, 2]])
def test_rejects_invalid_validation_token_counts(tokens):
    with pytest.raises(ValueError):
        measurement(tokens=tokens)


def test_rejects_zero_baseline_and_training_validation_overlap():
    with pytest.raises(ValueError, match="positive"):
        tradeoff_score(measurement(), measurement(tokens=(0, 0)))
    with pytest.raises(ValueError, match="disjoint"):
        optimize_prompt("initial", ((TrainingExample("val-a", "x", "gold"),),),
                        generate=None, task_evaluator=None, brevity_evaluator=None,
                        optimizer=None, validate=None, cot_baseline=measurement(), length_threshold=4)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_only_contract(seed):
    result = diagnostic(seed)
    assert result["diagnostic_only"] is True
    assert all(result["checks"].values())
    assert result["metrics"]["reference_normalized_score"] == pytest.approx(.92)
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, "cuda")


@pytest.mark.parametrize("overrides", [
    {"generate": lambda p, q: "fabricated string without token count"},
    {"task_evaluator": lambda p, row, out: "untyped feedback"},
    {"brevity_evaluator": lambda p, q, out: None},
    {"optimizer": lambda p, contexts: ""},
    {"validate": lambda p: {"accuracy": 1}},
    {"length_threshold": True},
])
def test_callback_boundary_fails_closed(overrides):
    with pytest.raises(ValueError):
        run(**overrides)


def test_paper_metadata_figure_and_four_level_authored_questions():
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / "src/auto_research/paper_specs/catalog/agent-research/crop.json").read_text())
    assert spec["published_at"] == "2026-04-08T19:31:25Z"
    assert spec["intake_class"] == "historical_backfill"
    assert spec["code"] is None and spec["code_status"]
    assert spec["adapter"] is None and spec["evolve_integrated"] is False
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert spec["requires_gpu_validation"] is False
    path = root / "docs" / spec["detail_path"]
    text = path.read_text()
    assert "2026-04-08 19:31:25 UTC" in text
    assert "原作者代码" in text and "本地复现代码" in text
    headings = set(re.findall(r"^#{1,6} (.+)$", text, flags=re.MULTILINE))
    bank = json.loads((root / "docs/learning/questions/oct30-priority.json").read_text())
    questions = bank["papers"]["agent-research:crop"]["questions"]
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    assert all(q["question"] and q["answer"] and q["example"] for q in questions)
    assert all(set(q["source_sections"]) <= headings for q in questions)
    provenance = json.loads((path.parent / "assets/provenance.json").read_text())
    image = path.parent / "assets" / provenance["local_path"]
    assert hashlib.sha256(image.read_bytes()).hexdigest() == provenance["sha256"]
