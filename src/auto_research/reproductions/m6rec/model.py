from __future__ import annotations

import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ...datasets import movielens_100k


@dataclass(frozen=True)
class M6RecConfig:
    model_name: str = "prajjwal1/bert-tiny"
    maximum_length: int = 96
    history_items: int = 6
    adapter_width: int = 24
    batch_size: int = 32
    steps: int = 100
    learning_rate: float = 8e-4
    maximum_examples: int = 5000


def require_backend():
    try:
        import torch
        from torch import nn
        from transformers import AutoModel, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("M6-Rec requires `pip install -e '.[plum]'`.") from exc
    return torch, nn, AutoModel, AutoTokenizer


def movielens_text_examples(root: Path, config: M6RecConfig):
    ratings = movielens_100k(root)
    titles: dict[int, str] = {}
    genres = [
        "unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western",
    ]
    with (root / "ml-100k" / "u.item").open(encoding="latin-1") as stream:
        for line in stream:
            fields = line.rstrip().split("|")
            labels = [name for name, flag in zip(genres, fields[5:24]) if flag == "1"]
            titles[int(fields[0])] = f'{fields[1]} ({", ".join(labels)})'
    by_user: dict[int, list[tuple[int, int, float]]] = {}
    for user, item, rating, timestamp in ratings:
        by_user.setdefault(user, []).append((timestamp, item, rating))
    train, test = [], []
    for events in by_user.values():
        history: list[str] = []
        rows = []
        for _, item, rating in sorted(events):
            if history and rating != 3:
                text = (
                    "User recently liked: " + " ; ".join(history[-config.history_items:])
                    + ". Candidate item: " + titles[item]
                    + ". Will the user like this candidate?"
                )
                rows.append((text, int(rating >= 4)))
            if rating >= 4:
                history.append(titles[item])
        if len(rows) >= 4:
            split = max(1, int(0.8 * len(rows)))
            train.extend(rows[:split])
            test.extend(rows[split:])
    rng = random.Random(17)
    rng.shuffle(train)
    rng.shuffle(test)
    return tuple(train[:config.maximum_examples]), tuple(test[: max(500, config.maximum_examples // 4)])


def build_model(config: M6RecConfig, use_adapters: bool):
    torch, nn, AutoModel, AutoTokenizer = require_backend()
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    backbone = AutoModel.from_pretrained(config.model_name)
    for parameter in backbone.parameters():
        parameter.requires_grad = False
    hidden = backbone.config.hidden_size

    class Adapter(nn.Module):
        def __init__(self):
            super().__init__()
            self.down = nn.Linear(hidden, config.adapter_width)
            self.up = nn.Linear(config.adapter_width, hidden)
            nn.init.zeros_(self.up.weight)
            nn.init.zeros_(self.up.bias)

        def forward(self, values):
            return self.up(torch.nn.functional.gelu(self.down(values)))

    class OptionAdapterModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.backbone = backbone
            layers = list(backbone.encoder.layer)
            self.adapters = nn.ModuleList(Adapter() for _ in layers)
            self.options = nn.Parameter(torch.empty(2, hidden))
            nn.init.normal_(self.options, std=0.02)
            self.handles = []
            if use_adapters:
                for layer, adapter in zip(layers, self.adapters):
                    self.handles.append(layer.register_forward_hook(self._hook(adapter)))
            else:
                for parameter in self.adapters.parameters():
                    parameter.requires_grad = False

        @staticmethod
        def _hook(adapter):
            def apply(_module, _inputs, output):
                if isinstance(output, tuple):
                    return (output[0] + adapter(output[0]), *output[1:])
                return output + adapter(output)
            return apply

        def forward(self, input_ids, attention_mask):
            representation = self.backbone(
                input_ids=input_ids, attention_mask=attention_mask,
                return_dict=True,
            ).last_hidden_state[:, 0]
            representation = torch.nn.functional.normalize(representation, dim=-1)
            options = torch.nn.functional.normalize(self.options, dim=-1)
            return representation @ options.T * 12.0

    return OptionAdapterModel(), tokenizer


def train_and_evaluate(rows, test, config: M6RecConfig, seed: int, use_adapters: bool):
    torch, _, _, _ = require_backend()
    torch.manual_seed(seed)
    model, tokenizer = build_model(config, use_adapters)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    trainable = [parameter for parameter in model.parameters() if parameter.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        encoded = tokenizer(
            [text for text, _ in batch], padding=True, truncation=True,
            max_length=config.maximum_length, return_tensors="pt",
        ).to(device)
        labels = torch.tensor([label for _, label in batch], device=device)
        logits = model(encoded["input_ids"], encoded["attention_mask"])
        loss = torch.nn.functional.cross_entropy(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    metrics = evaluate(model, tokenizer, test, config, device, torch)
    metrics.update({
        "initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])),
        "seconds": time.perf_counter() - started,
        "trainable_parameters": sum(value.numel() for value in trainable),
        "total_parameters": sum(value.numel() for value in model.parameters()), "device": device.type,
    })
    return metrics


def evaluate(model, tokenizer, rows, config, device, torch):
    scores, labels = [], []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            batch = rows[start:start + config.batch_size]
            encoded = tokenizer(
                [text for text, _ in batch], padding=True, truncation=True,
                max_length=config.maximum_length, return_tensors="pt",
            ).to(device)
            probability = torch.softmax(model(encoded["input_ids"], encoded["attention_mask"]), -1)[:, 1]
            scores.extend(probability.cpu().tolist())
            labels.extend(label for _, label in batch)
    predictions = [value >= 0.5 for value in scores]
    return {"auc": binary_auc(labels, scores), "accuracy": float(np.mean(np.asarray(predictions) == labels)), "examples": len(rows)}


def binary_auc(labels, scores):
    order = np.argsort(np.asarray(scores))
    ranks = np.empty(len(order), dtype=np.float64)
    ranks[order] = np.arange(1, len(order) + 1)
    labels = np.asarray(labels)
    positives = labels == 1
    positive_count = int(positives.sum())
    negative_count = len(labels) - positive_count
    return float((ranks[positives].sum() - positive_count * (positive_count + 1) / 2) / (positive_count * negative_count))
