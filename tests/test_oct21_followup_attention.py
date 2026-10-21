import math

import pytest
import torch

from auto_research.foundation_models.oct21_followup_attention import (
    apply_rope, calibrate_race, fold_race_weights, native_race_attention,
    race_pair_selection, stratified_sparse_attention,
)


def test_ssa_full_budget_is_dense_and_gradient_connected():
    torch.manual_seed(12)
    q = torch.randn(4, dtype=torch.double, requires_grad=True)
    k = torch.randn(7, 4, dtype=torch.double, requires_grad=True)
    v = torch.randn(7, 3, dtype=torch.double, requires_grad=True)
    result = stratified_sparse_attention(q, k, v, torch.zeros(7), 7)
    torch.testing.assert_close(result.output, (k @ q / 2).softmax(0) @ v)
    result.output.square().sum().backward()
    assert all(item.grad is not None and bool(torch.isfinite(item.grad).all()) for item in (q, k, v))


def test_ssa_duplicate_draws_use_inclusion_not_draw_probability(monkeypatch):
    # Force a duplicate to test the estimator independently of RNG implementations.
    def duplicate_draws(probabilities, number, *, replacement, generator):
        assert number == 3 and replacement is True
        return torch.tensor([0, 0, 1], device=probabilities.device)
    monkeypatch.setattr(torch, "multinomial", duplicate_draws)
    q = torch.tensor([0.0, 0.0], requires_grad=True)
    k = torch.ones(4, 2, requires_grad=True)
    v = torch.arange(8.0).reshape(4, 2).requires_grad_()
    proxy = torch.zeros(4, requires_grad=True)
    result = stratified_sparse_attention(q, k, v, proxy, 3, generator=torch.Generator().manual_seed(0))
    assert result.heavy_indices.numel() == 0
    assert result.residual_draws.numel() == 3
    assert result.selected_indices.numel() < 3
    torch.testing.assert_close(result.inclusion_probabilities, torch.full_like(result.inclusion_probabilities, 1 - 0.75**3))
    torch.testing.assert_close(result.output, v[result.selected_indices].mean(0))
    result.output.sum().backward()
    assert proxy.grad is None
    assert v.grad is not None and bool(torch.isfinite(v.grad).all())


def test_ssa_heavy_tokens_are_certain_and_score_correction_matches_formula():
    q = torch.tensor([1.0, -0.5])
    k = torch.arange(12.0).reshape(6, 2) / 10
    v = torch.arange(18.0).reshape(6, 3)
    result = stratified_sparse_attention(q, k, v, torch.tensor([8.0, 1, 0, -1, -2, -3]), 3,
                                         generator=torch.Generator().manual_seed(3))
    assert 0 in result.heavy_indices.tolist()
    assert result.selected_indices.numel() <= 3
    for index in result.heavy_indices:
        assert result.inclusion_probabilities[result.selected_indices == index] == 1
    logits = k[result.selected_indices] @ q / math.sqrt(2)
    expected = (logits.double() - result.inclusion_probabilities.log()).softmax(0).float() @ v[result.selected_indices]
    torch.testing.assert_close(result.output, expected)


@pytest.mark.parametrize("budget", [0, 8, True, 1.5])
def test_ssa_invalid_budget(budget):
    with pytest.raises(ValueError):
        stratified_sparse_attention(torch.zeros(2), torch.zeros(7, 2), torch.ones(7, 3), torch.zeros(7), budget)


def test_ssa_rejects_nonfinite_and_underflow_instead_of_hidden_clamp():
    with pytest.raises(ValueError):
        stratified_sparse_attention(torch.zeros(2), torch.zeros(3, 2), torch.ones(3, 3), torch.tensor([float("nan"), 0, 0]), 1)
    with pytest.raises(ValueError, match="underflow"):
        stratified_sparse_attention(torch.zeros(2), torch.zeros(3, 2), torch.ones(3, 3), torch.tensor([10000.0, 0, 0]), 1)


@pytest.mark.parametrize("layout", ["split_half", "interleaved"])
def test_race_retains_complete_pairs_and_original_frequencies(layout):
    torch.manual_seed(3)
    q, k = torch.randn(8, 8, dtype=torch.double), torch.randn(8, 8, dtype=torch.double)
    # Different energy scales guarantee noncontiguous surviving frequencies.
    ids = [0, 3] if layout == "split_half" else [0, 6]
    q[:, ids] *= 100
    pair_ids, coords, _ = race_pair_selection(q, k, 4, layout=layout)
    assert pair_ids.tolist() == [0, 3]
    positions = torch.arange(8, dtype=torch.double)
    frequencies = torch.tensor([1.0, 0.31, 0.07, 0.013], dtype=torch.double)
    before = apply_rope(q, positions, frequencies, layout=layout)[:, coords]
    after = apply_rope(q[:, coords], positions, frequencies[pair_ids], layout=layout)
    torch.testing.assert_close(before, after)
    # Regenerating/reindexing frequencies as if reduced width were a new model is wrong.
    wrong = apply_rope(q[:, coords], positions, frequencies[:2], layout=layout)
    assert float((before - wrong).norm()) > 1


@pytest.mark.parametrize("layout", ["split_half", "interleaved"])
def test_race_folded_forward_equals_explicit_projection_with_original_scale(layout):
    torch.manual_seed(42)
    x = torch.randn(12, 6, dtype=torch.double, requires_grad=True)
    weights = tuple(torch.randn(*shape, dtype=torch.double, requires_grad=True) / 3
                    for shape in [(6, 8), (6, 8), (6, 5), (5, 6)])
    q, k, v = x @ weights[0], x @ weights[1], x @ weights[2]
    projection = calibrate_race(q, k, v, 4, 3, layout=layout)
    assert not projection.value_basis.requires_grad
    positions = torch.arange(12, dtype=torch.double)
    frequencies = torch.tensor([1.0, 0.1, 0.01, 0.001], dtype=torch.double)
    folded = fold_race_weights(*weights, projection)
    actual = native_race_attention(x, positions, frequencies, folded, projection)
    rq = apply_rope(q, positions, frequencies, layout=layout)[:, projection.coordinate_ids]
    rk = apply_rope(k, positions, frequencies, layout=layout)[:, projection.coordinate_ids]
    scores = rq @ rk.T / math.sqrt(8)
    scores = scores.masked_fill(torch.ones_like(scores, dtype=torch.bool).triu(1), -torch.inf)
    expected = scores.softmax(-1) @ v @ projection.value_basis @ projection.value_basis.T @ weights[3]
    torch.testing.assert_close(actual, expected)
    actual.square().mean().backward()
    assert x.grad is not None and float(x.grad.norm()) > 0
    assert bool(torch.isfinite(x.grad).all())


def test_race_full_rank_fold_recovers_original_attention():
    torch.manual_seed(7)
    x = torch.randn(9, 4, dtype=torch.double)
    w = tuple(torch.randn(4, 4, dtype=torch.double) for _ in range(4))
    projection = calibrate_race(x @ w[0], x @ w[1], x @ w[2], 4, 4, layout="split_half")
    positions = torch.arange(9)
    frequencies = torch.tensor([1.0, 0.01])
    actual = native_race_attention(x, positions, frequencies, fold_race_weights(*w, projection), projection, causal=False)
    q = apply_rope(x @ w[0], positions, frequencies, layout="split_half")
    k = apply_rope(x @ w[1], positions, frequencies, layout="split_half")
    expected = (q @ k.T / 2).softmax(-1) @ (x @ w[2]) @ w[3]
    torch.testing.assert_close(actual, expected)


def test_race_bad_rank_and_nonfinite_are_rejected():
    with pytest.raises(ValueError):
        race_pair_selection(torch.zeros(3, 8), torch.zeros(3, 8), 3, layout="split_half")
    with pytest.raises(ValueError):
        calibrate_race(torch.zeros(3, 8), torch.zeros(3, 8), torch.zeros(3, 4), 4, 4, layout="split_half")
