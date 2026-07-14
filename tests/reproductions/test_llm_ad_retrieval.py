from pathlib import Path

import numpy as np

from auto_research.reproductions.llm_ad_retrieval.data import RetrievalData, creative
from auto_research.reproductions.llm_ad_retrieval.model import (
    SemanticRepresentation,
    collaborative_matrix,
    evaluate,
    fuzzy_relevance,
    graph_stability,
    parse_representation,
    stat_sig_difference,
)
from auto_research.reproductions.registry import get_adapter


def test_adapter_carries_quantified_online_ab_evidence():
    adapter = get_adapter("llm-ad-retrieval")
    assert adapter.paper.has_online_ab
    assert adapter.paper.online_ab[0].lift_percent == 0.45


def test_hierarchical_parser_and_phrase_token_backoff():
    left = parse_representation(
        "CATEGORY: beauty, skin care\nATTRIBUTES: moisturizer, dry skin"
    )
    right = parse_representation(
        "CATEGORY: beauty, facial care\nATTRIBUTES: skin moisturizer, dry skin"
    )
    assert "beauty" in left.categories
    assert "moisturizer" in left.attributes
    assert fuzzy_relevance(left, right) > 0


def test_stat_sig_difference_matches_paper_guardrail():
    assert stat_sig_difference(0, 0, 1.0) == 0
    assert stat_sig_difference(1000, 1000, 0.20) > 0
    assert stat_sig_difference(10, 10, 0.05) == 0


def test_graph_route_runs_at_matched_budget():
    data = RetrievalData(
        titles=("a", "b", "c", "d", "e", "f"),
        genres=(("x",),) * 6,
        train=((0, 1, 2), (0, 1, 3), (4, 1, 2)),
        validation=(3, 2, 5),
        test=(4, 5, 3),
    )
    collaborative = collaborative_matrix(data)
    semantic = np.eye(6, dtype=np.float32)
    semantic[4, 2] = semantic[2, 4] = 1
    result = evaluate(data, collaborative, semantic, 1.0, "test", 3, 42)
    assert 0 <= result["recall_at_k"] <= 1
    assert 0 <= result["ndcg_at_k"] <= 1


def test_stability_compares_primary_and_shadow_graphs():
    primary = [
        SemanticRepresentation(frozenset({"a"}), frozenset({str(index)}))
        for index in range(4)
    ]
    same = graph_stability(primary, primary, 2)
    assert same["neighbor_jaccard_at_k"] == 1.0
    assert same["mean_score_difference"] == 0.0
    assert "released 1999" in creative("Example (1999)", ("Drama",), True)
