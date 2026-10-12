"""Formula/causality/cache tests, not GPU/public-data evidence."""
import inspect
import math

import pytest
torch = pytest.importorskip("torch")
from torch import nn
from torch.nn import functional as F

from auto_research.foundation_models.oct12_mechanisms import (
    DepthRead, DualQuantLinear, MSARLM, OrthrosLM, SourceExpansion,
    TinyTransformerLM, int4_grid, project_inverse_scale, sliding_window_attention,
    solve_dual_scale,
)


def test_msar_full_channel_multiscale_causal_expansion():
    torch.manual_seed(11)
    bank = SourceExpansion(8, (2, 4))
    for convolution in bank.convs:
        nn.init.uniform_(convolution.weight, -.3, .3)
    x = torch.randn(2, 9, 8)
    altered = x.clone()
    altered[:, 5:] += 20
    original, changed = bank(x), bank(altered)
    assert original.shape == (2, 9, 3, 8)  # NO channel slicing
    torch.testing.assert_close(original[:, :5], changed[:, :5])
    torch.testing.assert_close(original[:, :, 0], x)
    assert not torch.allclose(original[:, :, 1], original[:, :, 2])


def test_msar_depth_softmax_and_sigmoid_mixer_formula():
    source = [torch.randn(2, 5, 4), torch.randn(2, 5, 4)]
    banks = [SourceExpansion(4, (2,)) for _ in source]
    read = DepthRead(4, 2)
    result, weights, mixing = read(source, banks, return_weights=True)
    torch.testing.assert_close(weights.sum(2), torch.ones_like(weights.sum(2)))
    torch.testing.assert_close(mixing, torch.full_like(mixing, .5))
    torch.testing.assert_close(result, (source[0] + source[1]) / 2)
    result.square().mean().backward()
    assert read.query.grad is not None
    assert banks[0].convs[0].weight.grad.abs().sum() > 0
    assert read.mixer.weight.grad.abs().sum() > 0


def test_msar_block_summaries_train_real_lm_and_are_causal():
    torch.manual_seed(17)
    model = MSARLM(width=16, layers=2, heads=2, block_size=2, kernels=(2, 4))
    ids = torch.randint(256, (2, 9))
    change = ids.clone()
    change[:, 5:] = (change[:, 5:] + 51) % 256
    torch.testing.assert_close(model(ids)[:, :5], model(change)[:, :5], atol=1e-5, rtol=1e-5)
    assert model.last_persistent_sources == 3  # embedding + TWO blocks, not six streams
    loss = F.cross_entropy(model(ids[:, :-1]).flatten(0, 1), ids[:, 1:].flatten())
    loss.backward()
    assert model.reads[0].query.grad is not None
    assert model.blocks[0].attention.q.weight.grad.abs().sum() > 0


def test_fixed_window_prefill_matches_dense_swa_equation():
    torch.manual_seed(19)
    q, k, v = [torch.randn(2, 3, 9, 4) for _ in range(3)]
    scores = q @ k.transpose(-1, -2) / 2
    positions = torch.arange(9)
    allowed = (positions[:, None] >= positions[None]) & (positions[:, None] - positions[None] < 3)
    expected = scores.masked_fill(~allowed, -torch.inf).softmax(-1) @ v
    torch.testing.assert_close(sliding_window_attention(q, k, v, 3), expected)


def test_orthros_true_prefill_decode_cache_equals_batch_training_path():
    torch.manual_seed(23)
    model = OrthrosLM(width=16, layers=3, heads=2, window=3).eval()
    for block in model.blocks:
        nn.init.uniform_(block.attention.output_alpha, .6, 1.4)
        nn.init.normal_(block.attention.base_beta, std=.2)
    ids = torch.randint(256, (2, 12))
    expected = model(ids, output_start=4)
    first, states = model.prefill(ids[:, :5])
    incremental = [first]
    for pos in range(5, 12):
        output, states = model.decode(ids[:, pos:pos + 1], states)
        incremental.append(output)
    torch.testing.assert_close(torch.cat(incremental, 1), expected, atol=1e-5, rtol=1e-5)
    assert all(state.key.shape[-2] == 12 for state in states)
    # Base SWA is bounded, but GLOBAL cache remains complete for output retrieval.
    assert all(state.key.shape == (2, 2, 12, 8) for state in states)


def test_orthros_conversion_has_exact_standard_limit_and_training_gradient():
    torch.manual_seed(29)
    vanilla = TinyTransformerLM(width=16, layers=2, heads=2)
    converted = OrthrosLM.from_transformer(vanilla, window=32)
    ids = torch.randint(256, (2, 10))
    torch.testing.assert_close(converted(ids), vanilla(ids), atol=1e-5, rtol=1e-5)
    converted.blocks[0].attention.window = 2
    loss = F.cross_entropy(converted(ids[:, :-1]).flatten(0, 1), ids[:, 1:].flatten())
    loss.backward()
    assert converted.blocks[0].attention.output_alpha.grad.abs().sum() > 0
    assert converted.blocks[0].attention.k.weight.grad.abs().sum() > 0


def test_dualquant_black_box_variable_splitting_closed_form():
    weight = torch.tensor([[1.3, -2.2, .17], [3.1, .41, -1.6]])
    calls = []
    def quantizer(x):
        calls.append(x.clone())
        return int4_grid(x)
    actual = solve_dual_scale(weight, iterations=1, quantizer=quantizer)
    ri = project_inverse_scale(weight.abs().amax(1) / 7, "bf16")
    q = int4_grid(weight / ri[:, None])
    ri = project_inverse_scale((weight * q).sum(1) / q.square().sum(1), "bf16")
    q = int4_grid(weight / ri[:, None])
    s = q * ri[:, None]
    ci = project_inverse_scale((weight * s).sum(0) / s.square().sum(0), "bf16")
    q = int4_grid(weight / ri[:, None] / ci[None])
    assert len(calls) == 3
    torch.testing.assert_close(actual.row_inverse, ri)
    torch.testing.assert_close(actual.column_inverse, ci)
    torch.testing.assert_close(actual.codes, q)
    assert "activation" not in inspect.signature(solve_dual_scale).parameters


@pytest.mark.parametrize("format", ["bf16", "e8m0"])
def test_dualquant_zero_rows_and_admissible_scales(format):
    weight = torch.tensor([[0., 0., 0.], [.01, 4.1, -8.5], [1., 7.2, .02]])
    tile = solve_dual_scale(weight, iterations=5, scale_format=format)
    assert torch.isfinite(tile.reconstruct()).all()
    assert all(math.isfinite(x) for x in tile.mse_history)
    assert tile.codes.min() >= -8 and tile.codes.max() <= 7
    if format == "e8m0":
        torch.testing.assert_close(tile.row_inverse.log2(), tile.row_inverse.log2().round())
        torch.testing.assert_close(tile.column_inverse.log2(), tile.column_inverse.log2().round())
    torch.testing.assert_close(tile.reconstruct()[0], torch.zeros(3))


def test_dualquant_real_activation_factorization_not_weight_only_forward():
    torch.manual_seed(31)
    original = nn.Linear(8, 7)
    method = DualQuantLinear(original, group_size=4, tile_rows=3, iterations=5)
    x = torch.randn(2, 3, 8)
    out = method(x)
    assert out.shape == (2, 3, 7)
    assert torch.isfinite(out).all() and math.isfinite(method.weight_mse())
    # A linear FP reconstructed-weight-only forward would obey scaling exactly;
    # dynamic INT4 activation rounding generally does not obey additivity.
    y = torch.randn_like(x)
    assert not torch.allclose(method(x + y) - original.bias,
                             method(x) + method(y) - 2 * original.bias, atol=1e-5)
    with pytest.raises(ValueError, match="only bf16"):
        solve_dual_scale(original.weight, scale_format="nvfp4")
