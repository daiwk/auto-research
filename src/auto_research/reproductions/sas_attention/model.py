from __future__ import annotations

import copy
import math


def build_tiny_sas_lm(
    *,
    vocab_size: int,
    dimensions: int = 32,
    heads: int = 4,
    sequence_length: int = 64,
    block_size: int = 8,
    top_k_blocks: int = 2,
):
    """Build a tiny decoder containing the paper's differentiable SAS router.

    PyTorch stays optional at package-import time.  This reference path executes
    the selector, hard block Top-K, normalized continuous gates and the causal
    attention computation; it intentionally does not claim the paper's Triton
    kernel speedups.
    """
    import torch
    from torch import nn

    if dimensions % heads:
        raise ValueError("dimensions must be divisible by heads")

    class SASAttention(nn.Module):
        def __init__(self):
            super().__init__()
            self.heads = heads
            self.head_dim = dimensions // heads
            self.block_size = block_size
            self.top_k_blocks = top_k_blocks
            self.qkv = nn.Linear(dimensions, 3 * dimensions, bias=False)
            self.output = nn.Linear(dimensions, dimensions, bias=False)
            selector_dim = max(8, self.head_dim)
            self.selector_q = nn.Linear(dimensions, selector_dim, bias=False)
            self.selector_k = nn.Linear(dimensions, selector_dim, bias=False)
            self.sparse = True
            self.last_diagnostics: dict[str, float] = {}

        def _selector_bias(self, values):
            batch, length, _ = values.shape
            blocks = math.ceil(length / self.block_size)
            selector_q = self.selector_q(values)
            block_keys = []
            for block in range(blocks):
                start = block * self.block_size
                stop = min(length, start + self.block_size)
                block_keys.append(self.selector_k(values[:, start:stop]).mean(dim=1))
            block_keys = torch.stack(block_keys, dim=1)
            scores = torch.einsum("bld,bcd->blc", selector_q, block_keys)
            scores = scores / math.sqrt(selector_q.shape[-1])

            bias = values.new_full((batch, length, length), float("-inf"))
            allowed = 0
            selected = 0
            gate_entropy = []
            for query in range(length):
                current = query // self.block_size
                current_start = current * self.block_size
                # The current block is always retained with unit gate and remains causal.
                bias[:, query, current_start : query + 1] = 0.0
                allowed += query + 1
                selected += batch * (query - current_start + 1)
                if current == 0:
                    continue
                historical = scores[:, query, :current]
                gates = torch.softmax(historical, dim=-1)
                keep = min(self.top_k_blocks, current)
                indices = historical.topk(keep, dim=-1).indices
                selected_gates = gates.gather(1, indices)
                gate_entropy.append(
                    -(gates * gates.clamp_min(1e-12).log()).sum(dim=-1).mean()
                )
                for row in range(batch):
                    for rank in range(keep):
                        block = int(indices[row, rank])
                        start = block * self.block_size
                        stop = min(length, start + self.block_size)
                        # Equation (5): the positive selector gate is injected as
                        # log(g) inside attention softmax and stays continuous.
                        bias[row, query, start:stop] = selected_gates[row, rank].clamp_min(1e-12).log()
                        selected += stop - start
            entropy = torch.stack(gate_entropy).mean() if gate_entropy else values.new_zeros(())
            self.last_diagnostics = {
                "retained_attention_fraction": float(selected / max(batch * allowed, 1)),
                "selector_gate_entropy": float(entropy.detach().cpu()),
            }
            return bias

        def forward(self, values):
            batch, length, _ = values.shape
            qkv = self.qkv(values).view(batch, length, 3, self.heads, self.head_dim)
            query, key, value = qkv.unbind(dim=2)
            query, key, value = (tensor.transpose(1, 2) for tensor in (query, key, value))
            logits = torch.matmul(query, key.transpose(-1, -2)) / math.sqrt(self.head_dim)
            causal = torch.triu(
                torch.ones(length, length, dtype=torch.bool, device=values.device), diagonal=1
            )
            if self.sparse:
                logits = logits + self._selector_bias(values)[:, None]
            else:
                logits = logits.masked_fill(causal[None, None], float("-inf"))
                self.last_diagnostics = {
                    "retained_attention_fraction": 1.0,
                    "selector_gate_entropy": 0.0,
                }
            weights = torch.softmax(logits, dim=-1)
            output = torch.matmul(weights, value).transpose(1, 2).reshape(batch, length, dimensions)
            return self.output(output)

    class TinySASLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding(vocab_size, dimensions)
            self.position = nn.Embedding(sequence_length, dimensions)
            self.norm1 = nn.LayerNorm(dimensions)
            self.attention = SASAttention()
            self.norm2 = nn.LayerNorm(dimensions)
            self.mlp = nn.Sequential(
                nn.Linear(dimensions, 4 * dimensions),
                nn.GELU(),
                nn.Linear(4 * dimensions, dimensions),
            )
            self.final_norm = nn.LayerNorm(dimensions)
            self.output = nn.Linear(dimensions, vocab_size, bias=False)
            self.apply(self._initialize)
            self.output.weight = self.token.weight

        @staticmethod
        def _initialize(module):
            if isinstance(module, (nn.Linear, nn.Embedding)):
                nn.init.normal_(module.weight, mean=0.0, std=0.02)

        def forward(self, tokens):
            positions = torch.arange(tokens.shape[1], device=tokens.device)
            values = self.token(tokens) + self.position(positions)[None]
            values = values + self.attention(self.norm1(values))
            values = values + self.mlp(self.norm2(values))
            return self.output(self.final_norm(values))

    return TinySASLM()


def clone_as_sparse(dense):
    sparse = copy.deepcopy(dense)
    sparse.attention.sparse = True
    for parameter in sparse.parameters():
        parameter.requires_grad = False
    for module in (sparse.attention.selector_q, sparse.attention.selector_k):
        for parameter in module.parameters():
            parameter.requires_grad = True
    return sparse
