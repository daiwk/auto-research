from __future__ import annotations

import copy
import csv
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ...datasets import kuairand_pure_files
from ..plum.model import residual_kmeans


@dataclass(frozen=True)
class OneRecV2Config:
    dimensions: int = 64
    heads: int = 4
    layers: int = 2
    history_items: int = 32
    batch_size: int = 64
    sft_steps: int = 160
    gbpo_steps: int = 80
    learning_rate: float = 5e-4
    maximum_events: int = 180_000
    maximum_examples: int = 36_000


@dataclass(frozen=True)
class KuaiExample:
    history: tuple[int, ...]
    target: int
    semantic_id: tuple[int, int, int]
    advantage: float


@dataclass(frozen=True)
class KuaiData:
    train: tuple[KuaiExample, ...]
    validation: tuple[KuaiExample, ...]
    item_codes: np.ndarray
    cardinalities: tuple[int, int, int]
    items: int
    events: int

    @property
    def sid_uniqueness(self) -> float:
        return len(set(map(tuple, self.item_codes))) / self.items


def require_backend():
    try:
        import torch
        from torch import nn
    except ImportError as exc:
        raise RuntimeError("OneRec-V2 requires `pip install -e '.[neural-recs]'`.") from exc
    return torch, nn


def load_kuairand_examples(root: Path, config: OneRecV2Config) -> KuaiData:
    directory = kuairand_pure_files(root)
    features = directory / "video_features_basic_pure.csv"
    raw: dict[int, tuple[int, str, float]] = {}
    with features.open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            video = int(row["video_id"])
            author = int(float(row["author_id"] or 0))
            tag = (row["tag"] or "unknown").split(",", 1)[0]
            raw[video] = (author, tag, float(row["video_duration"] or 0.0))
    videos = sorted(raw)
    item_index = {video: index for index, video in enumerate(videos)}
    tag_values = {value[1] for value in raw.values()}
    tags = {value: index for index, value in enumerate(sorted(tag_values))}
    # Train a real residual-quantized SID tokenizer over public content fields.
    # Tag is explicit, author uses a stable hash projection, and a fixed
    # identity projection stands in for the private multimodal video embedding.
    # Duration is log scaled to avoid dominating the content geometry.
    features = np.zeros((len(videos), len(tags) + 97), dtype=np.float64)
    identity = np.random.default_rng(17).normal(size=(len(videos), 32))
    identity /= np.maximum(np.linalg.norm(identity, axis=1, keepdims=True), 1e-8)
    for row, video in enumerate(videos):
        author, tag, duration = raw[video]
        features[row, tags[tag]] = 1.0
        features[row, len(tags) + author % 64] = 1.0
        features[row, len(tags) + 64: len(tags) + 96] = 2.0 * identity[row]
        features[row, -1] = math.log1p(max(duration, 0.0)) / 16.0
    codes, _ = residual_kmeans(features, (128, 64, 32), seed=17, iterations=12)
    by_user: dict[int, list[tuple[int, int, float, float, int]]] = {}
    log = directory / "log_standard_4_22_to_5_08_pure.csv"
    with log.open(encoding="utf-8") as stream:
        for number, row in enumerate(csv.DictReader(stream)):
            if number >= config.maximum_events:
                break
            video = int(row["video_id"])
            if video not in item_index:
                continue
            duration = max(float(row["duration_ms"] or 0.0), 1.0)
            play = max(float(row["play_time_ms"] or 0.0), 0.0)
            hate = int(row["is_hate"] or 0)
            by_user.setdefault(int(row["user_id"]), []).append(
                (int(row["time_ms"]), item_index[video], play, duration, hate)
            )

    examples: list[KuaiExample] = []
    for events in by_user.values():
        events.sort()
        # Paper DARS: percentiles are computed within user and duration bucket.
        buckets: dict[int, list[float]] = {}
        for _, _, play, duration, _ in events:
            bucket = int(math.floor(math.log(duration + 1e-3, 2)))
            buckets.setdefault(bucket, []).append(play)
        thresholds = {
            bucket: float(np.quantile(values, 0.75))
            for bucket, values in buckets.items()
        }
        history: list[int] = []
        for _, item, play, duration, hate in events:
            if history:
                bucket = int(math.floor(math.log(duration + 1e-3, 2)))
                advantage = -1.0 if hate else (1.0 if play >= thresholds[bucket] else 0.0)
                examples.append(
                    KuaiExample(tuple(history[-config.history_items:]), item, tuple(codes[item]), advantage)
                )
            history.append(item)
            if len(examples) >= config.maximum_examples:
                break
        if len(examples) >= config.maximum_examples:
            break
    split = int(0.85 * len(examples))
    return KuaiData(
        tuple(examples[:split]), tuple(examples[split:]), codes,
        (128, 64, 32), len(videos), sum(len(v) for v in by_user.values()),
    )


def build_lazy_decoder(data: KuaiData, config: OneRecV2Config):
    torch, nn = require_backend()

    class LazyBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.cross = nn.MultiheadAttention(config.dimensions, config.heads, batch_first=True)
            self.self_attention = nn.MultiheadAttention(config.dimensions, config.heads, batch_first=True)
            self.ffn = nn.Sequential(
                nn.Linear(config.dimensions, 4 * config.dimensions), nn.GELU(),
                nn.Linear(4 * config.dimensions, config.dimensions),
            )
            self.norms = nn.ModuleList([nn.RMSNorm(config.dimensions) for _ in range(3)])

        def forward(self, target, context):
            # The same context tensor is K and V, and is shared across layers.
            target = target + self.cross(self.norms[0](target), context, context, need_weights=False)[0]
            length = target.shape[1]
            mask = torch.triu(torch.ones(length, length, device=target.device, dtype=torch.bool), 1)
            target = target + self.self_attention(
                self.norms[1](target), self.norms[1](target), self.norms[1](target),
                attn_mask=mask, need_weights=False,
            )[0]
            return target + self.ffn(self.norms[2](target))

    class LazyDecoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.items, config.dimensions)
            self.context_projection = nn.Linear(config.dimensions, config.dimensions, bias=False)
            self.bos = nn.Parameter(torch.zeros(config.dimensions))
            self.level = nn.ModuleList(nn.Embedding(size, config.dimensions) for size in data.cardinalities)
            self.blocks = nn.ModuleList(LazyBlock() for _ in range(config.layers))
            self.output = nn.ModuleList(nn.Linear(config.dimensions, size) for size in data.cardinalities)

        def forward(self, histories, target_codes):
            context = self.context_projection(self.item(histories))
            parts = [self.bos.expand(histories.shape[0], 1, -1)]
            for level in range(2):
                parts.append(self.level[level](target_codes[:, level]).unsqueeze(1))
            hidden = torch.cat(parts, dim=1)
            for block in self.blocks:
                hidden = block(hidden, context)
            return tuple(head(hidden[:, level]) for level, head in enumerate(self.output))

    return LazyDecoder()


def build_encoder_decoder(data: KuaiData, config: OneRecV2Config):
    torch, nn = require_backend()

    class EncoderDecoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.items, config.dimensions)
            self.bos = nn.Parameter(torch.zeros(config.dimensions))
            self.level = nn.ModuleList(nn.Embedding(size, config.dimensions) for size in data.cardinalities)
            layer = nn.TransformerDecoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            encoder = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.encoder = nn.TransformerEncoder(encoder, config.layers)
            self.decoder = nn.TransformerDecoder(layer, config.layers)
            self.output = nn.ModuleList(nn.Linear(config.dimensions, size) for size in data.cardinalities)

        def forward(self, histories, target_codes):
            memory = self.encoder(self.item(histories))
            parts = [self.bos.expand(histories.shape[0], 1, -1)]
            for level in range(2):
                parts.append(self.level[level](target_codes[:, level]).unsqueeze(1))
            target = torch.cat(parts, dim=1)
            mask = torch.triu(torch.ones(3, 3, device=target.device, dtype=torch.bool), 1)
            hidden = self.decoder(target, memory, tgt_mask=mask)
            return tuple(head(hidden[:, level]) for level, head in enumerate(self.output))

    return EncoderDecoder()


def train_sft(model, rows, config: OneRecV2Config, seed: int):
    torch, _ = require_backend()
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    for _ in range(config.sft_steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories, codes = _batch(batch, config, device, torch)
        logits = model(histories, codes)
        loss = sum(torch.nn.functional.cross_entropy(score, codes[:, level]) for level, score in enumerate(logits))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])),
        "seconds": time.perf_counter() - started,
        "parameters": sum(value.numel() for value in model.parameters()), "device": device.type,
    }


def train_gbpo(model, rows, config: OneRecV2Config, seed: int):
    torch, _ = require_backend()
    reference = copy.deepcopy(model).eval()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate * 0.25)
    device = next(model.parameters()).device
    rng = random.Random(seed)
    losses = []
    informative = [row for row in rows if row.advantage]
    for _ in range(config.gbpo_steps):
        batch = [informative[rng.randrange(len(informative))] for _ in range(config.batch_size)]
        histories, codes = _batch(batch, config, device, torch)
        advantages = torch.tensor([row.advantage for row in batch], device=device)
        current = _sequence_probability(model(histories, codes), codes, torch)
        with torch.no_grad():
            old = _sequence_probability(reference(histories, codes), codes, torch)
        # GBPO's dynamic denominator bounds positive and negative gradients
        # without PPO sample clipping.
        denominator = torch.where(
            advantages > 0,
            torch.maximum(old, current.detach()),
            torch.maximum(old, 1.0 - current.detach()),
        )
        loss = -(current / denominator.clamp_min(1e-8) * advantages).mean()
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {"initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])), "informative_examples": len(informative)}


def evaluate(model, rows, config: OneRecV2Config):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    model.eval()
    losses, exact, first, rewards, elapsed = [], 0, 0, [], 0.0
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            batch = rows[start:start + config.batch_size]
            histories, codes = _batch(batch, config, device, torch)
            tick = time.perf_counter()
            logits = model(histories, codes)
            if device.type == "mps":
                torch.mps.synchronize()
            elapsed += time.perf_counter() - tick
            loss = sum(torch.nn.functional.cross_entropy(score, codes[:, level]) for level, score in enumerate(logits))
            predictions = torch.stack([score.argmax(-1) for score in logits], dim=1)
            exact += int((predictions == codes).all(dim=1).sum().cpu())
            first += int((predictions[:, 0] == codes[:, 0]).sum().cpu())
            probabilities = _sequence_probability(logits, codes, torch).cpu().numpy()
            rewards.extend(probabilities * np.asarray([row.advantage for row in batch]))
            losses.append(float(loss.cpu()) * len(batch))
    count = len(rows)
    return {
        "loss": sum(losses) / count, "semantic_id_exact_accuracy": exact / count,
        "level_1_accuracy": first / count, "feedback_weighted_probability": float(np.mean(rewards)),
        "milliseconds_per_example": 1000 * elapsed / count,
    }


def _batch(rows, config, device, torch):
    histories = torch.zeros((len(rows), config.history_items), dtype=torch.long, device=device)
    for index, row in enumerate(rows):
        values = row.history[-config.history_items:]
        histories[index, -len(values):] = torch.tensor(values, device=device)
    codes = torch.tensor([row.semantic_id for row in rows], dtype=torch.long, device=device)
    return histories, codes


def _sequence_probability(logits, codes, torch):
    values = []
    for level, score in enumerate(logits):
        values.append(torch.softmax(score, -1).gather(1, codes[:, level:level + 1]).squeeze(1))
    return torch.stack(values, 1).prod(1)
