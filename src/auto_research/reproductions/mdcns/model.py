from __future__ import annotations

import math

import numpy as np


class SequentialModel:
    def __init__(self, context: np.ndarray, item: np.ndarray):
        self.context = context
        self.item = item

    @classmethod
    def create(cls, items: int, factors: int, seed: int) -> "SequentialModel":
        rng = np.random.default_rng(seed)
        scale = 0.08 / math.sqrt(factors)
        return cls(
            rng.normal(0, scale, (items, factors)),
            rng.normal(0, scale, (items, factors)),
        )

    def scores(self, previous: int, candidates: np.ndarray) -> np.ndarray:
        return self.item[candidates] @ self.context[previous]

    def bpr_update(
        self,
        previous: int,
        positive: int,
        negative: int,
        lr: float,
        reg: float,
        weight: float = 1.0,
    ) -> None:
        context = self.context[previous].copy()
        pos = self.item[positive].copy()
        neg = self.item[negative].copy()
        diff = float(context @ (pos - neg))
        gradient = weight / (1.0 + math.exp(min(30.0, diff)))
        self.context[previous] += lr * (gradient * (pos - neg) - reg * context)
        self.item[positive] += lr * (gradient * context - reg * pos)
        self.item[negative] += lr * (-gradient * context - reg * neg)

    def distill(
        self,
        previous: int,
        candidates: np.ndarray,
        teacher: np.ndarray,
        lr: float,
        gamma: float,
    ) -> None:
        logits = self.scores(previous, candidates)
        student = softmax(logits)
        grad = gamma * (student - teacher)
        context = self.context[previous].copy()
        item_vectors = self.item[candidates].copy()
        self.context[previous] -= lr * (grad[:, None] * item_vectors).sum(axis=0)
        np.add.at(self.item, candidates, -lr * grad[:, None] * context)


def softmax(values: np.ndarray) -> np.ndarray:
    shifted = values - values.max()
    exp = np.exp(shifted)
    return exp / exp.sum()
