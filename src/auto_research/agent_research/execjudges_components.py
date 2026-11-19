"""ExecJudges fixed grade mappings and floor consensus; no generated code runs.

These APIs consume explicit boolean evidence, not raw passages or gold qrels.
No LLM writer, lexical judge, sandbox or retrieval relevance capability is claimed.
"""

from __future__ import annotations
import math

REQUIRES_GPU_VALIDATION = False


def grade_dl(*, on_subject: bool, some_answer: bool, exact_answer: bool, dedicated: bool) -> int:
    if any(type(x) is not bool for x in (on_subject, some_answer, exact_answer, dedicated)):
        raise ValueError("explicit boolean evidence required")
    if not on_subject:
        return 0
    if not some_answer:
        return 1
    return 3 if exact_answer and dedicated else 2


def grade_ternary(*, relevant: bool, key: bool) -> int:
    if type(relevant) is not bool or type(key) is not bool:
        raise ValueError("explicit boolean evidence required")
    return 0 if not relevant else 2 if key else 1


def consensus(grades, *, maximum_grade: int = 3) -> int:
    values = tuple(grades)
    if (
        maximum_grade not in (2, 3)
        or type(maximum_grade) is not int
        or not values
        or any(type(x) is not int or not 0 <= x <= maximum_grade for x in values)
    ):
        raise ValueError("nonempty valid integer grades required")
    return sum(values) // len(values)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU required")
    low, high = consensus([1, 0, 1]), consensus([3, 2, 3])
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l0_interface",
        "checks": {
            "floor_not_nearest_rounding": low == 0 and high == 2,
            "off_subject_zero": grade_dl(
                on_subject=False, some_answer=True, exact_answer=True, dedicated=True
            )
            == 0,
            "no_answer_one": grade_dl(
                on_subject=True, some_answer=False, exact_answer=True, dedicated=True
            )
            == 1,
            "ternary_not_dl": grade_ternary(relevant=True, key=True) == 2,
        },
        "metrics": {
            "fixture_low_consensus": low,
            "fixture_high_consensus": high,
            "fixture_mean_before_floor": math.fsum([3, 2, 3]) / 3,
        },
    }
