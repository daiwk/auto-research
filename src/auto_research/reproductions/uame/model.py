from __future__ import annotations

import numpy as np


def pair_features(data, history, items: np.ndarray) -> np.ndarray:
    history = list(history[-8:])
    user = data.sequences.features[history].mean(axis=0)
    item = data.sequences.features[items]
    proxies = np.stack((
        data.transition[history].mean(axis=0)[items],
        data.cosine[history].mean(axis=0)[items],
        data.popularity[items],
    ), axis=1)
    return np.concatenate((np.repeat(user[None], len(items), axis=0), item, proxies), axis=1).astype(np.float32)


def build_training_pairs(data, seed: int, negatives: int = 3):
    rng = np.random.default_rng(seed)
    left, right, labels, conflicts = [], [], [], []
    for sequence in data.sequences.train:
        for end in range(2, len(sequence)):
            history, positive = sequence[max(0, end - 8):end], sequence[end]
            excluded = set(history) | {positive}
            pool = np.asarray([item for item in range(data.item_count) if item not in excluded])
            sampled = rng.choice(pool, min(negatives, len(pool)), replace=False)
            items = np.concatenate(([positive], sampled))
            features = pair_features(data, history, items)
            proxy = features[:, -3:]
            ranks = np.empty_like(proxy)
            for objective in range(proxy.shape[1]):
                order = np.argsort(-proxy[:, objective])
                ranks[order, objective] = np.arange(len(items))
            item_conflict = ranks.std(axis=1)
            for neg in range(1, len(items)):
                y = (proxy[0] > proxy[neg]).astype(np.float32)
                left.append(features[0]); right.append(features[neg]); labels.append(y)
                conflicts.append([float(item_conflict[0]), float(item_conflict[neg])])
    return tuple(np.asarray(row, dtype=np.float32) for row in (left, right, labels, conflicts))


def build_ranker(input_dim: int, uncertainty: bool, torch):
    nn = torch.nn
    output = 2 if uncertainty else 1
    return nn.Sequential(nn.Linear(input_dim, 64), nn.SiLU(), nn.Linear(64, 32), nn.SiLU(), nn.Linear(32, output))


def train_ranker(data, uncertainty: bool, seed: int, torch, steps: int = 100):
    left, right, labels, conflicts = build_training_pairs(data, seed)
    torch.manual_seed(seed)
    model = build_ranker(left.shape[1], uncertainty, torch)
    from auto_research.runtime import device_for
    device = device_for(torch); model.to(device)
    tensors = [torch.tensor(value, device=device) for value in (left, right, labels, conflicts)]
    optimizer = torch.optim.Adagrad(model.parameters(), lr=0.01)
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        index = torch.tensor(rng.choice(len(left), min(256, len(left)), replace=False), device=device)
        a, b, targets, conflict = (value[index] for value in tensors)
        out_a, out_b = model(a), model(b)
        if not uncertainty:
            probability = torch.sigmoid(out_a[:, 0] - out_b[:, 0]).clamp(1e-6, 1 - 1e-6)
            soft_target = targets.mean(-1)
            loss = torch.nn.functional.binary_cross_entropy(probability, soft_target)
        else:
            mu_a, logvar_a = out_a[:, 0], out_a[:, 1].clamp(-7, 5)
            mu_b, logvar_b = out_b[:, 0], out_b[:, 1].clamp(-7, 5)
            var_a, var_b = logvar_a.exp(), logvar_b.exp()
            z = (mu_a - mu_b) / (var_a + var_b + 1e-6).sqrt()
            probability = (0.5 * (1.0 + torch.erf(z / 2 ** 0.5))).clamp(1e-6, 1 - 1e-6)
            uncertainty_pair = var_a + var_b
            weight = 2.0 * (uncertainty_pair - uncertainty_pair.min()) / (uncertainty_pair.max() - uncertainty_pair.min() + 1e-6)
            ppr = torch.nn.functional.binary_cross_entropy(
                probability[:, None].expand_as(targets), targets, reduction="none"
            ).mean(-1)
            regularizer = torch.log1p(uncertainty_pair).mean()
            conflict_order = (conflict[:, 0] > conflict[:, 1]).float()
            auxiliary = torch.nn.functional.binary_cross_entropy_with_logits(logvar_a - logvar_b, conflict_order)
            loss = (weight * ppr).mean() + 0.02 * regularizer + 0.1 * auxiliary
        optimizer.zero_grad(set_to_none=True); loss.backward(); optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, {"initial_loss": float(np.mean(losses[:5])), "final_loss": float(np.mean(losses[-5:])), "pairs": len(left), "steps": steps, "device": device.type}


def scorer(model, data, history, torch):
    device = next(model.parameters()).device
    features = pair_features(data, history, np.arange(data.item_count))
    with torch.inference_mode():
        return model(torch.tensor(features, device=device))[:, 0].cpu().numpy()
