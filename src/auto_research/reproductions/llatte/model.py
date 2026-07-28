from __future__ import annotations

import numpy as np

from ..industrial_ranking import require_backend


def build_llatte_model(content: np.ndarray, dimensions: int = 32, method: str = "llatte"):
    torch, nn = require_backend()
    items = len(content)

    class LLaTTE(nn.Module):
        def __init__(self):
            super().__init__()
            self.method = method
            self.id_embedding = nn.Embedding(items + 1, dimensions, padding_idx=items)
            padded_content = np.concatenate(
                (content.astype(np.float32), np.zeros((1, content.shape[1]), dtype=np.float32)), 0
            )
            self.register_buffer("semantic_content", torch.tensor(padded_content))
            self.semantic_adapter = nn.Sequential(
                nn.Linear(content.shape[1], dimensions), nn.GELU(),
                nn.Linear(dimensions, dimensions),
            )
            self.latent_queries = nn.Parameter(torch.randn(4, dimensions) * 0.02)
            self.mla = nn.MultiheadAttention(dimensions, 4, batch_first=True)
            self.online_attention = nn.MultiheadAttention(dimensions, 4, batch_first=True)
            self.dhen_gate = nn.Sequential(
                nn.Linear(4 * dimensions, dimensions), nn.GELU(), nn.Linear(dimensions, 3),
            )
            self.norm = nn.LayerNorm(dimensions)

        def sequence_features(self, history, mask):
            ids = self.id_embedding(history)
            semantics = self.semantic_adapter(self.semantic_content[history])
            tokens = self.norm(ids + semantics)
            weights = mask.float().unsqueeze(-1)
            semantic_profile = (semantics * weights).sum(1) / weights.sum(1).clamp_min(1)
            id_profile = (ids[:, -8:] * weights[:, -8:]).sum(1) / weights[:, -8:].sum(1).clamp_min(1)
            queries = self.latent_queries.unsqueeze(0).expand(history.shape[0], -1, -1)
            latent, _ = self.mla(queries, tokens, tokens, key_padding_mask=~mask)
            upstream = latent.mean(1)
            return tokens, id_profile, semantic_profile, upstream

        def _pair(self, history, mask, candidate):
            tokens, id_profile, semantic_profile, upstream = self.sequence_features(history, mask)
            vector = self.id_embedding(candidate) + self.semantic_adapter(self.semantic_content[candidate])
            if self.method == "short":
                return (id_profile * vector).sum(-1)
            recent, recent_mask = tokens[:, -12:], mask[:, -12:]
            online, _ = self.online_attention(
                vector.unsqueeze(1), recent, recent, key_padding_mask=~recent_mask
            )
            online = online[:, 0]
            gate_input = torch.cat((id_profile, semantic_profile, upstream, vector), -1)
            gates = torch.softmax(self.dhen_gate(gate_input), -1)
            experts = torch.stack((id_profile, semantic_profile, upstream + online), 1)
            user = (gates.unsqueeze(-1) * experts).sum(1)
            return (user * vector).sum(-1)

        def forward(self, history, mask, candidate):
            return self._pair(history, mask, candidate)

        def score_catalog(self, history, mask, candidates):
            tokens, id_profile, semantic_profile, upstream = self.sequence_features(history, mask)
            vectors = self.id_embedding(candidates) + self.semantic_adapter(self.semantic_content[candidates])
            if self.method == "short":
                return id_profile @ vectors.T
            batch, count = history.shape[0], len(candidates)
            recent, recent_mask = tokens[:, -12:], mask[:, -12:]
            queries = vectors[None].expand(batch, -1, -1).reshape(batch * count, 1, -1)
            keys = recent[:, None].expand(-1, count, -1, -1).reshape(batch * count, recent.shape[1], -1)
            key_mask = recent_mask[:, None].expand(-1, count, -1).reshape(batch * count, recent.shape[1])
            online, _ = self.online_attention(queries, keys, keys, key_padding_mask=~key_mask)
            online = online[:, 0].reshape(batch, count, -1)
            gate_input = torch.cat((
                id_profile[:, None].expand(-1, count, -1),
                semantic_profile[:, None].expand(-1, count, -1),
                upstream[:, None].expand(-1, count, -1),
                vectors[None].expand(batch, -1, -1),
            ), -1)
            gates = torch.softmax(self.dhen_gate(gate_input), -1)
            experts = torch.stack((
                id_profile[:, None].expand(-1, count, -1),
                semantic_profile[:, None].expand(-1, count, -1),
                upstream[:, None] + online,
            ), 2)
            users = (gates.unsqueeze(-1) * experts).sum(2)
            return (users * vectors[None]).sum(-1)

    return LLaTTE()
