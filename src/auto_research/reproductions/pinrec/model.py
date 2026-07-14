from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training


@dataclass(frozen=True)
class PinRecConfig:
    dimensions: int = 64
    heads: int = 4
    layers: int = 2
    history: int = 24
    future_window: int = 3
    batch_size: int = 64
    steps: int = 160
    learning_rate: float = 4e-4


def build_model(item_count: int, config: PinRecConfig, conditioned: bool, multi_token: bool):
    torch, nn = require_backend()
    outputs = config.future_window if multi_token else 1

    class PinRec(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count + 1, config.dimensions, padding_idx=0)
            self.action = nn.Embedding(4, config.dimensions, padding_idx=3)
            self.position = nn.Embedding(config.history, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.decoder = nn.TransformerEncoder(layer, config.layers)
            self.output = nn.ModuleList([
                nn.Sequential(nn.Linear(2 * config.dimensions, config.dimensions), nn.GELU(), nn.Linear(config.dimensions, config.dimensions))
                for _ in range(outputs)
            ])

        def representations(self, items, actions, desired):
            positions = torch.arange(items.shape[1], device=items.device)
            hidden = self.item(items) + self.action(actions) + self.position(positions)
            causal = torch.triu(torch.ones(items.shape[1], items.shape[1], device=items.device, dtype=torch.bool), 1)
            context = self.decoder(hidden, mask=causal)[:, -1]
            condition = self.action(desired) if conditioned else torch.zeros_like(context)
            joined = torch.cat((context, condition), dim=-1)
            return torch.stack([torch.nn.functional.normalize(head(joined), dim=-1) for head in self.output], dim=1)

        def item_vectors(self):
            return torch.nn.functional.normalize(self.item.weight[1:], dim=-1)

    return PinRec()


def train_model(model, data, config: PinRecConfig, seed: int, multi_token: bool):
    model, device, torch = initialize(model, seed)
    rng = random.Random(seed)
    examples = []
    width = config.future_window if multi_token else 1
    for items, actions in zip(data.train_items, data.train_actions):
        for position in range(2, len(items)):
            future = list(zip(
                items[position:position + 2 * width],
                actions[position:position + 2 * width],
            ))
            if not future:
                continue
            desired = future[0][1]
            matched = [item for item, action in future if action == desired][:width]
            matched += [matched[-1]] * (width - len(matched))
            examples.append((items[:position], actions[:position], tuple(matched), (desired,) * width))
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    for _ in range(config.steps):
        batch = [examples[rng.randrange(len(examples))] for _ in range(config.batch_size)]
        items, actions = _histories(batch, config, device, torch)
        targets = torch.tensor([row[2] for row in batch], device=device)
        desired = torch.tensor([row[3][0] for row in batch], device=device)
        representations = model.representations(items, actions, desired)
        if multi_token:
            # Items inside the future window are time-equivalent. Randomizing
            # their assignment prevents a strict next-offset objective.
            for row in range(len(batch)):
                order = torch.randperm(width, device=device)
                targets[row] = targets[row, order]
        target_vectors = model.item_vectors()[targets]
        logits = torch.einsum("bwd,nwd->bwn", representations, target_vectors) / 0.07
        labels = torch.arange(len(batch), device=device)[None].expand(width, -1).T
        loss = torch.nn.functional.cross_entropy(logits.reshape(-1, len(batch)), labels.reshape(-1))
        optimizer.zero_grad(set_to_none=True); loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def evaluate(model, data, config: PinRecConfig):
    torch, _ = require_backend(); device = next(model.parameters()).device
    item_vectors = model.item_vectors(); recall = ndcg = 0.0
    model.eval()
    with torch.inference_mode():
        for index, history in enumerate(data.train_items):
            items = history
            actions = data.train_actions[index]
            row = (items, actions, (), ())
            item_batch, action_batch = _histories([row], config, device, torch)
            desired = torch.tensor([data.test_actions[index]], device=device)
            reps = model.representations(item_batch, action_batch, desired)[0]
            scores = (reps @ item_vectors.T).max(0).values.cpu().numpy()
            scores[list(set(items))] = -np.inf
            top = np.argpartition(scores, -10)[-10:]
            top = top[np.argsort(scores[top])[::-1]]
            future = [
                item for item, action in (
                    (data.validation_items[index], data.validation_actions[index]),
                    (data.test_items[index], data.test_actions[index]),
                ) if action == data.test_actions[index]
            ]
            gains = []
            for target in future:
                positions = np.flatnonzero(top == target)
                if positions.size:
                    recall += 1 / len(future)
                    gains.append(1 / np.log2(int(positions[0]) + 2))
            ndcg += sum(gains) / len(future)
    count = len(data.test_items)
    return {"unordered_recall_at_10": recall / count, "ndcg_at_10": ndcg / count, "users": count}


def _histories(batch, config, device, torch):
    items = torch.zeros((len(batch), config.history), dtype=torch.long, device=device)
    actions = torch.full_like(items, 3)
    for index, row in enumerate(batch):
        width = min(config.history, len(row[0]))
        items[index, -width:] = torch.tensor(row[0][-width:], device=device) + 1
        actions[index, -width:] = torch.tensor(row[1][-width:], device=device)
    return items, actions
