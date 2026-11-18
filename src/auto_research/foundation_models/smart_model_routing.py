"""Cost/quality arithmetic for external model routing, not an inference router.

arXiv:2611.15911v1 Sections 3.1--3.3; quantities are supplied estimates, not
gold outcomes observed by a deployed router.  Hypothetical prices are not quotes.
"""

from __future__ import annotations

import math

REQUIRES_GPU_VALIDATION = False


def _finite_nonnegative(values: list[float]) -> None:
    if any(not math.isfinite(x) or x < 0 for x in values):
        raise ValueError("finite nonnegative costs required")


def _probabilities(values: list[float]) -> None:
    if any(not math.isfinite(x) or not 0 <= x <= 1 for x in values):
        raise ValueError("probabilities must lie in [0, 1]")


def _finite_result(value: float) -> float:
    if not math.isfinite(value):
        raise ValueError("cost arithmetic exceeded finite floating-point range")
    return value


def token_cost(input_tokens: int, output_tokens: int, input_price_per_million: float,
               output_price_per_million: float) -> float:
    if any(type(x) is not int or x < 0 for x in (input_tokens, output_tokens)):
        raise ValueError("nonnegative integer token counts required")
    _finite_nonnegative([input_price_per_million, output_price_per_million])
    return _finite_result((input_tokens / 1_000_000) * input_price_per_million
                          + (output_tokens / 1_000_000) * output_price_per_million)


def shadow_price_tier(costs: list[float], predicted_qualities: list[float], shadow_price: float) -> int:
    """Equation 7: argmin_i(c_i - lambda*q_i), deterministic first-index tie.

    Lambda must be selected on validation data to meet the aggregate quality
    constraint; this function alone does not guarantee any per-segment floor.
    Quality predictions are inputs, never held-out labels queried at routing time.
    """
    if not costs or len(costs) != len(predicted_qualities):
        raise ValueError("equal nonempty candidate costs and predicted qualities required")
    _finite_nonnegative([*costs, shadow_price])
    _probabilities(predicted_qualities)
    return min(range(len(costs)), key=lambda i: costs[i] - shadow_price * predicted_qualities[i])


def minimum_frontier_share(cheap_quality: float, frontier_quality: float, floor: float) -> float:
    """Constant-quality counterexample: calibration alone cannot identify easy requests."""
    _probabilities([cheap_quality, frontier_quality, floor])
    if floor <= cheap_quality:
        return 0.0
    if frontier_quality <= cheap_quality or floor > frontier_quality:
        raise ValueError("quality floor is infeasible")
    return (floor - cheap_quality) / (frontier_quality - cheap_quality)


def cost_reduction(frontier_share: float, price_ratio: float, *, frontier_token_ratio: float = 1,
                   router_cost_in_cheap_units: float = 0) -> float:
    """Equation 5, with router overhead; baseline uses the same request/token mix."""
    _probabilities([frontier_share])
    if not math.isfinite(price_ratio) or price_ratio <= 0 or not math.isfinite(frontier_token_ratio) or frontier_token_ratio <= 0:
        raise ValueError("positive finite price and token ratios required")
    _finite_nonnegative([router_cost_in_cheap_units])
    phi, tau = frontier_share, frontier_token_ratio
    baseline = price_ratio * ((1 - phi) + phi * tau)
    routed = (1 - phi) + phi * tau * price_ratio + router_cost_in_cheap_units
    if routed == 0:
        raise ValueError("cost arithmetic exceeded finite floating-point range")
    return _finite_result(baseline / routed)


def cascade_cost(costs: list[float], acceptance_rates: list[float], *,
                 checker_costs: list[float] | None = None, router_cost: float = 0) -> float:
    """Equation 6 plus reached-stage checker and once-per-request router overhead."""
    if not costs or len(costs) != len(acceptance_rates) or acceptance_rates[-1] != 1:
        raise ValueError("equal nonempty stages and terminal acceptance=1 required")
    checkers = [0.0] * len(costs) if checker_costs is None else checker_costs
    if len(checkers) != len(costs):
        raise ValueError("one checker cost per stage required")
    _finite_nonnegative([*costs, *checkers, router_cost])
    _probabilities(acceptance_rates)
    reach, total = 1.0, router_cost
    for cost, checker, acceptance in zip(costs, checkers, acceptance_rates, strict=True):
        total += reach * (cost + checker)
        reach *= 1 - acceptance
    return _finite_result(total)


def two_stage_breakeven(cheap_cost: float, frontier_cost: float, *, checker_cost: float = 0,
                        router_cost: float = 0) -> float:
    """Strictly lower cost requires acceptance > this threshold, not >=."""
    _finite_nonnegative([cheap_cost, frontier_cost, checker_cost, router_cost])
    if frontier_cost == 0:
        raise ValueError("positive escalation cost required")
    return _finite_result((cheap_cost + checker_cost + router_cost) / frontier_cost)


def cascade_quality(acceptance_rates: list[float], conditional_qualities: list[float]) -> float:
    if not acceptance_rates or len(acceptance_rates) != len(conditional_qualities) or acceptance_rates[-1] != 1:
        raise ValueError("equal stages and final acceptance=1 required")
    _probabilities([*acceptance_rates, *conditional_qualities])
    reach, total = 1.0, 0.0
    for acceptance, quality in zip(acceptance_rates, conditional_qualities, strict=True):
        total += reach * acceptance * quality
        reach *= 1 - acceptance
    return total


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    naive = cost_reduction(.02, 25)
    corrected = cost_reduction(.02, 25, frontier_token_ratio=100)
    threshold = two_stage_breakeven(1, 10, checker_cost=1, router_cost=.5)
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "checks": {"token_mix_reduces_apparent_savings": corrected < naive,
                       "router_overhead_reduces_savings": cost_reduction(.02, 25, router_cost_in_cheap_units=1) < naive,
                       "breakeven_is_strict": math.isclose(cascade_cost([1, 10], [threshold, 1], checker_costs=[1, 0], router_cost=.5), 10),
                       "residual_quality_not_unconditional": math.isclose(cascade_quality([.5, 1], [1, .2]), .6),
                       "calibration_does_not_identify_easy_queries": math.isclose(minimum_frontier_share(.9, .99, .98), 8 / 9)},
            "metrics": {"teaching_naive_reduction": naive, "teaching_token_corrected_reduction": corrected,
                        "teaching_breakeven_acceptance": threshold}}
