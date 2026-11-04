import numpy as np
import pytest

from auto_research.reproductions.wesearch_components import (
    IndexSnapshot, adc_squared_distance, candidates, coarse_shortlist, diagnostic, mount,
    quantize, reconstruct,
)


@pytest.mark.parametrize('seed', [42,43,44])
def test_diagnostic(seed):
    result = diagnostic(seed)
    assert all(result['checks'].values())
    assert result['adc_max_absolute_error'] < 1e-12


def fixture():
    books = np.array([[[0.,0.],[1.,0.]], [[0.,0.],[0.,2.]]])
    codes = np.array([[0,0],[1,1],[1,0]])
    snapshot = IndexSnapshot('v1', np.array([3,1,2]), np.array([0,1,1]), codes)
    return books, codes, snapshot


def test_adc_uses_subspace_lookup_and_rotated_query():
    books, codes, _ = fixture()
    r = np.eye(4)[::-1]
    q = np.array([2.,1.,0.,1.])
    actual = adc_squared_distance(q,r,books,codes)
    expected = ((reconstruct(codes,books) - r@q)**2).sum(-1)
    np.testing.assert_allclose(actual,expected)
    np.testing.assert_array_equal(quantize(reconstruct(codes,books)@r,r,books),codes)


def test_candidate_union_then_shortlist_not_full_corpus():
    books, _, snapshot = fixture()
    centers = np.array([[0.,0.,0.,0.],[1.,0.,0.,0.]])
    selected, positions = candidates(np.zeros(4),centers,snapshot,top_clusters=1)
    np.testing.assert_array_equal(selected,[0])
    np.testing.assert_array_equal(positions,[0])
    ids, scores = coarse_shortlist(np.zeros(4),np.eye(4),books,snapshot,positions,top_documents=1)
    assert ids.tolist()==[3] and scores.tolist()==[0.]


def test_mount_keeps_old_version_immutable_and_fixed_artifacts():
    books, codes, snapshot = fixture()
    codes[0,0] = 1
    assert snapshot.codes[0,0]==0
    with pytest.raises(ValueError):
        snapshot.codes[0,0]=1
    updated=mount(snapshot,revision='v2',document_ids=np.array([4]),embeddings=np.array([[1.,0.,0.,2.]]),
                  cluster_embeddings=np.array([[0.,0.,0.,0.],[1.,0.,0.,2.]]),rotation=np.eye(4),codebooks=books)
    assert snapshot.document_ids.tolist()==[3,1,2]
    assert updated.document_ids.tolist()==[3,1,2,4]
    assert updated.assignments[-1]==1 and updated.codes[-1].tolist()==[1,1]


@pytest.mark.parametrize('codes', [np.array([[-1,0]]),np.array([[2,0]]),np.array([[.5,0.]]),np.array([[0]])])
def test_invalid_codes_fail_closed(codes):
    books,_,_=fixture()
    with pytest.raises(ValueError):
        adc_squared_distance(np.zeros(4),np.eye(4),books,codes)


@pytest.mark.parametrize('count', [True,0,-1,3,1.5])
def test_invalid_cluster_budget(count):
    _,_,snapshot=fixture()
    with pytest.raises(ValueError):
        candidates(np.zeros(4),np.zeros((2,4)),snapshot,top_clusters=count)


def test_overflow_is_not_silently_ranked():
    with pytest.raises(ValueError):
        quantize(np.full((1,4),1e308),np.eye(4),np.zeros((2,2,2)))


def test_cpu_only_no_cuda_fallback():
    with pytest.raises(ValueError):
        diagnostic(device='cuda')


def test_small_inputs_cannot_expand_to_unbounded_reconstruction():
    # Each input is small; the 4096x4096 gather would exceed the fixed budget.
    with pytest.raises(ValueError):
        reconstruct(np.zeros((4096,1),dtype=np.int64), np.zeros((1,1,4096)))
