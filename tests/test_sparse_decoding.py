import pytest

torch = pytest.importorskip("torch")

from auto_research.foundation.sparse_decoding import DecodeCalibration, pack_bitmask, unpack_bitmask, wanda_nm


@pytest.mark.parametrize("n,m", [(2, 4), (4, 8), (8, 16), (16, 32)])
def test_word_has_exact_16_bits_and_values_follow_increasing_columns(n, m):
    torch.manual_seed(2)
    weight = torch.randn(5, 64)
    sparse, keep = wanda_nm(weight, torch.arange(64).float(), n=n, m=m)
    assert (keep.reshape(5, -1, m).sum(-1) == n).all()
    values, words = pack_bitmask(sparse, keep)
    assert words.numel() * 4 * 8 / values.numel() == 2  # exactly 2 metadata bits/nonzero
    torch.testing.assert_close(unpack_bitmask(values, words), sparse)
    x = torch.randn(64)
    torch.testing.assert_close(unpack_bitmask(values, words) @ x, sparse @ x)


def test_phase_excludes_prefill_even_for_single_token_and_hooks_are_removed():
    layer = torch.nn.Linear(32, 4)
    collector = DecodeCalibration({"layer": layer})
    layer(torch.ones(1, 1, 32) * 9)  # one-token prefill must not be retained
    assert collector.counts["layer"] == 0
    with collector.decoding():
        layer(torch.ones(1, 1, 32) * 2)
    assert collector.counts["layer"] == 1
    torch.testing.assert_close(collector.energy["layer"], torch.full((32,), 4.))
    collector.close()
    assert not layer._forward_pre_hooks


def test_rejects_unaligned_pattern_and_invalid_activation_energy():
    with pytest.raises(ValueError):
        wanda_nm(torch.ones(3, 31), torch.ones(31))
    with pytest.raises(ValueError):
        wanda_nm(torch.ones(3, 32), -torch.ones(32))
    with pytest.raises(ValueError, match="sixteen"):
        pack_bitmask(torch.ones(3, 32), torch.ones(3, 32, dtype=torch.bool))
