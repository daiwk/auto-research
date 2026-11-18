"""Independent equation, gradient, candidate-set and leakage-boundary checks."""
from dataclasses import FrozenInstanceError

import numpy as np
import pytest
import torch
from torch.nn import functional as F

from auto_research.foundation_models import real_loss
from auto_research.multimodal import c2_routing, onlyact


def test_real_path_and_rb_match_exact_tree_and_reverse_wtv_gradient():
    theta = torch.tensor(.5, dtype=torch.float64, requires_grad=True)
    first = torch.tensor(.8, dtype=torch.float64, requires_grad=True)
    terms, _ = real_loss.counterexample(theta, first)
    # Independently enumerate propose-and-accept mass, not estimator path weights.
    overlap1 = .4 + (1 - first)
    tree = overlap1 + .4 * (.1 + theta) + (1 - first) * (1.1 - theta)
    assert float(terms["branch"].detach()) == pytest.approx(float(tree.detach()))
    assert float(terms["path"].detach()) == pytest.approx(float(tree.detach()))
    assert torch.allclose(torch.autograd.grad(terms["branch"], (theta, first), retain_graph=True)[0],
                          torch.autograd.grad(tree, theta, retain_graph=True)[0])
    assert float(torch.autograd.grad(terms["branch"], first, retain_graph=True)[0]) == pytest.approx(-1.6)
    assert float(torch.autograd.grad(terms["wtv"], theta)[0]) == pytest.approx(-.12)


def test_real_prefix_mask_fixed_gamma_and_frozen_target():
    logits = torch.tensor([[[1., 0.], [0., 1.], [3., 0.]]], requires_grad=True)
    target = logits.detach().clone().requires_grad_()
    tokens = torch.tensor([[0, 1, 0]])
    mask = torch.tensor([[True, True, False]])
    terms = real_loss.eal_terms(logits, target, tokens, mask)
    assert terms["branch"].item() == pytest.approx(2)
    assert real_loss.real_loss(logits, target, tokens, mask, mixture=1).item() == pytest.approx(1 / 3)
    real_loss.real_loss(logits, target, tokens, mask).backward()
    assert target.grad is None
    assert torch.equal(logits.grad[:, 2], torch.zeros_like(logits.grad[:, 2]))
    with pytest.raises(ValueError, match="prefix"):
        real_loss.eal_terms(logits, target, tokens, torch.tensor([[True, False, True]]))


def test_real_gradient_matches_finite_differences_off_ties():
    generator = torch.Generator().manual_seed(44)
    target = torch.randn(2, 3, 4, generator=generator, dtype=torch.float64)
    draft = torch.randn(2, 3, 4, generator=generator, dtype=torch.float64, requires_grad=True)
    tokens = torch.tensor([[1, 2, 3], [0, 1, 2]])
    mask = torch.tensor([[True, True, True], [True, True, False]])
    assert torch.autograd.gradcheck(lambda q: real_loss.real_loss(q, target, tokens, mask), (draft,))


def test_onlyact_bank_has_own_hard_negative_and_exactly_one_self_exclusion():
    allowed, targets = onlyact.bank_contract(2)
    assert allowed.shape == (4, 6)
    assert targets.tolist() == [2, 3, 0, 1]
    assert allowed.sum(-1).tolist() == [5] * 4
    assert allowed[:, 4:].all()  # all hard negatives, including own same-video pair
    assert not allowed[torch.arange(4), torch.arange(4)].any()


def test_onlyact_independent_loss_and_symmetry():
    generator = torch.Generator().manual_seed(42)
    a, p, h = [F.normalize(torch.randn(2, 5, generator=generator, dtype=torch.float64), dim=-1)
               for _ in range(3)]
    bank = list(a) + list(p) + list(h)
    terms = []
    for i in range(4):
        numerator = torch.exp(bank[i] @ bank[(i + 2) % 4] / .3)
        denominator = sum(torch.exp(bank[i] @ bank[j] / .3) for j in range(6) if j != i)
        terms.append(-torch.log(numerator / denominator))
    assert onlyact.contrastive_loss(a, p, h, .3) == pytest.approx(float(torch.stack(terms).mean()))
    assert torch.allclose(onlyact.contrastive_loss(a, p, h), onlyact.contrastive_loss(p, a, h))


def test_onlyact_fixed_projection_and_same_video_nonoverlap_contract():
    tokens = torch.randn(2, 4, 6, dtype=torch.float64, requires_grad=True)
    projection = torch.randn(3, 6, dtype=torch.float64, requires_grad=True)
    output = onlyact.pooled_action(tokens, projection)
    assert torch.allclose(output.norm(dim=-1), torch.ones(2, dtype=torch.float64))
    output[:, 0].sum().backward()
    assert tokens.grad is not None and projection.grad is None
    anchor = onlyact.PairWindow("one-video", 0, 4)
    onlyact.validate_hard_negative(anchor, onlyact.PairWindow("one-video", 4, 8))
    for negative in (onlyact.PairWindow("another-video", 4, 8), onlyact.PairWindow("one-video", 3, 7)):
        with pytest.raises(ValueError, match="SAME video"):
            onlyact.validate_hard_negative(anchor, negative)


def test_c2_joint_harm_benefit_are_not_reduced_error_probability():
    policy = c2_routing.SafetyPolicy(0, {"R": .5, "C256": .25, "C512": .5})
    assert policy.decide("R", np.array([.1, 0, 0, .9])) == "R"  # shared failures not fixed by fallback
    assert policy.decide("R", np.array([.1, .1, .7, .1])) == "R"  # benefit credited
    assert policy.decide("R", np.array([.1, .7, .1, .1])) == "F"
    assert policy.decide("R", np.array([.4, .1, .1, .4])) == "R"  # inclusive threshold
    with pytest.raises(TypeError):
        policy.cost_ratios["R"] = .9
    with pytest.raises(FrozenInstanceError):
        policy.tradeoff = .2


def test_c2_validation_macro_ratio_rejects_test_data():
    original = np.array([1., 100., 1.])
    reduced = np.array([.1, 50., .9])
    expected = ((50.1 / 101) + .9) / 2
    actual = c2_routing.validation_cost_ratio(reduced, original, ["a", "a", "b"], split="validation")
    assert actual == pytest.approx(expected)
    assert actual != pytest.approx(np.mean(reduced / original))
    assert actual != pytest.approx(reduced.sum() / original.sum())
    with pytest.raises(ValueError, match="validation"):
        c2_routing.validation_cost_ratio(reduced, original, ["a", "a", "b"], split="test")
    with pytest.raises(ValueError):
        c2_routing.SafetyPolicy(.1, {"R": .5, "C256": .25, "C512": .5}, fitted_split="test")


@pytest.mark.parametrize("module", [real_loss, c2_routing, onlyact])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostics_remain_finite_l1(module, seed):
    result = module.diagnostic(seed)
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert all(type(x) is bool and x for x in result["checks"].values())
    assert all(np.isfinite(x) for x in result["metrics"].values())


def test_c2_does_not_advertise_a_cuda_router():
    with pytest.raises(ValueError, match="CPU"):
        c2_routing.diagnostic(42, device="cuda")
