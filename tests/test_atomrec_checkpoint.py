import gzip
import json

from auto_research.agent_research.atomrec_checkpoint import product_cases, rank


def test_product_memory_excludes_target_and_future(tmp_path):
    with gzip.open(tmp_path / "reviews_Beauty_5.json.gz", "wt") as stream:
        for user, sequence in (("a", ["a", "b", "c", "d", "e"]),
                               ("b", ["d", "e", "a", "b", "c"])):
            for index, item in enumerate(sequence):
                stream.write(json.dumps({"reviewerID": user, "asin": item, "unixReviewTime": index + 1}) + "\n")
    with gzip.open(tmp_path / "meta_Beauty.json.gz", "wt") as stream:
        for item in "abcde":
            stream.write(repr({"asin": item, "title": item, "related": {"also_bought": ["hidden"]}}) + "\n")
    cases, metadata, hashes = product_cases(tmp_path, users=1)
    assert len(hashes) == 2
    assert [case["target"] for case in cases] == ["d", "e"]
    for case in cases:
        assert case["target"] not in case["seen"]
        assert all(stamp < case["timestamp"] for stamp, _ in case["history"])
    assert all("related" not in item for item in metadata.values())


def test_ranker_scores_every_candidate_without_a_gold_label():
    seen = []

    def encode(text):
        assert "target" not in text and "correct" not in text
        seen.append(text)
        return __import__("numpy").array([
            0.0 if "public evidence" in text else 1.0,
            1.0 if ("public evidence" in text or "preferred" in text) else 0.0,
        ])

    ranking = rank(encode, "public evidence", [
        {"id": "a", "title": "ordinary"}, {"id": "b", "title": "preferred"},
    ])
    assert ranking == ["b", "a"]
    assert len(seen) == 3
