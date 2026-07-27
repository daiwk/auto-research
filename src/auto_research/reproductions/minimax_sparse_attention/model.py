from __future__ import annotations

from ..industrial_ranking import require_backend


def build_tiny_lm(vocab_size=128, dimensions=64, heads=4, kv_heads=2, block_size=16, top_blocks=2, sparse=True):
    torch, nn = require_backend()
    if heads % kv_heads:
        raise ValueError("heads must be divisible by kv_heads")
    head_dim = dimensions // heads

    class MSAttention(nn.Module):
        def __init__(self):
            super().__init__()
            self.q = nn.Linear(dimensions, heads * head_dim, bias=False)
            self.k = nn.Linear(dimensions, kv_heads * head_dim, bias=False)
            self.v = nn.Linear(dimensions, kv_heads * head_dim, bias=False)
            self.index_q = nn.Linear(dimensions, kv_heads * head_dim, bias=False)
            self.index_k = nn.Linear(dimensions, kv_heads * head_dim, bias=False)
            self.out = nn.Linear(dimensions, dimensions, bias=False)
            self.last_pair_ratio = 1.0
            self.index_loss = None

        def forward(self, x):
            batch, length, _ = x.shape
            q = self.q(x).view(batch, length, heads, head_dim).transpose(1, 2)
            k = self.k(x).view(batch, length, kv_heads, head_dim).transpose(1, 2)
            v = self.v(x).view(batch, length, kv_heads, head_dim).transpose(1, 2)
            repeat = heads // kv_heads
            k_full = k.repeat_interleave(repeat, dim=1)
            v_full = v.repeat_interleave(repeat, dim=1)
            scores = q @ k_full.transpose(-1, -2) / (head_dim ** 0.5)
            causal = torch.tril(torch.ones(length, length, dtype=torch.bool, device=x.device))
            mask = causal[None, None].expand(batch, heads, -1, -1)
            if sparse:
                iq = self.index_q(x).view(batch, length, kv_heads, head_dim).transpose(1, 2)
                ik = self.index_k(x).view(batch, length, kv_heads, head_dim).transpose(1, 2)
                blocks = (length + block_size - 1) // block_size
                padded = blocks * block_size - length
                if padded:
                    ik = torch.nn.functional.pad(ik, (0, 0, 0, padded))
                pooled = ik.view(batch, kv_heads, blocks, block_size, head_dim).mean(3)
                index_scores = iq @ pooled.transpose(-1, -2) / (head_dim ** 0.5)
                grouped_q = q.view(batch, kv_heads, repeat, length, head_dim).mean(2)
                grouped_k = k
                if padded:
                    grouped_k = torch.nn.functional.pad(grouped_k, (0, 0, 0, padded))
                target_keys = grouped_k.view(
                    batch, kv_heads, blocks, block_size, head_dim
                ).mean(3)
                target_scores = (
                    grouped_q @ target_keys.transpose(-1, -2) / (head_dim ** 0.5)
                ).detach()
                self.index_loss = torch.nn.functional.kl_div(
                    torch.log_softmax(index_scores, dim=-1),
                    torch.softmax(target_scores, dim=-1),
                    reduction="batchmean",
                ) / max(length * kv_heads, 1)
                selected = torch.topk(index_scores, min(top_blocks, blocks), dim=-1).indices
                token_blocks = torch.arange(length, device=x.device) // block_size
                block_mask = (selected[..., None] == token_blocks[None, None, None, None, :]).any(-2)
                block_mask = block_mask.repeat_interleave(repeat, dim=1)
                mask = mask & block_mask
                diagonal = torch.eye(length, dtype=torch.bool, device=x.device)[None, None]
                mask = mask | diagonal
                self.last_pair_ratio = float(mask.float().mean().detach().cpu())
            scores = scores.masked_fill(~mask, -1e4)
            values = torch.softmax(scores, dim=-1) @ v_full
            return self.out(values.transpose(1, 2).reshape(batch, length, dimensions))

    class TinyLM(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding(vocab_size, dimensions)
            self.position = nn.Embedding(256, dimensions)
            self.norm1 = nn.LayerNorm(dimensions)
            self.attention = MSAttention()
            self.norm2 = nn.LayerNorm(dimensions)
            self.ffn = nn.Sequential(nn.Linear(dimensions, 3 * dimensions), nn.SiLU(), nn.Linear(3 * dimensions, dimensions))
            self.output = nn.Linear(dimensions, vocab_size, bias=False)
            self.output.weight = self.token.weight
            nn.init.normal_(self.token.weight, mean=0.0, std=0.02)
            nn.init.normal_(self.position.weight, mean=0.0, std=0.02)

        def forward(self, tokens):
            positions = torch.arange(tokens.shape[1], device=tokens.device)
            x = self.token(tokens) + self.position(positions)
            x = x + self.attention(self.norm1(x))
            x = x + self.ffn(self.norm2(x))
            return self.output(x)

    return TinyLM()
