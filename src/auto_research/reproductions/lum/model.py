from __future__ import annotations

from auto_research.runtime import device_for

import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ...datasets import movielens_1m
from ..industrial_ranking import require_backend
from ..llm_rec_data import binary_auc


@dataclass(frozen=True)
class LUMRow:
    user: int
    history_items: tuple[int, ...]
    history_conditions: tuple[int, ...]
    condition: int
    candidate: int
    label: int


@dataclass(frozen=True)
class LUMData:
    train: tuple[LUMRow, ...]
    test: tuple[LUMRow, ...]
    pretrain: tuple[LUMRow, ...]
    item_features: np.ndarray
    users: int
    items: int
    conditions: int = 3


@dataclass(frozen=True)
class LUMConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    history_length: int = 16
    maximum_users: int = 1000
    pretrain_steps: int = 200
    ranker_steps: int = 160
    batch_size: int = 64
    learning_rate: float = 5e-4
    maximum_train: int = 6000
    maximum_test: int = 1500


def load_lum_data(root: Path, maximum_users: int = 1000) -> LUMData:
    ratings = movielens_1m(root)
    raw_users = sorted({row[0] for row in ratings})[:maximum_users]
    user_ids = {user: index for index, user in enumerate(raw_users)}
    raw_items = sorted({row[1] for row in ratings if row[0] in user_ids})
    item_ids = {item: index for index, item in enumerate(raw_items)}
    by_user = {user: [] for user in raw_users}
    for user, item, rating, timestamp in ratings:
        if user in by_user:
            by_user[user].append((timestamp, item_ids[item], _condition(rating)))
    train, test, pretrain = [], [], []
    for raw_user, events in by_user.items():
        events.sort()
        split = max(3, int(0.8 * len(events)))
        rows = []
        for position in range(2, len(events)):
            history = events[max(0, position - 32) : position]
            row = LUMRow(
                user_ids[raw_user], tuple(x[1] for x in history), tuple(x[2] for x in history),
                events[position][2], events[position][1], int(events[position][2] >= 1),
            )
            rows.append(row)
            if position < split:
                pretrain.append(row)
        train.extend(rows[: max(0, split - 2)])
        test.extend(rows[max(0, split - 2) :])
    return LUMData(tuple(train), tuple(test), tuple(pretrain), _features(root, raw_items), len(raw_users), len(raw_items))


def _condition(rating: float) -> int:
    return 2 if rating >= 4 else 1 if rating == 3 else 0


def _features(root: Path, raw_items: list[int]):
    genres = (root / "ml-1m" / "movies.dat").read_text(encoding="latin-1").splitlines()
    names = sorted({genre for line in genres for genre in line.split("::")[2].split("|")})
    genre_ids = {name: index for index, name in enumerate(names)}
    rows = {}
    for line in genres:
        item, _, values = line.split("::")
        vector = np.zeros(len(names), dtype=np.float32)
        for value in values.split("|"):
            vector[genre_ids[value]] = 1
        rows[int(item)] = vector
    return np.stack([rows[item] for item in raw_items])


def build_lum(data: LUMData, config: LUMConfig):
    torch, nn = require_backend()

    class LUM(nn.Module):
        def __init__(self):
            super().__init__()
            self.item_id = nn.Embedding(data.items + 1, config.dimensions, padding_idx=data.items)
            self.condition = nn.Embedding(data.conditions, config.dimensions)
            self.feature = nn.Linear(data.item_features.shape[1], config.dimensions)
            self.register_buffer("item_features", torch.tensor(data.item_features))
            self.position = nn.Embedding(2 * config.history_length + data.conditions, config.dimensions)
            layer = nn.TransformerEncoderLayer(config.dimensions, config.heads, 4 * config.dimensions, batch_first=True, norm_first=True, dropout=0.0)
            self.encoder = nn.TransformerEncoder(layer, config.layers)
            self.norm = nn.LayerNorm(config.dimensions)

        def item_embedding(self, items):
            safe = items.clamp_max(data.items - 1)
            value = self.item_id(items)
            content = self.feature(self.item_features[safe])
            return value + content * (items != data.items).unsqueeze(-1)

        def query(self, histories, conditions, query_conditions):
            batch, width = histories.shape
            prefix_width = 2 * width
            query_count = query_conditions.shape[1]
            values = torch.zeros(batch, prefix_width + query_count, config.dimensions, device=histories.device)
            values[:, 0:prefix_width:2] = self.condition(conditions)
            values[:, 1:prefix_width:2] = self.item_embedding(histories)
            values[:, prefix_width:] = self.condition(query_conditions)
            values = values + self.position(torch.arange(values.shape[1], device=values.device))
            padding = torch.zeros(batch, values.shape[1], dtype=torch.bool, device=values.device)
            history_padding = histories == data.items
            padding[:, 0:prefix_width:2] = history_padding
            padding[:, 1:prefix_width:2] = history_padding
            mask = torch.ones((values.shape[1], values.shape[1]), dtype=torch.bool, device=values.device)
            mask[:prefix_width, :prefix_width] = torch.triu(
                torch.ones((prefix_width, prefix_width), dtype=torch.bool, device=values.device), diagonal=1
            )
            for index in range(query_count):
                position = prefix_width + index
                mask[position, :prefix_width] = False
                mask[position, position] = False
            hidden = self.encoder(values, mask=mask, src_key_padding_mask=padding)
            return self.norm(hidden[:, prefix_width:])

    return LUM()


def _collate(rows, data, config, device, torch):
    width = config.history_length
    items = torch.full((len(rows), width), data.items, dtype=torch.long, device=device)
    conditions = torch.zeros((len(rows), width), dtype=torch.long, device=device)
    for index, row in enumerate(rows):
        hi, hc = row.history_items[-width:], row.history_conditions[-width:]
        items[index, -len(hi) :] = torch.tensor(hi, device=device)
        conditions[index, -len(hc) :] = torch.tensor(hc, device=device)
    return items, conditions


def pretrain_lum(data: LUMData, config: LUMConfig, seed: int):
    torch, _ = require_backend()
    torch.manual_seed(seed); np.random.seed(seed)
    rng = random.Random(seed)
    device = device_for(torch)
    model = build_lum(data, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    model.train()
    for _ in range(config.pretrain_steps):
        rows = [data.pretrain[rng.randrange(len(data.pretrain))] for _ in range(config.batch_size)]
        histories, conditions = _collate(rows, data, config, device, torch)
        queries = torch.tensor([[row.condition] for row in rows], device=device)
        output = model.query(histories, conditions, queries).squeeze(1)
        targets = torch.tensor([row.candidate for row in rows], device=device)
        target_embeddings = model.item_embedding(targets)
        logits = output @ target_embeddings.T / np.sqrt(config.dimensions)
        loss = torch.nn.functional.cross_entropy(logits, torch.arange(len(rows), device=device))
        optimizer.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:]))}


def query_knowledge(model, rows, data, config):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    outputs = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            batch = rows[start : start + config.batch_size]
            histories, conditions = _collate(batch, data, config, device, torch)
            queries = torch.arange(data.conditions, device=device).unsqueeze(0).expand(len(batch), -1)
            outputs.append(model.query(histories, conditions, queries).cpu())
        item_embeddings = model.item_embedding(torch.arange(data.items, device=device)).cpu()
    return torch.cat(outputs).numpy(), item_embeddings.numpy()


def build_ranker(data, knowledge, item_knowledge, config: LUMConfig, use_lum: bool):
    torch, nn = require_backend()

    class Ranker(nn.Module):
        def __init__(self):
            super().__init__()
            self.user = nn.Embedding(data.users, config.dimensions)
            self.item = nn.Embedding(data.items, config.dimensions)
            self.register_buffer("knowledge", torch.tensor(knowledge))
            self.register_buffer("item_knowledge", torch.tensor(item_knowledge))
            extra = data.conditions * config.dimensions + config.dimensions + data.conditions if use_lum else 0
            self.head = nn.Sequential(nn.Linear(3 * config.dimensions + extra, 2 * config.dimensions), nn.GELU(), nn.Linear(2 * config.dimensions, 1))

        def forward(self, row_indices, users, items):
            user, item = self.user(users), self.item(items)
            values = [user, item, user * item]
            if use_lum:
                queries = self.knowledge[row_indices]
                target = self.item_knowledge[items]
                similarities = torch.nn.functional.cosine_similarity(queries, target.unsqueeze(1), dim=-1)
                values.extend((queries.flatten(1), target, similarities))
            return self.head(torch.cat(values, -1)).squeeze(-1)

    return Ranker()


def train_ranker(model, train, test, config: LUMConfig, seed: int):
    torch, _ = require_backend()
    torch.manual_seed(seed); rng = random.Random(seed)
    device = device_for(torch)
    model.to(device); optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    train_count = min(len(train), config.maximum_train)
    losses = []; started = time.perf_counter()
    for _ in range(config.ranker_steps):
        indices = [rng.randrange(train_count) for _ in range(config.batch_size)]
        rows = [train[index] for index in indices]
        logits = model(torch.tensor(indices, device=device), torch.tensor([r.user for r in rows], device=device), torch.tensor([r.candidate for r in rows], device=device))
        labels = torch.tensor([r.label for r in rows], dtype=torch.float32, device=device)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step(); losses.append(float(loss.detach().cpu()))
    labels, scores = [], []; model.eval()
    test_rows = test[: config.maximum_test]
    offset = len(train)
    with torch.inference_mode():
        for start in range(0, len(test_rows), config.batch_size):
            rows = test_rows[start : start + config.batch_size]
            indices = torch.arange(offset + start, offset + start + len(rows), device=device)
            logits = model(indices, torch.tensor([r.user for r in rows], device=device), torch.tensor([r.candidate for r in rows], device=device))
            scores.extend(torch.sigmoid(logits).cpu().tolist()); labels.extend(r.label for r in rows)
    return {"auc": binary_auc(labels, scores), "initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])), "seconds": time.perf_counter() - started}
