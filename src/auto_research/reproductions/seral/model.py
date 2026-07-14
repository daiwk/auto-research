from __future__ import annotations

import copy
import random

import numpy as np

from ..industrial_batch import device_for, padded_histories, require_torch, training_pairs


def build_model(data):
    torch, nn = require_torch()
    features = torch.tensor(data.features)
    class SerenGPT(nn.Module):
        def __init__(self):
            super().__init__()
            self.register_buffer("features", features)
            self.item = nn.Embedding(data.item_count, 40)
            self.profile = nn.Sequential(nn.Linear(3 * data.features.shape[1], 80), nn.GELU(), nn.Linear(80, 40))
            self.content = nn.Linear(data.features.shape[1], 40, bias=False)
        def cognition(self, histories):
            values = self.features[histories]
            static = (values > 0).float().mean(1)
            short = values[:, -min(3, values.shape[1]):].mean(1)
            long = values.mean(1)
            return self.profile(torch.cat((static, short, long), -1))
        def forward(self, histories):
            user = self.cognition(histories)
            items = self.item.weight + self.content(self.features)
            return user @ items.T
    return SerenGPT()


def train_sft(data, seed, steps):
    torch, _ = require_torch()
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_model(data).to(device)
    rows = training_pairs(data)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    losses = []
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories = padded_histories([row[0] for row in batch], 20, device, torch)
        targets = torch.tensor([row[1] for row in batch], device=device)
        loss = torch.nn.functional.cross_entropy(model(histories), targets)
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:]))}


def align_ipo(model, data, seed, steps, tau=0.2):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    reference = copy.deepcopy(model).eval()
    rows = training_pairs(data)
    rng = random.Random(seed + 991)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    losses = []
    features = data.features
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]
        histories_raw = [row[0] for row in batch]
        winners = np.asarray([row[1] for row in batch])
        losers = []
        for history, winner in zip(histories_raw, winners):
            seen = features[list(history)].max(0)
            novelty = 1 - np.clip(features @ seen, 0, 1)
            relevance = features @ features[winner]
            teacher = 0.6 * relevance + 0.4 * novelty
            teacher[winner] = -np.inf
            losers.append(int(np.argmax(teacher)))
        histories = padded_histories(histories_raw, 20, device, torch)
        winners_t = torch.tensor(winners, device=device)
        losers_t = torch.tensor(losers, device=device)
        logp = torch.log_softmax(model(histories), -1)
        with torch.inference_mode():
            ref = torch.log_softmax(reference(histories), -1)
        margin = (logp.gather(1, winners_t[:, None]) - logp.gather(1, losers_t[:, None]) - ref.gather(1, winners_t[:, None]) + ref.gather(1, losers_t[:, None])).squeeze(1)
        ipo = ((margin - 1 / (2 * tau)) ** 2).mean()
        sft = torch.nn.functional.nll_loss(logp, winners_t)
        loss = ipo + 0.1 * sft
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "tau": tau}


def scorer(model):
    torch, _ = require_torch(); device = next(model.parameters()).device; model.eval()
    def score(history):
        with torch.inference_mode(): return model(padded_histories([history], 20, device, torch))[0].cpu().numpy()
    return score


def serendipity_at_10(data, score_function):
    values = []
    for user, history in enumerate(data.train):
        context = (*history, data.validation[user]); scores = score_function(context).copy(); scores[list(set(context))] = -np.inf
        top = np.argsort(-scores)[:10]; seen = data.features[list(context)].max(0)
        values.append(float(np.mean([1 - min(1.0, float(data.features[item] @ seen)) for item in top])))
    return float(np.mean(values))

