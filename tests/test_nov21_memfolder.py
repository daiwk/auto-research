"""Explicit record grouping, with no LLM, filesystem or evaluation-answer access."""
import itertools
import math

import pytest

from auto_research.agent_research import memfolder


def test_anchor_selection_is_progressive_and_distinct():
    vectors = [(1., 0.), (.99, .01), (-1., 0.), (0., 1.)]
    anchors = memfolder.progressive_anchors(vectors, 4)
    assert len(set(anchors)) == 4
    assert set(anchors) == {0, 1, 2, 3}
    assert memfolder.progressive_anchors(vectors, 2) == anchors[:2]
    assert memfolder.progressive_anchors([(1.,)], 1) == (0,)


def test_common_or_absent_entities_recover_cosine():
    vectors = [(1., 0.), (0., 1.), (-1., 0.)]
    for labels in ([set(), set(), set()], [{"common"}] * 3):
        affinity, metadata = memfolder.entity_affinity(vectors, labels)
        assert affinity[0] == pytest.approx([1, 0, -1])
        assert metadata["variance_pairs"] == 3
        assert metadata["entity_variance"] == 1e-6
        assert metadata["common_entity_zero_weight"]


def test_rare_shared_entity_increases_affinity_and_window_counts_before_filter():
    vectors = [(1., 0.), (0., 1.), (-1., 0.), (0., -1.)]
    affinity, metadata = memfolder.entity_affinity(vectors, [{"rare"}, {"rare"}, set(), set()], window=2)
    assert 0 < affinity[0][1] < 1
    assert metadata["variance_pairs"] == 5
    assert metadata["variance_convention"] == "population_ddof0"


def test_hungarian_global_solution_not_greedy(monkeypatch):
    vectors = [(1., 0., 0.), (0., 1., 0.), (0., 0., 1.), (0., .6, .8)]
    matrix = [[0., 0., .9, .8], [0., 0., .8, 0.], [0.] * 4, [0.] * 4]
    monkeypatch.setattr(memfolder, "progressive_anchors", lambda *a, **kw: (0,))
    monkeypatch.setattr(memfolder, "entity_affinity", lambda *a, **kw: (matrix, {"variance_pairs": 6}))
    output = memfolder.record_partition(vectors, [set()] * 4, keep_ratio=.25)
    assert {(p, s) for p, s, _ in output.links} == {(0, 3), (1, 2)}
    assert sum(g for _, _, g in output.links) == pytest.approx(1.6)


def test_anchors_never_receive_links_and_groups_preserve_all_records():
    vectors = [(1., .2), (.9, .1), (-1., .2), (-.9, .1), (.2, 1.)]
    result = memfolder.record_partition(vectors, [{"a"}, {"a"}, {"b"}, {"b"}, {"c"}], keep_ratio=.6)
    assert len(result.groups) == 3
    assert sorted(itertools.chain.from_iterable(result.groups)) == list(range(5))
    assert all(a in group for a, group in zip(result.anchors, result.groups, strict=True))
    assert all(p < s and s not in result.anchors for p, s, _ in result.links)
    assert len({p for p, _, _ in result.links}) == len(result.links)
    assert len({s for _, s, _ in result.links}) == len(result.links)


def test_duplicate_embeddings_keep_nonempty_anchor_groups():
    result = memfolder.record_partition([(1., 0.)] * 4, [set()] * 4)
    assert len(result.groups) == 2 and all(result.groups)
    assert result.links == ()


@pytest.mark.parametrize("vectors", [[], [(0., 0.)], [(1., 0.), (1.,)], [(math.nan,)], [(math.inf,)]])
def test_bad_embedding_vectors_rejected(vectors):
    with pytest.raises(ValueError):
        memfolder.progressive_anchors(vectors, 1)


def test_bad_counts_ratios_labels_and_budget():
    for ratio in (0, -1, 1.01, True, math.nan):
        with pytest.raises(ValueError):
            memfolder.record_partition([(1.,)], [set()], keep_ratio=ratio)
    with pytest.raises(ValueError):
        memfolder.entity_affinity([(1.,)], ["not-a-label-set"])
    with pytest.raises(ValueError):
        memfolder.record_partition([(1.,)] * (memfolder.MAX_RECORDS + 1), [set()] * (memfolder.MAX_RECORDS + 1))


def test_diagnostic_never_advertises_cuda_or_capability():
    for seed in (42, 43, 44):
        result = memfolder.diagnostic(seed)
        assert result["seed"] == seed and result["diagnostic_only"] is True
        assert all(result["checks"].values())
    with pytest.raises(ValueError):
        memfolder.diagnostic(42, "cuda")
