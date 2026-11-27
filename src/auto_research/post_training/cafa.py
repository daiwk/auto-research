"""CAFA fixed-bank exact support planning (v1 Eqs.2--4, Algorithm2).

Exact identities are (prompt, decoded response), never normalized text or token
IDs. Rational coefficients cancel before scoring. No model sampler or judge is
bundled; the scorer callback receives only the prompt and response.
"""

from dataclasses import dataclass
from fractions import Fraction
import math

REQUIRES_GPU_VALIDATION = False


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("finite rational coefficients required")
    try:
        # Decimal spellings of finite float inputs define the exact rationals.
        result = value if isinstance(value, Fraction) else Fraction(str(value))
    except (ValueError, TypeError, ZeroDivisionError) as exc:
        raise ValueError("finite rational coefficients required") from exc
    return result


def _sum_vectors(left, right):
    return tuple(a+b for a, b in zip(left, right))


@dataclass(frozen=True)
class ReportPlan:
    dimension: int
    mode: str
    weights: dict
    draw_maps: dict
    aggregates: dict
    cache_support: frozenset
    mean_support: frozenset
    draw_support: frozenset

    @property
    def required(self):
        return self.mean_support if self.mode == "mean" else self.draw_support


def plan_report(banks, coefficients, *, mode="mean", weights=None):
    """Plan before reading scores; all-zero draws remain in original denominators.

    ``banks[prompt][draw][policy]`` contains exact decoded strings. Coefficients
    may be integers, Fraction values or decimal strings/finite float spellings.
    Float inputs are not aggregated using a numerical zero tolerance.
    """
    if mode not in {"mean", "mean+cov"} or not isinstance(banks, dict) or not banks:
        raise ValueError("nonempty prompt bank and explicit report mode required")
    try:
        matrix = [tuple(_fraction(v) for v in row) for row in coefficients]
    except TypeError as exc:
        raise ValueError("rectangular report matrix required") from exc
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("nonempty rectangular report matrix required")
    d, policies = len(matrix), len(matrix[0])
    columns = [tuple(matrix[k][j] for k in range(d)) for j in range(policies)]
    zero = (Fraction(0),)*d
    active = [j for j, column in enumerate(columns) if any(column)]
    if weights is None:
        weights = {prompt: Fraction(1, len(banks)) for prompt in banks}
    elif not isinstance(weights, dict) or set(weights) != set(banks):
        raise ValueError("weights must align with every distinct prompt")
    weights = {p: _fraction(w) for p, w in weights.items()}
    if any(w <= 0 for w in weights.values()) or sum(weights.values()) != 1:
        raise ValueError("positive rational prompt weights must sum exactly to one")
    maps, aggregates, cache_support, mean_support, draw_support = {}, {}, set(), set(), set()
    for prompt, draws in banks.items():
        if not isinstance(prompt, str) or not isinstance(draws, (list, tuple)) or not draws:
            raise ValueError("exact string prompt and nonempty draw sequence required")
        if mode == "mean+cov" and len(draws) < 2:
            raise ValueError("ordinary covariance requires at least two draws per prompt")
        per_draw, aggregate = [], {}
        for responses in draws:
            if (not isinstance(responses, (list, tuple)) or len(responses) != policies
                    or any(not isinstance(s, str) for s in responses)):
                raise ValueError("complete decoded response for each policy required")
            mapping = {}
            for j in active:
                identity = (prompt, responses[j])
                cache_support.add(identity)
                mapping[identity] = _sum_vectors(mapping.get(identity, zero), columns[j])
            mapping = {u: b for u, b in mapping.items() if any(b)}
            draw_support.update(mapping)
            for u, b in mapping.items():
                aggregate[u] = _sum_vectors(aggregate.get(u, zero), b)
            per_draw.append(mapping)
        aggregate = {u: a for u, a in aggregate.items() if any(a)}
        mean_support.update(aggregate)
        maps[prompt], aggregates[prompt] = tuple(per_draw), aggregate
    return ReportPlan(d, mode, weights, maps, aggregates, frozenset(cache_support),
                      frozenset(mean_support), frozenset(draw_support))


def recover(plan, cache, *, scorer_version, scorer=None, score_range=None):
    """Acquire only required unknown scores and recover means/covariance.

    Cache keys are (version,prompt,response). A failed/unavailable score stays
    missing, never zero. With an explicit range, missing feedback yields mean
    bounds and NO covariance. ``new_score_calls`` counts callback invocations,
    not a monetary bill or an assurance that a failed call is free.
    """
    if not isinstance(plan, ReportPlan) or not isinstance(cache, dict) or not isinstance(scorer_version, str) or not scorer_version:
        raise ValueError("report plan, mutable versioned cache and version required")
    if score_range is not None:
        if (len(score_range) != 2 or not all(math.isfinite(x) for x in score_range)
                or score_range[0] > score_range[1]):
            raise ValueError("finite ordered score range required")
    scores, missing, calls = {}, [], 0
    for u in sorted(plan.required):
        key = (scorer_version, *u)
        value = cache.get(key)
        if key not in cache and scorer is not None:
            calls += 1
            try:
                value = scorer(*u)
            except Exception:
                value = None
            if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value):
                cache[key] = float(value)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
            missing.append(u)
        elif score_range is not None and not score_range[0] <= value <= score_range[1]:
            raise ValueError("observed score is outside declared range")
        else:
            scores[u] = float(value)
    counts = {"required_inputs": len(plan.required), "cache_only_inputs": len(plan.cache_support),
              "mean_inputs": len(plan.mean_support), "mean_cov_inputs": len(plan.draw_support),
              "new_score_calls": calls}
    if missing:
        result = {"status": "incomplete", "missing": missing, "mean": None, "covariance": None, **counts}
        if score_range is not None:
            lower, upper = [], []
            for k in range(plan.dimension):
                lo, hi = [], []
                for prompt, aggregate in plan.aggregates.items():
                    factor = plan.weights[prompt]/len(plan.draw_maps[prompt])
                    for u, a in aggregate.items():
                        coefficient = float(factor*a[k])
                        if u in scores:
                            lo.append(coefficient*scores[u]); hi.append(coefficient*scores[u])
                        else:
                            ends = [coefficient*x for x in score_range]
                            lo.append(min(ends)); hi.append(max(ends))
                lower.append(math.fsum(lo)); upper.append(math.fsum(hi))
            result.update(status="bounded", mean_bounds=(lower, upper))
        return result
    prompt_means = {}
    for prompt, aggregate in plan.aggregates.items():
        n = len(plan.draw_maps[prompt])
        prompt_means[prompt] = [math.fsum(float(a[k])*scores[u] for u, a in aggregate.items())/n
                                for k in range(plan.dimension)]
    mean = [math.fsum(float(plan.weights[p])*m[k] for p, m in prompt_means.items())
            for k in range(plan.dimension)]
    covariance, per_prompt_covariance = None, None
    if plan.mode == "mean+cov":
        per_prompt_covariance = {}
        for prompt, draws in plan.draw_maps.items():
            vectors = [[math.fsum(float(b[k])*scores[u] for u, b in draw.items())
                        for k in range(plan.dimension)] for draw in draws]
            center, n = prompt_means[prompt], len(draws)
            per_prompt_covariance[prompt] = [[math.fsum((z[a]-center[a])*(z[b]-center[b]) for z in vectors)/(n-1)
                                             for b in range(plan.dimension)] for a in range(plan.dimension)]
        covariance = [[math.fsum(float(plan.weights[p])**2*per_prompt_covariance[p][a][b]/len(plan.draw_maps[p])
                                for p in plan.draw_maps) for b in range(plan.dimension)] for a in range(plan.dimension)]
    return {"status": "complete", "mean": mean, "covariance": covariance,
            "per_prompt_covariance": per_prompt_covariance, **counts}


def diagnostic(seed=42, device="cpu"):
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    import random
    rng = random.Random(seed)
    bank = {"exact prompt": [("A", "A"), ("B", "C"), ("D", "B")]}
    values = {text: rng.uniform(-2, 3) for text in "ABCD"}
    mean_plan, cov_plan = (plan_report(bank, [[-1, 1]], mode=m) for m in ("mean", "mean+cov"))
    cache = {}
    mean = recover(mean_plan, cache, scorer_version="v1", scorer=lambda p, y: values[y])
    covariance = recover(cov_plan, cache, scorer_version="v1", scorer=lambda p, y: values[y])
    full = [values[b]-values[a] for a, b in bank["exact prompt"]]
    expected_mean = math.fsum(full)/3
    expected_variance = math.fsum((x-expected_mean)**2 for x in full)/2
    mirror = {"x": [("A", "B"), ("B", "A")]}
    zero = plan_report(mirror, [[-1, 1]])
    anchored = plan_report(bank, [[-1, 1], [1, 0]])
    failed = recover(cov_plan, {}, scorer_version="v1", score_range=(-2, 3))
    checks = {"mean_matches_full_scoring": abs(mean["mean"][0]-expected_mean) < 1e-12,
              "ordinary_covariance_matches_full": abs(covariance["per_prompt_covariance"]["exact prompt"][0][0]-expected_variance) < 1e-12,
              "mean_and_covariance_support_differ": len(mean_plan.required) == 2 and len(cov_plan.required) == 3,
              "mirror_mean_needs_no_scores": len(zero.required) == 0,
              "absolute_anchor_restores_cache_support": anchored.required == anchored.cache_support,
              "covariance_acquires_only_one_extra_score": covariance["new_score_calls"] == 1,
              "missing_feedback_is_bounded_not_zero": failed["status"] == "bounded" and failed["covariance"] is None}
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "training_executed": False, "checks": checks, "metrics": {"mean_max_abs_error": abs(mean["mean"][0]-expected_mean),
            "covariance_max_abs_error": abs(covariance["per_prompt_covariance"]["exact prompt"][0][0]-expected_variance),
            "cache_only_inputs": 4, "mean_inputs": 2, "mean_cov_inputs": 3}}
