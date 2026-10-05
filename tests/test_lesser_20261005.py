import pytest
import torch

from auto_research.post_training.lesser import (
    output_gradient_feature,
    rademacher_projection,
    round_robin_select,
)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_forward_feature_equals_autograd_of_readout_copy(seed):
    torch.manual_seed(seed)
    hidden = torch.randn(5, 4, dtype=torch.float64)
    readout = torch.randn(7, 4, dtype=torch.float64, requires_grad=True)
    target = torch.tensor([0, 1, 6, 2, 3])
    weights = torch.tensor([1.0, 0.0, -0.7, 0.5, 1.3], dtype=torch.float64)
    logits = hidden @ readout.T
    feature = output_gradient_feature(hidden, logits.detach(), target, weights, normalize=False)
    loss = -(weights * logits.log_softmax(-1).gather(1, target[:, None]).squeeze(1)).sum()
    reference = torch.autograd.grad(loss, readout)[0]
    assert torch.allclose(feature.reshape_as(reference), reference, atol=1e-12)
    assert readout.grad is None


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_tokenwise_projection_equals_projected_full_gradient(seed):
    torch.manual_seed(seed)
    hidden = torch.randn(6, 5, dtype=torch.float64)
    logits = torch.randn(6, 8, dtype=torch.float64)
    targets = torch.tensor([0, 2, 3, 5, 7, 1])
    weights = torch.tensor([1.0, 0.0, -0.4, 0.2, 0.3, 1.1], dtype=torch.float64)
    left, right = rademacher_projection(8, 5, 3, 4, seed=seed)
    full = output_gradient_feature(hidden, logits, targets, weights, normalize=False).reshape(8, 5)
    projected = output_gradient_feature(
        hidden, logits, targets, weights, projection=(left, right), normalize=False
    ).reshape(3, 4)
    assert torch.allclose(projected, left @ full @ right, atol=1e-12)
    normalized = output_gradient_feature(hidden, logits, targets, weights, projection=(left, right))
    assert torch.linalg.vector_norm(normalized).item() == pytest.approx(1)


def test_same_projection_and_round_robin_are_reproducible():
    assert all(torch.equal(a, b) for a, b in zip(
        rademacher_projection(8, 5, 3, 4, seed=42),
        rademacher_projection(8, 5, 3, 4, seed=42),
    ))
    pool = torch.tensor([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0], [0.1, 0.9]])
    query = torch.tensor([[1.0, 0.0], [0.0, 1.0]])
    assert round_robin_select(pool, query, 4) == [0, 2, 1, 3]
    assert round_robin_select(pool, query, 0) == []


def test_invalid_or_zero_features_are_rejected():
    with pytest.raises(ValueError, match="zero"):
        output_gradient_feature(
            torch.ones(2, 2), torch.zeros(2, 3), torch.tensor([0, 1]), torch.zeros(2)
        )
    with pytest.raises(ValueError, match="budget"):
        round_robin_select(torch.ones(2, 2), torch.ones(1, 2), 3)
