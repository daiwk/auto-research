import pytest
from types import SimpleNamespace

torch = pytest.importorskip("torch")

from auto_research.post_training.pivot_checkpoint import frozen_adapter_state, padded_stack, response_logits


def test_frozen_warmup_reference_restores_actual_candidate_even_after_failure():
    model = torch.nn.Linear(1, 1)
    reference = {"weight": model.weight.detach().clone() + 1}
    before = model.weight.detach().clone()
    with pytest.raises(RuntimeError):
        with frozen_adapter_state(model, reference):
            torch.testing.assert_close(model.weight, reference["weight"])
            raise RuntimeError("teacher pass failed")
    torch.testing.assert_close(model.weight, before)


def test_variable_response_padding_preserves_gradient_and_masks_prompt_out():
    banks = [{"mask": torch.ones(2, 2).bool()}, {"mask": torch.ones(2, 3).bool()}]
    first = torch.ones(2, 2, 4, requires_grad=True)
    second = torch.ones(2, 3, 4, requires_grad=True)
    logits = padded_stack(banks, [first, second], is_logits=True)
    mask = padded_stack(banks, [b["mask"] for b in banks])
    assert logits.shape == (2, 2, 3, 4) and not mask[0, :, -1].any()
    logits[mask].sum().backward()
    assert first.grad.eq(1).all() and second.grad.eq(1).all()


def test_full_token_identity_preserved_while_unnamed_projection_padding_is_removed():
    class Model:
        pivot_vocabulary_size = 4

        def __call__(self, ids, **kwargs):
            result = torch.arange(6.).expand(1, 5, 6)
            return SimpleNamespace(logits=result)

    logits = response_logits(Model(), {"ids": torch.ones(1, 5).long(), "start": 2})
    assert logits.shape == (1, 2, 4)
    torch.testing.assert_close(logits[0, 0], torch.arange(4.))
