import pytest
import torch

from auto_research.foundation_models.elastic_expert_routing import ElasticExpertRouting


def test_discrete_gaussian_expectation_dispatch_and_inference_budget():
    torch.manual_seed(42)
    model = ElasticExpertRouting(8, 16, 7, target_k=3, radius=2)
    assert torch.allclose((model.budgets * model.budget_probability).sum(), torch.tensor(3.))
    x = torch.randn(100, 8)
    output, stats = model(x, return_statistics=True)
    assert stats["dispatch_counts"].sum() == stats["budgets"].sum()
    assert len(stats["budgets"].unique()) > 1
    (output.square().mean() + .01 * stats["balance_loss"]).backward()
    assert model.router.weight.grad.abs().sum() > 0
    assert all(expert[0].weight.grad is not None for expert in model.experts)
    model.eval()
    a, stats = model(x, return_statistics=True)
    b = model(x)
    assert torch.equal(a, b) and (stats["budgets"] == 3).all()
    assert stats["dispatch_counts"].sum() == 300


def test_rejects_asymmetric_clipped_neighborhood():
    with pytest.raises(ValueError):
        ElasticExpertRouting(8, 16, 4, target_k=1, radius=1)
