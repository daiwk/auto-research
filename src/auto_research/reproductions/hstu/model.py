from __future__ import annotations

from dataclasses import dataclass

from ..industrial_ranking import require_backend
from ..sequence_training import SequenceModelConfig, train_sequence_model


@dataclass(frozen=True)
class HSTUConfig(SequenceModelConfig):
    linear_multiplier: int = 2
    relative_buckets: int = 32


def build_model(item_count: int, config: HSTUConfig):
    torch, nn = require_backend()
    head_dim = config.dimensions // config.heads
    linear_dim = head_dim * config.linear_multiplier

    class HSTULayer(nn.Module):
        def __init__(self):
            super().__init__()
            total = config.heads * (2 * linear_dim + 2 * head_dim)
            self.uvqk = nn.Linear(config.dimensions, total, bias=False)
            self.output = nn.Linear(config.heads * linear_dim, config.dimensions)
            self.relative_position = nn.Embedding(
                config.relative_buckets, config.heads
            )

        def forward(self, hidden):
            batch, length, _ = hidden.shape
            normalized = torch.nn.functional.layer_norm(
                hidden, (config.dimensions,)
            )
            projected = torch.nn.functional.silu(self.uvqk(normalized))
            widths = [
                config.heads * linear_dim,
                config.heads * linear_dim,
                config.heads * head_dim,
                config.heads * head_dim,
            ]
            u, v, q, k = torch.split(projected, widths, dim=-1)
            u = u.view(batch, length, config.heads, linear_dim)
            v = v.view(batch, length, config.heads, linear_dim)
            q = q.view(batch, length, config.heads, head_dim)
            k = k.view(batch, length, config.heads, head_dim)
            scores = torch.einsum("bthd,bshd->bhts", q, k)
            positions = torch.arange(length, device=hidden.device)
            distance = (positions[:, None] - positions[None, :]).clamp(
                0, config.relative_buckets - 1
            )
            bias = self.relative_position(distance).permute(2, 0, 1)
            causal = positions[:, None] >= positions[None, :]
            weights = torch.nn.functional.silu(scores + bias.unsqueeze(0)) / length
            weights = weights * causal[None, None]
            aggregated = torch.einsum("bhts,bshd->bthd", weights, v)
            aggregated = torch.nn.functional.layer_norm(
                aggregated.flatten(2), (config.heads * linear_dim,)
            ).view_as(u)
            gated = (u * aggregated).flatten(2)
            return hidden + self.output(gated)

    class HSTU(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            nn.init.normal_(self.item.weight, std=0.02)
            nn.init.normal_(self.position.weight, std=0.02)
            self.layers = nn.ModuleList([HSTULayer() for _ in range(config.layers)])
            self.final_norm = nn.LayerNorm(config.dimensions)

        def forward(self, items):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.item(items) + self.position(positions)
            for layer in self.layers:
                hidden = layer(hidden)
            return self.final_norm(hidden) @ self.item.weight.T

    return HSTU()


def train_model(data, config: HSTUConfig, seed: int):
    return train_sequence_model(
        build_model(data.item_count, config),
        data,
        config,
        seed,
        loss_kind="sampled_softmax",
    )
