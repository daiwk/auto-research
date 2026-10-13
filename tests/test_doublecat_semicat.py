from dataclasses import replace

import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models.doublecat_semicat import DiffusionLM, corrupt, denoising_loss, sample


def test_two_level_interpolant_and_simplex_prior():
    tokens = torch.tensor([[1, 2, 3], [2, 4, 0]])
    time = torch.tensor([.2, .8])
    corruption = corrupt(tokens, 5, time, method="doublecat",
                          generator=torch.Generator().manual_seed(7))
    torch.testing.assert_close(corruption.simplex_prior.sum(-1), torch.ones_like(tokens).float())
    gamma, kappa = time[:, None, None], time[:, None, None].sqrt()
    expected = ((1 - gamma) * corruption.noise
                + gamma * (1 - kappa) * corruption.simplex_prior
                + gamma * kappa * F.one_hot(tokens, 5).float())
    torch.testing.assert_close(corruption.state, expected)


def test_semicat_endpoint_reveals_and_masked_ce():
    tokens = torch.randint(0, 5, (2, 3))
    corruption = corrupt(tokens, 5, torch.ones(2), method="semicat")
    assert corruption.revealed.all()
    torch.testing.assert_close(corruption.state, F.one_hot(tokens, 5).float())
    model = DiffusionLM(vocabulary=5, width=16, layers=1, heads=2, length=3)
    loss = denoising_loss(model, tokens, corruption)
    loss.backward()
    assert float(loss.detach()) == 0


def test_real_diffusion_gradient_and_bidirectional_attention():
    torch.manual_seed(5)
    model = DiffusionLM(vocabulary=8, width=16, layers=1, heads=2, length=4)
    tokens = torch.randint(0, 8, (2, 4))
    corruption = corrupt(tokens, 8, torch.tensor([.2, .6]), method="semicat")
    denoising_loss(model, tokens, corruption).backward()
    assert float(model.output.weight.grad.norm()) > 0
    original = corruption.state.clone()
    altered = original.clone()
    altered[:, -1] += 1
    with torch.no_grad():
        first = model(original, corruption.time)[:, 0]
        second = model(altered, corruption.time)[:, 0]
    assert not torch.equal(first, second)  # last position influences first, not AR proxy


@pytest.mark.parametrize("self_conditioning", [False, True])
def test_sampling_carries_revealed_tokens_and_finishes_without_extra_nfe(self_conditioning):
    model = DiffusionLM(vocabulary=8, width=16, layers=1, heads=2, length=4,
                        self_conditioning=self_conditioning)
    calls = []
    handle = model.register_forward_pre_hook(lambda _model, inputs: calls.append(inputs[2]))
    ids, stats = sample(model, 2, 4, method="semicat", steps=4,
                        generator=torch.Generator().manual_seed(3))
    handle.remove()
    assert len(calls) == stats["nfe"] == 4
    assert calls[0] is None
    if self_conditioning:
        assert all(condition is not None and not condition.requires_grad for condition in calls[1:])
    else:
        assert all(condition is None for condition in calls)
    assert ids.shape == (2, 4)
    assert stats["revealed_counts"][-1] == 8
    assert stats["revealed_counts"] == sorted(stats["revealed_counts"])
    assert stats["previously_revealed_changes"] == 0


@pytest.mark.parametrize("method", ["onehot", "doublecat", "semicat"])
def test_default_core_training_uses_exactly_one_denoiser_evaluation(method):
    model = DiffusionLM(vocabulary=8, width=16, layers=1, heads=2, length=4)
    assert model.self_conditioning is False and model.self_condition is None
    tokens = torch.randint(0, 8, (2, 4))
    corruption = corrupt(tokens, 8, torch.tensor([.2, .6]), method=method,
                          generator=torch.Generator().manual_seed(17))
    calls = []
    handle = model.register_forward_pre_hook(lambda _model, inputs: calls.append(
        (torch.is_grad_enabled(), inputs[2])))
    denoising_loss(model, tokens, corruption).backward()
    handle.remove()
    assert calls == [(True, None)]
    assert model.output.weight.grad is not None and model.output.weight.grad.norm() > 0


def test_standard_self_conditioning_is_explicit_detached_two_forward_ablation():
    model = DiffusionLM(vocabulary=8, width=16, layers=1, heads=2, length=4,
                        self_conditioning=True)
    tokens = torch.randint(0, 8, (2, 4))
    corruption = corrupt(tokens, 8, torch.tensor([.2, .6]), method="doublecat")
    calls = []
    handle = model.register_forward_pre_hook(lambda _model, inputs: calls.append(
        (torch.is_grad_enabled(), inputs[2] if len(inputs) == 3 else None)))
    denoising_loss(model, tokens, corruption, use_self_condition=False).backward()
    assert calls == [(True, None)]  # having an SC projection does not activate it
    model.zero_grad()
    calls.clear()
    denoising_loss(model, tokens, corruption, use_self_condition=True).backward()
    handle.remove()
    assert len(calls) == 2 and [enabled for enabled, _ in calls] == [False, True]
    assert calls[0][1] is None and calls[1][1] is not None
    assert calls[1][1].requires_grad is False
    assert model.self_condition.weight.grad.norm() > 0


def test_appendix_l2_weighting_is_detached_and_training_sums_masked_positions():
    class FixedDenoiser(torch.nn.Module):
        vocabulary, self_conditioning = 3, False

        def __init__(self):
            super().__init__()
            self.logits = torch.nn.Parameter(torch.tensor([
                [[1., -1., .5], [.2, .5, 0.], [-.5, 1., 0.]],
                [[.2, 1., -.1], [0., .1, .5], [1., .5, -.5]]]))

        def forward(self, _state, _time, _condition=None):
            return self.logits

    model = FixedDenoiser()
    tokens = torch.tensor([[0, 1, 2], [1, 2, 0]])
    corruption = corrupt(tokens, 3, torch.tensor([.3, .7]), method="semicat")
    corruption = replace(corruption, revealed=torch.tensor([[False, True, False], [True, True, False]]))
    ce = F.cross_entropy(model.logits.flatten(0, 1), tokens.flatten(), reduction="none").reshape_as(tokens)
    delta = (model.logits.softmax(-1) - F.one_hot(tokens, 3)).norm(dim=-1).add(1e-2).sqrt()
    valid = ~corruption.revealed
    expected = (ce / delta.detach() * valid).sum() / len(tokens)
    actual = denoising_loss(model, tokens, corruption)
    torch.testing.assert_close(actual, expected)
    actual_grad = torch.autograd.grad(actual, model.logits, retain_graph=True)[0]
    torch.testing.assert_close(actual_grad, torch.autograd.grad(expected, model.logits, retain_graph=True)[0])
    attached = (ce / delta * valid).sum() / len(tokens)
    assert not torch.allclose(actual_grad, torch.autograd.grad(attached, model.logits)[0])
    assert torch.count_nonzero(actual_grad[corruption.revealed]) == 0
    unweighted_metric = denoising_loss(model, tokens, corruption, l2_weighting=False,
                                      reduction="per_unrevealed_token")
    torch.testing.assert_close(unweighted_metric, (ce * valid).sum() / valid.sum())
