"""Validation-only selection and paired test reporting for public-task runs.

This is an evaluation contract, not a substitute for running the underlying
OPSD or MaD-RL model. In particular, the test score is read only *after* a
winner is fixed by validation data, and unequal budgets are rejected.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from statistics import mean


@dataclass(frozen=True)
class PublicRun:
    method: str
    seed: int
    validation_score: float
    test_score: float
    update_steps: int
    generated_tokens: int
    dataset_revision: str
    checkpoint_revision: str


def compare_runs(
    runs: tuple[PublicRun, ...], *, baseline: str, maximize: bool = True,
) -> dict:
    """Choose by validation and report paired held-out differences.

    The caller must supply independently executed, disjoint public-task runs.
    This function requires identical seeds, update steps, token budget,
    dataset revision and starting checkpoint across every method.
    """
    if len(runs) < 6 or len({row.method for row in runs}) < 2:
        raise ValueError("at least two methods and three seeds each are required")
    methods = sorted({row.method for row in runs})
    if baseline not in methods:
        raise ValueError("baseline method is missing")
    by_method = {method: {row.seed: row for row in runs if row.method == method}
                 for method in methods}
    seeds = set(by_method[baseline])
    if len(seeds) < 3 or any(set(rows) != seeds for rows in by_method.values()):
        raise ValueError("all methods must share at least three distinct seeds")
    if len(runs) != len(methods) * len(seeds):
        raise ValueError("duplicate method/seed pair")
    reference = runs[0]
    budget = (reference.update_steps, reference.generated_tokens,
              reference.dataset_revision, reference.checkpoint_revision)
    if reference.update_steps < 1 or reference.generated_tokens < 1:
        raise ValueError("update and token budgets must be positive")
    for row in runs:
        if (row.update_steps, row.generated_tokens,
                row.dataset_revision, row.checkpoint_revision) != budget:
            raise ValueError("public-task budgets or revisions differ")
        if not (isfinite(row.validation_score) and isfinite(row.test_score)):
            raise ValueError("scores must be finite")
    validation_means = {
        method: mean(by_method[method][seed].validation_score for seed in seeds)
        for method in methods
    }
    # Stable tie: retain the named baseline rather than choosing on test.
    winner = baseline
    for method in methods:
        if ((validation_means[method] > validation_means[winner]) if maximize else
                (validation_means[method] < validation_means[winner])):
            winner = method
    paired = tuple(
        by_method[winner][seed].test_score - by_method[baseline][seed].test_score
        for seed in sorted(seeds)
    )
    return {
        "selected_by": "validation_only",
        "test_used_for_selection": False,
        "winner": winner,
        "baseline": baseline,
        "seeds": sorted(seeds),
        "validation_mean_by_method": validation_means,
        "paired_test_differences": paired,
        "paired_test_difference_mean": mean(paired),
        "budget": {
            "update_steps": reference.update_steps,
            "generated_tokens": reference.generated_tokens,
            "dataset_revision": reference.dataset_revision,
            "checkpoint_revision": reference.checkpoint_revision,
        },
    }
