"""ProEval finite-pool empirical GP/BQ core (2604.23099v1 Eq2,5,7,10,12).

Historical score rows exclude the target model; no hidden target scores are
accepted by acquisition. Prompt-encoder pretraining and SS-Gen are not present.
"""
from __future__ import annotations

import numpy as np


class EmpiricalGP:
    def __init__(self, historical_scores, *, historical_ids, target_id, noise=1e-4):
        scores = np.asarray(historical_scores, dtype=float)
        if (scores.ndim != 2 or scores.shape[0] < 3 or not scores.shape[1]
                or not np.isfinite(scores).all() or len(historical_ids) != len(scores)
                or len(set(historical_ids)) != len(scores) or target_id in historical_ids
                or not np.isfinite(noise) or noise <= 0):
            raise ValueError(">=3 distinct historical models, no target and positive noise required")
        self.prior_mean = scores.mean(axis=0)
        features = (scores-self.prior_mean)/np.sqrt(len(scores)-1)
        self.prior_cov = features.T@features
        self.noise = noise
        self.observed: dict[int, float] = {}

    def observe(self, index: int, value: float):
        if (not isinstance(index, (int, np.integer)) or not 0 <= index < len(self.prior_mean)
                or index in self.observed or not np.isfinite(value)):
            raise ValueError("new valid index and finite score required")
        self.observed[int(index)] = float(value)

    def posterior(self):
        if not self.observed:
            return self.prior_mean.copy(), self.prior_cov.copy()
        indices = list(self.observed)
        cross = self.prior_cov[:, indices]
        gram = self.prior_cov[np.ix_(indices, indices)]+self.noise*np.eye(len(indices))
        mean = self.prior_mean+cross@np.linalg.solve(gram,
                    np.array(list(self.observed.values()))-self.prior_mean[indices])
        cov = self.prior_cov-cross@np.linalg.solve(gram, cross.T)
        return mean, (cov+cov.T)/2

    def quadrature(self, weights=None):
        mean, cov = self.posterior()
        w = self._weights(weights)
        return {"mean": float(w@mean), "variance": max(0.0, float(w@cov@w))}

    def _weights(self, weights):
        size = len(self.prior_mean)
        w = np.ones(size)/size if weights is None else np.asarray(weights, dtype=float)
        if w.shape != (size,) or not np.isfinite(w).all() or (w < 0).any() or not np.isclose(w.sum(), 1):
            raise ValueError("normalized nonnegative pool weights required")
        return w

    def acquisition(self, *, objective="bq", threshold=0.5, beta=1.0, weights=None):
        mean, cov = self.posterior()
        diagonal = np.maximum(0, np.diag(cov))
        if objective == "bq":
            # Exact finite-pool one-observation variance reduction, Eq10.
            scores = (self._weights(weights)@cov)**2/(diagonal+self.noise)
        elif objective == "failure":
            if not np.isfinite([threshold, beta]).all():
                raise ValueError("finite superlevel parameters required")
            scores = np.where(mean+beta*np.sqrt(diagonal) >= threshold, diagonal, -np.inf)
        else:
            raise ValueError("objective must be bq or failure")
        scores[list(self.observed)] = -np.inf
        return scores

    def select(self, **kwargs):
        scores = self.acquisition(**kwargs)
        return None if not np.isfinite(scores).any() else int(np.argmax(scores))
