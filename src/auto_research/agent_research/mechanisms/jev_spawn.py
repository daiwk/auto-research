"""Extracted unchanged from auto_research.agent_research.latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def jev_spawn(probabilities, actions, feedback, *, branches: int):
    """Spawn finite actions, revise their probabilities and retain alternatives."""
    import torch

    posterior = probabilities * torch.exp(torch.as_tensor(feedback, dtype=probabilities.dtype))
    posterior = posterior / posterior.sum().clamp_min(1e-12)
    indices = torch.topk(posterior, min(branches, len(actions))).indices.tolist()
    return tuple(actions[index] for index in indices), posterior
