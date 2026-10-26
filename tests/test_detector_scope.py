"""Defining numerical controls for the bounded DetectorScope sparse head."""
import copy

import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models.detector_scope import (
    AuditableSparseHead,
    diagnostic,
    fit_training_rms,
    pool_sae_features,
    spearman_simulation_scores,
)


def fixture():
    x = torch.tensor([[0., 2., 1., 0.], [2., 0., 5., 0.], [1., 4., 3., 0.]], dtype=torch.float64)
    scores = torch.tensor([.85, .849, 1., -.2], dtype=torch.float64)
    return x, scores


def test_pooling_ignores_padding_and_preserves_layer_order():
    x = torch.tensor([[[[1., 4.], [3., 2.], [100., 200.]],
                       [[9., 1.], [4., 7.], [300., 400.]]]], requires_grad=True)
    result = pool_sae_features(x, torch.tensor([[True, True, False]]))
    assert result.tolist() == [[3., 4., 9., 7.]]
    assert not result.requires_grad
    assert not torch.equal(result, x.detach().mean(2).flatten(1))


@pytest.mark.parametrize("mutation", ["all_padding", "shape", "dtype", "negative", "nan", "empty"])
def test_bad_sae_inputs_rejected(mutation):
    x, m = torch.ones(2, 1, 3, 2), torch.ones(2, 3, dtype=torch.bool)
    if mutation == "all_padding":
        m[0] = False
    elif mutation == "shape":
        m = m[:, :2]
    elif mutation == "dtype":
        m = m.float()
    elif mutation == "negative":
        x[0, 0, 0, 0] = -1
    elif mutation == "nan":
        x[0, 0, 0, 0] = float("nan")
    else:
        x, m = x[:, :, :0], m[:, :0]
    with pytest.raises(ValueError):
        pool_sae_features(x, m)


def test_spearman_uses_average_ranks_not_pearson_values():
    real = torch.tensor([[0., 0., 2., 5., 5.], [0., 1., 2., 3., 4.]], dtype=torch.float64)
    pred = torch.tensor([[0., 0., 1., 4., 4.], [0., 1., 2., 3., 100.]], dtype=torch.float64)
    score = spearman_simulation_scores(real.requires_grad_(), pred.requires_grad_())
    assert torch.allclose(score, torch.ones_like(score))
    assert not score.requires_grad
    pearson = torch.corrcoef(torch.stack((real[1], pred[1])))[0, 1]
    assert pearson < .8
    assert torch.allclose(spearman_simulation_scores(real, real.flip(-1)), -torch.ones(2, dtype=torch.float64))
    tied = spearman_simulation_scores(torch.tensor([[0., 0., 1., 2.]], dtype=torch.float64),
                                     torch.tensor([[0., 1., 1., 2.]], dtype=torch.float64))
    assert tied.item() == pytest.approx(5 / 6)


@pytest.mark.parametrize("mutation", ["constant_real", "constant_pred", "nan", "fraction", "negative", "shape"])
def test_bad_description_validation_rejected(mutation):
    real = torch.tensor([[0., 0., 1., 2.]])
    pred = real.clone()
    if mutation == "constant_real":
        real.zero_()
    elif mutation == "constant_pred":
        pred.zero_()
    elif mutation == "nan":
        pred[0, 0] = float("nan")
    elif mutation == "fraction":
        pred[0, 0] = .3
    elif mutation == "negative":
        pred[0, 0] = -1
    else:
        pred = pred[:, :3]
    with pytest.raises(ValueError):
        spearman_simulation_scores(real, pred)


def test_training_rms_is_not_zscore_and_zero_features_stay_zero():
    x, scores = fixture()
    head = AuditableSparseHead(x.requires_grad_(), scores.requires_grad_(), tau=.85)
    expected = x.detach().square().mean(0).sqrt()
    expected[-1] = 1
    assert torch.allclose(head.rms_scale, expected)
    assert head.interp_mask.tolist() == [True, False, True, False]
    assert not head.rms_scale.requires_grad and not head.interp_mask.requires_grad
    assert (x.detach() / head.rms_scale)[0, 0].item() == 0
    assert not torch.allclose(head.rms_scale, x.detach().std(0))
    before = copy.deepcopy(head.state_dict())
    head.predict_with_attributions(x.detach() * 1e8)
    assert all(torch.equal(v, head.state_dict()[k]) for k, v in before.items())


def test_rms_stable_large_values_and_no_implicit_test_fitting():
    x = torch.tensor([[1e200, 0.], [2e200, 0.]], dtype=torch.float64)
    scale = fit_training_rms(x)
    assert bool(torch.isfinite(scale).all())
    assert scale[0].item() == pytest.approx(1e200 * (2.5 ** .5))
    assert scale[1].item() == 1


def test_repeated_sgd_momentum_then_prox_matches_independent_torch_oracle():
    x, scores = fixture()
    head = AuditableSparseHead(x, scores)
    y = torch.tensor([0., 1., 1.], dtype=torch.float64)
    oracle = torch.nn.Linear(4, 1).double()
    with torch.no_grad():
        oracle.weight.zero_()
        oracle.bias.zero_()
    optimizer = torch.optim.SGD(oracle.parameters(), lr=.03, momentum=.9)
    normalized = x * head.interp_mask / head.rms_scale
    for _ in range(3):
        optimizer.zero_grad()
        loss = F.binary_cross_entropy_with_logits(oracle(normalized).squeeze(-1), y)
        loss.backward()
        optimizer.step()
        with torch.no_grad():
            w = oracle.weight
            w.copy_(w.sign() * (w.abs() - .03 * .1).clamp_min(0))
        head.proximal_step(x, y, lr=.03, l1=.1, momentum=.9)
        assert torch.allclose(head.weight, oracle.weight[0], atol=1e-15)
        assert torch.allclose(head.bias, oracle.bias[0], atol=1e-15)
    assert head.weight[1].item() == head.weight[3].item() == 0
    assert head.bias.item() != 0


def test_no_gradient_into_frozen_backbone_scores_or_labels():
    x, scores = fixture()
    x.requires_grad_()
    scores.requires_grad_()
    y = torch.tensor([0., 1., 0.], dtype=torch.float64, requires_grad=True)
    head = AuditableSparseHead(x, scores)
    result = head.proximal_step(x, y)
    assert result['gradient_norm'] > 0
    assert x.grad is None and scores.grad is None and y.grad is None


def test_raw_fold_and_every_zero_ablation_reconstructs_logit():
    x, scores = fixture()
    head = AuditableSparseHead(x, scores)
    with torch.no_grad():
        head.weight.copy_(torch.tensor([1., 999., -2., 8.], dtype=torch.float64))
        head.bias.fill_(.31)
    result = head.predict_with_attributions(x)
    assert torch.allclose(result['logits'], head(x))
    assert torch.allclose(result['contributions'].sum(-1) + result['bias'], result['logits'])
    assert not torch.allclose(result['raw_weight'], head.weight * head.interp_mask)
    for feature in range(4):
        ablated = x.clone()
        ablated[:, feature] = 0
        delta = result['logits'] - head.predict_with_attributions(ablated)['logits']
        assert torch.allclose(delta, result['contributions'][:, feature], atol=1e-15)
    assert (result['contributions'][:, [1, 3]] == 0).all()


@pytest.mark.parametrize("mutation", ["tau", "score_range", "score_shape", "score_nan", "negative_train"])
def test_bad_head_configuration_rejected(mutation):
    x, scores = fixture()
    tau = .85
    if mutation == "tau":
        tau = float('inf')
    elif mutation == "score_range":
        scores[0] = 1.1
    elif mutation == "score_shape":
        scores = scores[:2]
    elif mutation == "score_nan":
        scores[0] = float('nan')
    else:
        x[0, 0] = -1
    with pytest.raises(ValueError):
        AuditableSparseHead(x, scores, tau=tau)


@pytest.mark.parametrize("kwargs", [{"lr": 0.}, {"l1": -1.}, {"momentum": 1.}, {"lr": float('nan')}])
def test_bad_optimizer_arguments_rejected_without_mutation(kwargs):
    x, scores = fixture()
    head = AuditableSparseHead(x, scores)
    before = copy.deepcopy(head.state_dict())
    with pytest.raises(ValueError):
        head.proximal_step(x, torch.zeros(3, dtype=torch.float64), **kwargs)
    assert all(torch.equal(v, head.state_dict()[k]) for k, v in before.items())


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_seeded_mechanism_not_capability(seed):
    result = diagnostic(seed)
    assert all(value is True for value in result['checks'].values())
    assert len(result['checks']) == 8
    assert result['metrics']['pretrained_model_calls'] == 0
    assert result['metrics']['fixture_bce_after'] < result['metrics']['fixture_bce_before']


def test_unavailable_or_invalid_device_never_silently_falls_back():
    with pytest.raises(ValueError):
        diagnostic(device='mps')
    if not torch.cuda.is_available():
        with pytest.raises(ValueError):
            diagnostic(device='cuda')
