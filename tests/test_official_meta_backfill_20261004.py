import pytest

from auto_research.agent_research.official_meta_backfill_20261004 import (
    PAHFMemory,
    aira2_async_schedule,
    aira2_hidden_consistent_select,
    bounded_hyperagent_step,
    hyperagent_parent_probabilities,
    sira_filter_terms,
    sira_weighted_scores,
)
from auto_research.latest_20261004_catalog import LATEST_METHOD_PAPERS


def test_catalog_has_complete_p0_metadata():
    assert len(LATEST_METHOD_PAPERS) == 4
    assert {paper["priority"] for paper in LATEST_METHOD_PAPERS} == {"P0"}
    for paper in LATEST_METHOD_PAPERS:
        assert paper["published"] and paper["first_author_affiliation"]
        assert paper["paper_url"].startswith("https://arxiv.org/abs/")


def test_sira_df_gate_and_weighted_single_retrieval():
    terms = sira_filter_terms(
        ("rare", "missing", "common"), {"rare": 3, "common": 80},
        corpus_size=100, max_fraction=.1,
    )
    assert terms == ("rare",)
    assert sira_weighted_scores((1, 2), (4, 1), expansion_weight=.5) == (3.0, 2.5)
    assert sira_filter_terms(
        ("new",), {}, corpus_size=100, max_fraction=.1, query_side=False
    ) == ("new",)


def test_aira2_dispatches_without_generation_barrier_and_hides_final_signal():
    assignments = aira2_async_schedule((10, 1, 1), workers=2)
    assert assignments[2][2] == pytest.approx(1.0)  # fast worker starts task 3
    selected, audit = aira2_hidden_consistent_select(
        {"overfit": .99, "robust": .8}, {"overfit": .4, "robust": .9}
    )
    assert selected == "robust"
    assert audit["search_frontier"] == "overfit" and not audit["test_labels_visible"]


def test_pahf_asks_before_unknown_action_and_repairs_preference_drift():
    memory = PAHFMemory.empty()
    assert memory.pre_action("sleepy")["ask_clarification"]
    memory.integrate_pre_action_feedback("sleepy", "tea")
    assert memory.pre_action("sleepy")["preference"] == "tea"
    assert memory.integrate_post_action_feedback("sleepy", "coffee")
    assert memory.pre_action("sleepy")["preference"] == "coffee"


def test_hyperagent_selection_balances_frontier_and_novelty():
    probabilities = hyperagent_parent_probabilities((.9, .8), (20, 0), top_m=2)
    assert sum(probabilities) == pytest.approx(1.0)
    assert probabilities[1] > probabilities[0]  # novelty can offset score


def test_hyperagent_step_only_accepts_bounded_structured_variants():
    archive = ({"strategy": "base", "score": .5},)
    updated = bounded_hyperagent_step(
        archive, parent_index=0,
        modifier=lambda _: {"strategy": "reflect", "reflection": True},
        evaluator=lambda child: .8 if child["reflection"] else .1,
    )
    assert len(updated) == 2 and updated[-1]["score"] == pytest.approx(.8)
    with pytest.raises(ValueError, match="executable"):
        bounded_hyperagent_step(
            archive, parent_index=0,
            modifier=lambda _: {"strategy": "x", "shell": "rm -rf /"},
            evaluator=lambda _: 0,
        )
