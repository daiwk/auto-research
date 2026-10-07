"""Extracted unchanged from auto_research.foundation_latest_20260919; stable mechanism boundary."""
from __future__ import annotations



def dqwen35_cuda_kernel(hidden, recurrent_matrix, attention_matrix, mask_ratio=0.3):
    import torch
    if any(t.device.type != "cuda" for t in (hidden, recurrent_matrix, attention_matrix)):
        raise ValueError("dqwen35_cuda_kernel requires CUDA tensors")
    forward, state = [], torch.zeros_like(hidden[0])
    for token in hidden:
        state = torch.tanh(token + state @ recurrent_matrix); forward.append(state)
    backward, state = [], torch.zeros_like(hidden[0])
    for token in hidden.flip(0):
        state = torch.tanh(token + state @ recurrent_matrix); backward.append(state)
    recurrent = (torch.stack(forward) + torch.stack(backward[::-1])) / 2
    return (1 - mask_ratio) * recurrent + mask_ratio * hidden @ attention_matrix
