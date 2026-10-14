"""Beyond the Final Embedding: sparse token retrieval, floor and fusion."""
from __future__ import annotations

import numpy as np


def standardize(scores: np.ndarray) -> np.ndarray:
    return (scores - scores.mean()) / max(float(scores.std()), 1e-6)


class SparseTokenIndex:
    """Fixed token bank; exact global top-k is the paper's Appendix D control."""

    def __init__(self, memory_tokens: list[np.ndarray], pooled: np.ndarray,
                 device: str = "cpu"):
        import torch
        if len(memory_tokens) != len(pooled) or not memory_tokens:
            raise ValueError("one token sequence and pooled vector per memory required")
        self.torch, self.device = torch, device
        self.pooled = np.asarray(pooled)
        self.ids = torch.as_tensor(np.concatenate([
            np.full(len(t), i, dtype=np.int64) for i, t in enumerate(memory_tokens)
        ]), device=device)
        self.tokens = torch.as_tensor(np.concatenate(memory_tokens), device=device, dtype=torch.float32)
        self.memory_count = len(memory_tokens)
        self.search_count = 0

    def local_scores(self, query_tokens: np.ndarray, token_budget: int = 64) -> np.ndarray:
        torch = self.torch
        if token_budget < 1 or not len(query_tokens):
            raise ValueError("positive token budget and nonempty query tokens required")
        q = torch.as_tensor(query_tokens, device=self.device, dtype=torch.float32)
        sims, indices = torch.topk(q @ self.tokens.T, min(token_budget, len(self.tokens)), dim=1)
        self.search_count += 1
        floor = sims[:, -1].clamp_min(0)
        local = floor[:, None].expand(-1, self.memory_count).clone()
        memory_ids = self.ids[indices]
        local.scatter_reduce_(1, memory_ids, sims, reduce="amax", include_self=True)
        return local.mean(0).cpu().numpy()

    def scores(self, query_tokens: np.ndarray, query_pooled: np.ndarray,
               *, token_budget: int = 64, alpha: float = 0.5) -> np.ndarray:
        if not 0 <= alpha <= 1:
            raise ValueError("fusion weight must be in [0,1]")
        local = self.local_scores(query_tokens, token_budget)
        whole = self.pooled @ query_pooled
        return alpha * standardize(whole) + (1 - alpha) * standardize(local)


def query_adapter(dimension: int, rank: int = 32):
    """Norm-preserving bias-free low-rank residual, zero B init (Eq. 4)."""
    import torch
    from torch import nn

    class QueryAdapter(nn.Module):
        def __init__(self):
            super().__init__()
            self.a = nn.Linear(dimension, rank, bias=False)
            self.b = nn.Linear(rank, dimension, bias=False)
            nn.init.zeros_(self.b.weight)

        def forward(self, h):
            changed = h + self.b(self.a(h))
            return h.norm(dim=-1, keepdim=True) * changed / changed.norm(
                dim=-1, keepdim=True).clamp_min(1e-12)

    return QueryAdapter()


def multipositive_maxsim_loss(adapted_query, memories, positive_indices, temperature: float = 0.07):
    import torch
    if not positive_indices:
        raise ValueError("at least one source-training positive required")
    scores = torch.stack([(adapted_query @ memory.T).max(1).values.mean() for memory in memories])
    logits = scores / temperature
    positive = torch.as_tensor(sorted(positive_indices), device=logits.device)
    return torch.logsumexp(logits, 0) - torch.logsumexp(logits[positive], 0)
