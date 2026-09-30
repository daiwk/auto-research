"""Gold-isolated Agent evaluation and memory kernels from 2026-09-29."""

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


def premature_disclosure_rate(turns, private_fields):
    """Audit whether a simulated user reveals a private field before it is requested."""
    requested: set[str] = set()
    violations = 0
    disclosures = 0
    for turn in turns:
        requested.update(turn.get("requested_fields", ()))
        for field in turn.get("disclosed_fields", ()):
            if field not in private_fields:
                continue
            disclosures += 1
            violations += field not in requested
    return {"premature_disclosures": violations, "private_disclosures": disclosures, "rate": violations / max(1, disclosures)}


def set_level_uplift(with_memory, without_memory):
    """UpliftMem target: paired outcome improvement over the same executor without memory."""
    import numpy as np

    treatment = np.asarray(with_memory, dtype=np.float64)
    control = np.asarray(without_memory, dtype=np.float64)
    if treatment.shape != control.shape:
        raise ValueError("paired memory/no-memory outcomes must match")
    uplift = treatment - control
    return uplift, {"mean_uplift": float(uplift.mean()), "positive_fraction": float((uplift > 0).mean())}


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
