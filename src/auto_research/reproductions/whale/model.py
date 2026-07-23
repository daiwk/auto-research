from __future__ import annotations

from ..industrial_ranking import require_backend
from ..july_2026_common import item_feature_tensor


def build_whale(data, config):
    torch, nn = require_backend()

    class WukongInteraction(nn.Module):
        def __init__(self):
            super().__init__()
            self.left = nn.Linear(config.dimensions, config.dimensions * 2)
            self.right = nn.Linear(config.dimensions, config.dimensions * 2)
            self.compress = nn.Linear(config.dimensions * 2, config.dimensions)
            self.norm = nn.LayerNorm(config.dimensions)

        def forward(self, values):
            crossed = self.left(values) * self.right(values)
            return self.norm(values + self.compress(crossed))

    class HSTUBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.attention = nn.MultiheadAttention(
                config.dimensions, config.heads, batch_first=True, dropout=0.0
            )
            self.gate = nn.Linear(config.dimensions, 2 * config.dimensions)
            self.norm = nn.LayerNorm(config.dimensions)

        def forward(self, sequence):
            length = sequence.shape[1]
            causal = torch.triu(
                torch.ones(length, length, dtype=torch.bool, device=sequence.device), diagonal=1
            )
            attended, _ = self.attention(sequence, sequence, sequence, attn_mask=causal)
            update, gate = self.gate(attended).chunk(2, dim=-1)
            return self.norm(sequence + torch.nn.functional.silu(update) * torch.sigmoid(gate))

    class WhaleLayer(nn.Module):
        def __init__(self):
            super().__init__()
            self.wukong = WukongInteraction()
            self.hstu = HSTUBlock()
            self.fusion = nn.MultiheadAttention(
                config.dimensions, config.heads, batch_first=True, dropout=0.0
            )
            self.ffn = nn.Sequential(
                nn.LayerNorm(config.dimensions),
                nn.Linear(config.dimensions, 3 * config.dimensions),
                nn.SiLU(),
                nn.Linear(3 * config.dimensions, config.dimensions),
            )

        def forward(self, context, sequence):
            context = self.wukong(context)
            sequence = self.hstu(sequence)
            retrieved, weights = self.fusion(context[:, None], sequence, sequence)
            context = context + retrieved[:, 0]
            context = context + self.ffn(context)
            return context, sequence, weights

    class WHALE(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            self.content = nn.Parameter(
                item_feature_tensor(data, config.dimensions, torch), requires_grad=False
            )
            self.layers = nn.ModuleList([WhaleLayer() for _ in range(config.layers)])
            self.final = nn.LayerNorm(config.dimensions)

        def forward(self, histories, **_):
            positions = torch.arange(histories.shape[1], device=histories.device)
            sequence = self.item(histories) + self.position(positions)
            context = sequence.mean(1) + sequence[:, -1] + self.content[histories].mean(1)
            exchanges = []
            for layer in self.layers:
                context, sequence, weights = layer(context, sequence)
                exchanges.append(weights.mean())
            logits = self.final(context) @ (self.item.weight + self.content).T
            return {"logits": logits, "exchange_attention": torch.stack(exchanges).mean()}

    return WHALE()
