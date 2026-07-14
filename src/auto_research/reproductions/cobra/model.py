from __future__ import annotations

import random

import numpy as np

from ..industrial_batch import device_for, padded_histories, require_torch, training_pairs
from ..tiger.model import residual_kmeans


def semantic_codes(data, seed: int):
    return residual_kmeans(data.features.copy(), levels=2, size=8, seed=seed, iterations=20)


def build_model(data, codes, cascaded: bool):
    torch, nn = require_torch()
    code_tensor = torch.tensor(codes, dtype=torch.long)

    class COBRA(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("codes", code_tensor)
            self.item = nn.Embedding(data.item_count, 40)
            self.code = nn.ModuleList([nn.Embedding(8, 40) for _ in range(2)])
            self.sparse = nn.ModuleList([nn.Linear(40, 8) for _ in range(2)])
            self.dense = nn.Sequential(nn.Linear(120, 80), nn.GELU(), nn.Linear(80, 40))

        def user(self, histories):
            return self.item(histories).mean(1)

        def forward(self, histories, targets):
            user = self.user(histories)
            sparse_logits = [head(user) for head in self.sparse]
            target_codes = self.codes[targets]
            condition = torch.cat([self.code[level](target_codes[:, level]) for level in range(2)], -1)
            dense_query = self.dense(torch.cat((user, condition), -1)) if cascaded else user
            dense_logits = dense_query @ self.item.weight.T
            return sparse_logits, dense_logits

        def score(self, histories):
            user = self.user(histories)
            sparse_logits = [torch.log_softmax(head(user), -1) for head in self.sparse]
            sparse_score = sum(values[:, self.codes[:, level]] for level, values in enumerate(sparse_logits))
            if not cascaded:
                return sparse_score
            batch = len(histories)
            code_features = torch.cat([self.code[level](self.codes[:, level]) for level in range(2)], -1)
            user_expand = user[:, None, :].expand(batch, data.item_count, -1)
            query = self.dense(torch.cat((user_expand, code_features[None].expand(batch, -1, -1)), -1))
            dense_score = (query * self.item.weight[None]).sum(-1)
            return sparse_score + 0.15 * dense_score

    return COBRA()


def train(data, codes, seed: int, steps: int, cascaded: bool):
    torch, _ = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_model(data, codes, cascaded).to(device)
    rows = training_pairs(data)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    losses = []
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories = padded_histories([row[0] for row in batch], 20, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        sparse, dense = model(histories, targets)
        target_codes = model.codes[targets]
        loss = sum(torch.nn.functional.cross_entropy(logits, target_codes[:, level]) for level, logits in enumerate(sparse))
        if cascaded:
            loss = loss + torch.nn.functional.cross_entropy(dense, targets)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:]))}


def scorer(model):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    model.eval()
    def score(history):
        with torch.inference_mode():
            return model.score(padded_histories([history], 20, device, torch))[0].cpu().numpy()
    return score

