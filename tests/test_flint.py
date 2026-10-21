"""Formula, masking, residual and gradient contracts for FLINT's L1 component."""
from __future__ import annotations

import math

import pytest

torch = pytest.importorskip("torch")
from torch.nn import functional as F  # noqa: E402

from auto_research.foundation_models.flint import (  # noqa: E402
    FlintFixedBudgetRetrieval,
    FlintLatentPool,
    diagnostic,
    flint_maxsim,
    run_flint_diagnostic,
)


def _pool():
    torch.manual_seed(6)
    return FlintLatentPool(dim=8, num_latents=3, num_heads=2, ff_ratio=2, dropout=0).double()


def test_attention_formula_includes_both_pre_norm_residual_blocks():
    model = _pool()
    x = torch.randn(2, 5, 8, dtype=torch.double)
    mask = torch.tensor([[True, True, True, False, False], [True] * 5])
    latents = model.query_latents[None].expand(2, -1, -1)
    q = model.norm_latents_cross(latents)
    kv = model.norm_context_cross(x)
    weights = model.cross_attn.in_proj_weight.chunk(3)
    biases = model.cross_attn.in_proj_bias.chunk(3)
    projected = [F.linear(v, w, b).view(2, v.shape[1], 2, 4).transpose(1, 2)
                 for v, w, b in zip((q, kv, kv), weights, biases)]
    qp, kp, vp = projected
    logits = (qp @ kp.transpose(-1, -2)) / math.sqrt(4)
    attention = logits.masked_fill(~mask[:, None, None, :], -torch.inf).softmax(-1)
    combined = (attention @ vp).transpose(1, 2).reshape(2, 3, 8)
    attended = F.linear(combined, model.cross_attn.out_proj.weight,
                        model.cross_attn.out_proj.bias)
    hidden = latents + attended
    expected = hidden + model.ff(model.norm_ff(hidden))
    actual = model(x, mask, side="query")
    torch.testing.assert_close(actual, expected, rtol=1e-12, atol=1e-12)
    assert not torch.allclose(actual, attended)  # Not bare attention without residual/FFN.
    assert not torch.allclose(actual, expected.mean(1, keepdim=True).expand_as(expected))


def test_zero_attention_and_ff_preserves_learned_latents_without_post_norm():
    model = _pool()
    with torch.no_grad():
        model.cross_attn.out_proj.weight.zero_()
        model.cross_attn.out_proj.bias.zero_()
        model.ff[2].weight.zero_()
        model.ff[2].bias.zero_()
    x = torch.randn(2, 7, 8, dtype=torch.double)
    for side, parameter in (("query", model.query_latents), ("doc", model.doc_latents)):
        actual = model(x, side=side)
        torch.testing.assert_close(actual, parameter[None].expand(2, -1, -1))
        assert not torch.allclose(actual, F.layer_norm(actual, (8,)))


def test_fixed_budget_padding_and_token_permutation_contract():
    model = _pool().eval()
    x = torch.randn(2, 5, 8, dtype=torch.double)
    reference = model(x, side="query")
    long = torch.cat((x, torch.randn(2, 13, 8, dtype=torch.double)), dim=1)
    mask = torch.cat((torch.ones(2, 5, dtype=torch.bool), torch.zeros(2, 13, dtype=torch.bool)), dim=1)
    torch.testing.assert_close(model(long, mask, side="query"), reference)
    permutation = torch.tensor([3, 0, 4, 1, 2])
    torch.testing.assert_close(model(x[:, permutation], side="query"), reference)
    assert model(long, side="query").shape == reference.shape == (2, 3, 8)
    assert not torch.allclose(model(long, side="query"), reference)  # Valid content matters.


def test_masked_tokens_get_zero_gradient_and_both_sides_are_trainable():
    torch.manual_seed(4)
    model = FlintFixedBudgetRetrieval(8, 3, 2, 2, 0, 4).double()
    q = torch.randn(2, 4, 8, dtype=torch.double, requires_grad=True)
    d = torch.randn(2, 6, 8, dtype=torch.double, requires_grad=True)
    qm = torch.tensor([[True, True, False, False], [True, True, True, False]])
    dm = torch.tensor([[True, True, True, False, False, False], [True] * 6])
    model(q, d, qm, dm).sum().backward()
    assert torch.count_nonzero(q.grad[~qm]) == 0
    assert torch.count_nonzero(d.grad[~dm]) == 0
    assert q.grad[qm].norm() > 0 and d.grad[dm].norm() > 0
    for name, parameter in model.named_parameters():
        assert parameter.grad is not None, name
        assert torch.isfinite(parameter.grad).all(), name
        assert parameter.grad.norm() > 0, name


def test_query_and_document_latents_are_distinct_but_pooling_weights_shared():
    model = _pool()
    x = torch.randn(2, 4, 8, dtype=torch.double)
    query_before = model(x, side="query")
    doc_before = model(x, side="doc")
    assert model.query_latents is not model.doc_latents
    assert not torch.allclose(query_before, doc_before)
    with torch.no_grad():
        model.doc_latents.add_(0.1)
    torch.testing.assert_close(model(x, side="query"), query_before)
    assert not torch.allclose(model(x, side="doc"), doc_before)
    assert sum(isinstance(m, torch.nn.MultiheadAttention) for m in model.modules()) == 1


@pytest.mark.parametrize("shared", [True, False])
def test_backbone_specific_projection_sharing_and_normalization(shared):
    model = FlintFixedBudgetRetrieval(8, 3, 2, 2, 0, 4, shared_projection=shared).double()
    assert (model.query_projection is model.document_projection) is shared
    assert model.query_projection.bias is None and model.document_projection.bias is None
    encoded = model.encode(torch.randn(2, 7, 8, dtype=torch.double), side="query")
    assert encoded.shape == (2, 3, 4)
    torch.testing.assert_close(encoded.norm(dim=-1), torch.ones(2, 3, dtype=torch.double))


def test_maxsim_uses_sum_of_document_maxima_and_is_not_symmetric():
    q = torch.tensor([[[1., 0.], [1., 0.]]])
    d = torch.tensor([[[1., 0.], [0., 1.]]])
    assert flint_maxsim(q, d).item() == 2
    assert flint_maxsim(d, q).item() == 1
    assert flint_maxsim(q, d).item() != (q @ d.transpose(-1, -2)).mean().item()


def test_maxsim_gradient_follows_the_selected_document_vector():
    q = torch.tensor([[[1., 0.], [0., 1.]]], dtype=torch.double, requires_grad=True)
    d = torch.tensor([[[2., .1], [.2, 3.], [-1., -1.]]], dtype=torch.double, requires_grad=True)
    value = flint_maxsim(q, d)
    torch.testing.assert_close(value, torch.tensor([5.], dtype=torch.double))
    value.sum().backward()
    torch.testing.assert_close(d.grad, torch.tensor([[[1., 0.], [0., 1.], [0., 0.]]], dtype=torch.double))
    torch.testing.assert_close(q.grad, d.detach()[:, :2])


def test_maxsim_tie_gradient_matches_official_first_maximum_selection():
    q = torch.tensor([[[1., 0.]]], requires_grad=True)
    d = torch.tensor([[[1., 0.], [1., 0.]]], requires_grad=True)
    flint_maxsim(q, d).sum().backward()
    torch.testing.assert_close(d.grad, torch.tensor([[[1., 0.], [0., 0.]]]))


def test_full_component_passes_gradcheck():
    model = _pool()
    x = torch.randn(1, 3, 8, dtype=torch.double, requires_grad=True)
    assert torch.autograd.gradcheck(lambda values: model(values, side="query"), (x,), fast_mode=True)


@pytest.mark.parametrize("kwargs", [{"dim": 7, "num_heads": 2}, {"num_latents": 0},
                                    {"ff_ratio": float("nan")}, {"dropout": 1}])
def test_invalid_configuration_rejected(kwargs):
    with pytest.raises(ValueError):
        FlintLatentPool(**kwargs)


def test_invalid_masks_modes_and_nonfinite_inputs_rejected():
    model = _pool()
    x = torch.randn(2, 4, 8, dtype=torch.double)
    with pytest.raises(ValueError, match="unmasked"):
        model(x, torch.zeros(2, 4, dtype=torch.bool))
    with pytest.raises(ValueError, match="boolean"):
        model(x, torch.ones(2, 4))
    with pytest.raises(ValueError, match="boolean"):
        model(x, torch.ones(2, 3, dtype=torch.bool))
    with pytest.raises(ValueError, match="side"):
        model(x, side="document")
    x[0, 0, 0] = torch.nan
    with pytest.raises(ValueError, match="finite"):
        model(x)


def test_diagnostic_is_seeded_generated_only_and_not_promotable():
    a, b = run_flint_diagnostic(seed=42), run_flint_diagnostic(seed=42)
    assert a == b
    assert a["query_vectors"] == a["document_vectors"] == 4
    assert a["pairwise_comparisons_per_pair"] == 16
    assert a["all_parameter_gradients_finite"]
    assert a["parameter_gradient_norm"] > 0
    assert a["query_gradient_norm"] > 0 and a["document_gradient_norm"] > 0
    assert a["masked_query_gradient_max"] == a["masked_document_gradient_max"] == 0
    assert a["masked_content_score_error"] < 1e-6
    assert a["normalization_max_error"] < 1e-6
    assert a["diagnostic_only"] and not a["promotion_eligible"] and not a["evolve_integrated"]
    assert a["pretrained_checkpoint"] is None
    assert a["full_experiment_status"] == "not_reproduced_high_cost"


def test_cuda_request_never_falls_back_to_cpu(monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    with pytest.raises(RuntimeError, match="unavailable"):
        run_flint_diagnostic(device="cuda")


def test_unified_runner_interface_contains_finite_scalars_and_passing_checks():
    result = diagnostic(43, "cpu")
    assert result["seed"] == 43
    assert result["metrics"] and all(math.isfinite(v) for v in result["metrics"].values())
    assert result["checks"] and all(value is True for value in result["checks"].values())
