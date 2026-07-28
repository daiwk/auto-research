from __future__ import annotations


def build_native_sparse_attention(
    *,
    torch,
    nn,
    config,
    head_dim: int,
    rotary,
    gated: bool,
):
    """Build the trainable three-branch Native Sparse Attention operator.

    This is a readable PyTorch reference implementation for small public-data
    experiments. It preserves NSA's compressed, selected and sliding branches;
    it intentionally does not claim the custom-kernel speedups from the paper.
    """

    class NativeSparseAttention(nn.Module):
        def __init__(self):
            super().__init__()
            dimensions = config.dimensions
            heads = config.heads
            self.heads = heads
            self.block_size = max(4, min(16, config.sequence_length // 8))
            self.local_window = max(4, min(16, config.sequence_length // 8))
            self.selected_blocks = 1
            self.q = nn.Linear(dimensions, heads * head_dim, bias=False)
            self.k = nn.Linear(dimensions, heads * head_dim, bias=False)
            self.v = nn.Linear(dimensions, heads * head_dim, bias=False)
            self.output = nn.Linear(dimensions, dimensions, bias=False)
            self.branch_gate = nn.Linear(dimensions, heads * 3, bias=True)
            self.output_gate = (
                nn.Linear(dimensions, heads, bias=True) if gated else None
            )
            self.last_statistics = {}

        def _compressed(self, keys, values, length):
            block = self.block_size
            pad = (-length) % block
            if pad:
                keys = torch.nn.functional.pad(keys, (0, 0, 0, pad))
                values = torch.nn.functional.pad(values, (0, 0, 0, pad))
            blocks = keys.shape[-2] // block
            keys = keys.view(*keys.shape[:-2], blocks, block, head_dim).mean(-2)
            values = values.view(
                *values.shape[:-2], blocks, block, head_dim
            ).mean(-2)
            return keys, values

        def forward(self, hidden):
            batch, length, _ = hidden.shape
            q = self.q(hidden).view(
                batch, length, self.heads, head_dim
            ).transpose(1, 2)
            k = self.k(hidden).view(
                batch, length, self.heads, head_dim
            ).transpose(1, 2)
            v = self.v(hidden).view(
                batch, length, self.heads, head_dim
            ).transpose(1, 2)
            q, k = rotary(
                q,
                k,
                torch,
                mode="standard",
                context_length=config.sequence_length,
            )
            positions = torch.arange(length, device=hidden.device)
            causal = positions[None, :] <= positions[:, None]
            local_mask = causal & (
                positions[None, :] >= positions[:, None] - self.local_window + 1
            )
            local = torch.nn.functional.scaled_dot_product_attention(
                q, k, v, attn_mask=local_mask, is_causal=False
            )

            compressed_k, compressed_v = self._compressed(k, v, length)
            blocks = compressed_k.shape[-2]
            block_ends = (
                (torch.arange(blocks, device=hidden.device) + 1)
                * self.block_size
                - 1
            )
            completed = block_ends[None, :] <= positions[:, None]
            compressed = torch.nn.functional.scaled_dot_product_attention(
                q,
                compressed_k,
                compressed_v,
                attn_mask=completed,
                is_causal=False,
            )
            compressed = torch.nan_to_num(compressed)

            scores = torch.einsum(
                "bhld,bhkd->bhlk", q.float(), compressed_k.float()
            )
            scores = scores.masked_fill(
                ~completed[None, None], torch.finfo(scores.dtype).min
            )
            top_k = min(self.selected_blocks, blocks)
            selected_ids = scores.topk(top_k, dim=-1).indices
            key_blocks = torch.div(
                positions, self.block_size, rounding_mode="floor"
            )
            selected_mask = (
                selected_ids[..., None] == key_blocks[None, None, None, None, :]
            ).any(-2)
            selected_mask = selected_mask & causal[None, None]
            has_completed = completed.any(-1)[None, None, :, None]
            selected_mask = selected_mask & has_completed
            selected = torch.nn.functional.scaled_dot_product_attention(
                q, k, v, attn_mask=selected_mask, is_causal=False
            )
            selected = torch.nan_to_num(selected)

            gates = torch.softmax(
                self.branch_gate(hidden).view(
                    batch, length, self.heads, 3
                ).permute(0, 2, 1, 3),
                dim=-1,
            )
            mixed = (
                gates[..., 0, None] * compressed
                + gates[..., 1, None] * selected
                + gates[..., 2, None] * local
            )
            output_gate = None
            if self.output_gate is not None:
                output_gate = torch.sigmoid(
                    self.output_gate(hidden).transpose(1, 2).unsqueeze(-1)
                )
                mixed = output_gate * mixed

            full_edges = max(1, length * (length + 1) // 2)
            compressed_edges = int(completed.sum())
            selected_edges = int(selected_mask[0, 0].sum())
            local_edges = int(local_mask.sum())
            self.last_statistics = {
                "compression_block": self.block_size,
                "selected_blocks": top_k,
                "local_window": self.local_window,
                "attention_edge_fraction": (
                    compressed_edges + selected_edges + local_edges
                )
                / full_edges,
                "compressed_gate_mean": float(
                    gates[..., 0].detach().mean().cpu()
                ),
                "selected_gate_mean": float(
                    gates[..., 1].detach().mean().cpu()
                ),
                "local_gate_mean": float(
                    gates[..., 2].detach().mean().cpu()
                ),
            }
            if output_gate is not None:
                self.last_statistics.update(
                    {
                        "output_gate_mean": float(
                            output_gate.detach().mean().cpu()
                        ),
                        "output_gate_below_0_5": float(
                            (output_gate.detach() < 0.5).float().mean().cpu()
                        ),
                    }
                )
            return self.output(
                mixed.transpose(1, 2).reshape(
                    batch, length, config.dimensions
                )
            )

    return NativeSparseAttention()
