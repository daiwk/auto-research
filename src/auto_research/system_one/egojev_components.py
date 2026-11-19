"""CPU EgoJev probability/window/quantile postprocessing (fixed v1 Eq3–4).

Inputs are explicitly supplied VLM readout probabilities, never gold evidence.
No VLM, label-token scoring, video loading or answer generation is implemented.
"""

import math
import random

REQUIRES_GPU_VALIDATION = False


def _count(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(name + " must be a positive integer")


def _distribution(values):
    if (
        not isinstance(values, (list, tuple))
        or not values
        or any(type(x) not in (float, int) or not math.isfinite(x) or x < 0 for x in values)
    ):
        raise ValueError("finite nonnegative probability vector required")
    total = math.fsum(values)
    if not math.isfinite(total) or total <= 0:
        raise ValueError("positive finite total probability required")
    return tuple(float(x) / total for x in values)


def window_probabilities(coarse, windows):
    p = _distribution(coarse)
    _count(windows, "windows")
    if len(p) % windows:
        raise ValueError("equal aligned windows must divide coarse segment count")
    size = len(p) // windows
    return tuple(math.fsum(p[w * size : (w + 1) * size]) for w in range(windows))


def refinement_windows(coarse, windows, count):
    mass = window_probabilities(coarse, windows)
    if type(count) is not int or not 0 <= count <= windows:
        raise ValueError("integer refinement budget in [0,windows] required")
    return tuple(sorted(range(windows), key=lambda w: (-mass[w], w))[:count])


def fuse_readouts(coarse, windows, refined):
    """Eq3; each refined window supplies N local masses, N=len(coarse).

    For k=0 return the original N-segment distribution (paper single level).
    Otherwise return W*N fine-segment probabilities in chronological order.
    """
    p = _distribution(coarse)
    mass = window_probabilities(p, windows)
    if (
        not isinstance(refined, dict)
        or any(type(w) is not int or not 0 <= w < windows for w in refined)
        or set(refined) != set(refinement_windows(p, windows, len(refined)))
    ):
        raise ValueError("refined keys must be the budget-selected top coarse-mass windows")
    if not refined:
        return p
    n = len(p)
    log_fine = []
    for w in range(windows):
        local = _distribution(refined[w]) if w in refined else (1 / n,) * n
        if len(local) != n:
            raise ValueError("each local fine readout must have N probabilities")
        log_fine.extend(
            math.log(mass[w]) + math.log(x) if mass[w] > 0 and x > 0 else -math.inf for x in local
        )
    # Fine segment s spans [s/(WN),(s+1)/(WN)], inside coarse floor(s/W).
    geometric_logs = tuple(
        0.5 * (math.log(p[s // windows]) + log_probability)
        if p[s // windows] > 0 and math.isfinite(log_probability)
        else -math.inf
        for s, log_probability in enumerate(log_fine)
    )
    largest = max(geometric_logs)
    if not math.isfinite(largest):
        raise ValueError("coarse and fine distributions have disjoint support")
    return _distribution(tuple(math.exp(x - largest) for x in geometric_logs))


def quantile_times(probabilities, duration, budget):
    """Eq4 inverse CDF for equal-duration, piecewise-uniform segments."""
    p = _distribution(probabilities)
    _count(budget, "budget")
    if type(duration) not in (float, int) or not math.isfinite(duration) or duration <= 0:
        raise ValueError("positive finite duration required")
    output = []
    for b in range(budget):
        target = (b + 0.5) / budget
        before = 0.0
        for index, probability in enumerate(p):
            after = before + probability
            if probability > 0 and target <= after:
                fraction = min(1.0, max(0.0, (target - before) / probability))
                output.append((index + fraction) * duration / len(p))
                break
            before = after
        else:
            raise ValueError("CDF failed to cover an interior quantile")
    return tuple(output)


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU required")
    rng = random.Random(seed)
    coarse = (0.1, 0.1, 0.3, 0.5)
    local = (0.1 + rng.random() / 100, 0.2, 0.3, 0.4)
    fused = fuse_readouts(coarse, 2, {1: local})
    times = quantile_times(fused, 80.0, 8)
    direct = quantile_times((0.0, 1.0), 10.0, 2)
    # A bin-center lookup would return(7.5,7.5), losing within-segment quantiles.
    fine = [0.2 / 4] * 4 + [0.8 * x / math.fsum(local) for x in local]
    product = _distribution([coarse[s // 2] * f for s, f in enumerate(fine)])
    difference = max(abs(a - b) for a, b in zip(fused, product, strict=True))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "top_window_by_mass": refinement_windows(coarse, 2, 1) == (1,),
            "single_level_unchanged": fuse_readouts(coarse, 2, {}) == coarse,
            "normalized_fine_geometry": abs(math.fsum(fused) - 1) < 1e-12 and len(fused) == 8,
            "inverse_cdf_not_bin_center": direct == (6.25, 8.75),
            "flat_readout_is_uniform_midpoints": quantile_times([1.0] * 4, 8.0, 4)
            == (1.0, 3.0, 5.0, 7.0),
            "geometric_not_product": difference > 1e-3,
            "chronological_quantiles": all(a <= b for a, b in zip(times, times[1:])),
        },
        "metrics": {
            "fine_segments": len(fused),
            "quantile_budget": len(times),
            "geometric_product_max_difference": difference,
            "first_quantile_seconds": times[0],
            "last_quantile_seconds": times[-1],
        },
    }
