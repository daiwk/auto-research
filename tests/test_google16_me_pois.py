"""Independent formula and information-boundary diagnostics; no map labels."""
import math

import pytest
import torch

from auto_research.foundation_models.google16_me_pois import (
    MobilityPrototypeLoss, distribution_kl_sum, prototype_contrastive_loss,
    transferred_visit_distribution,
)


def test_multiscale_prior_normalizes_each_scale_before_averaging():
    sparse = torch.tensor([[0., 0.]], dtype=torch.float64)
    anchors = torch.tensor([[0., 0.], [2., 0.]], dtype=torch.float64)
    histogram = torch.tensor([[10., 0.], [0., 1.]], dtype=torch.float64)
    result = transferred_visit_distribution(sparse, anchors, histogram, torch.tensor([1., 2.]))
    first = 1 / (1 + math.exp(-2))
    second = 1 / (1 + math.exp(-.5))
    torch.testing.assert_close(result, torch.tensor([[(first + second) / 2, 1 - (first + second) / 2]], dtype=torch.float64))
    torch.testing.assert_close(result.sum(-1), torch.ones(1, dtype=torch.float64))


def test_contrastive_unique_poi_identity_not_duplicate_negatives():
    prototype = torch.eye(2)
    visits = prototype[torch.tensor([0, 0, 1])]
    loss = prototype_contrastive_loss(visits, prototype, torch.tensor([0, 0, 1]), temperature=1)
    assert loss.item() == pytest.approx(math.log1p(math.exp(-1)))


def test_kl_direction_and_sum_match_independent_definition():
    logits = torch.tensor([[1., 2., 3.], [3., 2., 1.]], dtype=torch.float64)
    target = torch.tensor([[.2, .3, .5], [1., 0., 0.]], dtype=torch.float64)
    actual = distribution_kl_sum(logits, target)
    expected = sum(float(p) * math.log(float(p / q)) for rowp, rowq in zip(target, logits.softmax(-1), strict=True)
                   for p, q in zip(rowp, rowq, strict=True) if p)
    assert actual.item() == pytest.approx(expected)


def test_all_defined_loss_paths_receive_gradients_and_external_text_is_frozen():
    torch.manual_seed(4)
    model = MobilityPrototypeLoss(3, 4, 5, 2)
    visits = torch.randn(4, 4, requires_grad=True)
    text = torch.randn(3, 5, requires_grad=True)
    prior = torch.tensor([[.2, .8], [.7, .3]], requires_grad=True)
    result = model(visits, torch.tensor([0, 1, 1, 2]), text, torch.tensor([0]),
                   torch.tensor([[.4, .6]]), torch.tensor([1, 2]), prior)
    result["loss"].backward()
    assert all(parameter.grad is not None and parameter.grad.norm() > 0 for parameter in model.parameters())
    assert visits.grad.norm() > 0 and text.grad is None and prior.grad is None


@pytest.mark.parametrize("bad", [0., -1., float("nan")])
def test_invalid_gaussian_bandwidth_rejected(bad):
    with pytest.raises(ValueError):
        transferred_visit_distribution(torch.zeros(1, 2), torch.zeros(1, 2), torch.ones(1, 2), torch.tensor([bad]))


def test_zero_visit_anchor_and_bad_distribution_rejected():
    with pytest.raises(ValueError):
        transferred_visit_distribution(torch.zeros(1, 2), torch.zeros(1, 2), torch.zeros(1, 2), torch.ones(1))
    with pytest.raises(ValueError):
        distribution_kl_sum(torch.zeros(1, 2), torch.zeros(1, 2))
