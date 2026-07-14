from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training, training_examples
from ..sequence_training import padded_windows


@dataclass(frozen=True)
class PinFMConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    sequence_length: int = 32
    batch_size: int = 40
    pretrain_steps: int = 160
    finetune_steps: int = 160
    learning_rate: float = 5e-4
    future_window: int = 3
    mtl_weight: float = 0.5
    ftl_weight: float = 0.5
    finetune_ntl_weight: float = 0.1
    candidate_randomization: float = 0.1
    candidate_chunk: int = 384


def build_model(item_count: int, item_features: np.ndarray, config: PinFMConfig):
    torch, nn = require_backend()
    head_dim = config.dimensions // config.heads

    class DCATLayer(nn.Module):
        def __init__(self):
            super().__init__()
            self.norm1 = nn.LayerNorm(config.dimensions)
            self.query = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.key = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.value = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.output = nn.Linear(config.dimensions, config.dimensions)
            self.norm2 = nn.LayerNorm(config.dimensions)
            self.ffn = nn.Sequential(
                nn.Linear(config.dimensions, 4 * config.dimensions), nn.GELU(),
                nn.Linear(4 * config.dimensions, config.dimensions),
            )

        def split(self, values):
            return values.view(*values.shape[:-1], config.heads, head_dim).transpose(1, 2)

        def context(self, hidden):
            normalized = self.norm1(hidden)
            q = self.split(self.query(normalized))
            k = self.split(self.key(normalized))
            v = self.split(self.value(normalized))
            attended = torch.nn.functional.scaled_dot_product_attention(
                q, k, v, is_causal=True
            ).transpose(1, 2).flatten(2)
            hidden = hidden + self.output(attended)
            return hidden + self.ffn(self.norm2(hidden)), (k, v)

        def candidates(self, hidden, cache):
            # Algebraically equivalent to appending each candidate after a causal
            # user sequence, while reusing the de-duplicated context K/V once.
            batch, candidates, _ = hidden.shape
            normalized = self.norm1(hidden)
            q = self.query(normalized).view(batch, candidates, config.heads, head_dim)
            own_k = self.key(normalized).view(batch, candidates, config.heads, head_dim)
            own_v = self.value(normalized).view(batch, candidates, config.heads, head_dim)
            context_k, context_v = cache
            context_logits = torch.einsum("bchd,bhld->bchl", q, context_k)
            own_logits = (q * own_k).sum(-1, keepdim=True)
            weights = torch.softmax(
                torch.cat((context_logits, own_logits), dim=-1) / head_dim**0.5, dim=-1
            )
            context_weights, own_weights = weights[..., :-1], weights[..., -1:]
            attended = torch.einsum("bchl,bhld->bchd", context_weights, context_v)
            attended = attended + own_weights * own_v
            hidden = hidden + self.output(attended.flatten(2))
            return hidden + self.ffn(self.norm2(hidden))

    class PinFM(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            self.input_mlp = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, config.dimensions), nn.LayerNorm(config.dimensions),
            )
            self.output_mlp = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, config.dimensions), nn.LayerNorm(config.dimensions),
            )
            self.target_mlp = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, config.dimensions),
            )
            self.content = nn.Linear(item_features.shape[1], config.dimensions, bias=False)
            self.layers = nn.ModuleList([DCATLayer() for _ in range(config.layers)])
            self.rank = nn.Sequential(
                nn.Linear(3 * config.dimensions, 80), nn.ReLU(), nn.Linear(80, 1)
            )
            self.temperature_logit = nn.Parameter(torch.tensor(-2.3))
            self.register_buffer("features", torch.tensor(item_features, dtype=torch.float32))
            nn.init.normal_(self.item.weight, std=0.02)
            nn.init.normal_(self.position.weight, std=0.02)

        def encode_context(self, items):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.input_mlp(self.item(items)) + self.position(positions)
            caches = []
            for layer in self.layers:
                hidden, cache = layer.context(hidden)
                caches.append(cache)
            return self.output_mlp(hidden), caches

        def score(self, histories, candidate_ids, feature_ids=None):
            if candidate_ids.ndim == 1:
                candidate_ids = candidate_ids[:, None]
            if feature_ids is None:
                feature_ids = candidate_ids
            elif feature_ids.ndim == 1:
                feature_ids = feature_ids[:, None]
            context, caches = self.encode_context(histories)
            candidate = self.input_mlp(
                self.item(candidate_ids) + self.content(self.features[feature_ids])
            )
            for layer, cache in zip(self.layers, caches):
                candidate = layer.candidates(candidate, cache)
            candidate = self.output_mlp(candidate)
            user = context[:, -1:, :].expand_as(candidate)
            logits = self.rank(torch.cat((user, candidate, user * candidate), dim=-1)).squeeze(-1)
            return logits

        def contrastive(self, source, target_ids, valid):
            source = source[valid]
            target_ids = target_ids[valid]
            if source.shape[0] == 0:
                return source.sum()
            source = torch.nn.functional.normalize(source, dim=-1)
            target = torch.nn.functional.normalize(
                self.target_mlp(self.item(target_ids)), dim=-1
            )
            temperature = torch.nn.functional.softplus(self.temperature_logit) + 1e-3
            logits = source @ target.T / temperature
            labels = torch.arange(logits.shape[0], device=logits.device)
            return torch.nn.functional.cross_entropy(logits, labels)

        def sequence_losses(self, items, valid):
            hidden, _ = self.encode_context(items)
            ntl = self.contrastive(hidden[:, :-1], items[:, 1:], valid[:, 1:])
            mtl_terms = [
                self.contrastive(hidden[:, :-offset], items[:, offset:], valid[:, offset:])
                for offset in range(2, config.future_window + 1)
            ]
            mtl = sum(mtl_terms) / len(mtl_terms)
            anchor = hidden[:, -(config.future_window + 1), :]
            future = items[:, -config.future_window:]
            future_valid = valid[:, -config.future_window:]
            repeated = anchor[:, None, :].expand(-1, config.future_window, -1)
            ftl = self.contrastive(repeated, future, future_valid)
            return ntl, mtl, ftl

    return PinFM()


def pretrain_model(data, config: PinFMConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model, device, torch = initialize(build_model(data.item_count, data.item_features, config), seed)
    rows = padded_windows(data.train, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.train()
    for _ in range(config.pretrain_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        items = torch.tensor([row[0] for row in batch], device=device)
        valid = torch.tensor([row[2] for row in batch], dtype=torch.bool, device=device)
        ntl, mtl, ftl = model.sequence_losses(items, valid)
        loss = ntl + config.mtl_weight * mtl + config.ftl_weight * ftl
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def finetune_model(model, kind, data, config: PinFMConfig, seed: int):
    model, device, torch = initialize(model, seed)
    rows = training_examples(data.train, config.sequence_length)
    rng = random.Random(seed + 7919)
    if kind == "pinfm":
        head_parameters = list(model.rank.parameters())
        head_ids = {id(parameter) for parameter in head_parameters}
        backbone = [parameter for parameter in model.parameters() if id(parameter) not in head_ids]
        optimizer = torch.optim.AdamW([
            {"params": backbone, "lr": config.learning_rate / 10},
            {"params": head_parameters, "lr": config.learning_rate},
        ])
    else:
        optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.train()
    for _ in range(config.finetune_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], device=device)
        positives = torch.tensor([row[1] for row in batch], device=device)
        negatives = torch.randint(0, data.item_count, positives.shape, device=device)
        lookup = positives
        if kind == "pinfm":
            randomized = torch.rand(positives.shape, device=device) < config.candidate_randomization
            lookup = torch.where(
                randomized, torch.randint(0, data.item_count, positives.shape, device=device), positives
            )
        positive_logits = model.score(histories, lookup, positives).squeeze(-1)
        negative_logits = model.score(histories, negatives).squeeze(-1)
        loss = -torch.nn.functional.logsigmoid(positive_logits).mean()
        loss -= torch.nn.functional.logsigmoid(-negative_logits).mean()
        if kind == "pinfm":
            valid = torch.ones_like(histories, dtype=torch.bool)
            ntl, _, _ = model.sequence_losses(histories, valid)
            loss = loss + config.finetune_ntl_weight * ntl
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def train_scratch(data, config: PinFMConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    return finetune_model(
        build_model(data.item_count, data.item_features, config), "scratch_dcat", data, config, seed
    )


def score_all(model, history, item_count: int, config: PinFMConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    recent = history[-config.sequence_length:]
    padded = (recent[0],) * (config.sequence_length - len(recent)) + recent
    histories = torch.tensor([padded], device=device)
    scores = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, item_count, config.candidate_chunk):
            candidates = torch.arange(start, min(start + config.candidate_chunk, item_count), device=device)[None]
            scores.append(model.score(histories, candidates)[0].cpu().numpy())
    return np.concatenate(scores)


def score_batch(model, histories, item_count: int, config: PinFMConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    padded = []
    for history in histories:
        recent = history[-config.sequence_length:]
        padded.append((recent[0],) * (config.sequence_length - len(recent)) + recent)
    user_histories = torch.tensor(padded, device=device)
    candidates = torch.arange(item_count, device=device)[None].expand(len(histories), -1)
    model.eval()
    with torch.inference_mode():
        return model.score(user_histories, candidates).cpu().numpy()
