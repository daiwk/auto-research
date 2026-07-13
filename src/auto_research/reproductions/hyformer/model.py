from __future__ import annotations

from dataclasses import dataclass

from ..industrial_ranking import NeuralRankingConfig, require_backend


@dataclass(frozen=True)
class HyFormerConfig(NeuralRankingConfig):
    queries: int = 2
    non_sequence_tokens: int = 2


def build_model(kind: str, data, config: HyFormerConfig):
    torch, nn = require_backend()
    features = torch.tensor(data.item_features, dtype=torch.float32)
    item_count, feature_count = features.shape

    class LateFusion(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions, config.heads, 4 * config.dimensions,
                batch_first=True, norm_first=True, dropout=0.0,
            )
            self.sequence = nn.TransformerEncoder(layer, config.layers)
            self.dense = nn.Sequential(
                nn.Linear(feature_count, config.dimensions), nn.GELU(),
                nn.Linear(config.dimensions, config.dimensions),
            )
            self.output = nn.Linear(2 * config.dimensions, config.dimensions)
            self.register_buffer("features", features)

        def forward(self, history):
            sequence = self.sequence(self.item(history))[:, -1]
            dense = self.dense(self.features[history].mean(dim=1))
            user = self.output(torch.cat((sequence, dense), dim=-1))
            return user @ self.item.weight.T

    class QueryBoost(nn.Module):
        def __init__(self, token_count):
            super().__init__()
            self.token_count = token_count
            self.width = config.dimensions // token_count
            self.ffn = nn.ModuleList([
                nn.Sequential(
                    nn.Linear(config.dimensions, 2 * config.dimensions), nn.GELU(),
                    nn.Linear(2 * config.dimensions, config.dimensions),
                ) for _ in range(token_count)
            ])

        def forward(self, values):
            mixed = values.reshape(
                len(values), self.token_count, self.token_count, self.width
            ).transpose(1, 2).reshape(len(values), self.token_count, config.dimensions)
            refined = torch.stack(
                [network(mixed[:, token]) for token, network in enumerate(self.ffn)], dim=1
            )
            return values + refined

    class HyFormerLayer(nn.Module):
        def __init__(self):
            super().__init__()
            self.sequence = nn.Sequential(
                nn.LayerNorm(config.dimensions),
                nn.Linear(config.dimensions, 2 * config.dimensions), nn.SiLU(),
                nn.Linear(2 * config.dimensions, config.dimensions),
            )
            self.decoding = nn.MultiheadAttention(
                config.dimensions, config.heads, batch_first=True, dropout=0.0
            )
            self.boost = QueryBoost(config.queries + config.non_sequence_tokens)

        def forward(self, queries, sequence, non_sequence):
            sequence = sequence + self.sequence(sequence)
            decoded, _ = self.decoding(queries, sequence, sequence, need_weights=False)
            boosted = self.boost(torch.cat((queries + decoded, non_sequence), dim=1))
            return boosted[:, : config.queries], sequence

    class HyFormer(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.feature = nn.Linear(
                feature_count,
                config.non_sequence_tokens * config.dimensions,
            )
            global_width = feature_count + config.dimensions
            self.query = nn.ModuleList([
                nn.Linear(global_width, config.dimensions) for _ in range(config.queries)
            ])
            self.layers = nn.ModuleList([HyFormerLayer() for _ in range(config.layers)])
            self.item_projection = nn.Linear(
                config.dimensions + feature_count, config.dimensions
            )
            self.register_buffer("features", features)

        def forward(self, history):
            sequence = self.item(history)
            profile = self.features[history].mean(dim=1)
            non_sequence = self.feature(profile).reshape(
                len(history), config.non_sequence_tokens, config.dimensions
            )
            global_info = torch.cat((profile, sequence.mean(dim=1)), dim=-1)
            queries = torch.stack([projection(global_info) for projection in self.query], dim=1)
            for layer in self.layers:
                queries, sequence = layer(queries, sequence, non_sequence)
            user = queries.mean(dim=1)
            candidates = torch.cat((self.item.weight, self.features), dim=-1)
            return user @ self.item_projection(candidates).T

    if kind == "late_fusion":
        return LateFusion()
    if kind == "hyformer":
        return HyFormer()
    raise ValueError(f"unknown HyFormer kind: {kind}")
