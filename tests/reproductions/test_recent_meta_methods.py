import numpy as np

from auto_research.reproductions.cmsl.model import CMSLScorer, semantic_assignments
from auto_research.reproductions.g2rec.model import G2RecScorer


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


def test_g2rec_interest_tokens_change_item_only_scores():
    graph = np.asarray([[0.0, 1.0, 0.0], [1.0, 0.0, 0.2], [0.0, 0.2, 0.0]])
    membership = np.asarray([[1.0, 0.0], [0.8, 0.2], [0.0, 1.0]])
    scorer = G2RecScorer(graph, membership, beta=0.5)
    assert not np.allclose(scorer.item_only_scores((0,)), scorer.interest_token_scores((0,)))
