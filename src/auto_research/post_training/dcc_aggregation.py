"""Exact one-dimensional two-medians DCC reward aggregation (v1 Eq.8-11)."""

import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(x):
    if type(x) not in {int, float} or not math.isfinite(x):
        raise ValueError("finite non-Boolean score required")
    return float(x)


def centers(values):
    a = sorted(_real(v) for v in values)
    if not a:
        raise ValueError("nonempty scores required")
    n = len(a)
    prefix = [0.]
    for x in a:
        prefix.append(prefix[-1]+x)

    def interval(left, right):
        count = right-left
        mid = (left+right)//2
        median = a[mid] if count % 2 else (a[mid-1]+a[mid])/2
        split = (left+right)//2
        cost = median*(split-left)-(prefix[split]-prefix[left])
        cost += (prefix[right]-prefix[split])-median*(right-split)
        return median, cost

    best = None
    for s in range(1, n):
        if a[s] == a[s-1]:
            continue
        lo, lc = interval(0, s)
        hi, hc = interval(s, n)
        candidate = (lc+hc, s, lo, hi)
        if best is None or candidate[:2] < best[:2]:
            best = candidate
    return (a[0], a[0]) if best is None else (best[2], best[3])


def aggregate(scores, weights=None):
    if not isinstance(scores, (list, tuple)) or not scores:
        raise ValueError("nonempty rectangular candidate-by-criterion scores required")
    if any(not isinstance(r, (list, tuple)) or not r for r in scores):
        raise ValueError("nonempty score rows required")
    width = len(scores[0])
    if any(len(r) != width for r in scores):
        raise ValueError("ragged score matrix")
    rows = [[_real(x) for x in r] for r in scores]
    w = [1.]*width if weights is None else [_real(x) for x in weights]
    if len(w) != width or sum(w) == 0:
        raise ValueError("criterion weights need matching width and nonzero sum")
    lo, hi = centers([x for r in rows for x in r])
    clipped = [[min(hi, max(lo, x)) for x in r] for r in rows]
    return {"centers": (lo, hi), "clipped_scores": clipped,
            "rewards": [sum(x*y for x, y in zip(r, w, strict=True))/sum(w) for r in clipped]}


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required; this is a scalar reward operator")
    rng = random.Random(seed)
    rows = [[-2., -1., 1.], [2., 3., 8.], [-1.+rng.random()/10, 1., 2.]]
    out = aggregate(rows)
    weighted = aggregate(rows, [1, 2, 3])
    lo, hi = out["centers"]
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {
                "two_cluster_median_clips_moderate_outlier": hi == 2.,
                "isolated_extreme_can_form_own_cluster": centers([0., 1., 100.])[1] == 100.,
                "one_shared_interval": all(lo <= x <= hi for r in out["clipped_scores"] for x in r),
                "weights_do_not_change_centers": weighted["centers"] == out["centers"],
                "constant_group_is_constant": aggregate([[7., 7.], [7., 7.]])["rewards"] == [7., 7.],
                "smallest_split_breaks_tie": centers([0., 1., 2.]) == (0., 1.5),
            }, "metrics": {"lower_center": lo, "upper_center": hi,
                           "raw_outlier": 8., "clipped_outlier": out["clipped_scores"][1][2]}}
