import math

import pytest
import torch

from auto_research.reproductions import camar_components as c
from auto_research.reproductions import onequery_components as q


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_industrial_diagnostics_use_real_mechanisms(seed):
    torch.set_num_threads(1)
    for module in (q, c):
        row = module.diagnostic(seed)
        assert row["seed"] == seed and row["device"] == "cpu"
        assert row["diagnostic_only"] and row["evaluation_tier"] == "l1_mechanism"
        assert all(row["checks"].values()), row["checks"]
        assert all(math.isfinite(x) for x in row["metrics"].values())


def example():
    return {"lang": "en", "spell": "red shoes", "trans": "red shoes", "qt": [("color", "red"), ("product", "shoes")]}


def test_onequery_normalization_is_nfkc_lower_and_whitespace():
    assert q.normalize("  ＡＢＣ\tShoes \n") == "abc shoes"
    with pytest.raises(TypeError):
        q.normalize(1)


def test_spelling_branch_penalizes_overcorrection_and_caps_partial_credit():
    target = example()
    assert q.reward("red shoes", target | {"spell": "red shoe"}, target)["spell"] == 0
    assert q.reward("red shose", target, target)["spell"] == 1
    assert q.reward("red shose", target | {"spell": "red shoe"}, target)["spell"] == pytest.approx(.3*(1-1/9))
    assert q.edit_similarity("", "") == 1


def test_qt_is_exact_normalized_set_not_f1_or_sequence_matching():
    target = example()
    reordered = target | {"qt": [("PRODUCT", "SHOES"), ("color", "red"), ("color", "red")]}
    assert q.reward("red shoes", reordered, target)["qt"] == 1
    assert q.reward("red shoes", target | {"qt": [("color", "red")]}, target)["qt"] == 0
    assert q.reward("red shoes", target | {"trans": "red footwear"}, target)["trans"] == 0
    with pytest.raises(TypeError):
        q.reward("red shoes", target | {"qt": "color:red"}, target)


def test_reward_weights_are_not_silently_renormalized():
    assert q.reward("red shoes", example(), example(), (1, 1, 1, 1))["total"] == 4
    for weights in ((0, 0, 0, 0), (1, 2), (1, -1, 0, 1), (1, 1, 1, float("nan"))):
        with pytest.raises(ValueError):
            q.reward("red shoes", example(), example(), weights)
    with pytest.raises(ValueError):
        q.reward("red shoes", {"lang": "en"}, example())


def test_group_and_clip_arithmetic_have_both_signs_and_validation():
    assert q.group_advantages((1, 1, 1)) == (0, 0, 0)
    assert q.group_advantages((1, 3)) == pytest.approx((-1, 1))
    assert q.clipped_objective((2, .5), (1, -1)) == pytest.approx(.2)
    for rewards in ((1,), (1, float("nan"))):
        with pytest.raises(ValueError):
            q.group_advantages(rewards)
    with pytest.raises(ValueError):
        q.clipped_objective((0,), (1,))
    with pytest.raises(ValueError, match="CPU-only"):
        q.diagnostic(42, "cuda")


def test_transnet_completes_only_inactive_and_detaches_both_rep_targets():
    core = c.PreferenceCore(3, 4).double()
    h = torch.randn(2, 3, 4, dtype=torch.float64, requires_grad=True)
    mask = torch.tensor([[True, True, False], [False, True, True]])
    out = core.complete(h, mask)
    assert torch.equal(out[mask], h[mask])
    expected = (core.pcn["0_2"](h[0, 0].detach()) + core.pcn["1_2"](h[0, 1].detach()))/2
    assert torch.allclose(out[0, 2], expected)
    grad = torch.autograd.grad(out[~mask].sum(), h)[0]
    assert torch.equal(grad, torch.zeros_like(h))
    loss = core.representation_loss(h, mask)
    loss.backward()
    assert h.grad is None
    assert any(p.grad is not None for p in core.pcn.parameters())


def test_camar_orthogonality_is_squared_raw_dot_not_cosine():
    core = c.PreferenceCore(3, 2).double()
    inv = torch.tensor([[[2., 0], [0, 3.], [1., 1.]]], dtype=torch.float64)
    spec = inv.clone()
    mask = torch.ones(1, 3, dtype=torch.bool)
    expected = torch.tensor((16+81+4)/3, dtype=torch.float64)
    assert torch.allclose(core.orthogonality_loss(inv, spec, mask), expected)


def test_grl_identity_forward_and_only_input_gradient_reversed():
    x = torch.tensor([1., 2.], requires_grad=True)
    weight = torch.tensor([2., 3.], requires_grad=True)
    y = c.reverse(x, .4)
    assert torch.equal(y, x)
    (y*weight).sum().backward()
    assert torch.allclose(x.grad, -.4*weight)
    assert torch.equal(weight.grad, x.detach())
    with pytest.raises(ValueError):
        c.reverse(x, 1.1)


def test_masks_and_domain_constraints_fail_closed():
    with pytest.raises(ValueError):
        c.PreferenceCore(2, 4)
    core = c.PreferenceCore(3, 4)
    h = torch.randn(2, 3, 4)
    with pytest.raises(ValueError):
        core(h, torch.zeros(2, 3, dtype=torch.bool))
    mask = torch.tensor([[True, False, False], [True, False, False]])
    with pytest.raises(ValueError, match="overlapping"):
        core.representation_loss(h, mask)


def test_camar_recall_is_sum_of_per_domain_means_and_first_is_positive():
    core = c.PreferenceCore(3, 2)
    users = torch.ones(2, 3, 2)
    items = torch.zeros(2, 3, 4, 2)
    active = torch.tensor([[True, True, False], [True, False, True]])
    assert core.recall_loss(users, items, active).item() == pytest.approx(3*math.log(4))
    items[:, :, 0] = 1
    assert core.recall_loss(users, items, active).item() < 3*math.log(4)
