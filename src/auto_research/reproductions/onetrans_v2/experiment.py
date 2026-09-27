"""Leakage-isolated MovieLens-1M proxy evaluation for OneTrans-V2."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
import torch
from torch import Tensor

from ...datasets import movielens_1m
from ..rec_utils import _load_ml1m_genres
from ..tiger.model import residual_kmeans
from .model import OneTransV2


def load_public_stages(dataset_dir: Path):
    ratings = movielens_1m(dataset_dir)
    items = sorted({item for _, item, _, _ in ratings})
    ids = {item: index for index, item in enumerate(items)}
    genres = _load_ml1m_genres(dataset_dir, items).astype(np.float32)
    by_user: dict[int, list[tuple[int, int, float]]] = {}
    for user, item, rating, timestamp in ratings:
        by_user.setdefault(user, []).append((timestamp, ids[item], rating))
    train, validation, test = [], [], []
    for events in by_user.values():
        events.sort(key=lambda entry: entry[0])
        if len(events) < 7:
            continue
        observations = tuple((item, rating) for _, item, rating in events)
        for position in range(1, len(observations) - 2):
            train.append((observations[max(0, position - 40):position], observations[position]))
        validation.append((observations[-42:-2], observations[-2]))
        test.append((observations[-41:-1], observations[-1]))
    return train, validation, test, genres


def _batch(rows, genres: Tensor, codes: Tensor):
    width = max(len(history) for history, _ in rows)
    history = torch.zeros(len(rows), width, dtype=torch.long)
    valid = torch.zeros(len(rows), width, dtype=torch.bool)
    targets = []
    decision = []
    labels = []
    for row, (events, (item, rating)) in enumerate(rows):
        ids = [past_item for past_item, _ in events]
        history[row, :len(ids)] = torch.tensor(ids)
        valid[row, :len(ids)] = True
        targets.append(item)
        # MovieLens proxies, not purchase/spend/advertising labels.
        discovery = int(not any((genres[item] * genres[past_item]).sum() > 0 for past_item in ids))
        decision.append((int(rating >= 4), discovery))
        labels.append((float(rating >= 3), float(rating >= 4)))
    target = torch.tensor(targets, dtype=torch.long)
    return history, valid, target, genres[target], torch.tensor(decision), codes[target], torch.tensor(labels)


def _auc(labels: np.ndarray, scores: np.ndarray) -> float:
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    if not len(positives) or not len(negatives):
        return float("nan")
    # Exact pairwise AUC, robust to ties; evaluation has one event per user.
    return float(((positives[:, None] > negatives[None]).mean() + 0.5 * (positives[:, None] == negatives[None]).mean()))


def _evaluate(model: OneTransV2, rows, genres: Tensor, codes: Tensor):
    probabilities = {"pre": [], "fine": []}
    labels_all = []
    sid_correct = decision_correct = positives = 0
    with torch.no_grad():
        for start in range(0, len(rows), 64):
            history, valid, target, features, decision, sid, labels = _batch(rows[start:start + 64], genres, codes)
            outputs = model(history, valid, target, features)
            labels_all.append(labels.numpy())
            for stage in probabilities:
                probabilities[stage].append(outputs[stage].sigmoid().numpy())
            positive = labels[:, 0].bool()
            positives += int(positive.sum())
            sid_correct += int((torch.stack([x.argmax(-1) for x in outputs["sids"]], -1)[positive] == sid[positive]).all(-1).sum())
            decision_correct += int((torch.stack([x.argmax(-1) for x in outputs["decisions"]], -1)[positive] == decision[positive]).all(-1).sum())
    labels = np.concatenate(labels_all)
    result = {"positive_events": positives, "decision_exact_accuracy": decision_correct / max(positives, 1), "sid_exact_accuracy": sid_correct / max(positives, 1)}
    for stage, blocks in probabilities.items():
        scores = np.concatenate(blocks)
        for column, objective in enumerate(("rating_ge_3", "rating_ge_4")):
            result[f"{stage}_{objective}_auc"] = _auc(labels[:, column], scores[:, column])
            result[f"{stage}_{objective}_brier"] = float(np.mean((scores[:, column] - labels[:, column]) ** 2))
    return result


def reproduce_onetrans_v2(dataset_dir: Path, seed: int = 42) -> dict:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(min(torch.get_num_threads(), 4))
    train, validation, test, features = load_public_stages(dataset_dir)
    if len(train) < 100_000:
        raise ValueError("full MovieLens-1M is required")
    # The item-to-SID quantizer sees public item metadata only, no held-out
    # labels. It is a proxy for production item representation RQ-KMeans.
    codes = torch.tensor(residual_kmeans(features.copy(), 3, 16, seed), dtype=torch.long)
    genres = torch.tensor(features)
    model = OneTransV2(len(features), features.shape[1], codes)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.001)
    generator = torch.Generator().manual_seed(seed + 7)
    training = []
    model.train()
    for _ in range(200):
        selection = torch.randint(len(train), (64,), generator=generator)
        batch = _batch([train[int(index)] for index in selection], genres, codes)
        history, valid, item, item_genres, decision, sid, labels = batch
        outputs = model(history, valid, item, item_genres, decision, sid)
        loss, components = model.loss(outputs, decision_targets=decision, sid_targets=sid, labels=labels, retrieval_mask=labels[:, 0].bool())
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 2.0)
        optimizer.step()
        training.append({"total": float(loss.detach()), **components})
    model.eval()
    valid_metrics = _evaluate(model, validation, genres, codes)
    test_metrics = _evaluate(model, test, genres, codes)
    return {
        "paper": "2609.28589",
        "seed": seed,
        "dataset": {"name": "MovieLens 1M", "train_events": len(train), "validation_users": len(validation), "test_users": len(test)},
        "training": {"steps": 200, "batch_size": 64, "last_loss": training[-1], "mean_last_20": {key: float(np.mean([row[key] for row in training[-20:]])) for key in training[-1]}},
        "validation": valid_metrics,
        "test": test_metrics,
        "diagnostic_only": True,
        "scope": "共享因果用户编码、三级 SID 的决策条件自回归检索、预排/精排双目标 BCE 与精排到预排蒸馏均执行；MovieLens 评分与流派仅是公开代理信号，非真实 CTR/CVR、购买/金额/广告供给或线上 A/B。",
    }
