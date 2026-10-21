import math

import pytest
import torch

from auto_research.foundation_models.locale_jepa import (
    ballreg_loss, local_ballreg_loss, locale_jepa_loss,
    torch_kmeans_labels, uniform_ball_cf,
)


def generator(seed=42):
    return torch.Generator().manual_seed(seed)


def test_ball_characteristic_function_is_uniform_not_gaussian():
    t = torch.tensor([0., 0.5, 1., 2.])
    # d=1 is Uniform[-sqrt(3), sqrt(3)], whose exact CF is sinc.
    expected = torch.sinc(t * math.sqrt(3) / math.pi)
    actual = uniform_ball_cf(t, 1)
    torch.testing.assert_close(actual, expected, atol=2e-6, rtol=2e-6)
    assert abs(float(actual[-1] - torch.exp(-t[-1].square() / 2))) > .1
    assert uniform_ball_cf(t, 8)[0] == pytest.approx(1)


def test_centered_ball_statistic_matches_independent_integration_and_shift():
    z = torch.tensor([[[1., 2.], [2., 0.], [-1., 3.], [0., -2.]]])
    g = generator()
    directions = torch.randn(2, 5, generator=g)
    directions = directions / directions.norm(dim=0)
    t = torch.linspace(0, 3, 17)
    projected = ((z - z.mean(1, keepdim=True)) @ directions)[..., None] * t
    cf = uniform_ball_cf(t, 2)
    err = (projected.cos().mean(1) - cf).square() + projected.sin().mean(1).square()
    independent = (2 * torch.trapezoid(err * torch.exp(-t.square() / 2), t, dim=-1)).mean() * 4
    actual = ballreg_loss(z, num_slices=5, generator=generator())
    torch.testing.assert_close(actual, independent)
    torch.testing.assert_close(actual, ballreg_loss(z + 20, num_slices=5, generator=generator()))


def test_kmeans_is_detached_and_reference_views_share_assignment():
    points = torch.tensor([[1., 0.], [1.1, .1], [-1., 0.], [-1.1, -.1]], requires_grad=True)
    # This seed initializes one centroid in each separated group. Lloyd k-means
    # is not guaranteed to escape all poor starts, nor does the paper claim so.
    labels = torch_kmeans_labels(points, 2, generator=generator(1))
    assert not labels.requires_grad
    assert labels[0] == labels[1] and labels[2] == labels[3] and labels[0] != labels[2]
    assert torch_kmeans_labels(points, 20, generator=generator()).shape == (4,)


def test_local_regularizer_is_equal_cluster_weighted_and_has_gradient():
    torch.manual_seed(7)
    z = torch.randn(2, 12, 3, requires_grad=True)
    # Reproduce random assignment then each cluster's independent test in order.
    g = generator()
    labels = torch_kmeans_labels(z.mean(0), 2, generator=g)
    expected = torch.stack([ballreg_loss(z[:, labels == index], num_slices=7, generator=g)
                            for index in range(2)]).mean()
    actual = local_ballreg_loss(z, num_clusters=2, min_cluster_size=1,
                               num_slices=7, generator=generator())
    torch.testing.assert_close(actual, expected)
    actual.backward()
    assert torch.isfinite(z.grad).all() and z.grad.norm() > 0


def test_empty_kept_clusters_use_whole_batch_test_not_zero():
    z = torch.randn(2, 3, 4)
    stats = {}
    g = generator()
    torch_kmeans_labels(z.mean(0), 3, generator=g)
    expected = ballreg_loss(z, num_slices=5, generator=g)
    actual = local_ballreg_loss(z, num_clusters=3, min_cluster_size=4, stats=stats,
                               num_slices=5, generator=generator())
    torch.testing.assert_close(actual, expected)
    assert stats == {"configured_clusters": 3., "effective_clusters": 0.,
                     "kept_fraction": 0., "fallback": 1.}
    assert ballreg_loss(torch.zeros(2, 8, 4), generator=generator()) > 0


def test_prediction_reference_not_stop_gradient_and_composite_objective():
    z = torch.randn(3, 8, 4, requires_grad=True)
    terms = locale_jepa_loss(z, regularization_weight=.2, num_global=2,
                            num_clusters=1, generator=generator())
    expected = (z - z[:2].mean(0, keepdim=True)).square().mean()
    torch.testing.assert_close(terms["prediction"], expected)
    torch.testing.assert_close(terms["loss"], .8 * expected + .2 * terms["regularizer"])
    terms["loss"].backward()
    assert z.grad.norm() > 0


@pytest.mark.parametrize("value", [torch.empty(0, 4, 3), torch.zeros(3, 4),
                                    torch.full((2, 3, 4), float("nan"))])
def test_invalid_projections_fail_closed(value):
    with pytest.raises(ValueError):
        local_ballreg_loss(value)


def test_invalid_settings_fail_closed():
    z = torch.randn(2, 8, 3)
    for kwargs in ({"num_clusters": 0}, {"min_cluster_size": 0}, {"num_global": 3}):
        with pytest.raises(ValueError):
            local_ballreg_loss(z, **kwargs)
    with pytest.raises(ValueError):
        ballreg_loss(z, knots=1)
