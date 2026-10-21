import pytest
import torch

from auto_research.foundation_models.google16_robust_gate import (
    cached_router_nll, gated_mass, primal_dual_step, sir_resample,
)


def test_inputwise_expert_softmax_does_not_imply_global_normalization():
    experts = torch.tensor([[.9, .1], [.1, .9]])
    logits = torch.tensor([[10., -10.], [-10., 10.]])
    assert gated_mass(experts, logits).sum() == pytest.approx(1.8)


def test_three_player_practical_update_uses_nll_adversary_and_partition_dual():
    experts = torch.tensor([[.8, .2], [.1, .9]])
    domains = torch.tensor([[.7, .3], [.05, .95]])
    gate = torch.nn.Parameter(torch.tensor([[1., -1.], [-1., 1.]]))
    before = gate.detach().clone()
    mass = gated_mass(experts, gate).detach()
    nll = -(domains * mass.log()).sum(-1)
    expected_adversary = (.2 * nll).softmax(-1)
    expected_dual = .3 * (mass.sum() - 1)
    state = primal_dual_step(gate, experts, domains, torch.tensor([.5, .5]), torch.tensor(0.),
                            torch.optim.SGD([gate], lr=.01), adversary_lr=.2, dual_lr=.3)
    torch.testing.assert_close(state["adversary"], expected_adversary)
    torch.testing.assert_close(state["dual"], expected_dual)
    assert not torch.equal(before, gate) and gate.grad.norm() > 0


def test_unequal_domain_entropies_distinguish_practice_nll_from_theory_kl():
    experts = torch.tensor([[.5, .5], [.5, .5]])
    domains = torch.tensor([[.5, .5], [.99, .01]])
    outputs = {}
    for objective in ("nll", "kl"):
        gate = torch.nn.Parameter(torch.zeros(2, 2))
        outputs[objective] = primal_dual_step(
            gate, experts, domains, torch.tensor([.5, .5]), torch.tensor(0.),
            torch.optim.SGD([gate], lr=.01), adversary_lr=1., adversary_objective=objective)
    torch.testing.assert_close(outputs["nll"]["adversary"], torch.tensor([.5, .5]))
    # KL(domain || uniform) is larger for the lower-entropy second domain.
    assert outputs["kl"]["adversary"][1] > .65
    assert not torch.allclose(outputs["nll"]["adversary"], outputs["kl"]["adversary"])
    for state in outputs.values():
        entropy = -(domains * domains.log()).sum(-1)
        torch.testing.assert_close(state["domain_nll"] - state["domain_kl"], entropy)


def test_cached_logits_objective_is_mixture_likelihood_not_expert_average_nll():
    logits = torch.tensor([[[0., 0.]]], requires_grad=True)
    cached = torch.tensor([[[.9, .1]]], requires_grad=True)
    result = cached_router_nll(logits, cached.log())
    assert result.item() == pytest.approx(-torch.log(torch.tensor(.5)).item())
    result.backward()
    assert logits.grad.norm() > 0 and cached.grad is None


def test_sir_reproducibility_and_support():
    experts = torch.tensor([[.8, .1, .1], [.1, .1, .8]])
    logits = torch.zeros(3, 2)
    first = sir_resample(experts, logits, 16, 128, torch.Generator().manual_seed(42))
    second = sir_resample(experts, logits, 16, 128, torch.Generator().manual_seed(42))
    assert torch.equal(first, second)
    assert set(first.tolist()) <= {0, 1, 2}
    assert len(set(first.tolist())) == 3


def test_invalid_expert_normalization_and_empty_token_mask_rejected():
    with pytest.raises(ValueError):
        gated_mass(torch.ones(2, 3), torch.zeros(3, 2))
    with pytest.raises(ValueError):
        cached_router_nll(torch.zeros(1, 2, 2), torch.ones(1, 2, 2).log(), torch.zeros(1, 2, dtype=torch.bool))
