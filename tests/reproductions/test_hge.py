import pytest
import torch

from auto_research.reproductions.hge import HierarchicalGTV, diagnostic, proxy_value, residual_fusion


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_defining_mechanisms(seed):
    assert all(diagnostic(seed)["checks"].values())


def test_proxy_bernoulli_not_categorical_and_signed_residual():
    c = torch.tensor([0.5], dtype=torch.float64)
    p = torch.tensor([[0.8, 0.9]], dtype=torch.float64)
    q = torch.tensor([[2., 3.]], dtype=torch.float64)
    price = torch.tensor([[10., 20.]], dtype=torch.float64)
    assert proxy_value(c, p, q, price).item() == pytest.approx(35.)
    x = torch.tensor([1.])
    assert residual_fusion(x, x * -4, x * 8, x).item() == -3


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -1.])
def test_invalid_price(bad):
    with pytest.raises(ValueError):
        proxy_value(torch.ones(1), torch.ones(1, 2), torch.ones(1, 2), torch.tensor([[bad, 1.]]))


@pytest.mark.parametrize("shape", [(1, 2, 2), (0, 2), (1, 0)])
def test_invalid_proxy_shapes(shape):
    with pytest.raises(ValueError):
        proxy_value(torch.ones(1), torch.ones(shape), torch.ones(shape), torch.ones(shape))


@pytest.mark.parametrize("alpha", [-0.1, 1.1, float("nan")])
def test_invalid_gate(alpha):
    with pytest.raises(ValueError):
        residual_fusion(torch.ones(1), torch.ones(1), torch.ones(1), torch.tensor([alpha]))


@pytest.mark.parametrize("dims", [(8, 4, 3, 16), (True, 4, 1, 16), (8, 4, 2, 0), (512, 512, 1, 512)])
def test_cost_and_dimension_gate(dims):
    with pytest.raises(ValueError):
        HierarchicalGTV(*dims)


def test_context_does_not_enter_mhsa_and_heads_are_shared():
    torch.manual_seed(42)
    model = HierarchicalGTV(8, 4, 2, 16).double()
    items, positions, context = torch.randn(2, 3, 8).double(), torch.randn(2, 3, 8).double(), torch.randn(2, 4).double()
    args = (torch.ones(2, 3).double(), torch.ones(2).double())
    a = model(items, positions, context, *args)
    b = model(items, positions, context + 10, *args)
    assert torch.equal(a["item_attention"], b["item_attention"])
    assert not torch.allclose(a["value"], b["value"])
    order = torch.tensor([2, 0, 1])
    permuted = model(items[:, order], positions[:, order], context, *args)
    torch.testing.assert_close(permuted["item_probability"], a["item_probability"][:, order])
    torch.testing.assert_close(permuted["value"], a["value"])


def test_wrong_dtype_and_broadcast_are_rejected():
    model = HierarchicalGTV(8, 4, 2, 16)
    with pytest.raises(ValueError):
        model(torch.ones(1, 2, 8), torch.ones(2, 8), torch.ones(1, 4), torch.ones(1, 2), torch.ones(1))
    with pytest.raises(ValueError):
        proxy_value(torch.ones(1), torch.ones(1, 2).double(), torch.ones(1, 2), torch.ones(1, 2))
