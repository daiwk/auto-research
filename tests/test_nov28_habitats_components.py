"""Independent checks of Habitats v1 equations, not an agent benchmark.

Primary contract: arXiv:2611.31160v1, Section 3 and Appendix C. In
particular, the paper normalizes only policy rows and maps constant columns
to zero; the pinned author's repository uses a different convention.
"""

import itertools
import math

import numpy as np
import pytest

from auto_research.agent_research import habitats as h


EPS = 1e-8


def reference_summary(fitness, random_mean, random_std, reward_valid):
    """Explicit scalar reference, independent of implementation helpers."""
    n = len(fitness)
    normalized = []
    for row in fitness:
        normalized.append([
            (row[j] - min(fitness[k][j] for k in range(n)))
            / (max(fitness[k][j] for k in range(n))
               - min(fitness[k][j] for k in range(n)) + EPS)
            for j in range(n)
        ])
    survivors = tuple(
        fitness[i][i] == max(fitness[k][i] for k in range(n))
        and fitness[i][i] > random_mean[i]
        for i in range(n)
    )
    nonzero = [row for row in normalized if any(value != 0 for value in row)]
    distances = []
    for left, right in itertools.combinations(nonzero, 2):
        dot = math.fsum(a * b for a, b in zip(left, right))
        norms = math.sqrt(math.fsum(x * x for x in left)) * math.sqrt(
            math.fsum(x * x for x in right)
        )
        distances.append(1 - dot / (norms + EPS))
    grounded = tuple(
        bool(reward_valid[i]
             and (fitness[i][i] - random_mean[i]) / (random_std[i] + EPS) > .5)
        for i in range(n)
    )
    coverage = len({
        tuple(round(x, 1) for x in normalized[i])
        for i in range(n) if grounded[i]
    })
    return {
        "normalized": normalized,
        "survivors": survivors,
        "specialist_quality": math.fsum(normalized[i][i] for i in range(n)) / n,
        "behavioral_diversity": math.fsum(distances) / len(distances) if distances else 0.,
        "grounded": grounded,
        "grounded_coverage": coverage,
    }


def test_habitats_episode_return_means_preserve_policy_reward_axes():
    # Each scalar is already a complete undiscounted episode return.
    returns = np.array([[[1., 3., 5.], [-4., 2., 8.]],
                        [[10., 20., 30.], [9., 0., -9.]]])
    original = returns.copy()
    actual = h.mean_cross_fitness(returns)
    np.testing.assert_allclose(actual, [[3., 2.], [20., 0.]], rtol=0, atol=0)
    np.testing.assert_array_equal(returns, original)
    assert isinstance(actual, np.ndarray)
    np.testing.assert_array_equal(h.mean_cross_fitness([[[7.]]]), [[7.]])


def test_habitats_normalization_columnwise_with_epsilon_not_rowwise():
    f = [[10., 100.], [20., 200.]]
    expected = [[0., 0.], [10. / (10. + EPS), 100. / (100. + EPS)]]
    np.testing.assert_allclose(h.normalize_cross_fitness(f), expected, rtol=0, atol=1e-15)
    assert not np.allclose(h.normalize_cross_fitness(f), [[0., 1.], [0., 1.]])
    # The epsilon is in the formula, not merely a branch for constant columns.
    tiny = h.normalize_cross_fitness([[0., 0.], [EPS, EPS]])
    np.testing.assert_array_equal(tiny, [[0., 0.], [.5, .5]])


def test_habitats_normalization_does_not_include_random_baseline_or_round4():
    f = [[0., 0.], [1., 3.]]
    low = h.summarize(f, [-100., -100.], [1., 1.], [True, True])
    high = h.summarize(f, [100., 100.], [1., 1.], [True, True])
    np.testing.assert_array_equal(low.normalized, high.normalized)
    assert low.normalized[1, 0] == 1 / (1 + EPS)
    assert low.normalized[1, 0] != 1.0


def test_habitats_survivors_use_raw_column_niches_ties_and_strict_random_margin():
    f = [[2., 5., 1.], [2., 4., 3.], [1., 2., 3.]]
    assert h.survivor_mask(f, [0., 0., 0.]) == (True, False, True)
    assert h.survivor_mask(f, [2., 0., 3.]) == (False, False, False)
    assert h.survivor_mask(f, [math.nextafter(2., -math.inf), 0., 0.]) == (
        True, False, True
    )
    # A row-wise winner is not necessarily the best policy on its own column.
    assert h.survivor_mask([[5., 100.], [6., 99.]], [0., 0.]) == (False, False)


def test_habitats_constant_columns_zero_diversity_but_coverage_can_be_one():
    result = h.summarize([[2., 2.], [2., 2.]], [0., 0.], [1., 1.], [True, True])
    np.testing.assert_array_equal(result.normalized, np.zeros((2, 2)))
    assert result.specialist_quality == result.behavioral_diversity == 0.
    assert result.survivors == result.grounded == (True, True)
    # Zero profiles are excluded from BD only, not from grounded coverage.
    assert result.grounded_coverage == 1


def test_habitats_behavioral_diversity_excludes_zero_norm_not_maximally_different():
    assert h.behavioral_diversity([[0., 0.], [1., 0.], [0., 1.]]) == 1.
    assert h.behavioral_diversity([[0., 0.], [1., 0.]]) == 0.
    assert h.behavioral_diversity([[0., 0.], [0., 0.]]) == 0.
    assert h.behavioral_diversity([[.2, .7]]) == 0.
    # With the literal paper epsilon, identical nonzero profiles have a tiny
    # positive distance; the repository's unit-normalize-then-dot is different.
    actual = h.behavioral_diversity([[1., 0.], [1., 0.]])
    assert actual == pytest.approx(1 - 1 / (1 + EPS), abs=1e-15)
    assert actual > 0.


def test_habitats_nonzero_tiny_profiles_are_not_misclassified_as_zero_norm():
    # Squaring 1e-200 underflows in naive Euclidean norms, but the row is not
    # zero. The paper's explicit epsilon makes orthogonal distances exactly 1.
    assert h.behavioral_diversity([[1e-200, 0.], [0., 1e-200]]) == 1.


def test_habitats_grounding_is_strict_half_std_and_requires_successful_reward():
    at_threshold = EPS * .5
    assert h.summarize([[at_threshold]], [0.], [0.], [True]).grounded == (False,)
    above = math.nextafter(at_threshold, math.inf)
    assert h.summarize([[above]], [0.], [0.], [True]).grounded == (True,)
    assert h.summarize([[2.]], [0.], [1.], [False]).grounded == (False,)
    assert h.summarize([[2.]], [2.], [0.], [True]).grounded == (False,)


def test_habitats_grounded_coverage_deduplicates_quantized_profiles_per_generation():
    f = [[1., 0., 0.], [.98, 0., 0.], [0., 1., 1.]]
    result = h.summarize(f, [-1., -1., -1.], [1., 1., 1.], [True] * 3)
    assert result.grounded == (True, True, True)
    assert result.grounded_coverage == 2
    assert h.summarize(f, [-1.] * 3, [1.] * 3, [True, True, False]).grounded_coverage == 1
    # Coordinate systems can change by generation: AUC adds counts, it does
    # not deduplicate identities/profiles across generations.
    assert h.coverage_auc([2, 2, 1]) == 5
    assert h.coverage_auc(iter([0, 3, 0])) == 3
    assert h.coverage_auc([]) == 0


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_habitats_summary_matches_independent_reference(seed):
    rng = np.random.default_rng(seed)
    f = rng.normal(size=(6, 6)).tolist()
    mu = rng.normal(size=6).tolist()
    std = rng.uniform(0, 3, size=6).tolist()
    valid = [True, False, True, True, True, False]
    expected = reference_summary(f, mu, std, valid)
    actual = h.summarize(f, mu, std, valid)
    np.testing.assert_allclose(actual.normalized, expected["normalized"], rtol=0, atol=1e-14)
    assert actual.survivors == expected["survivors"]
    assert actual.grounded == expected["grounded"]
    assert actual.grounded_coverage == expected["grounded_coverage"]
    assert actual.specialist_quality == pytest.approx(expected["specialist_quality"], abs=1e-14)
    assert actual.behavioral_diversity == pytest.approx(expected["behavioral_diversity"], abs=1e-14)


def test_habitats_summary_exposes_readonly_independent_matrix():
    f = np.array([[1., 2.], [0., 3.]])
    original = f.copy()
    result = h.summarize(f, [0., 0.], [1., 1.], [True, True])
    np.testing.assert_array_equal(f, original)
    assert not np.shares_memory(result.normalized, f)
    assert not result.normalized.flags.writeable
    with pytest.raises(ValueError):
        result.normalized[0, 0] = -1
    with pytest.raises((AttributeError, TypeError)):
        result.grounded_coverage = 0


@pytest.mark.parametrize("bad", [
    [], [1., 2.], [[1., 2.]], [[1.], [2.]], [[1., 2.], [3.]],
    [[True]], [[True, 2.], [3., 4.]], [[1 + 0j]], [["1"]],
    [[float("nan")]], [[float("inf")]],
    np.array([[1.]], dtype=object),
])
def test_habitats_fitness_matrix_rejects_invalid_domains(bad):
    with pytest.raises(ValueError):
        h.normalize_cross_fitness(bad)
    with pytest.raises(ValueError):
        h.survivor_mask(bad, [0.])
    with pytest.raises(ValueError):
        h.summarize(bad, [0.], [1.], [True])


@pytest.mark.parametrize("bad", [
    [], [[1.]], [[[1.], [2.]]], [[[1.], [2.]], [[3.]]],
    [[[True]]], [[[True, 2.]]], [[[1 + 0j]]], [[["1"]]], [[[float("nan")]]],
    [[[float("inf")]]], [[[]]], np.ones((1, 1, 1), dtype=object),
])
def test_habitats_return_cube_requires_finite_square_population_and_rollouts(bad):
    with pytest.raises(ValueError):
        h.mean_cross_fitness(bad)


@pytest.mark.parametrize("mu,std,valid", [
    ([], [1., 1.], [True, True]),
    ([0., 0.], [1.], [True, True]),
    ([0., 0.], [1., 1.], [True]),
    ([True, 0.], [1., 1.], [True, True]),
    ([0., 0.], [True, 1.], [True, True]),
    ([0., 0.], [-1., 1.], [True, True]),
    ([0., float("inf")], [1., 1.], [True, True]),
    ([0., 0.], [1., float("nan")], [True, True]),
    ([0., 0.], [1., 1.], [1, 1]),
    ([0., 0.], [1., 1.], [True, "False"]),
])
def test_habitats_summary_aligned_vector_and_boolean_boundaries(mu, std, valid):
    with pytest.raises(ValueError):
        h.summarize([[1., 0.], [0., 1.]], mu, std, valid)


@pytest.mark.parametrize("bad", [[], [1.], [[-1., 0.]], [[1.01, 0.]],
                                 [[float("nan")]], [[True]], [[True, 0.]], [[1 + 0j]]])
def test_habitats_behavioral_profile_domain(bad):
    with pytest.raises(ValueError):
        h.behavioral_diversity(bad)


@pytest.mark.parametrize("bad", [[-1], [True], [1.5], [float("inf")], ["1"]])
def test_habitats_coverage_auc_requires_nonnegative_integer_counts(bad):
    with pytest.raises(ValueError):
        h.coverage_auc(bad)


def test_habitats_overflow_does_not_emit_nonfinite_or_mutate_inputs():
    f = np.array([[-1e308, 0.], [1e308, 1.]])
    original = f.copy()
    with pytest.raises(ValueError):
        h.normalize_cross_fitness(f)
    np.testing.assert_array_equal(f, original)
    with pytest.raises(ValueError):
        h.summarize([[1e308]], [-1e308], [0.], [True])


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_habitats_diagnostic_cpu_contract_is_not_capability_evidence(seed):
    result = h.diagnostic(seed, "cpu")
    assert h.REQUIRES_GPU_VALIDATION is False
    assert result["seed"] == seed and result["device"] == "cpu"
    assert result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(type(v) is bool and v for v in result["checks"].values())
    assert result["metrics"] and all(
        type(v) in (int, float) and math.isfinite(v) for v in result["metrics"].values()
    )
    assert result == h.diagnostic(seed, "cpu")


@pytest.mark.parametrize("seed,device", [(-1, "cpu"), (2**32, "cpu"),
                                         (True, "cpu"), (1.5, "cpu"),
                                         (42, "cuda"), (42, "mps"), (42, None)])
def test_habitats_diagnostic_rejects_invalid_seed_and_accelerator(seed, device):
    with pytest.raises(ValueError):
        h.diagnostic(seed, device)
