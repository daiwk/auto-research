"""SIMQ finite centroid-graph query and SIMQ+ tie-preserving count selection.

An exact finite kNN proximity graph and Lloyd binary splitting are deliberately
small-data backends, not HNSW/VSAG performance reproductions. Query traversal is
bounded graph navigation. Full token-by-centroid interaction is not queried.
"""

from collections import Counter
import heapq
import numpy as np

REQUIRES_GPU_VALIDATION = False


def normalized(x):
    x = np.asarray(x, dtype=float)
    norm = np.linalg.norm(x, axis=-1, keepdims=True)
    if x.ndim != 2 or not x.size or not np.isfinite(x).all() or (norm <= 1e-12).any():
        raise ValueError("finite nonzero token vectors required")
    return x / norm


def _graph(points, degree):
    return tuple(
        tuple(
            sorted(
                (j for j in range(len(points)) if i != j), key=lambda j: (-points[i] @ points[j], j)
            )[:degree]
        )
        for i in range(len(points))
    )


def _navigate(points, graph, query, count, beam):
    result = {0: float(query @ points[0])}
    queue = [(-result[0], 0)]
    seen = {0}
    while queue:
        negative, x = heapq.heappop(queue)
        if len(result) == beam and -negative < min(result.values()):
            break
        for y in graph[x]:
            if y in seen:
                continue
            seen.add(y)
            score = float(query @ points[y])
            if len(result) < beam or score > min(result.values()):
                result[y] = score
                heapq.heappush(queue, (-score, y))
                if len(result) > beam:
                    del result[min(result, key=lambda j: (result[j], -j))]
    return sorted(result, key=lambda j: (-result[j], j))[:count]


class Index:
    def __init__(self, documents, *, ratio=0.2, cluster_limit=8, degree=8, seed=42):
        if (
            not documents
            or not 0 < ratio <= 1
            or type(cluster_limit) is not int
            or cluster_limit < 1
            or degree < 1
        ):
            raise ValueError(
                "nonempty corpus, bounded sampling ratio and cluster settings required"
            )
        self.documents = tuple(normalized(d) for d in documents)
        if len({d.shape[1] for d in self.documents}) != 1:
            raise ValueError("one token dimension required")
        vectors = np.concatenate(self.documents)
        owner = np.repeat(np.arange(len(documents)), [len(d) for d in self.documents])
        rng = np.random.default_rng(seed)
        sample = np.sort(
            rng.choice(len(vectors), max(1, int(np.ceil(ratio * len(vectors)))), replace=False)
        )
        initial = vectors[sample]
        temporary = _graph(initial, min(degree, len(initial) - 1))
        buckets = {i: [int(v)] for i, v in enumerate(sample)}
        for token in sorted(set(range(len(vectors))) - set(sample)):
            hit = _navigate(
                initial, temporary, vectors[token], 1, min(len(initial), max(4, degree))
            )
            buckets[hit[0]].append(token)
        clusters = list(buckets.values())
        while any(len(c) > cluster_limit for c in clusters):
            c = next(c for c in clusters if len(c) > cluster_limit)
            clusters.remove(c)
            points = vectors[c]
            centers = points[[0, np.argmin(points @ points[0])]].copy()
            labels = np.zeros(len(c), dtype=int)
            for _ in range(12):
                new = (
                    (points - centers[1]).__pow__(2).sum(-1)
                    < (points - centers[0]).__pow__(2).sum(-1)
                ).astype(int)
                if len(np.unique(new)) < 2:
                    # Degenerate identical points: explicit balanced nonempty tie policy.
                    new = np.arange(len(c)) >= len(c) // 2
                if np.array_equal(new, labels):
                    break
                labels = new
                centers = np.stack([points[labels == j].mean(0) for j in range(2)])
            clusters.extend([[c[i] for i in range(len(c)) if labels[i] == j] for j in range(2)])
        self.centroids = normalized(np.stack([vectors[c].mean(0) for c in clusters]))
        self.members = tuple(frozenset(int(owner[t]) for t in c) for c in clusters)
        self.cluster_sizes = tuple(map(len, clusters))
        self.graph = _graph(self.centroids, min(degree, len(clusters) - 1))

    def query(
        self,
        query,
        *,
        centroid_count=2,
        beam=8,
        documents_per_token=4,
        rerank=6,
        k=3,
        plus=False,
        minimum_candidates=4,
    ):
        query = normalized(query)
        if (
            query.shape[1] != self.centroids.shape[1]
            or not 1 <= centroid_count <= beam <= len(self.centroids)
            or min(documents_per_token, rerank, k, minimum_candidates) < 1
            or k > rerank
        ):
            raise ValueError("valid query and positive bounded retrieval budgets required")
        approximate = Counter()
        counts = Counter()
        for token in query:
            hits = _navigate(self.centroids, self.graph, token, centroid_count, beam)
            scores = {}
            for h in hits:
                score = float(token @ self.centroids[h])
                for d in self.members[h]:
                    scores[d] = max(scores.get(d, -np.inf), score)
            counts.update(scores.keys())  # exactly one hit per document per query token
            for d in sorted(scores, key=lambda d: (-scores[d], d))[:documents_per_token]:
                approximate[d] += scores[d]
        if plus:
            if len(counts) < minimum_candidates:
                selected = list(counts)
            else:
                threshold = max(
                    t
                    for t in set(counts.values())
                    if sum(c >= t for c in counts.values()) >= minimum_candidates
                )
                selected = [d for d, c in counts.items() if c >= threshold]
        else:
            selected = sorted(approximate, key=lambda d: (-approximate[d], d))[:rerank]
        exact = {d: float((query @ self.documents[d].T).max(-1).sum()) for d in selected}
        return {
            "ranking": sorted(exact, key=lambda d: (-exact[d], d))[:k],
            "candidates": sorted(selected),
            "counts": dict(counts),
            "exact_scores": exact,
        }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    if device != "cpu":
        raise ValueError("CPU graph implementation only")
    rng = np.random.default_rng(seed)
    docs = [rng.normal(size=(5, 6)) for _ in range(12)]
    index = Index(docs, ratio=0.3, cluster_limit=5, degree=8, seed=seed)
    out = index.query(
        docs[0][:3],
        centroid_count=2,
        beam=min(8, len(index.centroids)),
        plus=True,
        minimum_candidates=4,
    )
    selected = set(out["candidates"])
    boundary = min((out["counts"][d] for d in selected), default=0)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "bounded_clusters": max(index.cluster_sizes) <= 5,
            "every_token_assigned": sum(index.cluster_sizes) == 60,
            "distinct_token_hit_count": max(out["counts"].values()) <= 3,
            "ties_not_split": all(
                (c >= boundary) == (d in selected) for d, c in out["counts"].items()
            ),
            "exact_rerank_only_candidates": set(out["exact_scores"]) == selected,
        },
        "metrics": {
            "centroid_count": len(index.centroids),
            "rerank_candidates": len(selected),
            "corpus_documents": len(docs),
        },
    }
