from __future__ import annotations

import random

import numpy as np

from ..industrial_batch import device_for, padded_histories, require_torch, training_pairs


def build_model(data, decomposed: bool, dimensions: int = 48):
    torch, nn = require_torch()

    class ARGUS(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, dimensions)
            self.position = nn.Embedding(32, dimensions)
            layer = nn.TransformerEncoderLayer(dimensions, 4, 4 * dimensions, batch_first=True, norm_first=True, dropout=0.0)
            self.encoder = nn.TransformerEncoder(layer, 2)
            self.feedback = nn.Linear(dimensions, data.features.shape[1])
            self.feedback_projection = nn.Linear(data.features.shape[1], dimensions, bias=False)
            self.norm = nn.LayerNorm(dimensions)

        def forward(self, histories):
            positions = torch.arange(histories.shape[1], device=histories.device)
            hidden = self.encoder(self.item(histories) + self.position(positions))[:, -1]
            feedback_logits = self.feedback(hidden)
            if decomposed:
                hidden = self.norm(hidden + self.feedback_projection(torch.sigmoid(feedback_logits)))
            return hidden @ self.item.weight.T, feedback_logits

    return ARGUS()


def train(data, seed: int, steps: int, decomposed: bool, feedback_weight: float = 0.35):
    torch, _ = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_model(data, decomposed).to(device)
    features = torch.tensor(data.features, device=device)
    rows = training_pairs(data, 32)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4)
    losses = []
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories = padded_histories([row[0] for row in batch], 32, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        item_logits, feedback_logits = model(histories)
        loss = torch.nn.functional.cross_entropy(item_logits, targets)
        if decomposed:
            loss = loss + feedback_weight * torch.nn.functional.binary_cross_entropy_with_logits(feedback_logits, features[targets].clamp(0, 1))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "parameters": sum(p.numel() for p in model.parameters())}


def scorer(model):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    model.eval()
    def score(history):
        with torch.inference_mode():
            return model(padded_histories([history], 32, device, torch))[0][0].cpu().numpy()
    return score
