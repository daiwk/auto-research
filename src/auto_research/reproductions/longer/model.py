from __future__ import annotations

from ..industrial_ranking import require_backend


def build_longer_model(items: int, dimensions: int = 32, group_size: int = 4, method: str = "longer"):
    torch, nn = require_backend()

    class LONGER(nn.Module):
        def __init__(self):
            super().__init__()
            self.items = items
            self.group_size = group_size
            self.method = method
            self.embedding = nn.Embedding(items + 1, dimensions, padding_idx=items)
            self.position = nn.Embedding(64, dimensions)
            self.inner_trans = nn.TransformerEncoder(
                nn.TransformerEncoderLayer(
                    dimensions, 4, 2 * dimensions, batch_first=True,
                    norm_first=True, dropout=0.0,
                ), 1,
            )
            self.inner_pool = nn.Linear(dimensions, 1)
            self.global_token = nn.Parameter(torch.zeros(1, 1, dimensions))
            self.hybrid_attention = nn.TransformerEncoder(
                nn.TransformerEncoderLayer(
                    dimensions, 4, 4 * dimensions, batch_first=True,
                    norm_first=True, dropout=0.0,
                ), 1,
            )
            self.output = nn.LayerNorm(dimensions)

        def encode(self, history, mask):
            positions = torch.arange(history.shape[1], device=history.device)
            hidden = self.embedding(history) + self.position(positions)
            if self.method == "recent":
                recent, recent_mask = hidden[:, -12:], mask[:, -12:]
                encoded = self.hybrid_attention(recent, src_key_padding_mask=~recent_mask)
                weights = recent_mask.float()
                return self.output((encoded * weights.unsqueeze(-1)).sum(1) / weights.sum(1, keepdim=True).clamp_min(1))

            old, old_mask = hidden[:, :-12], mask[:, :-12]
            usable = (old.shape[1] // self.group_size) * self.group_size
            old, old_mask = old[:, -usable:], old_mask[:, -usable:]
            batch, length, dim = old.shape
            groups = old.reshape(batch * (length // self.group_size), self.group_size, dim)
            group_mask = old_mask.reshape(batch * (length // self.group_size), self.group_size)
            safe_mask = group_mask.clone()
            empty = ~safe_mask.any(1)
            safe_mask[empty, -1] = True
            inner = self.inner_trans(groups, src_key_padding_mask=~safe_mask)
            logits = self.inner_pool(inner).squeeze(-1).masked_fill(~safe_mask, -1e4)
            merged = (torch.softmax(logits, -1).unsqueeze(-1) * inner).sum(1)
            merged = merged.reshape(batch, -1, dim)
            merged_mask = group_mask.any(1).reshape(batch, -1)
            recent, recent_mask = hidden[:, -12:], mask[:, -12:]
            global_token = self.global_token.expand(batch, -1, -1)
            tokens = torch.cat((global_token, merged, recent), 1)
            token_mask = torch.cat((
                torch.ones(batch, 1, dtype=torch.bool, device=mask.device),
                merged_mask, recent_mask,
            ), 1)
            encoded = self.hybrid_attention(tokens, src_key_padding_mask=~token_mask)
            return self.output(encoded[:, 0])

        def forward(self, history, mask, candidate):
            return (self.encode(history, mask) * self.embedding(candidate)).sum(-1)

        def score_catalog(self, history, mask, candidates):
            return self.encode(history, mask) @ self.embedding(candidates).T

    return LONGER()
