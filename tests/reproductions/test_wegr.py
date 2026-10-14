import torch

from auto_research.reproductions.wegr.model import (
    CoCoVAE, SIDPolicy, dhpo_loss, horizon, multi_positive_loss, prefix_rewards,
)


def test_horizon_rewards_keep_max_positive_and_full_exact_match():
    samples = torch.tensor([[[1, 2, 3], [1, 4, 5], [7, 4, 5]]])
    positives = torch.tensor([[[1, 2, 3], [1, 2, 4]]])
    values = torch.tensor([[1., 2.]])
    assert prefix_rewards(samples, positives, values, horizon_length=1).tolist() == [[2., 2., 0.]]
    assert prefix_rewards(samples, positives, values, horizon_length=3).tolist() == [[1., 0., 0.]]
    assert [horizon(i, 2, 3) for i in range(7)] == [1, 1, 2, 2, 3, 3, 3]


def test_policy_gradient_never_supervises_beyond_reward_horizon():
    logp = torch.zeros(1, 2, 3, requires_grad=True)
    loss = dhpo_loss(logp, logp.detach(), torch.tensor([[0., 2.]]), horizon_length=1)
    loss.backward()
    assert logp.grad[..., 0].abs().sum() > 0
    assert logp.grad[..., 1:].abs().sum() == 0
    assert logp.grad[0, 1, 0] < 0  # gradient descent increases the rewarded prefix


def test_msft_weights_sessions_not_number_of_positives():
    logp = torch.tensor([[[-1., -1.], [-3., -3.]], [[-2., -2.], [-9., -9.]]])
    assert multi_positive_loss(logp, torch.tensor([[True, True], [True, False]])).item() == 2.


def test_tokenizer_far_updates_multiple_codes_but_refreshes_first_layer_only():
    torch.manual_seed(42)
    model = CoCoVAE(5, dimension=4, codebook_sizes=(5, 5, 5))
    x = torch.randn(8, 5)
    _, codes, loss, parts = model(x)
    loss.backward()
    assert parts["collision"].item() >= 0
    assert all((book.grad.abs().sum(-1) > 0).sum() > 1 for book in model.books)
    later = [book.detach().clone() for book in model.books[1:]]
    model.refresh(codes)
    assert all(torch.equal(before, after) for before, after in zip(later, model.books[1:]))


def test_causal_sid_decoder_has_no_future_token_access():
    torch.manual_seed(1)
    model = SIDPolicy(4).eval()
    context = torch.randn(1, 4)
    first = model.logits(context, torch.tensor([[1, 2]]))
    second = model.logits(context, torch.tensor([[1, 7]]))
    assert torch.allclose(first[:, :2], second[:, :2])
    assert not torch.allclose(first[:, 2], second[:, 2])
