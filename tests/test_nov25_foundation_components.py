import math

import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models import thresholded_longce as tlce
from auto_research.foundation_models.udvr import UDVPair, diagnostic, learning_rates, rebalance


def factors():
    g = torch.Generator().manual_seed(11)
    return torch.randn(5, 3, generator=g, dtype=torch.float64), torch.randn(3, 5, generator=g, dtype=torch.float64)


def test_udvr_attention_product_and_norms_match_independent_dense_reference():
    u, v = factors()
    d = torch.tensor([.4, -2., 3.], dtype=torch.float64)
    a, b, c = rebalance(u, d, v)
    torch.testing.assert_close(a @ torch.diag(b) @ c, u @ torch.diag(d) @ v, rtol=1e-14, atol=1e-14)
    torch.testing.assert_close(a.norm(dim=0), torch.full((3,), .01 * math.sqrt(5), dtype=u.dtype))
    torch.testing.assert_close(c.norm(dim=1), torch.full((3,), .01 * math.sqrt(5), dtype=u.dtype))


def test_udvr_ffn_drops_only_v_scale_and_does_not_claim_function_invariance():
    u, v = factors()
    d = torch.ones(3, dtype=u.dtype)
    a, b, c = rebalance(u, d, v, kind="ffn")
    torch.testing.assert_close(a * b, u * d)
    x = torch.ones(2, 5, dtype=u.dtype)
    assert not torch.allclose(F.gelu(x @ a * b) @ c, F.gelu(x @ u * d) @ v)
    _, attention_d, _ = rebalance(u, d, v)
    assert not torch.allclose(b, attention_d)


@pytest.mark.parametrize("kind", ["attention", "ffn"])
def test_udvr_exact_regularizer_and_buffer_excluded_from_adam(kind):
    u, v = factors()
    p = UDVPair(u, v, kind=kind)
    gamma = .2
    if kind == "attention":
        reference = gamma * ((p.u @ torch.diag(p.diagonal)).square().sum()
                             + (torch.diag(p.diagonal) @ p.v).square().sum())
    else:
        reference = 2 * gamma * ((p.u @ torch.diag(p.diagonal)).square().sum() + p.v.square().sum())
    torch.testing.assert_close(p.regularizer(gamma), reference)
    p.regularizer(gamma).backward()
    assert p.u.grad.abs().sum() > 0 and p.v.grad.abs().sum() > 0
    assert p.diagonal.grad is None and not p.diagonal.requires_grad
    assert set(dict(p.named_parameters())) == {"u", "v"}
    assert len(list(p.parameters())) == 2


def test_udvr_learning_rates_use_stacked_heads_and_only_ffn_ratio():
    assert learning_rates(64, 256) == learning_rates(128, 512)
    assert learning_rates(64, 256)["attention"] == pytest.approx(.000217)
    assert learning_rates(64, 256)["ffn"] == pytest.approx(.000434)
    assert learning_rates(64, 64)["ffn"] == learning_rates(64, 64)["attention"]


def test_udvr_rejects_zero_nonfinite_wrong_shapes_and_unadvertised_devices():
    u, v = factors()
    for bad in (u * 0, u * math.nan):
        with pytest.raises(ValueError):
            rebalance(bad, torch.ones(3, dtype=u.dtype), v)
    with pytest.raises(ValueError):
        rebalance(u, torch.ones(2), v)
    with pytest.raises(ValueError):
        diagnostic(42, "cuda")


def test_tlce_strict_delta_boundary_context_boundary_cap_and_valid_denominator():
    full = torch.tensor([[-2., -2., -2., -2., math.nan]], dtype=torch.float64, requires_grad=True)
    short = torch.tensor([[-3., -3.01, -3.01, -1000., math.nan]], dtype=torch.float64, requires_grad=True)
    offsets = torch.tensor([[128, 127, 128, 511, -1]])
    valid = torch.tensor([[True, True, True, True, False]])
    w = tlce.weights(full, short, offsets, valid)
    expected = torch.tensor([[1., 1., math.exp(1.01), 5., 0.]], dtype=torch.float64)
    torch.testing.assert_close(w, expected)
    value = tlce.loss(full, short, offsets, valid)
    assert value.item() == pytest.approx(2.)
    value.backward()
    torch.testing.assert_close(full.grad, -expected / expected.sum())
    assert short.grad is None and not w.requires_grad


def test_tlce_normalizes_by_total_weight_not_token_count():
    full, short = torch.tensor([[-1., -3.]]), torch.tensor([[-4., -3.]])
    offsets, valid = torch.tensor([[128, 129]]), torch.ones(1, 2, dtype=torch.bool)
    assert tlce.loss(full, short, offsets, valid).item() == pytest.approx(8 / 6)


class RecordingModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.scale = torch.nn.Parameter(torch.tensor(1.))
        self.calls = []

    def forward(self, x):
        self.calls.append((x.shape[1], torch.is_grad_enabled()))
        prefix = x.float().cumsum(1) * self.scale / 100
        return torch.stack([prefix, -prefix], -1)


def test_tlce_actual_short_forwards_reset_and_use_no_grad():
    model = RecordingModel()
    tokens, targets = torch.ones(1, 650, dtype=torch.int64), torch.zeros(1, 650, dtype=torch.int64)
    full, short, offsets = tlce.context_scores(model, tokens, targets)
    assert model.calls == [(650, True), (512, False), (138, False)]
    assert offsets[0, 511].item() == 511 and offsets[0, 512].item() == 0
    torch.testing.assert_close(short[:, 512], short[:, 0])
    assert not torch.equal(full[:, 512], short[:, 512]) and not short.requires_grad
    tlce.loss(full, short, offsets, torch.ones_like(tokens, dtype=torch.bool)).backward()
    assert torch.isfinite(model.scale.grad)


def test_tlce_all_invalid_mask_positive_logprob_and_invalid_window_are_rejected():
    p = torch.zeros(1, 3)
    offsets = torch.zeros(1, 3, dtype=torch.int64)
    with pytest.raises(ValueError):
        tlce.loss(p, p, offsets, torch.zeros(1, 3, dtype=torch.bool))
    with pytest.raises(ValueError):
        tlce.loss(p + .1, p, offsets, torch.ones(1, 3, dtype=torch.bool))
    with pytest.raises(ValueError):
        tlce.context_scores(RecordingModel(), offsets, offsets, window=513)
    with pytest.raises(ValueError):
        tlce.diagnostic(42, "cuda")


@pytest.mark.parametrize("seed", [42, 43, 44])
@pytest.mark.parametrize("run", [diagnostic, tlce.diagnostic])
def test_cpu_diagnostics_have_real_mechanism_checks_and_no_capability_claims(run, seed):
    result = run(seed)
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert all(result["checks"].values())
    assert all(math.isfinite(x) for x in result["metrics"].values())
