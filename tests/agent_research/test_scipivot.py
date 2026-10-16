import json
from pathlib import Path

import pytest

from auto_research.agent_research.scipivot import (
    PublicCase, audit_release, export_options_only, parse_choice, partition_release,
    score_predictions,
)

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "docs/agent-research/2610.21082-scipivot/validation/upstream"


def test_real_release_and_official_aggregate_arithmetic():
    result = audit_release(UPSTREAM / "questions.json", UPSTREAM / "all_model_scores.csv")
    assert result["cases"] == 248 and result["planned_options_only_runs"] == 496
    assert result["aggregate_rows_validated"] == 60
    assert result["new_model_evaluated"] is False
    assert result["model_accuracy_recomputed_from_predictions"] is False
    medium = {r["model"]: r for r in result["official_medium_options_only"]}
    assert medium["gpt-6-astra"]["correct"] == 316
    assert medium["gpt-5.6-sol"]["correct"] == 232


def test_public_projection_cannot_carry_reference_or_extra_gold_fields(tmp_path):
    rows = [{"id": "case", "options": {"A": "option one", "B": "option two"},
             "reference_answer": "B", "gold_plan": "NEVER EXPOSE", "project": "private history"}]
    public, refs = partition_release(rows)
    assert public == (PublicCase("case", "option one", "option two"),)
    assert refs == {"case": "B"}
    result = export_options_only(rows, tmp_path / "public", tmp_path / "grader")
    prompts = (tmp_path / "public/prompts.jsonl").read_text()
    assert not any(word in prompts for word in ("NEVER EXPOSE", "reference_answer", "private history"))
    a, b = [json.loads(line) for line in prompts.splitlines()]
    assert "(A) option one" in a["prompt"] and "(A) option two" in b["prompt"]
    assert result["evaluator_executed"] is False
    assert (tmp_path / "grader/references.json").stat().st_mode & 0o777 == 0o600
    with pytest.raises(FileExistsError):
        export_options_only(rows, tmp_path / "public", tmp_path / "grader")
    with pytest.raises(ValueError, match="disjoint"):
        export_options_only(rows, tmp_path / "x", tmp_path / "x/private")


@pytest.mark.parametrize("value", [None, "A and B", '{"response":"A"} trailing',
                                    '{"response":"A","response":"B"}', '{"response":"AB"}'])
def test_strict_parser_rejects_ambiguous_outputs(value):
    assert parse_choice(value) is None


def test_case_equal_weight_both_orders_missing_timeout_and_truncation():
    refs = {"one": "A", "two": "B", "missing": "A"}
    predictions = [{"id": "one", "order": "ab", "response": "A"},
                   {"id": "one", "order": "ba", "response": '{"response":"B"}'},
                   {"id": "two", "order": "ab", "response": "B", "status": "timeout"},
                   {"id": "two", "order": "ba", "response": "A", "status": "truncated"}]
    result = score_predictions(refs, predictions, resamples=100, seed=42)
    assert result["accuracy"] == pytest.approx(1 / 3)
    assert result["planned_runs"] == 6 and result["missing_runs"] == 2
    assert result["invalid_observed_runs"] == 2
    assert result["case_scores"] == [0, 1, 0]
    assert result["bootstrap"]["unit"] == "case"
    assert result == score_predictions(refs, predictions, resamples=100, seed=42)
    with pytest.raises(ValueError, match="duplicate"):
        score_predictions(refs, predictions + predictions[:1])
    with pytest.raises(ValueError, match="outside"):
        score_predictions(refs, [{"id": "one", "order": "xx"}])


def test_one_observed_order_does_not_shrink_denominator():
    result = score_predictions({"case": "A"}, [{"id": "case", "order": "ab", "response": "A"}], resamples=10)
    assert result["accuracy"] == .5
    assert result["missing_runs"] == 1
