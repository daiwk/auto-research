"""TokenWorth Appendix B: selected-pair online learning and bounded admission.

CPU mathematical controller only, not an Agent, benchmark or semantic encoder.
Reward enters `finish` only after the caller's native task evaluation. Pending
tasks prohibit retrieval/admission updates, and only the selected pair is fit.
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import hashlib
import math
import re

import numpy as np


PRIOR = np.array([1., .1, .1, .02])


def vector(text: str, dimension: int = 512) -> np.ndarray:
    """Stable token + character 3--5 gram hashing; no learned semantics.

    Hash family/tokenizer are explicit local choices (SHA256, Unicode words,
    lowercase text), since Appendix B does not specify those implementation bits.
    """
    if not isinstance(text, str) or type(dimension) is not int or not 1 <= dimension <= 4096:
        raise ValueError("text and bounded positive dimension required")
    text = text.lower()
    features = ["w:" + token for token in re.findall(r"\w+", text)]
    features += [f"c{width}:" + text[i:i+width] for width in (3, 4, 5)
                 for i in range(max(0, len(text)-width+1))]
    result = np.zeros(dimension)
    for feature in features:
        digest = hashlib.sha256(feature.encode()).digest()
        result[int.from_bytes(digest[:8], "big") % dimension] += 1.
    norm = np.linalg.norm(result)
    return result / norm if norm else result


def _matrix(value, width: int | None = None):
    value = np.asarray(value, dtype=float)
    if (value.ndim != 2 or not value.shape[0] or not value.shape[1]
            or (width is not None and value.shape[1] != width) or not np.isfinite(value).all()):
        raise ValueError("finite nonempty matrix required")
    return value


def _labels(labels, n: int):
    labels = np.asarray(labels, dtype=float)
    if labels.shape != (n,) or not np.isfinite(labels).all():
        raise ValueError("finite aligned targets required")
    return labels


def sigmoid(value):
    value = np.asarray(value, dtype=float)
    return np.exp(-np.logaddexp(0., -value))


def logistic_loss(weights, features, labels, *, regularization=.1):
    features = _matrix(features, 4)
    labels = _labels(labels, len(features))
    weights = np.asarray(weights, dtype=float)
    if (weights.shape != (4,) or not np.isfinite(weights).all()
            or not np.isin(labels, [-1., 1.]).all()
            or not math.isfinite(regularization) or regularization <= 0):
        raise ValueError("invalid logistic parameters")
    return float(np.logaddexp(0., -labels*(features @ weights)).sum()
                 + regularization*np.square(weights-PRIOR).sum())


def fit_base(features, labels, current=None, *, regularization=.1):
    """Deterministic Newton/backtracking, then Appendix B smoothing and clipping."""
    features = _matrix(features, 4)
    labels = _labels(labels, len(features))
    current = PRIOR.copy() if current is None else np.asarray(current, dtype=float)
    logistic_loss(current, features, labels, regularization=regularization)
    weights = current.copy()
    for _ in range(80):
        p = sigmoid(-labels*(features @ weights))
        gradient = features.T @ (-labels*p) + 2*regularization*(weights-PRIOR)
        if np.linalg.norm(gradient) < 1e-9:
            break
        hessian = features.T @ (features*(p*(1-p))[:, None]) + 2*regularization*np.eye(4)
        direction = np.linalg.solve(hessian, gradient)
        loss = logistic_loss(weights, features, labels, regularization=regularization)
        step = 1.
        while step >= 2**-30:
            candidate = weights-step*direction
            if logistic_loss(candidate, features, labels, regularization=regularization) <= (
                    loss-1e-4*step*float(gradient @ direction)):
                weights = candidate
                break
            step *= .5
        else:
            break
    return np.clip(.5*current+.5*weights, [0., 0., 0., 0.], [2., 1., 1., 1.])


def laplacian(left, right, metric):
    left, right = _matrix(left), _matrix(right)
    metric = np.asarray(metric, dtype=float)
    if (left.shape[1] != right.shape[1] or metric.shape != (left.shape[1],)
            or not np.isfinite(metric).all() or np.any(metric <= 0)):
        raise ValueError("positive finite diagonal metric and aligned vectors required")
    delta = left[:, None, :]-right[None, :, :]
    return np.exp(-np.sqrt(np.sum(delta*delta*metric, axis=2)))


class ResidualRFM:
    def __init__(self, dimension: int):
        if type(dimension) is not int or not 1 <= dimension <= 4101:
            raise ValueError("bounded positive feature dimension required")
        self.metric = np.ones(dimension)
        self.centers, self.coefficients = np.empty((0, dimension)), np.empty(0)
        self.fits = 0

    def fit(self, features, targets):
        features = _matrix(features, len(self.metric))
        if len(features) > 128:
            raise ValueError("fast window cannot exceed 128")
        targets = _labels(targets, len(features))
        gram = laplacian(features, features, self.metric)
        coefficients = np.linalg.solve(gram + .01*np.eye(len(features)), targets)
        self.centers, self.coefficients = features.copy(), coefficients
        self.fits += 1

    def predict(self, features):
        features = _matrix(features, len(self.metric))
        return (laplacian(features, self.centers, self.metric) @ self.coefficients
                if len(self.centers) else np.zeros(len(features)))

    def gradients(self, features):
        features = _matrix(features, len(self.metric))
        if not len(self.centers):
            return np.zeros_like(features)
        delta = features[:, None, :]-self.centers[None, :, :]
        distance = np.sqrt(np.sum(delta*delta*self.metric, axis=2))
        # Laplacian kernel has a cusp at identical vectors; use the symmetric
        # zero subgradient there, not division by epsilon or NaN.
        scales = np.divide(-np.exp(-distance)*self.coefficients[None, :], distance,
                           out=np.zeros_like(distance), where=distance > 0)
        return np.sum(scales[:, :, None]*delta*self.metric, axis=1)

    def adapt(self, slow_features, fast_features, fast_targets):
        slow_features = _matrix(slow_features, len(self.metric))
        if len(slow_features) > 256 or not len(self.centers):
            raise ValueError("fitted predictor and at most 256 slow examples required")
        agop = np.mean(self.gradients(slow_features)**2, axis=0)
        updated = np.clip(.75*self.metric+.25*agop, .05, 8.)
        self.metric = updated/updated.mean()
        self.fit(fast_features, fast_targets)


@dataclass
class Memory:
    key: str
    text: str
    created: int
    utility: float = 1.
    hits: int = 0
    misses: int = 0
    accesses: int = 0
    last_access: int | None = None


def features(query: str, memory: Memory, t: int, *, dimension=512):
    if (not isinstance(memory.key, str) or not memory.key or type(t) is not int
            or type(memory.created) is not int or not 0 <= memory.created <= t
            or memory.last_access is not None and not memory.created <= memory.last_access <= t
            or not math.isfinite(memory.utility) or not -2 <= memory.utility <= 5
            or any(type(x) is not int or x < 0 for x in (memory.hits, memory.misses, memory.accesses))
            or memory.hits+memory.misses != memory.accesses):
        raise ValueError("invalid/acyclic memory statistics")
    eq, em = vector(query, dimension), vector(memory.text, dimension)
    sim = float(eq @ em)
    reliability = (memory.hits+1)/(memory.hits+memory.misses+2)
    recent = math.exp(-.02*(t-(memory.last_access if memory.last_access is not None else memory.created)))
    frequency = memory.accesses/max(1, t-memory.created+1)
    phi = np.array([sim, memory.utility, reliability, recent])
    residual = np.concatenate((np.abs(eq-em), [sim, memory.utility, reliability, recent, frequency]))
    return phi, residual


@dataclass(frozen=True)
class Selection:
    """Actor-visible public memory only; no outcome, private features or gold."""
    task: int
    key: str | None
    text: str


def admission_decision(bank, candidate, probes, *, score, capacity: int, dimension=512):
    """Appendix B gate; successful provenance is enforced by controller.finish."""
    if (type(capacity) is not int or capacity <= 0 or len(bank) > capacity
            or not probes or len(probes) > 9 or any(not isinstance(q, str) for q in probes)
            or candidate.key in {memory.key for memory in bank}
            or len({memory.key for memory in bank}) != len(bank)):
        raise ValueError("invalid bounded admission inputs")
    if len(bank) < capacity:
        return tuple(bank)+(candidate,), "coverage"
    scores = {memory.key: np.array([score(query, memory) for query in probes], dtype=float)
              for memory in (*bank, candidate)}
    if any(not np.isfinite(values).all() for values in scores.values()):
        raise ValueError("finite worth scores required")
    values = {key: float(array.mean()) for key, array in scores.items()}
    similarities = [(float(vector(candidate.text, dimension) @ vector(memory.text, dimension)), memory)
                    for memory in bank]
    similarity, nearest = max(similarities, key=lambda entry: entry[0])
    passes = (1-similarity > .35 or (values[candidate.key] > max(values[m.key] for m in bank)+.02
               and float(np.mean(scores[candidate.key] > 0)) >= .45))
    if passes:
        enlarged = (*bank, candidate)
        # Equal values deterministically evict the new candidate, conservatively.
        evicted = min(enlarged, key=lambda m: (values[m.key], m.key != candidate.key))
        return tuple(m for m in enlarged if m.key != evicted.key), (
            "candidate_self_evicted" if evicted.key == candidate.key else "admit_evict")
    if nearest.utility < .5 and values[candidate.key] > values[nearest.key]+.10:
        return tuple(m for m in bank if m.key != nearest.key)+(candidate,), "replace_nearest"
    return tuple(bank), "reject"


class TokenWorth:
    """DB defaults; interval changes for diagnostics must be reported explicitly."""

    def __init__(self, *, capacity=64, dimension=512, base_interval=50,
                 krr_interval=50, agop_interval=200, warmup=4, eta=.15):
        if (any(type(v) is not int or v <= 0 for v in (
                capacity, dimension, base_interval, krr_interval, agop_interval, warmup))
                or capacity > 4096 or dimension > 4096 or warmup > 128
                or not math.isfinite(eta) or not 0 <= eta <= 1):
            raise ValueError("invalid bounded controller configuration")
        self.capacity, self.dimension = capacity, dimension
        self.base_interval, self.krr_interval = base_interval, krr_interval
        self.agop_interval, self.warmup, self.eta = agop_interval, warmup, eta
        self.weights, self.rfm = PRIOR.copy(), ResidualRFM(dimension+5)
        self.bank: dict[str, Memory] = {}
        self.base, self.fast, self.slow = deque(maxlen=256), deque(maxlen=128), deque(maxlen=256)
        self.queries = deque(maxlen=8)
        self.t, self.feedback, self.pending = 1, 0, None

    def score(self, query, memory):
        phi, residual = features(query, memory, self.t, dimension=self.dimension)
        return float(self.weights @ phi + self.eta*min(self.rfm.fits/3, 1)*self.rfm.predict(residual[None])[0])

    def begin(self, query: str) -> Selection:
        if self.pending is not None:
            raise ValueError("finish previous task before the next retrieval")
        vector(query, self.dimension)
        candidates = sorted(self.bank.values(), key=lambda m: (
            -float(vector(query, self.dimension) @ vector(m.text, self.dimension)), m.key))[:12]
        selected = max(candidates, key=lambda m: (self.score(query, m), m.key)) if candidates else None
        phi, residual = features(query, selected, self.t, dimension=self.dimension) if selected else (None, None)
        self.pending = (query, selected.key if selected else None, phi, residual,
                        float(self.weights @ phi) if selected else None)
        return Selection(self.t, selected.key if selected else None, selected.text if selected else "")

    def finish(self, reward: bool, *, new_memory: tuple[str, str] | None = None):
        """Caller supplies completed native grader outcome, never current gold.

        Successful public trajectories may become memory; benchmark reference
        solutions/unit tests must never be used as `new_memory`.
        """
        if self.pending is None or type(reward) is not bool:
            raise ValueError("one completed native boolean outcome per pending task required")
        query, key, phi, residual, base_score = self.pending
        if new_memory is not None:
            if (not reward or type(new_memory) is not tuple or len(new_memory) != 2
                    or any(not isinstance(s, str) or not s for s in new_memory)
                    or new_memory[0] in self.bank):
                raise ValueError("unique public memory from a verified successful task required")
        if key is not None:
            label = 1. if reward else -1.
            target = label-(2*float(sigmoid(base_score))-1)
            self.base.append((phi.copy(), label))
            self.fast.append((residual.copy(), target))
            self.slow.append((residual.copy(), target))
            self.feedback += 1
            if self.feedback % self.base_interval == 0:
                x, y = zip(*self.base)
                self.weights = fit_base(x, y, self.weights)
            fast_x, fast_y = zip(*self.fast)
            if len(self.fast) >= self.warmup and self.feedback % self.krr_interval == 0:
                self.rfm.fit(fast_x, fast_y)
            if (len(self.fast) >= self.warmup and len(self.rfm.centers)
                    and self.feedback % self.agop_interval == 0):
                self.rfm.adapt([x for x, _ in self.slow], fast_x, fast_y)
            memory = self.bank[key]
            memory.utility = min(5., max(-2., memory.utility+(.25 if reward else -.45)))
            memory.hits += int(reward)
            memory.misses += int(not reward)
            memory.accesses += 1
            memory.last_access = self.t
        # Post-execution admission can use this completed task's public query
        # and reward; only the next begin() sees the resulting bank/model.
        reason = "no_successful_candidate"
        if new_memory:
            candidate = Memory(*new_memory, created=self.t)
            bank, reason = admission_decision(tuple(self.bank.values()), candidate,
                tuple(self.queries)+(query,), score=self.score, capacity=self.capacity, dimension=self.dimension)
            self.bank = {memory.key: memory for memory in bank}
        if key is not None:
            self.queries.append(query)
        self.pending = None
        self.t += 1
        return reason
