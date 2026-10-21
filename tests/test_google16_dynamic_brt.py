import pytest

from auto_research.agent_research.google16_dynamic_brt import (
    Patch, execute_subset, normalized_implementation, review_patch, select_patch,
)

BUGGY = "def increment(x):\n    return x\n"
FIXED = "def increment(x):\n    return x + 1\n"
BRT = "assert increment(2) == 3\n"
REGRESSION = "assert increment(-1) == 0\n"


def review(patch):
    return review_patch(patch, buggy=BUGGY, regression=REGRESSION, bug_report="increment by one")


def test_actual_subprocess_fail_to_pass_not_a_precomputed_flag():
    result = review(Patch("good", FIXED, BRT))
    assert result.accepted and result.candidate_brt
    assert result.buggy_brt.outcome == "assertion_failed"
    assert result.patched_brt.outcome == "passed"
    assert result.regression.outcome == "passed"
    assert not result.semantic_reviewer_observed


def test_trivial_or_broken_tests_do_not_count_as_brt():
    assert not review(Patch("trivial", FIXED, "assert 1 == 1")).accepted
    assert not review(Patch("broken", FIXED, "assert increment(1 // 0) == 2")).accepted
    result = execute_subset(FIXED, "assert increment(1 // 0) == 2")
    assert result.outcome == "error" and result.detail == "ZeroDivisionError"
    with pytest.raises(ValueError):
        execute_subset(FIXED, "")


@pytest.mark.parametrize("source", [
    "import os\n", "def increment(x):\n    return x.__class__\n",
    "def increment(x):\n    return open(x)\n", "def increment(x):\n    while True: pass\n",
    "def increment(x=1):\n    return x\n", "def increment(x):\n    return 2 ** x\n",
])
def test_outside_subset_rejected_before_process(source):
    with pytest.raises(ValueError):
        execute_subset(source, BRT)


def test_reviewer_callback_sees_no_oracle_and_can_reject():
    seen = []

    def reviewer(report, patch, before):
        seen.append((report, patch.key, before.outcome))
        return False

    result = review_patch(Patch("good", FIXED, BRT), buggy=BUGGY,
                          regression=REGRESSION, bug_report="increment by one",
                          semantic_reviewer=reviewer)
    assert not result.accepted and result.semantic_reviewer_observed
    assert seen == [("increment by one", "good", "assertion_failed")]


def test_ranked_keeps_brt_in_majority_fix_group_unlike_dual():
    reviews = tuple(review(Patch(str(i), FIXED, BRT if i == 0 else None)) for i in range(3))
    assert select_patch(reviews, strategy="ranked").key == "0"
    assert select_patch(reviews, strategy="dual").brt is None


def test_normalization_groups_identifier_variants_not_different_constant():
    alternate = "def successor(value):\n    return value + 1\n"
    assert normalized_implementation(FIXED) == normalized_implementation(alternate)
    assert normalized_implementation(FIXED) != normalized_implementation(BUGGY)
    assert select_patch((review(Patch("wrong", BUGGY, BRT)),)) is None
