"""Extracted unchanged from auto_research.post_training.latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def gats_schedule(teacher_scores, student_history, *, window: int, withdrawn: bool = False):
    """One-step-lagged GATS weight and permanent teacher withdrawal."""
    import numpy as np

    if window < 1 or len(teacher_scores) < window or not student_history:
        raise ValueError("GATS requires teacher tail and prior student measurements")
    teacher_ref = float(np.mean(teacher_scores[-window:]))
    student_ref = float(np.mean(student_history[-window:]))
    if teacher_ref <= 0:
        raise ValueError("teacher reference must be positive")
    withdrawn = bool(withdrawn or student_ref >= teacher_ref)
    weight = 0.0 if withdrawn else max(1.0 - student_ref / teacher_ref, 0.0)
    return weight, withdrawn, {"teacher_reference": teacher_ref, "student_reference": student_ref}
