import pytest
import torch

from auto_research.reproductions.elbo_tds_components import ELBOTDSCore, augment_features, diagnostic


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic(seed):
    assert all(diagnostic(seed)["checks"].values())


def test_view_mean_gradient_and_reconstruction_are_not_detached():
    model = ELBOTDSCore(2, 2, 2).double()
    views = torch.arange(12, dtype=torch.float64).reshape(3, 2, 2).requires_grad_()
    original = torch.zeros(2, 2, dtype=torch.float64)
    noise = torch.zeros_like(views)
    out = model.objective(original, original, torch.zeros(2, dtype=torch.float64), views, views,
                          alpha=1., user_noise=noise, item_noise=noise)
    grad = torch.autograd.grad(out["prior"], views, retain_graph=True)[0]
    assert grad.abs().sum() > 0
    assert torch.allclose(grad.sum(0), torch.zeros_like(grad[0]), atol=1e-12)
    assert torch.autograd.grad(out["reconstruction"], views)[0].abs().sum() > 0


def test_masking_is_not_inverted_dropout_and_statistical_clips():
    x = torch.tensor([[0., 4., 3.], [3., 6., 9.]])
    out = augment_features(x, ("statistical", "sequential", "categorical"), views=8,
                           selection_probability=1., statistical_radius=10, bucket_maxima=(3, 0, 0),
                           sequence_mask_probability=1., categorical_dropout_probability=1.,
                           generator=torch.Generator().manual_seed(42))
    assert torch.count_nonzero(out[:, :, 1:]) == 0
    assert out[:, :, 0].min() == 0 and out[:, :, 0].max() == 3


@pytest.mark.parametrize("alpha", [-1, float("nan"), float("inf")])
def test_reject_bad_weight(alpha):
    model = ELBOTDSCore(2, 2, 2)
    x = torch.ones(2, 2)
    with pytest.raises(ValueError):
        model.objective(x, x, torch.zeros(2), x[None], x[None], alpha=alpha)


def test_reject_fractional_statistical_bucket():
    with pytest.raises(ValueError):
        augment_features(torch.tensor([[.5]]), ("statistical",), views=1, selection_probability=.5,
                         statistical_radius=1, bucket_maxima=(3,), sequence_mask_probability=.5,
                         categorical_dropout_probability=.5, generator=torch.Generator())
