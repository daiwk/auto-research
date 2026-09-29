import pytest

from auto_research.post_training.token_ids import token_ids


def test_token_ids_accepts_standard_tokenizer_return_shapes():
    class Encoding:
        ids = [4, 5]

    assert token_ids([1, 2, 3]) == [1, 2, 3]
    assert token_ids(Encoding()) == [4, 5]
    assert token_ids({"input_ids": [6, 7], "attention_mask": [1, 1]}) == [6, 7]
    assert token_ids({"input_ids": [[8, 9]]}) == [8, 9]


@pytest.mark.parametrize("bad", [[], "tokens", ["input_ids"], {"input_ids": []}, [[1], [2]]])
def test_token_ids_rejects_missing_or_ambiguous_ids(bad):
    with pytest.raises((ValueError, KeyError)):
        token_ids(bad)
