"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations



def dr_opd_token_weights(
    teacher_student_log_ratio,
    reward_directional_derivative,
    *,
    strength: float = 1.0,
    minimum: float = 0.1,
    maximum: float = 3.0,
    epsilon: float = 1e-6,
):
    """Dr. OPD Eqs. (12)-(14): credit-aware closed-form token weights.

    The caller supplies the JVP directional derivative along the sampled
    reward gradient.  Keeping that interface explicit prevents this L1 kernel
    from pretending that a heuristic score is the paper's model-space JVP.
    """
    import torch

    if teacher_student_log_ratio.shape != reward_directional_derivative.shape:
        raise ValueError("discrepancy and reward directional derivative must match")
    if not 0 < minimum <= maximum:
        raise ValueError("weight bounds must be positive and ordered")
    credits = teacher_student_log_ratio.detach() * reward_directional_derivative.detach()
    rms = credits.square().mean().sqrt().clamp_min(epsilon)
    weights = (1 + strength * credits / rms).clamp(minimum, maximum)
    return weights, {"credit_rms": float(rms), "minimum_weight": float(weights.min()), "maximum_weight": float(weights.max())}
