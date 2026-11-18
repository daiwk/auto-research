"""Finite UniGraph Alg1/2 and dense-first pruning; not a scalable ANN benchmark.

Exact all-pairs construction and exact guide lookup are explicit small-data
backends. Traversal is the actual bounded graph algorithm, never exact rerank
masquerading as successful graph recall. gamma<1 pruning is NOT safe.
"""

from collections import Counter
import heapq
import numpy as np

REQUIRES_GPU_VALIDATION = False


def _matrix(value):
    value = np.asarray(value, dtype=float)
    if value.ndim != 2 or not value.size or not np.isfinite(value).all():
        raise ValueError("finite nonempty matrix required")
    return value


def alpha_cover(dense, sparse, alphas=(0.0, 0.25, 0.5, 0.75, 1.0), neighbors=4, degree=8):
    dense, sparse = _matrix(dense), _matrix(sparse)
    n = len(dense)
    if (
        len(sparse) != n
        or not 1 <= neighbors < n
        or not 1 <= degree < n
        or not alphas
        or any(not 0 <= a <= 1 for a in alphas)
    ):
        raise ValueError("aligned data, valid alpha sample and degree required")
    graph = []
    for i in range(n):
        dd, ds = 1 - dense @ dense[i], 1 - sparse @ sparse[i]
        counts = Counter()
        for alpha in alphas:
            counts.update(
                sorted(
                    (j for j in range(n) if j != i),
                    key=lambda j: (alpha * dd[j] + (1 - alpha) * ds[j], j),
                )[:neighbors]
            )
        graph.append(tuple(sorted(counts, key=lambda j: (-counts[j], j))[:degree]))
    return tuple(graph)


def search(
    dense,
    sparse,
    graph,
    qd,
    qs,
    *,
    alpha: float,
    k: int = 3,
    beam: int = 8,
    gamma: float = 1.0,
    guide_count: int = 1,
    prune: bool = True,
):
    dense, sparse = _matrix(dense), _matrix(sparse)
    qd, qs = np.asarray(qd, dtype=float), np.asarray(qs, dtype=float)
    n = len(dense)
    if (
        len(sparse) != n
        or len(graph) != n
        or qd.shape != dense.shape[1:]
        or qs.shape != sparse.shape[1:]
        or not np.isfinite(qd).all()
        or not np.isfinite(qs).all()
        or not 0 <= alpha <= 1
        or not 0 <= gamma <= 1
        or not 1 <= k <= beam <= n
        or not 1 <= guide_count <= beam
        or any(j == i or not 0 <= j < n for i, edges in enumerate(graph) for j in edges)
    ):
        raise ValueError("valid aligned graph/query, alpha, gamma and bounded beam required")
    dense_dist = 1 - dense @ qd
    guide_dist = dense_dist if alpha > 0.5 else 1 - sparse @ qs
    entries = sorted(range(n), key=lambda j: (guide_dist[j], j))[:guide_count]

    def exact(j):
        return float(alpha * dense_dist[j] + (1 - alpha) * (1 - sparse[j] @ qs))

    result = {j: exact(j) for j in entries}
    candidates = [(d, j) for j, d in result.items()]
    heapq.heapify(candidates)
    seen = set(entries)
    sparse_evals = len(entries)
    pruned = 0
    while candidates:
        dx, x = heapq.heappop(candidates)
        worst = max(result.values())
        if len(result) == beam and dx > worst:
            break
        for y in graph[x]:
            if y in seen:
                continue
            seen.add(y)
            estimate = alpha * dense_dist[y] + (1 - alpha) * (
                1 - gamma * np.linalg.norm(qs) * np.linalg.norm(sparse[y])
            )
            if prune and len(result) == beam and estimate >= worst:
                pruned += 1
                continue
            dy = exact(y)
            sparse_evals += 1
            if len(result) < beam or dy < worst:
                result[y] = dy
                heapq.heappush(candidates, (dy, y))
                if len(result) > beam:
                    del result[max(result, key=lambda j: (result[j], j))]
                worst = max(result.values())
    ranking = sorted(result, key=lambda j: (result[j], j))[:k]
    return {
        "ranking": ranking,
        "sparse_evaluations": sparse_evals,
        "pruned": pruned,
        "visited": len(seen),
        "safe_pruning": gamma == 1,
        "guide": "dense" if alpha > 0.5 else "sparse",
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    if device != "cpu":
        raise ValueError("CPU graph implementation only")
    rng = np.random.default_rng(seed)
    dense = rng.normal(size=(24, 5))
    sparse = rng.uniform(size=(24, 7)) * (rng.random((24, 7)) < 0.3)
    graph = alpha_cover(dense, sparse, neighbors=4, degree=8)
    qd, qs = rng.normal(size=5), rng.uniform(size=7)
    safe = search(dense, sparse, graph, qd, qs, alpha=0.4, beam=10)
    plain = search(dense, sparse, graph, qd, qs, alpha=0.4, beam=10, prune=False)
    dense_run = search(dense, sparse, graph, qd, qs, alpha=0.8, beam=10)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "bounded_degree": max(map(len, graph)) <= 8,
            "no_self_edge": all(i not in e for i, e in enumerate(graph)),
            "gamma1_preserves_unpruned_beam": safe["ranking"] == plain["ranking"],
            "sparse_distance_not_more_calls": safe["sparse_evaluations"]
            <= plain["sparse_evaluations"],
            "adaptive_guide": safe["guide"] == "sparse" and dense_run["guide"] == "dense",
        },
        "metrics": {
            "finite_graph_vertices": len(graph),
            "safe_sparse_evaluations": safe["sparse_evaluations"],
            "unpruned_sparse_evaluations": plain["sparse_evaluations"],
        },
    }
