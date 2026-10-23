"""Independent numeric references and negative controls, not LLM benchmarks."""
import math
import hashlib
import json
from pathlib import Path

import pytest
import torch

from auto_research.foundation_models.moezip import compress_cache, fisher_trace, select_cache
from auto_research.foundation_models.openattention import (
    attend, errorgate, fit_cache, query_geometry, qgs_scores,
    residual_proxy_attention, waterfill,
)


def dense(q, k, v):
    return (k @ q / math.sqrt(k.shape[1])).softmax(0) @ v


def expanded_proxy_reference(q, k, v, labels, exact):
    """Expand every proxy to N duplicate mean rows; no log-count implementation."""
    proxy_keys, proxy_values = k.clone(), v.clone()
    exact_set = set(exact.tolist())
    for label in labels.unique().tolist():
        rows = [i for i, group in enumerate(labels.tolist()) if group == label and i not in exact_set]
        if rows:
            proxy_keys[rows] = k[rows].mean(0)
            proxy_values[rows] = v[rows].mean(0)
    return dense(q, proxy_keys, proxy_values)


def test_fisher_against_explicit_matrices():
    gates = torch.tensor([[.2, .3, .5], [.9, .05, .05]], dtype=torch.float64)
    expected = torch.stack([torch.trace(torch.diag(p) - p[:, None] * p[None, :]) for p in gates])
    torch.testing.assert_close(fisher_trace(gates), expected)
    sigmoid = torch.tensor([[.2, .4, .7], [.1, .9, .8]], dtype=torch.float64)
    expected = torch.stack([torch.trace(torch.diag(p * (1 - p))) for p in sigmoid])
    torch.testing.assert_close(fisher_trace(sigmoid, "sigmoid"), expected)
    # On probabilities summing to one the two traces coincide algebraically;
    # the gate families differ when applied to the same underlying logits.
    torch.testing.assert_close(fisher_trace(gates), fisher_trace(gates, "sigmoid"))
    logits = torch.tensor([[0., 1., 2.]], dtype=torch.float64)
    assert not torch.allclose(fisher_trace(logits.softmax(-1)), fisher_trace(logits.sigmoid(), "sigmoid"))
    with pytest.raises(ValueError):
        fisher_trace(sigmoid)


def test_moezip_cross_head_max_anchors_and_no_duplicate_fill():
    gates = torch.tensor([[[.5, .5], [.99, .01]]], dtype=torch.float64)
    attention = torch.tensor([[[[.8, .0, .0, .0], [.0, .0, .9, .0]],
                               [[.0, .6, .0, .0], [.0, .0, .0, .8]]]], dtype=torch.float64)
    base = torch.tensor([[[0., 1., 4., 3.], [4., 3., 0., 1.]],
                         [[1., 4., 3., 0.], [0., 1., 3., 4.]]], dtype=torch.float64)
    result = select_cache(gates, attention, base, 2, min_anchors=1, max_anchors=1)
    reference = torch.zeros(4, dtype=torch.float64)
    for token in range(2):
        for position in range(4):
            reference[position] += max(float(attention[0, head, token, position]) for head in range(2)) * float(fisher_trace(gates)[0, token])
    torch.testing.assert_close(result.routing_scores, reference)
    assert result.anchors.tolist() == [0]
    for layer in range(2):
        for head in range(2):
            indices = result.indices[layer, head].tolist()
            assert 0 in indices and len(set(indices)) == 2
            assert indices == sorted(indices)
    assert not torch.allclose(reference, (attention.mean(1) * fisher_trace(gates)[..., None]).sum((0, 1)))
    k = torch.arange(2 * 2 * 4 * 3, dtype=torch.float64).reshape(2, 2, 4, 3)
    v = k[..., :2] + 10
    ck, cv = compress_cache(k, v, result)
    for layer in range(2):
        for head in range(2):
            torch.testing.assert_close(ck[layer, head], k[layer, head, result.indices[layer, head]])
            torch.testing.assert_close(cv[layer, head], v[layer, head, result.indices[layer, head]])


def test_moezip_adaptive_budget_and_tiny_bounds():
    uniform = torch.full((2, 3, 4), .25)
    peaked = torch.zeros_like(uniform)
    peaked[..., 0] = 1
    attention = torch.full((2, 2, 3, 512), 1 / 512)
    base = torch.arange(512.).expand(2, 2, -1)
    assert select_cache(uniform, attention, base, 256).anchor_count == 64
    assert select_cache(peaked, attention, base, 256).anchor_count == 32
    assert select_cache(uniform, attention, base, 3).indices.shape == (2, 2, 3)
    assert select_cache(uniform, attention, base, 0).indices.shape == (2, 2, 0)
    with pytest.raises(ValueError):
        select_cache(uniform, attention * 2, base, 4)
    with pytest.raises(ValueError):
        select_cache(uniform, attention, base, 513)


@pytest.mark.parametrize("budget", range(11))
def test_waterfill_capacity_and_exact_budget(budget):
    scores = torch.tensor([8., 2., 0.], dtype=torch.float64)
    capacities = torch.tensor([2, 3, 5])
    allocation = waterfill(scores, capacities, budget)
    assert int(allocation.sum()) == budget
    assert bool(((allocation >= 0) & (allocation <= capacities)).all())
    if budget == 4:
        assert allocation.tolist() == [2, 2, 0]
    zero_allocation = waterfill(torch.zeros_like(scores), capacities, budget)
    assert int(zero_allocation.sum()) == budget


@pytest.mark.parametrize("tiny", [1e-30, 1e-100, 1e-300])
def test_waterfill_active_set_preserves_ratios_across_extreme_dynamic_range(tiny):
    scores = torch.tensor([1., .5, tiny], dtype=torch.float64)
    # The active unconstrained level is 20/1.5, NOT the huge upper bound
    # 100/tiny. Flooring [13.333,6.666,~0] and rank-first remainder gives 14/6.
    assert waterfill(scores, torch.tensor([100, 100, 100]), 20).tolist() == [14, 6, 0]
    # Once the high-weight cluster fills, recompute ratios on the active set.
    assert waterfill(scores, torch.tensor([2, 100, 100]), 20).tolist() == [2, 18, 0]
    scaled = scores * 1e-8
    assert waterfill(scaled, torch.tensor([100, 100, 100]), 20).tolist() == [14, 6, 0]


def test_waterfill_zero_score_degeneracy_only_after_positive_capacity_fills():
    scores = torch.tensor([1., 0., 0.], dtype=torch.float64)
    assert waterfill(scores, torch.tensor([1, 100, 100]), 51).tolist() == [1, 25, 25]
    # Positive but tiny weights must retain their proportions after saturation.
    scores = torch.tensor([1., 2e-300, 1e-300], dtype=torch.float64)
    assert waterfill(scores, torch.tensor([1, 100, 100]), 31).tolist() == [1, 20, 10]


def test_errorgate_formula_and_signed_mean_negative_control():
    q = torch.tensor([2., 0.], dtype=torch.float64)
    means = torch.tensor([[1., 0.], [-1., 0.], [0., 0.]], dtype=torch.float64)
    variances = torch.tensor([[.3, 0.], [.3, 0.], [0., 0.]], dtype=torch.float64)
    counts = torch.tensor([3, 3, 2])
    raw = []
    for mean, variance, count in zip(means, variances, counts, strict=True):
        mu = float(q @ mean) / math.sqrt(2)
        sigma2 = float(q.square() @ variance) / 2
        raw.append(int(count) * math.exp(mu + sigma2 / 2) * math.erf(math.sqrt(sigma2 / 2)))
    expected = torch.tensor(raw, dtype=torch.float64)
    expected /= expected.max()
    torch.testing.assert_close(errorgate(q, means, variances, counts), expected)
    assert float(expected[0]) > float(expected[1])  # squared mean would erase the sign
    assert float(expected[2]) == 0


def test_residual_proxy_expansion_and_all_exact():
    generator = torch.Generator().manual_seed(11)
    k = torch.randn(9, 4, generator=generator, dtype=torch.float64)
    v = torch.randn(9, 3, generator=generator, dtype=torch.float64)
    q = torch.randn(4, generator=generator, dtype=torch.float64)
    labels = torch.tensor([0, 0, 0, 1, 1, 1, 2, 2, 2])
    for exact in (torch.tensor([], dtype=torch.long), torch.tensor([0, 3, 4]), torch.arange(9)):
        actual = residual_proxy_attention(q, k, v, labels, exact)
        torch.testing.assert_close(actual, expanded_proxy_reference(q, k, v, labels, exact))
    torch.testing.assert_close(residual_proxy_attention(q, k, v, labels, torch.arange(9)), dense(q, k, v))
    with pytest.raises(ValueError):
        residual_proxy_attention(q, k, v, labels, torch.tensor([0, 0]))


def test_count_correction_and_residual_recomputation_are_essential():
    q = torch.tensor([1.], dtype=torch.float64)
    k = torch.tensor([[0.], [0.], [0.], [2.]], dtype=torch.float64)
    v = torch.tensor([[1.], [1.], [1.], [4.]], dtype=torch.float64)
    labels = torch.tensor([0, 0, 0, 1])
    empty = torch.tensor([], dtype=torch.long)
    actual = residual_proxy_attention(q, k, v, labels, empty)
    torch.testing.assert_close(actual, dense(q, k, v))
    missing_count = dense(q, k[[0, 3]], v[[0, 3]])
    assert not torch.allclose(actual, missing_count)
    # Removing a high-scoring exact row changes the remaining cluster's mean.
    k = torch.tensor([[0.], [1.], [5.], [2.]], dtype=torch.float64)
    actual = residual_proxy_attention(q, k, v, labels, torch.tensor([2]))
    torch.testing.assert_close(actual, expanded_proxy_reference(q, k, v, labels, torch.tensor([2])))


def test_qgc_qgs_and_complete_operator():
    generator = torch.Generator().manual_seed(7)
    k = torch.randn(40, 6, generator=generator, dtype=torch.float64)
    v = torch.randn(40, 3, generator=generator, dtype=torch.float64)
    static = torch.randn(9, 6, generator=generator, dtype=torch.float64)
    conditioning = torch.randn(5, 6, generator=generator, dtype=torch.float64)
    q = torch.randn(6, generator=generator, dtype=torch.float64)
    eigenvalues, basis = query_geometry(static, conditioning)
    moment = .5 * (static.T @ static / 9 + conditioning.T @ conditioning / 5)
    torch.testing.assert_close(basis @ torch.diag(eigenvalues) @ basis.T, moment)
    index = fit_cache(k, v, static, conditioning, clusters=4, cluster_rank=3, selector_rank=4, generator=generator)
    assert index.key_codes.dtype == torch.int8
    recovered = index.key_codes.double() * index.key_scales
    assert bool(((recovered - k @ index.basis).abs() <= index.key_scales / 2 + 1e-12).all())
    torch.testing.assert_close(qgs_scores(index, q), recovered @ (q @ index.basis))
    for budget in (0, 1, 7, 40):
        result = attend(index, q, budget)
        assert len(result.exact_indices) == budget
        assert len(result.exact_indices.unique()) == budget
        assert result.charged_kv_rows == budget + 6
        torch.testing.assert_close(result.output, expanded_proxy_reference(q, k, v, index.labels, result.exact_indices))
    torch.testing.assert_close(attend(index, q, 40).output, dense(q, k, v))


def test_invalid_operator_inputs_fail_closed():
    with pytest.raises(ValueError):
        waterfill(torch.tensor([1.]), torch.tensor([1]), 2)
    with pytest.raises(ValueError):
        fit_cache(torch.ones(2, 2), torch.ones(2, 2), torch.ones(3, 2), torch.ones(3, 2), clusters=3)
    with pytest.raises(ValueError):
        query_geometry(torch.tensor([[float("nan")]]), torch.ones(1, 1))


@pytest.mark.parametrize("key,arxiv,published", [
    ("openattention", "2610.30951", "2026-10-22T09:03:08Z"),
    ("moezip", "2610.30206", "2026-10-21T13:06:30Z"),
])
def test_component_metadata_and_original_figure(key, arxiv, published):
    root = Path(__file__).resolve().parents[1]
    spec = json.loads((root / f"src/auto_research/paper_specs/catalog/foundation-models/{key}.json").read_text())
    assert spec["published_at"] == published
    assert spec["adapter"] is None and spec["implementation_status"] == "component_only"
    assert spec["diagnostic_only"] and not spec["promotion_eligible"] and not spec["evolve_integrated"]
    assert spec["requires_gpu_validation"]
    assert spec["gpu_validation_artifact"] == f"docs/gpu-validations/{key}-a100-20261023.json"
    assert spec["full_experiment_status"] == "not_reproduced_high_cost" and spec["review_done"]
    readme = root / "docs" / spec["detail_path"]
    text = readme.read_text()
    for field in ("论文信息", "论文链接", "公司 / 机构 / 学校", "首次公开日期", "原作者代码", "本地 adapter / 稳定键", "本地复现代码目录", "核心公式", "未报告生产线上 A/B", "成本过高，不复现（审查 DONE）"):
        assert field in text
    assert arxiv in text and f"{key}.py" in text
    provenance = json.loads((readme.parent / "assets/provenance.json").read_text())
    asset = readme.parent / "assets" / provenance["image"]
    assert provenance["visually_verified"]
    assert hashlib.sha256(asset.read_bytes()).hexdigest() == provenance["image_sha256"]


def test_packaged_diagnostic_entry_points():
    from auto_research.foundation_models.moezip import diagnostic as moe_diagnostic
    from auto_research.foundation_models.openattention import diagnostic as attention_diagnostic
    moe = moe_diagnostic(42, "cpu")
    attention = attention_diagnostic(42, "cpu")
    assert moe["metrics"]["all_anchors_present"] and all(moe["checks"].values())
    assert attention["metrics"]["full_read_max_abs_error"] == 0 and all(attention["checks"].values())
