from __future__ import annotations

from auto_research.runtime import device_for

import random
from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True)
class G2RecConfig:
    interests: int = 12
    dimensions: int = 96
    heads: int = 4
    layers: int = 2
    sequence_length: int = 20
    graph_steps: int = 120
    training_steps: int = 240
    batch_size: int = 48
    learning_rate: float = 3e-4
    profile_weight: float = 0.1
    evaluation_users: int = 1000


def require_backend():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError(
            "G2Rec trains its soft graph clusters and autoregressive decoder; "
            "install with `pip install -e '.[neural-recs]'`."
        ) from exc
    return torch, nn


def coengagement_edges(sequences, item_count: int, window: int = 3):
    weights: dict[tuple[int, int], float] = {}
    degree = np.zeros(item_count, dtype=np.float32)
    for sequence in sequences:
        for position, left in enumerate(sequence):
            for right in sequence[position + 1 : position + 1 + window]:
                if left == right:
                    continue
                edge = (left, right) if left < right else (right, left)
                weights[edge] = weights.get(edge, 0.0) + 1.0
    edges = np.asarray(list(weights), dtype=np.int64)
    values = np.log1p(np.asarray(list(weights.values()), dtype=np.float32))
    if len(edges):
        np.add.at(degree, edges[:, 0], values)
        np.add.at(degree, edges[:, 1], values)
    return edges, values, degree


def train_soft_membership(data, config: G2RecConfig, seed: int):
    """Optimize the paper's edge-agreement minus degree-prior modularity."""

    torch, _ = require_backend()
    torch.manual_seed(seed)
    device = device_for(torch)
    edges, weights, degree = coengagement_edges(data.train, data.item_count)
    edge_tensor = torch.tensor(edges, dtype=torch.long, device=device)
    weight_tensor = torch.tensor(weights, dtype=torch.float32, device=device)
    degree_tensor = torch.tensor(degree, dtype=torch.float32, device=device)
    logits = torch.nn.Parameter(
        torch.randn(data.item_count, config.interests, device=device) * 0.01
    )
    optimizer = torch.optim.Adam([logits], lr=0.05)
    losses: list[float] = []
    total_degree = degree_tensor.sum().clamp_min(1.0)
    for _ in range(config.graph_steps):
        membership = torch.softmax(logits, dim=-1)
        agreement = (
            (membership[edge_tensor[:, 0]] * membership[edge_tensor[:, 1]]).sum(-1)
            * weight_tensor
        ).sum() / weight_tensor.sum().clamp_min(1.0)
        cluster_mass = (membership * degree_tensor[:, None]).sum(dim=0) / total_degree
        modularity = agreement - torch.square(cluster_mass).sum()
        entropy = -(membership * membership.clamp_min(1e-8).log()).sum(-1).mean()
        loss = -modularity + 0.01 * entropy
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    membership = torch.softmax(logits, dim=-1).detach().cpu().numpy()
    return membership.astype(np.float32), {
        "edges": len(edges),
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "soft_modularity": float(modularity.detach().cpu()),
    }


def build_model(kind: str, item_count: int, membership: np.ndarray, config: G2RecConfig):
    torch, nn = require_backend()
    profile_values = torch.tensor(membership, dtype=torch.float32)

    class ItemOnlyDecoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.decoder = nn.TransformerEncoder(layer, config.layers)
            self.output = nn.Linear(config.dimensions, item_count, bias=False)
            self.output.weight = self.item.weight

        def forward(self, items):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.item(items) + self.position(positions)
            mask = torch.triu(
                torch.ones(items.shape[1], items.shape[1], device=items.device),
                diagonal=1,
            ).bool()
            return self.output(self.decoder(hidden, mask=mask))

    class InterestTokenDecoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.prototypes = nn.Parameter(
                torch.randn(config.interests, config.dimensions) * 0.02
            )
            self.position = nn.Embedding(2 * config.sequence_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.decoder = nn.TransformerEncoder(layer, config.layers)
            self.item_output = nn.Linear(config.dimensions, item_count, bias=False)
            self.item_output.weight = self.item.weight
            self.profile_output = nn.Linear(config.dimensions, config.interests)
            self.register_buffer("membership", profile_values)

        def forward(self, items):
            item_tokens = self.item(items)
            interest_tokens = self.membership[items] @ self.prototypes
            tokens = torch.stack((item_tokens, interest_tokens), dim=2).flatten(1, 2)
            positions = torch.arange(tokens.shape[1], device=items.device)
            mask = torch.triu(
                torch.ones(tokens.shape[1], tokens.shape[1], device=items.device),
                diagonal=1,
            ).bool()
            hidden = self.decoder(tokens + self.position(positions), mask=mask)
            item_hidden = hidden[:, 0::2]
            interest_hidden = hidden[:, 1::2]
            return self.item_output(interest_hidden), self.profile_output(item_hidden)

    if kind == "item_only":
        return ItemOnlyDecoder()
    if kind == "g2rec":
        return InterestTokenDecoder()
    raise ValueError(f"unknown G2Rec model kind: {kind}")


def sequence_windows(sequences, length: int):
    rows = []
    for sequence in sequences:
        for end in range(2, len(sequence) + 1):
            window = sequence[max(0, end - length) : end]
            if len(window) >= 2:
                rows.append(window)
    return tuple(rows)


def train_decoder(kind: str, data, membership, config: G2RecConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_model(kind, data.item_count, membership, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rows = sequence_windows(data.train, config.sequence_length)
    rng = random.Random(seed)
    losses: list[float] = []
    for _ in range(config.training_steps):
        selected = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        width = max(len(row) for row in selected)
        batch = [((row[0],) * (width - len(row)) + row) for row in selected]
        valid = torch.tensor(
            [[0.0] * (width - len(row)) + [1.0] * (len(row) - 1) for row in selected],
            dtype=torch.float32, device=device,
        )
        items = torch.tensor(batch, dtype=torch.long, device=device)
        optimizer.zero_grad(set_to_none=True)
        if kind == "item_only":
            logits = model(items[:, :-1])
            token_loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, data.item_count), items[:, 1:].reshape(-1),
                reduction="none",
            ).reshape_as(valid)
            loss = (token_loss * valid).sum() / valid.sum()
        else:
            logits, profile_logits = model(items[:, :-1])
            token_loss = torch.nn.functional.cross_entropy(
                logits.reshape(-1, data.item_count), items[:, 1:].reshape(-1),
                reduction="none",
            ).reshape_as(valid)
            item_loss = (token_loss * valid).sum() / valid.sum()
            profile_targets = torch.tensor(
                membership[items[:, :-1].detach().cpu().numpy()],
                dtype=torch.float32, device=device,
            )
            profile_token_loss = -(
                profile_targets * torch.log_softmax(profile_logits, dim=-1)
            ).sum(-1)
            profile_loss = (profile_token_loss * valid).sum() / valid.sum()
            loss = item_loss + config.profile_weight * profile_loss
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {
        "initial_loss": float(np.mean(losses[:20])),
        "final_loss": float(np.mean(losses[-20:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def next_item_logits(model: Any, kind: str, history: tuple[int, ...], config: G2RecConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    recent = history[-config.sequence_length :]
    items = torch.tensor([recent], dtype=torch.long, device=device)
    with torch.inference_mode():
        output = model(items)
        logits = output[0] if kind == "g2rec" else output
    return logits[0, -1].detach().cpu().numpy()
