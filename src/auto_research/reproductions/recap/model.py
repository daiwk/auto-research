from __future__ import annotations

import copy
import numpy as np


def build_policy(categories: int, torch):
    nn = torch.nn
    class StreamingPolicy(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(categories + 1, 48)
            layer = nn.TransformerEncoderLayer(48, 4, 96, batch_first=True, norm_first=True)
            self.encoder = nn.TransformerEncoder(layer, 2)
            self.output = nn.Linear(48, categories)

        def forward(self, tokens):
            length = tokens.shape[1]
            mask = torch.triu(torch.full((length, length), float("-inf"), device=tokens.device), diagonal=1)
            return self.output(self.encoder(self.embedding(tokens), mask=mask)[:, -1])
    return StreamingPolicy()


def examples(data, width: int = 12):
    rows, targets = [], []
    pad = int(data.domains.max()) + 1
    for sequence in data.sequences.train:
        domains = data.domains[list(sequence)]
        for end in range(2, len(domains)):
            history = domains[max(0, end - width):end].tolist()
            rows.append([pad] * (width - len(history)) + history)
            targets.append(int(domains[end]))
    return np.asarray(rows, dtype=np.int64), np.asarray(targets, dtype=np.int64)


def train_sft(data, seed: int, torch, steps: int = 80):
    rows, targets = examples(data); categories = int(data.domains.max()) + 1
    torch.manual_seed(seed); model = build_policy(categories, torch)
    from auto_research.runtime import device_for
    device = device_for(torch); model.to(device)
    x, y = torch.tensor(rows, device=device), torch.tensor(targets, device=device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=8e-4)
    rng = np.random.default_rng(seed); losses = []
    for _ in range(steps):
        index = torch.tensor(rng.choice(len(rows), min(192, len(rows)), replace=False), device=device)
        loss = torch.nn.functional.cross_entropy(model(x[index]), y[index])
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step(); losses.append(float(loss.detach().cpu()))
    return model, (rows, targets), {"steps": steps, "initial_loss": float(np.mean(losses[:5])), "final_loss": float(np.mean(losses[-5:])), "device": device.type}


def train_evaluator(rows, targets, categories: int, seed: int, torch, steps: int = 60):
    nn = torch.nn
    class Evaluator(nn.Module):
        def __init__(self):
            super().__init__(); self.embedding = nn.Embedding(categories + 1, 32); self.item = nn.Embedding(categories, 32)
        def forward(self, history, candidate):
            mask = (history < categories).float().unsqueeze(-1)
            query = (self.embedding(history) * mask).sum(1) / mask.sum(1).clamp_min(1)
            return torch.nn.functional.cosine_similarity(query, self.item(candidate), dim=-1) * 4
    torch.manual_seed(seed + 7); evaluator = Evaluator()
    from auto_research.runtime import device_for
    device = device_for(torch); evaluator.to(device)
    x, y = torch.tensor(rows, device=device), torch.tensor(targets, device=device)
    optimizer = torch.optim.AdamW(evaluator.parameters(), lr=1e-3); rng = np.random.default_rng(seed + 7)
    for _ in range(steps):
        index = torch.tensor(rng.choice(len(rows), min(192, len(rows)), replace=False), device=device)
        negative = torch.randint(0, categories, (len(index),), device=device)
        logits = torch.cat((evaluator(x[index], y[index])[:, None], evaluator(x[index], negative)[:, None]), 1)
        loss = torch.nn.functional.cross_entropy(logits, torch.zeros(len(index), dtype=torch.long, device=device))
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
    evaluator.eval()
    return evaluator


def train_grpo(policy, reference, evaluator, rows, targets, categories: int, seed: int, torch, steps: int = 45):
    device = next(policy.parameters()).device; x = torch.tensor(rows, device=device); y = torch.tensor(targets, device=device)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=2e-4); rng = np.random.default_rng(seed + 11); stats = []
    reference.eval()
    for _ in range(steps):
        index = torch.tensor(rng.choice(len(rows), min(96, len(rows)), replace=False), device=device)
        context, target = x[index], y[index]
        logits = policy(context); distribution = torch.distributions.Categorical(logits=logits)
        samples = distribution.sample((4,)).T
        expanded = context[:, None].expand(-1, 4, -1).reshape(-1, context.shape[1])
        with torch.no_grad():
            reward = evaluator(expanded, samples.reshape(-1)).reshape(-1, 4)
            # Label-consistent feedback: retain the implicit positive signal.
            reward = reward + 0.5 * (samples == target[:, None]).float()
            advantage = (reward - reward.mean(1, keepdim=True)) / (reward.std(1, keepdim=True) + 1e-5)
            ref_logp = torch.log_softmax(reference(context), -1).gather(1, samples)
        logp = torch.log_softmax(logits, -1).gather(1, samples)
        ratio = torch.exp(logp - ref_logp)
        clipped = ratio.clamp(0.8, 1.2)
        loss = -torch.minimum(ratio * advantage, clipped * advantage).mean() + 0.02 * (logp - ref_logp).pow(2).mean()
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step(); stats.append(float(reward.mean().cpu()))
    return {"steps": steps, "mean_reward_first": float(np.mean(stats[:5])), "mean_reward_last": float(np.mean(stats[-5:])), "group_size": 4}


def bounded_profile(policy, data, history, torch, capacity: int = 4):
    categories = int(data.domains.max()) + 1; pad = categories; state = {}
    domains = data.domains[list(history)]
    for end in range(1, len(domains) + 1):
        chunk = domains[max(0, end - 12):end].tolist(); tokens = [pad] * (12 - len(chunk)) + chunk
        device = next(policy.parameters()).device
        with torch.inference_mode(): predicted = int(policy(torch.tensor([tokens], device=device)).argmax(-1).item())
        # Deterministic lifecycle: decay, refresh, merge and capacity eviction.
        state = {key: value * 0.92 for key, value in state.items() if value * 0.92 >= 0.08}
        state[predicted] = min(1.0, state.get(predicted, 0.0) + 0.35)
        while len(state) > capacity: state.pop(min(state, key=state.get))
    profile = np.zeros(categories, dtype=np.float64)
    for key, value in state.items(): profile[key] = value
    return profile
