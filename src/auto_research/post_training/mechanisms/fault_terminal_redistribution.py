"""Extracted unchanged from auto_research.post_training.latest_20261002; stable mechanism boundary."""
from __future__ import annotations



def fault_terminal_redistribution(
    terminal_rewards,
    diagnoses,
    error_costs,
    *,
    maximum_penalty: float = 0.8,
):
    """FAULT terminal-anchored, conserved credit redistribution.

    Diagnosed error claims are used only when ``verified``.  Their learned
    costs form localization weights; total redistributed credit is conserved
    for each trajectory and the terminal ordering is retained.
    """
    import torch

    rewards = torch.as_tensor(terminal_rewards, dtype=torch.float32)
    if not 0 <= maximum_penalty < 1:
        raise ValueError("maximum_penalty must be in [0, 1)")
    rows = []
    coverage = []
    for terminal, claims in zip(rewards, diagnoses):
        length = max((int(item["step"]) for item in claims), default=0) + 1
        weights = torch.zeros(length, dtype=rewards.dtype)
        for claim in claims:
            if claim.get("verified", False):
                weights[int(claim["step"])] += float(error_costs[claim["category"]])
        if float(weights.sum()) > 0:
            normalized = weights / weights.sum()
            penalty = maximum_penalty * normalized
            redistributed = terminal * (1.0 / length + penalty.mean() - penalty)
            coverage.append(True)
        else:
            redistributed = terminal.expand(length) / length
            coverage.append(False)
        # Numerical guard: preserve the terminal total exactly.
        redistributed[-1] += terminal - redistributed.sum()
        rows.append(redistributed)
    return rows, {"signal_coverage": sum(coverage) / max(len(coverage), 1)}
