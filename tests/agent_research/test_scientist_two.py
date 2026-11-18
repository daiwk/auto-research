"""ScientistTwo CPU scheduling/negative controls, not semantic research evaluation."""
import math

import pytest

from auto_research.agent_research.scientist_two import (
    Artifact, Assessment, Critique, Idea, Review, build_round, diagnostic,
    promote_subset, review_rebuttal, run_stage, search_decision, strict_refinement,
)


def artifact(idea="idea", version="v0"):
    return Artifact(idea, version, f"fixture://not-experimental/{version}")


def test_literal_stage_refines_then_accepts_only_reviewed_artifact():
    seen = []

    def critic(candidate):
        seen.append(candidate.artifact_id)
        return Critique("refine" if candidate.artifact_id == "v0" else "accept", "change it")

    result = run_stage(artifact(), critic, lambda x, feedback: artifact(version="v1"), max_rounds=3)
    assert seen == ["v0", "v1"]
    assert result.accepted == artifact(version="v1")
    assert result.refinement_calls == 1 and result.status == "accepted"


def test_literal_last_refinement_is_not_silently_accepted():
    calls = []

    def refine(candidate, feedback):
        calls.append(candidate.artifact_id)
        return artifact(version="unreviewed")

    result = run_stage(artifact(), lambda x: Critique("refine"), refine, max_rounds=1)
    assert result.accepted is None and result.status == "exhausted"
    assert len(result.observations) == 1 and calls == ["v0"]
    empty = run_stage(artifact(), lambda x: pytest.fail("no critic budget"), refine, max_rounds=0)
    assert empty.accepted is None and not empty.observations


def test_reject_stops_without_refinement_and_external_exceptions_propagate():
    result = run_stage(artifact(), lambda x: Critique("reject"), lambda *args: pytest.fail("must stop"),
                       max_rounds=2)
    assert result.status == "rejected" and result.refinement_calls == 0
    with pytest.raises(RuntimeError, match="judge unavailable"):
        run_stage(artifact(), lambda x: (_ for _ in ()).throw(RuntimeError("judge unavailable")),
                  lambda *args: artifact(), max_rounds=1)


@pytest.mark.parametrize("decision", ["Engineer", "Bad"])
def test_subset_non_good_never_launches_full_experiment(decision):
    assert promote_subset(Assessment(artifact(), "subset", decision),
                          lambda x: pytest.fail("full benchmark must not run")) is None


def test_subset_good_unlocks_exactly_one_full_result_without_fabricating_success():
    calls = []

    def full(candidate):
        calls.append(candidate)
        return Assessment(candidate, "full", "Bad", "full regression")

    result = promote_subset(Assessment(artifact(), "subset", "Good"), full)
    assert calls == [artifact()] and result.decision == "Bad"
    with pytest.raises(ValueError, match="identity"):
        promote_subset(Assessment(artifact(), "subset", "Good"),
                       lambda x: Assessment(artifact("other"), "full", "Good"))


def history():
    return [Assessment(artifact("failed"), "subset", "Bad", "negative evidence"),
            Assessment(artifact("passed"), "full", "Good", "positive evidence")]


def test_evolver_receives_full_history_and_seeds_explore_in_external_novelty_order():
    archive = history()
    seen = []

    def evolve(records, count):
        seen.extend(records)
        assert count == 1
        return [Idea("evolved", "externally proposed, not generated here", .1)]

    seeds = [Idea("failed", "already tried", 100), Idea("low", "fixture", 1),
             Idea("high", "fixture", 3), Idea("middle", "fixture", 2)]
    pool = build_round(seeds, archive, evolve, exploration_count=2)
    assert [x.idea_id for x in pool] == ["evolved", "high", "middle"]
    assert seen == archive and seen[0].feedback == "negative evidence"
    assert len(archive) == 2  # caller history remains unchanged


def test_oversized_or_reused_evolved_pool_rejected_not_truncated():
    for proposals in ([Idea("failed", "old", 1)],
                      [Idea("a", "fixture", 1), Idea("b", "fixture", 2)]):
        with pytest.raises(ValueError):
            build_round([], history(), lambda h, n: proposals, evolved_count=1)
    with pytest.raises(ValueError, match="closed"):
        build_round([], [Assessment(artifact(), "subset", "Good")], lambda h, n: [])


def test_search_exhaustion_retains_any_full_success_but_no_subset_success():
    assert search_decision(history(), rounds_completed=1) == "continue"
    assert search_decision(history(), rounds_completed=4) == "select_best_externally"
    failed = [Assessment(artifact("f"), "subset", "Bad")]
    assert search_decision(failed, rounds_completed=4) == "terminate_without_success"
    four = [Assessment(artifact(str(i)), "full", "Good") for i in range(4)]
    assert search_decision(four, rounds_completed=2) == "select_best_externally"


def test_strict_refinement_does_not_use_a_proxy_scalar_or_accept_ties():
    best, proposed = artifact(version="best"), artifact(version="new")
    seen = []

    def compare(new, old):
        seen.append((new, old))
        return False  # explicit fixture for tie/no established superiority

    kept, redo = strict_refinement(best, proposed, compare)
    assert kept is best and not redo and seen == [(proposed, best)]
    replaced, redo = strict_refinement(best, proposed, lambda new, old: True)
    assert replaced is proposed and redo
    with pytest.raises(ValueError, match="boolean"):
        strict_refinement(best, proposed, lambda new, old: 1)


def test_review_acceptance_threshold_and_rebuttal_budget():
    calls, rebuttals = [], []

    def review(draft):
        calls.append(draft.artifact_id)
        return Review(7 if len(calls) == 1 else 8, "external review fixture")

    def rebuttal(draft, report):
        rebuttals.append(report.score)
        return artifact(version="revised")

    result = review_rebuttal(artifact(), review, rebuttal)
    assert result.accepted and calls == ["v0", "revised"] and rebuttals == [7]
    immediate = review_rebuttal(artifact(), lambda x: Review(8, ""),
                               lambda *args: pytest.fail("already accepted"))
    assert immediate.accepted and immediate.rebuttal_calls == 0


def test_exhausted_reviews_do_not_allow_unreviewed_revision_or_call_it_accepted():
    result = review_rebuttal(artifact(), lambda x: Review(7.9, "below threshold"),
                            lambda *args: pytest.fail("no follow-up review slot"), maximum_reviews=1)
    assert not result.accepted and result.rebuttal_calls == 0 and result.artifact == artifact()


@pytest.mark.parametrize("bad", [True, -1, 1.5, "2", None])
def test_budgets_are_explicit_nonnegative_integers(bad):
    with pytest.raises(ValueError):
        run_stage(artifact(), lambda x: Critique("accept"), lambda x, y: x, max_rounds=bad)
    with pytest.raises(ValueError):
        review_rebuttal(artifact(), lambda x: Review(8, ""), lambda x, y: x, maximum_reviews=bad)


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), True, "8", 0, 11])
def test_review_scores_are_external_finite_and_on_declared_scale(bad):
    with pytest.raises(ValueError):
        Review(bad, "fixture")


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_cpu_control_evidence_only(seed):
    result = diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert all(type(value) is bool and value for value in result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, device="cuda")
