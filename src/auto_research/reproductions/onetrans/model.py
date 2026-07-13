from __future__ import annotations

import math
import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import NeuralRankingConfig, require_backend, summarize_training


@dataclass(frozen=True)
class OneTransConfig(NeuralRankingConfig):
    non_sequence_tokens: int = 2
    negatives: int = 15
    batch_size: int = 32


def build_model(kind: str, data, config: OneTransConfig):
    torch, nn = require_backend()
    features = torch.tensor(data.item_features, dtype=torch.float32)
    item_count, feature_count = features.shape

    class EncodeThenInteract(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.sequence = nn.TransformerEncoder(layer, config.layers)
            self.score = nn.Sequential(
                nn.Linear(2 * config.dimensions + 2 * feature_count, config.dimensions),
                nn.GELU(), nn.Linear(config.dimensions, 1),
            )
            self.register_buffer("features", features)

        def pair_scores(self, history, candidates):
            user = self.sequence(self.item(history))[:, -1]
            profile = self.features[history].mean(dim=1)
            count = candidates.shape[1]
            user = user[:, None].expand(-1, count, -1)
            profile = profile[:, None].expand(-1, count, -1)
            candidate = self.item(candidates)
            values = torch.cat((user, candidate, profile, self.features[candidates]), dim=-1)
            return self.score(values).squeeze(-1)

        def forward(self, history):
            candidates = torch.arange(item_count, device=history.device)[None].expand(len(history), -1)
            return self.pair_scores(history, candidates)

    class RMSNorm(nn.Module):
        def __init__(self):
            super().__init__()
            self.weight = nn.Parameter(torch.ones(config.dimensions))

        def forward(self, values):
            scale = torch.rsqrt(values.square().mean(dim=-1, keepdim=True) + 1e-6)
            return values * scale * self.weight

    class MixedBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.norm_attention = RMSNorm()
            self.norm_ffn = RMSNorm()
            self.shared_qkv = nn.Linear(config.dimensions, 3 * config.dimensions)
            self.ns_qkv = nn.ModuleList([
                nn.Linear(config.dimensions, 3 * config.dimensions)
                for _ in range(config.non_sequence_tokens)
            ])
            self.output = nn.Linear(config.dimensions, config.dimensions)
            self.shared_ffn = nn.Sequential(
                nn.Linear(config.dimensions, 4 * config.dimensions), nn.GELU(),
                nn.Linear(4 * config.dimensions, config.dimensions),
            )
            self.ns_ffn = nn.ModuleList([
                nn.Sequential(
                    nn.Linear(config.dimensions, 4 * config.dimensions), nn.GELU(),
                    nn.Linear(4 * config.dimensions, config.dimensions),
                ) for _ in range(config.non_sequence_tokens)
            ])

        def forward(self, values, sequence_tokens):
            normalized = self.norm_attention(values)
            sequence_qkv = self.shared_qkv(normalized[:, :sequence_tokens])
            ns_qkv = torch.stack([
                projection(normalized[:, sequence_tokens + token])
                for token, projection in enumerate(self.ns_qkv)
            ], dim=1)
            qkv = torch.cat((sequence_qkv, ns_qkv), dim=1)
            query, key, value = qkv.chunk(3, dim=-1)
            batch, length, _ = query.shape
            head_width = config.dimensions // config.heads
            query = query.reshape(batch, length, config.heads, head_width).transpose(1, 2)
            key = key.reshape(batch, length, config.heads, head_width).transpose(1, 2)
            value = value.reshape(batch, length, config.heads, head_width).transpose(1, 2)
            scores = query @ key.transpose(-1, -2) / math.sqrt(head_width)
            causal = torch.triu(torch.ones(length, length, device=values.device), diagonal=1).bool()
            scores = scores.masked_fill(causal, -torch.inf)
            attention = torch.softmax(scores, dim=-1) @ value
            attention = attention.transpose(1, 2).reshape(batch, length, config.dimensions)
            values = values + self.output(attention)
            normalized = self.norm_ffn(values)
            sequence = self.shared_ffn(normalized[:, :sequence_tokens])
            non_sequence = torch.stack([
                network(normalized[:, sequence_tokens + token])
                for token, network in enumerate(self.ns_ffn)
            ], dim=1)
            return values + torch.cat((sequence, non_sequence), dim=1)

    class OneTrans(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            self.user_token = nn.Linear(feature_count, config.dimensions)
            self.candidate_token = nn.Linear(
                config.dimensions + feature_count, config.dimensions
            )
            self.blocks = nn.ModuleList([MixedBlock() for _ in range(config.layers)])
            self.head = nn.Linear(config.dimensions, 1)
            self.register_buffer("features", features)

        def pair_scores(self, history, candidates):
            batch, candidate_count = candidates.shape
            positions = torch.arange(history.shape[1], device=history.device)
            sequence = self.item(history) + self.position(positions)
            profile = self.features[history].mean(dim=1)
            user = self.user_token(profile)
            candidate = self.candidate_token(
                torch.cat((self.item(candidates), self.features[candidates]), dim=-1)
            )
            sequence = sequence[:, None].expand(-1, candidate_count, -1, -1)
            user = user[:, None, None].expand(-1, candidate_count, 1, -1)
            values = torch.cat((sequence, user, candidate[:, :, None]), dim=2)
            values = values.reshape(batch * candidate_count, values.shape[2], config.dimensions)
            sequence_tokens = history.shape[1]
            for layer, block in enumerate(self.blocks):
                values = block(values, sequence_tokens)
                if layer + 1 < len(self.blocks):
                    keep = max(2, sequence_tokens // 2)
                    values = torch.cat((values[:, sequence_tokens - keep : sequence_tokens], values[:, sequence_tokens:]), dim=1)
                    sequence_tokens = keep
            return self.head(values[:, -1]).reshape(batch, candidate_count)

        def forward(self, history):
            candidates = torch.arange(item_count, device=history.device)[None].expand(len(history), -1)
            return self.pair_scores(history, candidates)

    if kind == "encode_then_interact":
        return EncodeThenInteract()
    if kind == "onetrans":
        return OneTrans()
    raise ValueError(f"unknown OneTrans kind: {kind}")


def train_model(kind: str, data, config: OneTransConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = build_model(kind, data, config).to(device)
    from ..industrial_ranking import training_examples

    rows = training_examples(data.train, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        history = torch.tensor([row[0] for row in batch], dtype=torch.long, device=device)
        positive = torch.tensor([row[1] for row in batch], dtype=torch.long, device=device)
        negative = torch.randint(0, data.item_count, (config.batch_size, config.negatives), device=device)
        candidates = torch.cat((positive[:, None], negative), dim=1)
        logits = model.pair_scores(history, candidates)
        labels = torch.zeros_like(logits)
        labels[:, 0] = 1.0
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)
