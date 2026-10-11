import importlib.util
from pathlib import Path

import pytest
import hashlib
import json

from auto_research.public_holdout import validate_holdout

spec = importlib.util.spec_from_file_location("split_public", Path(__file__).parents[1] / "scripts/split_public_training_jsonl.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_holdout_is_deterministic_deduplicated_and_disjoint():
    rows = [{"question": f"Question {i}", "answer": str(i)} for i in range(100)]
    a, b = module.split_rows(rows + rows)
    c, d = module.split_rows(list(reversed(rows)))
    assert {r["question"] for r in a} == {r["question"] for r in c}
    assert {r["question"] for r in b} == {r["question"] for r in d}
    assert not {r["question"] for r in a} & {r["question"] for r in b}
    assert len(a) + len(b) == 100
    with pytest.raises(ValueError, match="conflicting"):
        module.split_rows(rows + [{"question": "Question 0", "answer": "wrong"}])


def test_holdout_claim_requires_manifest_bound_to_actual_files(tmp_path):
    train, valid = tmp_path / "train.jsonl", tmp_path / "validation.jsonl"
    train.write_text(json.dumps({"question": "A", "answer": "1"}) + "\n")
    valid.write_text(json.dumps({"question": "B", "answer": "2"}) + "\n")
    assert validate_holdout(None, train, valid, dataset_revision="abc")["test_read"] is None
    record = {"source_split": "train", "test_opened": False, "source_revision": "abc",
              "source_id": "public/data", "source_sha256": "source-hash", "partition": "holdout",
              "counts": {"train": 1, "validation": 1},
              "partition_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest()
                                   for name, path in (("train", train), ("validation", valid))}}
    manifest = tmp_path / "split.json"
    manifest.write_text(json.dumps(record))
    assert validate_holdout(manifest, train, valid, dataset_revision="abc")["verified"]
    valid.write_text(json.dumps({"question": "C", "answer": "3"}) + "\n")
    with pytest.raises(ValueError, match="digest"):
        validate_holdout(manifest, train, valid, dataset_revision="abc")
