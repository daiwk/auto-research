"""Extracted unchanged from auto_research.agent_research.latest_20260930_followup; stable mechanism boundary."""
from __future__ import annotations



def gaussian_evsi(means, covariance, candidate_sets, *, observation_noise: float = 1.0):
    """Closed-form one-step correlated-Gaussian EVSI for targeted memory-set probes."""
    import numpy as np

    means = np.asarray(means, dtype=np.float64)
    covariance = np.asarray(covariance, dtype=np.float64)
    candidates = np.asarray(candidate_sets, dtype=np.int64)
    if covariance.shape != (len(means), len(means)) or np.any(candidates < 0) or np.any(candidates >= len(means)):
        raise ValueError("invalid Gaussian posterior or candidate index")
    incumbent = means.max()
    scores = []
    for index in candidates:
        posterior_variance = covariance[index, index] ** 2 / (covariance[index, index] + observation_noise)
        expected_positive = max(0.0, means[index] - incumbent) + (posterior_variance ** 0.5) / (2 * np.pi) ** 0.5
        scores.append(expected_positive)
    scores = np.asarray(scores)
    return int(candidates[int(scores.argmax())]), scores
