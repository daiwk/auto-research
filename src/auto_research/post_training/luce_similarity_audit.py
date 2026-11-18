"""L1 arithmetic for Luce/Bradley--Terry similarity audits, not a fitted ranker.

Fixed source: arXiv:2610.19095v3, Equations 1--3 and Section 6.  Ties and
frozen-transfer uncertainty must be reported separately from non-tied odds.
"""

from __future__ import annotations

import math

REQUIRES_GPU_VALIDATION = False


def corrected_win_probability(score_gap: float, decisiveness: float = 1.0) -> float:
    """P(i wins | not tied), Equation 2; this does not fit a tie model."""
    if not math.isfinite(score_gap) or not math.isfinite(decisiveness) or decisiveness <= 0:
        raise ValueError("finite gap and positive decisiveness are required")
    z = decisiveness * score_gap
    return 1 / (1 + math.exp(-z)) if z >= 0 else math.exp(z) / (1 + math.exp(z))


def menu_log_odds_shift(
    sibling_outsider: float, sibling_anchor: float,
    placebo_outsider: float, placebo_anchor: float,
) -> float:
    """Equation 3 on supplied shares/counts, without hiding zero-cell problems.

    Pooling counts over prompts is not a within-prompt IIA test.  The caller
    must preserve prompt/order strata for that separate estimand.
    """
    values = (sibling_outsider, sibling_anchor, placebo_outsider, placebo_anchor)
    if any(not math.isfinite(v) or v <= 0 for v in values):
        raise ValueError("all four counts/shares must be positive and finite")
    return (math.log(sibling_outsider) - math.log(sibling_anchor)) - (
        math.log(placebo_outsider) - math.log(placebo_anchor)
    )


def heldout_log_loss(labels: list[int], probabilities: list[float]) -> float:
    """Non-tied binary log loss only; it cannot establish a three-outcome gain."""
    if not labels or len(labels) != len(probabilities):
        raise ValueError("equal nonempty labels and probabilities required")
    if any(y not in (0, 1) for y in labels) or any(
        not math.isfinite(p) or not 0 < p < 1 for p in probabilities
    ):
        raise ValueError("binary labels and probabilities strictly inside (0, 1) required")
    return -sum(math.log(p if y else 1 - p) for y, p in zip(labels, probabilities, strict=True)) / len(labels)


def transfer_improvement_established(interval_low: float, interval_high: float) -> bool:
    """A positive point estimate is insufficient when its interval includes zero."""
    if not all(math.isfinite(v) for v in (interval_low, interval_high)) or interval_low > interval_high:
        raise ValueError("ordered finite interval required")
    return interval_low > 0


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU only")
    plain = corrected_win_probability(0.5)
    sibling = corrected_win_probability(0.5, 1.1)
    delta = menu_log_odds_shift(30, 20, 30, 30)
    return {
        "seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
        "checks": {
            "greater_decisiveness_moves_odds_away_from_even": sibling > plain > 0.5,
            "same_score_remains_even": corrected_win_probability(0, 1.37) == 0.5,
            "reverse_pair_complements": math.isclose(corrected_win_probability(-0.5, 1.1), 1 - sibling),
            "identical_menus_have_zero_shift": math.isclose(menu_log_odds_shift(3, 2, 6, 4), 0, abs_tol=1e-12),
            "extreme_positive_counts_remain_finite": math.isfinite(menu_log_odds_shift(1e300, 1e-300, 1, 1)),
            "frozen_transfer_interval_is_inconclusive": not transfer_improvement_established(-2.92, 1.68),
        },
        "metrics": {"teaching_plain_probability": plain, "teaching_corrected_probability": sibling,
                    "teaching_menu_shift": delta},
    }
