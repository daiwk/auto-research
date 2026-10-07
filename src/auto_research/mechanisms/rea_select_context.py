"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def rea_select_context(instructions, episodes, relevance, *, episode_budget: int):
    """Keep persistent instructions and retrieve only useful episodic turns."""
    import torch

    if len(episodes) != len(relevance) or episode_budget < 0:
        raise ValueError("invalid episodic inputs")
    count = min(episode_budget, len(episodes))
    selected = torch.topk(torch.as_tensor(relevance), count).indices.tolist() if count else []
    return tuple(instructions), tuple(episodes[index] for index in selected)
