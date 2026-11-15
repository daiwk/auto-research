"""Formula, initialization and negative controls; no model capability claims."""
import math

import pytest
import torch

from auto_research.foundation_models import archspace, d_jepa, duojepa, unbundling_vision


@pytest.mark.parametrize("qkvo", [True, False])
def test_unbundling_zero_init_and_modality_mask(qkvo):
    block = unbundling_vision.InFusionBlock(8, 12, qkvo=qkvo)
    x = torch.randn(2, 5, 8)
    visual = torch.ones(2, 5, dtype=torch.bool)
    assert torch.equal(block(x, visual), block(x, visual, added_capacity=False))
    with torch.no_grad():
        block.vision_ffn.down.bias.fill_(2)
    text_only = torch.zeros_like(visual)
    assert torch.equal(block(x, text_only), block(x, text_only, added_capacity=False))
    assert not torch.equal(block(x, visual), block(x, visual, added_capacity=False))
    with pytest.raises(ValueError):
        block(x, visual.float())


def test_unbundling_both_ffns_receive_same_normalized_input():
    block = unbundling_vision.InFusionBlock(8, 12)
    seen = []
    handles = [m.register_forward_pre_hook(lambda module, args: seen.append(args[0].detach().clone()))
               for m in [block.ffn, block.vision_ffn]]
    block(torch.randn(2, 4, 8), torch.ones(2, 4, dtype=torch.bool))
    for handle in handles:
        handle.remove()
    assert torch.equal(*seen)


@pytest.mark.parametrize("law", [archspace.QWEN35, archspace.OLMO3])
def test_archspace_conditional_lr_and_budget_not_parameter_count(law):
    m, d = law.budget_optimum(3e19)
    assert m * d == pytest.approx(3e19)
    lr, batch = law.recipe(m, d)
    base = law.base_loss(m, d)
    assert law.loss(m, d, lr, batch) == pytest.approx(base)
    assert law.loss(m, d, lr * 3, batch * 9) < law.loss(m, d, lr, batch * 9)
    for wrong in [0, -1, math.nan, math.inf]:
        with pytest.raises(ValueError):
            law.base_loss(wrong, d)
    with pytest.raises(ValueError):
        archspace.diagnostic(42, "cuda")


def test_d_jepa_no_private_to_private_penalty_and_sample_correlation():
    # Columns of these two centered subspaces are exactly orthogonal.
    private = torch.tensor([[1., 0.], [-1., 0.], [0., 1.], [0., -1.]])
    shared = torch.tensor([[1., 1.], [1., -1.], [-1., -1.], [-1., 1.]])
    # Explicitly verify the four terms, not a generic all-pairs decorrelation.
    actual = d_jepa.independence(shared, private, shared, private)
    four = 4 * d_jepa.correlation_penalty(private, shared)
    assert torch.allclose(actual, four)
    assert d_jepa.correlation_penalty(private, private) > 0
    assert not torch.allclose(actual, four + d_jepa.correlation_penalty(private, private))
    with pytest.raises(ValueError):
        d_jepa.correlation_penalty(private[:1], shared[:1])


def test_d_jepa_separate_sigreg_and_stop_gradient():
    torch.manual_seed(2)
    cv, uv, ct, ut = [torch.randn(8, 3, requires_grad=True) for _ in range(4)]
    targets = [torch.randn(8, 4, requires_grad=True) for _ in range(2)]
    predictions = [torch.randn(8, 4, requires_grad=True) for _ in range(2)]
    directions = torch.randn(3, 5)
    result = d_jepa.objective(cv, uv, ct, ut, invariance_loss=cv.new_zeros(()),
                             predicted_v=predictions[0], target_v=targets[0],
                             predicted_t=predictions[1], target_t=targets[1], directions=directions)
    separate = .5 * sum(d_jepa.sigreg(x, directions) for x in (cv, ct, uv, ut))
    assert torch.allclose(result["sigreg"], separate)
    result["total"].backward()
    assert all(x.grad is None for x in targets)
    assert all(x.grad is not None for x in [cv, uv, ct, ut, *predictions])


def test_duojepa_translation_uses_other_target_space_and_both_target_gradients():
    torch.manual_seed(3)
    a, b, ta, tb = [torch.randn(4, 2, 5, requires_grad=True) for _ in range(4)]
    loss = duojepa.target_space_loss(a, b, ta, tb)
    # A paired batch permutation leaves the loss invariant; shuffling only
    # target identities destroys the pairing. Own-space cosine isn't the loss.
    permutation = torch.tensor([2, 0, 3, 1])
    paired = duojepa.target_space_loss(*(x[permutation] for x in (a, b, ta, tb)))
    unpaired = duojepa.target_space_loss(a[permutation], b, ta, tb)
    assert torch.allclose(loss, paired)
    assert not torch.allclose(loss, unpaired)
    loss.backward()
    assert all(x.grad is not None and x.grad.norm() > 0 for x in (a, b, ta, tb))


def test_duojepa_skipless_initialization_and_absence_of_identity_route():
    layer = duojepa.SkiplessTranslator(8)
    assert torch.allclose(layer.q @ layer.k.T, layer.initial_qk_product, atol=2e-5)
    assert torch.allclose(layer.v @ layer.v.T, 9 * torch.eye(8), atol=2e-5)
    with torch.no_grad():
        layer.mlp[2].weight.zero_()
        layer.mlp[2].bias.zero_()
    x = torch.randn(2, 3, 8)
    assert torch.equal(layer(x), torch.zeros_like(x))


@pytest.mark.parametrize("module", [unbundling_vision, archspace, d_jepa, duojepa])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_bounded_components_are_diagnostics(module, seed):
    result = module.diagnostic(seed, device="cpu")
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(result["checks"].values())
    assert all(math.isfinite(v) for v in result["metrics"].values())
