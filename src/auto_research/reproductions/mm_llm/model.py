from __future__ import annotations

import random

import numpy as np

from ..industrial_batch import device_for, padded_histories, require_torch, training_pairs


def train_caption_tokens(data, seed: int, steps: int = 100):
    torch, nn = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    features = torch.tensor(data.features, device=device)
    vocabulary = data.features.shape[1]

    class QFormerCaptioner(nn.Module):
        def __init__(self):
            super().__init__()
            self.visual = nn.Linear(vocabulary, 48)
            self.queries = nn.Parameter(torch.randn(4, 48) * 0.02)
            self.cross = nn.MultiheadAttention(48, 4, batch_first=True)
            self.caption = nn.Linear(48, vocabulary)

        def forward(self, values):
            visual = self.visual(values).unsqueeze(1)
            query = self.queries.unsqueeze(0).expand(len(values), -1, -1)
            hidden, _ = self.cross(query, visual, visual)
            return self.caption(hidden.mean(1))

    model = QFormerCaptioner().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=2e-3)
    losses = []
    for _ in range(steps):
        logits = model(features)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, features.clamp(0, 1))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    with torch.inference_mode():
        probabilities = torch.sigmoid(model(features))
        top = torch.topk(probabilities, k=min(4, vocabulary), dim=-1).indices.cpu().numpy()
    tokens = np.zeros((data.item_count, vocabulary), dtype=np.float32)
    for item, values in enumerate(top):
        tokens[item, values] = 1.0
    return tokens, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "caption_tokens_per_item": top.shape[1]}


def train_ranker(data, caption_tokens, seed: int, steps: int, use_captions: bool):
    torch, nn = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    visual = torch.tensor(data.features, device=device)
    captions = torch.tensor(caption_tokens, device=device)

    class MultimediaRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, 32)
            self.visual = nn.Linear(data.features.shape[1], 32, bias=False)
            self.caption = nn.Linear(caption_tokens.shape[1], 32, bias=False)
            self.gate = nn.Linear(64, 32)

        def representations(self):
            base = self.item.weight + self.visual(visual)
            if not use_captions:
                return base
            semantic = self.caption(captions)
            return base + torch.sigmoid(self.gate(torch.cat((base, semantic), -1))) * semantic

        def forward(self, histories):
            items = self.representations()
            user_ids = self.item(histories).mean(1)
            if use_captions:
                interest = self.caption(captions[histories]).mean(1)
                user_ids = user_ids + interest
            return user_ids @ items.T

    model = MultimediaRanker().to(device)
    rows = training_pairs(data)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    losses = []
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories = padded_histories([row[0] for row in batch], 20, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        loss = torch.nn.functional.cross_entropy(model(histories), targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:]))}


def scorer(model, data):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    model.eval()
    def score(history):
        with torch.inference_mode():
            return model(padded_histories([history], 20, device, torch))[0].cpu().numpy()
    return score

