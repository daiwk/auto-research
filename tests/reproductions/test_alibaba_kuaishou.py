import pytest

from auto_research.reproductions.base import PaperMetadata
from auto_research.reproductions.m6rec.model import (
    M6RecConfig,
    binary_auc,
    movielens_text_examples,
)
from auto_research.reproductions.onerec_v2.model import (
    OneRecV2Config,
    load_kuairand_examples,
)


def test_m6rec_builds_plain_text_chronological_examples(tmp_path):
    directory = tmp_path / "ml-100k"
    directory.mkdir()
    flags = "|".join(["1", *(["0"] * 18)])
    (directory / "u.item").write_text(
        "\n".join(f"{item}|Movie {item}|01-Jan-1995||url|{flags}" for item in range(1, 4)) + "\n",
        encoding="latin-1",
    )
    rows = []
    sequence = [(1, 5), (2, 1), (3, 5), (2, 2), (3, 4), (1, 1)]
    for user in (1, 2):
        rows.extend(f"{user}\t{item}\t{rating}\t{user * 100 + step}" for step, (item, rating) in enumerate(sequence))
    (directory / "u.data").write_text("\n".join(rows) + "\n")
    train, test = movielens_text_examples(tmp_path, M6RecConfig(maximum_examples=80))
    assert train and test
    assert "User recently liked:" in train[0][0]
    assert "Candidate item:" in train[0][0]
    assert {label for _, label in train} == {0, 1}


def test_auc_is_one_for_perfect_ranking():
    assert binary_auc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]) == 1.0


def test_catalogued_industrial_paper_requires_online_ab_evidence():
    paper = PaperMetadata(
        arxiv_id="fixture", title="No live test", url="https://example.com",
        track="recommendation", organization="Example", published="2026-07",
    )
    with pytest.raises(ValueError, match="no quantified online A/B"):
        paper.validate_catalog_entry()


def test_onerec_v2_uses_real_duration_feedback_and_catalog_valid_sids(tmp_path):
    directory = tmp_path / "kuairand-pure" / "data"
    directory.mkdir(parents=True)
    (directory / "video_features_basic_pure.csv").write_text(
        "video_id,author_id,tag,video_duration\n"
        "0,10,fun,10000\n1,11,sport,20000\n2,12,fun,30000\n3,13,music,40000\n"
    )
    header = "user_id,video_id,time_ms,duration_ms,play_time_ms,is_hate\n"
    rows = []
    for user in (0, 1):
        for step in range(14):
            rows.append(f"{user},{step % 4},{user * 100 + step},{10000 * (step % 4 + 1)},{1000 * step},{int(step == 9)}")
    (directory / "log_standard_4_22_to_5_08_pure.csv").write_text(header + "\n".join(rows) + "\n")
    config = OneRecV2Config(maximum_events=30, maximum_examples=24)
    data = load_kuairand_examples(tmp_path, config)
    assert data.train and data.validation
    assert data.item_codes.shape == (data.items, 3)
    assert all(0 <= code[level] < data.cardinalities[level] for code in data.item_codes for level in range(3))
    assert set(row.advantage for row in (*data.train, *data.validation)) <= {
        -1.0,
        0.0,
        1.0,
    }
