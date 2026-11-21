"""DFRL v1 cost advantages and batch-level reward correction, CPU only.

Costs and score gradients are explicit inputs, not an LLM or a learned reward
model. Exact costs are obtained lazily, once for the whole selected batch.
"""

from dataclasses import dataclass
import itertools
import math
import random

REQUIRES_GPU_VALIDATION = False


def _real(value, name):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f"{name}: finite real number required")
    return float(value)


def _matrix(values, name):
    if not isinstance(values, (tuple, list)) or not values:
        raise ValueError(f"{name}: nonempty rectangular cost batch required")
    rows = []
    width = None
    for row in values:
        if not isinstance(row, (tuple, list)) or len(row) < 2:
            raise ValueError(f"{name}: at least two independent predictions per instance required")
        width = len(row) if width is None else width
        if len(row) != width:
            raise ValueError(f"{name}: rectangular cost batch required")
        rows.append(tuple(_real(value, name) for value in row))
    return tuple(rows)


def cost_advantages(realized_costs):
    """Eq.7: negative cost minus its within-instance leave-one-out baseline.

The optimal hindsight cost is shared and cancels. Never normalize advantages
by their standard deviation: that would change the analyzed estimator.
"""
    rows = _matrix(realized_costs, "realized_costs")
    result = []
    try:
        for row in rows:
            advantages = tuple(-cost + math.fsum(row[:i] + row[i+1:]) / (len(row)-1)
                               for i, cost in enumerate(row))
            if not all(math.isfinite(value) for value in advantages):
                raise ValueError("cost advantage overflow")
            result.append(advantages)
    except OverflowError as error:
        raise ValueError("cost advantage overflow") from error
    return tuple(result)


@dataclass(frozen=True)
class CorrectedBatch:
    advantages: tuple[tuple[float, ...], ...]
    exact_evaluated: bool
    probability: float
    draw: float


def corrected_advantages(cheap_costs, exact_costs, probability, *, rng):
    """Eq.12: ONE Bernoulli draw selects every exact solve in a batch.

``exact_costs`` is a zero-argument callback returning all M-by-K exact costs.
It is not called at all when I=0. The cheap estimate may be biased. Bounds on
variance and independence from the correction draw remain caller assumptions.
"""
    p = _real(probability, "probability")
    if not 0 < p <= 1 or not isinstance(rng, random.Random) or not callable(exact_costs):
        raise ValueError("probability in (0,1], Random instance and lazy exact callback required")
    cheap = cost_advantages(cheap_costs)
    draw = _real(rng.random(), "random draw")
    if not 0 <= draw < 1:
        raise ValueError("random draw must be in [0,1)")
    if draw >= p:
        return CorrectedBatch(cheap, False, p, draw)
    exact = cost_advantages(exact_costs())
    if len(exact) != len(cheap) or any(len(a) != len(b) for a, b in zip(exact, cheap, strict=True)):
        raise ValueError("exact and cheap costs must have the same batch shape")
    corrected = tuple(tuple(b + (a-b)/p for a, b in zip(erow, crow, strict=True))
                      for erow, crow in zip(exact, cheap, strict=True))
    if not all(math.isfinite(value) for row in corrected for value in row):
        raise ValueError("corrected advantage overflow")
    return CorrectedBatch(corrected, True, p, draw)


def warm_start_advantages(cheap_costs, exact_costs, *, step, warm_start_steps):
    """Heuristic phase, then exact phase at a caller/validation-fixed boundary."""
    if (type(step) is not int or step < 0 or type(warm_start_steps) is not int
            or warm_start_steps < 0 or not callable(exact_costs)):
        raise ValueError("nonnegative integer steps and lazy exact callback required")
    if step < warm_start_steps:
        return cost_advantages(cheap_costs), "heuristic"
    return cost_advantages(exact_costs()), "exact"


def enumerate_knapsack(profits, weights, capacity):
    """Tiny exact oracle for diagnostics, not a scalable production optimizer.

Returns a feasible binary decision maximizing predicted profit. A fixed
lexicographic decision order resolves ties, independently of observed profits.
"""
    if (not isinstance(profits, (tuple, list)) or not isinstance(weights, (tuple, list))
            or not 1 <= len(profits) <= 16 or len(profits) != len(weights)):
        raise ValueError("one to sixteen matched profit/weight entries required")
    p = tuple(_real(x, "profit") for x in profits)
    w = tuple(_real(x, "weight") for x in weights)
    cap = _real(capacity, "capacity")
    if any(x <= 0 for x in w) or cap < 0:
        raise ValueError("positive weights and nonnegative capacity required")
    best, best_value = None, -math.inf
    try:
        for decision in itertools.product((0, 1), repeat=len(p)):
            if math.fsum(x*y for x, y in zip(w, decision, strict=True)) > cap:
                continue
            value = math.fsum(x*y for x, y in zip(p, decision, strict=True))
            if not math.isfinite(value):
                raise ValueError("knapsack objective overflow")
            if value > best_value:
                best, best_value = decision, value
    except OverflowError as error:
        raise ValueError("knapsack arithmetic overflow") from error
    return best


def _score_gradient(probabilities, index):
    return tuple(float(j == index)-p for j, p in enumerate(probabilities))


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU device required")
    rng = random.Random(seed)
    raw = [rng.uniform(.3, 1.3) for _ in range(3)]
    probabilities = tuple(x/math.fsum(raw) for x in raw)
    predictions = ((8., 5., 3.), (1., 9., 2.), (2., 2., 10.))
    actual, weights, capacity = (4., 7., 5.), (2., 2., 1.), 3.
    decisions = [enumerate_knapsack(x, weights, capacity) for x in predictions]
    costs = tuple(-math.fsum(x*y for x, y in zip(actual, decision, strict=True))
                  for decision in decisions)
    expected_cost = math.fsum(p*c for p, c in zip(probabilities, costs, strict=True))
    analytic = tuple(-p*(c-expected_cost) for p, c in zip(probabilities, costs, strict=True))
    exact_gradient, cheap_gradient = [0.]*3, [0.]*3
    for i, j in itertools.product(range(3), repeat=2):
        mass = probabilities[i]*probabilities[j]
        advantages = cost_advantages(((costs[i], costs[j]),))[0]
        cheap = cost_advantages(((costs[i]+(1., -3., 2.)[i],
                                  costs[j]+(1., -3., 2.)[j]),))[0]
        for index, a, b in zip((i, j), advantages, cheap, strict=True):
            for d, score in enumerate(_score_gradient(probabilities, index)):
                exact_gradient[d] += mass*a*score/2
                cheap_gradient[d] += mass*b*score/2
    probability = .25
    corrected_gradient = [
        (1-probability)*b+probability*(b+(a-b)/probability)
        for a, b in zip(exact_gradient, cheap_gradient, strict=True)
    ]
    calls = []

    def exact():
        calls.append("whole-batch")
        return ((3., 8.), (9., 2.))

    class FixedRandom(random.Random):
        def __init__(self, value):
            super().__init__(0)
            self.value = value

        def random(self):
            return self.value

    skipped = corrected_advantages(((4., 4.), (5., 5.)), exact, probability,
                                   rng=FixedRandom(.9))
    skipped_no_calls = len(calls) == 0
    selected = corrected_advantages(((4., 4.), (5., 5.)), exact, probability,
                                    rng=FixedRandom(.1))
    selected_once = len(calls) == 1
    expected = cost_advantages(exact())
    one = corrected_advantages(((4., 4.), (5., 5.)), exact, 1., rng=FixedRandom(.9))
    before = len(calls)
    _, phase0 = warm_start_advantages(((4., 4.),), exact, step=1, warm_start_steps=2)
    untouched = len(calls) == before
    _, phase1 = warm_start_advantages(((4., 4.),), exact, step=2, warm_start_steps=2)
    error = max(abs(a-b) for a, b in zip(analytic, exact_gradient, strict=True))
    correction_error = max(abs(a-b) for a, b in zip(analytic, corrected_gradient, strict=True))
    biased_error = max(abs(a-b) for a, b in zip(analytic, cheap_gradient, strict=True))
    checks = {
        "enumerated_rloo_matches_analytic_score_gradient": error < 1e-12,
        "batch_correction_expectation_recovers_exact_gradient": correction_error < 1e-12,
        "uncorrected_cheap_estimate_is_a_distinct_biased_control": biased_error > 1e-3,
        "unselected_batch_never_calls_exact_solver": skipped_no_calls and not skipped.exact_evaluated,
        "selected_batch_calls_exact_supplier_once_for_every_instance": selected_once and selected.exact_evaluated,
        "probability_one_recovers_exact_advantages": one.advantages == expected,
        "warm_start_obeys_declared_boundary": untouched and (phase0, phase1) == ("heuristic", "exact"),
        "hindsight_constant_cancels": cost_advantages(((3., 8.),)) == cost_advantages(((103., 108.),)),
    }
    return {"seed": seed, "device": device, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "controls": checks, "metrics": {
                "analytic_gradient_max_abs_error": error,
                "corrected_gradient_max_abs_error": correction_error,
                "uncorrected_gradient_max_abs_error": biased_error,
                "expected_exact_solves_per_batch": probability*2*2,
                "knapsack_items": 3,
            }}
