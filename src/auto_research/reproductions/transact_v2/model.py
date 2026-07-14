from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training, training_examples


@dataclass(frozen=True)
class TransActV2Config:
    dimensions: int = 48
    heads: int = 2
    layers: int = 2
    lifelong_length: int = 96
    realtime_length: int = 24
    recent_length: int = 6
    nearest_lifelong: int = 12
    nearest_realtime: int = 6
    batch_size: int = 48
    steps: int = 160
    learning_rate: float = 4e-4
    nal_weight: float = 0.25
    nal_negatives: int = 16
    candidate_chunk: int = 2048

    @property
    def selected_length(self):
        return self.nearest_lifelong + self.nearest_realtime + self.recent_length


def build_model(kind: str, item_count: int, item_features: np.ndarray, config: TransActV2Config):
    torch, nn = require_backend()
    content = torch.tensor(item_features, dtype=torch.float32)

    class TransActV2(nn.Module):
        def __init__(self):
            super().__init__()
            self.kind = kind
            self.item = nn.Embedding(item_count, config.dimensions)
            self.content_projection = nn.Linear(item_features.shape[1], config.dimensions, bias=False)
            self.early_fusion = nn.Linear(2 * config.dimensions, config.dimensions)
            self.position = nn.Embedding(config.selected_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 2 * config.dimensions,
                dropout=0.0, batch_first=True, norm_first=True,
            )
            self.encoder = nn.TransformerEncoder(layer, config.layers)
            self.rank = nn.Sequential(
                nn.Linear(3 * config.dimensions, 64), nn.ReLU(), nn.Linear(64, 1)
            )
            self.nal_projection = nn.Linear(config.dimensions, config.dimensions)
            self.register_buffer("features", content)
            nn.init.normal_(self.item.weight, std=0.02)
            nn.init.normal_(self.position.weight, std=0.02)

        def item_vector(self, items):
            return self.item(items) + self.content_projection(self.features[items])

        def select(self, histories, candidates):
            if self.kind == "transact":
                selected = histories[:, -config.selected_length:]
                if selected.shape[1] < config.selected_length:
                    padding = selected[:, :1].expand(-1, config.selected_length - selected.shape[1])
                    selected = torch.cat((padding, selected), dim=1)
                return selected
            history_features = self.features[histories]
            candidate_features = self.features[candidates]
            similarity = torch.einsum("blf,bf->bl", history_features, candidate_features)
            long_end = max(0, histories.shape[1] - config.realtime_length)
            realtime_start = max(0, histories.shape[1] - config.realtime_length)
            recent_start = max(0, histories.shape[1] - config.recent_length)

            def choose(start, end, count):
                values = similarity[:, start:end]
                if values.shape[1] == 0:
                    return histories[:, :1].expand(-1, count)
                k = min(count, values.shape[1])
                indices = values.topk(k, dim=1).indices + start
                indices = indices.sort(dim=1).values
                picked = histories.gather(1, indices)
                if k < count:
                    picked = torch.cat((picked[:, :1].expand(-1, count - k), picked), dim=1)
                return picked

            lifelong = choose(0, long_end, config.nearest_lifelong)
            realtime = choose(realtime_start, recent_start, config.nearest_realtime)
            recent = histories[:, recent_start:]
            if recent.shape[1] < config.recent_length:
                recent = torch.cat(
                    (recent[:, :1].expand(-1, config.recent_length - recent.shape[1]), recent), dim=1
                )
            return torch.cat((lifelong, realtime, recent), dim=1)

        def encode(self, histories, candidates):
            selected = self.select(histories, candidates)
            history = self.item_vector(selected)
            candidate = self.item_vector(candidates)
            fused = self.early_fusion(torch.cat(
                (history, candidate[:, None, :].expand_as(history)), dim=-1
            ))
            positions = torch.arange(fused.shape[1], device=fused.device)
            causal = torch.triu(
                torch.ones(fused.shape[1], fused.shape[1], device=fused.device), diagonal=1
            ).bool()
            return self.encoder(fused + self.position(positions), mask=causal)

        def forward(self, histories, candidates):
            encoded = self.encode(histories, candidates)
            pooled = encoded.max(dim=1).values
            candidate = self.item_vector(candidates)
            joined = torch.cat((pooled, candidate, pooled * candidate), dim=-1)
            return self.rank(joined).squeeze(-1)

        def nal_loss(self, histories):
            sequence = histories[:, -config.realtime_length:]
            source, targets = sequence[:, :-1], sequence[:, 1:]
            token = self.item_vector(source)
            positions = torch.arange(token.shape[1], device=token.device)
            causal = torch.triu(
                torch.ones(token.shape[1], token.shape[1], device=token.device), diagonal=1
            ).bool()
            # NAL shares the same transformer. A zero candidate channel represents
            # the paper's candidate-independent next-action auxiliary task.
            fused = self.early_fusion(torch.cat((token, torch.zeros_like(token)), dim=-1))
            hidden = self.encoder(fused + self.position(positions), mask=causal)
            query = self.nal_projection(hidden)
            positive = self.item_vector(targets)
            negative_ids = torch.randint(
                0, item_count, (*targets.shape, config.nal_negatives), device=targets.device
            )
            negative = self.item_vector(negative_ids)
            positive_logits = (query * positive).sum(-1, keepdim=True)
            negative_logits = torch.einsum("bld,blnd->bln", query, negative)
            logits = torch.cat((positive_logits, negative_logits), dim=-1)
            labels = torch.zeros(logits.shape[:-1], dtype=torch.long, device=targets.device)
            return torch.nn.functional.cross_entropy(
                logits.flatten(0, 1), labels.flatten()
            )

    return TransActV2()


def train_model(kind, data, config: TransActV2Config, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model, device, torch = initialize(
        build_model(kind, data.item_count, data.item_features, config), seed
    )
    rows = training_examples(data.train, config.lifelong_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], device=device)
        positives = torch.tensor([row[1] for row in batch], device=device)
        negatives = torch.randint(0, data.item_count, positives.shape, device=device)
        positive_logits = model(histories, positives)
        negative_logits = model(histories, negatives)
        loss = -torch.nn.functional.logsigmoid(positive_logits).mean()
        loss -= torch.nn.functional.logsigmoid(-negative_logits).mean()
        if kind == "transact_v2":
            loss = loss + config.nal_weight * model.nal_loss(histories)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def score_all(model, history, item_count: int, config: TransActV2Config):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    recent = history[-config.lifelong_length:]
    padded = (recent[0],) * (config.lifelong_length - len(recent)) + recent
    histories = torch.tensor([padded], device=device)
    scores = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, item_count, config.candidate_chunk):
            candidates = torch.arange(start, min(start + config.candidate_chunk, item_count), device=device)
            expanded = histories.expand(len(candidates), -1)
            scores.append(model(expanded, candidates).cpu().numpy())
    return np.concatenate(scores)


def score_batch(model, histories, item_count: int, config: TransActV2Config):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    padded = []
    for history in histories:
        recent = history[-config.lifelong_length:]
        padded.append((recent[0],) * (config.lifelong_length - len(recent)) + recent)
    user_histories = torch.tensor(padded, device=device)
    outputs = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, item_count, config.candidate_chunk):
            candidates = torch.arange(
                start, min(start + config.candidate_chunk, item_count), device=device
            )
            count = len(candidates)
            expanded_histories = user_histories[:, None, :].expand(-1, count, -1).flatten(0, 1)
            expanded_candidates = candidates[None, :].expand(len(histories), -1).flatten()
            scores = model(expanded_histories, expanded_candidates)
            outputs.append(scores.view(len(histories), count).cpu().numpy())
    return np.concatenate(outputs, axis=1)
