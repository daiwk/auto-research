"""Snapshot intervention and structured advantages from arXiv:2610.20293.

This CPU component implements equations 4, 7 and 11--15.  The caller supplies
the frozen set evaluator; no evaluator result is a claim of production value.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Callable, Sequence

import numpy as np


@dataclass(frozen=True)
class Candidate:
    key: str
    rank_score: float
    value: float

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key:
            raise ValueError("candidate requires a nonempty string identity")
        if not math.isfinite(self.rank_score) or not math.isfinite(self.value):
            raise ValueError("candidate scores must be finite")


@dataclass(frozen=True)
class RetrievalSnapshot:
    actions: tuple[str, ...]
    results: tuple[tuple[Candidate, ...], ...]

    def __post_init__(self):
        if not 1 <= len(self.actions) <= 16 or len(self.actions) != len(self.results):
            raise ValueError("snapshot needs 1..16 actions with aligned cached results")
        if any(not isinstance(x, str) or not x for x in self.actions) or len(set(self.actions)) != len(self.actions):
            raise ValueError("action identities must be unique and nonempty")
        if not isinstance(self.actions, tuple) or not isinstance(self.results, tuple):
            raise ValueError("snapshot containers must be immutable tuples")
        seen: dict[str, Candidate] = {}
        for row in self.results:
            if not isinstance(row, tuple) or any(not isinstance(c, Candidate) for c in row):
                raise ValueError("cached candidates must be immutable Candidate tuples")
            if len({c.key for c in row}) != len(row):
                raise ValueError("one action retrieved the same candidate twice")
            for candidate in row:
                previous = seen.setdefault(candidate.key, candidate)
                if previous != candidate:
                    raise ValueError("a shared candidate changed within the frozen snapshot")

    @classmethod
    def capture(cls, actions: Sequence[str], retrieve: Callable[[str], Sequence[Candidate]]):
        identities = tuple(actions)
        if (not 1 <= len(identities) <= 16
                or any(not isinstance(x, str) or not x for x in identities)
                or len(set(identities)) != len(identities)):
            raise ValueError("capture needs distinct nonempty action identities")
        # Exactly one retrieval per realized action, before any coalition score.
        return cls(identities, tuple(tuple(retrieve(action)) for action in identities))

    @property
    def sha256(self) -> str:
        payload = {"actions": self.actions, "results": [
            [(c.key, c.rank_score, c.value) for c in row] for row in self.results
        ]}
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

    def merge(self, mask: int) -> tuple[Candidate, ...]:
        if not isinstance(mask, int) or not 0 <= mask < 1 << len(self.actions):
            raise ValueError("coalition mask outside snapshot")
        candidates = {c.key: c for i, row in enumerate(self.results)
                      if mask & (1 << i) for c in row}
        return tuple(candidates[key] for key in sorted(candidates))


class CachedCoalitionEvaluator:
    """Memoize evaluations while keeping retrieval and scoring roles separate."""

    def __init__(self, snapshot: RetrievalSnapshot,
                 evaluate: Callable[[tuple[Candidate, ...]], float]):
        self.snapshot = snapshot
        self.evaluate = evaluate
        self.cache: dict[int, float] = {0: 0.0}
        self.calls = 0

    def value(self, mask: int) -> float:
        # merge validates even a cached request.  The empty set is never scored.
        candidates = self.snapshot.merge(mask)
        if mask not in self.cache:
            value = float(self.evaluate(candidates))
            if not math.isfinite(value):
                raise ValueError("frozen evaluator returned a non-finite value")
            self.cache[mask] = value
            self.calls += 1
        return self.cache[mask]

    def exact_values(self, *, max_actions: int = 8) -> np.ndarray:
        if not 1 <= max_actions <= 12 or len(self.snapshot.actions) > max_actions:
            raise ValueError("exact enumeration exceeds the explicit affordable action cap")
        return np.array([self.value(mask) for mask in range(1 << len(self.snapshot.actions))])


def credit_rules(values: Sequence[float]) -> dict[str, np.ndarray]:
    """Exact Shapley plus the paper's Singleton/LOO endpoint controls."""
    v = np.asarray(values, dtype=np.float64)
    if v.ndim != 1 or len(v) < 2 or len(v) & (len(v) - 1):
        raise ValueError("coalition table must have power-of-two length >=2")
    if not np.isfinite(v).all() or v[0] != 0:
        raise ValueError("coalition values must be finite, with v(empty)=0")
    m = (len(v) - 1).bit_length()
    if m > 12:
        raise ValueError("exact credit computation exceeds the bounded component budget")
    shapley = np.zeros(m)
    for i in range(m):
        bit = 1 << i
        for mask in range(len(v)):
            if mask & bit:
                continue
            size = mask.bit_count()
            weight = 1.0 / (m * math.comb(m - 1, size))
            shapley[i] += weight * (v[mask | bit] - v[mask])
    full = len(v) - 1
    return {"shapley": shapley, "singleton": np.array([v[1 << i] for i in range(m)]),
            "loo": np.array([v[full] - v[full ^ (1 << i)] for i in range(m)])}


def permutation_credit(evaluator: CachedCoalitionEvaluator, *, permutations: int,
                       seed: int) -> np.ndarray:
    if not isinstance(permutations, int) or not 1 <= permutations <= 4096:
        raise ValueError("permutations must be an integer within 1..4096")
    m = len(evaluator.snapshot.actions)
    rng = np.random.default_rng(seed)
    credit = np.zeros(m)
    for _ in range(permutations):
        mask = 0
        value = 0.0
        for i in rng.permutation(m):
            next_mask = mask | (1 << int(i))
            next_value = evaluator.value(next_mask)
            credit[i] += next_value - value
            mask, value = next_mask, next_value
    return credit / permutations


def bounded_zero_sum(vector: Sequence[float], *, kappa: float) -> np.ndarray:
    """Euclidean box-plus-hyperplane projection (paper equation 13)."""
    u = np.asarray(vector, dtype=np.float64)
    if u.ndim != 1 or not len(u) or not np.isfinite(u).all():
        raise ValueError("projection needs a finite nonempty vector")
    if not math.isfinite(kappa) or kappa <= 0:
        raise ValueError("kappa must be finite and positive")
    low, high = float(u.min() - kappa), float(u.max() + kappa)
    for _ in range(100):
        middle = low / 2 + high / 2
        z = np.clip(u - middle, -kappa, kappa)
        if z.sum() > 0:
            low = middle
        else:
            high = middle
    return np.clip(u - (low / 2 + high / 2), -kappa, kappa)


def shape_advantages(credits, rollout_advantages, *, beta: float = 0.2,
                     kappa: float = 1.0, epsilon: float = 1e-8) -> dict:
    c, base = np.asarray(credits, dtype=np.float64), np.asarray(rollout_advantages, dtype=np.float64)
    if c.ndim != 2 or not all(c.shape) or base.shape != (len(c),):
        raise ValueError("credits must be [rollout, action], aligned with rollout advantages")
    if not np.isfinite(c).all() or not np.isfinite(base).all():
        raise ValueError("advantages and credits must be finite")
    if not math.isfinite(beta) or beta < 0 or not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("beta must be nonnegative and epsilon positive")
    centered = c - c.mean(axis=1, keepdims=True)
    # Population std over every centered action in the *whole rollout group*.
    scale = float(centered.std(ddof=0))
    offsets = np.stack([bounded_zero_sum(row / (scale + epsilon), kappa=kappa)
                        for row in centered])
    return {"advantages": base[:, None] + beta * offsets,
            "offsets": offsets, "group_std": scale}


def token_advantages(action_advantages, rollout_advantages, action_ids, *, mask=None):
    action, base, spans = (np.asarray(x) for x in
                           (action_advantages, rollout_advantages, action_ids))
    if action.ndim != 2 or base.shape != (len(action),) or spans.ndim != 2 or len(spans) != len(action):
        raise ValueError("unaligned action, rollout or token arrays")
    if not np.issubdtype(spans.dtype, np.integer) or (spans < -1).any() or (spans >= action.shape[1]).any():
        raise ValueError("token owner must be -1 (shared) or a valid action index")
    if not np.isfinite(action).all() or not np.isfinite(base).all():
        raise ValueError("non-finite advantage")
    result = np.broadcast_to(base[:, None], spans.shape).astype(np.float64, copy=True)
    for row in range(len(spans)):
        owned = spans[row] >= 0
        result[row, owned] = action[row, spans[row, owned]]
    if mask is not None:
        mask = np.asarray(mask)
        if mask.shape != spans.shape or not np.isin(mask, (0, 1)).all():
            raise ValueError("token mask must be aligned and binary")
        result *= mask
    return result
