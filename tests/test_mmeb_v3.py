import math

import pytest

from auto_research.multimodal.mmeb_v3 import (
    OmniCandidate, RankingCase, diagnostic, hit_at_one, ndcg_at_five, omni_target_ids,
    score_all_directions, score_omniset, score_task, task_macro_average,
)


def test_official_linear_and_exponential_gain_are_explicit_and_different():
    ranking, rel = ("weak", "strong"), {"strong": 3, "weak": 1}
    discount = 1 / math.log2(3)
    assert ndcg_at_five(ranking, rel, gain="linear") == pytest.approx((1 + 3 * discount) / (3 + discount))
    assert ndcg_at_five(ranking, rel, gain="exponential") == pytest.approx((1 + 7 * discount) / (7 + discount))
    assert ndcg_at_five((), rel, gain="linear") == 0
    assert ndcg_at_five(("unknown",), {}, gain="linear") == 0
    with pytest.raises(ValueError):
        ndcg_at_five(ranking, rel, gain="unspecified")


def test_task_categories_and_equal_task_weighting_are_not_query_weighted():
    case = RankingCase("q", ("wrong", "right"), ("wrong", "right"), {"right": 1})
    for category in ("audio", "image", "video", "agent"):
        assert score_task([case], category=category) == 0
    for category in ("text", "visdoc"):
        assert score_task([case], category=category, ndcg_gain="linear") == pytest.approx(1 / math.log2(3))
    assert task_macro_average({"task-with-1000queries": .1, "task-with-1query": .9},
                              expected_tasks=["task-with-1000queries", "task-with-1query"]) == .5
    with pytest.raises(ValueError, match="exact"):
        task_macro_average({"one": .5}, expected_tasks=["one", "missing"])
    with pytest.raises(ValueError, match="OmniSET"):
        score_task([case], category="omniset")


def pool():
    return [OmniCandidate(f"{semantic}-{modality}", semantic, modality)
            for semantic in ("same", "other") for modality in "TIVA"]


def test_omniset_semantics_does_not_substitute_for_requested_modality():
    candidates = pool()
    query = candidates[1]
    assert query.modality == "I"
    wrong = score_omniset(query, candidates, ("same-I", "same-A"), target_modality="A")
    assert wrong["semantic_match_at_one"] == 1 and wrong["requested_modality_at_one"] == 0
    assert wrong["semantic_and_modality_hit_at_one"] == 0
    other = score_omniset(query, candidates, ("other-A",), target_modality="A")
    assert other["semantic_match_at_one"] == 0 and other["requested_modality_at_one"] == 1
    assert score_omniset(query, candidates, ("same-A",), target_modality="A")["semantic_and_modality_hit_at_one"] == 1


def test_one_shared_pool_twelve_directions_and_no_leaderboard_mixing():
    candidates = pool()
    queries = [item for item in candidates if item.semantic_id == "same"]
    rankings = {(source, target): (f"same-{target}", f"same-{source}")
                for source in "TIVA" for target in "TIVA" if source != target}
    result = score_all_directions(queries, candidates, rankings)
    assert len(result["directions"]) == 12 and result["shared_candidate_count"] == 8
    assert result["included_in_leaderboard"] is False
    assert all(value["semantic_and_modality_hit_at_one"] == 1 for value in result["directions"].values())
    del rankings["T", "A"]
    with pytest.raises(ValueError, match="twelve"):
        score_all_directions(queries, candidates, rankings)


def test_removing_input_or_filtering_to_target_modality_is_not_official_pool():
    candidates = pool()
    query = candidates[1]
    with pytest.raises(ValueError, match="distractor"):
        omni_target_ids(query, [item for item in candidates if item != query], target_modality="A")
    with pytest.raises(ValueError, match="four modalities"):
        omni_target_ids(query, candidates[:-1], target_modality="A")
    with pytest.raises(ValueError, match="cross-modality"):
        omni_target_ids(query, candidates, target_modality="I")


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -1, True])
def test_invalid_relevance_rejected(bad):
    with pytest.raises(ValueError):
        hit_at_one(["a"], {"a": bad})


def test_duplicate_and_unknown_ids_rejected():
    with pytest.raises(ValueError, match="unique"):
        hit_at_one(["a", "a"], {"a": 1})
    with pytest.raises(ValueError, match="pool"):
        RankingCase("q", ("a",), ("b",), {"a": 1})


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_contract(seed):
    assert all(diagnostic(seed)["checks"].values())
    assert diagnostic(seed)["evaluation_tier"] == "l0_interface"
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, "cuda")
