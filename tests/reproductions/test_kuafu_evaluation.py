"""Public MRQA evaluation must keep gold outside the policy prompt."""

import pytest

torch = pytest.importorskip("torch")

from auto_research.reproductions.kuafu.evaluation import (  # noqa: E402
    exact_match, raw_context_qa_loss, token_f1, same_token_budget,
)


def test_mrqa_answers_use_standard_normalization_and_max_reference() -> None:
    assert exact_match("The Eiffel Tower!", ("eiffel tower", "tower")) == 1.0
    assert token_f1("Paris France", ("Berlin", "Paris")) == pytest.approx(2 / 3)
    assert exact_match("Berlin", ("Paris",)) == 0.0


def test_equal_budget_controls_keep_exactly_cached_token_count() -> None:
    ids = torch.arange(2, 22)
    head, tail = same_token_budget(ids, item_count=3, tokens_per_item=2)
    assert head.tolist() == [2, 3, 4, 5, 6, 7]
    assert tail.tolist() == [16, 17, 18, 19, 20, 21]
    with pytest.raises(ValueError, match="budget"):
        same_token_budget(ids[:3], item_count=3, tokens_per_item=2)


def test_independent_raw_control_masks_source_and_question_from_loss() -> None:
    class Decoder:
        def __call__(self, *, input_ids, labels, return_dict):
            assert return_dict
            assert input_ids.tolist() == [[2, 3, 4, 5, 6]]
            assert labels.tolist() == [[-100, -100, -100, 5, 6]]
            return type("Output", (), {"loss": torch.tensor(0.25)})()

    loss = raw_context_qa_loss(
        Decoder(), torch.tensor([2, 3]), torch.tensor([4]), torch.tensor([5, 6])
    )
    assert loss.item() == 0.25
    with pytest.raises(ValueError, match="nonempty"):
        raw_context_qa_loss(Decoder(), torch.tensor([]), torch.tensor([4]), torch.tensor([5]))
