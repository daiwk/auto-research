from __future__ import annotations

import random

import numpy as np

from ..industrial_batch import CompactSequences, device_for, padded_histories, require_torch, training_pairs


def subset(data: CompactSequences, indices) -> CompactSequences:
    return CompactSequences(
        train=tuple(data.train[i] for i in indices),
        validation=tuple(data.validation[i] for i in indices),
        test=tuple(data.test[i] for i in indices),
        features=data.features,
        popularity=data.popularity,
    )


def build_ranker(items: int, feature_dim: int, dimensions: int):
    torch, nn = require_torch()

    class MultiTaskRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(items, dimensions)
            self.content = nn.Linear(feature_dim, dimensions, bias=False)
            self.auxiliary = nn.Linear(dimensions, feature_dim)

        def user(self, histories):
            return self.item(histories).mean(1)

        def forward(self, histories, features):
            user = self.user(histories)
            candidates = self.item.weight + self.content(features)
            return user @ candidates.T, self.auxiliary(user)

    return MultiTaskRanker()


def train_teacher(data, seed: int, steps: int, dimensions: int = 64):
    return _train(data, seed, steps, dimensions, teacher=None, kd_weight=0.0)


def train_student(data, seed: int, steps: int, teacher=None, kd_weight: float = 0.0):
    return _train(data, seed, steps, 24, teacher, kd_weight)


def _train(data, seed, steps, dimensions, teacher, kd_weight):
    torch, _ = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    features = torch.tensor(data.features, device=device)
    model = build_ranker(data.item_count, data.features.shape[1], dimensions).to(device)
    rows = training_pairs(data)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    losses = []
    if teacher is not None:
        teacher.eval()
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories = padded_histories([row[0] for row in batch], 20, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        logits, auxiliary = model(histories, features)
        loss = torch.nn.functional.cross_entropy(logits, targets)
        target_features = features[targets]
        loss = loss + 0.1 * torch.nn.functional.binary_cross_entropy_with_logits(auxiliary, target_features)
        if teacher is not None:
            with torch.no_grad():
                teacher_logits, teacher_aux = teacher(histories, features)
            temperature = 2.0
            kd = torch.nn.functional.kl_div(
                torch.log_softmax(logits / temperature, dim=-1),
                torch.softmax(teacher_logits / temperature, dim=-1),
                reduction="batchmean",
            ) * temperature**2
            aux_kd = torch.nn.functional.mse_loss(auxiliary, teacher_aux)
            loss = loss + kd_weight * (kd + 0.1 * aux_kd)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {
        "initial_loss": float(np.mean(losses[:10])),
        "final_loss": float(np.mean(losses[-10:])),
        "trainable_parameters": sum(p.numel() for p in model.parameters()),
    }


def scorer(model, data):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    features = torch.tensor(data.features, device=device)
    model.eval()

    def score(history):
        with torch.inference_mode():
            histories = padded_histories([history], 20, device, torch)
            return model(histories, features)[0][0].cpu().numpy()

    return score
