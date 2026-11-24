import math

import pytest
import torch

from auto_research.foundation_models.deep_cross_attention import DCAAttention, GRN3, diagnostic, history_stack


def test_grn3_literal_text_formula_has_feature_weights_and_token_dependent_scores():
    generator = torch.Generator().manual_seed(7)
    stack = torch.randn(2, 4, 3, 6, generator=generator, dtype=torch.double)
    route = GRN3(6, 3).double()
    with torch.no_grad():
        route.base.copy_(torch.randn(3, 6, generator=generator, dtype=torch.double))
        route.dynamic.copy_(torch.randn(6, generator=generator, dtype=torch.double))
    expected = torch.zeros(2, 4, 6, dtype=torch.double)
    for source in range(3):
        score = (stack[:, :, source] * route.dynamic).sum(-1).relu()
        expected += stack[:, :, source] * (route.base[source] + score.unsqueeze(-1))
    torch.testing.assert_close(route(stack), expected)
    assert not torch.equal(route(stack)[0, 0], route(stack)[0, 1])


def test_initialization_is_sum_not_softmax_mean_and_zero_relu_gradient_is_visible():
    route = GRN3(4, 3)
    stack = torch.ones(1, 2, 3, 4)
    assert torch.equal(route(stack), torch.full((1, 2, 4), 3.))
    route(stack).sum().backward()
    assert torch.count_nonzero(route.dynamic.grad) == 0
    assert torch.count_nonzero(route.base.grad) == route.base.numel()
    with torch.no_grad():
        route.base.fill_(-2.)
    assert torch.equal(route(stack), torch.full((1, 2, 4), -6.))


def test_first_middle_sum_last_k_order_and_gradients():
    history = [torch.full((1, 2, 3), float(i), requires_grad=True) for i in range(6)]
    stack = history_stack(history, keep_last=2)
    assert stack.shape == (1, 2, 4, 3)
    for index, expected in enumerate((5., 4., 6., 0.)):
        assert torch.equal(stack[..., index, :], torch.full((1, 2, 3), expected))
    stack.sum().backward()
    assert all(torch.equal(x.grad, torch.ones_like(x)) for x in history)
    assert history_stack(history, keep_last=0).shape[-2] == 2
    assert history_stack(history[:1], keep_last=0).shape[-2] == 1
    assert torch.equal(history_stack(history, keep_last=20), history_stack(history))


def test_qkv_routing_parameters_are_independent_and_init_recovers_standard_attention():
    torch.manual_seed(8)
    model = DCAAttention(8, 3, heads=2)
    stack = torch.randn(2, 5, 3, 8)
    base = stack.sum(-2)
    q, k, v = [projection(norm(base)).reshape(2, 5, 2, 4).transpose(1, 2)
               for projection, norm in zip(model.projections, model.norms, strict=True)]
    logits = q @ k.transpose(-1, -2) / math.sqrt(4)
    causal = torch.ones(5, 5, dtype=torch.bool).triu(1)
    expected = model.output((logits.masked_fill(causal, -torch.inf).softmax(-1) @ v).transpose(1, 2).reshape(2, 5, 8))
    torch.testing.assert_close(model(stack), expected)
    before = model.routed_inputs(stack)
    with torch.no_grad():
        model.routes[0].base[0, 0] += 1
    after = model.routed_inputs(stack)
    assert not torch.equal(before[0], after[0])
    assert torch.equal(before[1], after[1]) and torch.equal(before[2], after[2])


def test_nonzero_dynamic_route_is_differentiable_and_attention_is_causal():
    model = DCAAttention(4, 2, heads=2)
    with torch.no_grad():
        for route in model.routes:
            route.dynamic.fill_(.1)
    stack = torch.rand(1, 4, 2, 4, requires_grad=True)
    output = model(stack)
    output.square().sum().backward()
    assert all(route.dynamic.grad is not None and route.dynamic.grad.abs().sum() > 0 for route in model.routes)
    future = stack.detach().clone()
    future[:, 2:] += 10
    torch.testing.assert_close(output.detach()[:, :2], model(future)[:, :2])
    assert stack.grad is not None and torch.isfinite(stack.grad).all()


@pytest.mark.parametrize("kwargs", [{"width": 0, "sources": 2}, {"width": 4, "sources": True}])
def test_invalid_router_dimensions(kwargs):
    with pytest.raises(ValueError):
        GRN3(**kwargs)


def test_invalid_history_and_attention_shapes():
    with pytest.raises(ValueError):
        history_stack([])
    with pytest.raises(ValueError):
        history_stack([torch.ones(2), torch.ones(3)])
    with pytest.raises(ValueError):
        history_stack([torch.ones(2)], keep_last=True)
    with pytest.raises(ValueError):
        DCAAttention(5, 2, heads=2)
    with pytest.raises(ValueError):
        DCAAttention(4, 2)(torch.ones(1, 3, 3, 4))
    with pytest.raises(ValueError):
        GRN3(4, 2)(torch.full((2, 4), float("nan")))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic(seed):
    result = diagnostic(seed)
    assert result["evaluation_tier"] == "l1_mechanism" and result["diagnostic_only"]
    assert result["checks"] and all(result["checks"].values())
    assert all(math.isfinite(x) for x in result["metrics"].values())
