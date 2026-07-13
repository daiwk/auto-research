from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Candidate:
    name: str
    optimizer: str
    gated: bool
    multi_objective_reward: bool


CANDIDATES = (
    Candidate("human_adagrad", "adagrad", False, False),
    Candidate("agent_rmsprop", "rmsprop", False, False),
    Candidate("agent_rmsprop_glu", "rmsprop", True, False),
    Candidate("agent_rmsprop_glu_multi_reward", "rmsprop", True, True),
)


class EvolvingModel:
    def __init__(self, items: int, factors: int, seed: int, candidate: Candidate):
        rng = np.random.default_rng(seed)
        scale = 0.08 / math.sqrt(factors)
        self.context = rng.normal(0, scale, (items, factors))
        self.item = rng.normal(0, scale, (items, factors))
        self.gate = np.zeros(factors)
        self.candidate = candidate
        self.context_acc = np.zeros_like(self.context)
        self.item_acc = np.zeros_like(self.item)
        self.gate_acc = np.zeros_like(self.gate)

    def _gating(self) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-self.gate)) if self.candidate.gated else np.ones_like(self.gate)

    def scores(self, previous: int, candidates: np.ndarray) -> np.ndarray:
        return self.item[candidates] @ (self.context[previous] * self._gating())

    def update(self, previous: int, positive: int, negative: int, weight: float) -> None:
        user = self.context[previous].copy()
        pos = self.item[positive].copy()
        neg = self.item[negative].copy()
        gate = self._gating()
        representation = user * gate
        diff = float(representation @ (pos - neg))
        coefficient = weight / (1.0 + math.exp(min(30.0, diff)))
        reg = 0.002
        user_grad = coefficient * (pos - neg) * gate - reg * user
        pos_grad = coefficient * representation - reg * pos
        neg_grad = -coefficient * representation - reg * neg
        self._apply(self.context, self.context_acc, previous, user_grad)
        self._apply(self.item, self.item_acc, positive, pos_grad)
        self._apply(self.item, self.item_acc, negative, neg_grad)
        if self.candidate.gated:
            gate_grad = coefficient * user * (pos - neg) * gate * (1.0 - gate) - reg * self.gate
            self._apply_dense(self.gate, self.gate_acc, gate_grad)

    def _apply(self, parameter, accumulator, index: int, gradient: np.ndarray) -> None:
        if self.candidate.optimizer == "rmsprop":
            accumulator[index] = 0.95 * accumulator[index] + 0.05 * gradient**2
        else:
            accumulator[index] += gradient**2
        parameter[index] += 0.015 * gradient / np.sqrt(accumulator[index] + 1e-6)

    def _apply_dense(self, parameter, accumulator, gradient: np.ndarray) -> None:
        if self.candidate.optimizer == "rmsprop":
            accumulator[:] = 0.95 * accumulator + 0.05 * gradient**2
        else:
            accumulator[:] += gradient**2
        parameter += 0.015 * gradient / np.sqrt(accumulator + 1e-6)


def train_candidate(data, candidate: Candidate, seed: int, factors: int = 20, epochs: int = 3):
    rng = np.random.default_rng(seed)
    model = EvolvingModel(data.item_count, factors, seed, candidate)
    examples = []
    for sequence in data.train:
        denominator = max(1, len(sequence) - 1)
        for index, (previous, positive) in enumerate(zip(sequence, sequence[1:])):
            reward = 0.6 + 0.8 * (index / denominator) if candidate.multi_objective_reward else 1.0
            examples.append((previous, positive, reward))
    examples = np.asarray(examples, dtype=np.float64)
    for _ in range(epochs):
        rng.shuffle(examples)
        for previous, positive, reward in examples:
            negative = int(rng.integers(data.item_count))
            if negative == int(positive):
                negative = (negative + 1) % data.item_count
            model.update(int(previous), int(positive), negative, float(reward))
    return model
