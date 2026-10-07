"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def llm2jev_distribution(option_log_probs, *, temperature: float = 1.0):
    """Turn bracketed-option token likelihoods into a Jev distribution."""
    import torch

    if temperature <= 0 or option_log_probs.ndim != 2:
        raise ValueError("option_log_probs must be [options, option_tokens]")
    return torch.softmax(option_log_probs.sum(-1) / temperature, dim=0)
