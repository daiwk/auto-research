"""MMEB-V3 ranking and OmniSET evaluator arithmetic, not an embedding model.

Input rankings/embeddings and official release materialization remain external.
Relevance and semantic tuple IDs are evaluator-only. OmniSET is diagnostic and
is never added to the leaderboard categories by this module.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import math
from numbers import Real
import random

REQUIRES_GPU_VALIDATION = False
MODALITIES = frozenset("TIVA")
HIT_CATEGORIES = frozenset(("audio", "image", "video", "agent"))
NDCG_CATEGORIES = frozenset(("text", "visdoc"))


def _ids(values, label):
    if (not isinstance(values, Sequence) or isinstance(values, (str, bytes))
            or any(not isinstance(value, str) or not value.strip() for value in values)
            or len(set(values)) != len(values)):
        raise ValueError(f"explicit unique {label} IDs required")
    return tuple(values)


def _relevance(values):
    if not isinstance(values, Mapping) or any(
            not isinstance(key, str) or not key.strip() or isinstance(value, bool)
            or not isinstance(value, Real) or not math.isfinite(value) or value < 0
            for key, value in values.items()):
        raise ValueError("finite nonnegative evaluator relevance map required")
    return dict(values)


def hit_at_one(ranking: Sequence[str], relevance: Mapping[str, float]) -> float:
    ordered, rel = _ids(ranking, "ranking"), _relevance(relevance)
    return float(bool(ordered) and rel.get(ordered[0], 0) > 0)


def ndcg_at_five(ranking: Sequence[str], relevance: Mapping[str, float], *, gain: str) -> float:
    """The official fixed upstream emits both linear and exponential NDCG.

    Require an explicit form rather than silently choosing one for the paper's
    unqualified NDCG column. Binary relevance makes the two forms identical.
    """
    ordered, rel = _ids(ranking, "ranking"), _relevance(relevance)
    if gain not in ("linear", "exponential"):
        raise ValueError("explicit linear/exponential NDCG gain required")

    def transform(value):
        return value if gain == "linear" else 2.0 ** value - 1

    def dcg(values):
        try:
            result = math.fsum(transform(value) / math.log2(index + 2) for index, value in enumerate(values))
        except OverflowError as exc:
            raise ValueError("relevance gain overflow") from exc
        if not math.isfinite(result):
            raise ValueError("finite DCG required")
        return result

    ideal = dcg(sorted(rel.values(), reverse=True)[:5])
    return dcg([rel.get(identity, 0) for identity in ordered[:5]]) / ideal if ideal > 0 else 0.0


@dataclass(frozen=True)
class RankingCase:
    identity: str
    ranked_ids: tuple[str, ...]
    candidate_ids: tuple[str, ...]
    relevance: Mapping[str, float]

    def __post_init__(self):
        if not isinstance(self.identity, str) or not self.identity.strip():
            raise ValueError("query identity required")
        ranking, pool, rel = _ids(self.ranked_ids, "ranking"), _ids(self.candidate_ids, "candidate"), _relevance(self.relevance)
        if not pool or not set(ranking) <= set(pool) or not set(rel) <= set(pool):
            raise ValueError("ranking and evaluator relevance must belong to the declared candidate pool")


def score_task(cases: Sequence[RankingCase], *, category: str, ndcg_gain: str | None = None) -> float:
    if (not isinstance(cases, Sequence) or not cases or not all(isinstance(case, RankingCase) for case in cases)
            or len({case.identity for case in cases}) != len(cases)):
        raise ValueError("nonempty unique typed query cases required")
    if category in HIT_CATEGORIES:
        values = [hit_at_one(case.ranked_ids, case.relevance) for case in cases]
    elif category in NDCG_CATEGORIES:
        values = [ndcg_at_five(case.ranked_ids, case.relevance, gain=ndcg_gain) for case in cases]
    else:
        raise ValueError("one of six leaderboard categories required; OmniSET is separate")
    return math.fsum(values) / len(values)


def task_macro_average(scores: Mapping[str, float], *, expected_tasks: Sequence[str]) -> float:
    """Equal task weights, not query-count weights. Exact caller manifest needed."""
    expected = _ids(expected_tasks, "expected task")
    if not expected or not isinstance(scores, Mapping) or set(scores) != set(expected):
        raise ValueError("exact declared task coverage required; partial suites are not complete scores")
    if any(isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value)
           or not 0 <= value <= 1 for value in scores.values()):
        raise ValueError("finite task scores in [0,1] required")
    return math.fsum(scores.values()) / len(expected)


@dataclass(frozen=True)
class OmniCandidate:
    identity: str
    semantic_id: str
    modality: str

    def __post_init__(self):
        if (any(not isinstance(value, str) or not value.strip() for value in (self.identity, self.semantic_id))
                or self.modality not in MODALITIES):
            raise ValueError("candidate identity, evaluator semantic tuple ID and T/I/V/A modality required")


def omni_target_ids(query: OmniCandidate, candidates: Sequence[OmniCandidate], *, target_modality: str) -> frozenset[str]:
    """Preserve the mixed pool and self distractor; never prefilter by target."""
    if (not isinstance(query, OmniCandidate) or target_modality not in MODALITIES
            or target_modality == query.modality or not isinstance(candidates, Sequence)
            or not all(isinstance(item, OmniCandidate) for item in candidates)
            or len({item.identity for item in candidates}) != len(candidates)):
        raise ValueError("cross-modality query and unique mixed candidate pool required")
    pool = {item.identity: item for item in candidates}
    if pool.get(query.identity) != query:
        raise ValueError("the query input must remain in the shared pool as a distractor")
    semantic_modalities: dict[str, set[str]] = {}
    for item in candidates:
        semantic_modalities.setdefault(item.semantic_id, set()).add(item.modality)
    if any(modalities != MODALITIES for modalities in semantic_modalities.values()):
        raise ValueError("full OmniSET contract requires every semantic tuple in all four modalities")
    matches = frozenset(item.identity for item in candidates
                        if item.modality == target_modality and item.semantic_id == query.semantic_id)
    if not matches:
        raise ValueError("declared target modality has no semantically matching candidate")
    return matches


def score_omniset(query: OmniCandidate, candidates: Sequence[OmniCandidate], ranking: Sequence[str], *,
                  target_modality: str) -> dict:
    truth = omni_target_ids(query, candidates, target_modality=target_modality)
    ordered = _ids(ranking, "ranking")
    pool = {item.identity: item for item in candidates}
    if not set(ordered) <= set(pool):
        raise ValueError("unknown candidate in ranking")
    top = pool[ordered[0]] if ordered else None
    return {"semantic_and_modality_hit_at_one": float(bool(ordered) and ordered[0] in truth),
            "requested_modality_at_one": float(top is not None and top.modality == target_modality),
            "semantic_match_at_one": float(top is not None and top.semantic_id == query.semantic_id),
            "diagnostic_only": True, "included_in_leaderboard": False}


def score_all_directions(queries: Sequence[OmniCandidate], candidates: Sequence[OmniCandidate],
                         rankings: Mapping[tuple[str, str], Sequence[str]]) -> dict:
    """Twelve directions use one identical full candidate pool, never twelve filters."""
    if (not isinstance(queries, Sequence) or len(queries) != 4
            or not all(isinstance(item, OmniCandidate) for item in queries)
            or {item.modality for item in queries} != MODALITIES
            or len({item.semantic_id for item in queries}) != 1):
        raise ValueError("one complete semantically equivalent query tuple required")
    directions = {(source, target) for source in MODALITIES for target in MODALITIES if source != target}
    if not isinstance(rankings, Mapping) or set(rankings) != directions:
        raise ValueError("all twelve directed rankings required")
    by_modality = {item.modality: item for item in queries}
    results = {f"{source}->{target}": score_omniset(by_modality[source], candidates, rankings[source, target],
                                                  target_modality=target)
               for source, target in sorted(directions)}
    return {"directions": results, "shared_candidate_count": len(candidates),
            "diagnostic_only": True, "included_in_leaderboard": False}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only evaluator required; no CUDA embedding model")
    rel = {"good": 3, "partial": 1}
    case = RankingCase("q", ("partial", "good", "none"), ("none", "partial", "good"), rel)
    linear = score_task([case], category="text", ndcg_gain="linear")
    exponential = score_task([case], category="text", ndcg_gain="exponential")
    pool = [OmniCandidate(f"s-{modality}", "s", modality) for modality in sorted(MODALITIES)]
    pool += [OmniCandidate(f"negative-{modality}", "other", modality) for modality in sorted(MODALITIES)]
    random.Random(seed).shuffle(pool)
    query = next(item for item in pool if item.identity == "s-I")
    wrong_modality = score_omniset(query, pool, ["s-I", "s-A"], target_modality="A")
    right = score_omniset(query, pool, ["s-A", "s-I"], target_modality="A")
    directions = [(a, b) for a in MODALITIES for b in MODALITIES if a != b]
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "metrics": {"fixture_linear_ndcg_at_five": linear, "fixture_exponential_ndcg_at_five": exponential,
                        "directed_cross_modal_pairs": len(directions), "shared_fixture_pool_size": len(pool)},
            "checks": {"gain_variants_not_silently_mixed": 0 < exponential < linear < 1,
                       "hit_categories_use_top_one": score_task([case], category="agent") == 1,
                       "task_mean_not_query_weighted": task_macro_average({"large": 1., "small": 0.}, expected_tasks=["large", "small"]) == .5,
                       "same_instance_is_not_a_correct_target": wrong_modality["semantic_match_at_one"] == 1
                       and wrong_modality["semantic_and_modality_hit_at_one"] == 0,
                       "target_semantics_and_modality_both_required": right["semantic_and_modality_hit_at_one"] == 1,
                       "omniset_not_a_leaderboard_task": right["included_in_leaderboard"] is False,
                       "all_twelve_directed_pairs": len(directions) == 12}}
