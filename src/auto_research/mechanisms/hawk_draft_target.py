"""Extracted unchanged from auto_research.foundation_latest_20261003; stable mechanism boundary."""
from __future__ import annotations



def hawk_draft_target(target_hidden_states, layer_weights, shifted_target_logits):
    """Mix informative target layers and expose shifted-trajectory supervision."""
    import torch

    weights = torch.softmax(layer_weights, dim=0)
    hidden = sum(weights[index] * state for index, state in enumerate(target_hidden_states))
    return hidden, shifted_target_logits.detach()
