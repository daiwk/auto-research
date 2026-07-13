import numpy as np
from types import SimpleNamespace

from auto_research.reproductions.plum.data import build_cpt_corpus, build_sft_examples
from auto_research.reproductions.plum.model import (
    MovieMetadata,
    SID_END,
    SemanticIDIndex,
    TokenTrie,
    ranking_from_beams,
    residual_kmeans,
)


def test_residual_kmeans_builds_multiresolution_codes():
    rng = np.random.default_rng(4)
    features = rng.normal(size=(40, 8))
    codes, codebooks = residual_kmeans(features, (8, 4, 2), seed=3)
    assert codes.shape == (40, 3)
    assert [len(codebook) for codebook in codebooks] == [8, 4, 2]
    assert np.all(codes[:, 0] < 8)
    assert np.all(codes[:, 1] < 4)
    assert np.all(codes[:, 2] < 2)


def test_sid_vocabulary_has_one_token_namespace_per_level():
    index = SemanticIDIndex(
        codes=np.asarray([[0, 1], [1, 0]]), cardinalities=(2, 2)
    )
    assert index.tokens(0) == ("<sid_0_0>", "<sid_1_1>")
    assert index.text(0).endswith(SID_END)
    assert len(index.vocabulary()) == 5


def test_token_trie_only_allows_catalog_sid_sequences():
    trie = TokenTrie([(10, 20, 99), (10, 21, 99), (11, 22, 99)])
    assert trie.allowed(()) == (10, 11)
    assert trie.allowed((10,)) == (20, 21)
    assert trie.contains((10, 20, 99))
    assert not trie.contains((10, 22, 99))


def test_collision_expansion_penalizes_shared_sid_and_removes_history():
    ranking = ranking_from_beams(
        [((0, 0), -0.1), ((1, 1), -0.2)],
        {(0, 0): (0, 1), (1, 1): (2,)},
        history=(0,),
        popularity=np.asarray([3.0, 2.0, 1.0]),
    )
    assert 0 not in ranking
    assert set(ranking) == {1, 2}


def test_cpt_is_exactly_half_behavior_half_metadata_and_sft_masks_by_contract():
    sequences = SimpleNamespace(train=((0, 1, 2, 1, 0), (2, 1, 0, 2, 1)))
    metadata = MovieMetadata(
        titles=("zero", "one", "two"),
        genres=(("a",), ("b",), ("c",)),
    )
    index = SemanticIDIndex(
        codes=np.asarray([[0, 0], [0, 1], [1, 0]]), cardinalities=(2, 2)
    )
    corpus = build_cpt_corpus(sequences, metadata, index, seed=2, examples_per_source=4)
    assert len(corpus) == 8
    assert sum(row.startswith("watch history") for row in corpus) == 4
    assert sum(row.startswith("Video") for row in corpus) == 4
    sft = build_sft_examples(sequences, index, seed=2, maximum=10)
    assert sft
    assert all(row.prompt.endswith("next movie SID = ") for row in sft)
    assert all(row.completion.endswith(SID_END) for row in sft)
