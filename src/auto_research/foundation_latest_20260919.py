"""Reference kernels for the 2026-09-19 foundation-model batch."""

from __future__ import annotations

import numpy as np


def fit_recall_head(local_states, global_gain, ridge: float = 1e-3):
    x = np.asarray(local_states, dtype=np.float64)
    y = np.asarray(global_gain, dtype=np.float64)
    return np.linalg.solve(x.T @ x + ridge * np.eye(x.shape[1]), x.T @ y)


def on_demand_attention(query, local_keys, local_values, global_keys, global_values, recall_head, threshold=0.0):
    query = np.asarray(query, dtype=np.float64)
    def attend(keys, values):
        scores = np.asarray(keys) @ query / np.sqrt(query.size)
        weights = np.exp(scores - scores.max()); weights /= weights.sum()
        return weights @ np.asarray(values)
    local = attend(local_keys, local_values)
    predicted_gain = float(local @ np.asarray(recall_head))
    used_global = predicted_gain > threshold
    output = attend(global_keys, global_values) if used_global else local
    return output, {"predicted_global_gain": predicted_gain, "global_attention_used": used_global, "kv_retained": len(global_keys)}


def dqwen35_hybrid(hidden, recurrent_matrix, attention_matrix, mask_ratio=0.3):
    x = np.asarray(hidden, dtype=np.float64)
    forward = np.zeros_like(x); backward = np.zeros_like(x)
    for index in range(len(x)):
        forward[index] = np.tanh(x[index] + (forward[index - 1] @ recurrent_matrix if index else 0))
    for index in range(len(x) - 1, -1, -1):
        backward[index] = np.tanh(x[index] + (backward[index + 1] @ recurrent_matrix if index + 1 < len(x) else 0))
    attention = x @ attention_matrix
    output = (1 - mask_ratio) * (forward + backward) / 2 + mask_ratio * attention
    return output, {"bidirectional_passes": 2, "mask_ratio": float(mask_ratio), "hybrid_state_norm": float(np.linalg.norm(output))}


def aspire_schedule(acceptance, draft_cost, verify_cost, batch_sizes, refresh_interval=4):
    acceptance = np.asarray(acceptance, dtype=np.float64)
    batch = np.asarray(batch_sizes, dtype=np.float64)
    speculative_gain = acceptance * verify_cost - draft_cost * (1 + 0.1 * batch)
    draft_lengths = np.maximum(1, np.floor(1 + 7 * np.clip(speculative_gain / max(verify_cost, 1e-8), 0, 1))).astype(int)
    refresh = np.arange(len(draft_lengths)) % refresh_interval == 0
    return draft_lengths, refresh, {"mean_draft_length": float(draft_lengths.mean()), "refresh_fraction": float(refresh.mean()), "positive_gain_fraction": float((speculative_gain > 0).mean())}


def oda_cuda_kernel(query, local_keys, local_values, global_keys, global_values, recall_head, threshold=0.0):
    import torch
    if any(t.device.type != "cuda" for t in (query, local_keys, local_values, global_keys, global_values, recall_head)):
        raise ValueError("oda_cuda_kernel requires CUDA tensors")
    local_weights = torch.softmax(local_keys @ query / query.numel() ** 0.5, dim=0)
    local = local_weights @ local_values
    gate = (local @ recall_head) > threshold
    global_output = torch.softmax(global_keys @ query / query.numel() ** 0.5, dim=0) @ global_values
    return torch.where(gate, global_output, local), gate


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


def aspire_cuda_kernel(acceptance, draft_cost, verify_cost, batch_sizes, refresh_interval=4):
    import torch
    if any(t.device.type != "cuda" for t in (acceptance, batch_sizes)):
        raise ValueError("aspire_cuda_kernel requires CUDA tensors")
    gain = acceptance * verify_cost - draft_cost * (1 + 0.1 * batch_sizes)
    lengths = torch.clamp(torch.floor(1 + 7 * torch.clamp(gain / verify_cost, 0, 1)), min=1).long()
    refresh = torch.arange(len(lengths), device=lengths.device) % refresh_interval == 0
    return lengths, refresh
