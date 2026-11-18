import pytest
import torch
from torch import nn

from auto_research.foundation_models import hvmap as h
from auto_research.foundation_models import mixed_signals_weights as w


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_actual_cpu_components(seed):
    for module in (h, w):
        report = module.diagnostic(seed)
        assert all(report["checks"].values())
        assert report["diagnostic_only"] is True


def test_fuzzy_is_cross_target_not_rkd_or_infonce():
    y = torch.eye(3, requires_grad=True)
    assert h.fuzzy_contrastive_loss(y, y).item() == 0
    assert h.fuzzy_contrastive_loss(-y, y).item() == 12
    assert h.fuzzy_contrastive_loss(-y, y, reduction="mean").item() == pytest.approx(12 / 9)
    assert h.fuzzy_contrastive_loss(y, y, metric="l2").item() == 0
    with pytest.raises(ValueError):
        h.fuzzy_contrastive_loss(y, y, metric="hinge")
    with pytest.raises(ValueError):
        h.fuzzy_contrastive_loss(torch.zeros(3, 3), y)
    with pytest.raises(ValueError):
        h.fuzzy_contrastive_loss(torch.full((3, 3), 1e30), y)
    with pytest.raises(ValueError):
        h.fuzzy_contrastive_loss(y[:2], y)


def test_network_layers_native_scores_and_hub():
    net = h.HVMap(4, 3)
    assert [(layer.in_features, layer.out_features) for layer in net.layers] == [(4, 15), (15, 15), (15, 15), (15, 3)]
    zero = h.HVMap(4, 3)
    with torch.no_grad():
        for parameter in zero.parameters():
            parameter.zero_()
    with pytest.raises(ValueError):
        zero(torch.ones(2, 4))
    q = torch.tensor([[1., 0.]])
    x = torch.eye(2)
    assert h.score2(q, x, q, x.flip(0)).tolist() == pytest.approx([.7, .3])
    assert h.score2(q, x, q, x.flip(0), native_weight=.2).tolist() == pytest.approx([.2, .8])
    with pytest.raises(ValueError):
        h.score2(q, x, q, x.flip(0), native_weight=float("nan"))
    calls = []
    def transform(edge):
        def run(value):
            calls.append(edge)
            return value * 2
        return run
    result = h.map_via_hub(x, "a", "b", "hub", {("a", "hub"): transform("in"), ("hub", "b"): transform("out")})
    assert calls == ["in", "out"] and torch.equal(result, 4 * x) and torch.equal(x, torch.eye(2))
    with pytest.raises(ValueError):
        h.map_via_hub(x, "a", "b", "hub", {})
    assert [row[0] for row in h.federated_topk({"a": torch.tensor([.9, .8]), "b": torch.tensor([.1])}, 2)] == ["a", "a"]
    with pytest.raises(ValueError):
        h.federated_topk({"a": torch.arange(3.)}, 2)


def test_atomic_patch_validation_and_only_parameters():
    model = nn.Linear(3, 2)
    original = {key: value.clone() for key, value in model.state_dict().items()}
    for bad in ({"weight": torch.zeros_like(model.weight), "bias": torch.ones(1)},
                {"unknown": torch.ones(2)}, {"bias": torch.full_like(model.bias, float("inf"))},
                {"weight": model.weight.double()}, {}):
        with pytest.raises(ValueError):
            w.apply_weight_patch(model, bad)
        assert all(torch.equal(value, original[key]) for key, value in model.state_dict().items())
    model.register_buffer("stats", torch.zeros(2))
    with pytest.raises(ValueError):
        w.apply_weight_patch(model, {"stats": torch.ones(2)})
    w.apply_weight_patch(model, {"bias": torch.zeros_like(model.bias)})
    assert torch.equal(model.bias, torch.zeros(2))


def test_practice_failures_and_unclipped_evaluator_metrics():
    calls = []
    def bad(_):
        calls.append(1)
        return {"bad": float("nan")}
    budget = w.PracticeBudget(bad, 1)
    with pytest.raises(ValueError):
        budget.evaluate(nn.Linear(1, 1))
    with pytest.raises(RuntimeError):
        budget.evaluate(nn.Linear(1, 1))
    assert calls == [1] and budget.outcomes == ["failed"]
    assert w.recovery_fraction(.9, .4, .8) == pytest.approx(1.25)
    assert w.recovery_fraction(.3, .4, .8) == pytest.approx(-.25)
    with pytest.raises(ValueError):
        w.recovery_fraction(.5, .4, .4)
    with pytest.raises(ValueError):
        w.recovery_fraction(1e308, -1e308, -1e308 + 1e293)
    with pytest.raises(ValueError):
        w.balanced_accuracy(torch.tensor([0]), torch.tensor([0]), 2)
    assert w.balanced_accuracy(torch.tensor([0, 0, 0, 1]), torch.tensor([0, 0, 1, 1]), 2) == .75
