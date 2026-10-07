"""Extracted unchanged from auto_research.agent_research.latest_20260930_closure; stable mechanism boundary."""
from __future__ import annotations



def rubric_process_credit(history_support, new_support):
    """Dr.Credit counts new, partial rubric support rather than repeated evidence."""
    import numpy as np

    history = np.asarray(history_support, dtype=np.float64)
    current = np.asarray(new_support, dtype=np.float64)
    if history.shape != current.shape or np.any((current < 0) | (current > 1)):
        raise ValueError("rubric support must align and lie in [0,1]")
    credit = np.maximum(current - history, 0)
    return credit, {"new_support": float(credit.sum()), "covered_rubrics": int((current > 0).sum())}
