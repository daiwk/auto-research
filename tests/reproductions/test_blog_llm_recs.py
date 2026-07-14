import pytest

from auto_research.reproductions.beque.model import RewriteExample, offline_feedback
from auto_research.reproductions.llm_rec_data import binary_auc, load_text_ctr_data


def _write_movielens_fixture(root):
    directory = root / "ml-100k"
    directory.mkdir()
    flags = "|".join(["1", *(["0"] * 18)])
    (directory / "u.item").write_text(
        "\n".join(
            f"{item}|Movie {item} (1995)|01-Jan-1995||url|{flags}"
            for item in range(1, 5)
        ) + "\n",
        encoding="latin-1",
    )
    sequence = [(1, 5), (2, 1), (3, 5), (4, 2), (2, 4), (1, 1), (4, 5)]
    rows = []
    for user in (1, 2):
        rows.extend(
            f"{user}\t{item}\t{rating}\t{user * 100 + step}"
            for step, (item, rating) in enumerate(sequence)
        )
    (directory / "u.data").write_text("\n".join(rows) + "\n")


def test_shared_text_ctr_data_uses_chronological_history(tmp_path):
    _write_movielens_fixture(tmp_path)
    data = load_text_ctr_data(tmp_path)
    assert data.train and data.test
    assert data.train[0].history == (0,)
    assert {row.label for row in data.train} == {0, 1}
    assert "Candidate:" in data.prompt(data.train[0])


def test_beque_feedback_rewards_relevant_incremental_rewrite():
    row = RewriteExample("wireless", "wireless noise cancelling headphones", 0)
    catalog = (row.target, "kitchen coffee maker")
    weak = offline_feedback(row, "wireless", catalog)
    strong = offline_feedback(row, row.target, catalog)
    assert strong > weak


def test_beque_preference_sampling_does_not_inject_supervised_target():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.beque.model import (
        BEQUEConfig,
        BEQUEData,
        sample_preference_lists,
    )

    row = RewriteExample("toy", "secret supervised target", 0)
    data = BEQUEData((row,), (), (row.target,))

    class Encoded(dict):
        def to(self, _device):
            return self

    class Tokenizer:
        def __call__(self, *_args, **_kwargs):
            return Encoded(input_ids=torch.tensor([[1]]))

        def batch_decode(self, _generated, skip_special_tokens=True):
            return ["model rewrite"] * 4

    class Model:
        def parameters(self):
            return iter((type("Parameter", (), {"device": torch.device("cpu")})(),))

        def eval(self):
            return self

        def generate(self, **_kwargs):
            return torch.tensor([[1], [1], [1], [1]])

    lists = sample_preference_lists(Model(), Tokenizer(), (row,), data, BEQUEConfig())
    assert row.target not in lists[0][1]


def test_shared_auc_perfect_ranking():
    assert binary_auc([0, 0, 1, 1], [0.1, 0.2, 0.8, 0.9]) == 1.0
