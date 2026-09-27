"""Shared causal user backbone with retrieval, pre-rank and fine-rank tasks."""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class OneTransV2(nn.Module):
    """Reduced-width staged model; no private commerce features or serving stack.

    The history is encoded once and all three stage tokens cross-attend only
    that context. Stage tokens cannot affect behavior tokens or one another.
    """

    def __init__(self, items: int, genres: int, sid_codes: Tensor, *, width: int = 48, history_limit: int = 40) -> None:
        super().__init__()
        if sid_codes.shape != (items, 3):
            raise ValueError("one three-level SID required per catalog item")
        self.register_buffer("sid_codes", sid_codes)
        self.history_limit = history_limit
        self.item_embedding = nn.Embedding(items, width)
        self.position = nn.Embedding(history_limit, width)
        self.backbone = nn.TransformerEncoderLayer(width, 4, width * 4, dropout=0.0, batch_first=True, norm_first=True)
        self.stage_query = nn.Embedding(3, width)
        self.stage_attention = nn.MultiheadAttention(width, 4, batch_first=True)
        self.pre_head = nn.Linear(width, 2)
        self.fine_features = nn.Linear(genres, width)
        self.fine_head = nn.Linear(width, 2)
        # Only the two decision dimensions observable as MovieLens proxies
        # are supervised. Purchase, spending and ad supply are not fabricated.
        self.decisions = nn.ModuleList((nn.Linear(width, 2), nn.Linear(width, 2)))
        self.decision_embedding = nn.ModuleList((nn.Embedding(2, width), nn.Embedding(2, width)))
        self.sid_embedding = nn.ModuleList(nn.Embedding(int(sid_codes.max()) + 1, width) for _ in range(2))
        self.sid_heads = nn.ModuleList(nn.Linear(width, int(sid_codes.max()) + 1) for _ in range(3))

    def encode(self, history: Tensor, valid: Tensor) -> Tensor:
        length = history.shape[1]
        if length > self.history_limit or not valid.any(dim=1).all():
            raise ValueError("invalid user history")
        positions = self.position(torch.arange(length, device=history.device))[None]
        tokens = self.item_embedding(history) + positions
        causal = torch.triu(torch.ones(length, length, device=history.device, dtype=torch.bool), diagonal=1)
        return self.backbone(tokens, src_mask=causal, src_key_padding_mask=~valid)

    def stage_state(self, context: Tensor, valid: Tensor, stage: int, candidate: Tensor | None = None, genres: Tensor | None = None) -> Tensor:
        query = self.stage_query.weight[stage][None, None].expand(len(context), -1, -1)
        if candidate is not None:
            query = query + self.item_embedding(candidate)[:, None]
        if genres is not None:
            query = query + self.fine_features(genres)[:, None]
        attended, _ = self.stage_attention(query, context, context, key_padding_mask=~valid, need_weights=False)
        return attended[:, 0] + query[:, 0]

    def forward(self, history: Tensor, valid: Tensor, candidate: Tensor, genres: Tensor, decision_targets: Tensor | None = None, sid_targets: Tensor | None = None, decision_offsets: Tensor | None = None) -> dict[str, Tensor | list[Tensor]]:
        if decision_targets is not None and decision_offsets is not None:
            raise ValueError("decision offsets apply at generation, not teacher-forced training")
        context = self.encode(history, valid)
        retrieval = self.stage_state(context, valid, 0)
        decision_logits = [head(retrieval) for head in self.decisions]
        if decision_offsets is not None and decision_offsets.shape != (2, 2):
            raise ValueError("one offset per observable decision value is required")
        decisions = decision_targets if decision_targets is not None else torch.stack([
            (logit + (decision_offsets[index] if decision_offsets is not None else 0)).argmax(-1)
            for index, logit in enumerate(decision_logits)
        ], dim=-1)
        sid_state = retrieval + sum(embedding(decisions[:, index]) for index, embedding in enumerate(self.decision_embedding))
        sid_logits = []
        for level, head in enumerate(self.sid_heads):
            sid_logits.append(head(sid_state))
            if level < 2:
                code = sid_targets[:, level] if sid_targets is not None else sid_logits[-1].argmax(-1)
                sid_state = sid_state + self.sid_embedding[level](code)
        pre = self.pre_head(self.stage_state(context, valid, 1, candidate))
        fine = self.fine_head(self.stage_state(context, valid, 2, candidate, genres))
        return {"decisions": decision_logits, "selected_decisions": decisions, "sids": sid_logits, "pre": pre, "fine": fine}

    def loss(self, outputs: dict, *, decision_targets: Tensor, sid_targets: Tensor, labels: Tensor, retrieval_mask: Tensor) -> tuple[Tensor, dict[str, float]]:
        decision_ce = sum(F.cross_entropy(logits[retrieval_mask], decision_targets[retrieval_mask, index]) for index, logits in enumerate(outputs["decisions"]))
        sid_ce = sum(F.cross_entropy(logits[retrieval_mask], sid_targets[retrieval_mask, index]) for index, logits in enumerate(outputs["sids"]))
        pre_bce = F.binary_cross_entropy_with_logits(outputs["pre"], labels)
        fine_bce = F.binary_cross_entropy_with_logits(outputs["fine"], labels)
        # The teacher is detached; mean-centered, temperature-scaled fine
        # logits guide the pre-rank student without teacher gradient leakage.
        teacher = ((outputs["fine"].detach() - outputs["fine"].detach().mean(0, keepdim=True)) / 0.5).sigmoid()
        kd = F.binary_cross_entropy_with_logits(outputs["pre"], teacher)
        total = 0.1 * (decision_ce + sid_ce) + pre_bce + fine_bce + kd
        return total, {"decision_ce": float(decision_ce.detach()), "sid_ce": float(sid_ce.detach()), "pre_bce": float(pre_bce.detach()), "fine_bce": float(fine_bce.detach()), "fine_to_pre_kd": float(kd.detach())}
