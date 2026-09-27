"""Trainable residual-SID autoregressive comparator for X-Rec.

The quantizer is fitted on the same train-only item vectors as X-Rec.  The
decoder predicts each code conditioned on the history and previous codes; it
never sees a validation or test target at generation time.
"""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F

from .experiment import U2IBaseline


def fit_item_codes(vectors: Tensor, *, seed: int, levels: int = 3, size: int = 16) -> tuple[Tensor, Tensor]:
    if size > len(vectors):
        raise ValueError("codebook larger than item catalog")
    generator = torch.Generator().manual_seed(seed)
    residual = vectors.detach().float().cpu().clone()
    codes = []
    codebooks = []
    for _ in range(levels):
        centers = residual[torch.randperm(len(residual), generator=generator)[:size]].clone()
        for _ in range(20):
            assignment = torch.cdist(residual, centers).argmin(dim=-1)
            counts = torch.bincount(assignment, minlength=size)
            sums = torch.zeros_like(centers).index_add_(0, assignment, residual)
            centers = torch.where(counts[:, None] > 0, sums / counts[:, None].clamp_min(1), centers)
        assignment = torch.cdist(residual, centers).argmin(dim=-1)
        codes.append(assignment)
        codebooks.append(centers)
        residual = residual - centers[assignment]
    return torch.stack(codes, dim=-1), torch.stack(codebooks)


class SIDAutoregressive(nn.Module):
    """Causal code decoder with the same two-layer history encoder as U2I."""

    def __init__(self, vectors: Tensor, codes: Tensor, codebooks: Tensor, *, width: int = 48, max_history: int = 40) -> None:
        super().__init__()
        if codes.shape[0] != len(vectors) or codes.ndim != 2:
            raise ValueError("one SID sequence required per item")
        self.register_buffer("codes", codes)
        if codebooks.shape[:2] != (codes.shape[1], int(codes.max()) + 1):
            raise ValueError("codebook and SID cardinalities disagree")
        self.register_buffer("codebooks", codebooks)
        self.history = U2IBaseline(vectors, width, max_history)
        self.levels = codes.shape[1]
        self.size = int(codes.max()) + 1
        self.context = nn.Linear(vectors.shape[1], width)
        self.code_embeddings = nn.ModuleList(nn.Embedding(self.size, width) for _ in range(self.levels - 1))
        self.code_heads = nn.ModuleList(nn.Linear(width, self.size) for _ in range(self.levels))

    def logits(self, history: Tensor, valid: Tensor, prefix: Tensor | None = None) -> list[Tensor]:
        state = self.context(self.history(history, valid))
        outputs = []
        for level, head in enumerate(self.code_heads):
            outputs.append(head(state))
            if level < self.levels - 1:
                code = prefix[:, level] if prefix is not None else outputs[-1].argmax(dim=-1)
                state = state + self.code_embeddings[level](code)
        return outputs

    def loss(self, history: Tensor, valid: Tensor, item: Tensor) -> Tensor:
        target = self.codes[item]
        return sum(F.cross_entropy(logit, target[:, level]) for level, logit in enumerate(self.logits(history, valid, target)))

    @torch.no_grad()
    def beam_codes(self, history: Tensor, valid: Tensor, *, width: int = 20) -> tuple[Tensor, Tensor]:
        """Exact levelwise beam over conditional log probabilities."""
        if width < 1:
            raise ValueError("beam width must be positive")
        state = self.context(self.history(history, valid))
        batch = len(history)
        beam_state = state[:, None, :]
        beam_codes = torch.empty(batch, 1, 0, dtype=torch.long, device=history.device)
        beam_scores = torch.zeros(batch, 1, device=history.device)
        for level, head in enumerate(self.code_heads):
            logp = F.log_softmax(head(beam_state), dim=-1)
            scores = beam_scores[:, :, None] + logp
            count = min(width, scores.shape[1] * self.size)
            beam_scores, flat = scores.flatten(1).topk(count, dim=-1)
            parent, token = torch.div(flat, self.size, rounding_mode="floor"), flat % self.size
            prior = beam_codes.gather(1, parent[:, :, None].expand(-1, -1, level))
            beam_codes = torch.cat((prior, token[:, :, None]), dim=-1)
            beam_state = beam_state.gather(1, parent[:, :, None].expand(-1, -1, state.shape[-1]))
            if level < self.levels - 1:
                beam_state = beam_state + self.code_embeddings[level](token)
        return beam_codes, beam_scores

    @torch.no_grad()
    def trigger_vectors(self, history: Tensor, valid: Tensor, *, width: int = 20) -> Tensor:
        """Decode beam SIDs through RQ codebooks before exact ANN lookup."""
        beams, _ = self.beam_codes(history, valid, width=width)
        decoded = sum(self.codebooks[level][beams[:, :, level]] for level in range(self.levels))
        return F.normalize(decoded, dim=-1)
