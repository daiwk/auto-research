"""Trace-driven cold-restart cascade from arXiv:2611.24324, IV.E--G.

This is an offline policy-accounting component, not a coding agent. Completion
and verification labels remain evaluator input; the actor is never passed them.
Effective exclusive-allocation GPU hours are not physical cluster GPU hours.
"""

from __future__ import annotations
from dataclasses import dataclass
from collections.abc import Sequence
import math

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class Trace:
    seconds: float
    gpu_count: int
    valid_patch: bool
    tests_passed: bool

    def __post_init__(self):
        if isinstance(self.seconds, bool) or not math.isfinite(self.seconds) or self.seconds < 0:
            raise ValueError("finite nonnegative recorded runtime required")
        if type(self.gpu_count) is not int or self.gpu_count < 1:
            raise ValueError("positive exclusive GPU allocation required")
        if type(self.valid_patch) is not bool or type(self.tests_passed) is not bool:
            raise ValueError("strict evaluator labels required")
        if self.tests_passed and not self.valid_patch:
            raise ValueError("passing tests require a valid submitted patch")


def cascade(small: Trace, large: Trace, timeout_seconds: float) -> dict:
    """Charge only elapsed small time before timeout; fallback restarts from zero."""
    if not isinstance(small, Trace) or not isinstance(large, Trace):
        raise TypeError("a complete pair of recorded traces is required")
    if (
        isinstance(timeout_seconds, bool)
        or not math.isfinite(timeout_seconds)
        or timeout_seconds < 0
    ):
        raise ValueError("finite nonnegative timeout required")
    small_elapsed = min(small.seconds, timeout_seconds)
    small_success = small.seconds <= timeout_seconds and small.valid_patch and small.tests_passed
    fallback = not small_success
    gpu_hours = small_elapsed * small.gpu_count / 3600
    wall_seconds = small_elapsed
    if fallback:
        gpu_hours += large.seconds * large.gpu_count / 3600
        wall_seconds += large.seconds
    return {
        "resolved": small_success or (fallback and large.valid_patch and large.tests_passed),
        "fallback": fallback,
        "small_seconds_charged": small_elapsed,
        "gpu_hours": gpu_hours,
        "wall_seconds": wall_seconds,
        "fallback_initial_state": "original_task",
        "accounting": "exclusive_effective_gpu_hours",
    }


def evaluate(pairs: Sequence[tuple[Trace, Trace]], timeout_seconds: float) -> dict:
    if not pairs:
        raise ValueError("nonempty matched trace pairs required; missing records are not failures")
    rows = [cascade(s, l, timeout_seconds) for s, l in pairs]
    return {
        "paired_tasks": len(rows),
        "resolve_rate": sum(r["resolved"] for r in rows) / len(rows),
        "fallback_rate": sum(r["fallback"] for r in rows) / len(rows),
        "gpu_hours": sum(r["gpu_hours"] for r in rows),
        "wall_seconds": sum(r["wall_seconds"] for r in rows),
    }


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU required")
    small = Trace(60, 1, True, True)
    large = Trace(120, 4, True, True)
    short, enough = cascade(small, large, 30), cascade(small, large, 60)
    failure = cascade(Trace(10, 1, True, False), large, 60)
    zero = cascade(small, large, 0)
    measured = evaluate(((small, large), (Trace(80, 1, False, False), large)), 60)
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "timeout_charges_prefix": short["small_seconds_charged"] == 30,
            "at_boundary_accepts_valid_patch": not enough["fallback"],
            "failed_tests_force_cold_restart": failure["fallback"]
            and failure["fallback_initial_state"] == "original_task",
            "zero_timeout_large_only": zero["gpu_hours"] == 120 * 4 / 3600,
            "sequential_latency_counts_both": short["wall_seconds"] == 150,
            "effective_not_cluster_cost": short["gpu_hours"] == (30 + 120 * 4) / 3600,
        },
        "metrics": {
            "controlled_pair_fallback_rate": measured["fallback_rate"],
            "controlled_effective_gpu_hours": measured["gpu_hours"],
            "controlled_wall_seconds": measured["wall_seconds"],
        },
    }
