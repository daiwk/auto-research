from __future__ import annotations

import math


def build_model(data, *, debiased: bool, dimensions: int = 48):
    import torch
    from torch import nn

    class Ranker(nn.Module):
        def __init__(self):
            super().__init__()
            self.debiased = debiased
            self.user = nn.Embedding(data.users, dimensions)
            self.user_content = nn.Linear(data.genres.shape[1], dimensions, bias=False)
            self.item = nn.Embedding(data.items, dimensions)
            self.content = nn.Linear(data.genres.shape[1], dimensions, bias=False)
            self.scalar = nn.Linear(3, dimensions)
            self.cross = nn.Linear(dimensions + 3, dimensions)
            self.bias = nn.Embedding(data.items, 1)
            self.register_buffer("genres", torch.tensor(data.genres))
            self.register_buffer("user_profiles", torch.tensor(data.user_profiles))
            popularity = torch.tensor(data.popularity)
            self.register_buffer(
                "engagement",
                torch.log1p(popularity) / torch.log1p(popularity.max().clamp_min(1)),
            )
            self.register_buffer("fresh", torch.tensor(data.fresh, dtype=torch.float32))
            self.register_buffer(
                "underexplored",
                torch.tensor(data.underexplored, dtype=torch.float32),
            )

        def item_representation(self, items, *, training_dropout: bool = False):
            content = self.content(self.genres[items])
            engagement = self.engagement[items]
            if self.debiased and training_dropout:
                engagement = engagement * (
                    torch.rand_like(engagement) > 0.35
                ).to(engagement.dtype)
            scalars = torch.stack((
                engagement, self.fresh[items], self.underexplored[items]
            ), dim=-1)
            values = self.item(items) + content + self.scalar(scalars)
            if self.debiased:
                # DCNv2-style explicit content × age/engagement interaction.
                values = values + content * torch.tanh(
                    self.cross(torch.cat((content, scalars), dim=-1))
                )
            return values

        def forward(self, users, items, *, training_dropout: bool = False):
            user = self.user(users) + self.user_content(self.user_profiles[users])
            item = self.item_representation(
                items, training_dropout=training_dropout
            )
            return (user * item).sum(dim=-1) / math.sqrt(dimensions) + self.bias(items).squeeze(-1)

        def catalog_scores(self, users):
            items = torch.arange(data.items, device=users.device)
            item = self.item_representation(items)
            user = self.user(users) + self.user_content(self.user_profiles[users])
            return user @ item.T / math.sqrt(dimensions) + self.bias(items).T

    return Ranker()


def train_model(model, data, *, steps: int, seed: int, torch) -> dict:
    import numpy as np

    device = next(model.parameters()).device
    rng = np.random.default_rng(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1.5e-3, weight_decay=1e-4)
    losses = []
    model.train()
    for _ in range(steps):
        users = rng.integers(0, data.users, size=512)
        positives = np.asarray([
            data.train[user][rng.integers(0, len(data.train[user]))] for user in users
        ])
        negatives = rng.integers(0, data.items, size=len(users))
        user_tensor = torch.tensor(users, dtype=torch.long, device=device)
        positive_tensor = torch.tensor(positives, dtype=torch.long, device=device)
        negative_tensor = torch.tensor(negatives, dtype=torch.long, device=device)
        positive_scores = model(
            user_tensor, positive_tensor, training_dropout=model.debiased
        )
        negative_scores = model(
            user_tensor, negative_tensor, training_dropout=model.debiased
        )
        ranking = torch.nn.functional.softplus(negative_scores - positive_scores).mean()
        regularization = torch.zeros((), device=device)
        if model.debiased:
            fresh = model.fresh[positive_tensor] > 0
            if fresh.any() and (~fresh).any():
                # Align score centers for fresh and established positives.
                regularization = (
                    positive_scores[fresh].mean() - positive_scores[~fresh].mean()
                ).pow(2)
        loss = ranking + 0.02 * regularization
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:5])),
        "final_loss": float(np.mean(losses[-5:])),
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
    }


def fit_calibration(model, data, *, grouped: bool, seed: int, torch) -> dict:
    """Fit global or content-type-aware Platt scaling on balanced held-out pairs."""
    import numpy as np

    device = next(model.parameters()).device
    rng = np.random.default_rng(seed)
    values: dict[str, list[tuple[float, int]]] = {"all": []}
    if grouped:
        values |= {"fresh": [], "established": []}
    model.eval()
    with torch.inference_mode():
        fresh_items = np.flatnonzero(data.fresh)
        established_items = np.flatnonzero(~data.fresh)
        for user, target in enumerate(data.validation):
            cohort = fresh_items if data.fresh[target] else established_items
            negatives = rng.choice(cohort[cohort != target], 19, replace=False)
            items = np.asarray([target, *negatives])
            users = torch.full((len(items),), user, dtype=torch.long, device=device)
            item_tensor = torch.tensor(items, dtype=torch.long, device=device)
            scores = model(users, item_tensor).cpu().numpy()
            for item, score, label in zip(items, scores, [1] + [0] * 19):
                key = "fresh" if data.fresh[item] else "established"
                values["all"].append((float(score), label))
                if grouped:
                    values[key].append((float(score), label))

    def platt(rows):
        scores = np.asarray([row[0] for row in rows], dtype=np.float64)
        labels = np.asarray([row[1] for row in rows], dtype=np.float64)
        slope, intercept = 1.0, 0.0
        for _ in range(25):
            logits = np.clip(slope * scores + intercept, -20, 20)
            probabilities = 1 / (1 + np.exp(-logits))
            residual = probabilities - labels
            weight = probabilities * (1 - probabilities)
            gradient = np.asarray([
                np.mean(residual * scores) + 1e-3 * (slope - 1),
                np.mean(residual),
            ])
            hessian = np.asarray([
                [np.mean(weight * scores * scores) + 1e-3, np.mean(weight * scores)],
                [np.mean(weight * scores), np.mean(weight) + 1e-6],
            ])
            update = np.linalg.solve(hessian, gradient)
            slope, intercept = (np.asarray([slope, intercept]) - update).tolist()
        return {
            "scale": float(np.clip(slope, 0.05, 5.0)),
            "bias": float(intercept),
        }

    if grouped:
        return {key: platt(values[key]) for key in ("fresh", "established")}
    return {"all": platt(values["all"])}
