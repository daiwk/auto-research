from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import NeuralRankingConfig, require_backend, summarize_training


@dataclass(frozen=True)
class RankMixerConfig(NeuralRankingConfig):
    tokens: int = 4
    experts: int = 4
    negatives: int = 31
    sparsity_weight: float = 1e-4


def build_model(kind: str, data, config: RankMixerConfig):
    torch, nn = require_backend()
    item_count = data.item_count
    features = torch.tensor(data.item_features, dtype=torch.float32)
    feature_count = features.shape[1]
    head_width = config.dimensions // config.tokens

    class PerTokenFFN(nn.Module):
        def __init__(self, shared: bool):
            super().__init__()
            count = 1 if shared else config.tokens
            self.networks = nn.ModuleList([
                nn.Sequential(
                    nn.Linear(config.dimensions, 4 * config.dimensions), nn.GELU(),
                    nn.Linear(4 * config.dimensions, config.dimensions),
                ) for _ in range(count)
            ])
            self.shared = shared

        def forward(self, values):
            if self.shared:
                return self.networks[0](values)
            return torch.stack(
                [network(values[:, token]) for token, network in enumerate(self.networks)],
                dim=1,
            )

    class SparsePerTokenMoE(nn.Module):
        def __init__(self):
            super().__init__()
            self.routers = nn.ModuleList([
                nn.Linear(config.dimensions, config.experts) for _ in range(config.tokens)
            ])
            self.experts = nn.ModuleList([
                nn.ModuleList([
                    nn.Sequential(
                        nn.Linear(config.dimensions, 2 * config.dimensions), nn.GELU(),
                        nn.Linear(2 * config.dimensions, config.dimensions),
                    ) for _ in range(config.experts)
                ]) for _ in range(config.tokens)
            ])
            self.routing_penalty = None

        def forward(self, values):
            outputs, penalties = [], []
            for token in range(config.tokens):
                gates = torch.relu(self.routers[token](values[:, token]))
                if self.training:
                    dense_gates = torch.nn.functional.softplus(
                        self.routers[token](values[:, token])
                    )
                else:
                    top = torch.topk(gates, min(2, config.experts), dim=-1).indices
                    dense_gates = gates * torch.zeros_like(gates).scatter(-1, top, 1.0)
                expert_values = torch.stack(
                    [expert(values[:, token]) for expert in self.experts[token]], dim=1
                )
                outputs.append(
                    (expert_values * dense_gates.unsqueeze(-1)).sum(dim=1)
                    / dense_gates.sum(dim=-1, keepdim=True).clamp_min(1e-6)
                )
                penalties.append(gates.mean())
            self.routing_penalty = torch.stack(penalties).mean()
            return torch.stack(outputs, dim=1)

    class Block(nn.Module):
        def __init__(self):
            super().__init__()
            self.first_norm = nn.LayerNorm(config.dimensions)
            self.second_norm = nn.LayerNorm(config.dimensions)
            self.ffn = (
                SparsePerTokenMoE()
                if kind == "rankmixer_smoe"
                else PerTokenFFN(shared=kind == "shared_ffn")
            )

        def forward(self, values):
            # Paper Eq. 4: concatenate equal-index heads across heterogeneous tokens.
            mixed = values.reshape(
                len(values), config.tokens, config.tokens, head_width
            ).transpose(1, 2).reshape(len(values), config.tokens, config.dimensions)
            values = self.first_norm(values + mixed)
            return self.second_norm(values + self.ffn(values))

    class Ranker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.feature_projections = nn.ModuleList([
                nn.Linear(feature_count, config.dimensions) for _ in range(2)
            ])
            self.blocks = nn.ModuleList([Block() for _ in range(config.layers)])
            self.output = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, 1),
            )
            self.register_buffer("features", features)

        def pair_scores(self, history, candidates):
            batch, candidate_count = candidates.shape
            recent = self.item(history[:, -8:]).mean(dim=1)
            last = self.item(history[:, -1])
            profile = self.features[history].mean(dim=1)
            user_feature = self.feature_projections[0](profile)
            candidate_feature = self.feature_projections[1](self.features[candidates])
            candidate = self.item(candidates) + candidate_feature
            fixed = torch.stack((user_feature, recent, last), dim=1)
            fixed = fixed[:, None].expand(-1, candidate_count, -1, -1)
            values = torch.cat((fixed, candidate[:, :, None]), dim=2)
            values = values.reshape(batch * candidate_count, config.tokens, config.dimensions)
            for block in self.blocks:
                values = block(values)
            return self.output(values.mean(dim=1)).reshape(batch, candidate_count)

        def forward(self, history):
            candidates = torch.arange(item_count, device=history.device)[None].expand(len(history), -1)
            return self.pair_scores(history, candidates)

        def routing_penalty(self):
            penalties = [
                block.ffn.routing_penalty for block in self.blocks
                if isinstance(block.ffn, SparsePerTokenMoE)
            ]
            return sum(penalties) / len(penalties) if penalties else None

    return Ranker()


def train_model(kind: str, data, config: RankMixerConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = build_model(kind, data, config).to(device)
    from ..industrial_ranking import training_examples

    rows = training_examples(data.train, config.sequence_length)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = torch.tensor([row[0] for row in batch], dtype=torch.long, device=device)
        positives = torch.tensor([row[1] for row in batch], dtype=torch.long, device=device)
        negatives = torch.randint(
            0, data.item_count, (config.batch_size, config.negatives), device=device
        )
        candidates = torch.cat((positives[:, None], negatives), dim=1)
        logits = model.pair_scores(histories, candidates)
        labels = torch.zeros_like(logits)
        labels[:, 0] = 1.0
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        penalty = model.routing_penalty()
        if penalty is not None:
            loss = loss + config.sparsity_weight * penalty
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)
