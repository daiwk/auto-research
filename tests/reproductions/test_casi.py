from dataclasses import FrozenInstanceError
from pathlib import Path

import numpy as np
import pytest

from auto_research.reproductions.casi.algorithm import (
    Candidate, CachedCoalitionEvaluator, RetrievalSnapshot, bounded_zero_sum,
    credit_rules, permutation_credit, shape_advantages, token_advantages,
)
from auto_research.reproductions.casi.experiment import run


def test_exact_additive_credit_and_empty_set_never_scored():
    calls = []
    a = tuple(f"a{i}" for i in range(5))
    snapshot = RetrievalSnapshot.capture(a, lambda key: [Candidate(key, 1, 1)])
    evaluator = CachedCoalitionEvaluator(snapshot, lambda rows: calls.append(rows) or len(rows))
    rules = credit_rules(evaluator.exact_values())
    for rule in rules.values():
        np.testing.assert_allclose(rule, np.ones(5), atol=1e-14)
    assert len(calls) == 31 and evaluator.value(0) == 0 and all(calls)


def test_frozen_snapshot_copies_inputs_and_rejects_conflicting_candidates():
    source = [Candidate("x", 1, 2)]
    snapshot = RetrievalSnapshot.capture(("a", "b"), lambda _: source)
    digest = snapshot.sha256
    source.clear()
    assert len(snapshot.merge(3)) == 1 and snapshot.sha256 == digest
    with pytest.raises(FrozenInstanceError):
        snapshot.results[0][0].value = 8
    with pytest.raises(ValueError, match="changed"):
        RetrievalSnapshot(("a", "b"), ((Candidate("x", 1, 1),), (Candidate("x", 1, 2),)))


def test_intermediate_coalition_changes_credit_but_not_endpoints():
    first = np.array([mask.bit_count() for mask in range(16)], dtype=float)
    second = first.copy()
    second[3] += 8
    f, g = credit_rules(first), credit_rules(second)
    np.testing.assert_array_equal(f["singleton"], g["singleton"])
    np.testing.assert_array_equal(f["loo"], g["loo"])
    assert first[-1] == second[-1]
    assert not np.allclose(f["shapley"], g["shapley"])
    assert g["shapley"].sum() == pytest.approx(second[-1])


def test_negative_marginals_are_not_clamped_and_permutations_reuse_scores():
    values = np.array([0, 4, 2, 1], dtype=float)
    rules = credit_rules(values)
    assert rules["shapley"][1] < 0
    snapshot = RetrievalSnapshot(("a", "b"), ((Candidate("a", 1, 1),), (Candidate("b", 1, 1),)))
    def score(rows):
        return values[sum(1 if c.key == "a" else 2 for c in rows)]
    evaluator = CachedCoalitionEvaluator(snapshot, score)
    estimate = permutation_credit(evaluator, permutations=4096, seed=42)
    np.testing.assert_allclose(estimate, rules["shapley"], atol=.1)
    assert evaluator.calls == 3


def test_zero_sum_projection_is_not_independent_clipping_and_satisfies_kkt():
    u = np.array([9., -8., -1.])
    clipped = np.clip(u, -1, 1)
    assert clipped.sum() != 0
    z = bounded_zero_sum(u, kappa=1.)
    assert abs(z.sum()) < 1e-12 and np.max(abs(z)) <= 1
    np.testing.assert_allclose(z, [1, -1, 0], atol=1e-12)


def test_group_shared_std_and_action_token_mean_contract():
    c = np.array([[1., 2., 3.], [10., 20., 30.]])
    base = np.array([-.5, 2.])
    result = shape_advantages(c, base, beta=.5, kappa=10)
    centered = c - c.mean(axis=1, keepdims=True)
    assert result["group_std"] == pytest.approx(centered.std(ddof=0))
    assert np.linalg.norm(result["offsets"][1]) > 5 * np.linalg.norm(result["offsets"][0])
    np.testing.assert_allclose(result["advantages"].mean(1), base, atol=1e-12)
    spans = np.array([[-1, 0, 0, 1, 2, -1], [-1, 2, 1, 0, -1, -1]])
    mask = np.array([[1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 0, 0]])
    tokens = token_advantages(result["advantages"], base, spans, mask=mask)
    np.testing.assert_array_equal(tokens[:, 0], base)
    assert np.all(tokens[mask == 0] == 0)
    plain = shape_advantages(c, base, beta=0)["advantages"]
    np.testing.assert_allclose(plain, np.broadcast_to(base[:, None], c.shape))


@pytest.mark.parametrize("value", [np.nan, np.inf, -np.inf])
def test_nonfinite_inputs_rejected(value):
    with pytest.raises(ValueError):
        Candidate("x", value, 1)
    with pytest.raises(ValueError):
        bounded_zero_sum([0, value], kappa=1)
    with pytest.raises(ValueError):
        credit_rules([0, value])


def test_budgets_and_malformed_masks_fail_closed():
    snapshot = RetrievalSnapshot.capture(tuple(str(i) for i in range(9)), lambda k: [])
    evaluator = CachedCoalitionEvaluator(snapshot, lambda rows: 0)
    with pytest.raises(ValueError, match="cap"):
        evaluator.exact_values()
    with pytest.raises(ValueError):
        token_advantages([[1, 2]], [0], [[2]])
    with pytest.raises(ValueError):
        credit_rules([1., 2.])
    with pytest.raises(ValueError):
        permutation_credit(evaluator, permutations=100_000, seed=0)


def test_actual_mechanism_run_records_boundaries_and_exact_calls(tmp_path: Path):
    result = run(tmp_path, 42)
    assert result["diagnostic_only"] is True and result["promotion_eligible"] is False
    assert result["full_paper_reproduction"] is False
    assert result["metrics"]["retrieval_calls"] == 5
    assert result["metrics"]["exact_evaluator_calls"] == 31
    assert result["metrics"]["zero_sum_error"] < 1e-12
    assert result["metrics"]["action_mean_error"] < 1e-12
