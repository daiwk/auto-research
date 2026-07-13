import numpy as np

from auto_research.reproductions.longer.model import LONGERScorer
from auto_research.reproductions.mixformer.model import MixFormerScorer
from auto_research.reproductions.onerec.model import OneRecScorer


class _Backbone:
    context = np.asarray([[1.0, 0.0], [0.8, 0.2], [0.0, 1.0]])
    item = context.copy()

    def scores(self, previous, candidates):
        return self.item[candidates] @ self.context[previous]


def test_longer_merges_old_and_recent_tokens():
    scorer = LONGERScorer(_Backbone(), merge_weight=0.5, group_size=2)
    assert scorer.longer_scores((0, 1, 2)).shape == (3,)
    assert not np.allclose(
        scorer.longer_scores((0, 1, 2)), scorer.recent_transformer_scores((0, 1, 2))
    )


def test_mixformer_unifies_dense_and_sequence_interactions():
    features = np.asarray([[1.0, 0.0], [0.8, 0.2], [0.0, 1.0]])
    scorer = MixFormerScorer(_Backbone(), features, cross_weight=0.2)
    assert not np.allclose(scorer.stacked_scores((0, 1)), scorer.unified_scores((0, 1)))


def test_onerec_preference_alignment_changes_session_scores():
    features = np.asarray([[1.0, 0.0], [0.8, 0.2], [0.0, 1.0]])
    scorer = OneRecScorer(
        _Backbone(), features, np.asarray([3.0, 2.0, 1.0]), 0.3, 0.1
    )
    assert not np.allclose(scorer.session_scores((0, 1)), scorer.aligned_scores((0, 1)))
