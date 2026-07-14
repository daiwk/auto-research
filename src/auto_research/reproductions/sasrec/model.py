from __future__ import annotations

from ..industrial_ranking import require_backend
from ..sequence_training import SequenceModelConfig, train_sequence_model


SASRecConfig = SequenceModelConfig


def build_model(item_count: int, config: SASRecConfig):
    torch, nn = require_backend()

    class SASRecBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.attention_norm = nn.LayerNorm(config.dimensions)
            self.attention = nn.MultiheadAttention(
                config.dimensions,
                config.heads,
                dropout=config.dropout,
                batch_first=True,
            )
            self.ffn_norm = nn.LayerNorm(config.dimensions)
            self.ffn = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions),
                nn.ReLU(),
                nn.Dropout(config.dropout),
                nn.Linear(config.dimensions, config.dimensions),
                nn.Dropout(config.dropout),
            )

        def forward(self, hidden, causal_mask):
            normalized = self.attention_norm(hidden)
            attended, _ = self.attention(
                normalized, hidden, hidden, attn_mask=causal_mask, need_weights=False
            )
            hidden = hidden + attended
            return hidden + self.ffn(self.ffn_norm(hidden))

    class SASRec(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            nn.init.normal_(self.item.weight, std=0.02)
            nn.init.normal_(self.position.weight, std=0.02)
            self.dropout = nn.Dropout(config.dropout)
            self.blocks = nn.ModuleList([SASRecBlock() for _ in range(config.layers)])
            self.final_norm = nn.LayerNorm(config.dimensions)

        def forward(self, items):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.dropout(
                self.item(items) * config.dimensions**0.5 + self.position(positions)
            )
            causal = torch.triu(
                torch.ones(items.shape[1], items.shape[1], device=items.device),
                diagonal=1,
            ).bool()
            for block in self.blocks:
                hidden = block(hidden, causal)
            return self.final_norm(hidden) @ self.item.weight.T

    return SASRec()


def train_model(data, config: SASRecConfig, seed: int, loss_kind: str = "bce"):
    return train_sequence_model(
        build_model(data.item_count, config), data, config, seed, loss_kind=loss_kind
    )
