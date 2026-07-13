import numpy as np

from auto_research.reproductions.longer.model import LONGERScorer
from auto_research.reproductions.mixformer.model import training_examples
from auto_research.reproductions.onerec.model import TokenLayout, _catalog_transitions
from auto_research.reproductions.plum.model import SemanticIDIndex


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


def test_mixformer_training_examples_are_fixed_length_next_item_rows():
    rows = training_examples(((0, 1, 2),), length=3)
    assert rows == (((0, 0, 0), 1), ((0, 0, 1), 2))


def test_onerec_catalog_constraints_only_allow_observed_sid_prefixes():
    index = SemanticIDIndex(
        np.asarray([[0, 1, 0], [1, 0, 1]], dtype=np.int64), (2, 2, 2)
    )
    layout = TokenLayout.from_index(index)
    transitions = _catalog_transitions(index, layout)
    assert transitions[(0, ())] == [0, 1]
    assert transitions[(1, (0,))] == [layout.level_offsets[1] + 1]
