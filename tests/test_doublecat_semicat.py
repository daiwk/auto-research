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
    loss = denoising_loss(model, tokens, corruption, use_self_condition=True)
    loss.backward()
    assert float(loss.detach()) == 0


def test_real_diffusion_gradient_and_bidirectional_attention():
    torch.manual_seed(5)
    model = DiffusionLM(vocabulary=8, width=16, layers=1, heads=2, length=4)
    tokens = torch.randint(0, 8, (2, 4))
    corruption = corrupt(tokens, 8, torch.tensor([.2, .6]), method="semicat")
    denoising_loss(model, tokens, corruption, use_self_condition=True).backward()
    assert float(model.output.weight.grad.norm()) > 0
    original = corruption.state.clone()
    altered = original.clone()
    altered[:, -1] += 1
    with torch.no_grad():
        first = model(original, corruption.time)[:, 0]
        second = model(altered, corruption.time)[:, 0]
    assert not torch.equal(first, second)  # last position influences first, not AR proxy


def test_sampling_carries_revealed_tokens_and_finishes():
    model = DiffusionLM(vocabulary=8, width=16, layers=1, heads=2, length=4)
    ids, stats = sample(model, 2, 4, method="semicat", steps=4,
                        generator=torch.Generator().manual_seed(3))
    assert ids.shape == (2, 4)
    assert stats["revealed_counts"][-1] == 8
    assert stats["revealed_counts"] == sorted(stats["revealed_counts"])
    assert stats["previously_revealed_changes"] == 0
