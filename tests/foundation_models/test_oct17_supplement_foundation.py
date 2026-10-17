"""Defining invariants, independent causal passes, gradients and negative controls."""
from dataclasses import replace

import pytest
import torch

from auto_research.foundation_models.langdit import (
    LangDiTDenoiser, corrupt_tokens, likelihood_shortcut, noise_coefficients,
    normalized_codebook, posterior_mean, training_self_condition,
)
from auto_research.foundation_models.prism_one import PrismOneScorer, choice_diagnostics, pack_options


@pytest.fixture(autouse=True)
def one_thread():
    previous = torch.get_num_threads()
    torch.set_num_threads(1)
    yield
    torch.set_num_threads(previous)


def test_prism_packed_matches_independent_causal_passes_and_permutations():
    torch.manual_seed(42)
    model = PrismOneScorer().double()
    prefix = torch.tensor([4, 5, 6])
    options = [torch.tensor([7, 8]), torch.tensor([9]), torch.tensor([10, 11, 12])]
    packed = pack_options(prefix, options)
    expected_positions = [0, 1, 2, 3, 4, 3, 3, 4, 5]
    assert packed.position_ids.tolist() == expected_positions
    assert not packed.allowed_attention[6:, 3:6].any()
    scores = model(packed)
    # Independent oracle never builds an option-isolation mask: ordinary causal
    # attention over context+ONE option, with physical positions starting at 0.
    reference = []
    for option in options:
        token_ids = torch.cat((prefix, option))
        hidden = model.token_embedding(token_ids) + model.position_embedding(torch.arange(len(token_ids)))
        allowed = torch.ones(len(token_ids), len(token_ids), dtype=torch.bool).tril()
        for block in model.blocks:
            hidden = block(hidden, allowed)
        logits = model.vocabulary_head(model.final_norm(hidden[-1]))
        reference.append(logits[model.yes_token] - logits[model.no_token])
    assert torch.allclose(scores, torch.stack(reference), atol=1e-12, rtol=1e-12)
    order = [2, 0, 1]
    reordered = model(pack_options(prefix, [options[i] for i in order]))
    assert torch.allclose(reordered, scores[order], atol=1e-12, rtol=1e-12)
    extended = model(pack_options(prefix, options + [torch.tensor([20, 21, 22, 23])]))
    diagnostics = choice_diagnostics(scores, extended)
    assert max(diagnostics.values()) < 1e-12
    extreme_extra = torch.cat((scores.detach(), torch.tensor([1e20], dtype=scores.dtype)))
    assert choice_diagnostics(scores.detach(), extreme_extra)["renormalized_original_probability_tv"] == 0
    # A causal concatenation without block isolation leaks earlier options.
    wrong = replace(packed, allowed_attention=torch.ones_like(packed.allowed_attention).tril())
    assert (model(wrong) - scores).abs().max() > 1e-5
    scores.sum().backward()
    assert model.token_embedding.weight.grad.norm() > 0


@pytest.mark.parametrize("prefix,options", [
    (torch.tensor([], dtype=torch.long), [torch.tensor([1])]),
    (torch.tensor([1]), []), (torch.tensor([1]), [torch.tensor([], dtype=torch.long)]),
    (torch.tensor([-1]), [torch.tensor([2])]), (torch.tensor([1]), [torch.tensor([2.])]),
])
def test_prism_rejects_invalid_inputs(prefix, options):
    with pytest.raises(ValueError):
        pack_options(prefix, options)


def test_prism_capacity_and_empty_choice_diagnostic_rejected():
    model = PrismOneScorer(vocabulary=5, max_positions=3)
    with pytest.raises(ValueError):
        model(pack_options(torch.tensor([1, 2]), [torch.tensor([3, 4])]))
    with pytest.raises(ValueError):
        model(pack_options(torch.tensor([1]), [torch.tensor([5])]))
    with pytest.raises(ValueError):
        choice_diagnostics(torch.tensor([]), torch.tensor([1.]))
    with pytest.raises(ValueError):
        choice_diagnostics(torch.tensor([float("nan")]), torch.tensor([1., 2.]))


def test_langdit_noise_and_normalized_spherical_codebook():
    raw = torch.tensor([[1., 2.], [-3., 4.]], dtype=torch.float64, requires_grad=True)
    codebook = normalized_codebook(raw)
    assert torch.allclose(codebook.norm(dim=-1), torch.full((2,), .1 * 2 ** .5, dtype=raw.dtype))
    gamma = torch.tensor([-2., 1.], dtype=torch.float64)
    alpha, sigma = noise_coefficients(gamma)
    assert torch.allclose(alpha.square() + sigma.square(), torch.ones_like(gamma))
    tokens = torch.tensor([[0, 1], [1, 0]])
    noise = torch.zeros(2, 2, 2, dtype=torch.float64)
    assert torch.equal(corrupt_tokens(codebook, tokens, gamma, noise), alpha[:, None, None] * codebook[tokens])
    with pytest.raises(ValueError):
        normalized_codebook(torch.zeros(3, 4))
    with pytest.raises(ValueError):
        noise_coefficients(torch.tensor([float("inf")]))


def test_langdit_shortcut_removes_only_explicit_codebook_gradient():
    torch.manual_seed(43)
    c = torch.randn(7, 4, dtype=torch.float64, requires_grad=True)
    gamma = torch.tensor([-.5, .7], dtype=torch.float64)
    z = torch.randn(2, 3, 4, dtype=torch.float64, requires_grad=True)
    gate = torch.tensor([.5, 2.], dtype=torch.float64)
    detached = likelihood_shortcut(z, gamma, c, gate)
    direct = likelihood_shortcut(z, gamma, c, gate, detach_codebook=False)
    a, s = noise_coefficients(gamma)
    reference = torch.stack([gate[b] * a[b] / s[b].square() * z[b] @ c.detach().t() for b in range(2)])
    assert torch.equal(detached, direct)
    assert torch.allclose(detached, reference, atol=1e-12)
    gz, gc = torch.autograd.grad(detached.square().sum(), (z, c), allow_unused=True)
    assert gz.norm() > 0 and gc is None
    # z's path to C remains trainable even though explicit C^T is detached.
    raw = c.detach().clone().requires_grad_()
    tokens = torch.tensor([[0, 1, 2], [3, 4, 5]])
    noisy = corrupt_tokens(raw, tokens, gamma, torch.zeros_like(z))
    actual = likelihood_shortcut(noisy, gamma, raw, gate)
    gradient = torch.autograd.grad(actual.square().mean(), raw)[0]
    assert torch.isfinite(gradient).all() and gradient.norm() > 0
    with pytest.raises(ValueError):
        likelihood_shortcut(z, gamma, c, gate, warmup=1.1)
    with pytest.raises(ValueError):
        likelihood_shortcut(z, torch.full((2,), -1e4, dtype=z.dtype), c, gate)


@pytest.mark.parametrize("dtype,amplitude", [
    (torch.float32, 1e20), (torch.float32, 1e-30),
    (torch.float64, 1e200), (torch.float64, 1e-200),
])
def test_langdit_codebook_extreme_scales_preserve_radius_and_finite_gradient(dtype, amplitude):
    raw = torch.full((2, 4), amplitude, dtype=dtype, requires_grad=True)
    result = normalized_codebook(raw)
    assert torch.allclose(result, torch.full_like(result, .1))
    assert torch.allclose(result.norm(dim=-1), torch.full((2,), .2, dtype=dtype))
    result[:, 0].sum().backward()
    assert torch.isfinite(raw.grad).all() and torch.count_nonzero(raw.grad) > 0


def test_langdit_entropy_gate_only_training_and_detaches_complete_bootstrap():
    c = torch.tensor([[1., 0.], [0., 2.], [3., 1.]], dtype=torch.float64, requires_grad=True)
    p = torch.tensor([[[1 / 3, 1 / 3, 1 / 3], [0., 1., 0.]]], dtype=torch.float64, requires_grad=True)
    weighted, confidence = training_self_condition(p, c)
    assert abs(float(confidence[0, 0, 0])) < 1e-12
    assert confidence[0, 1, 0] == 1
    assert torch.allclose(weighted[0, 0], torch.zeros(2, dtype=c.dtype), atol=1e-12)
    assert torch.equal(weighted[0, 1], c[1])
    assert not weighted.requires_grad and not confidence.requires_grad
    assert torch.equal(posterior_mean(p, c)[0, 0], c.mean(0))
    with pytest.raises(ValueError):
        posterior_mean(torch.ones_like(p), c)


def test_langdit_real_noise_backbone_train_step_and_calibration_bounds():
    torch.manual_seed(44)
    model = LangDiTDenoiser().double()
    tokens = torch.randint(19, (4, 6))
    gamma = torch.tensor([-1., -.3, .4, 1.], dtype=torch.float64)
    noise = torch.randn(4, 6, 16, dtype=torch.float64)
    mask = torch.tensor([True, False, False, False])
    before = model.raw_codebook.detach().clone()
    optimizer = torch.optim.SGD(model.parameters(), lr=.02)
    for _ in range(3):
        optimizer.zero_grad()
        logits, auxiliary = model.training_logits(tokens, gamma, noise, mask)
        assert not auxiliary.requires_grad and torch.count_nonzero(auxiliary[1:]) == 0
        loss = model.token_loss(logits, tokens)
        assert torch.isfinite(loss)
        loss.backward()
        assert all(p.grad is None or torch.isfinite(p.grad).all() for p in model.parameters())
        optimizer.step()
    assert (model.raw_codebook - before).norm() > 0
    assert model.blocks[0].qkv.weight.grad.norm() > 0
    z = corrupt_tokens(model.codebook(), tokens, gamma, noise)
    expected = model(z, gamma).softmax(-1) @ model.codebook()
    assert torch.allclose(model.inference_mean(z, gamma), expected)
    assert torch.equal(model(z, gamma, warmup=0), model(z, gamma, warmup=0, detach_shortcut=False))
    with torch.no_grad():
        model.calibration_mlp[-1].bias.fill_(1000)
    calibrated = model(z, gamma) - model(z, gamma, warmup=0)
    ungated = likelihood_shortcut(z, gamma, model.codebook(), torch.ones_like(gamma))
    assert torch.allclose(calibrated, 2 * ungated, atol=1e-10)
