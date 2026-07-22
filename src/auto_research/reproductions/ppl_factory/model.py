from __future__ import annotations

import numpy as np


def budget_aware_mode(ratio: float) -> str:
    if ratio <= 0.02:
        return "mid_random"
    if ratio <= 0.20:
        return "middle"
    return "easy"


def select_blocks(scores: np.ndarray, ratio: float, seed: int, mode: str | None = None) -> np.ndarray:
    """Algorithm 1: task-aware NLL followed by a budget-aware rule."""
    mode = mode or budget_aware_mode(ratio)
    count = max(1, int(len(scores) * ratio))
    rng = np.random.default_rng(seed)
    if mode == "random":
        return np.sort(rng.choice(len(scores), count, replace=False))
    if mode == "easy":
        return np.argsort(scores)[:count]
    if mode == "hard":
        return np.argsort(scores)[-count:]
    distance = np.abs(scores - np.median(scores))
    if mode == "middle":
        return np.argsort(distance)[:count]
    if mode == "mid_random":
        pool_count = min(len(scores), max(count, count * 4))
        pool = np.argsort(distance)[:pool_count]
        return np.sort(rng.choice(pool, count, replace=False))
    raise ValueError(f"unknown selection mode: {mode}")


def score_blocks(model, tokens: np.ndarray, block_size: int, torch) -> tuple[np.ndarray, np.ndarray]:
    usable = len(tokens) // block_size * block_size
    blocks = tokens[:usable].reshape(-1, block_size)
    device = next(model.parameters()).device
    model.eval()
    scores = []
    with torch.inference_mode():
        for start in range(0, len(blocks), 32):
            batch = torch.tensor(blocks[start:start + 32], dtype=torch.long, device=device)
            logits = model(batch[:, :-1])
            loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, logits.shape[-1]), batch[:, 1:].reshape(-1), reduction="none",
            ).reshape(len(batch), -1).mean(-1)
            scores.extend(loss.cpu().tolist())
    return blocks, np.asarray(scores)
