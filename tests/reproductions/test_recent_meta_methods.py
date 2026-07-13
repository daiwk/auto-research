import numpy as np

from auto_research.reproductions.cmsl.model import CMSLScorer, semantic_assignments
from auto_research.reproductions.g2rec.model import coengagement_edges
from auto_research.reproductions.llatte.model import LLaTTEScorer
from auto_research.reproductions.memento.model import maximal_marginal_relevance
from auto_research.reproductions.self_evolving_rec.model import CANDIDATES


class _Model:
    context = np.asarray([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
    item = context.copy()


def test_cmsl_constructs_multiple_semantic_strands():
    features = np.asarray([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0]])
    assignments = semantic_assignments(features, clusters=2, seed=3)
    scorer = CMSLScorer(_Model(), assignments, alpha=1.0)
    scores = scorer.multi_sequence_scores((0, 2))
    assert scores.shape == (3,)
    assert len(set(assignments[[0, 2]])) == 2


def test_g2rec_builds_sparse_windowed_coengagement_graph():
    edges, weights, degree = coengagement_edges(((0, 1, 2), (2, 1)), 3, window=1)
    assert {tuple(edge) for edge in edges} == {(0, 1), (1, 2)}
    assert np.all(weights > 0)
    assert degree[1] > degree[0]


def test_memento_mmr_avoids_redundant_memories():
    documents = np.asarray([[1.0, 0.0], [0.99, 0.01], [0.0, 1.0]])
    selected = maximal_marginal_relevance(documents, np.asarray([1.0, 0.0]), 0.4, 2)
    assert selected == [0, 2]


def test_llatte_combines_online_and_cached_upstream_stages():
    scorer = LLaTTEScorer(_Model(), upstream_weight=0.5)
    assert scorer.two_stage_scores((0, 1, 2)).shape == (3,)


def test_self_evolving_search_contains_paper_discoveries():
    assert {candidate.optimizer for candidate in CANDIDATES} == {"adagrad", "rmsprop"}
    assert any(candidate.gated and candidate.multi_objective_reward for candidate in CANDIDATES)
