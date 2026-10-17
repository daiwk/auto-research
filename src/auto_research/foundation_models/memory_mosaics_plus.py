"""Small differentiable Memory Mosaics+ / two-stage memory operators (§3.2).

No pretrained model is represented here.  The future-valued associations are
causal because position t can only read i <= t-s, s >= 1.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def masked_average(logits: Tensor, values: Tensor, allowed: Tensor) -> Tensor:
    """Stable normalized kernel regression, with zero for an empty memory."""
    masked = logits.masked_fill(~allowed, -torch.inf)
    maximum = masked.amax(-1, keepdim=True)
    maximum = torch.where(torch.isfinite(maximum), maximum, torch.zeros_like(maximum))
    weights = (masked - maximum).exp()
    weights = weights / weights.sum(-1, keepdim=True).clamp_min(torch.finfo(weights.dtype).tiny)
    return weights @ values


class MemoryMosaicsPlus(nn.Module):
    """Shared Q/K Gaussian memory, local memory and separate task estimates.

    ``document_starts[b,t]`` is the current document's first token.  The two
    long-memory partitions have independent normalizers, not a pooled softmax.
    The default tiny skip/window differ from the paper's 64/256 for diagnosis.
    """
    def __init__(self, width: int = 16, heads: int = 4, skip: int = 1, window: int = 2):
        super().__init__()
        if width < 1 or heads < 1 or width % heads or skip < 1 or window < 1:
            raise ValueError("positive divisible dimensions and causal skip >= 1 required")
        self.heads, self.skip, self.window = heads, skip, window
        self.key = nn.Linear(width, width, bias=False)
        self.value = nn.Linear(width, width, bias=False)
        self.local_qkv = nn.Linear(width, 3 * width, bias=False)
        self.future_mix = nn.Parameter(torch.zeros(heads))
        self.beta = nn.Parameter(torch.zeros(heads, 3))
        self.gate = nn.Linear(width, heads)
        self.output = nn.Linear(width, width, bias=False)

    def components(self, x: Tensor, document_starts: Tensor) -> dict[str, Tensor]:
        if x.ndim != 3 or x.shape[1] < 2 or not bool(torch.isfinite(x).all()):
            raise ValueError("finite batch x time x width input, at least two tokens required")
        batch, length, width = x.shape
        positions = torch.arange(length, device=x.device)
        if (document_starts.shape != (batch, length) or document_starts.dtype != torch.long
                or document_starts.device != x.device or bool((document_starts < 0).any())
                or bool((document_starts > positions).any())
                or bool((document_starts[:, 1:] < document_starts[:, :-1]).any())
                or bool(((document_starts[:, 1:] != document_starts[:, :-1])
                         & (document_starts[:, 1:] != positions[1:])).any())):
            raise ValueError("document starts must be valid causal integer boundaries")
        split = lambda a: a.reshape(batch, length, self.heads, width // self.heads).transpose(1, 2)
        q, k, v = self.local_qkv(x).chunk(3, -1)
        q, k, v = split(q), split(k), split(v)
        local_mask = ((positions[None, :] <= positions[:, None])
                      & (positions[None, :] > positions[:, None] - self.window))
        local = masked_average(q @ k.transpose(-2, -1) / (width // self.heads) ** .5,
                               v, local_mask[None, None])
        # The local module is BELOW the long memory, not a parallel mixture:
        # long-memory examples are extracted after incorporating the near past.
        memory_input = x + local.transpose(1, 2).reshape(batch, length, width)
        keys = F.normalize(split(self.key(memory_input)), dim=-1)
        projected = split(self.value(memory_input))
        # The last value is never read: every readable i has i+1 <= t.
        following = torch.cat((projected[:, :, 1:], torch.zeros_like(projected[:, :, :1])), 2)
        mixing = self.future_mix.sigmoid()[None, :, None, None]
        values = F.normalize((1 - mixing) * projected + mixing * following, dim=-1)
        beta = (F.softplus(self.beta[:, 0])[None, :, None, None]
                * (positions + 1).to(x.dtype)[None, None, :, None].pow(self.beta[:, 1].sigmoid()[None, :, None, None])
                + F.softplus(self.beta[:, 2])[None, :, None, None])
        logits = (keys @ keys.transpose(-2, -1)) * beta
        causal = positions[None, :] <= positions[:, None] - self.skip
        target = causal[None, None] & (positions[None, None, None, :] >= document_starts[:, None, :, None])
        related = causal[None, None] & (positions[None, None, None, :] < document_starts[:, None, :, None])
        target_value = masked_average(logits, values, target)
        related_value = masked_average(logits, values, related)
        gate = self.gate(memory_input).sigmoid().transpose(1, 2).unsqueeze(-1)
        merged = local + gate * (target_value + related_value)
        return {"keys": keys, "values": values, "logits": logits, "target_mask": target,
                "related_mask": related, "target": target_value, "related": related_value,
                "memory_input": memory_input, "local": local,
                "merged": merged.transpose(1, 2).reshape(batch, length, width)}

    def forward(self, x: Tensor, document_starts: Tensor) -> Tensor:
        return self.output(self.components(x, document_starts)["merged"])
