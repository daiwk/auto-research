"""ERA v1 flat-PUCT mechanism tests; no code generation or scientific evaluator."""
import math

import pytest

from auto_research.agent_research.era_flat_puct import Candidate, FlatPUCT, diagnostic


def candidate(key, score):
    return Candidate(key, "fixture://" + key, score)


def test_v1_singleton_and_formula_use_total_visits_flat_prior():
    tree = FlatPUCT(candidate("root", 10), 2)
    assert tree.nodes[0].visits == 1
    assert tree.rank_scores() == {"root": 1}
    assert tree.puct_scores() == {"root": 2}
    tree.expand("root", candidate("child", 20))
    assert tree.rank_scores() == {"root": 0, "child": 1}
    assert tree.puct_scores()["root"] == pytest.approx(math.sqrt(3) / 3)
    assert tree.puct_scores()["child"] == pytest.approx(1 + math.sqrt(3) / 2)


def test_flat_competition_and_ancestor_counts_without_reward_backpropagation():
    tree = FlatPUCT(candidate("root", 0), 0)
    tree.expand("root", candidate("middle", 1))
    tree.expand("middle", candidate("leaf", 2))
    tree.expand("root", candidate("sibling", -.5))
    assert tree.select().identity == "leaf"
    assert {node.candidate.identity: node.visits for node in tree.nodes} == {
        "root": 4, "middle": 2, "leaf": 1, "sibling": 1}
    assert tree.nodes[0].candidate.validation_score == 0
    assert tree.best().identity == "leaf"


def test_average_rank_and_stable_identity_ties_are_explicit_local_conventions():
    tree = FlatPUCT(candidate("z", 2), 0)
    tree.expand("z", candidate("a", 2))
    tree.expand("a", candidate("low", 0))
    assert tree.rank_scores() == {"z": .75, "a": .75, "low": 0}
    assert tree.select().identity == "a"
    assert tree.best().identity == "a"


def test_external_evaluation_only_and_zero_budget():
    tree = FlatPUCT(candidate("root", 0))
    calls = []

    def external(parent):
        calls.append(parent.identity)
        return candidate("new" + str(len(calls)), len(calls))

    assert tree.run(external, iterations=0).identity == "root"
    assert not calls
    assert tree.run(external, iterations=2).identity == "new2"
    assert len(calls) == 2


@pytest.mark.parametrize("value", [True, float("nan"), float("inf"), "1", None])
def test_untrusted_scores_and_constants_rejected(value):
    with pytest.raises(ValueError):
        candidate("x", value)
    with pytest.raises(ValueError):
        FlatPUCT(candidate("x", 1), value)


@pytest.mark.parametrize("value", [True, -1, 1.5, None])
def test_invalid_budget_rejected(value):
    with pytest.raises(ValueError):
        FlatPUCT(candidate("x", 1)).run(lambda parent: candidate("y", 2), iterations=value)


def test_bad_callback_duplicate_parent_and_negative_constant_fail_closed():
    tree = FlatPUCT(candidate("root", 0))
    for parent, result in [("missing", candidate("new", 1)), ("root", candidate("root", 1)), ("root", 2)]:
        with pytest.raises(ValueError):
            tree.expand(parent, result)
    assert len(tree.nodes) == 1
    with pytest.raises(ValueError):
        FlatPUCT(candidate("x", 1), -1)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_checks_and_cpu_only(seed):
    row = diagnostic(seed)
    assert all(row["checks"].values())
    assert row["diagnostic_only"] is True and row["evaluation_tier"] == "l1_mechanism"
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, "cuda")
