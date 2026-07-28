from __future__ import annotations

from ..industrial_ranking import require_backend


def build_cmsl_model(items: int, dimensions: int = 32, lenses: int = 6, method: str = "cmsl"):
    torch, nn = require_backend()

    class HSTUBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.qkv = nn.Linear(dimensions, 3 * dimensions)
            self.gate = nn.Linear(dimensions, dimensions)
            self.out = nn.Linear(dimensions, dimensions)
            self.norm = nn.LayerNorm(dimensions)

        def forward(self, values, mask):
            q, k, v = self.qkv(values).chunk(3, -1)
            logits = torch.einsum("bld,bmd->blm", q, k) / dimensions**0.5
            logits = logits.masked_fill(~mask[:, None, :], -1e4)
            attention = torch.softmax(torch.nn.functional.silu(logits), -1)
            update = torch.einsum("blm,bmd->bld", attention, v)
            return self.norm(values + torch.sigmoid(self.gate(values)) * self.out(update))

    class CMSL(nn.Module):
        def __init__(self):
            super().__init__()
            self.method = method
            self.embedding = nn.Embedding(items + 1, dimensions, padding_idx=items)
            self.lens_queries = nn.Parameter(torch.randn(lenses, dimensions) * 0.02)
            self.contextual_lens = nn.Sequential(
                nn.Linear(dimensions, dimensions), nn.GELU(), nn.Linear(dimensions, dimensions),
            )
            self.hstu = HSTUBlock()
            self.fusion = nn.Linear(dimensions, 1)

        def profiles(self, history, mask):
            hidden = self.embedding(history)
            encoded = self.hstu(hidden, mask)
            if self.method == "single":
                weights = mask.float()
                return ((encoded * weights.unsqueeze(-1)).sum(1) / weights.sum(1, keepdim=True).clamp_min(1)).unsqueeze(1)
            contextual = self.contextual_lens(encoded)
            assignment = torch.einsum("bld,kd->blk", contextual, self.lens_queries)
            assignment = assignment.masked_fill(~mask.unsqueeze(-1), -1e4)
            assignment = torch.softmax(assignment, 1)
            profiles = torch.einsum("blk,bld->bkd", assignment, encoded)
            return profiles

        def pair_scores(self, history, mask, candidates):
            profiles = self.profiles(history, mask)
            vectors = self.embedding(candidates)
            logits = (profiles * vectors.unsqueeze(1)).sum(-1)
            return torch.logsumexp(logits, 1)

        def forward(self, history, mask, candidate):
            return self.pair_scores(history, mask, candidate)

        def score_catalog(self, history, mask, candidates):
            profiles = self.profiles(history, mask)
            logits = torch.einsum("bkd,nd->bkn", profiles, self.embedding(candidates))
            return torch.logsumexp(logits, 1)

    return CMSL()
