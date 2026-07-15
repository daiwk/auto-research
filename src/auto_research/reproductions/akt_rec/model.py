from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training


@dataclass(frozen=True)
class AKTConfig:
    dimensions: int = 48
    sequence_length: int = 20
    batch_size: int = 64
    steps: int = 180
    learning_rate: float = 5e-4
    transfer_weight_head: float = 0.05
    transfer_weight_tail: float = 0.20
    orthogonal_weight: float = 0.05


def build_model(data, item_codes, user_codes, config: AKTConfig, kind: str):
    torch, nn = require_backend()
    item_cluster = torch.tensor(item_codes[:, 0], dtype=torch.long)
    user_cluster = torch.tensor(user_codes[:, 0], dtype=torch.long)
    item_activity = torch.tensor(_activity(data.item_activity), dtype=torch.float32)
    user_activity = torch.tensor(_activity(data.user_activity), dtype=torch.float32)

    class AKTRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.kind = kind
            self.item_individual = nn.Embedding(data.item_count, config.dimensions)
            self.item_cluster_view = nn.Embedding(data.item_count, config.dimensions)
            self.user_individual = nn.Embedding(data.user_count, config.dimensions)
            self.user_cluster_view = nn.Embedding(data.user_count, config.dimensions)
            self.item_gate = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1))
            self.user_gate = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1))
            self.view_gate = nn.Sequential(nn.Linear(3, 16), nn.ReLU(), nn.Linear(16, 1))
            self.output = nn.Sequential(
                nn.Linear(3 * config.dimensions, 96), nn.ReLU(), nn.Linear(96, 1)
            )
            self.register_buffer("item_cluster", item_cluster)
            self.register_buffer("user_cluster", user_cluster)
            self.register_buffer("item_activity", item_activity)
            self.register_buffer("user_activity", user_activity)
            for embedding in (
                self.item_individual,
                self.item_cluster_view,
                self.user_individual,
                self.user_cluster_view,
            ):
                nn.init.normal_(embedding.weight, std=0.02)

        def fused_item(self, items):
            individual = self.item_individual(items)
            cluster = self.item_cluster_view(items)
            if self.kind == "online_base":
                return individual, cluster, individual
            gate = torch.sigmoid(self.item_gate(self.item_activity[items, None]))
            return individual, cluster, gate * cluster + (1.0 - gate) * individual

        def fused_user(self, users):
            individual = self.user_individual(users)
            cluster = self.user_cluster_view(users)
            if self.kind == "online_base":
                return individual, cluster, individual
            gate = torch.sigmoid(self.user_gate(self.user_activity[users, None]))
            return individual, cluster, gate * cluster + (1.0 - gate) * individual

        def forward(self, users, histories, candidates):
            _, candidate_cluster, candidate = self.fused_item(candidates)
            _, user_cluster, user = self.fused_user(users)
            _, history_cluster, history = self.fused_item(histories)
            weights = torch.softmax((history * candidate[:, None]).sum(-1) / config.dimensions**0.5, dim=-1)
            instance_history = (weights[..., None] * history).sum(1)
            instance = torch.cat((user, candidate, instance_history), dim=-1)
            same_cluster = self.item_cluster[histories] == self.item_cluster[candidates, None]
            cluster_weights = torch.softmax(
                (history_cluster * candidate_cluster[:, None]).sum(-1).masked_fill(~same_cluster, -1e4), dim=-1
            )
            fallback = ~same_cluster.any(dim=-1)
            cluster_weights = torch.where(fallback[:, None], weights, cluster_weights)
            cluster_history = (cluster_weights[..., None] * history_cluster).sum(1)
            cluster = torch.cat((user_cluster, candidate_cluster, cluster_history), dim=-1)
            if self.kind == "online_base":
                features = instance
            else:
                activity = torch.stack(
                    (self.user_activity[users], self.item_activity[candidates], self.user_activity[users] * self.item_activity[candidates]), dim=-1
                )
                gate = torch.sigmoid(self.view_gate(activity))
                features = gate * cluster + (1.0 - gate) * instance
            return self.output(features).squeeze(-1)

    return AKTRanker()


def train_model(kind, data, item_codes, user_codes, config: AKTConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model, device, torch = initialize(build_model(data, item_codes, user_codes, config, kind), seed)
    rows = data.train
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses, main_losses, transfer_losses, ortho_losses = [], [], [], []
    head_threshold = float(np.quantile(data.item_activity, 0.8))
    transfer_pairs = _transfer_pairs(item_codes[:, 0], data.item_activity, head_threshold)
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        users, histories, candidates, labels = _batch(batch, config, device, torch)
        logits = model(users, histories, candidates)
        main = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        transfer = logits.new_zeros(())
        ortho = logits.new_zeros(())
        if kind == "akt_rec":
            transfer = _asymmetric_transfer(model, transfer_pairs, rng, config, torch)
            item_i, item_c, _ = model.fused_item(candidates)
            user_i, user_c, _ = model.fused_user(users)
            ortho = _orthogonal(item_i, item_c, torch) + _orthogonal(user_i, user_c, torch)
        loss = main + transfer + config.orthogonal_weight * ortho
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        for bucket, value in ((losses, loss), (main_losses, main), (transfer_losses, transfer), (ortho_losses, ortho)):
            bucket.append(float(value.detach().cpu()))
    metrics = summarize_training(model, losses, device.type)
    metrics["loss_components"] = {
        "main": float(np.mean(main_losses[-20:])),
        "asymmetric_transfer": float(np.mean(transfer_losses[-20:])),
        "orthogonal": float(np.mean(ortho_losses[-20:])),
    }
    return model, metrics


def evaluate(model, rows, data, config: AKTConfig):
    from ..llm_rec_data import binary_auc

    torch, _ = require_backend()
    device = next(model.parameters()).device
    scores, labels, users, tail = [], [], [], []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), 256):
            batch = rows[start : start + 256]
            user, history, candidate, label = _batch(batch, config, device, torch)
            scores.extend(torch.sigmoid(model(user, history, candidate)).cpu().tolist())
            labels.extend(label.cpu().tolist())
            users.extend(user.cpu().tolist())
            tail.extend((data.item_activity[candidate.cpu().numpy()] < 10).tolist())
    per_user = []
    for user in sorted(set(users)):
        index = [i for i, value in enumerate(users) if value == user]
        per_user.append(binary_auc([labels[i] for i in index], [scores[i] for i in index]))
    tail_index = [i for i, value in enumerate(tail) if value]
    return {
        "auc": binary_auc(labels, scores),
        "gauc": float(np.mean(per_user)),
        "tail_auc": binary_auc([labels[i] for i in tail_index], [scores[i] for i in tail_index]),
    }


def _batch(rows, config, device, torch):
    histories = []
    for row in rows:
        recent = row.history[-config.sequence_length :]
        histories.append((recent[0],) * (config.sequence_length - len(recent)) + recent)
    return (
        torch.tensor([row.user for row in rows], device=device),
        torch.tensor(histories, device=device),
        torch.tensor([row.candidate for row in rows], device=device),
        torch.tensor([row.label for row in rows], dtype=torch.float32, device=device),
    )


def _asymmetric_transfer(model, pairs, rng, config, torch):
    if not pairs:
        return model.item_cluster_view.weight.sum() * 0.0
    selected = [group[rng.randrange(len(group))] for group in pairs]
    device = model.item_cluster_view.weight.device
    heads = torch.tensor([pair[0] for pair in selected], device=device)
    tails = torch.tensor([pair[1] for pair in selected], device=device)
    head = torch.nn.functional.normalize(model.item_cluster_view(heads), dim=-1)
    tail = torch.nn.functional.normalize(model.item_cluster_view(tails), dim=-1)
    labels = torch.arange(len(head), device=device)
    head_to_tail = torch.nn.functional.cross_entropy(head @ tail.detach().T / 0.1, labels)
    tail_to_head = torch.nn.functional.cross_entropy(tail @ head.detach().T / 0.1, labels)
    return config.transfer_weight_head * head_to_tail + config.transfer_weight_tail * tail_to_head


def _transfer_pairs(clusters, activity, threshold):
    groups = []
    for cluster in np.unique(clusters):
        members = np.flatnonzero(clusters == cluster)
        heads = [int(item) for item in members if activity[item] >= threshold]
        tails = [int(item) for item in members if activity[item] < threshold]
        if heads and tails:
            groups.append(
                tuple((heads[offset % len(heads)], tail) for offset, tail in enumerate(tails))
            )
    return tuple(groups)


def _orthogonal(individual, cluster, torch):
    cosine = torch.nn.functional.cosine_similarity(individual, cluster, dim=-1)
    return cosine.square().mean()


def _activity(values):
    values = np.log1p(np.asarray(values, dtype=np.float32))
    return values / max(float(values.max()), 1.0)
