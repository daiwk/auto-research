"""Formula references and negative controls; no public capability scores."""
import hashlib
import inspect
import json
import math
from pathlib import Path

import pytest
import torch
from torch import nn
from torch.nn import functional as F

from auto_research.foundation_models import dt_jepa as dt
from auto_research.multimodal import uniaction as ua
from auto_research.system_one import editjev as ej


@pytest.mark.parametrize("module", [dt, ua, ej])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics(module, seed):
    result = module.diagnostic(seed)
    assert result["seed"] == seed
    assert all(type(v) is bool and v for v in result["checks"].values())
    assert all(type(v) in (int, float) and math.isfinite(v) for v in result["metrics"].values())
    assert module.REQUIRES_GPU_VALIDATION is True


def test_editjev_pair_mean_not_global_pair_mean():
    u = torch.tensor([[1., 2., 3.], [1., 4., 2.]], dtype=torch.float64, requires_grad=True)
    q = torch.tensor([[1., 2., 3.], [2., 2., 1.]], dtype=torch.float64)
    a = (F.softplus(u[0, 0]-u[0, 1]) + F.softplus(u[0, 0]-u[0, 2]) + F.softplus(u[0, 1]-u[0, 2])) / 3
    b = (F.softplus(u[1, 2]-u[1, 0]) + F.softplus(u[1, 2]-u[1, 1])) / 2
    assert torch.allclose(ej.pairwise_ranking_loss(u, q), (a+b)/2)
    assert not torch.allclose(ej.pairwise_ranking_loss(u, q), (a*3+b*2)/5)


def test_editjev_near_ties_empty_and_detached_labels():
    u = torch.randn(2, 3, requires_grad=True)
    q = torch.full((2, 3), 2., requires_grad=True)
    loss = ej.pairwise_ranking_loss(u, q)
    assert loss.item() == 0
    loss.backward()
    assert torch.equal(u.grad, torch.zeros_like(u)) and q.grad is None
    near = torch.tensor([[1., 1.49, 1.49]])
    assert ej.pairwise_ranking_loss(u[:1], near).item() == 0


def test_editjev_last_nonpadding_token_not_length_minus_one():
    head = ej.PreferenceHead(2, 2).double()
    with torch.no_grad():
        head.projection.weight.copy_(torch.eye(2))
        head.projection.bias.zero_()
    hidden = torch.arange(16, dtype=torch.float64).reshape(2, 4, 2)
    mask = torch.tensor([[False, True, False, True], [True, True, False, False]])
    actual = head(hidden, mask)
    assert torch.equal(actual, torch.stack((hidden[0, 3], hidden[1, 1])))
    actual.sum().backward()
    assert head.projection.weight.grad is not None
    with pytest.raises(ValueError):
        head(hidden, torch.zeros_like(mask))


def test_editjev_inference_no_oracle_and_equal_latency_rejected():
    assert set(inspect.signature(ej.route).parameters) == {"utilities", "mean_latencies", "beta"}
    with pytest.raises(ValueError, match="undefined"):
        ej.route(torch.zeros(1, 2), torch.ones(2), beta=1.)
    assert ej.route(torch.tensor([[9., 8.]]), torch.tensor([10., 1.]), beta=2.)["editor_indices"].item() == 1


@pytest.mark.parametrize("bad", [-1., float("inf"), float("nan")])
def test_editjev_rejects_bad_parameters(bad):
    with pytest.raises(ValueError):
        ej.pairwise_ranking_loss(torch.ones(2, 3), torch.ones(2, 3), delta=bad)
    with pytest.raises(ValueError):
        ej.route(torch.ones(2, 3), torch.tensor([1., 2., 3.]), beta=bad)


def test_editjev_four_ratings_min_and_not_product_of_all():
    x = torch.tensor([[[9., 4., 8., 1.], [1., 4., 9., 9.]]], requires_grad=True)
    assert torch.equal(ej.offline_quality(x), torch.tensor([[2., 3.]]))
    assert not ej.offline_quality(x).requires_grad
    with pytest.raises(ValueError):
        ej.offline_quality(x.detach() + 10)


def test_uniaction_semantic_reuse_native_position_explicit():
    model = ua.ActionTokens(3, 4)
    ids = torch.tensor([[1, 1, 2]])
    coords = torch.tensor([[[0., 0., 0.], [1., 2., 3.], [0., 0., 0.]]])
    calls = []
    def native(tokens, positions):
        calls.append(positions)
        return tokens + positions.sum(-1, keepdim=True)
    result = model(ids, coords, native)
    assert len(calls) == 1 and torch.equal(calls[0], coords)
    assert torch.allclose(result[:, 1]-result[:, 0], torch.full((1, 4), 6.))
    result.sum().backward()
    assert model.codebook.weight.grad[1].abs().sum() > 0
    with pytest.raises(ValueError):
        model(ids, coords, lambda t, p: t[..., :2])


def test_uniaction_mask_gradients_and_count_per_request():
    torch.manual_seed(4)
    q = torch.randn(2, 1, 2, 3, dtype=torch.float64)
    vk, vv = (torch.randn(2, 1, 4, 3, dtype=torch.float64) for _ in range(2))
    ak, av = (torch.randn(2, 1, 3, 3, dtype=torch.float64, requires_grad=True) for _ in range(2))
    mask = torch.tensor([[True, True, False], [True, False, False]])
    result = ua.cardinality_attention(q, vk, vv, ak, av, reference_cardinality=2., action_mask=mask)
    for b, count in enumerate([2, 1]):
        single = ua.cardinality_attention(q[b:b+1], vk[b:b+1], vv[b:b+1], ak[b:b+1, :, :count], av[b:b+1, :, :count], reference_cardinality=2.)
        assert torch.allclose(result["output"][b], single["output"][0], atol=1e-12, rtol=0)
    result["output"].sum().backward()
    expanded = mask[:, None, :, None].expand_as(ak)
    assert torch.equal(ak.grad[~expanded], torch.zeros_like(ak.grad[~expanded]))
    assert torch.equal(av.grad[~expanded], torch.zeros_like(av.grad[~expanded]))
    with pytest.raises(ValueError):
        ua.cardinality_attention(q, vk, vv, ak, av, reference_cardinality=2., action_mask=torch.zeros_like(mask))


@pytest.mark.parametrize("dtype", [torch.float32, torch.float64, torch.bfloat16])
def test_uniaction_forward_backward(dtype):
    q = torch.randn(1, 1, 2, 4, dtype=dtype, requires_grad=True)
    k, v = (torch.randn(1, 1, 3, 4, dtype=dtype, requires_grad=True) for _ in range(2))
    result = ua.cardinality_attention(q, k, v, k, v, reference_cardinality=3.)
    result["output"].square().sum().backward()
    assert all(torch.isfinite(t.grad).all() for t in (q, k, v))


def test_dt_gaussian_nll_sum_not_latent_mean_and_stop_gradient():
    mu = torch.tensor([[1., 2.], [3., 4.]], requires_grad=True)
    ls = torch.zeros_like(mu, requires_grad=True)
    target = torch.zeros_like(mu, requires_grad=True)
    expected = -torch.distributions.Normal(mu, ls.exp()).log_prob(target).sum(-1).mean()
    actual = dt.gaussian_future_nll(mu, ls, target)
    assert torch.allclose(actual, expected)
    actual.backward()
    assert target.grad is None and mu.grad.abs().sum() > 0


def test_dt_nll_rejects_overflow_not_clipped():
    with pytest.raises(ValueError, match="nonfinite"):
        dt.gaussian_future_nll(torch.zeros(1, 2), torch.full((1, 2), -1000.), torch.ones(1, 2))


def test_dt_multistep_min_discount_and_detached_target():
    r = torch.tensor([[1., 2., 3.]], requires_grad=True)
    q1, q2 = torch.tensor([4.], requires_grad=True), torch.tensor([9.], requires_grad=True)
    t = dt.multistep_td_targets(r, q1, q2, discount=.5)
    assert torch.equal(t, torch.tensor([[3.25, 4.5, 5.]])) and not t.requires_grad
    assert torch.equal(dt.multistep_td_targets(r, q1, q2, discount=0.), r.detach())
    prediction = torch.zeros(1, 3, requires_grad=True)
    loss = dt.critic_loss(prediction, t, torch.ones(1, 3, dtype=torch.bool))
    assert loss == t.square().sum()
    loss.backward()
    assert r.grad is None and q1.grad is None and q2.grad is None


def test_dt_actor_no_detach_oracle_inference_and_overflow():
    assert set(inspect.signature(dt.PredictiveFuture.forward).parameters) == {"self", "history", "dt_hidden", "noise"}
    q = torch.tensor([[1., 2.]], requires_grad=True)
    valid = torch.tensor([[True, False]])
    x = dt.adaptation_objective(torch.tensor(2.), torch.tensor(3.), q, valid, jepa_weight=.5, q_weight=2.)
    assert x["loss"].item() == 1.5
    x["loss"].backward()
    assert torch.equal(q.grad, torch.tensor([[-2., 0.]]))
    with pytest.raises(ValueError, match="finite"):
        dt.adaptation_objective(torch.tensor(1e30), torch.tensor(1e30), q, valid, jepa_weight=1e30, q_weight=0.)


def test_dt_masked_reduction_and_finite_guard():
    x = torch.ones(2, 3, 4)
    valid = torch.tensor([[True, True, True], [True, False, False]])
    assert dt.masked_sequence_sum_mean(x, valid).item() == 8.
    with pytest.raises(ValueError):
        dt.masked_sequence_sum_mean(torch.full((2, 3), float("nan")), valid)


def test_dt_ema_no_grad_and_buffer_rule_not_invented():
    class Gaussian(nn.Module):
        def forward(self, x):
            return x, x * 0
    model = dt.PredictiveFuture(nn.Linear(2, 2), Gaussian(), nn.Linear(2, 2), nn.Linear(2, 2), nn.Linear(2, 1))
    model.train()
    assert not model.target_encoder.training
    assert all(not p.requires_grad for p in model.target_encoder.parameters())
    with torch.no_grad():
        for p in model.encoder.parameters():
            p.fill_(3.)
    model.update_target(rho=0.)
    assert all(torch.equal(p, q) for p, q in zip(model.encoder.parameters(), model.target_encoder.parameters()))
    with pytest.raises(ValueError, match="buffer"):
        dt.PredictiveFuture(nn.BatchNorm1d(2), Gaussian(), nn.Identity(), nn.Identity(), nn.Identity())
    before = {name: p.detach().clone() for name, p in model.target_encoder.named_parameters()}
    model.encoder.register_buffer("unreported_buffer", torch.ones(1))
    with pytest.raises(ValueError, match="buffer"):
        model.update_target()
    assert all(torch.equal(p, before[name]) for name, p in model.target_encoder.named_parameters())


def test_dt_ema_schema_failure_leaves_all_parameters_unchanged():
    model = dt.PredictiveFuture(nn.Linear(2, 2), nn.Identity(), nn.Identity(), nn.Identity(), nn.Identity())
    before = {name: p.detach().clone() for name, p in model.target_encoder.named_parameters()}
    model.encoder.bias = nn.Parameter(torch.zeros(3))
    with pytest.raises(ValueError, match="schema"):
        model.update_target()
    assert all(torch.equal(p, before[name]) for name, p in model.target_encoder.named_parameters())


@pytest.mark.parametrize("domain,key", [
    ("foundation-models", "dt-jepa"), ("foundation-models", "editjev"),
    ("multimodal-models", "uniaction"), ("foundation-models", "lazyflash"),
    ("foundation-models", "pathjev"), ("multimodal-models", "flexglue"),
])
def test_paper_metadata_original_figure_and_honest_scope(domain, key):
    root = Path(__file__).resolve().parents[1]
    metadata = json.loads((root / f"src/auto_research/paper_specs/catalog/{domain}/{key}.json").read_text())
    folder = root / "docs" / Path(metadata["detail_path"]).parent
    doc = (folder / "README.md").read_text()
    assert metadata["paper_url"].endswith("v1") and metadata["published_at"].endswith("Z")
    assert metadata["reviewed_version"] == "v1" and metadata["announcement_date"] == "2026-10-26"
    assert metadata["first_author_affiliation"] and metadata["code_status"] and metadata["code_license"]
    assert "### 背景与主要改动" in doc and "图片来自[原论文]" in doc and "版权归原作者所有" in doc
    assert "paper-figure:start" in doc and "paper-figure:end" in doc
    assert "成本过高，不复现（审查 DONE）" in doc
    provenance = json.loads((folder / "assets/provenance.json").read_text())
    png = (folder / "assets/paper-figure-01.png").read_bytes()
    assert png.startswith(b"\x89PNG\r\n\x1a\n")
    assert provenance["visually_verified"] and hashlib.sha256(png).hexdigest() == provenance["image_sha256"]
    assert metadata["automatic_retry"] is False and metadata["evolve_integrated"] is False
    assert metadata["promotion_eligible"] is False and metadata["full_experiment_review_done"] is True
    if key in {"lazyflash", "pathjev", "flexglue"}:
        assert metadata["implementation_status"] == "deferred_high_cost"
        assert metadata["local_operator"] is None and metadata["local_command"] is None
        assert metadata["gpu_validation_passed"] is False and metadata["gpu_validation_artifact"] is None
        assert not (folder / "metrics").exists()
    else:
        assert metadata["implementation_status"] == "component_only"
        assert metadata["requires_gpu_validation"] is True and metadata["local_operator"]
