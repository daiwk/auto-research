"""WeSearch v1 Eqs.2--15/26: CPU index and ADC kernels, not a retriever.

Embeddings, trained rotation, centroids and codebooks are caller inputs. No
query encoder, RQ-KMeans fitting, feature FFN, teacher or production service is
implemented. Diagnostics test identities, not retrieval quality.
"""
from dataclasses import dataclass

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _float(value, ndim):
    x = np.asarray(value)
    if (x.ndim != ndim or x.dtype.kind != 'f' or not 0 < x.size <= 1_048_576
            or not np.isfinite(x).all()):
        raise ValueError('bounded finite floating-point array required')
    return x


def _integer(value, ndim):
    x = np.asarray(value)
    if (x.ndim != ndim or x.dtype.kind not in 'iu' or not 0 < x.size <= 1_048_576):
        raise ValueError('bounded integer array required')
    return x


def _count(value, maximum):
    if type(value) is not int or not 1 <= value <= maximum:
        raise ValueError('positive count within the available range required')


def _finite_result(x):
    if not np.isfinite(x).all():
        raise ValueError('derived value is not finite')
    return x


def quantize(documents, rotation, codebooks):
    """Eq.7--10: nearest codeword per subspace; ties use the first codeword."""
    docs, r, b = _float(documents, 2), _float(rotation, 2), _float(codebooks, 3)
    m, k, width = b.shape
    dim = m * width
    if r.shape != (dim, dim) or docs.shape[1] != dim or len(docs) * m * k * width > 1_048_576:
        raise ValueError('aligned and bounded OPQ inputs required')
    rotated = _finite_result(docs @ r.T).reshape(len(docs), m, width)
    with np.errstate(over='ignore', invalid='ignore'):
        distance = ((rotated[:, :, None] - b[None]) ** 2).sum(-1)
    return _finite_result(distance).argmin(-1)


def reconstruct(codes, codebooks):
    """Eq.11 returns vectors in ROTATED space, not original embeddings."""
    z, b = _integer(codes, 2), _float(codebooks, 3)
    if z.shape[1] != len(b) or (z < 0).any() or (z >= b.shape[1]).any():
        raise ValueError('one valid integer code per subspace required')
    return b[np.arange(len(b))[None], z].reshape(len(z), -1)


def adc_squared_distance(query, rotation, codebooks, codes):
    """Eq.26 lookup sum equals squared L2 to reconstructed rotated vectors.

    Negative sqrt of the returned distances gives Eq.15 scores; do not compare
    these squared distances with an unrelated score threshold.
    """
    q, r, b = _float(query, 1), _float(rotation, 2), _float(codebooks, 3)
    z = _integer(codes, 2)
    dim = b.shape[0] * b.shape[2]
    if (q.shape != (dim,) or r.shape != (dim, dim) or z.shape[1] != len(b)
            or (z < 0).any() or (z >= b.shape[1]).any()):
        raise ValueError('aligned query, rotation and integer document codes required')
    rotated = _finite_result(r @ q).reshape(len(b), b.shape[2])
    with np.errstate(over='ignore', invalid='ignore'):
        table = ((rotated[:, None] - b) ** 2).sum(-1)
    _finite_result(table)
    return _finite_result(table[np.arange(len(b))[None], z].sum(-1))


@dataclass(frozen=True)
class IndexSnapshot:
    """Caller-owned immutable versioned artifact, not an atomic distributed store."""

    revision: str
    document_ids: np.ndarray
    assignments: np.ndarray
    codes: np.ndarray

    def __post_init__(self):
        ids, assignments, codes = (_integer(self.document_ids, 1),
                                   _integer(self.assignments, 1), _integer(self.codes, 2))
        if (not isinstance(self.revision, str) or not self.revision.strip()
                or len(ids) != len(assignments) or len(ids) != len(codes)
                or len(np.unique(ids)) != len(ids) or (assignments < 0).any() or (codes < 0).any()):
            raise ValueError('revision and aligned unique document artifacts required')
        for name, array in [('document_ids', ids), ('assignments', assignments), ('codes', codes)]:
            copied = array.copy()
            copied.flags.writeable = False
            object.__setattr__(self, name, copied)


def candidates(query, cluster_embeddings, snapshot, *, top_clusters):
    """Eqs.2/3/13: exact negative-L2 cluster selection and document union.

    Cluster embeddings may be sums of supplied two-level RQ codewords (Eq.6).
    This function does not fit those codewords or invent an ANN index.
    """
    q, centers = _float(query, 1), _float(cluster_embeddings, 2)
    _count(top_clusters, len(centers))
    if (centers.shape[1] != len(q) or (snapshot.assignments >= len(centers)).any()):
        raise ValueError('valid cluster assignments and embedding dimensions required')
    with np.errstate(over='ignore', invalid='ignore'):
        distances = ((centers - q) ** 2).sum(-1)
    selected = np.argsort(_finite_result(distances), kind='stable')[:top_clusters]
    mask = np.isin(snapshot.assignments, selected)
    positions = np.flatnonzero(mask)
    return selected, positions


def coarse_shortlist(query, rotation, codebooks, snapshot, positions, *, top_documents):
    """Algorithm1 step8 only; no stand-in for the feature-aware FFN ranker."""
    ix = _integer(positions, 1)
    if ((ix < 0).any() or (ix >= len(snapshot.codes)).any() or len(np.unique(ix)) != len(ix)):
        raise ValueError('unique valid candidate positions required')
    _count(top_documents, len(ix))
    distances = adc_squared_distance(query, rotation, codebooks, snapshot.codes[ix])
    order = np.lexsort((snapshot.document_ids[ix], distances))[:top_documents]
    return snapshot.document_ids[ix[order]], -np.sqrt(distances[order])


def mount(snapshot, *, revision, document_ids, embeddings, cluster_embeddings, rotation, codebooks):
    """Section5.2 builds a NEW snapshot using FIXED cluster/OPQ parameters.

    Visibility swap is the caller's responsibility. No model refresh, deletion,
    replacement, persistence or distributed atomicity is claimed.
    """
    ids = _integer(document_ids, 1)
    docs, centers = _float(embeddings, 2), _float(cluster_embeddings, 2)
    if (revision == snapshot.revision or len(ids) != len(docs) or docs.shape[1] != centers.shape[1]
            or np.intersect1d(ids, snapshot.document_ids).size or len(np.unique(ids)) != len(ids)
            or len(docs) * centers.size > 1_048_576):
        raise ValueError('new revision, new IDs and bounded aligned embeddings required')
    with np.errstate(over='ignore', invalid='ignore'):
        distances = ((docs[:, None] - centers[None]) ** 2).sum(-1)
    assignment = _finite_result(distances).argmin(-1)
    codes = quantize(docs, rotation, codebooks)
    return IndexSnapshot(revision, np.concatenate([snapshot.document_ids, ids]),
                         np.concatenate([snapshot.assignments, assignment]),
                         np.concatenate([snapshot.codes, codes]))


def diagnostic(seed=42, device='cpu'):
    if device != 'cpu':
        raise ValueError('this bounded index implementation is CPU-only')
    rng = np.random.default_rng(seed)
    dim = 8
    rotation, _ = np.linalg.qr(rng.normal(size=(dim, dim)))
    books = rng.normal(size=(2, 4, 4))
    docs = rng.normal(size=(12, dim))
    codes = quantize(docs, rotation, books)
    q = rng.normal(size=dim)
    actual = adc_squared_distance(q, rotation, books, codes)
    direct = ((reconstruct(codes, books) - rotation @ q) ** 2).sum(-1)
    snapshot = IndexSnapshot('initial', np.arange(12), np.arange(12) % 3, codes)
    centers = rng.normal(size=(3, dim))
    _, positions = candidates(q, centers, snapshot, top_clusters=2)
    shortlisted, scores = coarse_shortlist(q, rotation, books, snapshot, positions, top_documents=3)
    updated = mount(snapshot, revision='fresh', document_ids=np.array([100]), embeddings=docs[:1],
                    cluster_embeddings=centers, rotation=rotation, codebooks=books)
    return {'seed': seed, 'adc_max_absolute_error': float(np.max(abs(actual-direct))),
            'shortlist_size': int(len(shortlisted)), 'candidate_count': int(len(positions)),
            'fresh_document_count': int(len(updated.document_ids)-len(snapshot.document_ids)),
            'checks': {'adc_matches_reconstruction': bool(np.allclose(actual,direct,atol=1e-12)),
                       'snapshot_preserved': len(snapshot.document_ids)==12,
                       'scores_descending': bool(np.all(scores[:-1] >= scores[1:])),
                       'candidate_union_exact': len(positions)==8}}
