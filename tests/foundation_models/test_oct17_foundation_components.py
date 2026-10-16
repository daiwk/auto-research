"""Independent mathematics and adversarial bit-pattern contracts, not model quality."""
from __future__ import annotations

from dataclasses import replace
import itertools

import pytest
import torch

from auto_research.foundation_models.bit_sparse import (
    pack_activation, sparse_activation_linear, unpack_activation,
)
from auto_research.foundation_models.drop_kv import drop_kv_scores
from auto_research.foundation_models.lct import (
    _bounded_lengths, build_codebook, compress_bf16, decompress_bf16,
    gaussian_exponent_model, lct_linear,
)
from auto_research.foundation_models.mirror_moe import (
    MirrorMoELayer, cosine_mirror_ratio, mirror_routing,
)
from auto_research.foundation_models.roleq import exact_ternary_fit, quantize_by_role


def test_dropkv_exact_singleton_removal_and_gqa_mean():
    torch.manual_seed(3)
    q = torch.randn(1, 4, 2, 3, dtype=torch.float64)
    k = torch.randn(1, 2, 7, 3, dtype=torch.float64)
    v = torch.randn_like(k)
    result = drop_kv_scores(q, k, v, eviction_count=3)
    for kv in range(2):
        for index in range(5):
            score = 0.
            for head in range(2 * kv, 2 * kv + 2):
                for window in range(2):
                    available = list(range(6 + window))
                    retained = [i for i in available if i != index]
                    logits = q[0, head, window] @ k[0, kv].t() / (3 ** .5)
                    a = logits[available].softmax(0) @ v[0, kv, available]
                    b = logits[retained].softmax(0) @ v[0, kv, retained]
                    score += float((a - b).square().sum()) / 2
            assert float(result.scores[0, kv, index]) == pytest.approx(score, abs=1e-12)
    assert result.evicted_indices.shape == (1, 2, 3)
    assert (result.evicted_indices < 5).all()
    assert torch.isinf(result.scores[..., -2:]).all()


def test_dropkv_pooling_and_true_gradients():
    torch.manual_seed(7)
    q = torch.randn(1, 2, 2, 4, dtype=torch.float64, requires_grad=True)
    k = torch.randn(1, 1, 9, 4, dtype=torch.float64, requires_grad=True)
    v = torch.randn(1, 1, 9, 4, dtype=torch.float64, requires_grad=True)
    unpooled = drop_kv_scores(q, k, v, eviction_count=0)
    pooled = drop_kv_scores(q, k, v, eviction_count=2, pooling_kernel=3)
    assert (pooled.scores[..., :7] >= unpooled.scores[..., :7]).all()
    grads = torch.autograd.grad(pooled.scores[..., :7].sum(), (q, k, v))
    assert all(torch.isfinite(g).all() and g.norm() > 0 for g in grads)


@pytest.mark.parametrize("changes", [{"eviction_count": 8}, {"pooling_kernel": 2}])
def test_dropkv_rejects_invalid_capacity(changes):
    options = {"eviction_count": 1, **changes}
    with pytest.raises(ValueError):
        drop_kv_scores(torch.randn(1, 2, 2, 3), torch.randn(1, 1, 8, 3), torch.randn(1, 1, 8, 3), **options)


def test_dropkv_does_not_hide_singleton_singularity():
    with pytest.raises(ValueError, match="rounded-one"):
        drop_kv_scores(torch.tensor([[[[1000.]]]]), torch.tensor([[[[1000.], [-1000.]]]]),
                       torch.ones(1, 1, 2, 1), eviction_count=1)


def test_mirror_selects_mixed_distribution_but_aggregates_original():
    logits = torch.tensor([[4., 2., .3, -.3, -2., -4.]], dtype=torch.float64, requires_grad=True)
    result = mirror_routing(logits, top_k=3, ratio=.4)
    xi = logits.softmax(-1)
    expected = ((1 - .4) * xi + .4 * (-logits).softmax(-1)).topk(3, -1).indices
    assert torch.equal(result.selected, expected)
    assert torch.equal(result.aggregation_weights, xi.gather(-1, expected))
    assert not torch.allclose(result.aggregation_weights, result.selection_probabilities.gather(-1, expected))
    assert float(result.aggregation_weights.sum().detach()) < 1
    result.balancing_loss.backward()
    assert logits.grad.norm() > 0


def test_mirror_schedule_endpoints_and_actual_experts():
    assert cosine_mirror_ratio(0) == .4
    assert cosine_mirror_ratio(1) == 0
    with pytest.raises(ValueError):
        cosine_mirror_ratio(1.1)
    torch.manual_seed(1)
    layer = MirrorMoELayer(4, 6, 5, 2, 3).double()
    x = torch.randn(3, 4, dtype=torch.float64, requires_grad=True)
    y, info = layer(x, ratio=.4)
    expected = sum(expert(x) for expert in layer.shared)
    for token in range(3):
        for position in range(3):
            expert = int(info.selected[token, position])
            expected[token] += info.aggregation_weights[token, position] * layer.routed[expert](x[token])
    torch.testing.assert_close(y, expected)
    y.square().sum().backward()
    assert x.grad.norm() > 0 and layer.router.weight.grad.norm() > 0
    assert layer.shared[0][0].weight.grad.norm() > 0


@pytest.mark.parametrize("dtype", [torch.float64, torch.float32, torch.bfloat16])
def test_bit_sparse_padded_tiles_bitmask_prefix_and_roundtrip(dtype):
    x = torch.tensor([[0., 1., 0.], [2., 0., 3.], [0., 0., 4.]], dtype=dtype)
    packed = pack_activation(x, tile_size=4)
    assert packed.mask_bytes.dtype == torch.uint8 and packed.mask_bytes.numel() == 2
    assert packed.tile_prefix.dtype == torch.int32 and packed.tile_prefix.tolist() == [0]
    assert packed.values.tolist() == [1., 2., 3., 4.]
    assert torch.equal(unpack_activation(packed), x)
    assert packed.storage_bytes == 2 + 4 + 4 * x.element_size()
    with pytest.raises(ValueError, match="inconsistent"):
        unpack_activation(replace(packed, tile_prefix=torch.ones_like(packed.tile_prefix)))


@pytest.mark.parametrize("power", [1, 2])
def test_bit_sparse_gradcheck_does_not_store_dense_input(power):
    torch.manual_seed(4)
    z = (torch.randn(3, 5, dtype=torch.float64) + .1).requires_grad_()
    w = torch.randn(2, 5, dtype=torch.float64, requires_grad=True)
    assert torch.autograd.gradcheck(lambda a, b: sparse_activation_linear(a, b, power=power, tile_size=4), (z, w))
    actual = sparse_activation_linear(z, w, power=power, tile_size=4)
    reference = z.relu().pow(power) @ w.t()
    torch.testing.assert_close(actual, reference)
    assert actual.grad_fn.saved_tensors[0].dtype == torch.uint8
    assert actual.grad_fn.saved_tensors[1].numel() == int((z > 0).sum())


@pytest.mark.parametrize("bad", [-1., float("nan"), -0.])
def test_bit_sparse_rejects_nonrelu_bit_patterns(bad):
    with pytest.raises(ValueError):
        pack_activation(torch.tensor([[bad]]), tile_size=4)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_bit_sparse_rejects_nonfinite_before_relu_could_erase_it(bad):
    with pytest.raises(ValueError, match="before sparsification"):
        sparse_activation_linear(torch.tensor([[bad, 1.]]), torch.ones(1, 2), tile_size=4)
    with pytest.raises(ValueError, match="before sparsification"):
        sparse_activation_linear(torch.ones(1, 2), torch.tensor([[bad, 1.]]), tile_size=4)


@pytest.mark.parametrize("dtype,amplitude", [(torch.float32, 1e20), (torch.float32, 1e-30),
                                           (torch.float64, 1e200), (torch.float64, 1e-200)])
def test_roleq_support_is_scale_invariant_for_finite_extreme_vectors(dtype, amplitude):
    vector = torch.full((2,), amplitude, dtype=dtype)
    codes, scale = exact_ternary_fit(vector)
    assert codes.tolist() == [1, 1]
    assert torch.isfinite(scale) and torch.equal(codes * scale, vector)


def test_package_merge_matches_exhaustive_length_limited_optimum():
    weights = [.03, .07, .2, .7]
    actual = _bounded_lengths(weights, 3)
    valid = [lengths for lengths in itertools.product(range(1, 4), repeat=4)
             if sum(2 ** -length for length in lengths) <= 1]
    optimum = min(sum(w * length for w, length in zip(weights, lengths, strict=True)) for lengths in valid)
    assert sum(w * length for w, length in zip(weights, actual, strict=True)) == pytest.approx(optimum)


@pytest.fixture(scope="module")
def codebook():
    return build_codebook(gaussian_exponent_model())


def test_lct_precomputed_codebook_is_bounded_and_has_escape(codebook):
    assert max(codebook.lengths) <= 8 and codebook.codes[256] >= 0
    assert codebook.expected_bits < 8
    assigned = [(code, length) for code, length in zip(codebook.codes, codebook.lengths, strict=True) if code >= 0]
    assert sum(2 ** -length for _, length in assigned) == pytest.approx(1)
    for i, (a, la) in enumerate(assigned):
        for j, (b, lb) in enumerate(assigned):
            if i != j and la <= lb:
                assert a != b >> (lb - la)


@pytest.mark.parametrize("center,budget", [(-128, 8), (0, 32), (127, 512)])
def test_lct_preserves_all_exponents_sign_fraction_and_overflow(codebook, center, budget):
    exponent = torch.arange(256, dtype=torch.int64)
    raw = ((exponent << 7) | (exponent % 128) | ((exponent % 2) << 15)).to(torch.int16)
    x = raw.view(torch.bfloat16).reshape(16, 16)
    packed = compress_bf16(x, codebook, streams=8, budget_bits=budget, center=center)
    assert torch.equal(decompress_bf16(packed).view(torch.int16), raw.reshape(16, 16))
    if budget <= 32:
        assert packed.overflow_exponents.numel() > 0
    assert packed.side_bytes.dtype == torch.uint8
    assert packed.prefix_bytes.numel() == 8 * budget // 8


def test_lct_noncontiguous_shape_and_bitwise_edge_patterns(codebook):
    raw = torch.tensor([0, -32768, 32640, -128, 32704, 1, -32767, 16256], dtype=torch.int16)
    x = raw.view(torch.bfloat16).reshape(2, 4).t()
    packed = compress_bf16(x, codebook, streams=3, budget_bits=16)
    assert torch.equal(decompress_bf16(packed).view(torch.int16), x.contiguous().view(torch.int16))


def test_lct_real_linear_backward_matches_dense(codebook):
    torch.manual_seed(5)
    x = torch.randn(4, 7).to(torch.bfloat16).requires_grad_()
    w = torch.randn(3, 7).to(torch.bfloat16).requires_grad_()
    a, b = x.detach().clone().requires_grad_(), w.detach().clone().requires_grad_()
    actual, expected = lct_linear(x, w, codebook), a @ b.t()
    assert torch.equal(actual, expected)
    first = torch.autograd.grad(actual.sum(), (x, w))
    second = torch.autograd.grad(expected.sum(), (a, b))
    assert all(torch.equal(l, r) for l, r in zip(first, second, strict=True))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_roleq_exact_solver_matches_ternary_exhaustion(seed):
    torch.manual_seed(seed)
    w = torch.randn(5, dtype=torch.float64)
    codes, scale = exact_ternary_fit(w)
    possibilities = torch.tensor(list(itertools.product((-1., 0., 1.), repeat=5)), dtype=w.dtype)
    scales = ((possibilities @ w) / possibilities.square().sum(-1).clamp_min(1)).clamp_min(0)
    oracle = (w - possibilities * scales[:, None]).square().sum(-1).min()
    actual = (w - codes * scale).square().sum()
    torch.testing.assert_close(actual, oracle, atol=1e-12, rtol=1e-12)


def test_roleq_all_zero_and_equal_magnitude_ties():
    zeros, scale = exact_ternary_fit(torch.zeros(3, 7))
    assert not zeros.any() and not scale.any()
    w = torch.tensor([-2., 2., 2., -2.])
    code, scale = exact_ternary_fit(w)
    assert torch.equal(code * scale, w)


def test_roleq_role_axis_and_actual_packed_bytes():
    torch.manual_seed(7)
    w = torch.randn(7, 11, dtype=torch.float64)
    reader, writer = quantize_by_role(w, "reader"), quantize_by_role(w, "writer")
    assert reader.scales.shape == (7,) and writer.scales.shape == (11,)
    torch.testing.assert_close(writer.reconstruct(), quantize_by_role(w.t(), "reader").reconstruct().t())
    reader_codes, reader_scales = exact_ternary_fit(w)
    assert torch.equal(reader.codes(), reader_codes)
    assert torch.equal(reader.reconstruct(), reader_codes * reader_scales[:, None])
    accounting = reader.bit_accounting()
    assert accounting["packed_code_bits"] == 16 * 8
    assert accounting["scale_bits"] == 7 * 64
    assert accounting["packing_padding_trits"] == 3
    assert accounting["payload_and_scale_bpw"] > accounting["information_lower_bound_bpw"]


def test_roleq_rejects_unknown_role_or_nonfinite_weights():
    with pytest.raises(ValueError):
        quantize_by_role(torch.ones(2, 3), "guessed")
    with pytest.raises(ValueError):
        exact_ternary_fit(torch.tensor([float("nan")]))
