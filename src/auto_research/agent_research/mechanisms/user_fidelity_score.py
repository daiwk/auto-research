"""Extracted unchanged from auto_research.agent_research.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def user_fidelity_score(rubric_results):
    """UserProxyBench UFS: score simulator-role adherence independent of agent reward."""
    import numpy as np

    results = np.asarray(rubric_results, dtype=np.float64)
    if results.ndim != 2 or np.any((results < 0) | (results > 1)):
        raise ValueError("rubric results must be [episodes, criteria] in [0,1]")
    # Eq. (1) is deliberately strict: an episode passes only if every
    # applicable user-contract criterion passes.
    per_episode = results.prod(axis=1)
    return {"user_fidelity_score": float(per_episode.mean()), "episode_scores": per_episode}
