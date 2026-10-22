from dataclasses import FrozenInstanceError
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from auto_research.foundation_models.deepsea import (
    ALL_LANGS, DeepSEATask, corpus_chrf2, diagnostic, extract_number, extract_option,
    extract_qa_answer, extract_summary, inspect_fixed_mgsm_archive,
    load_official_json, score_predictions, token_f1,
)


@pytest.mark.parametrize("value,expected", [
    (None, ""), ("work 2 then <answer>1,200.0</answer>", "1200"),
    ("<answer>1</answer><answer>-2.50</answer>", "-2.5"),
    ("first 3 then 12", "3"), ("not numeric", "not numeric"),
    ("1.2.3", "1.2.3"),
])
def test_numeric_extraction_preserves_fixed_release(value, expected):
    assert extract_number(value) == expected


def test_choice_extraction_prefers_first_uppercase_then_lowercase_and_last_tag():
    assert extract_option("a or B") == "B"
    assert extract_option("<answer>A</answer><answer>c</answer>") == "C"
    assert extract_option("fallback text") == "fallback text"
    assert extract_option(None) == ""


def test_qa_plain_text_is_not_silently_accepted_by_release_extractor():
    assert extract_qa_answer("plain answer text") == ""
    assert extract_qa_answer("The answer is BLUE.") == "BLUE"
    assert extract_qa_answer("<answer>ANSWER red blue ANSWER</answer>") == "red blue"
    assert extract_qa_answer("<answer>first</answer><answer>second</answer>") == "second"


def test_summary_extraction_keeps_upstream_open_tag_quirk():
    assert extract_summary("<Target_Summary>full\ntext</Target_Summary>") == "full\ntext"
    assert extract_summary("<Target_Summary>not closed") == ""
    assert extract_summary("Summary: first Summary: ignored") == "first"
    assert extract_summary("real text\n\n**extra commentary") == "real text"


def test_whitespace_token_f1_not_character_or_best_reference_oracle():
    assert token_f1("red red blue", "red blue") == pytest.approx(.8)
    assert token_f1("ภาษาไทย", "ภาษา ไทย") == 0
    assert token_f1("", "") == 1
    assert token_f1("", "x") == 0
    assert token_f1("a", "") == 0
    data = {"en": [{"context": "source", "question": "q", "answers": [{"text": "first"}, {"text": "second"}]}]}
    score = score_predictions("xquad", data, {"en": ["<answer>second</answer>"]})
    assert score["per_language"]["en"] == 0


# Independently measured against official SacreBLEU 2.5.1 CHRF(word_order=0).
# These strings are synthetic, NOT benchmark examples or benchmark answers.
@pytest.mark.parametrize("hyps,refs,expected", [
    ([""], [""], 0.0), (["abc"], [""], 0.0), ([""], ["abc"], 0.0),
    (["a"], ["a"], 100.0), (["a"], ["b"], 0.0),
    (["abcdef"], ["abc"], 75.6578947368421),
    (["ผมชอบ ภาษาไทย", "မြန်မာစာ"], ["ผมชอบภาษาไทย", "မြန်မာ စာ"], 100.0),
    (["Hello!"], ["hello"], 51.31934032983507),
    (["ab", "a"], ["abcd", "a"], 52.23880597014926),
    (["abcdef", "x"], ["", "x"], 100.0),
    (["é"], ["e\u0301"], 0.0), (["a \tb\nc"], ["abc"], 100.0),
])
def test_chrf_corpus_defaults_match_official_reference(hyps, refs, expected):
    assert corpus_chrf2(hyps, refs) == pytest.approx(expected, abs=1e-12)


def test_chrf_is_not_sentence_macro_average_and_rejects_unaligned_corpora():
    actual = corpus_chrf2(["ab", "a"], ["abcd", "a"])
    average = (corpus_chrf2(["ab"], ["abcd"])+100)/2
    assert abs(actual-average) > 1
    for hyps, refs in (([], []), (["a"], []), (["a"], ["a", "b"]), ([1], ["a"])):
        with pytest.raises(ValueError):
            corpus_chrf2(hyps, refs)


def test_all_five_tasks_have_fixed_metric_identity_and_scale():
    mgsm = score_predictions("mgsm", {"en": [{"answer": "2"}, {"answer": "3"}]}, {"en": ["2.0", "4"]})
    assert mgsm["per_language"]["en"] == 50 and mgsm["scale"] == "0..100"
    science = {"en": {"test": {"small": [{"answer": "A"}], "large": [{"answer": "B"}]*3}}}
    result = score_predictions("indommlu", science, {"en": {"small": ["A"], "large": ["A"]*3}})
    assert result["per_language"]["en"] == 50  # subject macro, not sample micro=25
    summary = score_predictions("crosssum", {"en": [{"summary": "short"}]}, {"en": ["Summary: short"]})
    translation = score_predictions("wmt24", {"en": [{"target": "short"}]}, {"en": [" short "]})
    assert summary["per_language"]["en"] == translation["per_language"]["en"] == 100
    assert translation["metric"] == "corpus_chrf2_not_metricx24"
    assert not translation["metricx_implemented"]
    with pytest.raises(NotImplementedError, match="not a substitute"):
        score_predictions("metricx-24", {}, {})


def test_tier_averages_only_when_covered_and_exclude_english():
    gold = {language: [{"answer": "9"}] for language in ALL_LANGS}
    pred = {language: ["9" if language != "en" else "0"] for language in ALL_LANGS}
    scores = score_predictions("mgsm", gold, pred)
    assert scores["tier_macro_averages"] == {"high_sea": 100., "low_sea": 100., "all_sea": 100.}
    assert score_predictions("mgsm", {"en": gold["en"]}, {"en": ["0"]})["tier_macro_averages"] == {}


@pytest.mark.parametrize("predictions", [{}, {"en": []}, {"en": ["2", "3"]}, {"en": [2]}, {"en": "2"}])
def test_missing_or_wrong_prediction_coverage_is_not_silently_zipped(predictions):
    with pytest.raises(ValueError):
        score_predictions("mgsm", {"en": [{"answer": "2"}]}, predictions)


def test_missing_subject_rejected_but_extra_predictions_ignored_like_release():
    with pytest.raises(ValueError):
        score_predictions("indommlu", {"en": {"math": [{"answer": "A"}]}}, {"en": {}})
    score = score_predictions("mgsm", {"en": [{"answer": "2"}]}, {"en": ["2"], "unused": ["ignored"]})
    assert set(score["per_language"]) == {"en"}


def test_public_projection_discards_gold_cot_optional_metadata_and_examples():
    source = {"en": {"prompt": ["sensitive demonstration"], "test": [
        {"question": "public observation", "answer": "private-answer", "answer_with_cot": "private-cot",
         "gold_plan": ["private-step"], "metadata": {"secret": "x"}}]}}
    task = DeepSEATask("mgsm", source)
    record = task.public_examples()[0]
    assert record.model_input() == {"question": "public observation"}
    assert not hasattr(record, "answer") and not hasattr(record, "_gold")
    assert "private" not in repr(record)
    source["en"]["test"][0]["question"] = "changed-source"
    assert record.model_input()["question"] == "public observation"
    changed = record.model_input()
    changed["question"] = "local mutation"
    assert record.model_input()["question"] == "public observation"
    with pytest.raises(FrozenInstanceError):
        record.language = "th"


def test_predictor_callback_receives_only_public_record_and_order_is_stable():
    source = {"en": [{"question": "first", "answer": "7"}, {"question": "second", "answer": "8"}]}
    task = DeepSEATask("mgsm", source)
    seen = []
    def predictor(record):
        seen.append((record.example_id, record.model_input()))
        assert set(record.model_input()) == {"question"}
        return "unparseable"
    result = task.evaluate_predictor(predictor)
    assert [x[0] for x in seen] == ["mgsm/en//0", "mgsm/en//1"]
    assert result["per_language"]["en"] == 0
    with pytest.raises(ValueError):
        task.evaluate_predictor(lambda record: None)


@pytest.mark.parametrize("task,data,expected", [
    ("xquad", {"en": [{"context": "ctx", "question": "q", "answers": [{"text": "hidden"}]}]}, {"context": "ctx", "question": "q"}),
    ("crosssum", {"en": [{"text": "source", "summary": "hidden"}]}, {"text": "source"}),
    ("wmt24", {"en": [{"source": "source", "target": "hidden"}]}, {"source": "source"}),
    ("indommlu", {"en": {"math": [{"question": "q", "options": ["one", "two"], "answer": "B"}]}},
     {"question": "q", "options": ["one", "two"], "subject": "math"}),
])
def test_each_task_has_an_explicit_public_field_whitelist(task, data, expected):
    assert DeepSEATask(task, data).public_examples()[0].model_input() == expected


def test_file_loader_requires_exact_content_hash_and_archive_never_extracts(tmp_path):
    data = {"en": [{"question": "synthetic", "answer": "2"}]}
    path = tmp_path / "mgsm.json"
    raw = json.dumps(data).encode()
    path.write_bytes(raw)
    loaded = load_official_json(path, "mgsm", expected_sha256=hashlib.sha256(raw).hexdigest())
    assert len(loaded.public_examples()) == 1
    for value in ("", "0"*64):
        with pytest.raises(ValueError):
            load_official_json(path, "mgsm", expected_sha256=value)
    with pytest.raises(ValueError):
        inspect_fixed_mgsm_archive(path)
    assert sorted(p.name for p in tmp_path.iterdir()) == ["mgsm.json"]


def test_diagnostic_only_reports_scorer_contracts_not_supplied_model_accuracy():
    result = diagnostic(42)
    assert all(result["checks"].values())
    assert result["metrics"]["reference_score_error"] == 0
    assert result["metrics"]["model_calls"] == 0
    assert not any("accuracy" in key or "success" in key for key in result["metrics"])
    assert result["diagnostic_only"] and not result["promotion_eligible"] and not result["evolve_integrated"]
    json.dumps(result, allow_nan=False)


def test_module_has_no_optional_import_or_model_side_effect():
    code = """
import importlib.abc,sys
class Reject(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'torch','transformers','datasets','sacrebleu'}:
            raise AssertionError(fullname)
sys.meta_path.insert(0, Reject())
from auto_research.foundation_models.deepsea import diagnostic
assert diagnostic(42)['metrics']['model_calls']==0
"""
    subprocess.run([sys.executable, "-c", code], cwd=Path(__file__).resolve().parents[1], check=True)
