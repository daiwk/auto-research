"""Extracted unchanged from auto_research.recommendation_latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def repair_preference_state(state, cached_states, query, *, top_k: int):
    """REPAIR cached-evidence selection and residual state correction."""
    import torch

    if cached_states.ndim != 2 or state.ndim != 1 or query.shape != state.shape:
        raise ValueError("invalid REPAIR states")
    scores = cached_states @ query - cached_states @ state
    chosen = scores.topk(min(top_k, len(scores))).indices
    weights = torch.softmax(scores[chosen], dim=0)
    correction = (weights[:, None] * cached_states[chosen]).sum(0) - state
    return state + correction, {"selected_timesteps": chosen, "weights": weights}
