from copy import deepcopy
from types import SimpleNamespace

import pytest

torch = pytest.importorskip("torch")

from auto_research.post_training.recal import (
    coarsened_forward_kl, damage_weights, prune_gated_ffn, restricted_opd_loss, wanda_channel_score,
)


def test_coarsened_kl_keeps_tail_mass_not_topk_renormalization():
    t = torch.tensor([[.5, .3, .1, .1]])
    p = torch.tensor([[.1, .1, .4, .4]])
    actual = coarsened_forward_kl(t.log(), p.log(), topk=2)
    expected = .5 * torch.log(torch.tensor(5.)) + .3 * torch.log(torch.tensor(3.)) + .2 * torch.log(torch.tensor(.25))
    full = (t * (t.log() - p.log())).sum(-1)
    assert torch.allclose(actual, expected[None]) and bool((actual <= full + 1e-6).all())


def test_per_response_weights_exclude_prompt_padding_and_keep_zero_damage_uniform():
    mask = torch.tensor([[0, 1, 1], [0, 0, 1]], dtype=torch.bool)
    w = damage_weights(torch.tensor([[100., 1., 3.], [100., 100., 0.]]), mask)
    assert torch.allclose(w, torch.tensor([[0., .25, .75], [0., 0., 1.]]))
    score = wanda_channel_score(torch.ones(2, 3, 4), w, torch.ones(2, 4))
    assert torch.allclose(score, torch.full((4,), 2**.5))


def test_real_channel_deletion_equals_retained_gated_computation():
    mlp = SimpleNamespace(gate_proj=torch.nn.Linear(4, 8), up_proj=torch.nn.Linear(4, 8),
                          down_proj=torch.nn.Linear(8, 4), intermediate_size=8)
    original = deepcopy(mlp)
    x = torch.randn(3, 4)
    keep = torch.tensor([0, 3, 7])
    hidden = torch.nn.functional.silu(original.gate_proj(x)) * original.up_proj(x)
    expected = torch.nn.functional.linear(hidden[:, keep], original.down_proj.weight[:, keep],
                                           original.down_proj.bias)
    prune_gated_ffn(mlp, keep)
    actual = mlp.down_proj(torch.nn.functional.silu(mlp.gate_proj(x)) * mlp.up_proj(x))
    assert mlp.gate_proj.weight.shape == (3, 4) and mlp.down_proj.weight.shape == (4, 3)
    assert torch.allclose(actual, expected, atol=1e-6) and mlp.intermediate_size == 3


def test_restricted_opd_updates_student_only_and_keeps_original_vocab_gaps():
    s = torch.randn(2, 3, 8, requires_grad=True)
    t = torch.randn_like(s, requires_grad=True)
    loss = restricted_opd_loss(s, t, s.detach(), torch.ones(2, 3).bool(), topk=2)
    loss.backward()
    assert torch.isfinite(loss) and s.grad.abs().sum() > 0 and t.grad is None
