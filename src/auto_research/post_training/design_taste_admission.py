"""Tasteful Designs v1 §4 signal admission and gated reward protocol.

External experts/renderers supply observations. No expert score enters reward.
"""

import math
from ._nov18_contracts import receipt, scalar

REQUIRES_GPU_VALIDATION = False


def admit(*, expert_agreement, causal_sensitivity, hack_trap_failure, self_agreement):
    a = scalar(expert_agreement, "expert_agreement", lower=0, upper=1)
    c = scalar(causal_sensitivity, "causal_sensitivity", lower=0, upper=1)
    h = scalar(hack_trap_failure, "hack_trap_failure", lower=0, upper=1)
    s = scalar(self_agreement, "self_agreement", lower=0, upper=1)
    checks = {
        "expert_agreement": a >= 0.85,
        "causal_sensitivity": c >= 0.9,
        "hack_trap_resistance": h <= 0.2,
        "stability": s >= 0.9,
    }
    return {"admitted": all(checks.values()), "checks": checks}


def composite_reward(gates, scores, weights, *, length_penalty=0, turn_penalty=0):
    expected = {"func", "design", "rubric", "pref"}
    if (
        set(scores) != expected
        or set(weights) != expected
        or not gates
        or any(type(v) is not bool for v in gates.values())
    ):
        raise ValueError("four declared score/weight channels and Boolean V0 gates required")
    sc = {k: scalar(v, k, lower=0, upper=1) for k, v in scores.items()}
    w = {k: scalar(v, k, lower=0, upper=1) for k, v in weights.items()}
    if not math.isclose(sum(w.values()), 1, abs_tol=1e-10):
        raise ValueError("weights must sum to one")
    lp = scalar(length_penalty, "length_penalty", lower=0)
    tp = scalar(turn_penalty, "turn_penalty", lower=0)
    return float(all(gates.values())) * max(0.0, sum(sc[k] * w[k] for k in expected) - lp - tp)


def eligible_starting_state(start_reward):
    return scalar(start_reward, "starting_reward", lower=0, upper=1) <= 0.4


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("CPU admission protocol requires integer seed")
    good = admit(
        expert_agreement=0.85, causal_sensitivity=0.9, hack_trap_failure=0.2, self_agreement=0.9
    )
    hacked = admit(
        expert_agreement=0.99, causal_sensitivity=0.99, hack_trap_failure=0.21, self_agreement=0.99
    )
    scores = dict(func=0.9, design=0.8, rubric=0.7, pref=0.6)
    weights = dict.fromkeys(scores, 0.25)
    ok = composite_reward({"build": True, "render": True, "no_regression": True}, scores, weights)
    failure = composite_reward(
        {"build": True, "render": True, "no_regression": False}, scores, weights
    )
    return receipt(
        seed,
        "l0_interface",
        {
            "all_four_boundaries_are_inclusive": good["admitted"],
            "high_agreement_does_not_override_hack_trap": not hacked["admitted"],
            "integrity_is_multiplicative": failure == 0,
            "starting_state_floor_is_separate": eligible_starting_state(0.4)
            and not eligible_starting_state(0.41),
        },
        {"gated_reward": ok, "failed_gate_reward": failure, "admission_threshold": 0.85},
    )
