import itertools
from copy import deepcopy
from types import SimpleNamespace

import pytest
import torch

from auto_research.foundation.vfold import Alignment, ValueBanks, cca_map, fit_alignment, fold_attention, minimum_assignment


def test_hungarian_matches_exhaustive_cost():
    torch.manual_seed(3)
    cost = torch.rand(5, 5)
    selected = minimum_assignment(cost)
    got = sum(float(cost[i, j]) for i, j in enumerate(selected))
    best = min(sum(float(cost[i, j]) for i, j in enumerate(p)) for p in itertools.permutations(range(5)))
    assert got == pytest.approx(best)


def test_cca_permutation_recovers_related_heads_without_rank_truncation():
    torch.manual_seed(4)
    x = torch.randn(128, 3, 4, dtype=torch.double)
    rotation = torch.linalg.qr(torch.randn(4, 4, dtype=torch.double))[0]
    source = x[:, [2, 0, 1]] @ rotation
    result = fit_alignment(x, source)
    assert result.permutation == (1, 2, 0)
    aligned = torch.einsum("nhc,hcd->nhd", source[:, result.permutation], result.maps)
    torch.testing.assert_close(aligned, x, atol=2e-4, rtol=2e-4)
    assert (torch.linalg.matrix_rank(result.maps) == 4).all()
    t = cca_map(x[:, 0], source[:, 1])
    torch.testing.assert_close(t @ torch.linalg.inv(t), torch.eye(4, dtype=t.dtype))


@pytest.mark.parametrize("group", [1, 3])
def test_gqa_folding_preserves_attention_including_projection_biases(group):
    torch.manual_seed(7)
    heads, dim, hidden = 2, 4, 12
    attention = SimpleNamespace(q_proj=torch.nn.Linear(hidden, heads * group * dim, bias=True),
                                k_proj=torch.nn.Linear(hidden, heads * dim, bias=True),
                                v_proj=torch.nn.Linear(hidden, heads * dim, bias=True),
                                o_proj=torch.nn.Linear(heads * group * dim, hidden, bias=True))
    x = torch.randn(1, 8, hidden)

    def run():
        q = attention.q_proj(x).view(1, 8, heads * group, dim).transpose(1, 2)
        k = attention.k_proj(x).view(1, 8, heads, dim).transpose(1, 2).repeat_interleave(group, 1)
        v = attention.v_proj(x).view(1, 8, heads, dim).transpose(1, 2).repeat_interleave(group, 1)
        weights = (q @ k.transpose(-1, -2) / dim**.5).softmax(-1)
        return attention.o_proj((weights @ v).transpose(1, 2).reshape(1, 8, -1))

    before = run().detach()
    maps = torch.randn(heads, dim, dim) + 3 * torch.eye(dim)
    fold_attention(attention, Alignment((1, 0), maps, 0.), head_dim=dim,
                   query_heads=heads * group, kv_heads=heads)
    torch.testing.assert_close(run(), before, atol=1e-6, rtol=1e-5)


def test_current_values_consumed_before_merge_and_protection_moves_on_decode():
    banks = ValueBanks(2, sink=1, recent=2)
    a = torch.arange(12.).reshape(1, 1, 6, 2)
    b = a + 10
    ka, used_a = banks.update(0, a, a)
    torch.testing.assert_close(used_a, a)
    banks.finish_layer(0)
    kb, used_b = banks.update(1, b, b)
    torch.testing.assert_close(used_b, b)  # not average before this attention!
    banks.finish_layer(1)
    torch.testing.assert_close(banks.shared[0], (a[..., 1:4, :] + b[..., 1:4, :]) / 2)
    torch.testing.assert_close(banks.materialize(0)[..., :1, :], a[..., :1, :])
    torch.testing.assert_close(banks.materialize(1)[..., -2:, :], b[..., -2:, :])
    assert not banks.pending
    # 2 full keys + shared middle + 2 compact protected slices, no hidden full view.
    assert banks.persistent_bytes() == (24 + 6 + 12) * 4
    next_a = torch.full((1, 1, 1, 2), 50.)
    next_b = torch.full_like(next_a, 100.)
    _, current_a = banks.update(0, next_a, next_a)
    torch.testing.assert_close(current_a[..., -1:, :], next_a)
    banks.finish_layer(0)
    _, current_b = banks.update(1, next_b, next_b)
    torch.testing.assert_close(current_b[..., -1:, :], next_b)
    banks.finish_layer(1)
    torch.testing.assert_close(banks.shared[0][..., -1:, :], (a[..., 4:5, :] + b[..., 4:5, :]) / 2)
    torch.testing.assert_close(banks.materialize(0)[..., -1:, :], next_a)
    torch.testing.assert_close(banks.keys[0][..., :6, :], ka)
    torch.testing.assert_close(banks.keys[1][..., :6, :], kb)


def test_no_compression_when_entire_context_protected():
    banks = ValueBanks(2, sink=4, recent=128)
    x, y = torch.randn(1, 2, 8, 3), torch.randn(1, 2, 8, 3)
    for index, value in enumerate((x, y)):
        banks.update(index, value, value)
        banks.finish_layer(index)
    assert banks.shared[0].numel() == 0
    torch.testing.assert_close(banks.materialize(0), x)
    torch.testing.assert_close(banks.materialize(1), y)


def test_real_qwen_cache_bridge_decodes_protected_prefix_exactly():
    pytest.importorskip("transformers")
    from transformers import Qwen3Config, Qwen3ForCausalLM
    from auto_research.foundation.vfold import attach_finish_hooks
    from auto_research.foundation.vfold_cache import VFoldCache

    torch.manual_seed(11)
    config = Qwen3Config(hidden_size=32, intermediate_size=64, num_hidden_layers=2,
                        num_attention_heads=4, num_key_value_heads=2, head_dim=8,
                        vocab_size=128, max_position_embeddings=512)
    config._attn_implementation = "eager"
    original = Qwen3ForCausalLM(config).eval()
    model = deepcopy(original)
    maps = torch.randn(2, 8, 8) + 4 * torch.eye(8)
    fold_attention(model.model.layers[1].self_attn, Alignment((1, 0), maps, 0.),
                   head_dim=8, query_heads=4, kv_heads=2)
    hooks = attach_finish_hooks(model)
    ids = torch.randint(0, 128, (1, 8))
    try:
        with torch.no_grad():
            full = original(ids, use_cache=True)
            cache = VFoldCache(2, sink=4, recent=128)
            folded = model(ids, past_key_values=cache, use_cache=True)
            torch.testing.assert_close(folded.logits, full.logits, atol=1e-6, rtol=1e-5)
            token = torch.tensor([[17]])
            full = original(token, past_key_values=full.past_key_values, use_cache=True)
            folded = model(token, past_key_values=cache, use_cache=True)
            torch.testing.assert_close(folded.logits, full.logits, atol=1e-6, rtol=1e-5)
            assert cache.get_seq_length() == 9
            assert not cache.banks.pending
            assert all(layer.values.numel() == 0 for layer in cache.layers)
    finally:
        for handle in hooks:
            handle.remove()
