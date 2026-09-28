"""Small trainable KITE/SST architecture (arXiv:2609.27294, Sec. 2).

The Prefiller writes all historical KV. The Decoder owns only queries and
token-local transformations; it cannot influence the KV written for any
future token. This is a scaled-down dense reference, not the paper's MoE.
"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


class PrefillerBlock(nn.Module):
    def __init__(self, width: int):
        super().__init__()
        self.norm = nn.LayerNorm(width)
        self.q = nn.Linear(width, width, bias=False)
        self.k = nn.Linear(width, width, bias=False)
        self.v = nn.Linear(width, width, bias=False)
        self.out = nn.Linear(width, width, bias=False)
        self.ffn = nn.Sequential(nn.LayerNorm(width), nn.Linear(width, 4 * width),
                                 nn.GELU(), nn.Linear(4 * width, width))
        self.scale = width ** -0.5

    def forward(self, hidden: torch.Tensor, past=None):
        normalized = self.norm(hidden)
        key, value = self.k(normalized), self.v(normalized)
        offset = 0
        if past is not None:
            offset = past[0].shape[1]
            key = torch.cat((past[0], key), dim=1)
            value = torch.cat((past[1], value), dim=1)
        query = self.q(normalized)
        score = query @ key.transpose(-2, -1) * self.scale
        rows = torch.arange(hidden.shape[1], device=hidden.device)[:, None] + offset
        cols = torch.arange(key.shape[1], device=hidden.device)[None, :]
        score = score.masked_fill(cols > rows, torch.finfo(score.dtype).min)
        hidden = hidden + self.out(score.softmax(-1) @ value)
        return hidden + self.ffn(hidden), (key, value)


class DecoderBlock(nn.Module):
    def __init__(self, width: int):
        super().__init__()
        self.norm = nn.LayerNorm(width)
        self.q = nn.Linear(width, width, bias=False)
        self.out = nn.Linear(width, width, bias=False)
        self.ffn = nn.Sequential(nn.LayerNorm(width), nn.Linear(width, 4 * width),
                                 nn.GELU(), nn.Linear(4 * width, width))
        self.scale = width ** -0.5

    def forward(self, hidden: torch.Tensor, kv, *, offset: int):
        key, value = kv
        query = self.q(self.norm(hidden))
        score = query @ key.transpose(-2, -1) * self.scale
        rows = torch.arange(hidden.shape[1], device=hidden.device)[:, None] + offset
        cols = torch.arange(key.shape[1], device=hidden.device)[None, :]
        score = score.masked_fill(cols > rows, torch.finfo(score.dtype).min)
        hidden = hidden + self.out(score.softmax(-1) @ value)
        return hidden + self.ffn(hidden)


def _rms(tensor: torch.Tensor) -> torch.Tensor:
    return tensor * torch.rsqrt(tensor.square().mean(dim=-1, keepdim=True) + 1e-5)


class SmallSST(nn.Module):
    def __init__(self, vocab_size: int, width: int = 32, layers: int = 2,
                 max_positions: int = 256):
        super().__init__()
        if min(vocab_size, width, layers, max_positions) < 1:
            raise ValueError("model dimensions must be positive")
        self.embedding = nn.Embedding(vocab_size, width)
        self.position = nn.Embedding(max_positions, width)
        self.prefiller = nn.ModuleList(PrefillerBlock(width) for _ in range(layers))
        self.decoder: nn.ModuleList | None = None
        self.final_norm = nn.LayerNorm(width)
        self.lm_head = nn.Linear(width, vocab_size, bias=False)

    @property
    def expanded(self) -> bool:
        return self.decoder is not None

    def expand(self) -> None:
        """Copy source query/output/FFN weights; jointly train both towers."""
        if self.expanded:
            raise ValueError("model already expanded")
        width = self.embedding.embedding_dim
        decoder = nn.ModuleList(DecoderBlock(width) for _ in self.prefiller)
        for target, source in zip(decoder, self.prefiller):
            target.norm.load_state_dict(source.norm.state_dict())
            target.q.load_state_dict(source.q.state_dict())
            target.out.load_state_dict(source.out.state_dict())
            target.ffn.load_state_dict(source.ffn.state_dict())
        self.decoder = decoder.to(self.embedding.weight.device)

    def forward(self, tokens: torch.Tensor, *, past=None, last_only: bool = False):
        if tokens.ndim != 2 or not tokens.shape[1]:
            raise ValueError("tokens must have shape [batch, positive sequence]")
        offset = 0 if past is None else past[0][0].shape[1]
        if offset + tokens.shape[1] > self.position.num_embeddings:
            raise ValueError("sequence exceeds positional capacity")
        positions = torch.arange(offset, offset + tokens.shape[1], device=tokens.device)
        embedded = self.embedding(tokens) + self.position(positions)
        hidden = embedded
        memories = []
        for index, block in enumerate(self.prefiller):
            hidden, kv = block(hidden, None if past is None else past[index])
            memories.append(kv)
        if self.expanded:
            if last_only and past is None:
                embedded, hidden = embedded[:, -1:], hidden[:, -1:]
                decoder_offset = tokens.shape[1] - 1
            else:
                decoder_offset = offset
            hidden = _rms(embedded) + _rms(hidden)
            for block, kv in zip(self.decoder, memories):
                hidden = block(hidden, kv, offset=decoder_offset)
        elif last_only:
            hidden = hidden[:, -1:]
        return self.lm_head(self.final_norm(hidden)), tuple(memories)


def train_two_stages(model: SmallSST, train_tokens: torch.Tensor, *,
                     source_steps: int = 20, continuation_steps: int = 20,
                     learning_rate: float = 1e-3) -> dict[str, float]:
    """Run both real next-token training stages on a caller-supplied corpus.

    The caller owns train/validation/test separation. This function never
    selects hyperparameters or reports a test metric.
    """
    if train_tokens.ndim != 2 or train_tokens.shape[1] < 2 or source_steps < 1 or continuation_steps < 1:
        raise ValueError("valid next-token batches and positive stage budgets required")
    if model.expanded or learning_rate <= 0:
        raise ValueError("provide an unexpanded model and positive learning rate")
    inputs, labels = train_tokens[:, :-1], train_tokens[:, 1:]
    losses = {}
    for stage, steps in (("source", source_steps), ("expanded", continuation_steps)):
        if stage == "expanded":
            model.expand()
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        for _ in range(steps):
            logits, _ = model(inputs)
            loss = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1))
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()
        losses[f"{stage}_train_loss"] = float(loss.detach())
    return losses
