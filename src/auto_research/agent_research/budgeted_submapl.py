"""Budgeted SubMAPL finite-domain kernel, arXiv:2611.34211v1.

Real inclusion allocation, dependent rounding, IPW and KL mirror ascent. Not an
LLM agent, complete open-domain migration, or reproduction of coverage results.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
import random
from typing import Callable

REQUIRES_GPU_VALIDATION = False
Policy = tuple[tuple[float, ...], ...]


def _policy(policy: Policy) -> None:
    if type(policy) is not tuple or not policy:
        raise ValueError("nonempty immutable agent policy tuple required")
    for block in policy:
        if type(block) is not tuple or not block or any(
                type(x) not in (int, float) or not math.isfinite(x) or x <= 0 for x in block):
            raise ValueError("finite strictly positive categorical probabilities required")
        if not math.isclose(math.fsum(block), 1.0, abs_tol=1e-12, rel_tol=1e-12):
            raise ValueError("each agent policy must sum to one")


def inclusion_probabilities(policy: Policy, budget: int, floor: float) -> tuple[float, ...]:
    """Prop.3: clipped square-root allocation, without reading current gains."""
    _policy(policy)
    flat = tuple(x for block in policy for x in block)
    if type(budget) is not int or not 1 <= budget <= len(flat):
        raise ValueError("integer query budget must be within the active dimension")
    if type(floor) not in (int, float) or not math.isfinite(floor) or not 0 < floor <= budget / len(flat):
        raise ValueError("positive feasible inclusion floor required")
    if budget == len(flat):
        return (1.0,) * len(flat)
    if math.isclose(floor * len(flat), budget, rel_tol=0, abs_tol=1e-14):
        return (budget / len(flat),) * len(flat)
    roots = tuple(math.sqrt(x) for x in flat)
    lower, upper = 0.0, 1.0
    while math.fsum(min(1.0, max(floor, upper * x)) for x in roots) < budget:
        upper *= 2
        if not math.isfinite(upper):
            raise ValueError("allocation exceeds numerical range")
    for _ in range(120):
        tau = (lower + upper) / 2
        total = math.fsum(min(1.0, max(floor, tau * x)) for x in roots)
        if total < budget:
            lower = tau
        else:
            upper = tau
    rho = [min(1.0, max(floor, ((lower + upper) / 2) * x)) for x in roots]
    # Repair only floating-point sum residual, never a statistical reallocation.
    residual = budget - math.fsum(rho)
    for i, value in enumerate(rho):
        adjustment = min(1 - value, residual) if residual >= 0 else max(floor - value, residual)
        rho[i] += adjustment
        residual -= adjustment
        if abs(residual) < 1e-15:
            break
    return tuple(rho)


def dependent_round(rho: tuple[float, ...], rng: random.Random) -> tuple[bool, ...]:
    """Pairwise/pipage rounding: exact cardinality and preserved marginals."""
    if type(rho) is not tuple or not rho or any(
            type(x) not in (int, float) or not math.isfinite(x) or not 0 <= x <= 1 for x in rho):
        raise ValueError("finite inclusion probabilities in [0,1] required")
    target = round(math.fsum(rho))
    if not math.isclose(math.fsum(rho), target, abs_tol=1e-10, rel_tol=0):
        raise ValueError("inclusions must sum to an integer")
    values = list(rho)
    while True:
        fractional = [i for i, value in enumerate(values) if 1e-13 < value < 1 - 1e-13]
        if len(fractional) < 2:
            break
        i, j = fractional[:2]
        up = min(1 - values[i], values[j])
        down = min(values[i], 1 - values[j])
        if rng.random() < down / (up + down):
            values[i] += up
            values[j] -= up
        else:
            values[i] -= down
            values[j] += down
    selected = tuple(value > 0.5 for value in values)
    if sum(selected) != target or any(min(value, 1 - value) > 1e-10 for value in values):
        raise ValueError("rounding failed numerical integrality")
    return selected


def mirror_update(policy: Policy, estimate: Policy, eta: float) -> Policy:
    _policy(policy)
    if type(eta) not in (int, float) or not math.isfinite(eta) or eta <= 0:
        raise ValueError("positive finite step size required")
    if type(estimate) is not tuple or len(estimate) != len(policy):
        raise ValueError("aligned gradient blocks required")
    updated = []
    for block, gradient in zip(policy, estimate):
        if type(gradient) is not tuple or len(gradient) != len(block) or any(
                type(g) not in (int, float) or not math.isfinite(g) or g < 0 for g in gradient):
            raise ValueError("finite bounded nonnegative marginal estimates required")
        logits = [math.log(x) + eta * g for x, g in zip(block, gradient)]
        if not all(math.isfinite(z) for z in logits):
            raise ValueError("update exceeds numerical range")
        maximum = max(logits)
        weights = [math.exp(z - maximum) for z in logits]
        normalizer = math.fsum(weights)
        result = tuple(w / normalizer for w in weights)
        if min(result) <= 0:
            raise ValueError("update underflows the required positive support")
        updated.append(result)
    return tuple(updated)


@dataclass(frozen=True)
class Step:
    policy: Policy
    joint_action: tuple[int, ...]
    queried: tuple[tuple[int, int], ...]
    inclusions: tuple[float, ...]
    gradient_estimate: Policy


def step(policy: Policy, budget: int, *, floor: float, eta: float,
         marginal: Callable[[int, int, tuple[tuple[int, int], ...]], float],
         query_rng: random.Random, action_rng: random.Random, gain_bound: float = 1.0) -> Step:
    """Only selected marginals are called. No full gain table enters the learner.

    Random streams must be independent; oracle and environment are trusted inputs.
    Inputs are immutable and no partial policy state is committed on failure.
    """
    if query_rng is action_rng:
        raise ValueError("use separate query and joint-action random streams")
    if type(gain_bound) not in (int, float) or not math.isfinite(gain_bound) or gain_bound <= 0:
        raise ValueError("positive finite marginal-gain bound required")
    rho = inclusion_probabilities(policy, budget, floor)
    selected = dependent_round(rho, query_rng)
    joint = tuple(action_rng.choices(range(len(block)), weights=block, k=1)[0] for block in policy)
    estimates, queried, offset = [], [], 0
    for i, block in enumerate(policy):
        other_actions = tuple((j, action) for j, action in enumerate(joint) if j != i)
        values = []
        for action in range(len(block)):
            if selected[offset]:
                gain = marginal(i, action, other_actions)
                if type(gain) not in (int, float) or not math.isfinite(gain) or not 0 <= gain <= gain_bound:
                    raise ValueError("oracle returned invalid/out-of-bound marginal")
                values.append(gain / rho[offset])
                queried.append((i, action))
            else:
                values.append(0.0)
            offset += 1
        estimates.append(tuple(values))
    estimate = tuple(estimates)
    return Step(mirror_update(policy, estimate, eta), joint, tuple(queried), rho, estimate)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only execution required")
    policy = ((0.8, 0.2), (0.3, 0.7))
    footprints = ((frozenset({0, 1}), frozenset({2})), (frozenset({1, 2}), frozenset({3})))
    calls = []
    def coverage_gain(agent, action, others):
        calls.append((agent, action))
        covered = frozenset().union(*(footprints[j][a] for j, a in others))
        return len(footprints[agent][action] - covered) / 4
    result = step(policy, 2, floor=0.05, eta=0.5, marginal=coverage_gain,
                  query_rng=random.Random(seed), action_rng=random.Random(seed + 1_000_003))
    phi = math.fsum(x / r for x, r in zip((x for b in policy for x in b), result.inclusions))
    full_calls = []
    def full_gain(i, a, others):
        full_calls.append((i, a))
        return (a + 1) / 4
    full = step(policy, 4, floor=0.05, eta=0.5, marginal=full_gain,
                query_rng=random.Random(seed), action_rng=random.Random(seed + 1_000_003))
    expected = mirror_update(policy, ((0.25, 0.5), (0.25, 0.5)), 0.5)
    checks = {"exact_query_budget": len(calls) == len(result.queried) == 2,
              "no_duplicate_queries": len(set(calls)) == 2,
              "inclusion_sum_is_budget": math.isclose(math.fsum(result.inclusions), 2),
              "inclusion_floor": all(0.05 <= x <= 1 for x in result.inclusions),
              "allocation_improves_second_moment_bound": phi <= 4 + 1e-12,
              "simplexes_and_support_preserved": all(min(b) > 0 and math.isclose(math.fsum(b), 1) for b in result.policy),
              "full_budget_reduces_to_full_feedback": full.policy == expected and len(full_calls) == 4}
    return {"seed": seed, "device": "cpu", "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "checks": checks, "metrics": {"queried_coordinates": len(calls), "active_coordinates": 4,
            "allocation_second_moment_factor": phi, "policy_change_l1": math.fsum(
                abs(x - y) for b, old in zip(result.policy, policy) for x, y in zip(b, old))}}
