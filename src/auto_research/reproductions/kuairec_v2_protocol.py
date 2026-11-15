"""KuaiRecV2 v1 reporting/split protocol only; no benchmark ingestion or model.

Official linked repository returned 404 during review. Deliberately omit
underspecified Appendix-D diversity formulas rather than invent a convention.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Interaction:
    user: str
    day: int
    timestamp: int
    item: str


def daily_leave_one_out(interactions):
    """Last interaction per (day,user) is validation; never call it a test split.

    Exact timestamp ties are rejected: paper has no tie rule. Earlier-day
    validation labels are not silently added to training/history by this API.
    """
    groups = defaultdict(list)
    for row in interactions:
        groups[(row.day, row.user)].append(row)
    train, validation = [], []
    for key in sorted(groups):
        rows = sorted(groups[key], key=lambda row: row.timestamp)
        if len({row.timestamp for row in rows}) != len(rows):
            raise ValueError("ambiguous user/day timestamp tie")
        train.extend(rows[:-1])
        validation.append(rows[-1])
    return train, validation


def full_month_score(daily_scores, daily_counts):
    if not daily_scores or set(daily_scores) != set(daily_counts):
        raise ValueError("matching nonempty daily keys required")
    if any(not isinstance(n, int) or isinstance(n, bool) or n <= 0 for n in daily_counts.values()):
        raise ValueError("positive validation instance counts required")
    if any(not math.isfinite(value) for value in daily_scores.values()):
        raise ValueError("finite daily scores required")
    return sum(daily_counts[d] * daily_scores[d] for d in daily_scores) / sum(daily_counts.values())


def single_retrieval_evaluate_all(recommendations, evaluator_labels, k):
    """One output per request reused for behavior subsets; evaluator-only gold.

    The retrieval producer is absent. Multiple task-specific output lists are
    rejected structurally. This is a finite metric adapter, not a benchmark run.
    """
    if k <= 0 or set(recommendations) != set(evaluator_labels):
        raise ValueError("matching request identities and positive k required")
    totals = defaultdict(lambda: [0.0, 0.0, 0])
    for request, labels in evaluator_labels.items():
        output = recommendations[request]
        if not isinstance(output, (list, tuple)) or any(not isinstance(item, str) for item in output):
            raise ValueError("one flat item list per request, not one list per behavior")
        if len(set(output)) != len(output):
            raise ValueError("duplicate recommendations")
        target, behaviors = labels
        rank = output[:k].index(target) + 1 if target in output[:k] else None
        for behavior in set(behaviors):
            totals[behavior][0] += float(rank is not None)
            totals[behavior][1] += 1 / math.log2(rank + 1) if rank else 0
            totals[behavior][2] += 1
    return {behavior: {"hit_rate": hit / n, "ndcg": ndcg / n, "instances": n}
            for behavior, (hit, ndcg, n) in totals.items()}


def diagnostic(seed=42, device="cpu"):
    if device != "cpu":
        raise ValueError("CPU protocol only")
    rows = [Interaction("u", 1, 1, "a"), Interaction("u", 1, 2, "b"),
            Interaction("u", 2, 3, "c"), Interaction("u", 2, 4, "d")]
    train, validation = daily_leave_one_out(rows)
    metrics = single_retrieval_evaluate_all({"x": ["a", "b"], "y": ["b", "a"]},
                                          {"x": ("b", ["click", "like"]), "y": ("c", ["click"])}, 2)
    weighted = full_month_score({1: 1.0, 2: 0.0}, {1: 1, 2: 3})
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "checks": {"daily_not_global_split": [r.item for r in validation] == ["b", "d"],
                       "held_out_not_train": [r.item for r in train] == ["a", "c"],
                       "instance_weighted_not_macro": weighted == 0.25,
                       "shared_output_subsets": metrics["click"]["hit_rate"] == 0.5 and metrics["like"]["hit_rate"] == 1,
                       "rank_discount": math.isclose(metrics["like"]["ndcg"], 1 / math.log2(3))},
            "metrics": {"finite_example_weighted_score": weighted, "daily_validation_instances": len(validation)}}
