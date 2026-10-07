"""Extracted unchanged from auto_research.recommendation_latest_20261001; stable mechanism boundary."""
from __future__ import annotations



def recap_recursive_routes(features, shared_block, *, routes: int, ema_decay: float):
    """Weight-shared recursive routes, inference averaging and trajectory EMA."""
    import torch

    if routes < 1 or not 0 <= ema_decay < 1:
        raise ValueError("invalid RECAP recursion configuration")
    hidden = features
    outputs = []
    ema = None
    for _ in range(routes):
        hidden = shared_block(hidden)
        outputs.append(hidden)
        ema = hidden.detach() if ema is None else ema_decay * ema + (1 - ema_decay) * hidden.detach()
    stacked = torch.stack(outputs, dim=0)
    return stacked.mean(0), {"routes": stacked, "trajectory_ema": ema}
