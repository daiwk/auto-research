from __future__ import annotations

from auto_research.runtime import device_for

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
    optimizer: str = "adamw"
    interval_residual: int = 2
    auxiliary_weight: float = 0.15
    expansion: int = 3


def build_model(kind: str, data, config: RankMixerConfig):
    torch, nn = require_backend()
    item_count = data.item_count
    features = torch.tensor(data.item_features, dtype=torch.float32)
    feature_count = features.shape[1]
    head_width = config.dimensions // config.tokens
    supported = {
        "shared_ffn", "rankmixer_dense", "rankmixer_smoe",
        "tokenmixer_large", "zenith", "moi_mixer",
        "rankmixer_longer", "rankmixer_unimixer", "rankmixer_longer_unimixer",
        "rankmixer_whale", "rankmixer_tmallgs", "rankmixer_long_history",
        "rankmixer_ramp",
    }
    if kind not in supported:
        raise ValueError(f"unknown RankMixer evolution architecture: {kind}")
    if config.dimensions % config.tokens:
        raise ValueError("dimensions must be divisible by tokens")

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

    class PerTokenSwiGLU(nn.Module):
        def __init__(self):
            super().__init__()
            width = config.expansion * config.dimensions
            self.up = nn.ModuleList([nn.Linear(config.dimensions, width) for _ in range(config.tokens)])
            self.gate = nn.ModuleList([nn.Linear(config.dimensions, width) for _ in range(config.tokens)])
            self.down = nn.ModuleList([nn.Linear(width, config.dimensions) for _ in range(config.tokens)])
            for layer in self.down:
                nn.init.xavier_uniform_(layer.weight, gain=0.01)

        def forward(self, values):
            return torch.stack([
                self.down[token](torch.nn.functional.silu(self.gate[token](values[:, token])) * self.up[token](values[:, token]))
                for token in range(config.tokens)
            ], dim=1)

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

    class TokenMixerLargeBlock(nn.Module):
        """TokenMixer-Large mixing→head SwiGLU→reverting→token SwiGLU."""
        def __init__(self):
            super().__init__()
            self.pre_mix = nn.RMSNorm(config.dimensions)
            self.pre_token = nn.RMSNorm(config.dimensions)
            self.head_up = nn.ModuleList([nn.Linear(config.dimensions, config.expansion * config.dimensions) for _ in range(config.tokens)])
            self.head_gate = nn.ModuleList([nn.Linear(config.dimensions, config.expansion * config.dimensions) for _ in range(config.tokens)])
            self.head_down = nn.ModuleList([nn.Linear(config.expansion * config.dimensions, config.dimensions) for _ in range(config.tokens)])
            self.token_ffn = PerTokenSwiGLU()

        def forward(self, values):
            original = values
            mixed = self.pre_mix(values).reshape(
                len(values), config.tokens, config.tokens, head_width
            ).transpose(1, 2).reshape(len(values), config.tokens, config.dimensions)
            mixed = torch.stack([
                self.head_down[head](torch.nn.functional.silu(self.head_gate[head](mixed[:, head])) * self.head_up[head](mixed[:, head]))
                for head in range(config.tokens)
            ], dim=1) + mixed
            reverted = mixed.reshape(
                len(values), config.tokens, config.tokens, head_width
            ).transpose(1, 2).reshape(len(values), config.tokens, config.dimensions)
            reverted = original + reverted
            return reverted + self.token_ffn(self.pre_token(reverted))

    class ZenithBlock(nn.Module):
        """Prime-token RSA fusion followed by tokenwise SwiGLU boost."""
        def __init__(self):
            super().__init__()
            self.fusion = nn.Linear(config.dimensions, config.dimensions)
            self.residual = nn.Linear(config.dimensions, config.dimensions)
            self.first_norm = nn.LayerNorm(config.dimensions)
            self.second_norm = nn.LayerNorm(config.dimensions)
            self.boost = PerTokenSwiGLU()

        def forward(self, values):
            interaction = values @ values.transpose(1, 2) / config.dimensions**0.5
            fused = self.fusion(interaction @ values)
            values = self.first_norm(fused + self.residual(values))
            return self.second_norm(values + self.boost(values))

    class MultiOrderBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.ModuleList([nn.Linear(config.dimensions, config.dimensions) for _ in range(config.tokens)])
            self.quadratic = nn.ModuleList([nn.Linear(config.dimensions, config.dimensions) for _ in range(config.tokens)])
            self.norm = nn.LayerNorm(config.dimensions)

        def forward(self, values):
            outputs = []
            for token in range(config.tokens):
                x = values[:, token]
                outputs.append(self.linear[token](x) + self.quadratic[token](x * x))
            return self.norm(values + torch.stack(outputs, dim=1))

    class UniMixerBlock(nn.Module):
        def __init__(self):
            super().__init__()
            self.token_mix = nn.Linear(config.tokens, config.tokens, bias=False)
            self.channel = PerTokenSwiGLU()
            self.norm = nn.LayerNorm(config.dimensions)

        def forward(self, values):
            mixed = self.token_mix(values.transpose(1, 2)).transpose(1, 2)
            return self.norm(values + mixed + self.channel(values + mixed))

    class WhaleBlock(nn.Module):
        """Wukong multiplicative interaction followed by gated HSTU exchange."""

        def __init__(self):
            super().__init__()
            self.left = nn.Linear(config.dimensions, 2 * config.dimensions)
            self.right = nn.Linear(config.dimensions, 2 * config.dimensions)
            self.compress = nn.Linear(2 * config.dimensions, config.dimensions)
            self.attention = nn.MultiheadAttention(
                config.dimensions, config.tokens, batch_first=True, dropout=0.0
            )
            self.gate = nn.Linear(config.dimensions, 2 * config.dimensions)
            self.first_norm = nn.LayerNorm(config.dimensions)
            self.second_norm = nn.LayerNorm(config.dimensions)

        def forward(self, values):
            crossed = self.compress(self.left(values) * self.right(values))
            features = self.first_norm(values + crossed)
            causal = torch.triu(
                torch.ones(
                    config.tokens,
                    config.tokens,
                    dtype=torch.bool,
                    device=values.device,
                ),
                diagonal=1,
            )
            exchanged, _ = self.attention(
                features, features, features, attn_mask=causal
            )
            update, gate = self.gate(exchanged).chunk(2, dim=-1)
            return self.second_norm(
                features
                + torch.nn.functional.silu(update) * torch.sigmoid(gate)
            )

    class TMallGSBlock(nn.Module):
        """Field-wise QKV, distribution gate and per-token feed-forward path."""

        def __init__(self):
            super().__init__()
            self.q = nn.Parameter(
                torch.empty(config.tokens, config.dimensions, config.dimensions)
            )
            self.k = nn.Parameter(
                torch.empty(config.tokens, config.dimensions, config.dimensions)
            )
            self.v = nn.Parameter(
                torch.empty(config.tokens, config.dimensions, config.dimensions)
            )
            nn.init.xavier_uniform_(self.q)
            nn.init.xavier_uniform_(self.k)
            nn.init.xavier_uniform_(self.v)
            self.noise_gate = nn.Sequential(
                nn.Linear(config.dimensions, 1), nn.Sigmoid()
            )
            self.ffn = PerTokenSwiGLU()
            self.norm = nn.LayerNorm(config.dimensions)

        def forward(self, values):
            q = torch.einsum("btd,tdh->bth", values, self.q)
            k = torch.einsum("btd,tdh->bth", values, self.k)
            v = torch.einsum("btd,tdh->bth", values, self.v)
            attention = torch.softmax(
                q @ k.transpose(1, 2) / config.dimensions**0.5, dim=-1
            )
            gate = self.noise_gate(values)
            updated = self.norm(values + gate * (attention @ v))
            return updated + self.ffn(updated)

    class Ranker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.feature_projections = nn.ModuleList([
                nn.Linear(feature_count, config.dimensions) for _ in range(2)
            ])
            block_type = {
                "tokenmixer_large": TokenMixerLargeBlock,
                "zenith": ZenithBlock,
                "moi_mixer": MultiOrderBlock,
                "rankmixer_unimixer": UniMixerBlock,
                "rankmixer_longer_unimixer": UniMixerBlock,
                "rankmixer_whale": WhaleBlock,
                "rankmixer_tmallgs": TMallGSBlock,
            }.get(kind, Block)
            self.blocks = nn.ModuleList([block_type() for _ in range(config.layers)])
            self.output = nn.Sequential(
                nn.Linear(config.dimensions, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, 1),
            )
            self.register_buffer("features", features)
            self.auxiliary_logits = None
            self.alignment_logits = None
            self.restricted_logits = None
            self.personalized_logits = None
            if kind == "rankmixer_long_history":
                self.long_position = nn.Embedding(
                    config.sequence_length, config.dimensions
                )
                layer = nn.TransformerEncoderLayer(
                    config.dimensions,
                    config.tokens,
                    3 * config.dimensions,
                    batch_first=True,
                    norm_first=True,
                    dropout=0.0,
                )
                self.long_encoder = nn.TransformerEncoder(layer, 1)
                self.long_fusion = nn.Sequential(
                    nn.Linear(2 * config.dimensions, config.dimensions),
                    nn.SiLU(),
                    nn.LayerNorm(config.dimensions),
                )

        def pair_scores(self, history, candidates, mode=None):
            batch, candidate_count = candidates.shape
            if kind == "rankmixer_long_history":
                positions = torch.arange(history.shape[1], device=history.device)
                tokens = self.item(history) + self.long_position(positions)
                boundary = max(1, history.shape[1] - 4)
                cached = self.long_encoder(tokens[:, :boundary])[:, -1]
                runtime = tokens[:, -4:].mean(dim=1)
                recent = self.long_fusion(torch.cat((cached, runtime), dim=-1))
            elif "longer" in kind and history.shape[1] > 8:
                embedded = self.item(history)
                prefix, local = embedded[:, :-8], embedded[:, -8:]
                global_interest = prefix.mean(dim=1)
                recent = 0.5 * local.mean(dim=1) + 0.5 * global_interest
            else:
                recent = self.item(history[:, -8:]).mean(dim=1)
            last = self.item(history[:, -1])
            profile = self.features[history].mean(dim=1)
            user_feature = self.feature_projections[0](profile)
            public_profile = self.features.mean(dim=0, keepdim=True).expand(
                batch, -1
            )
            public_user_feature = self.feature_projections[0](public_profile)
            candidate_feature = self.feature_projections[1](self.features[candidates])
            candidate = self.item(candidates) + candidate_feature
            fixed = torch.stack((user_feature, recent, last), dim=1)
            fixed = fixed[:, None].expand(-1, candidate_count, -1, -1)
            values = torch.cat((fixed, candidate[:, :, None]), dim=2)
            values = values.reshape(batch * candidate_count, config.tokens, config.dimensions)
            public_fixed = torch.stack(
                (
                    public_user_feature,
                    public_user_feature,
                    public_user_feature,
                ),
                dim=1,
            )
            public_fixed = public_fixed[:, None].expand(
                -1, candidate_count, -1, -1
            )
            public_values = torch.cat(
                (public_fixed, candidate[:, :, None]), dim=2
            ).reshape(
                batch * candidate_count, config.tokens, config.dimensions
            )

            def score(encoded):
                anchor = encoded
                auxiliary = None
                for index, block in enumerate(self.blocks):
                    encoded = block(encoded)
                    if (
                        kind == "tokenmixer_large"
                        and config.interval_residual > 0
                        and index + 1 < len(self.blocks)
                        and (index + 1) % config.interval_residual == 0
                    ):
                        encoded = encoded + anchor
                        anchor = encoded
                    if index + 1 == max(1, len(self.blocks) // 2):
                        auxiliary = self.output(encoded.mean(dim=1)).reshape(
                            batch, candidate_count
                        )
                logits = self.output(encoded.mean(dim=1)).reshape(
                    batch, candidate_count
                )
                return logits, auxiliary

            personalized, auxiliary = score(values)
            restricted = None
            if mode == "restricted" or kind == "rankmixer_ramp":
                restricted, _ = score(public_values)
            if kind == "rankmixer_ramp":
                self.personalized_logits = personalized
                self.alignment_logits = restricted
                self.restricted_logits = restricted
                if self.training and mode is None:
                    availability = (
                        torch.arange(batch, device=history.device) % 5 != 0
                    )
                    logits = torch.where(
                        availability[:, None], personalized, restricted
                    )
                else:
                    logits = restricted if mode == "restricted" else personalized
            else:
                self.personalized_logits = None
                self.alignment_logits = None
                self.restricted_logits = None
                logits = restricted if mode == "restricted" else personalized
            self.auxiliary_logits = (
                auxiliary
                if kind in {"tokenmixer_large", "rankmixer_tmallgs"}
                else None
            )
            return logits

        def forward(self, history, mode=None):
            candidates = torch.arange(item_count, device=history.device)[None].expand(len(history), -1)
            return self.pair_scores(history, candidates, mode=mode)

        def routing_penalty(self):
            penalties = [block.ffn.routing_penalty for block in self.blocks if hasattr(block, "ffn") and isinstance(block.ffn, SparsePerTokenMoE)]
            return sum(penalties) / len(penalties) if penalties else None

    return Ranker()


def train_model(kind: str, data, config: RankMixerConfig, seed: int):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_model(kind, data, config).to(device)
    from ..industrial_ranking import training_examples

    rows = training_examples(data.train, config.sequence_length)
    optimizers = {
        "adamw": torch.optim.AdamW,
        "adam": torch.optim.Adam,
        "adagrad": torch.optim.Adagrad,
    }
    if config.optimizer not in optimizers:
        raise ValueError(f"unknown optimizer: {config.optimizer}")
    optimizer = optimizers[config.optimizer](model.parameters(), lr=config.learning_rate)
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
        if model.auxiliary_logits is not None:
            loss = loss + config.auxiliary_weight * torch.nn.functional.binary_cross_entropy_with_logits(model.auxiliary_logits, labels)
        if model.alignment_logits is not None:
            teacher = torch.sigmoid(model.personalized_logits.detach())
            alignment = torch.nn.functional.binary_cross_entropy_with_logits(
                model.alignment_logits, teacher
            )
            restricted = torch.nn.functional.binary_cross_entropy_with_logits(
                model.restricted_logits, labels
            )
            loss = loss + 0.15 * alignment + 0.25 * restricted
        penalty = model.routing_penalty()
        if penalty is not None:
            loss = loss + config.sparsity_weight * penalty
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)
