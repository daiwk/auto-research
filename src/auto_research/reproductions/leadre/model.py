from __future__ import annotations
import copy
import random
import numpy as np
from ..industrial_batch import device_for, padded_histories, require_torch, training_pairs
from ..tiger.model import residual_kmeans


def ad_semantic_ids(data, seed):
    codes = residual_kmeans(data.features.copy(), 2, 8, seed, iterations=20)
    return np.column_stack((codes, np.arange(data.item_count) % 16)).astype(np.int64)


def build_model(data, codes):
    torch, nn = require_torch(); tokens = torch.tensor(codes, dtype=torch.long); sizes = (8, 8, 16)
    class LEADRE(nn.Module):
        def __init__(self):
            super().__init__(); self.register_buffer("codes", tokens); self.item = nn.Embedding(data.item_count, 48)
            self.intent = nn.Sequential(nn.Linear(3 * data.features.shape[1], 96), nn.GELU(), nn.Linear(96, 48))
            self.heads = nn.ModuleList([nn.Linear(48, size) for size in sizes]); self.semantic = nn.Linear(48, data.features.shape[1]); self.value = nn.Linear(48, 1)
            self.register_buffer("features", torch.tensor(data.features)); self.register_buffer("popularity", torch.tensor(data.popularity / max(data.popularity.max(), 1)))
        def state(self, histories):
            values = self.features[histories]; long = values.mean(1); short = values[:, -min(3, values.shape[1]):].mean(1); business = (values * self.popularity[histories, None]).mean(1)
            return self.intent(torch.cat((long, short, business), -1)) + self.item(histories[:, -1])
        def forward(self, histories):
            state = self.state(histories); logits = [head(state) for head in self.heads]
            score = sum(torch.log_softmax(value, -1)[:, self.codes[:, level]] for level, value in enumerate(logits))
            return score, logits, self.semantic(state), self.value(state).squeeze(-1)
    return LEADRE()


def train_sft(data, codes, seed, steps):
    torch, _ = require_torch(); torch.manual_seed(seed); device = device_for(torch); model = build_model(data, codes).to(device)
    rows = training_pairs(data); rng = random.Random(seed); optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3); losses = []
    features = torch.tensor(data.features, device=device); values = torch.tensor(data.popularity / max(data.popularity.max(), 1), device=device)
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]; histories = padded_histories([r[0] for r in batch], 20, device, torch); targets = torch.tensor([r[1] for r in batch], device=device)
        _, logits, semantic, business = model(histories); target_codes = model.codes[targets]
        loss = sum(torch.nn.functional.cross_entropy(value, target_codes[:, level]) for level, value in enumerate(logits))
        loss = loss + 0.2 * torch.nn.functional.binary_cross_entropy_with_logits(semantic, features[targets].clamp(0, 1)) + 0.1 * torch.nn.functional.mse_loss(torch.sigmoid(business), values[targets])
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:]))}


def align_dpo(model, data, seed, steps, beta=0.2):
    torch, _ = require_torch(); device = next(model.parameters()).device; reference = copy.deepcopy(model).eval(); rows = training_pairs(data); rng = random.Random(seed + 77); optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4); losses = []
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(48, len(rows)))]; histories = padded_histories([r[0] for r in batch], 20, device, torch); winners = torch.tensor([r[1] for r in batch], device=device); losers = torch.randint(0, data.item_count, winners.shape, device=device)
        score = model(histories)[0]; with_ref = reference(histories)[0].detach(); policy_margin = score.gather(1, winners[:, None]) - score.gather(1, losers[:, None]); ref_margin = with_ref.gather(1, winners[:, None]) - with_ref.gather(1, losers[:, None])
        loss = -torch.nn.functional.logsigmoid(beta * (policy_margin - ref_margin)).mean() + 0.1 * torch.nn.functional.cross_entropy(score, winners)
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:10])), "final_loss": float(np.mean(losses[-10:])), "beta": beta}


def scorer(model):
    torch, _ = require_torch(); device = next(model.parameters()).device; model.eval()
    def score(history):
        with torch.inference_mode(): return model(padded_histories([history], 20, device, torch))[0][0].cpu().numpy()
    return score

