"""B3 self-calibrating spawn gate; no pretrained diffusion model or speed claim."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

REQUIRES_GPU_VALIDATION = False


def entropy(probabilities: np.ndarray) -> np.ndarray:
    values = np.asarray(probabilities, dtype=float)
    if (values.ndim != 2 or not np.isfinite(values).all() or np.any(values < 0)
            or not np.allclose(values.sum(-1), 1)):
        raise ValueError("finite normalized token distributions required")
    logs = np.zeros_like(values)
    np.log(values, out=logs, where=values > 0)
    return -(values * logs).sum(-1)


def block_causal_mask(block_size: int) -> np.ndarray:
    if type(block_size) is not int or block_size < 1:
        raise ValueError("positive integer block size required")
    positions = np.arange(2 * block_size)
    return positions[:, None] // block_size >= positions[None, :] // block_size


@dataclass
class SpawnGate:
    """Candidates carry across blocks, but never use current-pass entropy retroactively."""

    frontier: int = -1
    candidates: list[float] = field(default_factory=list)
    previous_entropy: np.ndarray | None = None
    block_start: int | None = None

    def observe(self, token_entropy: np.ndarray, accepted_positions: np.ndarray, *,
                block_start: int, future_active: bool = False, predicts_eos: bool = False) -> bool:
        h = np.asarray(token_entropy, dtype=float)
        accepted = np.asarray(accepted_positions)
        if (h.ndim != 1 or not len(h) or not np.isfinite(h).all() or np.any(h < 0)
                or accepted.shape != h.shape or accepted.dtype != np.bool_ or block_start < 0):
            raise ValueError("finite entropy, boolean acceptance and nonnegative block offset required")
        if self.block_start != block_start:
            self.previous_entropy = None
            self.block_start = block_start
        elif self.previous_entropy is not None and len(self.previous_entropy) != len(h):
            raise ValueError("block length cannot change within an active block")
        accepted_global = np.flatnonzero(accepted) + block_start
        frontier = max(self.frontier, int(accepted_global.max()) if accepted_global.size else -1)
        if (frontier > self.frontier and not future_active and self.previous_entropy is not None):
            left_count = min(len(h), frontier - block_start)
            if left_count > 0:
                self.candidates.append(float(self.previous_entropy[:left_count].max()))
        self.frontier = frontier
        self.previous_entropy = h.copy()
        return bool(self.candidates and not future_active and not predicts_eos
                    and h.max() <= np.mean(self.candidates))


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("B3 gate reference is CPU-only, not a CUDA denoiser")
    rng = np.random.default_rng(seed)
    gate = SpawnGate()
    first = 1.5 + rng.random(4)
    gate.observe(first, np.array([True, False, False, False]), block_start=0)
    second = np.full(4, 0.2)
    opened = gate.observe(second, np.array([True, True, False, False]), block_start=0)
    lagged = gate.candidates == [float(first[0])]
    count = len(gate.candidates)
    active = gate.observe(np.full(4, 0.1), np.ones(4, dtype=bool), block_start=0, future_active=True)
    excluded_active = len(gate.candidates) == count
    eos = gate.observe(np.full(4, 0.1), np.ones(4, dtype=bool), block_start=0, predicts_eos=True)
    gate.observe(np.full(4, 0.1), np.zeros(4, dtype=bool), block_start=4)
    mask = block_causal_mask(4)
    q, k, v = (rng.normal(size=(8, 6)) for _ in range(3))
    scores = q @ k.T / np.sqrt(6)
    scores[~mask] = -np.inf
    weights = np.exp(scores - scores.max(-1, keepdims=True))
    shared = weights / weights.sum(-1, keepdims=True) @ v
    current_scores = q[:4] @ k[:4].T / np.sqrt(6)
    current_weights = np.exp(current_scores - current_scores.max(-1, keepdims=True))
    vanilla = current_weights / current_weights.sum(-1, keepdims=True) @ v[:4]
    error = float(np.max(np.abs(shared[:4] - vanilla)))
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"candidate_count": len(gate.candidates), "calibrated_threshold": float(np.mean(gate.candidates)),
                        "current_block_attention_error": error},
            "checks": {"one_pass_lag": lagged, "gate_opens": opened, "eos_suppresses_spawn": not eos,
                       "active_future_excluded": excluded_active and not active,
                       "threshold_carries_across_blocks": len(gate.candidates) == count,
                       "future_cannot_change_current_attention": error < 1e-12}}
