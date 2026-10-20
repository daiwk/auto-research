"""Kronecker Delta Rule and a tiny KronLSTM mixer (arXiv:2610.26834).

The implementation is recurrent PyTorch, not the paper's fused chunk kernel.
It preserves scalar association erasure, decoupled writing and key-axis decay.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def kronecker_update(state: Tensor, key: Tensor, value: Tensor, beta: Tensor,
                     write: Tensor, forget: Tensor) -> Tensor:
    """Eq.10: S F - beta (v^T S F k) v k^T + c v k^T."""
    if state.shape[-2:] != (value.shape[-1], key.shape[-1]) or forget.shape != key.shape:
        raise ValueError("memory/value/key/forget shape mismatch")
    if state.shape[:-2] != key.shape[:-1] or value.shape[:-1] != key.shape[:-1]:
        raise ValueError("batch/head dimensions must agree")
    if beta.shape != key.shape[:-1] or write.shape != beta.shape:
        raise ValueError("erase/write are scalar per head")
    if any(not torch.isfinite(t).all() for t in (state, key, value, beta, write, forget)):
        raise ValueError("finite recurrence inputs required")
    if ((forget < 0) | (forget > 1)).any() or ((beta < 0) | (beta > 1)).any() or ((write < 0) | (write > 1)).any():
        raise ValueError("gates must be in [0,1]")
    decayed = state * forget.unsqueeze(-2)
    association = torch.einsum("...v,...vk,...k->...", value, decayed, key)
    outer = value.unsqueeze(-1) * key.unsqueeze(-2)
    return decayed + (write - beta * association)[..., None, None] * outer


def recurrent_memory(query: Tensor, key: Tensor, value: Tensor, beta: Tensor,
                     write: Tensor, forget: Tensor, initial: Tensor | None = None) -> tuple[Tensor, Tensor]:
    """Inputs [B,H,T,D], scalar gates [B,H,T]; inclusive causal readout."""
    if query.shape != key.shape or query.ndim != 4 or value.shape[:3] != key.shape[:3]:
        raise ValueError("[batch,head,time,channel] projections required")
    if beta.shape != key.shape[:3] or write.shape != beta.shape or forget.shape != key.shape:
        raise ValueError("sequence gate dimensions must agree")
    if query.shape[2] == 0 or not torch.isfinite(query).all():
        raise ValueError("nonempty sequences required")
    state = key.new_zeros(*key.shape[:2], value.shape[-1], key.shape[-1]) if initial is None else initial
    outputs = []
    for index in range(key.shape[2]):
        state = kronecker_update(state, key[:, :, index], value[:, :, index], beta[:, :, index],
                                 write[:, :, index], forget[:, :, index])
        outputs.append(torch.einsum("...vk,...k->...v", state, query[:, :, index]))
    return torch.stack(outputs, 2), state


class TinyKronLSTM(nn.Module):
    """Complete small Eq.10 mixer with short causal convs and learned gates.

    No FFN/language head or pretrained language-model capability is supplied.
    """
    def __init__(self, width: int = 12, heads: int = 2, key_dim: int = 3,
                 value_dim: int = 4, conv_size: int = 3):
        super().__init__()
        if min(width, heads, key_dim, value_dim, conv_size) < 1:
            raise ValueError("positive mixer dimensions required")
        self.heads, self.key_dim, self.value_dim, self.conv_size = heads, key_dim, value_dim, conv_size
        self.query = nn.Linear(width, heads * key_dim)
        self.key = nn.Linear(width, heads * key_dim)
        self.value = nn.Linear(width, heads * value_dim)
        self.convs = nn.ModuleList(nn.Conv1d(heads * dim, heads * dim, conv_size, groups=heads * dim)
                                   for dim in (key_dim, key_dim, value_dim))
        self.erase = nn.Linear(width, heads)
        self.write = nn.Linear(width, heads)
        self.forget = nn.Linear(width, heads * key_dim)
        self.a_log = nn.Parameter(torch.zeros(heads))
        self.output_gate = nn.Linear(width, heads * value_dim)
        self.rms_weight = nn.Parameter(torch.ones(heads, value_dim))
        self.output = nn.Linear(heads * value_dim, width)

    def forward(self, x: Tensor, initial: Tensor | None = None) -> tuple[Tensor, Tensor, dict[str, Tensor]]:
        if x.ndim != 3:
            raise ValueError("[batch,time,width] input required")
        batch, length, _ = x.shape
        projections = []
        for projection, conv, dim in zip((self.query, self.key, self.value), self.convs,
                                          (self.key_dim, self.key_dim, self.value_dim), strict=True):
            raw = projection(x).transpose(1, 2)
            filtered = F.silu(conv(F.pad(raw, (self.conv_size - 1, 0)))).transpose(1, 2)
            heads = filtered.reshape(batch, length, self.heads, dim).transpose(1, 2)
            projections.append(F.normalize(heads, dim=-1))
        query, key, value = projections
        beta = self.erase(x).sigmoid().transpose(1, 2)
        write = self.write(x).sigmoid().transpose(1, 2)
        sf = self.forget(x).reshape(batch, length, self.heads, self.key_dim).transpose(1, 2)
        forget = torch.exp(-F.softplus(sf) * self.a_log.exp()[None, :, None, None])
        read, state = recurrent_memory(query, key, value, beta, write, forget, initial)
        gate = self.output_gate(x).sigmoid().reshape(batch, length, self.heads, self.value_dim).transpose(1, 2)
        gated = gate * read
        normalized = gated * torch.rsqrt(gated.square().mean(-1, keepdim=True) + 1e-6) * self.rms_weight[None, :, None]
        output = self.output(normalized.transpose(1, 2).reshape(batch, length, -1))
        return output, state, dict(query=query, key=key, value=value, beta=beta, write=write, forget=forget, read=read)
