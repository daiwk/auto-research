"""Chronological public KuaiRand feedback experiment for FLVM."""

from __future__ import annotations

import csv
import hashlib
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F

from auto_research.datasets import kuairand_pure_files

from .model import FLVM, MultitaskControl


SIGNALS = ("long_view", "is_click", "is_like", "is_hate")


@dataclass(frozen=True)
class Split:
    users: torch.Tensor
    items: torch.Tensor
    confounders: torch.Tensor
    labels: torch.Tensor
    mask: torch.Tensor

    def __len__(self) -> int:
        return len(self.users)

    def batch(self, indices: torch.Tensor) -> tuple[torch.Tensor, ...]:
        return (self.users[indices], self.items[indices], self.confounders[indices],
                self.labels[indices], self.mask[indices])


@dataclass(frozen=True)
class PublicData:
    train: Split
    validation: Split
    test: Split
    users: int
    items: int
    source_sha256: str


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_data(root: Path, *, max_events: int | None = None) -> PublicData:
    """Only impression-time IDs, duration and hour enter features; feedback stays labels."""
    path = kuairand_pure_files(root) / "log_standard_4_22_to_5_08_pure.csv"
    events = []
    user_ids: dict[str, int] = {}
    item_ids: dict[str, int] = {}
    with path.open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            if max_events is not None and len(events) >= max_events:
                break
            user = user_ids.setdefault(row["user_id"], len(user_ids))
            item = item_ids.setdefault(row["video_id"], len(item_ids))
            hour = int(row["hourmin"]) // 100
            duration = max(float(row["duration_ms"]), 1.0)
            confounders = (math.log1p(duration) / 12.0,
                           math.sin(2 * math.pi * hour / 24),
                           math.cos(2 * math.pi * hour / 24))
            labels = tuple(float(row[name]) for name in SIGNALS)
            events.append((int(row["time_ms"]), user, item, confounders, labels))
    if len(events) < 100:
        raise ValueError("KuaiRand-Pure requires at least 100 real impressions")
    events.sort(key=lambda event: event[0])

    def split(rows: list[tuple]) -> Split:
        return Split(torch.tensor([row[1] for row in rows], dtype=torch.long),
                     torch.tensor([row[2] for row in rows], dtype=torch.long),
                     torch.tensor([row[3] for row in rows], dtype=torch.float32),
                     torch.tensor([row[4] for row in rows], dtype=torch.float32),
                     torch.ones((len(rows), len(SIGNALS)), dtype=torch.float32))

    cut_train, cut_validation = int(len(events) * 0.7), int(len(events) * 0.85)
    return PublicData(split(events[:cut_train]), split(events[cut_train:cut_validation]),
                      split(events[cut_validation:]), len(user_ids), len(item_ids),
                      _sha256(path))


def average_precision(labels: np.ndarray, scores: np.ndarray) -> float | None:
    positive = int(labels.sum())
    if positive == 0:
        return None
    order = np.argsort(-scores, kind="stable")
    ranked = labels[order]
    precision = np.cumsum(ranked) / np.arange(1, len(ranked) + 1)
    return float(np.dot(precision, ranked) / positive)


@torch.no_grad()
def evaluate(model: nn.Module, split: Split) -> dict:
    model.eval()
    predictions = []
    latents = []
    for start in range(0, len(split), 4096):
        users, items, confounders, _, _ = split.batch(
            torch.arange(start, min(start + 4096, len(split)))
        )
        if isinstance(model, FLVM):
            logits, _, mean, _ = model(users, items, confounders, sample=False)
            latents.append(mean.numpy())
        else:
            logits = model(users, items, confounders)
        predictions.append(logits.sigmoid().numpy())
    score = np.concatenate(predictions)
    targets = split.labels.numpy()
    result = {
        "impressions": len(split),
        "signals": {
            name: {"positive": int(targets[:, index].sum()),
                   "average_precision": average_precision(targets[:, index], score[:, index])}
            for index, name in enumerate(SIGNALS)
        },
    }
    if latents:
        mean = np.concatenate(latents)
        liked = targets[:, 2] == 1
        hated = targets[:, 3] == 1
        result["valence_mean_like_minus_hate"] = (
            float(mean[liked, 2].mean() - mean[hated, 2].mean())
            if liked.any() and hated.any() else None
        )
    return result


def train(model: nn.Module, split: Split, *, seed: int, steps: int = 300,
          batch_size: int = 1024) -> tuple[nn.Module, float]:
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    torch.manual_seed(seed + 1000)
    generator = torch.Generator().manual_seed(seed + 2000)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    model.train()
    loss_value = float("nan")
    for _ in range(steps):
        indices = torch.randint(len(split), (batch_size,), generator=generator)
        users, items, confounders, labels, mask = split.batch(indices)
        if isinstance(model, FLVM):
            logits, baseline, mean, log_variance = model(users, items, confounders)
            loss = FLVM.loss(logits, baseline, labels, mask, mean, log_variance)
        else:
            logits = model(users, items, confounders)
            weights = labels.new_tensor((1.0, 1.0, 3.0, 5.0))
            loss = (F.binary_cross_entropy_with_logits(logits, labels, reduction="none")
                    * mask * weights).sum() / (mask * weights).sum().clamp_min(1)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        loss_value = float(loss.detach())
    return model, loss_value


def run_on_data(data: PublicData, *, seed: int = 42, steps: int = 300) -> dict:
    variants = {}
    for name, constructor in (("flvm", FLVM), ("multitask_control", MultitaskControl)):
        torch.manual_seed(seed)
        model, train_loss = train(constructor(data.users, data.items), data.train,
                                  seed=seed, steps=steps)
        variants[name] = {"train_final_loss": train_loss,
                          "validation": evaluate(model, data.validation),
                          "test": evaluate(model, data.test)}
    return {"paper": "2609.32839", "seed": seed, "steps_per_variant": steps,
            "dataset": "KuaiRand-Pure", "source_sha256": data.source_sha256,
            "split": {"train": len(data.train), "validation": len(data.validation),
                      "test": len(data.test), "method": "global chronological 70/15/15"},
            "variants": variants,
            "scope": "Public-data concept diagnostic, not YouTube Shorts satisfaction or online A/B."}


def reproduce(root: Path, seed: int = 42) -> dict:
    return run_on_data(load_data(root), seed=seed)
