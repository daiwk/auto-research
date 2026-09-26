"""Public MovieLens comparison of stop-gradient and stateless Light Heads."""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import numpy as np
import torch

from auto_research.datasets import movielens_100k

from .model import HeadSpec, LightHeadRanker, head_loss


def _prepare(root: Path) -> tuple[dict[str, tuple[torch.Tensor, ...]], int, int, int]:
    ratings = movielens_100k(root)
    item_path = root / "ml-100k" / "u.item"
    genres: dict[int, np.ndarray] = {}
    with item_path.open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip("\n").split("|")
            genres[int(fields[0])] = np.asarray(fields[5:24], dtype=np.float32)
    users: dict[int, list[tuple[int, int, float, int]]] = defaultdict(list)
    for row in ratings:
        users[row[0]].append(row)
    split_rows: dict[str, list[tuple[int, int, float]]] = defaultdict(list)
    for user, events in users.items():
        ordered = sorted(events, key=lambda row: (row[3], row[1]))
        first = int(len(ordered) * 0.7)
        second = int(len(ordered) * 0.85)
        for index, (_, item, rating, _) in enumerate(ordered):
            split = "train" if index < first else "validation" if index < second else "test"
            split_rows[split].append((user, item, rating))
    output = {}
    for split, rows in split_rows.items():
        output[split] = (
            torch.tensor([row[0] for row in rows], dtype=torch.long),
            torch.tensor([row[1] for row in rows], dtype=torch.long),
            torch.tensor(np.stack([genres[row[1]] for row in rows])),
            torch.tensor([float(row[2] >= 4) for row in rows]),
            torch.tensor([float(row[2] == 5) for row in rows]),
        )
    return output, max(users) + 1, max(genres) + 1, 19


def _fit(model: LightHeadRanker, data: tuple[torch.Tensor, ...], *,
         target: str, steps: int, seed: int, stop_gradient: bool = True) -> None:
    generator = torch.Generator().manual_seed(seed)
    if target == "main":
        parameters = model.parameters()
    elif stop_gradient:
        parameters = model.light_heads[target].parameters()
    else:
        parameters = (
            parameter for name, parameter in model.named_parameters()
            if not name.startswith("main.")
        )
    optimizer = torch.optim.AdamW(parameters, lr=0.003)
    model.train()
    for _ in range(steps):
        indices = torch.randint(len(data[0]), (256,), generator=generator)
        users, items, genres = (value[indices] for value in data[:3])
        labels = data[3 if target == "main" else 4][indices]
        logits = model(users, items, genres, stop_gradient=stop_gradient)[target]
        loss = head_loss(logits, labels, HeadSpec(target))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()


def _subset(data: tuple[torch.Tensor, ...], first: int, last: int) -> tuple[torch.Tensor, ...]:
    return tuple(value[first:last] for value in data)


def _auc(scores: np.ndarray, labels: np.ndarray) -> float:
    positives = float(labels.sum())
    negatives = float(len(labels) - positives)
    if not positives or not negatives:
        raise ValueError("both classes are required for ROC-AUC")
    order = np.argsort(scores, kind="stable")
    ranks = np.empty(len(scores), dtype=np.float64)
    ranks[order] = np.arange(1, len(scores) + 1)
    values, inverse, counts = np.unique(scores, return_inverse=True, return_counts=True)
    del values
    if np.any(counts > 1):
        sums = np.bincount(inverse, weights=ranks)
        ranks = sums[inverse] / counts[inverse]
    return float((ranks[labels == 1].sum() - positives * (positives + 1) / 2)
                 / (positives * negatives))


@torch.no_grad()
def _score(model: LightHeadRanker, data: tuple[torch.Tensor, ...]) -> dict[str, float]:
    model.eval()
    main, light = [], []
    for start in range(0, len(data[0]), 1024):
        users, items, genres = (value[start:start + 1024] for value in data[:3])
        outputs = model(users, items, genres)
        main.extend(torch.sigmoid(outputs["main"]).tolist())
        light.extend(torch.sigmoid(outputs["high_rating"]).tolist())
    return {
        "main_auc": _auc(np.asarray(main), data[3].numpy()),
        "light_auc": _auc(np.asarray(light), data[4].numpy()),
    }


def reproduce(root: Path, seed: int = 42, *, base_steps: int = 120,
              head_steps: int = 80) -> dict:
    """Compare frozen-light, no-stop-gradient and no-reset under one split/budget."""
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    torch.manual_seed(seed)
    data, users, items, genres = _prepare(root)
    base = LightHeadRanker(users, items, genres)
    _fit(base, data["train"], target="main", steps=base_steps, seed=seed)
    spec = HeadSpec("high_rating")
    base.inject(spec)
    middle = len(data["train"][0]) // 2
    first = _subset(data["train"], 0, middle)
    second = _subset(data["train"], middle, len(data["train"][0]))
    variants = {}
    for name, reset, stop_gradient in (
        ("light_head", True, True),
        ("no_reset", False, True),
        ("no_stop_gradient", True, False),
    ):
        model = deepcopy(base)
        _fit(model, first, target=spec.name, steps=head_steps // 2,
             seed=seed + 1, stop_gradient=stop_gradient)
        if reset:
            model.reset_run()
        _fit(model, second, target=spec.name, steps=head_steps - head_steps // 2,
             seed=seed + 2, stop_gradient=stop_gradient)
        variants[name] = {
            "validation": _score(model, data["validation"]),
            "test": _score(model, data["test"]),
        }
    return {
        "paper": {"arxiv_id": "2609.25433", "url": "https://arxiv.org/abs/2609.25433"},
        "setup": {
            "dataset": "MovieLens 100K", "seed": seed, "base_steps": base_steps,
            "head_steps": head_steps, "split": "per-user chronological 70/15/15",
            "train_rows": len(data["train"][0]),
            "validation_rows": len(data["validation"][0]),
            "test_rows": len(data["test"][0]),
            "main_target": "rating >= 4", "light_target": "rating == 5",
            "same_budget_and_split": True, "device": "cpu",
        },
        "variants": variants,
        "mechanism": {
            "central_head_spec": spec.name,
            "stop_gradient": True,
            "head_reset_between_training_windows": True,
            "shared_backbone_retrained_for_new_task": False,
        },
        "scope": "公开显式评分二任务缩小实验；不复刻 YouTube 持续训练、跨模型 fleet 或线上流量。",
    }
