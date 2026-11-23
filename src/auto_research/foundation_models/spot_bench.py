"""SPOT-Bench fixed-v2 Algorithm 1/Eq2 scorer on explicit response traces.

No model, video reader, GPT judge, KV cache or Ctrl-SPOT controller is supplied.
Semantic matches belong to an evaluator, never to an evaluated policy. As in
Alg1 and pinned upstream, one response may fill multiple eligible open slots;
the prose's closest-single-slot description is not silently substituted.
"""

from __future__ import annotations

import math
import random

REQUIRES_GPU_VALIDATION = False


def timeliness(time, start, end, *, sigma_early, sigma_late):
    values = (time, start, end, sigma_early, sigma_late)
    if any(not math.isfinite(x) for x in values) or start > end or min(sigma_early, sigma_late) <= 0:
        raise ValueError("finite ordered interval and positive sigmas required")
    distance, sigma = (start-time, sigma_early) if time < start else (time-end, sigma_late)
    if start <= time <= end:
        return 1.0
    scaled = distance/sigma
    return math.exp(-.5*scaled*scaled)


def score(prediction_times, slot_intervals, semantics, *, occupancy=5, threshold=0.0,
          sigma_early=1.48, sigma_late=.74, device="cpu"):
    """Offline evaluator, semantics[slot][prediction]; no hidden label oracle.

    The threshold is explicit (pinned upstream exposes it); zero follows Alg1's
    positive-score rule. TP counts occupied slots, not every absorbed response.
    """
    if device != "cpu":
        raise ValueError("CPU evaluator only")
    if type(occupancy) is not int or occupancy < 1 or not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("positive integer occupancy and threshold in [0,1] required")
    timeliness(0, 0, 0, sigma_early=sigma_early, sigma_late=sigma_late)
    n, m = len(prediction_times), len(slot_intervals)
    if len(semantics) != m or any(len(row) != n or any(type(x) is not bool for x in row) for row in semantics):
        raise ValueError("explicit boolean slot-by-prediction semantic matrix required")
    for start, end in slot_intervals:
        timeliness(start, start, end, sigma_early=sigma_early, sigma_late=sigma_late)
    if any(not math.isfinite(t) for t in prediction_times):
        raise ValueError("finite prediction times required")
    count, best, matched = [0]*m, [0.0]*m, [False]*n
    for i in sorted(range(n), key=lambda i: (prediction_times[i], i)):
        for j in sorted(range(m), key=lambda j: (slot_intervals[j][0], j)):
            if count[j] == occupancy:
                continue
            t = timeliness(prediction_times[i], *slot_intervals[j], sigma_early=sigma_early, sigma_late=sigma_late)
            if t > 0 and t >= threshold and semantics[j][i]:
                count[j] += 1
                best[j] = max(best[j], t)
                matched[i] = True
    tp, fp, fn = sum(c > 0 for c in count), sum(not x for x in matched), sum(c == 0 for c in count)
    xtp = math.fsum(best)
    precision = xtp/(tp+fp) if tp+fp else 0.0
    recall = xtp/(tp+fn) if tp+fn else 0.0
    f1 = 2*precision*recall/(precision+recall) if precision+recall else 0.0
    return {"weighted_tp": xtp, "tp_slots": tp, "fp_predictions": fp, "fn_slots": fn,
            "precision": precision, "recall": recall, "timeliness_f1": f1,
            "slot_counts": count, "slot_best": best, "pred_matched": matched}


def diagnostic(seed=42, device="cpu"):
    if device != "cpu":
        raise ValueError("CPU evaluator only")
    rng = random.Random(seed)
    center = rng.uniform(10, 20)
    slots = [(center-1, center+1)]
    perfect = score([center], slots, [[True]])
    spam = score([center]*7, slots, [[True]*7], occupancy=5)
    wrong = score([center], slots, [[False]])
    early = timeliness(center-2, *slots[0], sigma_early=1.48, sigma_late=.74)
    late = timeliness(center+2, *slots[0], sigma_early=1.48, sigma_late=.74)
    overlap = score([center], slots*2, [[True], [True]])
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"perfect_trace_scores_one": perfect["timeliness_f1"] == 1,
                       "occupancy_excess_is_false_positive": spam["fp_predictions"] == 2,
                       "spam_penalty_is_not_capability": spam["timeliness_f1"] < 1,
                       "wrong_semantics_never_matches": wrong["tp_slots"] == 0,
                       "late_is_penalized_more_than_early": early > late,
                       "literal_algorithm1_can_fill_two_slots": overlap["tp_slots"] == 2,
                       "no_predictions_leaves_false_negative": score([], slots, [[]])["fn_slots"] == 1},
            "metrics": {"synthetic_perfect_trace_f1": perfect["timeliness_f1"],
                        "synthetic_spam_trace_f1": spam["timeliness_f1"],
                        "early_fractional_credit": early, "late_fractional_credit": late}}
