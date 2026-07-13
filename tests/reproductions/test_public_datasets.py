import gzip
import json

from auto_research.datasets import amazon_beauty_5core, mdcns_beauty_sequences
from auto_research.reproductions.mdcns.experiment import build_beauty_sequences


def test_amazon_beauty_reads_cached_public_records(tmp_path):
    target = tmp_path / "amazon-beauty-5core" / "reviews_Beauty_5.json.gz"
    target.parent.mkdir(parents=True)
    record = {
        "reviewerID": "u1",
        "asin": "i1",
        "overall": 5.0,
        "unixReviewTime": 123,
    }
    with gzip.open(target, "wt", encoding="utf-8") as stream:
        stream.write(json.dumps(record) + "\n")
    assert amazon_beauty_5core(tmp_path, allow_network=False) == [
        ("u1", "i1", 5.0, 123)
    ]


def test_mdcns_author_split_is_loaded_without_network(tmp_path):
    directory = tmp_path / "mdcns-beauty"
    directory.mkdir(parents=True)
    (directory / "Beauty_train.txt").write_text("1 2\n2 3\n", encoding="utf-8")
    (directory / "Beauty_val.txt").write_text("1 2 3\n", encoding="utf-8")
    (directory / "Beauty_test.txt").write_text("1 2 4\n", encoding="utf-8")
    sequences = mdcns_beauty_sequences(tmp_path, allow_network=False)
    train, test, seen, item_count = build_beauty_sequences(sequences, seed=7)
    assert train == [(1, 2), (2, 3)]
    assert test == [(2, 4)]
    assert seen == {0: {1, 2}}
    assert item_count == 5
