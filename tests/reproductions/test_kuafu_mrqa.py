import gzip
import json

import pytest

from auto_research.reproductions.kuafu.mrqa import load_mrqa, validate_disjoint_qids


def test_official_mrqa_parser_keeps_item_chunks_and_answers(tmp_path):
    path = tmp_path / "SQuAD.jsonl.gz"
    rows = [
        {"header": {"dataset": "SQuAD", "split": "train"}},
        {"context": "First fact. [PAR] Second fact about Berlin.",
         "qas": [{"qid": "q1", "question": "Which city?", "answers": ["Berlin"]}]},
    ]
    with gzip.open(path, "wt", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row) + "\n")
    records = load_mrqa(path, expected_split="train")
    assert len(records) == 1
    assert records[0].qid == "q1"
    assert records[0].items == ("First fact.", "Second fact about Berlin.")
    assert records[0].answers == ("Berlin",)
    with pytest.raises(ValueError, match="split"):
        load_mrqa(path, expected_split="dev")


def test_public_data_splits_must_not_reuse_questions():
    from auto_research.reproductions.kuafu.mrqa import MRQAExample

    train = [MRQAExample("same", ("a",), "?", ("a",))]
    dev = [MRQAExample("same", ("b",), "?", ("b",))]
    with pytest.raises(ValueError, match="overlap"):
        validate_disjoint_qids(train, dev)


def test_mrqa_sampling_can_limit_one_question_per_source(tmp_path):
    path = tmp_path / "train.jsonl.gz"
    with gzip.open(path, "wt", encoding="utf-8") as stream:
        stream.write(json.dumps({"header": {"split": "train"}}) + "\n")
        for index in range(2):
            stream.write(json.dumps({
                "context": f"Context {index}",
                "qas": [
                    {"qid": f"{index}-a", "question": "A?", "answers": ["A"]},
                    {"qid": f"{index}-b", "question": "B?", "answers": ["B"]},
                ],
            }) + "\n")
    records = load_mrqa(path, expected_split="train", one_per_context=True)
    assert [record.qid for record in records] == ["0-a", "1-a"]
