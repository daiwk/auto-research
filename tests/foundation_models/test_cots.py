import pytest

torch = pytest.importorskip("torch")
from auto_research.foundation_models.cots import CotsState, competitive_token_selection  # noqa: E402


def test_closed_form_top_two_competition_and_sampled_anchor_outside_support():
    p = torch.tensor([[.6, .3, .08, .02]], dtype=torch.float64, requires_grad=True)
    embeddings = torch.eye(4, dtype=torch.float64, requires_grad=True)
    result = competitive_token_selection(p, embeddings, torch.tensor([3]), CotsState.initial((1,)), top_k=2)
    assert result.alpha.item() == pytest.approx(1/3)
    torch.testing.assert_close(result.soft_embedding, torch.tensor([[2/3, 1/3, 0., 0.]], dtype=torch.float64))
    torch.testing.assert_close(result.next_embedding, torch.tensor([[2/9, 1/9, 0., 2/3]], dtype=torch.float64))
    assert result.sampled_coefficient.item() == pytest.approx(2/3)
    gradients = torch.autograd.grad(result.next_embedding.square().sum(), (p, embeddings))
    assert all(torch.isfinite(g).all() and g.abs().sum() > 0 for g in gradients)


def test_competition_schedule_endpoints_and_support_independence():
    embeddings = torch.eye(4)
    p = torch.tensor([[1., 0., 0., 0.], [.5, .5, 0., 0.], [.7, .2, .09, .01]])
    sampled = torch.tensor([0, 3, 0])
    small = competitive_token_selection(p, embeddings, sampled, CotsState.initial((3,)), top_k=2)
    large = competitive_token_selection(p, embeddings, sampled, CotsState.initial((3,)), top_k=4)
    assert small.alpha.tolist() == pytest.approx([0., .5, 2/9])
    torch.testing.assert_close(small.alpha, large.alpha)
    assert not torch.allclose(small.soft_embedding[2], large.soft_embedding[2])
    assert bool((small.sampled_coefficient >= .5).all())
    drift = (large.next_embedding - large.discrete_embedding).norm(dim=-1)
    soft_drift = (large.soft_embedding - large.discrete_embedding).norm(dim=-1)
    assert bool((drift <= .5 * soft_drift + 1e-7).all())


def test_end_think_immediate_irreversible_lock_protected_step_and_eos():
    p = torch.tensor([[.4, .3, .2, .1]]).expand(3, -1)
    embedding = torch.eye(4)
    tokens = torch.tensor([1, 2, 3])
    first = competitive_token_selection(p, embedding, tokens, CotsState.initial((3,)), top_k=3,
                                       end_think_token_ids=(1,), protected_token_ids=(2,), eos_token_ids=(3,))
    assert first.effective_alpha.tolist() == [0., 0., 0.]
    assert first.state.reasoning.tolist() == [False, True, False]
    assert first.state.finished.tolist() == [False, False, True]
    torch.testing.assert_close(first.next_embedding, embedding[tokens], rtol=0, atol=0)
    second = competitive_token_selection(p, embedding, torch.tensor([0, 0, 0]), first.state, top_k=3)
    assert second.effective_alpha[0] == 0 and second.effective_alpha[2] == 0
    assert second.effective_alpha[1] > 0  # protection is not an irreversible phase exit
    assert second.state.finished.tolist() == [False, False, True]


def test_true_gradcheck_through_logits_and_embedding_not_numpy_or_straight_through():
    logits = torch.tensor([[2., .8, -.4, -1.]], dtype=torch.float64, requires_grad=True)
    embedding = torch.randn(4, 3, dtype=torch.float64, requires_grad=True)
    state = CotsState.initial((1,))
    def operation(z, weight):
        return competitive_token_selection(z.softmax(-1), weight, torch.tensor([3]), state,
                                            top_k=3).next_embedding
    assert torch.autograd.gradcheck(operation, (logits, embedding))
    gradient = torch.autograd.grad(operation(logits, embedding).square().sum(), logits)[0]
    assert gradient.abs().sum() > 0


@pytest.mark.parametrize("probability", [[-.1, 1.1], [0., 0.], [float("nan"), 1.], [.1, .2]])
def test_invalid_probabilities_are_rejected(probability):
    with pytest.raises(ValueError):
        competitive_token_selection(torch.tensor(probability), torch.eye(2), torch.tensor(0),
                                    CotsState.initial(()), top_k=2)


def test_scalar_batch_and_low_precision_work_without_changing_embedding_dtype():
    result = competitive_token_selection(torch.tensor([.6, .4], dtype=torch.bfloat16),
                                        torch.eye(2, dtype=torch.bfloat16), torch.tensor(1),
                                        CotsState.initial(()), top_k=2)
    assert result.next_embedding.dtype == torch.bfloat16
    assert result.alpha.dtype == torch.float32
    assert result.sampled_coefficient >= .5
