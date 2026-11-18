"""Bounded page-retrieval/scalability protocol for arXiv:2611.17726v1.

External embeddings and sealed relevance judgments are separate inputs. This is
not ColPali inference, a Qdrant deployment, or a library-scale production claim.
"""

from __future__ import annotations

import math
from statistics import mean
from typing import Mapping, Sequence

REQUIRES_GPU_VALIDATION = False
Vector = Sequence[float]


def late_interaction_score(
    query: Sequence[Vector], page: Sequence[Vector], *, metric: str = "cosine"
) -> float:
    """ColPali-style sum of each query token's best page-token similarity.

Distances are negated before max so that smaller distance is better. No
relevance label, article title or answer is accepted by this scoring function.
    """
    if metric not in {"cosine", "dot", "euclidean", "manhattan"}:
        raise ValueError("unsupported vector metric")
    if not query or not page or not query[0]:
        raise ValueError("query and page need nonempty token vectors")
    dim = len(query[0])
    for vector in [*query, *page]:
        if len(vector) != dim or any(not math.isfinite(x) for x in vector):
            raise ValueError("vectors must be finite and dimension aligned")
        if metric == "cosine" and not any(vector):
            raise ValueError("zero-norm cosine vectors are undefined")

    def similarity(a: Vector, b: Vector) -> float:
        if metric == "cosine":
            # Scale before hypot: even the norm of finite 1e308 components can
            # exceed float range, whereas their unit-vector directions exist.
            scale_a, scale_b = max(abs(x) for x in a), max(abs(x) for x in b)
            norm_a = math.hypot(*(x / scale_a for x in a))
            norm_b = math.hypot(*(y / scale_b for y in b))
            return math.fsum((x / scale_a / norm_a) * (y / scale_b / norm_b)
                             for x, y in zip(a, b, strict=True))
        if metric == "dot":
            products = [x * y for x, y in zip(a, b, strict=True)]
            if any(not math.isfinite(x) for x in products):
                raise ValueError("dot-product magnitude exceeds finite float range")
            return math.fsum(products)
        differences = [abs(x - y) for x, y in zip(a, b, strict=True)]
        return -math.fsum(differences) if metric == "manhattan" else -math.hypot(*differences)

    try:
        result = math.fsum(max(similarity(q, p) for p in page) for q in query)
    except (OverflowError, ArithmeticError) as error:
        raise ValueError("late-interaction score exceeds finite float range") from error
    if not math.isfinite(result):
        raise ValueError("late-interaction score exceeds finite float range")
    return result


def retrieval_metrics(
    ranked_page_ids: Sequence[str], relevant_page_ids: set[str], *, k: int = 5
) -> dict[str, float]:
    """Rank-aware top-k evaluation using externally held-out relevance judgments.

Unjudged pages are conservatively treated as not relevant, never auto-relabeled
because the retriever found them. AP@k divides by ALL known relevant pages, so a
top-five run is not confused with full-ranking MAP.
    """
    if k < 1 or len(set(ranked_page_ids)) != len(ranked_page_ids):
        raise ValueError("positive k and unique ranked page IDs required")
    if not relevant_page_ids:
        raise ValueError("recall/AP need nonempty known relevance judgments")
    ranking = ranked_page_ids[:k]
    hits = 0
    precision_sum = 0.0
    reciprocal_rank = 0.0
    for rank, page_id in enumerate(ranking, 1):
        if page_id in relevant_page_ids:
            hits += 1
            precision_sum += hits / rank
            if reciprocal_rank == 0:
                reciprocal_rank = 1 / rank
    precision, recall = hits / k, hits / len(relevant_page_ids)
    return {
        "precision_at_k": precision, "recall_at_k": recall,
        "f1_at_k": 2 * precision * recall / (precision + recall) if hits else 0.0,
        "ap_at_k": precision_sum / len(relevant_page_ids),
        "reciprocal_rank_at_k": reciprocal_rank,
    }


def subgroup_means(
    per_query: Mapping[str, Mapping[str, float]], groups: Mapping[str, Sequence[str]]
) -> dict[str, dict[str, float]]:
    """Explicit potentially overlapping query subsets; never a disjoint partition."""
    result = {}
    for name, ids in groups.items():
        if not ids or len(ids) != len(set(ids)) or set(ids).difference(per_query):
            raise ValueError("subgroup membership must be nonempty, unique and evaluated")
        fields = set(per_query[ids[0]])
        if any(set(per_query[i]) != fields for i in ids):
            raise ValueError("query metric schemas must match")
        if any(not math.isfinite(v) for i in ids for v in per_query[i].values()):
            raise ValueError("query metrics must be finite")
        result[name] = {field: mean(per_query[i][field] for i in ids) for field in sorted(fields)}
    return result


def timing_summary(
    latencies_ms: Sequence[float], *, elapsed_seconds: float,
    scope: str, warmup_excluded: int = 0,
) -> dict[str, float | int | str]:
    """Summarize actual caller measurements; QPS = requests / wall time.

Concurrent QPS is NOT inverse mean latency. The scope must explicitly identify
database-only/preencoded versus end-to-end measurements to avoid paper Table VII
and Section V-D's ambiguous mixture of benchmark descriptions.
    """
    if scope not in {"database_only_preencoded", "end_to_end_encoding_and_retrieval"}:
        raise ValueError("explicit measurement scope is required")
    if not latencies_ms or any(not math.isfinite(v) or v < 0 for v in latencies_ms):
        raise ValueError("latencies must be nonempty, finite and nonnegative")
    if not math.isfinite(elapsed_seconds) or elapsed_seconds <= 0 or warmup_excluded < 0:
        raise ValueError("positive finite wall time and nonnegative warmup count required")
    values = sorted(latencies_ms)

    def percentile(fraction: float) -> float:
        position = (len(values) - 1) * fraction
        low, high = math.floor(position), math.ceil(position)
        return values[low] + (values[high] - values[low]) * (position - low)

    return {
        "requests": len(values), "qps": len(values) / elapsed_seconds,
        "mean_latency_ms": mean(values), "p95_latency_ms": percentile(0.95),
        "p99_latency_ms": percentile(0.99), "scope": scope,
        "warmup_excluded": warmup_excluded,
    }


def diagnostic(seed: int, device: str = "cpu") -> dict[str, object]:
    if device != "cpu":
        raise ValueError("this retrieval arithmetic protocol supports CPU only")
    query = [[1.0, 0.0], [0.0, 1.0]]
    match = late_interaction_score(query, [[1.0, 0.0], [0.0, 1.0]])
    distractor = late_interaction_score(query, [[-1.0, -1.0]])
    ranked = ["distractor", "a", "b", "c", "d"]
    scores = retrieval_metrics(ranked, {"a", "c", "unretrieved"})
    reordered_scores = retrieval_metrics(["a", "c", "distractor", "b", "d"], {"a", "c", "unretrieved"})
    timing = timing_summary([10, 20, 30], elapsed_seconds=0.05, scope="database_only_preencoded")
    invalid_rejected = False
    try:
        retrieval_metrics(["a", "a"], {"a"})
    except ValueError:
        invalid_rejected = True
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
        "checks": {
            "maxsim_uses_page_tokens_not_gold": match > distractor,
            "ranking_changes_ap_not_just_hit_count": scores["ap_at_k"] != reordered_scores["ap_at_k"],
            "unretrieved_relevance_remains_recall_denominator": scores["recall_at_k"] == 2 / 3,
            "duplicate_predictions_rejected": invalid_rejected,
            "throughput_uses_elapsed_wall_time": timing["qps"] == 60,
        },
        "metrics": {"fixture_ap_at_5": scores["ap_at_k"],
                    "fixture_recall_at_5": scores["recall_at_k"],
                    "fixture_maxsim_gap": match - distractor},
    }
