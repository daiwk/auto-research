"""Extracted unchanged from auto_research.agent_research.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def video_rsi_accept(
    incumbent_accuracy: float,
    incumbent_cost: float,
    candidate_accuracy: float,
    candidate_cost: float,
    *,
    maximum_cost_growth: float = 0.1,
    minimum_cost_reduction: float = 0.1,
    maximum_accuracy_loss: float = 0.01,
) -> tuple[bool, str]:
    """Video-RSI Eq. (3), the private-selection accuracy/cost admission gate."""
    delta = candidate_accuracy - incumbent_accuracy
    accuracy_gain = delta > 0 and candidate_cost <= (1 + maximum_cost_growth) * incumbent_cost
    cost_gain = (
        -maximum_accuracy_loss <= delta <= 0
        and incumbent_cost > 0
        and candidate_cost <= (1 - minimum_cost_reduction) * incumbent_cost
    )
    if accuracy_gain:
        return True, "accuracy_gain_with_bounded_cost"
    if cost_gain:
        return True, "cost_reduction_with_bounded_accuracy_loss"
    return False, "rejected_by_private_selection_gate"
