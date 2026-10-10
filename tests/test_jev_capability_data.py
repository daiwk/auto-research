import hashlib
import json

import pytest

from auto_research.system_one.capability_data import (
    DATASETS, ExcludedItem, load_capability_data, normalize_item,
)


@pytest.mark.parametrize("benchmark,row", [
    ("mmlu", {"question": "q", "choices": ["x", "y"], "answer": 1}),
    ("mmlu-redux", {"question": "q", "choices": ["x", "y", "z", "w"],
                    "answer": 0, "error_type": "wrong_groundtruth", "correct_answer": "1"}),
    ("mmlu-pro", {"question": "q", "options": ["x", "y"], "answer": "B"}),
    ("mmlu-prox", {"question": "q", **{f"option_{i}": str(i) for i in range(10)},
                   "answer": "B", "cot_content": "SECRET"}),
    ("mmmlu", {"Question": "q", "A": "x", "B": "y", "C": "z", "D": "w", "Answer": "B"}),
    ("c-eval", {"question": "q", "A": "x", "B": "y", "C": "z", "D": "w", "answer": "B"}),
    ("hellaswag", {"ctx": "q", "endings": ["x", "y"], "label": "1"}),
    ("winogrande", {"sentence": "q _", "option1": "x", "option2": "y", "answer": "2"}),
    ("truthfulqa", {"question": "q", "mc1_targets": {"choices": ["x", "y"], "labels": [0, 1]}}),
    ("arc-challenge", {"question": "q", "choices": {"label": ["1", "B"], "text": ["x", "y"]},
                       "answerKey": "B"}),
    ("mathqa", {"Problem": "q", "options": "a ) 1,000, b ) y, c ) z, d ) w, e ) v",
                "correct": "b", "Rationale": "SECRET"}),
    ("aqua-rat", {"question": "q", "options": ["A)x", "B)y"], "correct": "B", "rationale": "SECRET"}),
])
def test_public_schemas_no_reference_context(benchmark, row):
    item = normalize_item(benchmark, row, language="en")
    assert item.target == "B"
    assert "SECRET" not in str(item.request().to_dict())
    assert item.options["B"] == "y" or benchmark == "mmlu-prox"


def test_gpqa_randomization_and_exclusions_are_explicit():
    row = {"Question": "q", "Correct Answer": "good", **{
        f"Incorrect Answer {i}": f"wrong{i}" for i in range(1, 4)
    }}
    targets = set()
    for i in range(20):
        item = normalize_item("gpqa-diamond", row, index=i)
        assert item.options[item.target] == "good"
        assert item == normalize_item("gpqa-diamond", row, index=i)
        targets.add(item.target)
    assert targets == set("ABCD")
    with pytest.raises(ExcludedItem, match="not publicly labeled"):
        normalize_item("c-eval", {"question": "q", **dict.fromkeys("ABCD", "x")})
    with pytest.raises(ExcludedItem, match="ambiguous"):
        normalize_item("mmlu-redux", {"question": "q", "choices": ["x", "y"],
                                       "answer": 0, "error_type": "no_correct_answer"})


def test_source_hash_and_labels_are_checked(tmp_path):
    path = tmp_path / "arc.jsonl"
    raw = json.dumps({"identifier": "arc:x", "benchmark": "arc-challenge", "question": "q",
                      "options": {"A": "x", "B": "y"}, "target": "B", "language": "en"}) + "\n"
    path.write_text(raw)
    source = {"dataset_id": DATASETS["arc-challenge"], "revision": "a" * 40,
              "benchmark": "arc-challenge", "language": "en", "examples": 1,
              "sha256": hashlib.sha256(raw.encode()).hexdigest()}
    path.with_suffix(".jsonl.source.json").write_text(json.dumps(source))
    items, sources = load_capability_data([path])
    assert items[0].target == "B" and sources == [source]
    path.write_text(raw.replace('"target": "B"', '"target": "A"'))
    with pytest.raises(ValueError, match="source receipt"):
        load_capability_data([path])
