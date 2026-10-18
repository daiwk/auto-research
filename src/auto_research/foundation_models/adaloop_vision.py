"""Question-conditioned recurrence over frozen vision blocks (visual AdaLoop).

This component deliberately does not claim a trained VLM or VisRO accuracy.
"""
from __future__ import annotations

import torch
from torch import Tensor, nn


class FrozenModulatedBlock(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        self.attention = nn.MultiheadAttention(width, heads, dropout=0., batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(width, 2 * width), nn.GELU(), nn.Linear(2 * width, width))
        self.norm_attention, self.norm_mlp = nn.LayerNorm(width), nn.LayerNorm(width)
        for parameter in self.parameters():
            parameter.requires_grad_(False)
        self.modulation = nn.Linear(width, 6 * width)
        nn.init.zeros_(self.modulation.weight)
        nn.init.zeros_(self.modulation.bias)

    def forward(self, state: Tensor, question: Tensor) -> Tensor:
        beta_a, gamma_a, alpha_a, beta_m, gamma_m, alpha_m = self.modulation(question).unsqueeze(1).chunk(6, -1)
        query = (1 + gamma_a) * self.norm_attention(state) + beta_a
        state = state + (1 + alpha_a) * self.attention(query, query, query, need_weights=False)[0]
        return state + (1 + alpha_m) * self.mlp((1 + gamma_m) * self.norm_mlp(state) + beta_m)


class QuestionConditionedVisionLoop(nn.Module):
    def __init__(self, width: int = 16, heads: int = 4, depth: int = 2):
        super().__init__()
        if min(width, heads, depth) < 1 or width % heads:
            raise ValueError("positive valid visual dimensions required")
        self.question_query = nn.Parameter(torch.randn(width) / width ** .5)
        self.blocks = nn.ModuleList(FrozenModulatedBlock(width, heads) for _ in range(depth))
        self.connector = nn.Linear(width, width)

    def condition(self, question_tokens: Tensor) -> Tensor:
        if question_tokens.ndim != 3 or question_tokens.shape[1] < 1:
            raise ValueError("nonempty question token embeddings required")
        # Paper Appendix B.1/B.2: conditioner must not train the LM embeddings.
        # The learned pooling query is still differentiated normally.
        question_tokens = question_tokens.detach()
        weights = (question_tokens * self.question_query).sum(-1).softmax(-1)
        return (question_tokens * weights[..., None]).sum(1)

    def forward(self, initial: Tensor, question_tokens: Tensor, iterations: int = 3) -> tuple[Tensor, ...]:
        if initial.ndim != 3 or initial.shape[1] < 1 or iterations < 1:
            raise ValueError("visual tokens and positive loop budget required")
        condition = self.condition(question_tokens)
        state, outputs = initial, []
        for _ in range(iterations):
            for block in self.blocks:
                state = block(state, condition)
            outputs.append(self.connector(state))
        return tuple(outputs)


def visual_prefix(states: tuple[Tensor, ...], question: Tensor, variant: str = "A",
                  drafts: tuple[Tensor, ...] = (), separator: Tensor | None = None) -> Tensor:
    if not states or variant not in {"A", "B", "C"}:
        raise ValueError("nonempty visual states and A/B/C interface required")
    if variant == "A":
        return torch.cat((states[-1], question), 1)
    if variant == "B":
        return torch.cat((*states, question), 1)
    if len(drafts) != len(states) - 1 or separator is None:
        raise ValueError("C requires model-generated drafts and an explicit fixed separator")
    pieces = [states[0], question]
    for draft, state in zip(drafts, states[1:], strict=True):
        pieces.extend((draft.detach(), separator, state, question))
    return torch.cat(pieces, 1)


def depth_supervised_loss(logits: tuple[Tensor, ...], labels: Tensor, weights: Tensor) -> Tensor:
    if not logits or weights.shape != (len(logits),) or not bool(torch.isfinite(weights).all()) or bool((weights <= 0).any()):
        raise ValueError("one positive finite weight per depth required")
    if not torch.isclose(weights.sum(), weights.new_tensor(1.)):
        raise ValueError("depth weights must sum to one")
    losses = torch.stack([nn.functional.cross_entropy(scores, labels) for scores in logits])
    return (weights * losses).sum()


def stability_stop(answers: list[str], max_depth: int) -> int:
    """One-based stopping depth; no gold answers are inspected."""
    if not answers or max_depth < 1:
        raise ValueError("predicted answers and positive depth required")
    limit = min(len(answers), max_depth)
    for index in range(1, limit):
        if answers[index] == answers[index - 1]:
            return index + 1
    return limit
