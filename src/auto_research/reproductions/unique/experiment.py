"""KuaiRand-Pure exposure holdout for the scaled UNIQUE mechanism."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F

from auto_research.datasets import kuairand_pure_files

from .model import Unique


@dataclass(frozen=True)
class Impression:
    user: int
    history: tuple[int, ...]
    item: int
    clicked: int
    duration: float


@dataclass(frozen=True)
class Data:
    train: tuple[Impression, ...]
    validation: tuple[Impression, ...]
    test: tuple[Impression, ...]
    item_tags: torch.Tensor
    tags: int
    users: int
    raw_events: int


def load_data(root: Path, *, max_events: int = 500_000,
              max_users: int = 10_000) -> Data:
    directory = kuairand_pure_files(root)
    raw_tags = {}
    with (directory / "video_features_basic_pure.csv").open(encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            raw_tags[int(row["video_id"])] = (row["tag"] or "unknown").split(",")[0]
    item_ids = {item: index for index, item in enumerate(sorted(raw_tags))}
    tag_ids = {tag: index for index, tag in enumerate(sorted(set(raw_tags.values())))}
    item_tags = torch.tensor([tag_ids[raw_tags[item]] for item in sorted(raw_tags)])
    by_user: dict[int, list[tuple[int, int, int, float]]] = defaultdict(list)
    with (directory / "log_standard_4_22_to_5_08_pure.csv").open(encoding="utf-8") as stream:
        for number, row in enumerate(csv.DictReader(stream)):
            if number >= max_events:
                break
            user, item = int(row["user_id"]), int(row["video_id"])
            if user >= max_users or item not in item_ids:
                continue
            click = int(row["is_click"] == "1" or row["long_view"] == "1")
            duration = min(float(row["play_time_ms"]) /
                           max(1, float(row["duration_ms"])), 1.0)
            by_user[user].append((int(row["time_ms"]), item_ids[item], click, duration))
    train, validation, test = [], [], []
    for user, events in by_user.items():
        positives: list[int] = []
        ordered = sorted(events)
        for position, (_, item, click, duration) in enumerate(ordered):
            if len(positives) >= 8:
                observed = positives[-24:]
                # Repeating the earliest *observed* item pads short histories;
                # no held-out impression or future interaction enters the prefix.
                history = (observed[0],) * (24 - len(observed)) + tuple(observed)
                record = Impression(user, history, item, click, duration)
                if position == len(ordered) - 1:
                    test.append(record)
                elif position == len(ordered) - 2:
                    validation.append(record)
                else:
                    train.append(record)
            if click:
                positives.append(item)
    if not train or not validation or not test:
        raise ValueError("KuaiRand public slice lacks held-out impressions")
    return Data(tuple(train), tuple(validation), tuple(test), item_tags,
                len(tag_ids), max(by_user) + 1, sum(map(len, by_user.values())))


def _batch(rows: list[Impression]) -> tuple[torch.Tensor, ...]:
    return (torch.tensor([row.user for row in rows]),
            torch.tensor([row.history for row in rows]),
            torch.tensor([row.item for row in rows]),
            torch.tensor([row.clicked for row in rows], dtype=torch.float32),
            torch.tensor([row.duration for row in rows], dtype=torch.float32))


def train_variant(data: Data, *, seed: int, steps: int = 300,
                  joint: bool = True, balance: float = 0.5) -> tuple[Unique, float]:
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    model = Unique(len(data.item_tags), data.users, data.item_tags,
                   tags=data.tags, joint=joint, balance=balance)
    optim = torch.optim.AdamW(model.parameters(), lr=0.001)
    final = float("nan")
    for _ in range(steps):
        batch = [data.train[int(index)] for index in rng.choice(
            len(data.train), min(32, len(data.train)), replace=False)]
        users, history, items, clicks, durations = _batch(batch)
        negatives = torch.tensor(rng.integers(0, model.items, len(batch)))
        target = torch.stack((items, negatives), 1)
        rank, code_logits, vectors = model(users, history, target)
        labels = torch.stack((clicks, torch.zeros_like(clicks)), 1)
        rank_loss = F.binary_cross_entropy_with_logits(rank, labels)
        # Public exposure log supplies observed click/duration; randomly drawn
        # negatives are only auxiliary and are not counted in CTR evaluation.
        duration_loss = F.mse_loss(torch.sigmoid(rank[:, 0]), durations)
        profile = F.normalize(model.user_tower(model.user(users) +
                              model.item_id(history).mean(1)), dim=-1)
        two_tower = (profile * vectors[:, 0]).sum(-1)
        code_loss = F.binary_cross_entropy_with_logits(two_tower, clicks)
        if joint:
            positive = clicks.bool()
            gen = F.cross_entropy(code_logits[positive], model.assign(vectors[positive, 0])) \
                if positive.any() else rank_loss.new_zeros(())
        else:
            gen = rank_loss.new_zeros(())
        quant = F.mse_loss(vectors[:, 0], model.codebook[model.assign(vectors[:, 0])].detach())
        loss = rank_loss + 0.1 * duration_loss + 0.2 * code_loss + 0.2 * gen + 0.05 * quant
        optim.zero_grad(set_to_none=True)
        loss.backward()
        optim.step()
        model.update_codebook(model.item_vector(items))
        final = float(loss.detach())
    return model, final


def _auc(labels: list[int], scores: list[float]) -> float:
    positives = sum(labels)
    negatives = len(labels) - positives
    if not positives or not negatives:
        return float("nan")
    order = np.argsort(scores)
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1)
    return float((ranks[np.asarray(labels, dtype=bool)].sum() -
                  positives * (positives + 1) / 2) / (positives * negatives))


@torch.no_grad()
def evaluate(model: Unique, rows: tuple[Impression, ...], *, seed: int,
             limit: int = 400, retrieval_limit: int = 100) -> dict:
    model.eval()
    rng = np.random.default_rng(seed)
    selected = [rows[int(index)] for index in rng.choice(
        len(rows), min(limit, len(rows)), replace=False)]
    scores, labels = [], []
    for start in range(0, len(selected), 32):
        batch = selected[start:start + 32]
        users, history, items, clicks, _ = _batch(batch)
        rank, _, _ = model(users, history, items[:, None])
        scores.extend(rank[:, 0].tolist())
        labels.extend(int(row.clicked) for row in batch)
    result = {"ctr_auc": _auc(labels, scores), "evaluated_impressions": len(selected),
              "positive_impressions": sum(labels), "code_perplexity": model.code_perplexity()}
    if model.joint:
        all_items = torch.arange(model.items)
        assignments = model.assign(model.item_vector(all_items))
        pools = [all_items[assignments == code] for code in range(model.codes)]
        positives = [row for row in selected if row.clicked][:retrieval_limit]
        hits, rank_hits, ndcg, sizes = [], [], [], []
        for row in positives:
            users, history, target, _, _ = _batch([row])
            _, code_logits, _ = model(users, history, target[:, None])
            top_codes = code_logits[0].topk(4).indices.tolist()
            candidate = torch.cat([pools[code] for code in top_codes])
            candidate = candidate[~torch.isin(candidate, history[0])]
            hit = bool((candidate == row.item).any())
            hits.append(float(hit))
            sizes.append(len(candidate))
            if not hit:
                rank_hits.append(0.0)
                ndcg.append(0.0)
                continue
            ranked = []
            for chunk in candidate.split(256):
                output, _, _ = model(users, history, chunk[None])
                ranked.append(output[0])
            order = torch.argsort(torch.cat(ranked), descending=True)
            position = int(torch.where(candidate[order] == row.item)[0][0]) + 1
            rank_hits.append(float(position <= 10))
            ndcg.append(float(1 / np.log2(position + 1)) if position <= 10 else 0.0)
        result.update({"retrieval_evaluated": len(positives),
                       "candidate_recall_at_4_codes": float(np.mean(hits)) if hits else None,
                       "reranked_recall_at_10": float(np.mean(rank_hits)) if hits else None,
                       "reranked_ndcg_at_10": float(np.mean(ndcg)) if hits else None,
                       "mean_candidate_pool": float(np.mean(sizes)) if hits else None})
    return result


def reproduce(root: Path, seed: int = 42, *, steps: int = 300,
              max_events: int = 500_000) -> dict:
    data = load_data(root, max_events=max_events)
    variants = {}
    for name, joint, balance in (("unique_scaled", True, 0.5),
                                 ("without_joint_generation", False, 0.5),
                                 ("without_balance", True, 0.0)):
        model, loss = train_variant(data, seed=seed, steps=steps,
                                    joint=joint, balance=balance)
        variants[name] = {"train_final_loss": loss,
                          "validation": evaluate(model, data.validation, seed=seed + 1),
                          "test": evaluate(model, data.test, seed=seed + 2)}
    return {"paper": {"arxiv_id": "2609.23718", "url": "https://arxiv.org/abs/2609.23718"},
            "setup": {"dataset": "KuaiRand-Pure", "seed": seed, "steps_per_variant": steps,
                      "retained_events": data.raw_events, "items": len(data.item_tags),
                      "train": len(data.train), "validation": len(data.validation),
                      "test": len(data.test),
                      "split": "last two chronological impressions per user held out"},
            "variants": variants,
            "scope": "Scaled mechanism diagnostic: public item tags and click/duration feedback; "
                     "no private feed metadata, production retrieval system, or online A/B."}
