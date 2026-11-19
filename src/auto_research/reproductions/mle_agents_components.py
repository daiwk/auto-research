"""Meta MLE Agents: the published objective and admission protocol, not an agent.

No proposal generation, training job, model search, online experiment or evolve
operator is implemented here. Paper section 3.5 compares a completed candidate
with its same-iteration variance probe, not a stale historical incumbent.
"""

from __future__ import annotations

import math

REQUIRES_GPU_VALIDATION = False


def weighted_ne(click_ne: float, downstream_ne: float) -> float:
    values = (click_ne, downstream_ne)
    if any(
        isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0
        for x in values
    ):
        raise ValueError("finite nonnegative NE values required")
    return 0.3 * click_ne + 0.7 * downstream_ne


def assess_candidate(
    candidate: tuple[float, float],
    probe: tuple[float, float],
    *,
    completion_signals: tuple[bool, bool],
    coherent_changes: int = 1,
    threshold: float = 0.0005,
) -> dict:
    if len(candidate) != 2 or len(probe) != 2:
        raise ValueError("click and downstream NE required")
    if (
        not isinstance(completion_signals, tuple)
        or len(completion_signals) != 2
        or any(type(v) is not bool for v in completion_signals)
    ):
        raise ValueError("two independent completion signals required")
    if type(coherent_changes) is not int or coherent_changes != 1:
        raise ValueError("one coherent change per candidate required")
    if isinstance(threshold, bool) or not math.isfinite(threshold) or threshold <= 0:
        raise ValueError("positive finite probe threshold required")
    score, reference = weighted_ne(*candidate), weighted_ne(*probe)
    delta = reference - score
    complete = all(completion_signals)
    return {
        "complete": complete,
        "offline_search_accept": complete and delta >= threshold,
        "candidate_objective": score,
        "probe_objective": reference,
        "improvement": delta,
        "online_launch_authorized": False,
        "human_final_review_required": True,
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU required")
    win = assess_candidate((0.70, 0.63), (0.7056, 0.6421), completion_signals=(True, True))
    partial = assess_candidate((0.70, 0.63), (0.7056, 0.6421), completion_signals=(True, False))
    noisy = assess_candidate((0.7055, 0.6420), (0.7056, 0.6421), completion_signals=(True, True))
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l0_interface",
        "checks": {
            "probe_not_incumbent": win["offline_search_accept"],
            "partial_job_rejected": not partial["offline_search_accept"],
            "noise_rejected": not noisy["offline_search_accept"],
            "offline_never_launches": not win["online_launch_authorized"],
        },
        "metrics": {
            "fixture_weighted_ne": win["candidate_objective"],
            "fixture_probe_improvement": win["improvement"],
        },
    }
