"""Extracted unchanged from auto_research.agent_research.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def set_level_uplift(with_memory, without_memory):
    """UpliftMem target: paired outcome improvement over the same executor without memory."""
    import numpy as np

    treatment = np.asarray(with_memory, dtype=np.float64)
    control = np.asarray(without_memory, dtype=np.float64)
    if treatment.shape != control.shape:
        raise ValueError("paired memory/no-memory outcomes must match")
    uplift = treatment - control
    return uplift, {"mean_uplift": float(uplift.mean()), "positive_fraction": float((uplift > 0).mean())}
