from dataclasses import replace
from fractions import Fraction

import pytest

from auto_research.agent_research.verified_quantum_wiki import (
    ExternalComparatorResult, Solution, STANDARD_AXIOMS, admit, diagnostic,
)


@pytest.fixture
def rows():
    old = Solution("a" * 64, "b" * 64, "Q*T-v1", 100, 100)
    new = replace(old, artifact_sha256="c" * 64, cost=95)
    result = ExternalComparatorResult(
        new.specification_sha256, new.artifact_sha256, new.cost_metric,
        new.cost, "fixture-only", True, True, True, True, True, True,
        STANDARD_AXIOMS,
    )
    return old, new, result


@pytest.mark.parametrize("cost,size,expected", [
    (95, 200, True), (Fraction(95001, 1000), 100, False),
    (99, 80, True), (99, 81, False), (100, 1, False), (101, 1, False),
    (0, 200, True), (Fraction(99999, 1000), 80, True),
])
def test_exact_boundaries(rows, cost, size, expected):
    old, new, result = rows
    assert admit(old, replace(new, cost=cost, code_size=size),
                 replace(result, proved_cost=cost)).accepted is expected


@pytest.mark.parametrize("flag", [
    "clean_sandbox_replay", "target_theorems_match", "transitive_definitions_match",
    "proof_terms_checked", "no_sorry", "resource_theorem_reduces",
])
def test_each_external_verifier_failure_blocks_even_large_gain(rows, flag):
    old, new, result = rows
    new, result = replace(new, cost=1), replace(result, proved_cost=1)
    assert not admit(old, new, replace(result, **{flag: False})).accepted
    with pytest.raises(ValueError):
        replace(result, **{flag: "true"})


@pytest.mark.parametrize("changes", [
    {"artifact_sha256": "d" * 64}, {"specification_sha256": "d" * 64},
    {"proved_cost": 94}, {"cost_metric": "T-only"},
    {"axioms": STANDARD_AXIOMS | {"sorryAx"}},
    {"axioms": STANDARD_AXIOMS | {"custom"}},
])
def test_stale_unproved_or_custom_axiom_receipt_rejected(rows, changes):
    old, new, result = rows
    assert not admit(old, new, replace(result, **changes)).accepted


def test_specification_and_metric_cannot_change_between_records(rows):
    old, new, result = rows
    for field, value in (("specification_sha256", "d" * 64), ("cost_metric", "T")):
        assert not admit(old, replace(new, **{field: value}),
                         replace(result, **{field: value})).accepted
    assert not admit(old, new, None).accepted
    assert not admit(old, new, {"passed": True}).accepted
    # A theorem may use a strict subset of the allowed standard axioms.
    assert admit(old, new, replace(result, axioms=frozenset())).accepted


@pytest.mark.parametrize("cost", [-1, float("nan"), float("inf"), 95.0, True])
def test_non_exact_or_invalid_costs_rejected(rows, cost):
    old, _, result = rows
    with pytest.raises(ValueError):
        replace(old, cost=cost)
    with pytest.raises(ValueError):
        replace(result, proved_cost=cost)


def test_missing_provenance_invalid_dimensions_and_zero_baseline(rows):
    old, new, result = rows
    with pytest.raises(ValueError):
        replace(result, evidence_ref=" ")
    for size in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            replace(new, code_size=size)
    with pytest.raises(ValueError):
        replace(new, artifact_sha256="unbound")
    with pytest.raises(ValueError):
        admit(replace(old, cost=0), new, result)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_explicitly_synthetic_cpu(seed):
    row = diagnostic(seed)
    assert row == diagnostic(seed, "cpu")
    assert row["seed"] == seed and all(row["checks"].values())
    assert row["metrics"]["passed_cases"] == 9
    assert row["metrics"]["real_proofs_checked"] == 0
    assert row["diagnostic_only"] and not row["promotion_eligible"]
    with pytest.raises(ValueError):
        diagnostic(seed, "cuda")
