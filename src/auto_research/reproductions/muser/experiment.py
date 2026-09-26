"""Chronological, held-out KuaiRand comparison for a scaled MuSeR mechanism."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F

from auto_research.datasets import kuairand_pure_files

from .model import MuSeR


@dataclass(frozen=True)
class Example:
    history: tuple[int, ...]
    target: int


@dataclass(frozen=True)
class Data:
    train: tuple[Example, ...]
    validation: tuple[Example, ...]
    test: tuple[Example, ...]
    item_tags: torch.Tensor
    tags: int
    events: int


def load_data(root: Path, *, max_events: int = 500_000,
              max_users: int = 10_000) -> Data:
    directory = kuairand_pure_files(root)
    item_tags_raw: dict[int, str] = {}
    with (directory / "video_features_basic_pure.csv").open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            item_tags_raw[int(row["video_id"])] = (row["tag"] or "unknown").split(",")[0]
    item_ids = {video: index for index, video in enumerate(sorted(item_tags_raw))}
    tag_ids = {tag: index for index, tag in enumerate(sorted(set(item_tags_raw.values())))}
    item_tags = torch.tensor([tag_ids[item_tags_raw[item]] for item in sorted(item_tags_raw)])
    users: dict[int, list[tuple[int, int]]] = defaultdict(list)
    with (directory / "log_standard_4_22_to_5_08_pure.csv").open(encoding="utf-8") as stream:
        for number, row in enumerate(csv.DictReader(stream)):
            if number >= max_events:
                break
            user, item = int(row["user_id"]), int(row["video_id"])
            if user >= max_users or item not in item_ids:
                continue
            if row["is_click"] == "1" or row["long_view"] == "1":
                users[user].append((int(row["time_ms"]), item_ids[item]))
    train, validation, test = [], [], []
    for events in users.values():
        history = [item for _, item in sorted(events)]
        if len(history) < 8:
            continue
        for position in range(5, len(history)):
            example = Example(tuple(history[:position][-256:]), history[position])
            if position == len(history) - 1:
                test.append(example)
            elif position == len(history) - 2:
                validation.append(example)
            else:
                train.append(example)
    if not train or not validation or not test:
        raise ValueError("KuaiRand public slice lacks train/validation/test examples")
    return Data(tuple(train), tuple(validation), tuple(test), item_tags,
                len(tag_ids), sum(map(len, users.values())))


@torch.no_grad()
def evaluate(model: MuSeR, examples: tuple[Example, ...], *,
             seed: int, limit: int = 1000) -> dict[str, float]:
    model.eval()
    rng = np.random.default_rng(seed)
    recall, ndcg = [], []
    selected = rng.choice(len(examples), min(limit, len(examples)), replace=False)
    candidates = torch.arange(model.items)[None]
    for index in selected:
        example = examples[int(index)]
        history = [torch.tensor(example.history)]
        score = model.score(model.encode(history), candidates)[0]
        target_score = score[example.target].clone()
        score[torch.tensor(example.history)] = float("-inf")
        score[example.target] = target_score
        rank = int((score >= target_score).sum())
        recall.append(float(rank <= 10))
        ndcg.append(float(1 / np.log2(rank + 1)) if rank <= 10 else 0.0)
    return {"recall_at_10": float(np.mean(recall)),
            "ndcg_at_10": float(np.mean(ndcg)),
            "evaluated": len(recall), "candidates": model.items,
            "candidate_policy": "all catalog items excluding observed history"}


def train_variant(data: Data, *, seed: int, compression: bool, semantics: bool,
                  interests: int = 4, steps: int = 800) -> tuple[MuSeR, float]:
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    torch.manual_seed(seed)
    model = MuSeR(len(data.item_tags), data.tags, data.item_tags,
                  interests=interests, use_compression=compression,
                  use_semantics=semantics)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    rng = np.random.default_rng(seed)
    model.train()
    final_loss = float("nan")
    for _ in range(steps):
        selected = rng.choice(len(data.train), min(16, len(data.train)), replace=False)
        batch = [data.train[int(index)] for index in selected]
        histories = [torch.tensor(row.history) for row in batch]
        positive = np.asarray([row.target for row in batch])
        negatives = rng.integers(0, model.items, (len(batch), 31))
        negatives += (negatives == positive[:, None]).astype(np.int64)
        negatives %= model.items
        candidates = torch.tensor(np.concatenate((positive[:, None], negatives), 1))
        vectors = model.encode(histories)
        scores = model.score(vectors, candidates)
        loss = F.cross_entropy(scores, torch.zeros(len(batch), dtype=torch.long))
        loss = loss + 0.01 * model.orthogonality(vectors)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        final_loss = float(loss.detach())
    return model, final_loss


def reproduce(root: Path, seed: int = 42, *, steps: int = 800,
              max_events: int = 500_000) -> dict:
    data = load_data(root, max_events=max_events)
    variants = {}
    for name, compression, semantics, interests in (
        ("muser", True, True, 4),
        ("recent_single_id", False, False, 1),
        ("without_compression", False, True, 4),
        ("without_semantics", True, False, 4),
    ):
        model, loss = train_variant(data, seed=seed, compression=compression,
                                    semantics=semantics, interests=interests,
                                    steps=steps)
        variants[name] = {
            "train_final_loss": loss,
            "validation": evaluate(model, data.validation, seed=seed + 1),
            "test": evaluate(model, data.test, seed=seed + 2),
        }
    return {
        "paper": {"arxiv_id": "2609.23677", "url": "https://arxiv.org/abs/2609.23677"},
        "setup": {"dataset": "KuaiRand-Pure", "seed": seed,
                  "events": data.events, "items": len(data.item_tags),
                  "train": len(data.train), "validation": len(data.validation),
                  "test": len(data.test), "steps_per_variant": steps,
                  "split": "per-user last two positive events held out",
                  "candidate_policy": "full catalog, excluding observed history"},
        "variants": variants,
        "scope": "Scaled public-data mechanism experiment. Public video tags replace private LLM-generated summaries; no 10^5-item online serving, asynchronous cache, or HNSW beam search.",
    }
