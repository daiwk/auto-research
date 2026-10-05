"""Follow the Winners (arXiv:2610.03361) elite filtering and projection.

This is the paper's critic-free update on a small CPU policy, not a reproduction
of its Qwen/Sokoban/Search-R1 experiments. The replay proposal, repeated
minibatch top-K selection, and regularized cross-entropy update are explicit.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass

import numpy as np
import torch
from torch import Tensor


@dataclass(frozen=True)
class Trajectory:
    action: int
    outcome: float


class FIFOReplay:
    def __init__(self, capacity: int):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._items: deque[Trajectory] = deque(maxlen=capacity)

    def append(self, trajectory: Trajectory) -> None:
        if not math.isfinite(trajectory.outcome):
            raise ValueError("trajectory outcome must be finite")
        self._items.append(trajectory)

    def snapshot(self) -> tuple[Trajectory, ...]:
        return tuple(self._items)


def elite_indices(
    outcomes: np.ndarray,
    *,
    batch_size: int,
    winners: int,
    batches: int,
    rng: np.random.Generator,
) -> list[int]:
    """Draw J uniform no-replacement minibatches; retain top K in each.

    Repeated selection of the same replay item across independent minibatches
    is intentional: it gives that trajectory proportionally more CE weight.
    Equal-return ties are broken by the random minibatch sampling order.
    """
    values = np.asarray(outcomes, dtype=np.float64)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("outcomes must be a finite vector")
    if not (1 <= winners <= batch_size <= len(values)) or batches < 1:
        raise ValueError("require 1 <= winners <= batch_size <= buffer and batches >= 1")
    chosen: list[int] = []
    for _ in range(batches):
        sampled = rng.choice(len(values), size=batch_size, replace=False)
        order = np.argsort(-values[sampled], kind="stable")
        chosen.extend(int(index) for index in sampled[order[:winners]])
    return chosen


def rank_occupancy(*, buffer_size: int, batch_size: int, winners: int, rank: int) -> float:
    """Paper Eq. 5: normalized marginal mass for one-based buffer rank."""
    if not (1 <= rank <= buffer_size and 1 <= winners <= batch_size <= buffer_size):
        raise ValueError("invalid rank, batch, or buffer size")
    count = sum(
        math.comb(rank - 1, k - 1) * math.comb(buffer_size - rank, batch_size - k)
        for k in range(1, winners + 1)
        if k - 1 <= rank - 1 and 0 <= batch_size - k <= buffer_size - rank
    )
    return count / (winners * math.comb(buffer_size, batch_size))


def projection_loss(
    logits: Tensor,
    elite_actions: Tensor,
    reference_probs: Tensor,
    *,
    kl_weight: float,
) -> Tensor:
    """Cross-entropy projection of sampled elites plus policy/reference KL."""
    if logits.ndim != 1 or reference_probs.shape != logits.shape:
        raise ValueError("policy and reference must be vocabulary vectors")
    if elite_actions.ndim != 1 or not elite_actions.numel():
        raise ValueError("at least one elite action is required")
    if elite_actions.dtype != torch.long or bool(((elite_actions < 0) | (elite_actions >= logits.numel())).any()):
        raise ValueError("elite actions must be valid integer indices")
    if kl_weight < 0 or not math.isfinite(kl_weight):
        raise ValueError("kl_weight must be finite and nonnegative")
    if not bool(torch.isfinite(logits).all() and torch.isfinite(reference_probs).all()):
        raise ValueError("policy/reference must be finite")
    if bool((reference_probs <= 0).any()) or not torch.allclose(
        reference_probs.sum(), reference_probs.new_tensor(1.0), atol=1e-6
    ):
        raise ValueError("reference_probs must be strictly positive and sum to one")
    log_probs = logits.log_softmax(dim=0)
    probs = log_probs.exp()
    cross_entropy = -log_probs[elite_actions].mean()
    kl = (probs * (log_probs - reference_probs.log())).sum()
    return cross_entropy + kl_weight * kl


def run_bandit(seed: int, *, iterations: int = 240) -> dict[str, float | int]:
    """One-step, public-free L1 diagnostic of the complete FTW update path."""
    if iterations < 1:
        raise ValueError("iterations must be positive")
    rng = np.random.default_rng(seed)
    torch.manual_seed(seed)
    logits = torch.zeros(2, dtype=torch.float64, requires_grad=True)
    reference = torch.full((2,), 0.5, dtype=torch.float64)
    optimizer = torch.optim.SGD([logits], lr=0.08)
    replay = FIFOReplay(128)
    for _ in range(iterations):
        probabilities = logits.detach().softmax(dim=0).numpy()
        action = int(rng.choice(2, p=probabilities))
        # Continuous one-step rewards avoid presenting tied binary scores as
        # evidence of an LLM-agent capability result.
        outcome = float((1.0 if action == 0 else 0.3) + rng.normal(0, 0.2))
        replay.append(Trajectory(action, outcome))
        items = replay.snapshot()
        if len(items) < 5:
            continue
        selected = elite_indices(
            np.array([item.outcome for item in items]),
            batch_size=5, winners=1, batches=4, rng=rng,
        )
        actions = torch.tensor([items[index].action for index in selected], dtype=torch.long)
        optimizer.zero_grad()
        projection_loss(logits, actions, reference, kl_weight=0.05).backward()
        optimizer.step()
    best_action_probability = float(logits.detach().softmax(dim=0)[0])
    return {
        "seed": seed,
        "iterations": iterations,
        "best_action_probability_initial": 0.5,
        "best_action_probability_final": best_action_probability,
        "expected_reward_initial": 0.65,
        "expected_reward_final": 0.3 + 0.7 * best_action_probability,
    }
