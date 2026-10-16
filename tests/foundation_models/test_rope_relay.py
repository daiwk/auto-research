import pytest

torch = pytest.importorskip("torch")
from auto_research.foundation_models.rope_relay import (  # noqa: E402
    apply_rotary, relay_cache, relocate_keys, rotary_factors,
)


def factor_provider(position, amplitude=1.):
    return rotary_factors(position, torch.tensor([1., .01], dtype=torch.float64,
                                                device=position.device), amplitude)


@pytest.mark.parametrize("layout", ["split_half", "interleaved"])
@pytest.mark.parametrize("amplitude", [1., 1.7])
def test_scaled_inverse_and_relocation_equal_fresh_rotation(layout, amplitude):
    generator = torch.Generator().manual_seed(42)
    raw = torch.randn(2, 5, 7, generator=generator, dtype=torch.float64, requires_grad=True)
    old = torch.tensor([[1, 3, 7, 20, 99], [8, 19, 33, 51, 100]])
    new = torch.arange(5).expand(2, -1)
    source, target = factor_provider(old, amplitude), factor_provider(new, amplitude)
    cached = apply_rotary(raw, *source, layout=layout)
    torch.testing.assert_close(apply_rotary(cached, *source, inverse=True, layout=layout), raw)
    actual = relocate_keys(cached, source, target, layout=layout)
    torch.testing.assert_close(actual, apply_rotary(raw, *target, layout=layout), rtol=1e-12, atol=1e-12)
    torch.testing.assert_close(actual[..., 4:], raw[..., 4:], rtol=0, atol=0)
    assert torch.autograd.grad(actual.square().sum(), raw)[0].abs().sum() > 0
    assert torch.autograd.gradcheck(lambda x: relocate_keys(x, source, target, layout=layout), (raw,))


def test_stable_chronology_heterogeneous_endpoint_masks_values_and_continuation():
    source = torch.tensor([[20, -1, 3, 10], [8, 2, -1, -1], [-1, -1, -1, -1]])
    valid = source.ge(0)
    raw = torch.randn(3, 4, 6, dtype=torch.float64, requires_grad=True)
    values = torch.randn(3, 4, 3, dtype=torch.float64, requires_grad=True)
    cached = apply_rotary(raw, *factor_provider(source.clamp_min(0), 1.4))
    result = relay_cache(cached, values, source, lambda p: factor_provider(p, 1.4), valid)
    assert result.anchor == 3
    assert result.compact_positions.tolist() == [[0, 1, 2, -1], [1, 2, -1, -1], [-1]*4]
    assert result.source_positions.tolist() == [[3, 10, 20, -1], [2, 8, -1, -1], [-1]*4]
    expected_values = values.gather(-2, result.permutation[..., None].expand(3, 4, 3))
    torch.testing.assert_close(result.values, expected_values, rtol=0, atol=0)
    ordered_raw = raw.gather(-2, result.permutation[..., None].expand(3, 4, 6))
    expected_keys = apply_rotary(ordered_raw, *factor_provider(result.compact_positions.clamp_min(0), 1.4))
    torch.testing.assert_close(result.keys[result.valid_mask], expected_keys[result.valid_mask])
    assert result.question_positions(3).tolist() == [3, 4, 5]
    assert result.answer_input_positions(3, 2).tolist() == [6, 7]
    mask = result.causal_mask(2)
    assert mask.shape == (3, 2, 6)
    assert mask[1].tolist() == [[True, True, False, False, True, False],
                              [True, True, False, False, True, True]]
    assert not mask[2, :, :4].any()


def test_attention_uses_synchronized_query_phase_and_preserves_all_gradients():
    source = torch.tensor([[1, 100, 1000]])
    raw = torch.randn(1, 3, 4, dtype=torch.float64, requires_grad=True)
    values = torch.randn(1, 3, 5, dtype=torch.float64, requires_grad=True)
    query = torch.randn(1, 2, 4, dtype=torch.float64, requires_grad=True)
    cache = relay_cache(apply_rotary(raw, *factor_provider(source)), values, source, factor_provider)
    positions = cache.question_positions(2)
    rotated_query = apply_rotary(query, *factor_provider(positions))
    logits = rotated_query @ cache.keys.transpose(-1, -2)
    reference_keys = apply_rotary(raw, *factor_provider(torch.arange(3)))
    reference = rotated_query @ reference_keys.transpose(-1, -2)
    torch.testing.assert_close(logits, reference)
    unsynchronized = apply_rotary(query, *factor_provider(torch.tensor([1001, 1002]))) @ cache.keys.transpose(-1, -2)
    assert not torch.allclose(logits, unsynchronized)
    loss = (logits.softmax(-1) @ cache.values).square().sum()
    gradients = torch.autograd.grad(loss, (raw, values, query))
    assert all(torch.isfinite(g).all() and g.abs().sum() > 0 for g in gradients)


@pytest.mark.parametrize("dtype", [torch.float32, torch.float16, torch.bfloat16])
def test_low_precision_returns_storage_dtype_and_identity_with_nonrotary_tail(dtype):
    key = torch.randn(2, 4, 6).to(dtype)
    position = torch.arange(4).expand(2, -1)
    factors = factor_provider(position, 1.7)
    relocated = relocate_keys(key, factors, factors)
    assert relocated.dtype == dtype
    torch.testing.assert_close(relocated.float(), key.float(), rtol=1e-3, atol=1e-3)
    torch.testing.assert_close(relocated[..., 4:], key[..., 4:], rtol=0, atol=0)


def test_invalid_duplicate_source_and_noninvertible_factors_rejected():
    key = torch.randn(1, 2, 4)
    with pytest.raises(ValueError, match="duplicate"):
        relay_cache(key, key, torch.tensor([[2, 2]]), factor_provider)
    with pytest.raises(ValueError, match="invertible"):
        apply_rotary(key, torch.zeros(1, 2, 2), torch.zeros(1, 2, 2), inverse=True)
    with pytest.raises(ValueError):
        relay_cache(key, key, torch.tensor([[-1, 2]]), factor_provider)
